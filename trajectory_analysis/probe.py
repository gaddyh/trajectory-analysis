from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from trajectory_analysis.models import FailedAction, FailureRecord, LLMProbeResult
from trajectory_analysis.signals import iter_messages
from trajectory_analysis.utils import make_arg_trace_summary, classify_arg_failure_type

load_dotenv()

ALLOWED_LABELS = {
    "CONTRADICTORY_SUMMARY",
    "PREMATURE_TOOL_EXECUTION",
    "ATTRIBUTE_PRIORITY_ERROR",
    "FILTER_MISAPPLICATION",
    "FIRST_MATCH_BIAS",
    "ORDER_SCOPE_CONFUSION",
    "USER_CONFIRMATION_INDUCED_DRIFT",
    "POLICY_OVERCOMPLIANCE",
    "MISSING_AGGREGATION",
    "UNKNOWN",
}

_LABEL_DESCRIPTIONS = """
- CONTRADICTORY_SUMMARY: The agent's own prior summary negated the expected value, yet the agent still used the wrong value.
- PREMATURE_TOOL_EXECUTION: A write action was executed before the user finished specifying all parameters.
- ATTRIBUTE_PRIORITY_ERROR: The agent selected based on the wrong attribute (e.g. price vs. model, color vs. size).
- FILTER_MISAPPLICATION: The agent applied the wrong filter or ignored a filter constraint from the user.
- FIRST_MATCH_BIAS: The agent picked the first item that partially matched instead of the best match.
- ORDER_SCOPE_CONFUSION: The agent acted on the wrong order (e.g. wrong order_id) despite the correct one being visible.
- USER_CONFIRMATION_INDUCED_DRIFT: A user confirmation or rephrasing caused the agent to switch to a wrong value.
- POLICY_OVERCOMPLIANCE: The agent over-applied a policy constraint, rejecting a valid action or choosing a restricted path unnecessarily.
- MISSING_AGGREGATION: The agent failed to include all required items (e.g. returned only one of two required items).
- UNKNOWN: No label fits the evidence.
"""

_OUTPUT_SCHEMA = """{
  "proposed_signal": "<one of the constrained labels>",
  "evidence_turn": <integer turn number or null>,
  "why_expected_correct": "<brief explanation>",
  "why_actual_chosen": "<brief explanation>",
  "deterministically_detectable": <true or false>,
  "confidence": <float 0.0–1.0>,
  "explanation": "<overall reasoning>"
}"""


def build_context_window(
    sim: dict,
    action: FailedAction,
    window_before: int = 6,
    window_after: int = 3,
    max_messages: int = 20,
) -> list[dict[str, Any]]:
    actual_turn = action.actual_call_turn

    ref_turns = [
        ref.turn
        for ref in (action.expected_arg_refs + action.actual_arg_refs)
        if ref.turn is not None
    ]

    if actual_turn is not None:
        earliest = min(ref_turns + [actual_turn - window_before], default=0)
        latest = actual_turn + window_after
    elif ref_turns:
        earliest = min(ref_turns)
        latest = max(ref_turns) + window_after
    else:
        earliest = 0
        latest = max_messages

    earliest = max(0, earliest)

    messages = []
    for turn, msg in iter_messages(sim):
        if turn < earliest:
            continue
        if turn > latest:
            break

        role = msg.get("role") or msg.get("sender") or msg.get("type") or "unknown"

        text_parts = []
        content = msg.get("content")
        if content and str(content).strip() and str(content).strip().lower() != "none":
            text_parts.append(str(content).strip())

        tool_calls = msg.get("tool_calls") or msg.get("tool_calls_raw") or []
        if isinstance(tool_calls, list):
            for tc in tool_calls:
                name = (
                    tc.get("name")
                    or tc.get("tool_name")
                    or (tc.get("function") or {}).get("name")
                )
                args = (
                    tc.get("arguments")
                    or tc.get("args")
                    or (tc.get("function") or {}).get("arguments")
                    or {}
                )
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        pass
                if name:
                    text_parts.append(f"[tool_call] {name}({json.dumps(args, ensure_ascii=False)})")

        tool_result = msg.get("tool_result") or msg.get("tool_output") or msg.get("result")
        if tool_result:
            result_str = json.dumps(tool_result, ensure_ascii=False) if not isinstance(tool_result, str) else tool_result
            text_parts.append(f"[tool_result] {result_str[:400]}")

        if not text_parts:
            continue

        messages.append({
            "turn": turn,
            "role": role,
            "text": "\n".join(text_parts),
        })

    if len(messages) > max_messages:
        messages = messages[-max_messages:]

    return messages


def build_probe_prompt(
    record: FailureRecord,
    action: FailedAction,
    context_window: list[dict[str, Any]],
    arg_failure_type: str,
    trace_pattern: str,
) -> str:
    arg_diff_lines = json.dumps(action.arg_diff, indent=2, ensure_ascii=False)

    context_lines = []
    for msg in context_window:
        marker = " <-- ACTUAL CALL TURN" if msg["turn"] == action.actual_call_turn else ""
        context_lines.append(f"[turn {msg['turn']} | {msg['role']}]{marker}\n{msg['text']}")

    context_str = "\n\n".join(context_lines) if context_lines else "(no context extracted)"

    prompt = f"""You are analyzing a single failed agent action in a customer service task.

Your job is to propose the most likely ROOT CAUSE SIGNAL from a constrained label set.

IMPORTANT GUARDRAILS:
- Do not invent new labels.
- Choose UNKNOWN if none fit.
- Base the label only on the provided context.

---

TASK INSTRUCTION:
{record.task_description or "(not available)"}

FAILED ACTION: {action.name}

EXPECTED ARGS:
{json.dumps(action.expected_args, indent=2, ensure_ascii=False)}

ACTUAL ARGS:
{json.dumps(action.actual_args, indent=2, ensure_ascii=False)}

ARG DIFF:
{arg_diff_lines}

ARG FAILURE TYPE: {arg_failure_type}
TRACE PATTERN: {trace_pattern}

---

RELEVANT CONVERSATION TURNS (around the failed call):

{context_str}

---

CONSTRAINED LABEL SET (choose exactly one):
{_LABEL_DESCRIPTIONS}

Return JSON matching this schema exactly:
{_OUTPUT_SCHEMA}
"""
    return prompt


def call_probe(prompt: str, model: str = "gpt-4o-mini") -> dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    raw = response.choices[0].message.content or "{}"
    return json.loads(raw)


def parse_probe_response(
    raw: dict,
    record: FailureRecord,
    action: FailedAction,
    arg_failure_type: str,
    trace_pattern: str,
) -> LLMProbeResult:
    deterministic_signals = [
        s for s in [action.contradiction_signal, action.execution_timing_signal]
        if s and s != "-"
    ]

    proposed = str(raw.get("proposed_signal") or "UNKNOWN").strip().upper()
    if proposed not in ALLOWED_LABELS:
        proposed = "UNKNOWN"

    evidence_turn = raw.get("evidence_turn")
    if evidence_turn is not None:
        try:
            evidence_turn = int(evidence_turn)
        except (TypeError, ValueError):
            evidence_turn = None

    try:
        confidence = float(raw.get("confidence") or 0.0)
        confidence = max(0.0, min(1.0, confidence))
    except (TypeError, ValueError):
        confidence = 0.0

    detectable = raw.get("deterministically_detectable")
    if isinstance(detectable, str):
        detectable = detectable.lower() in ("true", "yes", "1")
    else:
        detectable = bool(detectable)

    return LLMProbeResult(
        task_id=record.task_id,
        failed_action=action.name,
        arg_failure_type=arg_failure_type,
        trace_pattern=trace_pattern,
        deterministic_signals=deterministic_signals,
        llm_proposed_signal=proposed,
        evidence_turn=evidence_turn,
        why_expected_correct=str(raw.get("why_expected_correct") or ""),
        why_actual_chosen=str(raw.get("why_actual_chosen") or ""),
        deterministically_detectable=detectable,
        confidence=confidence,
        explanation=str(raw.get("explanation") or ""),
    )

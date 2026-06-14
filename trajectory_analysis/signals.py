import re
from typing import Optional

from trajectory_analysis.models import FailedAction, ContradictionEvidence


def iter_messages(sim: dict):
    for key in ("messages", "trajectory", "events", "steps"):
        value = sim.get(key)
        if isinstance(value, list):
            for i, msg in enumerate(value):
                if isinstance(msg, dict):
                    yield i, msg


NEGATIVE_CLAIM_PATTERNS: list[re.Pattern] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"there are no\b",
        r"there is no\b",
        r"no matching\b",
        r"could not find",
        r"couldn't find",
        r"not available",
        r"does not exist",
        r"don't have any",
        r"cannot find",
        r"unable to find",
        r"not found",
        r"no .{0,40}available",
    ]
]

LATE_DISAMBIGUATION_PATTERNS: list[re.Pattern] = [
    re.compile(p, re.I)
    for p in [
        r"\bactually\b",
        r"\bi meant\b",
        r"\bnot just\b",
        r"\balso\b",
        r"\bupdate the request\b",
        r"\bcan you update\b",
    ]
]

PLURALITY_PATTERNS: list[re.Pattern] = [
    re.compile(p, re.I)
    for p in [
        r"\btwo\b",
        r"\bboth\b",
        r"\bsecond\b",
        r"\banother\b",
        r"\badditional\b",
        r"\binclude both\b",
        r"\badd .* to .* request\b",
    ]
]


def _extract_sentence_around(text: str, match: re.Match) -> str:
    start = max(0, match.start() - 20)
    end = min(len(text), match.end() + 120)
    snippet = text[start:end].replace("\n", " ").strip()
    return snippet


def _extract_value_snippet(text: str, value: str) -> str:
    idx = text.find(value)
    if idx == -1:
        return ""
    start = max(0, idx - 60)
    end = min(len(text), idx + len(value) + 60)
    return text[start:end].replace("\n", " ").strip()


def detect_contradiction(
    sim: dict,
    action: FailedAction,
) -> Optional[ContradictionEvidence]:
    if action.actual_call_turn is None:
        return None
    if not action.arg_diff:
        return None

    first_diff = action.arg_diff[0]
    if first_diff.get("kind") == "missing_actual_call":
        return None

    expected = first_diff.get("expected")
    actual = first_diff.get("actual")

    if isinstance(expected, list) and isinstance(actual, list):
        exp_set = set(str(v) for v in expected)
        act_set = set(str(v) for v in actual)
        exp_only = exp_set - act_set
        act_only = act_set - exp_set
        expected_val = next(iter(exp_only), str(expected[0]) if expected else "")
        actual_val = next(iter(act_only), str(actual[0]) if actual else "")
    else:
        expected_val = str(expected or "")
        actual_val = str(actual or "")

    if not expected_val or not actual_val or expected_val == actual_val:
        return None

    preceding = _find_preceding_assistant_text(sim, action.actual_call_turn)
    if preceding is None:
        return None

    msg_turn, msg_text = preceding

    if expected_val not in msg_text:
        return None
    if actual_val not in msg_text:
        return None

    negative_claim = ""
    for pattern in NEGATIVE_CLAIM_PATTERNS:
        m = pattern.search(msg_text)
        if m:
            negative_claim = _extract_sentence_around(msg_text, m)
            break

    if not negative_claim:
        return None

    snippets = [
        s for s in [
            _extract_value_snippet(msg_text, expected_val),
            _extract_value_snippet(msg_text, actual_val),
        ]
        if s
    ]

    return ContradictionEvidence(
        signal="CONTRADICTORY_SUMMARY",
        turn=msg_turn,
        negative_claim=negative_claim,
        expected_value=expected_val,
        actual_value=actual_val,
        contradicting_snippets=snippets,
    )


def detect_premature_execution(sim: dict, action: FailedAction) -> str:
    if not action.is_write:
        return "-"

    if action.actual_call_turn is None:
        return "-"

    later_user_text = "\n".join(
        str(msg.get("content") or "").lower()
        for turn, msg in iter_messages(sim)
        if turn > action.actual_call_turn
        and msg.get("role") == "user"
        and isinstance(msg.get("content"), str)
    )

    if not later_user_text:
        return "-"

    has_correction = any(
        p.search(later_user_text)
        for p in LATE_DISAMBIGUATION_PATTERNS
    )

    has_plurality = any(
        p.search(later_user_text)
        for p in PLURALITY_PATTERNS
    )

    if has_correction and has_plurality:
        return "PREMATURE_TOOL_EXECUTION"

    return "-"


def _find_preceding_assistant_text(
    sim: dict,
    before_turn: int,
) -> Optional[tuple[int, str]]:
    result = None

    for turn, msg in iter_messages(sim):
        if turn >= before_turn:
            break

        role = msg.get("role") or msg.get("sender") or msg.get("type")
        if role != "assistant":
            continue

        content = msg.get("content")
        if not content or not str(content).strip() or str(content).strip().lower() == "none":
            continue

        result = (turn, str(content))

    return result

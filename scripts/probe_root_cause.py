from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from trajectory_analysis.utils import (
    build_failure_records,
    load_json,
    make_arg_trace_summary,
    classify_arg_failure_type,
)
from trajectory_analysis.probe import (
    build_context_window,
    build_probe_prompt,
    call_probe,
    parse_probe_response,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run LLM root-cause probes on single-failed-action cases."
    )
    parser.add_argument("results_json", help="Path to Tau2 results JSON")
    parser.add_argument(
        "--out",
        default="reports/root_cause_probes.jsonl",
        help="Output JSONL path (default: reports/root_cause_probes.jsonl)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Max number of cases to probe (default: 20)",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model to use (default: gpt-4o-mini)",
    )
    parser.add_argument(
        "--print-evidence",
        action="store_true",
        help="Print LLM evidence/explanation for each probe result",
    )
    args = parser.parse_args()

    data = load_json(args.results_json)
    records = build_failure_records(data)

    candidates = [
        r for r in records
        if r.reward != 1.0 and r.failed_action_count == 1
    ]

    if not candidates:
        print("No single-failed-action cases found.", file=sys.stderr)
        sys.exit(1)

    candidates = candidates[: args.limit]

    sims_by_task = {
        str(sim.get("task_id")): sim
        for sim in _iter_simulations(data)
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    label_counter: Counter = Counter()
    probed = 0

    with out_path.open("w", encoding="utf-8") as out_f:
        for record in candidates:
            action = record.failed_actions[0]
            sim = sims_by_task.get(str(record.task_id))

            if sim is None:
                print(
                    f"  [skip] task {record.task_id}: simulation not found",
                    file=sys.stderr,
                )
                continue

            arg_trace = make_arg_trace_summary(action)
            arg_failure_type = classify_arg_failure_type(
                arg_path=str(arg_trace["arg_path"]),
                trace_pattern=str(arg_trace["trace_pattern"]),
                failed_action_count=record.failed_action_count,
            )
            trace_pattern = str(arg_trace["trace_pattern"])

            context_window = build_context_window(sim, action)
            prompt = build_probe_prompt(
                record=record,
                action=action,
                context_window=context_window,
                arg_failure_type=arg_failure_type,
                trace_pattern=trace_pattern,
            )

            print(f"  probing task {record.task_id} ({action.name}) ...", end=" ", flush=True)
            try:
                raw = call_probe(prompt, model=args.model)
                result = parse_probe_response(
                    raw=raw,
                    record=record,
                    action=action,
                    arg_failure_type=arg_failure_type,
                    trace_pattern=trace_pattern,
                )
            except Exception as exc:
                print(f"ERROR: {exc}", file=sys.stderr)
                continue

            print(result.llm_proposed_signal)
            label_counter[result.llm_proposed_signal] += 1
            out_f.write(result.model_dump_json() + "\n")
            probed += 1

            if args.print_evidence:
                print()
                print("=" * 80)
                print(f"Task {result.task_id} | {result.failed_action}")
                print(f"Label: {result.llm_proposed_signal}")
                print(f"Evidence turn: {result.evidence_turn}")
                print(f"Confidence: {result.confidence}")
                print()
                print("Why expected was correct:")
                print(result.why_expected_correct)
                print()
                print("Why actual was chosen:")
                print(result.why_actual_chosen)
                print()
                print("Explanation:")
                print(result.explanation)
                print("=" * 80)

    print(f"\nWrote {probed} probe records to: {out_path}")
    _print_summary(label_counter)


def _iter_simulations(data: dict):
    for key in ("simulations", "results", "episodes"):
        if isinstance(data.get(key), list):
            yield from data[key]
            return
    for value in data.values():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "reward_info" in item:
                    yield item


def _print_summary(counter: Counter) -> None:
    if not counter:
        print("\nRoot Cause Probe Summary\n------------------------\n(no results)")
        return

    total = sum(counter.values())
    col_w = max(len(label) for label in counter) + 2

    print("\nRoot Cause Probe Summary")
    print("-" * (col_w + 10))
    for label, count in counter.most_common():
        pct = round(100 * count / total, 1)
        print(f"{label.ljust(col_w)} {str(count).rjust(3)}  ({pct}%)")
    print("-" * (col_w + 10))
    print(f"{'TOTAL'.ljust(col_w)} {str(total).rjust(3)}")


if __name__ == "__main__":
    main()

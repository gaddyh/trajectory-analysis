from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

from trajectory_analysis.utils import (
    build_failure_records,
    classify_arg_failure_type,
    load_json,
    make_arg_trace_summary,
    make_table_rows_from_records,
)

FAILURE_TYPE_COLS = [
    ("variant",      "WRONG_VARIANT_SELECTION"),
    ("source_item",  "WRONG_SOURCE_ITEM_SELECTION"),
    ("product",      "WRONG_PRODUCT_LOOKUP"),
    ("order",        "WRONG_ORDER_SELECTION"),
    ("payment",      "WRONG_PAYMENT_METHOD"),
    ("reason",       "WRONG_REASON"),
    ("missing",      "MISSING_ACTION"),
    ("multi",        "MULTI_FAILED_ACTIONS"),
    ("unknown",      "UNKNOWN"),
]

TRACE_PATTERN_COLS = [
    ("expected+actual",  "EXPECTED_AND_ACTUAL_OBSERVED"),
    ("expected_missing", "EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED"),
    ("missing_call",     "MISSING_ACTUAL_CALL"),
]


def _extract_model_label(data: dict, path: Path) -> str:
    try:
        return data["info"]["agent_info"]["llm"]
    except (KeyError, TypeError):
        return path.stem


def _cell(count: int, denom: int) -> str:
    if denom == 0:
        return "0"
    pct = round(100 * count / denom)
    return f"{count} ({pct}%)"


def build_model_row(label: str, data: dict) -> dict:
    records = build_failure_records(data)
    rows = make_table_rows_from_records(records)

    total = len(records)
    failed = sum(1 for r in records if r.reward != 1.0)
    passed = total - failed
    pass_rate = f"{round(100 * passed / total)}%" if total else "N/A"

    failure_counts: Counter = Counter()
    trace_counts: Counter = Counter()

    failed_rows = [row for row in rows if float(row.reward) != 1.0]

    for row in failed_rows:
        ft = row.arg_failure_type
        if ft and ft != "-":
            failure_counts[ft] += 1

        tp = row.trace_pattern
        if tp and tp not in ("-", "NO_ARG_DIFF", "UNKNOWN",
                             "NEITHER_OBSERVED", "EXPECTED_OBSERVED_ACTUAL_NOT_OBSERVED"):
            trace_counts[tp] += 1

    multi_count = failure_counts["MULTI_FAILED_ACTIONS"]
    unknown_count = failure_counts["UNKNOWN"]
    localized = failed - multi_count - unknown_count

    failure_row = {
        "model": label,
        "tasks": str(total),
        "pass_rate": pass_rate,
        "failed": str(failed),
    }
    for col, ft_key in FAILURE_TYPE_COLS:
        failure_row[col] = _cell(failure_counts[ft_key], failed)
    failure_row["localized"] = _cell(localized, failed)

    trace_row = {
        "model": label,
    }
    for col, tp_key in TRACE_PATTERN_COLS:
        trace_row[col] = _cell(trace_counts[tp_key], failed)

    return failure_row, trace_row


def _print_table(rows: list[dict], headers: list[str], title: str) -> None:
    if not rows:
        print(f"\n{title}: (no data)")
        return

    widths = {
        h: max(len(h), *(len(str(r.get(h, ""))) for r in rows))
        for h in headers
    }

    sep = "+-" + "-+-".join("-" * widths[h] for h in headers) + "-+"

    print(f"\n{title}")
    print(sep)
    print("| " + " | ".join(h.ljust(widths[h]) for h in headers) + " |")
    print(sep)
    for r in rows:
        print("| " + " | ".join(str(r.get(h, "")).ljust(widths[h]) for h in headers) + " |")
    print(sep)


def _write_markdown_table(
    rows: list[dict],
    headers: list[str],
    title: str,
    f,
) -> None:
    f.write(f"\n## {title}\n\n")
    f.write("| " + " | ".join(headers) + " |\n")
    f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
    for r in rows:
        f.write("| " + " | ".join(str(r.get(h, "")).replace("|", "\\|") for h in headers) + " |\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cross-model failure breakdown table for tool-using agent trajectories."
    )
    parser.add_argument(
        "simulations_dir",
        type=Path,
        help="Directory containing simulation JSON files",
    )
    parser.add_argument(
        "--domain",
        default="retail",
        help="Domain filter: only process files whose name contains this string (default: retail)",
    )
    parser.add_argument(
        "--md-out",
        default=None,
        help="Optional path for markdown output (e.g. reports/model_comparison.md)",
    )
    args = parser.parse_args()

    sim_dir = args.simulations_dir
    if not sim_dir.is_dir():
        print(f"Error: {sim_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    json_files = sorted(
        p for p in sim_dir.glob("*.json")
        if args.domain in p.name
    )

    if not json_files:
        print(f"No *{args.domain}*.json files found in {sim_dir}", file=sys.stderr)
        sys.exit(1)

    failure_rows = []
    trace_rows = []

    for path in json_files:
        print(f"  loading {path.name} ...", end=" ", flush=True)
        try:
            data = load_json(str(path))
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            continue

        label = _extract_model_label(data, path)
        try:
            fr, tr = build_model_row(label, data)
        except Exception as exc:
            print(f"ERROR building rows: {exc}", file=sys.stderr)
            continue

        failure_rows.append(fr)
        trace_rows.append(tr)
        print(f"ok  (tasks={fr['tasks']}, failed={fr['failed']})")

    failure_headers = (
        ["model", "tasks", "pass_rate", "failed"]
        + [col for col, _ in FAILURE_TYPE_COLS]
        + ["localized"]
    )
    trace_headers = ["model"] + [col for col, _ in TRACE_PATTERN_COLS]

    _print_table(failure_rows, failure_headers, "Model Comparison — Failure Type Breakdown")
    _print_table(trace_rows, trace_headers, "Model Comparison — Trace Pattern Breakdown")

    print("\nLegend — Failure Types")
    print("  variant       = WRONG_VARIANT_SELECTION")
    print("  source_item   = WRONG_SOURCE_ITEM_SELECTION")
    print("  product       = WRONG_PRODUCT_LOOKUP")
    print("  order         = WRONG_ORDER_SELECTION")
    print("  missing       = MISSING_ACTION")
    print("  multi         = MULTI_FAILED_ACTIONS")
    print("  localized     = failed - multi - unknown (arg-level localizer coverage)")
    print("  % denominator = failed tasks")
    print("\nLegend — Trace Patterns")
    print("  expected+actual  = EXPECTED_AND_ACTUAL_OBSERVED (correct answer was in context)")
    print("  expected_missing = EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED (model never grounded on correct value)")
    print("  missing_call     = MISSING_ACTUAL_CALL (action never executed)")

    if args.md_out:
        out = Path(args.md_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as f:
            _write_markdown_table(failure_rows, failure_headers, "Model Comparison — Failure Type Breakdown", f)
            _write_markdown_table(trace_rows, trace_headers, "Model Comparison — Trace Pattern Breakdown", f)
            f.write("\n## Legend\n\n")
            f.write("Failure type % = count / failed_tasks\n\n")
            for col, ft in FAILURE_TYPE_COLS:
                f.write(f"- `{col}` = {ft}\n")
            f.write("- `localized` = failed - multi - unknown (arg-level localizer coverage)\n")
            f.write("\nTrace pattern % = count / failed_tasks\n\n")
            for col, tp in TRACE_PATTERN_COLS:
                f.write(f"- `{col}` = {tp}\n")
        print(f"\nWrote markdown to: {out}")


if __name__ == "__main__":
    main()

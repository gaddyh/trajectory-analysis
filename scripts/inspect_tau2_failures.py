from trajectory_analysis.models import FailedAction, FailureRecord, FailureTableRow
import json
import argparse
from pathlib import Path

from trajectory_analysis.utils import load_json, build_failure_records, make_table_rows_from_records, print_console_table, write_markdown_table, print_failure_details

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results_json", help="Path to Tau2 results JSON")
    parser.add_argument("--task-id", default=None)
    parser.add_argument("--failed-only", action="store_true")
    parser.add_argument("--table", action="store_true")
    parser.add_argument("--md-out", default=None)
    args = parser.parse_args()

    data = load_json(args.results_json)

    records = build_failure_records(data)

    for record in records:
        if record.failed_action_count == 1:
            print_failure_details(record)

    if args.failed_only:
        records = [r for r in records if r.reward != 1.0]

    if args.task_id is not None:
        records = [r for r in records if str(r.task_id) == str(args.task_id)]

    if args.table:
        table_rows = make_table_rows_from_records(records)
        table_dicts = [r.model_dump() for r in table_rows]

        print_console_table(table_dicts)

        if args.md_out:
            write_markdown_table(table_dicts, args.md_out)
            print(f"\nWrote markdown table to: {args.md_out}")

        return

    print(json.dumps([r.model_dump() for r in records], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
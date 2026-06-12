from __future__ import annotations

import argparse
from pathlib import Path

from trajectory_analysis.compare import compare_expected_to_actual
from trajectory_analysis.loaders import load_task_and_simulation, load_task_ids
from trajectory_analysis.report import build_report, format_percent
from trajectory_analysis.trajectory import extract_trajectory
from collections import Counter

def print_summary(rows: list[dict[str, str]]) -> None:
    total = len(rows)
    passed = sum(1 for row in rows if row["result"] == "PASS")
    failed = total - passed

    success_rate = passed / total if total else 0.0

    failure_counts = Counter(
        row["failure"]
        for row in rows
        if row["failure"] != "-"
    )

    db_failed = sum(1 for row in rows if row["db"] == "0")
    nl_failed = sum(1 for row in rows if row["nl"] == "0")

    composite_fidelities = [
        parse_percent(row["comp_fid"])
        for row in rows
        if row["comp_fid"] != "N/A"
    ]

    avg_composite_fidelity = (
        sum(composite_fidelities) / len(composite_fidelities)
        if composite_fidelities
        else 0.0
    )

    min_composite_fidelity = (
        min(composite_fidelities)
        if composite_fidelities
        else 0.0
    )

    successful_low_composite_fidelity = sum(
        1
        for row in rows
        if row["result"] == "PASS"
        and row["comp_fid"] != "N/A"
        and parse_percent(row["comp_fid"]) < 1.0
    )

    failed_full_composite_fidelity = sum(
        1
        for row in rows
        if row["result"] == "FAIL"
        and row["comp_fid"] != "N/A"
        and parse_percent(row["comp_fid"]) == 1.0
    )

    total_extra = sum(int(row["extra"]) for row in rows)
    total_missing = sum(int(row["missing"]) for row in rows)

    benchmark_issues = sum(
        1
        for row in rows
        if row["benchmark_issue"] == "yes"
    )

    print("Dataset Summary")
    print("===============")
    print("")
    print(f"Tasks analyzed: {total}")
    print(f"Pass: {passed}")
    print(f"Fail: {failed}")
    print(f"Success rate: {success_rate:.1%}")

    print("")
    print("Failure Types")
    print("-------------")
    if failure_counts:
        for name, count in failure_counts.most_common():
            print(f"{name}: {count}")
    else:
        print("- None")

    print("")
    print("Reward Channels Failed")
    print("----------------------")
    print(f"DB: {db_failed}")
    print(f"NL_ASSERTION: {nl_failed}")

    print("")
    print("Behavioral Fidelity")
    print("-------------------")
    print(f"Average fidelity: {avg_composite_fidelity:.1%}")
    print(f"Min fidelity: {min_composite_fidelity:.1%}")
    print(
        "Successful runs with fidelity < 100%: "
        f"{successful_low_composite_fidelity}"
    )
    print(
        "Failed runs with fidelity = 100%: "
        f"{failed_full_composite_fidelity}"
    )

    print("")
    print("Trajectory Variation")
    print("--------------------")
    print(f"Total extra actions: {total_extra}")
    print(f"Total missing actions: {total_missing}")

    print("")
    print("Potential Benchmark Issues")
    print("--------------------------")
    print(f"Flagged: {benchmark_issues}")


def parse_percent(value: str) -> float:
    return float(value.rstrip("%")) / 100.0

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run compact trajectory analysis over N Tau2 tasks."
    )
    parser.add_argument(
        "results_path",
        type=Path,
        help="Path to Tau2 results.json",
    )
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="First task id to analyze",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of tasks to analyze",
    )

    args = parser.parse_args()

    rows = []


    task_ids = load_task_ids(args.results_path)

    selected_task_ids = task_ids[
        args.start : args.start + args.limit
    ]

    for task_id in selected_task_ids:
        task, simulation = load_task_and_simulation(
            args.results_path,
            task_id=task_id,
        )

        trajectory = extract_trajectory(simulation)
        comparison = compare_expected_to_actual(task, trajectory)
        report = build_report(task, simulation, trajectory, comparison)

        rows.append(build_row(report))

    print_table(rows)
    print("")
    print_summary(rows)


def build_row(report) -> dict[str, str]:
    db = report.reward_breakdown.get("DB")
    nl = report.reward_breakdown.get("NL_ASSERTION")

    return {
        "task": report.task_id,
        "result": "PASS" if report.success else "FAIL",
        "db": format_score(db),
        "nl": format_score(nl),
        "failure": report.primary_failure or "-",
        "action_fid": format_percent(report.action_fidelity),
        "arg_fid": format_percent(report.argument_fidelity),
        "comp_fid": format_percent(report.composite_fidelity),
        "reads": f"{report.matched_reads}/{report.expected_reads}",
        "writes": f"{report.matched_writes}/{report.expected_writes}",
        "extra": str(report.extra_actions),
        "missing": str(report.missing_actions),
        "benchmark_issue": "yes" if report.potential_benchmark_issue else "-",
        "root_cause": shorten(report.root_cause or "-", 60),
    }


def format_score(value) -> str:
    if value is None:
        return "-"
    return f"{value:.0f}"


def shorten(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def print_table(rows: list[dict[str, str]]) -> None:
    if not rows:
        print("No rows.")
        return

    headers = list(rows[0].keys())

    widths = {
        header: max(
            len(header),
            *(len(row[header]) for row in rows),
        )
        for header in headers
    }

    header_line = " | ".join(
        header.ljust(widths[header])
        for header in headers
    )

    separator = "-+-".join(
        "-" * widths[header]
        for header in headers
    )

    print(header_line)
    print(separator)

    for row in rows:
        print(
            " | ".join(
                row[header].ljust(widths[header])
                for header in headers
            )
        )


if __name__ == "__main__":
    main()
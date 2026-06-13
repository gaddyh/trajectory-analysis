#!/usr/bin/env python3
import json
import argparse
from pathlib import Path

WRITE_PREFIXES = (
    "modify_",
    "exchange_",
    "return_",
    "cancel_",
)


def is_write_action(action_name):
    return action_name.startswith(WRITE_PREFIXES)

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def shorten(text, max_len=80):
    text = str(text or "").replace("\n", " ").strip()
    return text if len(text) <= max_len else text[: max_len - 3] + "..."


def make_table_rows(rows):
    table_rows = []

    for row in rows:
        task = row["task"] or {}
        sim = row["simulation"]

        action_checks = sim.get("action_checks", [])
        nl_runtime = sim.get("nl_assertions_runtime", [])
        communicate_info = task.get("communicate_info", [])

        failed_actions = [
            (c.get("action") or {}).get("name", "")
            for c in action_checks
            if not c.get("action_match")
        ]

        failed_assertions = [
            c.get("nl_assertion", "")
            for c in nl_runtime
            if not c.get("met")
        ]

        failed_action_names = [
            (c.get("action") or {}).get("name", "")
            for c in action_checks
            if not c.get("action_match")
        ]

        failed_action_count = len(failed_action_names)

        failed_write_count = sum(
            1
            for name in failed_action_names
            if is_write_action(name)
        )

        pattern = failure_pattern(
            [c for c in action_checks if not c.get("action_match")],
            [c for c in nl_runtime if not c.get("met")],
        )

        table_rows.append({
            "task": str(sim.get("task_id")),
            "reward": str(sim.get("reward")),
            "pattern": pattern,

            "failed_action_count": failed_action_count,
            "failed_write_count": failed_write_count,

            "failed_actions": shorten(", ".join(failed_action_names) or "-"),
            "failed_assertions": shorten("; ".join(failed_assertions) or "-"),
            "communicate_info": shorten(", ".join(str(x) for x in communicate_info) or "-"),
            "task_short": shorten(task.get("reason_for_call"), 90),
        })

    return table_rows


def print_console_table(table_rows):
    headers = [
        "task",
        "reward",
        "pattern",
        "failed_action_count",
        "failed_write_count",
        "failed_actions",
        "failed_assertions",
        "communicate_info",
    ]

    widths = {
        h: max(len(h), *(len(str(r[h])) for r in table_rows))
        for h in headers
    }

    def line():
        return "+-" + "-+-".join("-" * widths[h] for h in headers) + "-+"

    print(line())
    print("| " + " | ".join(h.ljust(widths[h]) for h in headers) + " |")
    print(line())

    for r in table_rows:
        print("| " + " | ".join(str(r[h]).ljust(widths[h]) for h in headers) + " |")

    print(line())


def write_markdown_table(table_rows, path):
    headers = [
        "task",
        "reward",
        "pattern",
        "failed_action_count",
        "failed_write_count",
        "failed_actions",
        "failed_assertions",
        "communicate_info",
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")

        for r in table_rows:
            f.write("| " + " | ".join(str(r[h]).replace("|", "\\|") for h in headers) + " |\n")


def iter_tasks(data):
    for task in data.get("tasks", []):
        yield task

def failure_pattern(failed_action_checks, failed_nl_assertions):
    has_action_failure = len(failed_action_checks) > 0
    has_nl_failure = len(failed_nl_assertions) > 0

    if has_action_failure and has_nl_failure:
        return "ACTION_AND_NL"
    if has_action_failure:
        return "ACTION_ONLY"
    if has_nl_failure:
        return "NL_ONLY"
    return "UNKNOWN"

def iter_simulations(data):
    # Tau2 result files usually keep simulations under one of these shapes
    for key in ("simulations", "results", "episodes"):
        if isinstance(data.get(key), list):
            yield from data[key]
            return

    # Fallback: search top-level list-ish values
    for value in data.values():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "reward_info" in item:
                    yield item


def summarize_task(task):
    criteria = task.get("evaluation_criteria") or {}

    return {
        "task_id": task.get("id"),
        "reason_for_call": (
            task.get("user_scenario", {})
            .get("instructions", {})
            .get("reason_for_call")
        ),
        "expected_actions": [
            {
                "name": a.get("name"),
                "arguments": a.get("arguments"),
                "compare_args": a.get("compare_args"),
            }
            for a in criteria.get("actions", []) or []
        ],
        "communicate_info": criteria.get("communicate_info") or [],
        "nl_assertions": criteria.get("nl_assertions") or [],
        "reward_basis": criteria.get("reward_basis") or [],
        "env_assertions": criteria.get("env_assertions") or [],
        "issues": task.get("issues") or [],
    }


def summarize_simulation(sim):
    reward_info = sim.get("reward_info") or {}

    nl_checks = reward_info.get("nl_assertions") or reward_info.get("nl_checks") or []
    communication_checks = (
        reward_info.get("communication_checks")
        or reward_info.get("communicate_info")
        or []
    )

    return {
        "simulation_id": sim.get("id") or sim.get("simulation_id"),
        "task_id": sim.get("task_id"),
        "reward": reward_info.get("reward"),
        "db": {
            "db_match": (reward_info.get("db_check") or {}).get("db_match"),
            "db_reward": (reward_info.get("db_check") or {}).get("db_reward"),
        },
        "nl_assertion_reward": reward_info.get("nl_assertion_reward"),
        "nl_assertions_runtime": nl_checks,
        "communication_checks_runtime": communication_checks,
        "action_checks": reward_info.get("action_checks") or [],
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results_json", help="Path to Tau2 results JSON")
    parser.add_argument("--task-id", default=None)
    parser.add_argument("--failed-only", action="store_true")
    
    parser.add_argument("--table", action="store_true")
    parser.add_argument("--md-out", default=None)
    args = parser.parse_args()

    data = load_json(args.results_json)

    tasks_by_id = {
        str(t.get("id")): summarize_task(t)
        for t in iter_tasks(data)
    }

    rows = []

    for sim in iter_simulations(data):
        sim_summary = summarize_simulation(sim)
        task_id = str(sim_summary["task_id"])

        if args.task_id is not None and task_id != str(args.task_id):
            continue

        if args.failed_only and sim_summary["reward"] == 1.0:
            continue

        rows.append({
            "task": tasks_by_id.get(task_id),
            "simulation": sim_summary,
        })

    if args.table:
        table_rows = make_table_rows(rows)
        print_console_table(table_rows)

        if args.md_out:
            write_markdown_table(table_rows, args.md_out)
            print(f"\nWrote markdown table to: {args.md_out}")

        return

    if args.pretty:
        for row in rows:
            task = row["task"] or {}
            sim = row["simulation"]

            task_id = sim.get("task_id")
            reward = sim.get("reward")
            reason_for_call = task.get("reason_for_call")

            communicate_info = task.get("communicate_info", [])
            nl_assertions = task.get("nl_assertions", [])
            nl_assertions_runtime = sim.get("nl_assertions_runtime", [])
            action_checks = sim.get("action_checks", [])

            failed_action_checks = [
                check for check in action_checks
                if not check.get("action_match")
            ]

            failed_nl_assertions = [
                check for check in nl_assertions_runtime
                if not check.get("met")
            ]

            pattern = failure_pattern(
                failed_action_checks,
                failed_nl_assertions,
            )

            print("=" * 80)
            print(f"Task ID: {task_id}")
            print(f"Reward: {reward}")

            print("\nFailure Pattern")
            print("---------------")
            print(pattern)

            if reason_for_call:
                print("\nTask")
                print("----")
                print(reason_for_call)

            print("\nFailed Action Checks")
            print("--------------------")

            if failed_action_checks:
                for check in failed_action_checks:
                    action = check.get("action") or {}
                    print(action.get("name"))
                    print(f"args={action.get('arguments')}")
                    print()
            else:
                print("None")

            print("\nExpected Communication")
            print("----------------------")

            if communicate_info:
                for info in communicate_info:
                    print(f"communicate_info: {info}")
            else:
                print("communicate_info: []")

            if nl_assertions:
                for assertion in nl_assertions:
                    print(f"assertion: {assertion}")
            else:
                print("assertion: []")

            print("\nRuntime Evaluation")
            print("------------------")

            if nl_assertions_runtime:
                for check in nl_assertions_runtime:
                    status = "PASS" if check.get("met") else "FAIL"

                    print(f"\n[{status}]")
                    print(check.get("nl_assertion"))

                    justification = check.get("justification")
                    if justification:
                        print(f"Reason: {justification}")
            else:
                print("No runtime NL assertions.")

            passed = sum(1 for x in nl_assertions_runtime if x.get("met"))
            failed = sum(1 for x in nl_assertions_runtime if not x.get("met"))

            print("\nSummary")
            print("-------")
            print(f"Assertions Passed: {passed}")
            print(f"Assertions Failed: {failed}")
            print()

    else:
        print(json.dumps(rows, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
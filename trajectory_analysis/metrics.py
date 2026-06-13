from trajectory_analysis.models import FailedAction, FailureRecord, FailureTableRow
import json
import argparse
from pathlib import Path

WRITE_PREFIXES = (
    "modify_",
    "exchange_",
    "return_",
    "cancel_",
)

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

def iter_tasks(data):
    for task in data.get("tasks", []):
        yield task

def is_write_action(action_name):
    return action_name.startswith(WRITE_PREFIXES)

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def shorten(text, max_len=80):
    text = str(text or "").replace("\n", " ").strip()
    return text if len(text) <= max_len else text[: max_len - 3] + "..."


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

def build_failure_records(data: dict) -> list[FailureRecord]:
    tasks_by_id = {
        str(t.get("id")): summarize_task(t)
        for t in iter_tasks(data)
    }

    records: list[FailureRecord] = []

    for sim in iter_simulations(data):
        sim_summary = summarize_simulation(sim)
        task_id = str(sim_summary["task_id"])
        task = tasks_by_id.get(task_id) or {}

        action_checks = sim_summary.get("action_checks", [])
        nl_runtime = sim_summary.get("nl_assertions_runtime", [])

        failed_action_checks = [
            c for c in action_checks
            if not c.get("action_match")
        ]

        failed_nl_assertions = [
            c for c in nl_runtime
            if not c.get("met")
        ]

        failed_actions = []
        for check in failed_action_checks:
            action = check.get("action") or {}
            name = action.get("name") or ""

            failed_actions.append(
                FailedAction(
                    name=name,
                    is_write=is_write_action(name),
                )
            )

        records.append(
            FailureRecord(
                task_id=int(task_id),
                reward=float(sim_summary.get("reward") or 0.0),
                pattern=failure_pattern(
                    failed_action_checks,
                    failed_nl_assertions,
                ),
                failed_action_count=len(failed_action_checks),
                failed_write_count=sum(a.is_write for a in failed_actions),
                failed_actions=failed_actions,
                failed_assertions=[
                    c.get("nl_assertion") or ""
                    for c in failed_nl_assertions
                ],
                communicate_info=[
                    str(x) for x in task.get("communicate_info", [])
                ],
                task_description=task.get("reason_for_call") or "",
            )
        )

    return records


def failure_record_to_table_row(record: FailureRecord) -> FailureTableRow:
    return FailureTableRow(
        task=str(record.task_id),
        reward=str(record.reward),
        pattern=record.pattern,
        failed_action_count=record.failed_action_count,
        failed_write_count=record.failed_write_count,
        failed_actions=shorten(
            ", ".join(a.name for a in record.failed_actions) or "-"
        ),
        failed_assertions=shorten(
            "; ".join(record.failed_assertions) or "-"
        ),
        communicate_info=shorten(
            ", ".join(record.communicate_info) or "-"
        ),
    )


def make_table_rows_from_records(
    records: list[FailureRecord],
) -> list[FailureTableRow]:
    return [
        failure_record_to_table_row(record)
        for record in records
    ]


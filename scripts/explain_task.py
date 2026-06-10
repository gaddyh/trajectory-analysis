from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from trajectory_analysis.loaders import load_task


READ_TOOL_HINTS = (
    "get_",
    "find_",
    "list_",
)

WRITE_TOOL_HINTS = (
    "return_",
    "exchange_",
    "modify_",
    "cancel_",
    "transfer_",
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Explain what a Tau2 task appears to require."
    )
    parser.add_argument(
        "results_path",
        type=Path,
        help="Path to Tau2 results.json",
    )
    parser.add_argument(
        "--task-id",
        default="0",
        help="Task id to explain",
    )

    args = parser.parse_args()

    task = load_task(args.results_path, task_id=args.task_id)
    explanation = explain_task(task)

    print(format_task_explanation(explanation))


def explain_task(task: Any) -> dict[str, Any]:
    expected_actions = task.expected_actions

    reads = []
    writes = []
    other_actions = []

    for action in expected_actions:
        name = action.get("name", "")
        item = {
            "action_id": action.get("action_id"),
            "name": name,
            "arguments": action.get("arguments", {}),
        }

        if is_read_tool(name):
            reads.append(item)
        elif is_write_tool(name):
            writes.append(item)
        else:
            other_actions.append(item)

    repeated_actions = find_repeated_actions(expected_actions)

    return {
        "task_id": task.task_id,
        "reward_basis": task.reward_basis,
        "expected_action_count": len(expected_actions),
        "read_count": len(reads),
        "write_count": len(writes),
        "other_action_count": len(other_actions),
        "reads": reads,
        "writes": writes,
        "other_actions": other_actions,
        "repeated_actions": repeated_actions,
        "communication_requirements": extract_communication_requirements(task),
    }


def is_read_tool(name: str) -> bool:
    return name.startswith(READ_TOOL_HINTS)


def is_write_tool(name: str) -> bool:
    return name.startswith(WRITE_TOOL_HINTS)


def action_signature(action: dict[str, Any]) -> tuple[str, str]:
    name = action.get("name", "")
    args = action.get("arguments", {})
    return name, stable_repr(args)


def stable_repr(value: Any) -> str:
    if isinstance(value, dict):
        items = sorted((k, stable_repr(v)) for k, v in value.items())
        return "{" + ", ".join(f"{k}: {v}" for k, v in items) + "}"

    if isinstance(value, list):
        return "[" + ", ".join(stable_repr(v) for v in value) + "]"

    return repr(value)


def find_repeated_actions(
    expected_actions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    signatures = [action_signature(action) for action in expected_actions]
    counts = Counter(signatures)

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)

    for action in expected_actions:
        signature = action_signature(action)
        if counts[signature] > 1:
            grouped[signature].append(action)

    repeated = []

    for (name, args_repr), actions in grouped.items():
        repeated.append(
            {
                "name": name,
                "arguments_repr": args_repr,
                "count": len(actions),
                "action_ids": [
                    action.get("action_id")
                    for action in actions
                ],
            }
        )

    return repeated


def extract_communication_requirements(task: Any) -> list[str]:
    requirements: list[str] = []

    for item in task.communicate_info:
        requirements.append(f"communicate_info: {item}")

    for assertion in task.nl_assertions:
        requirements.append(f"nl_assertion: {assertion}")

    return requirements


def format_task_explanation(explanation: dict[str, Any]) -> str:
    lines: list[str] = []

    lines.append("Task explanation")
    lines.append("================")
    lines.append("")
    lines.append(f"Task ID: {explanation['task_id']}")
    lines.append(f"Reward basis: {explanation['reward_basis']}")
    lines.append("")
    lines.append("Expected action structure")
    lines.append("-------------------------")
    lines.append(f"Total expected actions: {explanation['expected_action_count']}")
    lines.append(f"Read actions: {explanation['read_count']}")
    lines.append(f"Write actions: {explanation['write_count']}")
    lines.append(f"Other actions: {explanation['other_action_count']}")

    lines.append("")
    lines.append("Expected reads")
    lines.append("--------------")
    for action in explanation["reads"]:
        lines.append(
            f"- {action['action_id']} "
            f"{action['name']} args={action['arguments']}"
        )

    lines.append("")
    lines.append("Expected writes")
    lines.append("---------------")
    for action in explanation["writes"]:
        lines.append(
            f"- {action['action_id']} "
            f"{action['name']} args={action['arguments']}"
        )

    if explanation["other_actions"]:
        lines.append("")
        lines.append("Other expected actions")
        lines.append("----------------------")
        for action in explanation["other_actions"]:
            lines.append(
                f"- {action['action_id']} "
                f"{action['name']} args={action['arguments']}"
            )

    lines.append("")
    lines.append("Repeated expected actions")
    lines.append("-------------------------")

    if explanation["repeated_actions"]:
        for repeated in explanation["repeated_actions"]:
            lines.append(
                f"- {repeated['name']} "
                f"count={repeated['count']} "
                f"action_ids={repeated['action_ids']} "
                f"args={repeated['arguments_repr']}"
            )
    else:
        lines.append("- None")

    lines.append("")
    lines.append("Communication requirements")
    lines.append("--------------------------")

    if explanation["communication_requirements"]:
        for requirement in explanation["communication_requirements"]:
            lines.append(f"- {requirement}")
    else:
        lines.append(
            "- Not loaded yet. Extend Task model with nl_assertions "
            "and communicate_info."
        )

    return "\n".join(lines)


if __name__ == "__main__":
    main()
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from trajectory_analysis.models import Task, Trajectory, TrajectoryStep


@dataclass
class ArgumentMismatch:
    key: str
    expected: Any
    actual: Any


@dataclass
class MatchedAction:
    expected_idx: int
    actual_idx: int
    tool_name: str
    argument_mismatches: list[ArgumentMismatch]

    @property
    def exact_match(self) -> bool:
        return len(self.argument_mismatches) == 0


@dataclass
class TrajectoryComparison:
    matched_actions: list[MatchedAction]
    missing_expected_actions: list[dict[str, Any]]
    extra_actual_steps: list[TrajectoryStep]

    @property
    def expected_count(self) -> int:
        return (
            len(self.matched_actions)
            + len(self.missing_expected_actions)
        )

    @property
    def actual_count(self) -> int:
        return (
            len(self.matched_actions)
            + len(self.extra_actual_steps)
        )

    @property
    def exact_action_matches(self) -> int:
        return sum(1 for action in self.matched_actions if action.exact_match)


def compare_expected_to_actual(
    task: Task,
    trajectory: Trajectory,
) -> TrajectoryComparison:
    """
    Compare expected Tau2 actions against the observed tool-call trajectory.

    Matching strategy:
    - Preserve expected action order.
    - Only match actual steps with the same tool name.
    - When multiple actual steps have the same tool name, choose the one
      with the fewest argument mismatches.
    - This avoids greedily matching the wrong repeated read action.
    """
    expected_actions = task.expected_actions
    actual_steps = trajectory.steps

    matched_actions: list[MatchedAction] = []
    missing_expected_actions: list[dict[str, Any]] = []
    used_actual_indices: set[int] = set()

    search_from = 0

    for expected_idx, expected_action in enumerate(expected_actions):
        match_idx = find_best_matching_step(
            expected_action=expected_action,
            actual_steps=actual_steps,
            used_actual_indices=used_actual_indices,
            search_from=search_from,
        )

        if match_idx is None:
            missing_expected_actions.append(expected_action)
            continue

        actual_step = actual_steps[match_idx]
        used_actual_indices.add(match_idx)
        search_from = match_idx + 1

        argument_mismatches = compare_arguments(
            expected_action.get("arguments", {}),
            actual_step.arguments,
        )

        matched_actions.append(
            MatchedAction(
                expected_idx=expected_idx,
                actual_idx=actual_step.step_idx,
                tool_name=expected_action.get("name", ""),
                argument_mismatches=argument_mismatches,
            )
        )

    extra_actual_steps = [
        step
        for idx, step in enumerate(actual_steps)
        if idx not in used_actual_indices
    ]

    return TrajectoryComparison(
        matched_actions=matched_actions,
        missing_expected_actions=missing_expected_actions,
        extra_actual_steps=extra_actual_steps,
    )


def find_best_matching_step(
    expected_action: dict[str, Any],
    actual_steps: list[TrajectoryStep],
    used_actual_indices: set[int],
    search_from: int,
) -> int | None:
    expected_tool = expected_action.get("name")
    expected_args = expected_action.get("arguments", {})

    candidates: list[tuple[int, int]] = []

    for actual_idx in range(search_from, len(actual_steps)):
        if actual_idx in used_actual_indices:
            continue

        actual_step = actual_steps[actual_idx]

        if actual_step.tool_name != expected_tool:
            continue

        mismatches = compare_arguments(
            expected_args,
            actual_step.arguments,
        )

        candidates.append((len(mismatches), actual_idx))

    if not candidates:
        return None

    candidates.sort(key=lambda item: (item[0], item[1]))

    return candidates[0][1]

def compare_arguments(
    expected: dict[str, Any],
    actual: dict[str, Any],
) -> list[ArgumentMismatch]:
    """
    Shallow argument comparison.

    Important:
    - This compares expected keys only.
    - Extra actual keys are ignored for now.
    - List ordering is preserved for now.
    """
    mismatches: list[ArgumentMismatch] = []

    for key, expected_value in expected.items():
        actual_value = actual.get(key)

        if actual_value != expected_value:
            mismatches.append(
                ArgumentMismatch(
                    key=key,
                    expected=expected_value,
                    actual=actual_value,
                )
            )

    return mismatches


def format_comparison(comparison: TrajectoryComparison) -> str:
    lines: list[str] = []

    lines.append("Trajectory comparison")
    lines.append("=====================")
    lines.append("")

    lines.append(
        f"Matched expected actions: "
        f"{len(comparison.matched_actions)}/{comparison.expected_count}"
    )
    lines.append(
        f"Exact argument matches: "
        f"{comparison.exact_action_matches}/{len(comparison.matched_actions)}"
    )
    lines.append(
        f"Extra actual actions: {len(comparison.extra_actual_steps)}"
    )
    lines.append(
        f"Missing expected actions: {len(comparison.missing_expected_actions)}"
    )

    lines.append("")
    lines.append("Matched actions:")
    for match in comparison.matched_actions:
        status = "PASS" if match.exact_match else "ARG_MISMATCH"
        lines.append(
            f"- expected[{match.expected_idx}] "
            f"actual[{match.actual_idx}] "
            f"{match.tool_name}: {status}"
        )

        for mismatch in match.argument_mismatches:
            lines.append(f"  - {mismatch.key}")
            lines.append(f"    expected: {mismatch.expected}")
            lines.append(f"    actual:   {mismatch.actual}")

    if comparison.extra_actual_steps:
        lines.append("")
        lines.append("Extra actual actions:")
        for step in comparison.extra_actual_steps:
            lines.append(
                f"- actual[{step.step_idx}] "
                f"turn={step.turn_idx} "
                f"{step.tool_name} args={step.arguments}"
            )

    if comparison.missing_expected_actions:
        lines.append("")
        lines.append("Missing expected actions:")
        for action in comparison.missing_expected_actions:
            lines.append(
                f"- {action.get('name')} "
                f"args={action.get('arguments', {})}"
            )

    return "\n".join(lines)
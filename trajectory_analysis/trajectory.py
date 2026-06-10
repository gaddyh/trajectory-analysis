from __future__ import annotations

from trajectory_analysis.models import Simulation, Trajectory, TrajectoryStep


def extract_trajectory(simulation: Simulation) -> Trajectory:
    """
    Extract the observed agent trajectory from raw simulation messages.

    This intentionally ignores user/assistant text and focuses only on
    assistant tool calls, because the first trajectory view is about
    agent actions.
    """
    steps: list[TrajectoryStep] = []

    for message in simulation.messages:
        if message.get("role") != "assistant":
            continue

        tool_calls = message.get("tool_calls") or []

        for tool_call in tool_calls:
            steps.append(
                TrajectoryStep(
                    step_idx=len(steps),
                    turn_idx=message.get("turn_idx"),
                    tool_name=tool_call.get("name", ""),
                    arguments=tool_call.get("arguments", {}),
                )
            )

    return Trajectory(steps=steps)


def format_trajectory(trajectory: Trajectory) -> str:
    """
    Render a trajectory as a simple numbered list for inspection.
    """
    if not trajectory.steps:
        return "No tool calls found."

    lines: list[str] = []

    for step in trajectory.steps:
        lines.append(
            f"{step.step_idx + 1}. "
            f"turn={step.turn_idx} "
            f"tool={step.tool_name} "
            f"args={step.arguments}"
        )

    return "\n".join(lines)
from dataclasses import dataclass
from typing import Any

@dataclass
class Task:
    task_id: str

    expected_actions: list[dict[str, Any]]

    reward_basis: list[str]

    communicate_info: list[str]
    nl_assertions: list[str]

@dataclass
class Simulation:
    simulation_id: str

    reward: float

    messages: list[dict]

    action_checks: list[dict]

    reward_breakdown: dict[str, float]
    nl_assertions: list[dict[str, Any]]
    communicate_checks: list[dict[str, Any]]

@dataclass
class TrajectoryReport:
    task_id: str
    simulation_id: str

    success: bool
    reward: float

    reward_breakdown: dict[str, float]

    matched_actions: int
    expected_actions: int
    exact_argument_matches: int

    extra_actions: int
    missing_actions: int

    failure_channel: str | None

    nl_assertions: list[dict[str, Any]]
    communicate_checks: list[dict[str, Any]]

    primary_failure: str | None
    root_cause: str | None
    impact: str | None

    summary: str
    executive_summary: str | None = None

@dataclass
class TrajectoryStep:
    step_idx: int
    turn_idx: int | None
    tool_name: str
    arguments: dict[str, Any]


@dataclass
class Trajectory:
    steps: list[TrajectoryStep]


@dataclass
class TaskExplanation:
    task_id: str

    user_goals: list[str]

    information_requirements: list[str]

    expected_reads: list[str]

    expected_writes: list[str]

    communication_requirements: list[str]

    reward_basis: list[str]
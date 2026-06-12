import json
from pathlib import Path
from typing import Any

from trajectory_analysis.models import Simulation, Task


def load_results(path: str | Path) -> dict[str, Any]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Results file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_task_ids(results_path: str | Path) -> list[str]:
    data = load_results(results_path)

    return [
        str(task["id"])
        for task in data.get("tasks", [])
    ]
    
def load_task(results_path: str | Path, task_id: str = "0") -> Task:
    data = load_results(results_path)

    tasks = data.get("tasks", [])
    task_raw = next((t for t in tasks if str(t.get("id")) == str(task_id)), None)

    if task_raw is None:
        raise ValueError(f"Task id {task_id!r} not found in {results_path}")

    evaluation = task_raw.get("evaluation_criteria", {})

    return Task(
        task_id=str(task_raw["id"]),
        expected_actions=evaluation.get("actions", []),
        reward_basis=evaluation.get("reward_basis", []),
        communicate_info=evaluation.get("communicate_info", []),
        nl_assertions=evaluation.get("nl_assertions", []),
    )


def load_simulation(results_path: str | Path, task_id: str = "0") -> Simulation:
    data = load_results(results_path)

    simulations = data.get("simulations", [])
    sim_raw = next(
        (s for s in simulations if str(s.get("task_id")) == str(task_id)),
        None,
    )

    if sim_raw is None:
        raise ValueError(f"Simulation for task id {task_id!r} not found in {results_path}")

    reward_info = sim_raw.get("reward_info", {})

    return Simulation(
        simulation_id=str(sim_raw["id"]),
        reward=float(reward_info.get("reward", 0.0)),
        reward_breakdown=reward_info.get("reward_breakdown", {}),
        nl_assertions=reward_info.get("nl_assertions", []),
        communicate_checks=reward_info.get("communicate_checks", []),
        messages=sim_raw.get("messages", []),
        action_checks=reward_info.get("action_checks", []),
    )


def load_task_and_simulation(
    results_path: str | Path,
    task_id: str = "0",
) -> tuple[Task, Simulation]:
    return (
        load_task(results_path, task_id=task_id),
        load_simulation(results_path, task_id=task_id),
    )
#!/usr/bin/env python3
import json
import argparse
from pathlib import Path


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def iter_tasks(data):
    for task in data.get("tasks", []):
        yield task


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
    parser.add_argument("--pretty", action="store_true")
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

    if args.pretty:
        for row in rows:
            task = row["task"] or {}
            sim = row["simulation"]

            print("=" * 80)
            print(f"Task ID: {sim.get('task_id')}")
            print(f"Simulation ID: {sim.get('simulation_id')}")
            print(f"Reward: {sim.get('reward')}")
            print(f"DB match: {sim['db'].get('db_match')}")
            print(f"DB reward: {sim['db'].get('db_reward')}")
            print()

            print("Reason for call:")
            print(task.get("reason_for_call"))
            print()

            print("Expected actions:")
            for i, a in enumerate(task.get("expected_actions", []), 1):
                print(f"{i}. {a['name']} args={a['arguments']}")
            print()

            print("communicate_info:")
            print(task.get("communicate_info"))
            print()

            print("NL assertions:")
            for assertion in task.get("nl_assertions", []):
                print(f"- {assertion}")
            print()

            print("Runtime NL / communication checks:")
            print(json.dumps({
                "nl_assertions_runtime": sim.get("nl_assertions_runtime"),
                "communication_checks_runtime": sim.get("communication_checks_runtime"),
            }, indent=2, ensure_ascii=False))
            print()
    else:
        print(json.dumps(rows, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
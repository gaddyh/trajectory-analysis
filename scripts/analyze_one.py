import argparse

from trajectory_analysis.compare import (
    compare_expected_to_actual,
    format_comparison,
)
from trajectory_analysis.loaders import load_task_and_simulation
from trajectory_analysis.report import build_report, format_report, build_executive_summary
from trajectory_analysis.trajectory import extract_trajectory, format_trajectory

def run(path, task_id):
    task, simulation = load_task_and_simulation(
        path,
        task_id=task_id,
    )

    trajectory = extract_trajectory(simulation)
    comparison = compare_expected_to_actual(task, trajectory)
    report = build_report(task, simulation, trajectory, comparison)

    print("Expected actions:")
    for i, action in enumerate(task.expected_actions, start=1):
        print(f"{i}. {action['name']} args={action['arguments']}")

    print("\nActual trajectory:")
    print(format_trajectory(trajectory))

    print("\n")
    print(format_comparison(comparison))

    print("\n")
    report.executive_summary = build_executive_summary(
        simulation=simulation,
        report=report,
    )
    print(format_report(report))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", default="2", help="Task ID to analyze")
    parser.add_argument(
        "--path",
        default="data/raw/simulations/baseline_retail_100/results.json",
        help="Path to results JSON",
    )
    args = parser.parse_args()
    run(args.path, args.task_id)

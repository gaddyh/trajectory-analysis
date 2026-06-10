from __future__ import annotations

from trajectory_analysis.compare import TrajectoryComparison
from trajectory_analysis.models import Simulation, Task, Trajectory, TrajectoryReport

def determine_failure_channel(
    simulation: Simulation,
) -> str | None:

    if simulation.reward == 1.0:
        return None

    breakdown = simulation.reward_breakdown

    failed = [
        channel
        for channel, score in breakdown.items()
        if score < 1.0
    ]

    if not failed:
        return "unknown"

    return ", ".join(failed)

def build_report(
    task: Task,
    simulation: Simulation,
    trajectory: Trajectory,
    comparison: TrajectoryComparison,
) -> TrajectoryReport:
    """
    Build the first stable report object.

    This report intentionally contains only observable facts:
    outcome, match counts, and a short summary.
    """
    success = simulation.reward == 1.0

    summary = build_summary(
        simulation=simulation,
        comparison=comparison,
    )

    failure_channel = determine_failure_channel(
        simulation
    )

    primary_failure, root_cause, impact = diagnose_failure(
        simulation=simulation,
        comparison=comparison,
    )

    return TrajectoryReport(
        task_id=task.task_id,
        simulation_id=simulation.simulation_id,
        success=success,
        reward=simulation.reward,
        reward_breakdown=simulation.reward_breakdown,
        matched_actions=len(comparison.matched_actions),
        expected_actions=comparison.expected_count,
        exact_argument_matches=comparison.exact_action_matches,
        extra_actions=len(comparison.extra_actual_steps),
        missing_actions=len(comparison.missing_expected_actions),
        failure_channel=failure_channel,
        summary=summary,
        nl_assertions=simulation.nl_assertions,
        communicate_checks=simulation.communicate_checks,
        primary_failure=primary_failure,
        root_cause=root_cause,
        impact=impact,
    )


def build_summary(
    simulation: Simulation,
    comparison: TrajectoryComparison,
) -> str:
    if simulation.reward == 1.0:
        return (
            "The simulation succeeded according "
            "to all reward channels."
        )

    if simulation.reward_breakdown.get("DB") == 1.0:
        return (
            "Database state matched expected outcome, "
            "but one or more communication / NL "
            "requirements failed."
        )

    if simulation.reward_breakdown.get("NL_ASSERTION") == 1.0:
        return (
            "Communication requirements passed, "
            "but database state did not match "
            "expected outcome."
        )
        
    if comparison.missing_expected_actions:
        return (
            "The simulation failed and at least one expected action "
            "was missing from the observed trajectory."
        )

    mismatched = [
        match
        for match in comparison.matched_actions
        if not match.exact_match
    ]

    if mismatched:
        first = mismatched[0]
        keys = ", ".join(
            mismatch.key for mismatch in first.argument_mismatches
        )

        return (
            "The simulation failed after matching the expected tool sequence, "
            f"but arguments diverged at `{first.tool_name}` "
            f"for: {keys}."
        )

    if comparison.extra_actual_steps:
        return (
            "The simulation failed despite matching expected actions; "
            "the observed trajectory also contained extra actions."
        )

    return (
        "The simulation failed, but the first-pass comparison did not "
        "localize a clear trajectory divergence."
    )

def format_report(report: TrajectoryReport) -> str:
    lines: list[str] = []

    lines.append("Trajectory report")
    lines.append("=================")
    lines.append("")
    lines.append(f"Task ID: {report.task_id}")
    lines.append(f"Simulation ID: {report.simulation_id}")
    lines.append(f"Success: {report.success}")
    lines.append(f"Reward: {report.reward}")

    lines.append("")
    lines.append("Executive Summary")
    lines.append("-----------------")
    lines.append(report.executive_summary)

    lines.append("")
    lines.append("Reward Breakdown")
    lines.append("----------------")

    if report.reward_breakdown:
        for name, value in report.reward_breakdown.items():
            lines.append(f"{name}: {value}")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("Failure Channel")
    lines.append("---------------")
    lines.append(str(report.failure_channel))

    lines.append("")
    lines.append("Diagnosis")
    lines.append("---------")
    lines.append(f"Primary failure: {report.primary_failure}")
    lines.append(f"Root cause: {report.root_cause}")
    lines.append(f"Impact: {report.impact}")

    if report.nl_assertions:
        lines.append("")
        lines.append("NL Assertions")
        lines.append("-------------")

        for item in report.nl_assertions:
            lines.append(f"- Assertion: {item.get('nl_assertion')}")
            lines.append(f"  Met: {item.get('met')}")
            lines.append(f"  Justification: {item.get('justification')}")

    if report.communicate_checks:
        lines.append("")
        lines.append("Communication Checks")
        lines.append("--------------------")

        for item in report.communicate_checks:
            lines.append(f"- Info: {item.get('info')}")
            lines.append(f"  Met: {item.get('met')}")
            lines.append(f"  Justification: {item.get('justification')}")

    lines.append("")
    lines.append("Counts")
    lines.append("------")
    lines.append(
        f"Matched actions: "
        f"{report.matched_actions}/{report.expected_actions}"
    )
    lines.append(
        f"Exact argument matches: "
        f"{report.exact_argument_matches}/{report.matched_actions}"
    )
    lines.append(f"Extra actions: {report.extra_actions}")
    lines.append(f"Missing actions: {report.missing_actions}")

    lines.append("")
    lines.append("Trajectory Divergence")
    lines.append("---------------------")

    if report.missing_actions > 0 or report.extra_actions > 0:
        lines.append(
            "Secondary divergence detected in the observed tool trajectory."
        )
    else:
        lines.append(
            "No missing or extra actions detected by the first-pass comparer."
        )

    lines.append("")
    lines.append("Summary")
    lines.append("-------")
    lines.append(report.summary)

    return "\n".join(lines)



def diagnose_failure(
    simulation: Simulation,
    comparison: TrajectoryComparison,
) -> tuple[str | None, str | None, str | None]:
    if simulation.reward == 1.0:
        return (
            None,
            None,
            "All reward channels passed.",
        )

    db_score = simulation.reward_breakdown.get("DB")
    nl_score = simulation.reward_breakdown.get("NL_ASSERTION")

    if db_score == 1.0 and nl_score == 0.0:
        root_cause = extract_nl_root_cause(simulation)

        return (
            "communication",
            root_cause,
            "Database state was correct, but required user-facing information was not communicated correctly.",
        )

    if db_score == 0.0 and nl_score == 1.0:
        return (
            "database_state",
            "Database state did not match the expected outcome.",
            "The user-facing communication passed, but the underlying state mutation failed.",
        )

    if db_score == 0.0 and nl_score == 0.0:
        return (
            "database_and_communication",
            "Both database state and natural-language requirements failed.",
            "The run failed across multiple reward channels.",
        )

    if comparison.missing_expected_actions:
        return (
            "trajectory_missing_action",
            "At least one expected action was missing from the observed trajectory.",
            "The agent did not perform all expected trajectory steps.",
        )

    mismatched = [
        match
        for match in comparison.matched_actions
        if not match.exact_match
    ]

    if mismatched:
        first = mismatched[0]
        keys = ", ".join(
            mismatch.key for mismatch in first.argument_mismatches
        )

        return (
            "argument_mismatch",
            f"Arguments diverged at `{first.tool_name}` for: {keys}.",
            "The agent selected the right tool but supplied different arguments.",
        )

    return (
        "unknown",
        "The deterministic report could not localize the failure.",
        "Manual inspection required.",
    )


def extract_nl_root_cause(simulation: Simulation) -> str:
    failed_communications = [
        item for item in simulation.communicate_checks
        if item.get("met") is False
    ]

    if failed_communications:
        info = failed_communications[0].get("info")
        return f"Required information `{info}` was not communicated."

    failed_assertions = [
        item for item in simulation.nl_assertions
        if item.get("met") is False
    ]

    if failed_assertions:
        assertion = failed_assertions[0].get("nl_assertion")
        return f"Failed NL assertion: {assertion}"

    return "A natural-language / communication requirement failed."



def build_executive_summary(
    simulation: Simulation,
    report: TrajectoryReport,
) -> str:
    if simulation.reward == 1.0:
        return "PASS — all reward channels succeeded."

    if report.primary_failure == "communication":
        return (
            "FAIL — communication failure. "
            "Database action succeeded, but required user-facing "
            f"information was wrong or missing. {report.root_cause}"
        )

    if report.primary_failure == "database_state":
        return (
            "FAIL — database state failure. "
            "The user-facing communication passed, but the "
            "underlying state mutation was incorrect."
        )

    if report.primary_failure == "database_and_communication":
        return (
            "FAIL — multiple failure channels. "
            "Both database state and communication requirements failed."
        )

    return (
        f"FAIL — {report.primary_failure}. "
        f"{report.impact}"
    )
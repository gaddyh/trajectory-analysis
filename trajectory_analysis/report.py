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

    expected_reads, expected_writes = count_expected_by_type(task)

    matched_reads, matched_writes = count_matched_by_type(
        task=task,
        comparison=comparison,
    )

    action_fidelity = build_action_fidelity(comparison)
    argument_fidelity = build_argument_fidelity(comparison)
    composite_fidelity = build_composite_fidelity(comparison)

    potential_benchmark_issue = detect_potential_benchmark_issue(simulation)

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
        expected_reads=expected_reads,
        expected_writes=expected_writes,
        matched_reads=matched_reads,
        matched_writes=matched_writes,
        action_fidelity=action_fidelity,
        argument_fidelity=argument_fidelity,
        composite_fidelity=composite_fidelity,
        potential_benchmark_issue=potential_benchmark_issue,
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

    if report.potential_benchmark_issue:
        lines.append("")
        lines.append("Potential Benchmark Issue")
        lines.append("-------------------------")
        lines.append(report.potential_benchmark_issue)

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
    lines.append("Read / Write Coverage")
    lines.append("---------------------")
    lines.append(
        f"Read coverage: "
        f"{report.matched_reads}/{report.expected_reads}"
    )
    lines.append(
        f"Write coverage: "
        f"{report.matched_writes}/{report.expected_writes}"
    )

    lines.append("")
    lines.append("Behavioral Fidelity")
    lines.append("-------------------")
    lines.append(
        f"Action fidelity: {format_percent(report.action_fidelity)}"
    )
    lines.append(
        f"Argument fidelity: {format_percent(report.argument_fidelity)}"
    )
    lines.append(
        f"Composite fidelity: {format_percent(report.composite_fidelity)}"
    )
    lines.append(
        f"Outcome success: {'PASS' if report.success else 'FAIL'}"
    )

    if report.success and report.action_fidelity is not None and report.action_fidelity < 1.0:
        lines.append(
            "Interpretation: Agent achieved the correct outcome while "
            "following a different trajectory than the reference."
        )
            
    lines.append("")
    lines.append("Trajectory Variation")
    lines.append("--------------------")

    if report.extra_actions > 0 and report.missing_actions == 0:
        lines.append("Type: Additional Information Gathering")
        lines.append(f"Observed: {report.extra_actions} additional action(s)")
        lines.append("Impact: None directly attributable to trajectory variation")
        lines.append("Assessment: Expected trajectory was covered; extra actions require review only if they affected reward.")
    elif report.success and report.missing_actions > 0:
        lines.append("Type: Read Simplification / Alternative Trajectory")
        lines.append(f"Extra actions: {report.extra_actions}")
        lines.append(f"Missing actions: {report.missing_actions}")
        lines.append("Impact: None detected")
        lines.append("Assessment: Variation was benign because all reward channels passed.")
    elif report.missing_actions > 0 or report.extra_actions > 0:
        lines.append("Type: Divergence")
        lines.append(f"Extra actions: {report.extra_actions}")
        lines.append(f"Missing actions: {report.missing_actions}")
        lines.append("Impact: Requires interpretation against reward channels.")
    else:
        lines.append("No missing or extra actions detected.")
        lines.append("Argument-level differences may still exist.")



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


def is_read_action_name(name: str) -> bool:
    return name.startswith(("get_", "find_", "list_"))


def is_write_action_name(name: str) -> bool:
    return name.startswith(("return_", "exchange_", "modify_", "cancel_", "transfer_"))


def count_expected_by_type(task: Task) -> tuple[int, int]:
    expected_reads = 0
    expected_writes = 0

    for action in task.expected_actions:
        name = action.get("name", "")

        if is_read_action_name(name):
            expected_reads += 1
        elif is_write_action_name(name):
            expected_writes += 1

    return expected_reads, expected_writes


def count_matched_by_type(
    task: Task,
    comparison: TrajectoryComparison,
) -> tuple[int, int]:
    matched_reads = 0
    matched_writes = 0

    for match in comparison.matched_actions:
        expected_action = task.expected_actions[match.expected_idx]
        name = expected_action.get("name", "")

        if is_read_action_name(name):
            matched_reads += 1
        elif is_write_action_name(name):
            matched_writes += 1

    return matched_reads, matched_writes


def build_action_fidelity(
    comparison: TrajectoryComparison,
) -> float | None:
    if comparison.expected_count == 0:
        return None

    return len(comparison.matched_actions) / comparison.expected_count


def build_argument_fidelity(
    comparison: TrajectoryComparison,
) -> float | None:
    matched = len(comparison.matched_actions)

    if matched == 0:
        return None

    exact = sum(
        1
        for match in comparison.matched_actions
        if match.exact_match
    )

    return exact / matched


def build_composite_fidelity(
    comparison: TrajectoryComparison,
) -> float | None:
    action_fidelity = build_action_fidelity(comparison)
    argument_fidelity = build_argument_fidelity(comparison)

    if action_fidelity is None or argument_fidelity is None:
        return None

    return action_fidelity * argument_fidelity


def format_percent(value: float | None) -> str:
    if value is None:
        return "N/A"

    return f"{value:.0%}"
    
def detect_potential_benchmark_issue(
    simulation: Simulation,
) -> str | None:
    if simulation.reward_breakdown.get("DB") != 1.0:
        return None

    if simulation.reward_breakdown.get("NL_ASSERTION") != 0.0:
        return None

    trigger_phrases = [
        "agent's calculation is correct",
        "agent calculation is correct",
        "agent correctly",
        "agent accurately",
        "correct based on",
    ]

    for assertion in simulation.nl_assertions:
        if assertion.get("met") is not False:
            continue

        justification = assertion.get("justification", "")
        lowered = justification.lower()

        if any(phrase in lowered for phrase in trigger_phrases):
            return (
                "Agent output appears internally consistent, but the "
                "benchmark NL assertion was not met. Manual review may be needed."
            )

    return None
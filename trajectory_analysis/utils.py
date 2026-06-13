from trajectory_analysis.models import ArgReference, FailedAction, FailureRecord, FailureTableRow, FailureTypeStats, ToolCall
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
        "arg_path",
        "expected_value",
        "actual_value",
        "expected_refs",
        "actual_refs",
        "trace_pattern",
        "arg_failure_type",
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
        "arg_path",
        "expected_value",
        "actual_value",
        "expected_refs",
        "actual_refs",
        "trace_pattern",
        "arg_failure_type",
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

        actual_calls = extract_actual_tool_calls(sim)

        failed_actions = []
        for check in failed_action_checks:
            action = check.get("action") or {}
            name = action.get("name") or ""

            expected_args = action.get("arguments") or {}

            actual_call = find_closest_actual_call(
                expected_name=name,
                expected_args=expected_args,
                actual_calls=actual_calls,
            )

            actual_args = actual_call.args if actual_call else None
            arg_diff = diff_args(expected_args, actual_args)

            failed_actions.append(
                FailedAction(
                    name=name,
                    is_write=is_write_action(name),
                    expected_args=expected_args,
                    actual_args=actual_args,
                    arg_diff=arg_diff,
                    expected_arg_refs=find_arg_references(
                        sim,
                        expected_args,
                        source="expected",
                    ),
                    actual_arg_refs=find_arg_references(
                        sim,
                        actual_args or {},
                        source="actual",
                    ),
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


def first_arg_diff(action: FailedAction) -> dict | None:
    return action.arg_diff[0] if action.arg_diff else None


def ref_count(refs) -> int:
    return len(refs or [])


def make_arg_trace_summary(action: FailedAction) -> dict:
    diff = first_arg_diff(action)

    if not diff:
        return {
            "arg_path": "-",
            "expected_value": "-",
            "actual_value": "-",
            "expected_refs": 0,
            "actual_refs": 0,
            "trace_pattern": "NO_ARG_DIFF",
        }

    expected_refs = ref_count(action.expected_arg_refs)
    actual_refs = ref_count(action.actual_arg_refs)

    if diff.get("kind") == "missing_actual_call":
        trace_pattern = "MISSING_ACTUAL_CALL"
    elif expected_refs == 0 and actual_refs > 0:
        trace_pattern = "EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED"
    elif expected_refs > 0 and actual_refs > 0:
        trace_pattern = "EXPECTED_AND_ACTUAL_OBSERVED"
    elif expected_refs > 0 and actual_refs == 0:
        trace_pattern = "EXPECTED_OBSERVED_ACTUAL_NOT_OBSERVED"
    elif expected_refs == 0 and actual_refs == 0:
        trace_pattern = "NEITHER_OBSERVED"
    else:
        trace_pattern = "UNKNOWN"

    return {
        "arg_path": str(diff.get("path", "-")),
        "expected_value": shorten(diff.get("expected"), 40),
        "actual_value": shorten(diff.get("actual"), 40),
        "expected_refs": expected_refs,
        "actual_refs": actual_refs,
        "trace_pattern": trace_pattern,
    }


_ARG_PATH_TO_FAILURE_TYPE = {
    "product_id": "WRONG_PRODUCT_LOOKUP",
    "item_ids": "WRONG_SOURCE_ITEM_SELECTION",
    "new_item_ids": "WRONG_VARIANT_SELECTION",
    "payment_method_id": "WRONG_PAYMENT_METHOD",
    "order_id": "WRONG_ORDER_SELECTION",
    "reason": "WRONG_REASON",
}


def classify_arg_failure_type(
    arg_path: str,
    trace_pattern: str,
    failed_action_count: int,
) -> str:
    if failed_action_count != 1:
        return "MULTI_FAILED_ACTIONS"
    if trace_pattern == "MISSING_ACTUAL_CALL" or arg_path == "$":
        return "MISSING_ACTION"
    return _ARG_PATH_TO_FAILURE_TYPE.get(arg_path, "UNKNOWN")


def failure_record_to_table_row(record: FailureRecord) -> FailureTableRow:
    arg_trace = {
        "arg_path": "-",
        "expected_value": "-",
        "actual_value": "-",
        "expected_refs": "-",
        "actual_refs": "-",
        "trace_pattern": "-",
    }

    if record.failed_action_count == 1 and record.failed_actions:
        arg_trace = make_arg_trace_summary(record.failed_actions[0])

    arg_failure_type = classify_arg_failure_type(
        arg_path=str(arg_trace["arg_path"]),
        trace_pattern=str(arg_trace["trace_pattern"]),
        failed_action_count=record.failed_action_count,
    )

    return FailureTableRow(
        task=str(record.task_id),
        reward=str(record.reward),
        pattern=record.pattern,
        failed_action_count=record.failed_action_count,
        failed_write_count=record.failed_write_count,
        failed_actions=shorten(
            ", ".join(a.name for a in record.failed_actions) or "-"
        ),
        arg_path=str(arg_trace["arg_path"]),
        expected_value=str(arg_trace["expected_value"]),
        actual_value=str(arg_trace["actual_value"]),
        expected_refs=str(arg_trace["expected_refs"]),
        actual_refs=str(arg_trace["actual_refs"]),
        trace_pattern=str(arg_trace["trace_pattern"]),
        arg_failure_type=arg_failure_type,
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


def build_failure_type_stats(
    rows: list[FailureTableRow],
) -> list[FailureTypeStats]:
    from collections import Counter

    counter: Counter = Counter()

    for row in rows:
        if row.arg_failure_type == "MULTI_FAILED_ACTIONS":
            continue
        if not row.arg_failure_type or row.arg_failure_type == "-":
            continue
        counter[row.arg_failure_type] += 1

    total = sum(counter.values())

    return [
        FailureTypeStats(
            failure_type=ft,
            count=count,
            pct=round(100 * count / total, 1),
        )
        for ft, count in counter.most_common()
    ]


def build_trace_pattern_stats(
    rows: list[FailureTableRow],
) -> list[FailureTypeStats]:
    from collections import Counter

    counter: Counter = Counter()

    for row in rows:
        if not row.trace_pattern or row.trace_pattern == "-":
            continue
        counter[row.trace_pattern] += 1

    total = sum(counter.values())

    return [
        FailureTypeStats(
            failure_type=tp,
            count=count,
            pct=round(100 * count / total, 1),
        )
        for tp, count in counter.most_common()
    ]


def write_stats_table_markdown(
    stats: list[FailureTypeStats],
    title: str,
    path,
) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n## {title}\n\n")
        f.write("| failure_type | count | pct |\n")
        f.write("| --- | --- | --- |\n")
        for s in stats:
            f.write(f"| {s.failure_type} | {s.count} | {s.pct}% |\n")


def print_stats_table(stats: list[FailureTypeStats], title: str) -> None:
    if not stats:
        print(f"\n{title}: (no data)")
        return

    col_w = max(len(s.failure_type) for s in stats)
    col_w = max(col_w, len("failure_type"))

    def line():
        return "+-" + "-" * col_w + "-+-" + "-" * 5 + "-+-" + "-" * 6 + "-+"

    print(f"\n{title}")
    print(line())
    print(f"| {'failure_type'.ljust(col_w)} | {'count'.ljust(5)} | {'pct'.ljust(6)} |")
    print(line())

    for s in stats:
        print(
            f"| {s.failure_type.ljust(col_w)} "
            f"| {str(s.count).ljust(5)} "
            f"| {(str(s.pct) + '%').ljust(6)} |"
        )

    print(line())


def iter_messages(sim: dict):
    for key in ("messages", "trajectory", "events", "steps"):
        value = sim.get(key)
        if isinstance(value, list):
            for i, msg in enumerate(value):
                if isinstance(msg, dict):
                    yield i, msg


def flatten_arg_values(args: dict):
    for key, value in (args or {}).items():
        if isinstance(value, list):
            for item in value:
                yield key, item
        else:
            yield key, value


def message_text(msg: dict) -> str:
    parts = []

    for key in ("content", "text", "message", "tool_output", "result"):
        value = msg.get(key)
        if value is not None:
            parts.append(str(value))

    # fallback: tool calls/results are often nested json
    parts.append(json.dumps(msg, ensure_ascii=False))

    return "\n".join(parts)


def extract_actual_tool_calls(sim: dict) -> list[ToolCall]:
    calls = []

    for turn, msg in iter_messages(sim):
        tool_calls = msg.get("tool_calls") or msg.get("tool_calls_raw") or []

        if isinstance(tool_calls, list):
            for tc in tool_calls:
                name = (
                    tc.get("name")
                    or tc.get("tool_name")
                    or (tc.get("function") or {}).get("name")
                )

                args = (
                    tc.get("arguments")
                    or tc.get("args")
                    or (tc.get("function") or {}).get("arguments")
                    or {}
                )

                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {"raw": args}

                if name:
                    calls.append(ToolCall(name=name, args=args, turn=turn))

        name = msg.get("name") or msg.get("tool_name")
        args = msg.get("arguments") or msg.get("args")

        if name and isinstance(args, dict):
            calls.append(ToolCall(name=name, args=args, turn=turn))

    return calls


def arg_overlap_score(expected: dict, actual: dict) -> int:
    score = 0

    for key, expected_value in expected.items():
        actual_value = actual.get(key)

        if actual_value == expected_value:
            score += 2
        elif key in actual:
            score += 1

    return score


def find_closest_actual_call(
    expected_name: str,
    expected_args: dict,
    actual_calls: list[ToolCall],
) -> ToolCall | None:
    candidates = [c for c in actual_calls if c.name == expected_name]

    if not candidates:
        return None

    return max(
        candidates,
        key=lambda c: arg_overlap_score(expected_args, c.args),
    )


def diff_args(expected: dict, actual: dict | None) -> list[dict]:
    if actual is None:
        return [{
            "path": "$",
            "expected": expected,
            "actual": None,
            "kind": "missing_actual_call",
        }]

    diffs = []

    for key in sorted(set(expected) | set(actual)):
        ev = expected.get(key)
        av = actual.get(key)

        if ev != av:
            diffs.append({
                "path": key,
                "expected": ev,
                "actual": av,
                "kind": "value_mismatch",
            })

    return diffs


def find_arg_references(sim: dict, args: dict, source: str):
    refs = []

    for arg_name, arg_value in flatten_arg_values(args):
        if arg_value is None:
            continue

        needle = str(arg_value)

        for turn, msg in iter_messages(sim):
            text = message_text(msg)

            if needle in text:
                role = msg.get("role") or msg.get("sender") or msg.get("type")
                idx = text.find(needle)
                start = max(0, idx - 80)
                end = min(len(text), idx + len(needle) + 80)

                refs.append(
                    ArgReference(
                        source=source,
                        arg=arg_name,
                        value=arg_value,
                        turn=turn,
                        role=role,
                        snippet=text[start:end].replace("\n", " "),
                    )
                )

    return refs


def print_failure_details(record: FailureRecord):
    print(f"\nTask {record.task_id}")

    for action in record.failed_actions:
        print(f"\nFAILED ACTION: {action.name}")

        print("Expected args:")
        print(json.dumps(action.expected_args, indent=2))

        print("Actual args:")
        print(json.dumps(action.actual_args, indent=2, ensure_ascii=False))

        print("Arg diff:")
        print(json.dumps(action.arg_diff, indent=2, ensure_ascii=False))

        print("\nExpected references:")
        for ref in action.expected_arg_refs:
            print(
                f"turn={ref.turn} source={ref.source} "
                f"arg={ref.arg} value={ref.value}"
            )
            print(ref.snippet)
            print()

        print("\nActual references:")
        for ref in action.actual_arg_refs:
            print(
                f"turn={ref.turn} source={ref.source} "
                f"arg={ref.arg} value={ref.value}"
            )
            print(ref.snippet)
            print()
from typing import Any, List, Literal
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    name: str
    args: dict
    turn: int | None = None


class ArgReference(BaseModel):
    source: Literal["expected", "actual"]
    arg: str
    value: Any
    turn: int | None = None
    role: str | None = None
    snippet: str


class ContradictionEvidence(BaseModel):
    signal: str
    turn: int
    negative_claim: str
    expected_value: str
    actual_value: str
    contradicting_snippets: list[str]


class FailedAction(BaseModel):
    name: str
    is_write: bool

    expected_args: dict = Field(default_factory=dict)
    actual_args: dict | None = None
    arg_diff: list[dict] = Field(default_factory=list)

    expected_arg_refs: list[ArgReference] = Field(default_factory=list)
    actual_arg_refs: list[ArgReference] = Field(default_factory=list)

    actual_call_turn: int | None = None
    contradiction_signal: str = "-"
    contradiction_evidence: ContradictionEvidence | None = None
    execution_timing_signal: str = "-"


class FailureRecord(BaseModel):
    task_id: int
    reward: float

    pattern: str

    failed_action_count: int
    failed_write_count: int

    failed_actions: List[FailedAction]

    failed_assertions: List[str]
    communicate_info: List[str]

    task_description: str


class FailureTableRow(BaseModel):
    task: str
    reward: str
    pattern: str

    failed_action_count: int
    failed_write_count: int
    failed_actions: str

    arg_path: str
    expected_value: str
    actual_value: str
    expected_refs: str
    actual_refs: str
    trace_pattern: str
    arg_failure_type: str
    contradiction_signal: str
    execution_timing_signal: str

    failed_assertions: str
    communicate_info: str


class FailureTypeStats(BaseModel):
    failure_type: str
    count: int
    pct: float


class RootCauseRecord(BaseModel):
    task_id: int

    failed_action: str

    expected_args: dict
    actual_args: dict

    root_cause_label: str

    evidence_turns: list[int]

    explanation: str


class LLMProbeResult(BaseModel):
    task_id: int
    failed_action: str
    arg_failure_type: str
    trace_pattern: str
    deterministic_signals: list[str]
    llm_proposed_signal: str
    evidence_turn: int | None
    why_expected_correct: str
    why_actual_chosen: str
    deterministically_detectable: bool
    confidence: float
    explanation: str
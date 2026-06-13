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


class FailedAction(BaseModel):
    name: str
    is_write: bool

    expected_args: dict = Field(default_factory=dict)
    actual_args: dict | None = None
    arg_diff: list[dict] = Field(default_factory=list)

    expected_arg_refs: list[ArgReference] = Field(default_factory=list)
    actual_arg_refs: list[ArgReference] = Field(default_factory=list)


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

    failed_assertions: str
    communicate_info: str


class RootCauseRecord(BaseModel):
    task_id: int

    failed_action: str

    expected_args: dict
    actual_args: dict

    root_cause_label: str

    evidence_turns: list[int]

    explanation: str
"""Domain models used by the evaluation harness."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    """A tool invocation produced by an agent."""

    name: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExpectedToolCall:
    """A required tool invocation and the arguments that must match."""

    name: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Scenario:
    """A single agent task and its observable success criteria."""

    id: str
    prompt: str
    expected_calls: tuple[ExpectedToolCall, ...] = ()
    required_response_terms: tuple[str, ...] = ()
    forbidden_tools: tuple[str, ...] = ()


@dataclass(frozen=True)
class AgentResult:
    """The final response and tool trace returned by an agent."""

    response: str
    tool_calls: tuple[ToolCall, ...] = ()


@dataclass(frozen=True)
class Evaluation:
    """A transparent score and diagnostics for one scenario."""

    scenario_id: str
    score: float
    passed: bool
    checks: dict[str, bool]
    notes: tuple[str, ...] = ()


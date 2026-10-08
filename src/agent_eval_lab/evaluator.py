"""Deterministic evaluation for tool traces and final answers."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from .models import AgentResult, Evaluation, ExpectedToolCall, Scenario, ToolCall


def _arguments_match(expected: dict[str, Any], actual: dict[str, Any]) -> bool:
    """Return true when every expected argument is present and equal.

    Additional actual arguments are allowed so scenarios can assert only the
    behavior that matters rather than coupling to an agent implementation.
    """

    return all(key in actual and actual[key] == value for key, value in expected.items())


def _call_matches(expected: ExpectedToolCall, actual: ToolCall) -> bool:
    return expected.name == actual.name and _arguments_match(expected.arguments, actual.arguments)


def evaluate(scenario: Scenario, result: AgentResult, pass_threshold: float = 0.8) -> Evaluation:
    """Score an agent result using equally weighted, observable checks."""

    checks: dict[str, bool] = {}
    notes: list[str] = []

    for index, expected in enumerate(scenario.expected_calls, start=1):
        key = f"expected_call_{index}:{expected.name}"
        checks[key] = any(_call_matches(expected, actual) for actual in result.tool_calls)
        if not checks[key]:
            notes.append(f"Missing matching call to {expected.name}")

    used_tools = {call.name for call in result.tool_calls}
    for tool_name in scenario.forbidden_tools:
        key = f"avoids_forbidden_tool:{tool_name}"
        checks[key] = tool_name not in used_tools
        if not checks[key]:
            notes.append(f"Used forbidden tool {tool_name}")

    normalized_response = result.response.casefold()
    for term in scenario.required_response_terms:
        key = f"response_contains:{term}"
        checks[key] = term.casefold() in normalized_response
        if not checks[key]:
            notes.append(f"Response does not contain required term: {term}")

    if not checks:
        checks["non_empty_response"] = bool(result.response.strip())

    score = sum(checks.values()) / len(checks)
    return Evaluation(
        scenario_id=scenario.id,
        score=round(score, 4),
        passed=score >= pass_threshold,
        checks=checks,
        notes=tuple(notes),
    )


AgentRunner = Callable[[str], AgentResult]


def evaluate_suite(
    scenarios: Iterable[Scenario], runner: AgentRunner, pass_threshold: float = 0.8
) -> list[Evaluation]:
    """Run and evaluate a collection of scenarios."""

    return [evaluate(scenario, runner(scenario.prompt), pass_threshold) for scenario in scenarios]


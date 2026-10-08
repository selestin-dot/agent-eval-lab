"""JSON input/output helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import AgentResult, ExpectedToolCall, Scenario, ToolCall


def _read_json(path: str | Path) -> Any:
    with Path(path).open(encoding="utf-8") as file:
        return json.load(file)


def load_scenarios(path: str | Path) -> list[Scenario]:
    """Load scenarios from a JSON array."""

    items = _read_json(path)
    return [
        Scenario(
            id=item["id"],
            prompt=item["prompt"],
            expected_calls=tuple(
                ExpectedToolCall(name=call["name"], arguments=call.get("arguments", {}))
                for call in item.get("expected_calls", [])
            ),
            required_response_terms=tuple(item.get("required_response_terms", [])),
            forbidden_tools=tuple(item.get("forbidden_tools", [])),
        )
        for item in items
    ]


def load_results(path: str | Path) -> dict[str, AgentResult]:
    """Load pre-recorded agent results keyed by scenario ID."""

    items = _read_json(path)
    return {
        scenario_id: AgentResult(
            response=item["response"],
            tool_calls=tuple(
                ToolCall(name=call["name"], arguments=call.get("arguments", {}))
                for call in item.get("tool_calls", [])
            ),
        )
        for scenario_id, item in items.items()
    }


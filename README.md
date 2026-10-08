# Agent Eval Lab

[![CI](https://github.com/selestin-dot/agent-eval-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/selestin-dot/agent-eval-lab/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A lightweight, deterministic evaluation harness for tool-calling AI agents.
It checks observable behavior—tool selection, arguments, safety constraints,
and final-answer content—without requiring an API key or a particular agent framework.

## Why this project?

Agent demos often look convincing while hiding regressions. Agent Eval Lab turns
expected behavior into version-controlled scenarios that can run in CI. The scoring
is intentionally simple and transparent, making failures easy to diagnose.

## Features

- Framework-independent `AgentResult` and `ToolCall` models
- Partial argument matching for resilient behavioral assertions
- Required final-response terms
- Forbidden-tool safety checks
- JSON fixtures for replaying recorded runs
- Machine-readable reports and meaningful process exit codes
- Zero runtime dependencies

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

agent-eval examples/scenarios.json examples/results.json
```

The command prints a JSON report and exits with status `1` if any scenario fails.

## Scenario format

```json
{
  "id": "weather-detroit",
  "prompt": "What is the weather in Detroit today?",
  "expected_calls": [
    {"name": "weather", "arguments": {"location": "Detroit"}}
  ],
  "required_response_terms": ["Detroit"],
  "forbidden_tools": ["send_email"]
}
```

Expected arguments are a subset: the agent may supply additional arguments such
as units or language without failing the scenario.

## Python API

```python
from agent_eval_lab import AgentResult, Scenario, evaluate

scenario = Scenario(
    id="greeting",
    prompt="Say hello",
    required_response_terms=("hello",),
)
result = AgentResult(response="Hello there!")

report = evaluate(scenario, result)
print(report.score, report.passed)
```

Use `evaluate_suite(scenarios, runner)` to connect a live agent. A runner is any
callable that accepts a prompt and returns an `AgentResult`, so adapters for
LangGraph, OpenAI Agents SDK, CrewAI, or custom loops remain small.

## Roadmap

- Weighted and custom evaluators
- Latency and token-cost tracking
- JUnit and HTML reports
- Reference adapters for popular agent frameworks
- Statistical scoring for non-deterministic runs

## Responsible development

This repository was developed with AI assistance. Design decisions, tests, and
published changes should be reviewed and understood by the maintainer. AI-generated
code is a starting point—not a substitute for ownership.

## License

[MIT](LICENSE)

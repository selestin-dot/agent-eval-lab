"""Command-line interface for evaluating recorded agent runs."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .evaluator import evaluate
from .io import load_results, load_scenarios


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate recorded tool-calling agent runs")
    parser.add_argument("scenarios", help="Path to a scenario JSON file")
    parser.add_argument("results", help="Path to a result JSON file")
    parser.add_argument(
        "--threshold", type=float, default=0.8, help="Pass threshold (default: 0.8)"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not 0 <= args.threshold <= 1:
        raise SystemExit("--threshold must be between 0 and 1")

    scenarios = load_scenarios(args.scenarios)
    results = load_results(args.results)
    evaluations = []
    for scenario in scenarios:
        if scenario.id not in results:
            raise SystemExit(f"No result found for scenario: {scenario.id}")
        evaluations.append(evaluate(scenario, results[scenario.id], args.threshold))

    report = {
        "summary": {
            "scenarios": len(evaluations),
            "passed": sum(item.passed for item in evaluations),
            "average_score": round(
                sum(item.score for item in evaluations) / len(evaluations), 4
            )
            if evaluations
            else 0.0,
        },
        "evaluations": [asdict(item) for item in evaluations],
    }
    print(json.dumps(report, indent=2))
    return 0 if all(item.passed for item in evaluations) else 1


if __name__ == "__main__":
    raise SystemExit(main())

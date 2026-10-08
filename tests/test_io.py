import json

from agent_eval_lab.io import load_results, load_scenarios


def test_loads_scenarios_and_results(tmp_path):
    scenario_path = tmp_path / "scenarios.json"
    scenario_path.write_text(
        json.dumps([{"id": "one", "prompt": "Hi", "forbidden_tools": ["delete"]}]),
        encoding="utf-8",
    )
    result_path = tmp_path / "results.json"
    result_path.write_text(
        json.dumps({"one": {"response": "Hello", "tool_calls": []}}), encoding="utf-8"
    )

    scenarios = load_scenarios(scenario_path)
    results = load_results(result_path)

    assert scenarios[0].forbidden_tools == ("delete",)
    assert results["one"].response == "Hello"


from agent_eval_lab import AgentResult, ExpectedToolCall, Scenario, ToolCall, evaluate


def test_matching_expected_call_allows_extra_arguments():
    scenario = Scenario(
        id="weather",
        prompt="weather?",
        expected_calls=(ExpectedToolCall("weather", {"location": "Detroit"}),),
    )
    result = AgentResult(
        response="Clear",
        tool_calls=(ToolCall("weather", {"location": "Detroit", "units": "metric"}),),
    )

    evaluation = evaluate(scenario, result)

    assert evaluation.score == 1.0
    assert evaluation.passed


def test_forbidden_tool_causes_failure():
    scenario = Scenario(
        id="draft-only",
        prompt="draft an email",
        forbidden_tools=("send_email",),
    )
    result = AgentResult("Sent it", (ToolCall("send_email", {"to": "team@example.com"}),))

    evaluation = evaluate(scenario, result)

    assert evaluation.score == 0.0
    assert not evaluation.passed
    assert evaluation.notes == ("Used forbidden tool send_email",)


def test_required_terms_are_case_insensitive():
    scenario = Scenario(
        id="answer",
        prompt="status",
        required_response_terms=("COMPLETED", "tests"),
    )

    evaluation = evaluate(scenario, AgentResult("Completed all Tests"))

    assert evaluation.passed


def test_empty_criteria_requires_a_response():
    scenario = Scenario(id="basic", prompt="hello")

    assert evaluate(scenario, AgentResult("Hello!")).passed
    assert not evaluate(scenario, AgentResult("   ")).passed


from orchestration.orchestrator import run


def test_incomplete_api_requires_review():
    result = run({})
    assert result["system_id"] == "F47"
    assert result["status"] == "review_required"
    assert result["blockers"]


def test_human_approval_is_separate_gate():
    case = {
        "contract_defined": True,
        "schema_validated": True,
        "backward_compatibility_verified": True,
        "authentication_required": True,
        "authorization_model_reviewed": True,
        "rate_limits_defined": True,
        "input_validation_complete": True,
        "error_contract_defined": True,
        "observability_ready": True,
        "slo_defined": True,
        "rollback_tested": True,
        "contract_tests_passed": True,
        "integration_tests_passed": True,
        "security_tests_passed": True,
    }
    assert run(case)["status"] == "awaiting_human_approval"

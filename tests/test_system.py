from orchestration.orchestrator import run


def good_case(**updates):
    case = {
        "contract_defined": True, "schema_validated": True,
        "backward_compatibility_verified": True, "authentication_required": True,
        "authorization_model_reviewed": True, "rate_limits_defined": True,
        "input_validation_complete": True, "error_contract_defined": True,
        "observability_ready": True, "slo_defined": True, "rollback_tested": True,
        "contract_tests_passed": True, "integration_tests_passed": True,
        "security_tests_passed": True, "breaking_changes": [],
        "unresolved_conflicts": [], "unresolved_questions": [], "human_approval": True,
    }
    case.update(updates)
    return case


def test_healthy_release_is_approved():
    result = run(good_case())
    assert result["status"] == "approved_for_release"
    assert result["blockers"] == []
    assert len(result["analyses"]) == 5


def test_breaking_change_fails_closed():
    result = run(good_case(breaking_changes=["remove /v1/users field"]))
    assert "breaking_changes_unresolved" in result["blockers"]
    assert result["status"] == "review_required"


def test_security_and_authz_failures_block_release():
    result = run(good_case(authorization_model_reviewed=False, security_tests_passed=False))
    assert "authorization_unreviewed" in result["blockers"]
    assert "security_tests_failed" in result["blockers"]


def test_reliability_gates_fail_closed():
    result = run(good_case(observability_ready=False, slo_defined=False, rollback_tested=False))
    assert {"observability_not_ready", "slo_missing", "rollback_untested"}.issubset(result["blockers"])


def test_human_approval_cannot_override_blockers():
    result = run(good_case(schema_validated=False, human_approval=True))
    assert result["status"] == "review_required"

import json
from pathlib import Path

from orchestration.orchestrator import run


def healthy(**updates):
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


SCENARIOS = [
    ("healthy_api", healthy(), "approved_for_release"),
    ("awaiting_approval", healthy(human_approval=False), "awaiting_human_approval"),
    ("schema_failure", healthy(schema_validated=False), "review_required"),
    ("breaking_change", healthy(breaking_changes=["remove field"]), "review_required"),
    ("authz_gap", healthy(authorization_model_reviewed=False), "review_required"),
    ("rate_limit_gap", healthy(rate_limits_defined=False), "review_required"),
    ("reliability_gap", healthy(observability_ready=False, rollback_tested=False), "review_required"),
    ("test_failure", healthy(integration_tests_passed=False), "review_required"),
]


def main():
    rows = []
    for name, payload, expected in SCENARIOS:
        actual = run(payload)["status"]
        rows.append({"scenario": name, "expected": expected, "actual": actual, "passed": actual == expected})
    passed = sum(row["passed"] for row in rows)
    result = {"system_id": "F47", "version": "1.0.0", "scenario_count": len(rows), "passed": passed, "pass_rate": passed / len(rows), "scenarios": rows}
    Path("benchmarks/heldout_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["pass_rate"] != 1.0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

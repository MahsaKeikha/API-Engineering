import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from orchestration.orchestrator import run

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
result = run(case)
assert result["status"] == "approved_for_release"
print(result["status"], result["analyses"].keys())

from __future__ import annotations

from copy import deepcopy

from AGENTS import contract_agent, implementation_agent, reliability_agent, security_agent, testing_agent

SYSTEM_ID = "F47"
SYSTEM_NAME = "API Engineering"
VERSION = "1.0.0"


def run(ctx: dict) -> dict:
    state = _normalize(ctx)
    analyses = {}
    trace = []
    for step, agent in enumerate(
        [contract_agent, security_agent, implementation_agent, testing_agent, reliability_agent], 1
    ):
        name = agent.__name__.split(".")[-1]
        analyses[name] = agent.run(state)
        trace.append({"step": step, "actor": name, "event": "completed"})

    blockers = _blockers(state)
    if blockers:
        status = "review_required"
    elif state["human_approval"]:
        status = "approved_for_release"
    else:
        status = "awaiting_human_approval"

    trace.append({"step": len(trace) + 1, "actor": "api_release_gate", "event": status, "blockers": blockers})
    return {
        "system_id": SYSTEM_ID,
        "system_name": SYSTEM_NAME,
        "version": VERSION,
        "maturity": "L3 Gold Standard",
        "state": state,
        "analyses": analyses,
        "blockers": blockers,
        "ready_for_approval": not blockers,
        "status": status,
        "human_authority": "Production API release requires explicit human approval",
        "trace": trace,
    }


def _normalize(ctx: dict) -> dict:
    state = deepcopy(ctx)
    defaults = {
        "contract_defined": False,
        "schema_validated": False,
        "backward_compatibility_verified": False,
        "authentication_required": True,
        "authorization_model_reviewed": False,
        "rate_limits_defined": False,
        "input_validation_complete": False,
        "error_contract_defined": False,
        "observability_ready": False,
        "slo_defined": False,
        "rollback_tested": False,
        "contract_tests_passed": False,
        "integration_tests_passed": False,
        "security_tests_passed": False,
        "breaking_changes": [],
        "unresolved_conflicts": [],
        "unresolved_questions": [],
        "human_approval": False,
    }
    for key, value in defaults.items():
        state.setdefault(key, value)
    return state


def _blockers(state: dict) -> list[str]:
    checks = [
        (state["contract_defined"], "contract_missing"),
        (state["schema_validated"], "schema_unvalidated"),
        (state["backward_compatibility_verified"], "compatibility_unverified"),
        (state["authentication_required"], "authentication_disabled"),
        (state["authorization_model_reviewed"], "authorization_unreviewed"),
        (state["rate_limits_defined"], "rate_limits_missing"),
        (state["input_validation_complete"], "input_validation_incomplete"),
        (state["error_contract_defined"], "error_contract_missing"),
        (state["observability_ready"], "observability_not_ready"),
        (state["slo_defined"], "slo_missing"),
        (state["rollback_tested"], "rollback_untested"),
        (state["contract_tests_passed"], "contract_tests_failed"),
        (state["integration_tests_passed"], "integration_tests_failed"),
        (state["security_tests_passed"], "security_tests_failed"),
    ]
    blockers = [reason for passed, reason in checks if not passed]
    if state["breaking_changes"]:
        blockers.append("breaking_changes_unresolved")
    if state["unresolved_conflicts"]:
        blockers.append("unresolved_conflict")
    if state["unresolved_questions"]:
        blockers.append("unresolved_question")
    return blockers

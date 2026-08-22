from orchestration.orchestrator import run

result = run({})
assert result["status"] == "review_required"
print(result["status"], result["blockers"][:3])

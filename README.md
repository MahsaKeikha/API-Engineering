# F47 API Engineering

**Maturity:** L3 Gold Standard candidate  
**Version:** 1.0.0

A reproducible five-agent reference implementation for API release governance across contract design, security, implementation, testing, and reliability.

## Release gates

F47 fails closed when an API contract or schema is missing, backward compatibility is unverified, authentication is disabled, authorization review is incomplete, rate limits are absent, input validation or error contracts are incomplete, observability/SLOs are missing, rollback is untested, contract/integration/security tests fail, breaking changes remain unresolved, or open conflicts/questions remain. Human approval is required after all automated gates pass and cannot override blockers.

## Reproduce

```bash
python -m pip install -e '.[dev]'
ruff check .
pytest -q
python benchmarks/heldout_suite.py
python examples/minimal.py
python examples/complete.py
python run.py
```

CI runs this matrix on Python 3.10, 3.11, and 3.12 and publishes the Python 3.12 held-out artifact.

## Architecture

- `AGENTS/` contract, security, implementation, testing, and reliability roles
- `SKILLS/` reusable API engineering reasoning
- `TOOLS/` deterministic schema, dependency, test, risk, and release primitives
- `orchestration/` shared release-governance flow
- `benchmarks/` held-out reproducibility suite
- `examples/` minimal and complete clean-checkout examples
- `tests/` contract, safety, compatibility, reliability, and approval behavior

L3 denotes a reproducible reference implementation. It does not replace production security review, organization-specific API governance, threat modeling, or human release authority.

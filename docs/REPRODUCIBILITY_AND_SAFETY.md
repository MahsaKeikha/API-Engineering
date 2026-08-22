# Reproducibility and Safety

Use Python 3.10, 3.11, or 3.12. From a clean checkout run the install, lint, tests, held-out suite, examples, and smoke command documented in the README. The held-out suite writes deterministic JSON to `benchmarks/heldout_results.json`, and CI publishes the Python 3.12 artifact as `f47-heldout-results`.

F47 is advisory release governance. Production release authority remains human-owned. Automated gates fail closed for contract, schema, compatibility, authentication/authorization, rate-limit, validation, error-contract, reliability, rollback, test, breaking-change, conflict, and unresolved-question gaps. Human approval is only considered after blockers clear.

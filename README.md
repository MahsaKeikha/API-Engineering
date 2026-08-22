# F47 API Engineering

**Maturity:** L3 Gold Standard candidate  
**Version:** 1.0.0

A reproducible five-agent reference implementation for governed API engineering across contract design, security review, service implementation, testing, reliability, and human-controlled release.

F47 is designed for engineers, platform teams, researchers, and students who want to study how API delivery can be decomposed into specialist agents while keeping deterministic validation, schema governance, security controls, release evidence, observability, and accountable human authority explicit.

It is a reference architecture and decision-support system. It does not autonomously deploy production APIs, change gateway policy, rotate credentials, alter authorization rules, publish breaking changes, or replace accountable API engineers, security teams, platform owners, SREs, privacy professionals, or release authorities.

## What the system does

A production API is more than a set of endpoints. The team must know what the contract guarantees, whether consumers remain compatible, how authentication and authorization are enforced, how inputs and errors are handled, how dependencies behave, whether tests cover the right risks, what reliability targets apply, and how the service can be rolled back safely.

F47 separates those responsibilities into five specialist agents:

```text
API change request + service evidence
             |
             v
      Contract Agent
             |
             v
      Security Agent
             |
             v
   Implementation Agent
             |
             v
       Testing Agent
             |
             v
    Reliability Agent
             |
             v
   fail-closed release gate
             |
             v
     human release approval
```

Each stage produces a different kind of engineering evidence. A clean implementation does not erase an unresolved compatibility break or an incomplete authorization review.

## Repository architecture

The repository exposes the main capability layers directly:

```text
AGENTS/         contract, security, implementation, testing, reliability roles
SKILLS/         reusable API engineering procedures
TOOLS/          deterministic schema, dependency, test, risk, and release primitives
memory/         shared workflow state
observability/  trace and run visibility
orchestration/  multi-agent release-governance flow
benchmarks/     benchmark and held-out cases
evals/          evaluation entry point
examples/       minimal and complete runnable examples
docs/           architecture, reproducibility, safety, and L3 audit evidence
```

The repository also includes project configuration, CI, citation metadata, and a deterministic release gate.

## Agents and responsibilities

| Agent | Responsibility | Core engineering question |
|---|---|---|
| Contract Agent | Review endpoint schemas, semantics, versioning, and compatibility | Is the API contract explicit, stable, and safe for current consumers? |
| Security Agent | Review authentication, authorization, validation, rate limiting, and exposure | Is access controlled and are abuse and trust boundaries understood? |
| Implementation Agent | Review service behavior and dependency interactions | Does implementation behavior match the declared contract and operational constraints? |
| Testing Agent | Review contract, integration, security, and failure-path coverage | Is there sufficient evidence that the API behaves correctly under expected and adverse conditions? |
| Reliability Agent | Review SLOs, observability, rollback, dependency resilience, and operational readiness | Can the service be operated safely after release? |

The orchestrator combines these outputs but preserves specialist boundaries so one stage cannot silently override another.

## Skills layer

Reusable reasoning procedures live under `SKILLS/`:

```text
SKILLS/
├── api_contract_design.py
├── security_review.py
├── service_design.py
├── test_design.py
└── reliability_reasoning.py
```

### API contract design

Defines what the API promises to consumers. A mature contract should describe request and response schemas, field semantics, error behavior, authentication expectations, pagination, idempotency, versioning, and compatibility policy.

### Security review

Covers authentication, authorization, input handling, abuse controls, secrets, transport security, sensitive-data exposure, and trust boundaries. Security findings should remain explicit release evidence.

### Service design

Reviews how the implementation fulfills the contract, including dependency behavior, timeouts, retries, idempotency, concurrency, transaction boundaries, and failure handling.

### Test design

Maps risks to deterministic tests. Good coverage includes contract, integration, compatibility, negative-path, security, resilience, and regression tests rather than relying only on happy-path unit tests.

### Reliability reasoning

Reviews operational behavior such as SLOs, latency, error handling, dependency failure, observability, rollback, capacity, and incident readiness.

## Tools layer

Deterministic control primitives live under `TOOLS/`:

```text
TOOLS/
├── schema_registry.py
├── dependency_map.py
├── test_matrix.py
├── risk_register.py
└── release_gate.py
```

### Schema registry

Provides a canonical place for API schemas and contract versions. Production extensions can validate OpenAPI, JSON Schema, protobuf, GraphQL schemas, or other interface definitions.

### Dependency map

Makes upstream and downstream dependencies visible so a change can be evaluated against its blast radius.

### Test matrix

Tracks which test classes are required and whether evidence exists for each one.

### Risk register

Preserves unresolved security, compatibility, implementation, and reliability risks through the release workflow.

### Release gate

Evaluates release evidence and fails closed when mandatory controls are incomplete. The gate supports human decision making but does not replace authenticated production change authority.

## End-to-end workflow

A typical F47 release review follows this sequence:

1. Load the proposed API change and current contract evidence.
2. Validate the contract and identify versioning or compatibility implications.
3. Review authentication, authorization, input validation, rate limits, and data exposure.
4. Review implementation behavior and dependencies against the declared contract.
5. Build or evaluate the required test matrix.
6. Review reliability targets, observability, rollback, and operational readiness.
7. Accumulate unresolved risks and questions in shared state.
8. Apply automated release gates.
9. Fail closed when material evidence is missing or contradictory.
10. Require explicit human approval before production release.

This sequence makes it possible to trace a release decision back to contract, security, implementation, testing, and reliability evidence.

## Quick start

Install the project with development dependencies:

```bash
python -m pip install -e '.[dev]'
```

Run static checks and tests:

```bash
ruff check .
pytest -q
```

Run the held-out benchmark suite:

```bash
python benchmarks/heldout_suite.py
```

Run the examples:

```bash
python examples/minimal.py
python examples/complete.py
```

Run the main entry point:

```bash
python run.py
```

CI runs the repository across Python 3.10, 3.11, and 3.12 and publishes the Python 3.12 held-out artifact.

## Contract-first engineering

The Contract Agent treats the API contract as the interface between providers and consumers.

A strong contract can define:

- endpoint identity
- HTTP method or protocol operation
- path and query parameters
- request schema
- response schema
- error schema
- authentication requirements
- authorization expectations
- idempotency behavior
- pagination
- ordering guarantees
- consistency expectations
- rate-limit behavior
- deprecation policy
- versioning and compatibility rules

Implementation behavior should be tested against this contract rather than inferred from undocumented service behavior.

## Backward compatibility

Compatibility is a first-class release concern.

Potential breaking changes include:

- removing endpoints or fields
- renaming fields
- narrowing accepted values
- changing field types
- changing nullability
- changing default behavior
- changing error codes or structures
- changing pagination semantics
- adding required parameters
- tightening authorization unexpectedly
- altering ordering or consistency guarantees

The release flow should record whether each change is backward compatible, intentionally versioned, or blocked pending migration.

## Versioning and deprecation

Versioning should be explicit and tied to a deprecation policy. Production systems may use URL, header, media-type, schema, or protocol-level versioning.

A mature deprecation plan should define:

- affected consumers
- announced deprecation date
- migration guidance
- replacement contract
- usage telemetry
- support window
- final retirement criteria

A breaking change should not be treated as safe solely because a new version number exists.

## Authentication and authorization

Authentication answers who or what is calling. Authorization answers what that caller is allowed to do. F47 treats both as separate release concerns.

Production review should verify:

- supported identity mechanism
- credential scope and lifetime
- token or session validation
- service-to-service identity
- role or attribute checks
- object-level authorization where applicable
- tenant isolation
- privilege boundaries
- denial behavior
- auditability

An API with working authentication but incomplete authorization is not release-ready.

## Input validation and error contracts

Input validation should be deterministic where possible. Validate types, lengths, enumerations, required fields, ranges, formats, and semantic constraints before business logic relies on the data.

Error behavior should also be part of the contract. A consistent error model can define:

- machine-readable error code
- human-readable message
- correlation identifier
- retryability
- field-level validation details
- safe diagnostic context

Errors should avoid leaking secrets, internal stack traces, credentials, or sensitive implementation details.

## Rate limiting and abuse controls

Rate limits and abuse controls help protect service availability and downstream dependencies.

Depending on the system, review:

- per-user or per-client quotas
- burst limits
- global service limits
- concurrency limits
- expensive endpoint protections
- retry guidance
- backoff behavior
- quota-exceeded errors
- monitoring for unusual patterns

Production controls should be enforced by deterministic infrastructure rather than narrative policy alone.

## Idempotency and retry safety

APIs that perform writes should define retry behavior explicitly. Where appropriate, use idempotency keys, deduplication, transaction boundaries, or safe retry semantics.

Review whether:

- repeated requests create duplicate side effects
- client retries are safe
- dependency retries amplify load
- timeouts create ambiguous completion states
- partial failure can be detected and recovered

## Dependency behavior

The dependency map should make downstream services and infrastructure visible. Important review questions include:

- What dependencies are synchronous?
- Which failures propagate directly to clients?
- What timeouts apply?
- Are retries bounded?
- Are circuit breakers or load-shedding strategies required?
- Are fallbacks valid or misleading?
- What happens when a dependency is slow rather than unavailable?

Reliability should be evaluated across the dependency graph, not only inside the API process.

## Test strategy

The Testing Agent and `test_matrix.py` make testing requirements explicit.

A useful release test matrix can include:

- unit tests
- schema validation
- contract tests
- consumer-driven contract tests
- integration tests
- authorization tests
- input-validation tests
- negative-path tests
- rate-limit tests
- idempotency tests
- timeout and retry tests
- dependency-failure tests
- compatibility tests
- performance tests
- rollback tests

A passing unit-test suite alone should not satisfy the release gate for a consequential API change.

## Reliability and SLOs

The Reliability Agent connects API behavior to operational expectations.

Production review may include:

- availability target
- latency objectives
- error-rate objectives
- throughput expectations
- saturation signals
- dependency SLOs
- timeout budgets
- retry budgets
- capacity headroom
- incident ownership
- error-budget policy

SLOs should be measurable from actual telemetry.

## Observability

A production API should provide enough telemetry to determine whether it is healthy and why it is failing.

Useful signals include:

- request rate
- success and error rate
- latency distributions
- saturation
- dependency latency and errors
- authorization failures
- rate-limit events
- schema or validation failures
- retry counts
- timeout counts
- version usage

Use structured logs, metrics, traces, and correlation identifiers while minimizing sensitive-data exposure.

The repository's `observability/` layer provides the reference point for workflow traces as well as API operational evidence.

## Shared state and memory

The `memory/` layer preserves workflow evidence across agents. This allows the Reliability Agent to see unresolved contract or security findings without collapsing the whole workflow into one prompt.

Production state should be scoped by service, API version, release candidate, environment, and change identifier. Preserve prior evidence so reviewers can understand why a release moved from blocked to approved.

## Fail-closed release governance

F47 is designed to block release when required evidence is missing.

Examples of release blockers include:

```text
API CONTRACT MISSING
SCHEMA MISSING
BACKWARD COMPATIBILITY UNVERIFIED
AUTHENTICATION DISABLED
AUTHORIZATION REVIEW INCOMPLETE
RATE LIMITS MISSING
INPUT VALIDATION INCOMPLETE
ERROR CONTRACT INCOMPLETE
OBSERVABILITY MISSING
SLO MISSING
CONTRACT TEST FAILED
INTEGRATION TEST FAILED
SECURITY TEST FAILED
ROLLBACK UNTESTED
BREAKING CHANGE UNRESOLVED
CONFLICT UNRESOLVED
HUMAN APPROVAL REQUIRED
```

Human approval is required only after automated gates pass and should not override active blockers.

## Rollback and release strategy

A production release should define how to reverse or contain the change if behavior degrades.

Relevant strategies include:

- backward-compatible deployment
- feature flags
- canary release
- staged rollout
- traffic splitting
- schema compatibility windows
- dual-read or dual-write migrations where appropriate
- fast rollback

Rollback evidence should be tested, not assumed.

## Human authority and production boundaries

F47 must not autonomously:

- deploy an API to production
- alter production gateway rules
- change authentication configuration
- grant permissions or roles
- rotate or expose secrets
- publish breaking contracts
- disable rate limits
- suppress failed security tests
- bypass required review
- delete production data
- approve privacy or compliance risk

Production changes should flow through authenticated source control, CI/CD, secrets management, gateway controls, infrastructure policy, and accountable human approval.

## Security boundaries

Production API engineering should include controls appropriate to the service and data classification, including:

- transport security
- secret isolation
- least privilege
- tenant isolation
- input validation
- output filtering
- dependency scanning
- audit logs
- abuse prevention
- sensitive-data minimization
- network controls

The multi-agent system should receive only the credentials and data required for each role.

## Benchmarks and evaluation

F47 includes benchmark and evaluation assets under:

```text
benchmarks/cases.json
benchmarks/heldout_suite.py
benchmarks/RESULTS.md
evals/evaluate.py
```

Evaluation should measure engineering behavior, not only whether the generated text sounds plausible.

Useful dimensions include:

- contract completeness
- breaking-change detection
- compatibility reasoning
- authentication and authorization issue detection
- validation-gap detection
- test-matrix completeness
- reliability-gap detection
- rollback-gap detection
- unsupported-claim rate
- fail-closed gate behavior

Strong benchmark cases should contain deliberately missing schemas, undocumented breaking changes, weak authorization, absent rate limits, incomplete test coverage, missing SLOs, failed rollback evidence, and conflicting stage outputs.

## CI and reproducibility

The repository includes `.github/workflows/ci.yml` and `pyproject.toml`.

CI should validate:

- syntax and imports
- deterministic tool behavior
- schema compatibility fixtures
- agent contract behavior
- orchestration flow
- release-gate behavior
- adversarial and failure cases
- benchmark regressions

For production deployments, add integration tests against representative gateways, auth systems, service meshes, data stores, and sandbox environments.

## L3 Gold Standard candidate

F47 identifies itself as an **L3 Gold Standard candidate** based on the reproducibility, governance, and evaluation evidence documented under `docs/L3_AUDIT.md`.

The label describes the maturity of the reference implementation. It does not certify a particular production API, security posture, regulatory status, or release process.

## Failure behavior

The system should make incomplete evidence explicit rather than generating a confident release recommendation.

Appropriate states include:

```text
CONTRACT REVIEW REQUIRED
BREAKING CHANGE DETECTED
AUTHORIZATION REVIEW REQUIRED
TEST EVIDENCE MISSING
RELIABILITY REVIEW REQUIRED
ROLLBACK NOT VERIFIED
RELEASE BLOCKED
HUMAN DECISION REQUIRED
```

The system must not fabricate test results, consumer compatibility, SLO evidence, security approval, or production authorization.

## Extending F47

Common extensions include:

- OpenAPI validation
- protobuf and gRPC contract governance
- GraphQL schema governance
- consumer-driven contract testing
- API gateway integration
- service-mesh policy review
- OAuth or OIDC integration
- deterministic authorization-policy analysis
- API inventory and catalog integration
- dependency graph extraction
- rate-limit policy validation
- performance benchmarking
- schema-diff tooling
- deprecation tracking
- API version telemetry
- SLO dashboards
- automated rollback evidence

New agents should remain specialized, receive the minimum permissions required, emit structured artifacts, and have explicit escalation paths.

## Example use cases

F47 can serve as a reference architecture for:

- REST API development
- gRPC services
- GraphQL APIs
- internal platform APIs
- public developer APIs
- microservice interfaces
- API migration programs
- compatibility reviews
- release-readiness reviews
- teaching multi-agent API engineering

High-impact or regulated APIs should add domain-specific security, privacy, legal, compliance, and operational controls.

## Repository map

```text
.github/workflows/ci.yml
AGENTS/
├── contract_agent.py
├── security_agent.py
├── implementation_agent.py
├── testing_agent.py
└── reliability_agent.py
SKILLS/
├── api_contract_design.py
├── security_review.py
├── service_design.py
├── test_design.py
└── reliability_reasoning.py
TOOLS/
├── schema_registry.py
├── dependency_map.py
├── test_matrix.py
├── risk_register.py
└── release_gate.py
benchmarks/
config/
docs/
evals/
examples/
memory/
observability/
orchestration/
run.py
pyproject.toml
CITATION.cff
LICENSE
README.md
```

See `docs/ARCHITECTURE.md`, `docs/REPRODUCIBILITY_AND_SAFETY.md`, and `docs/L3_AUDIT.md` for additional implementation and audit context.

## Design principles

1. Treat the API contract as an explicit product interface.
2. Detect compatibility risk before release.
3. Separate authentication from authorization review.
4. Use deterministic validation and test tools wherever practical.
5. Preserve dependency, risk, and test evidence across agents.
6. Make observability and SLOs part of API design.
7. Require rollback evidence for consequential releases.
8. Fail closed when critical contract, security, test, or reliability evidence is missing.
9. Give agents the minimum tool and credential access required.
10. Keep production release authority with authenticated, accountable humans.

## Citation and reuse

The repository includes `CITATION.cff` for academic and technical citation. It is MIT licensed and may be studied, adapted, and extended subject to the license terms.

## Responsible use

Use F47 as an API engineering workflow and multi-agent architecture reference. Validate contracts, compatibility, security controls, implementation behavior, test evidence, SLOs, observability, and rollback procedures against the real production environment. Final release and production authority remain with accountable humans operating under the organization's engineering, security, privacy, platform, and change-management controls.
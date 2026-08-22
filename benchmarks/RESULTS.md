# F47 Held-Out Reproducibility Results

Gold Standard validation was executed from a clean GitHub Actions checkout on the `l3-gold-standard` branch.

- Evidence source run: `32545662766`
- Head: `8e55b04c47ed320381eaad0abbd435340a40fbd2`
- Python: 3.10, 3.11, 3.12 all green
- Held-out API scenarios: 8/8 expected behaviors passed
- Pass rate: 1.0
- Artifact: `f47-heldout-results`
- Artifact digest: `sha256:ba9dd658ad8e36c37918bd18ed791edbb0e481fcd72599b51d1df19b9eb381fd`

The suite validates healthy release, human approval, schema failure, breaking changes, authorization review, rate limiting, reliability readiness, and integration-test failure. It validates deterministic reference behavior, not universal production correctness.

# Contributing

[简体中文](CONTRIBUTING.zh-CN.md)

Thank you for improving ProofRelay. Start with a frozen-work-unit Issue. Use a dedicated branch and pull request; do not push directly to the protected branch.

Every contribution must:

1. identify the frozen target, route, work-unit ID, and base commit;
2. keep complete work in versioned files rather than chat or comments;
3. distinguish `PROVED`, `DISPROVED`, `PARTIAL`, `INCOMPLETE`, `BLOCKED`, and `NO_HIT_NOT_A_PROOF`;
4. include reproducible code and sanitized receipts for computational claims;
5. preserve failed and superseded work;
6. avoid credentials, personal data, and live infrastructure details;
7. pass `python scripts/validate_repo.py` and the standard-library test suite.

Candidate authors must not approve their own claims. State-ledger changes require a dedicated maintainer PR with linked candidate, audit, and verification evidence.

See [the workflow](docs/workflow.md) for the full contract.

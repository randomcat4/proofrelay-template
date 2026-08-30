# End-to-end workflow

[简体中文](workflow.zh-CN.md)

## Roles

- **Maintainer:** freezes work, controls accepted state, performs the main audit, and resolves governance conflicts.
- **Author/worker:** owns one bounded lane and submits a candidate. Cannot update accepted state.
- **Verifier:** receives a commit-pinned bundle and returns a bounded verdict. Cannot certify their own candidate.
- **Compute worker:** runs committed code and returns sanitized receipts. Has no authority to interpret results beyond the assigned scope.

One person or system may hold multiple roles across different work units, but never author and independent verifier for the same candidate.

## Phase 0 — Project setup

1. Replace template identifiers and define the protected branch.
2. Write the exact target in `contracts/frozen-target.md`.
3. Configure the verification threshold in `state/PROJECT_STATE.json`.
4. Enable branch protection and required CI.
5. Create labels from `config/labels.json`.

## Phase 1 — Freeze a work unit

Open a **Frozen work unit** Issue containing:

- immutable target version and base commit;
- exact scope and non-goals;
- permitted evidence and forbidden context;
- deliverables and directory ownership;
- success, partial-success, stop, and budget conditions;
- fastest falsification test and known hazards;
- required isolation level.

Substantive changes require a new Issue revision or a superseding work unit.

## Phase 2 — Claim and start

The worker posts one claim comment, records their handle and branch, and creates `work/<work-unit>-<handle>`. Work is `START_PENDING` until durable repository evidence appears; the recommended transition to `CLAIMED` requires both claim and branch.

Only one active worker owns a work unit unless the Issue explicitly defines independent replications. A monitor never treats chat presence as start evidence.

## Phase 3 — Candidate delivery

Run `python scripts/new_work_unit.py attempt <work-unit> <handle>` to scaffold the attempt. The candidate contains:

- `answer.md` with exact status and self-contained reasoning;
- `receipt.json` with provenance and execution metadata;
- `src/` for code;
- `out/` for necessary raw output or compact certificates.

The candidate PR is pinned to its base commit and begins with an allowed status. It does not edit accepted state.

## Phase 4 — Main audit

A maintainer:

1. checks target fidelity, quantifiers, edge cases, equivalences, and citation conditions;
2. distinguishes general reasoning from finite evidence;
3. reruns load-bearing computation in a clean environment;
4. compares hashes and denominators;
5. checks privacy and authority boundaries;
6. records `MAIN_AUDIT_PASS`, `MAIN_AUDIT_FAIL`, or `MAIN_AUDIT_INCONCLUSIVE` in a versioned audit.

Passing the main audit creates a verification task; it does not accept the claim.

## Phase 5 — Independent verification

Copy only the frozen target, candidate commit, and explicitly permitted baseline into a candidate bundle. The verification Issue names the immutable SHA and adversarial checklist. The verifier uses `verify/<work-unit>-<handle>` and a separate PR.

If the verifier finds a critical gap, they report it without rewriting the candidate. The author may submit a new candidate commit. Material revisions require a different independent verification.

## Phase 6 — State decision

A dedicated maintainer PR may update accepted state only when the configured evidence threshold is met. It updates, in one commit series:

- `state/PROJECT_STATE.json`;
- `state/STATUS.md` and `state/STATUS.zh-CN.md`;
- the route registry;
- the artifact manifest when preserved evidence changed;
- the changelog.

The state entry links every candidate, audit, verification, receipt, and exact commit.

## Phase 7 — Monitor or close

Close or pause the route when it is accepted, falsified, precisely blocked, over budget, superseded, or no longer worth pursuing. Preserve all evidence. Reusing a worker for a new task requires a new self-contained Issue and a fresh claim.

## Chat response contract

When external chat is used, ask for no more than three nonempty lines:

```text
STATUS: <allowed status>
PR: <URL>
BLOCKER: <URL, only when needed>
```

Everything substantive belongs in GitHub.

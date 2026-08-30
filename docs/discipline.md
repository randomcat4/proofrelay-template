# Collaboration discipline

[简体中文](discipline.zh-CN.md)

These rules are the normative core of ProofRelay.

## 1. One authoritative surface

GitHub stores the assignment, immutable inputs, candidate, evidence, review, and accepted state. Chat may announce a URL or short status, but a chat message is never the sole proof of start, completion, or acceptance.

## 2. Freeze before work

Every work unit fixes a target version, exact quantifiers or acceptance criteria, permitted inputs, expected outputs, base commit, budget, fastest falsification test, and stop condition. Changing the target creates a new version; it does not silently rewrite the current task.

## 3. Durable start evidence

`PROMPT_SENT`, `ACTIVE`, or an unanswered message is not start evidence. A work unit becomes `CLAIMED` only when a durable repository artifact exists: normally an Issue claim plus a dedicated branch. Monitors must not repeatedly dispatch the same task when delivery may already have occurred.

## 4. One owner, one lane, one branch

Each active work unit has one accountable owner and a bounded directory. Parallel routes must be structurally distinct or explicitly declared as replications. Workers do not edit sibling lanes or accepted-state files.

## 5. Repository-first delivery

The complete argument, implementation, logs, certificates, and receipts belong in the repository. Issue comments and chat replies stay short and point to the pull request or blocker.

## 6. Immutable candidate identity

Audits and verifications bind to a full commit SHA, not a moving branch, PR title, or latest file. A revision gets a new commit and may require a new verification.

## 7. Separation of duties

Candidate author, maintainer auditor, and independent verifier are distinct roles. The author cannot certify the candidate. The verifier does not silently repair it. Maintainers alone update accepted-state ledgers.

## 8. Honest isolation

Verification records what the verifier could see. Use `STRICT_FRESH`, `CONTEXT_ISOLATED`, `CROSS_LANE`, or `NOT_INDEPENDENT`; never claim blind or fresh review when prior sibling context was visible. Isolation failure yields `INCONCLUSIVE`, not a convenient pass.

## 9. Adversarial verification

Verification attempts to break the claim: reconstruct definitions, check boundary cases, audit equivalences and citations, rerun exact evidence with a structurally separate implementation where material, and state a bounded verdict: `CORRECT`, `INCORRECT`, or `INCONCLUSIVE`.

## 10. Statuses do not collapse

Claim truth, review state, computation, formalization, reproducibility, and novelty are independent axes. Examples:

- `PROVED_IN_CANDIDATE` is not `ACCEPTED`.
- `MAIN_AUDIT_PASS` is not independent verification.
- `COMPUTATION_REPRODUCED` is not a general proof.
- `FORMALLY_CHECKED_PARTIAL` is not full formalization.
- `NOT_ASSESSED` novelty is not `NOVEL`.

## 11. Finite evidence has a denominator

Every search reports its theoretical universe, executed count, pruning rule, and coverage justification. `NO_HIT` is a probe unless a proof shows the finite universe exhausts the stated target.

## 12. Receipts are part of the result

Computational work records the source commit, exact command, environment, start and finish times, exit code, inputs and outputs, hashes, resource use, and search denominator. Remote infrastructure details are redacted.

## 13. Main audit is independent work

A maintainer reads the load-bearing argument, checks scope and citations, reruns relevant evidence, inspects secret boundaries, and records the audit. Self-reported confidence or a verifier's label does not substitute for this gate.

## 14. State changes are atomic

An accepted-state PR updates the machine ledger and human ledger together and links the frozen task, candidate commit, candidate PR, audit, verification PR, and receipts. Partial updates fail validation.

## 15. Merge and truth are different events

A merged candidate may mean only that the artifact was preserved. Acceptance requires the state-change gate. Conversely, a rejected or false attempt remains valuable evidence and stays versioned.

## 16. Failure is preserved

Do not delete counterexamples, failed routes, mismatched receipts, or contamination reports. Supersede them with new commits and explicit provenance. Never make the history look cleaner than the work was.

## 17. Monitoring is quiet and idempotent

Read repository state before messaging a worker. Do not interrupt active generation, do not resend a possibly delivered task, and report only material change, precise blockers, completed gates, or required human action.

## 18. Budget follows evidence

Continue a route only for a complete proof or disproof, a verified strict partial result, a reproducible counterexample, or a precise structural blocker. Length, confidence, repeated no-hit searches, and sunk cost do not justify another round.

## 19. Authority and secrets stay bounded

Workers receive only the permissions and inputs needed for the lane. They do not share credentials or receive unrelated private context. Remote machines run committed code at pinned commits and return sanitized receipts.

## 20. Public claims remain conservative

The README leads with the current top-level status. Correctness, completeness, novelty, and publication readiness are stated separately. Project limitations and conflicts are disclosed near the claim they qualify.

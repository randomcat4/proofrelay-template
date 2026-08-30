# Status model

[简体中文](status-model.zh-CN.md)

ProofRelay uses orthogonal status axes. A single word such as “done” is forbidden for accepted-state decisions.

## Work-unit lifecycle

`DRAFT → FROZEN → START_PENDING → CLAIMED → CANDIDATE_SUBMITTED → MAIN_AUDIT → VERIFICATION → DECIDED`

Terminal operational states are `ACCEPTED`, `REJECTED`, `BLOCKED`, `SUPERSEDED`, and `CANCELLED`.

## Candidate result

- `PROVED`: complete proof of the frozen target is claimed.
- `DISPROVED`: a complete counterexample or contradiction certificate is claimed.
- `PARTIAL`: a strictly scoped result is established.
- `INCOMPLETE`: useful work exists but the target is not established.
- `BLOCKED`: a precise external or structural blocker prevents completion.
- `NO_HIT_NOT_A_PROOF`: a bounded search found no counterexample.

These are author claims until reviewed.

## Review and verification

- Main audit: `NOT_REVIEWED`, `MAIN_AUDIT_PASS`, `MAIN_AUDIT_FAIL`, `MAIN_AUDIT_INCONCLUSIVE`.
- Independent verdict: `NOT_VERIFIED`, `CORRECT`, `INCORRECT`, `INCONCLUSIVE`.
- Isolation: `STRICT_FRESH`, `CONTEXT_ISOLATED`, `CROSS_LANE`, `NOT_INDEPENDENT`, `UNKNOWN`.

## Evidence axes

- Computation: `NOT_RUN`, `RUN_UNREVIEWED`, `REPRODUCED`, `FAILED_REPRODUCTION`, `NOT_APPLICABLE`.
- Formalization: `NOT_FORMALIZED`, `PARTIALLY_CHECKED`, `FULLY_CHECKED`, `TRANSLATION_UNAUDITED`.
- Novelty: `NOT_ASSESSED`, `SEARCHED_NO_HIT`, `POSSIBLY_KNOWN`, `PRIOR_ART_FOUND`, `NOVELTY_AUDIT_PASS`.

`SEARCHED_NO_HIT` does not imply novelty.

## Acceptance gate

Route-level results normally require a main-audit pass and at least one independent `CORRECT` verdict. A project-level or high-impact claim should require at least two independent verifiers. The exact policy lives in `state/PROJECT_STATE.json`.

Only a maintainer state-change PR may write `ACCEPTED`. The accepted record must include immutable evidence references and must not infer missing axes.

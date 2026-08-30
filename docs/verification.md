# Independent verification

[简体中文](verification.zh-CN.md)

## Build the bundle

The maintainer creates a verification bundle containing only:

- frozen target and version;
- full candidate commit SHA;
- candidate files required to assess the claim;
- accepted prerequisites and public references;
- adversarial checklist;
- expected verdict vocabulary.

Do not include author discussions, reviewer conclusions, sibling attempts, desired answers, or unpublished hints unless the declared isolation level permits them.

## Verifier duties

1. Reconstruct the target and check semantic fidelity.
2. Identify the load-bearing steps before reading auxiliary material.
3. Test edge cases, sign/direction changes, hidden preconditions, and scope boundaries.
4. Verify external theorems from authoritative sources and match every hypothesis.
5. Reproduce decisive computation from the pinned commit; use a structurally separate implementation where feasible.
6. Audit finite coverage and pruning.
7. Report only `CORRECT`, `INCORRECT`, or `INCONCLUSIVE`, with exact scope.

The verifier does not improve the candidate in the same artifact. Suggested repairs are non-certifying notes; a repaired candidate returns to the author lane.

## Freshness failures

Prior access to sibling work, the maintainer's expected verdict, or an earlier version must be disclosed. If the configured independence requirement is not met, the verdict cannot satisfy the acceptance gate even when the mathematics appears correct.

## Verification counts

Count unique qualifying verification work units, not files, comments, repeated runs by the same context, or duplicated text. A verifier may not be counted twice for the same candidate revision.

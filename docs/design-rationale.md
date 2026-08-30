# Why the gates exist

[简体中文](design-rationale.zh-CN.md)

ProofRelay was distilled from a long-running, multi-worker research collaboration in which the mathematical work and the coordination system both had to survive adversarial review. The domain-specific claims were removed; the recurring failure modes became reusable controls.

| Observed failure mode | ProofRelay control |
|---|---|
| A task looked active in chat but no work existed | Durable Issue claim and dedicated branch define start |
| A delivery call failed ambiguously and risked duplicate prompts | Read back state; dispatch once; monitoring is idempotent |
| Several workers repeated the same attractive route | Route registry, structural differentiation, one owner per lane |
| A candidate moved while review was underway | Full candidate commit pin |
| A verifier had already seen sibling work | Isolation disclosure; contaminated reviews become `INCONCLUSIVE` |
| An author or friendly reviewer effectively self-certified | Separate author, maintainer-audit, and verifier roles |
| A long computation was mistaken for an infinite result | Denominator, pruning, and coverage fields; `NO_HIT_NOT_A_PROOF` |
| Exact outputs could not be reproduced later | Committed source, sanitized receipts, hashes, and artifact manifest |
| A partial theorem was reported as the full target | Frozen target plus separate route and top-level impact fields |
| “Correct”, “formalized”, and “novel” were conflated | Orthogonal status axes |
| A PR merge was treated as a truth vote | Merge preserves artifacts; a separate atomic state PR accepts claims |
| Failures disappeared during cleanup | Append-only provenance and superseding revisions |
| Repeated status checks overwhelmed useful updates | Quiet monitoring; notify only on material change or action required |

The design optimizes for conservative public claims and inspectable provenance. It intentionally accepts some process overhead when the cost of a false claim is high. Smaller projects may reduce required verifier counts, but should not collapse the roles or status axes without an explicit decision record.

# Governance and authority

[简体中文](governance.zh-CN.md)

## Maintainer powers

Maintainers freeze targets, assign lanes, audit candidates, decide whether evidence gates are met, update accepted state, protect secrets, and merge or close pull requests. They must not use those powers to erase negative evidence or waive an undisclosed conflict.

## Contributor powers

Contributors may change only the files and lanes assigned by their work unit. They may propose state changes but cannot declare acceptance, merge their own claim, or weaken verification requirements.

## Decision records

Material protocol exceptions, target changes, verification-policy changes, and acceptance decisions receive a short decision record under `docs/decisions/`. Record the context, decision, evidence, dissent, and consequences.

## Conflicts and uncertainty

When reviewers disagree, preserve both reports and mark the claim `INCONCLUSIVE` until the conflict is resolved. Missing access, contaminated context, unverifiable receipts, or insufficient authority are procedural blockers, not mathematical verdicts.

## Automation

Automations may monitor, validate, scaffold, and notify. They do not silently dispatch duplicates, approve claims, merge state changes, or reinterpret missing evidence. Unchanged state should produce no user-facing noise.

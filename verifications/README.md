# Verification artifacts

[简体中文](README.zh-CN.md)

Candidate bundles live under `verifications/candidates/<work-unit>/<candidate-sha>/`. Independent reports live under `verifications/reports/<work-unit>/<handle>-<sequence>/` and bind to that full SHA.

A verifier reports `CORRECT`, `INCORRECT`, or `INCONCLUSIVE`, records the isolation level, and does not repair the candidate being certified.

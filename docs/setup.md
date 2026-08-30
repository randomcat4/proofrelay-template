# Template setup

[简体中文](setup.zh-CN.md)

1. Replace `REPLACE_ME` in `state/PROJECT_STATE.json`, the status ledgers, and the frozen target.
2. Choose a stable project ID and protected branch.
3. Define target versions, accepted prerequisites, non-goals, and authority boundaries.
4. Set verification counts by impact. The defaults are one verifier for route-level claims and two for project-level claims.
5. Review secret patterns in `config/policy.json` and add project-specific forbidden paths.
6. Run `python scripts/print_label_commands.py` and execute the printed `gh label create` commands after review.
7. Enable branch protection: require pull requests, the `validate` check, resolved conversations, and no force pushes or deletions. Apply the rule to administrators where possible.
8. Configure CODEOWNERS or rulesets for `state/`, `contracts/`, and `.github/`.
9. Run the validator and tests locally, then open a setup PR.
10. Mark the repository as a template in GitHub settings.

Delete example placeholders only after the validator passes with project-specific replacements. Do not add copyrighted papers, private datasets, or credentials merely because the source project used local artifacts.

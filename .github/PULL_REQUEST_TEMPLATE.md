STATUS: INCOMPLETE

<!-- Allowed candidate statuses / 候选允许状态: PROVED, DISPROVED, PARTIAL, INCOMPLETE, BLOCKED, NO_HIT_NOT_A_PROOF -->
<!-- Verification PRs use / 验证 PR 使用: VERIFICATION -->
<!-- State-only PRs use / 仅状态 PR 使用: STATE_CHANGE -->

## Frozen identity / 冻结身份

- Work-unit Issue / 工作单元 Issue:
- Route and attempt / 路线与尝试:
- Target version / 目标版本:
- Base commit / 基准 commit:
- Candidate or verification commit / 候选或验证 commit:

## Result / 结果

- Exact scope / 精确范围:
- Repository artifact / 仓库工件:
- Known gaps / 已知缺口:
- Top-level target impact / 顶层目标影响:
- Novelty / 新颖性: `NOT_ASSESSED` unless separately audited / 除非另有审计，否则保持 `NOT_ASSESSED`

## Evidence / 证据

- [ ] Complete reasoning or counterexample is in a versioned file. / 完整论证或反例在版本化文件中。
- [ ] External dependencies and every applicable hypothesis are explicit. / 外部依赖及其全部适用假设已写明。
- [ ] Computation includes source, environment, exact command, exit code, hashes, denominator, and pruning justification. / 计算附源码、环境、精确命令、退出码、哈希、分母和剪枝理由。
- [ ] Finite `NO_HIT` is not presented as a general proof. / 有限 `NO_HIT` 未冒充一般证明。
- [ ] `python scripts/validate_repo.py` passes. / 仓库校验通过。

## Role and independence / 角色与独立性

- [ ] Candidate PR: I request a separate maintainer audit and independent verifier. / 候选 PR：我请求独立主审和验证。
- [ ] Verification PR: I did not author or repair this candidate, and I disclosed prior context. / 验证 PR：我未创作或修补候选，并已披露既有上下文。
- [ ] State PR: configured audit and verification gates are linked, and all ledgers change atomically. / 状态 PR：已链接配置要求的审计与验证，全部状态账原子更新。

## Security / 安全

- [ ] No credentials, session URLs, personal data, live infrastructure endpoints, or private machine details are included. / 不含凭据、会话链接、个人数据、实时基础设施端点或机器隐私。

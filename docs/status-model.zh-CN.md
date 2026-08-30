# 状态模型

[English](status-model.md)

ProofRelay 使用相互独立的状态轴。接受状态时禁止只写“完成”。

工作单元生命周期为：

`DRAFT → FROZEN → START_PENDING → CLAIMED → CANDIDATE_SUBMITTED → MAIN_AUDIT → VERIFICATION → DECIDED`

终止操作状态包括 `ACCEPTED`、`REJECTED`、`BLOCKED`、`SUPERSEDED` 和 `CANCELLED`。

候选结果使用 `PROVED`、`DISPROVED`、`PARTIAL`、`INCOMPLETE`、`BLOCKED`、`NO_HIT_NOT_A_PROOF`。这些只是作者主张，在审查前不是项目结论。

主审状态为 `NOT_REVIEWED`、`MAIN_AUDIT_PASS`、`MAIN_AUDIT_FAIL`、`MAIN_AUDIT_INCONCLUSIVE`；独立验证只用 `NOT_VERIFIED`、`CORRECT`、`INCORRECT`、`INCONCLUSIVE`；隔离等级为 `STRICT_FRESH`、`CONTEXT_ISOLATED`、`CROSS_LANE`、`NOT_INDEPENDENT` 或 `UNKNOWN`。

计算、形式化和新颖性分别记账。`SEARCHED_NO_HIT` 不代表新颖。路线级结果通常需要主审通过和至少一份独立 `CORRECT`；项目级或高影响主张建议至少两名独立验证者。精确策略写在 `state/PROJECT_STATE.json`。

只有维护者状态 PR 可以写入 `ACCEPTED`，且必须引用不可变证据，不能补猜缺失状态。

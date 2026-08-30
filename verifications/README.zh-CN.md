# 验证工件

[English](README.md)

候选包位于 `verifications/candidates/<work-unit>/<candidate-sha>/`。独立报告位于 `verifications/reports/<work-unit>/<handle>-<sequence>/`，并绑定完整 SHA。

验证者只给 `CORRECT`、`INCORRECT` 或 `INCONCLUSIVE`，记录隔离等级，且不能修补自己正在认证的候选。

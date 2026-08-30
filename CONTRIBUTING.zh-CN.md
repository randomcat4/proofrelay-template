# 贡献指南

[English](CONTRIBUTING.md)

感谢你改进 ProofRelay。请先建立冻结工作单元 Issue，再使用专用分支和 Pull Request；不得直接推送受保护分支。

每项贡献必须：

1. 标明冻结目标、路线、工作单元 ID 和基准 commit；
2. 把完整成果放入版本化文件，而不是只留在聊天或评论中；
3. 严格区分 `PROVED`、`DISPROVED`、`PARTIAL`、`INCOMPLETE`、`BLOCKED` 与 `NO_HIT_NOT_A_PROOF`；
4. 对计算主张附可复现代码和去敏收据；
5. 保留失败和被取代的工作；
6. 不提交凭据、个人数据或实时基础设施信息；
7. 通过 `python scripts/validate_repo.py` 和标准库测试。

候选作者不得批准自己的主张。修改状态账必须由维护者单独发起 PR，并链接候选、主审和验证证据。

完整契约见[工作流](docs/workflow.zh-CN.md)。

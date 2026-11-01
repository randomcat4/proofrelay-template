# GitHub 协作：任务、交付与审查各司其职

## 基本映射

- Issue：一个值得单独认领的数学工作包。说明目标、来源、前置条件、涉及文件、交付标准和 blocker。
- Draft PR：这个工作包的代码与解释的实际变化；工作中即可创建，持续提交到原 PR。
- PR Review/comment：语义、证明与可维护性的独立反馈。不默认再开“验证 PR”和“状态变更 PR”。
- main：项目已接纳的内容。合并仅按项目权限执行；研究完成程度仍由实际代码和说明体现。
- Actions：编译与文档构建，不用一堆自定义状态检查假装证明检查。

一个 Issue 可以关联多个合理实现 PR；一个 PR 可覆盖紧密耦合的小引理。不为每个 `have` 或 helper 创建任务。
父/子 Issue 表示工作拆分；Blocked by 表示工作前置条件，二者不相同，更不是真实证明依赖 DAG。

## 工作前读取，避免重复认领

读相关 open/closed Issues、现有 PR、评论、分支和目标文件，确认任务是否已有负责人或已交付。
主实例完成认领/分配后再启动对应工作者。GitHub 指派配合宿主实际生命周期管理，不承诺它是原子分布式锁。
不自建租约系统；有多主实例冲突时在原 Issue 明确协调，不同时修改同一文件。

已授权使用 gh 时的常见动作：

```bash
gh issue view NUMBER --repo OWNER/REPO
gh pr view NUMBER --repo OWNER/REPO
gh pr diff NUMBER --repo OWNER/REPO
```

先用实际 `gh ... --help` 核对版本。支持原生依赖时可使用：

```bash
gh issue edit NUMBER --repo OWNER/REPO --add-blocked-by PREDECESSOR
gh issue view NUMBER --repo OWNER/REPO --json blockedBy,blocking
```

版本或 connector 不支持时，用 GitHub 网页 Relationships，或在 Issue 正文写清 `Blocked by #...` 作为暂时人工约定。正文链接不是原生关系；不要说设置已成功。不得临时发明一个 API 或静默换身份。

## PR 范围与下游

PR 应是可独立审阅的增量。能先合入稳定定义/辅助引理就优先小 PR；紧密依赖可使用明确基线的 stacked PR，但先读项目习惯。
上游有新提交时，检查下游实际接口并重建；不因为 Issue closed 就假定依赖永远不变。
每个 PR 写明：对应 Issue、精确结果、变化文件、数学解释、实际执行的命令、未完成部分和需要的审查。
语义修改与普通 proof 修复分开说明。未通过独立审查时保持待审，不用 `Closes #...` 误关长期目标。

## CI 接入

优先现有 Actions 和官方 Lean action。`assets/templates/lean-ci.yml` 是仅构建的可选示例，不部署 Pages、不写回状态、不安装模型服务。普通构建能容忍 `sorry`，所以该模板不是完整验收器；仍按 `acceptance.md` 检查交付定理的传递依赖。
不启用 `pull_request_target` 执行不可信提交代码。不向 fork PR 注入秘密，不写脚本扫描和上传用户电脑凭据。

## 同账号多个 Agent

不能用同一账号模拟多个 GitHub 人类批准。报告由哪个隔离上下文检查了什么；如果无法提交独立 Review，就以普通审查 comment 留结论，等待具有实际权限的维护者处理。

## 恢复

从当前代码、Issue/PR 讨论、Review 和 CI 结果恢复。路线图只帮助理解目标，不能用旧摘要盖过新代码。不创建额外 `state.json`、双语状态账或自动镜像看板。

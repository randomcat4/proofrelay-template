# 模块依赖与加载顺序

本文件是 Skill 的阅读地图，不是调度程序或研究项目账本。不称为 DAG，也不据此统计研究完成率。

## 1. 内部依赖

| 阶段/模块 | 前置输入 | 必须加载 | 输出与下游 |
|---|---|---|---|
| 启动与接入 | 目标、仓库/材料访问、授权范围 | `workflows/start.md` + `references/boundaries.md` + `references/environment.md` | 项目定位、能力缺口、最小接入；供后续全体使用 |
| 来源与陈述 | 可阅读原文；相关定义 | `references/statements.md` + `agents/formalizer.md` | 准确的定义与 Lean 类型、未决歧义；交语义审查 |
| 语义审查 | 原文和实际 Lean 声明，非作者预期结论 | `agents/statement-reviewer.md` + `references/statements.md` | 陈述差异及裁决；决定哪些接口可以下发证明 |
| 路线规划 | 已明确的目标和接口、库可用情况 | `references/graphs.md` + `references/github.md` | 形式化路线图、工作包、Issue 关联 |
| 并行委派 | 前置接口、路径所有权、真实宿主能力 | `references/delegation.md` + 对应 `agents/*.md` | 子任务交付；主实例合入集成分支检查 |
| Lean 证明 | 对应声明和确切项目环境 | `references/proving.md` + `agents/prover.md` | 编译候选、缺口、数学说明；进入独立审查 |
| 数学叙述 | 实际陈述、现有证明和原文 | `references/readability.md` + `agents/expositor.md` | 人类可读结果页；不能代替证明或编译 |
| Blueprint | 前述结果页；兼容文档工具 | `references/blueprint.md` + `references/graphs.md` | 可读站点和明确来源的图；未安装可用文档退路 |
| 最终审查 | 集成后的代码、文本、实际构建结果 | `workflows/deliver.md` + `references/acceptance.md` + `agents/reviewer.md` | 分项结论、PR Review 或审查说明、交付与剩余义务 |
| 恢复/修复 | 当前分支、Issue/PR、真实文件 | `workflows/resume.md` + 受影响模块 | 重建当前工作，不导入旧“通过”标签 |

“必须加载”指执行该职责前读取，不要求所有阶段都预先读取全部文件。
所有运行模块可由 `SKILL.md` 一跳定位；这里的依赖是先决材料，不是要求自动执行被引用文件。

## 2. 可并行与不可并行

可以并行：不同已定接口的证明；不同结果的来源阅读；独立工作树的编译；已有确定材料的叙述草稿。
必须等待：目标对象尚不明确的最终 statement；尚未合入且未读取的依赖接口；新定义意义未核实的下游定理；尚未产生完整候选的最终验收。

声明冻结不等于证明完成。允许利用清楚标注的占位接口验证上层组织是否可行，但所有传递占位仍是未完成义务。
不得让“上游 Issue 已关闭”取代读取其实际 Lean 声明、代码和审查范围。

## 3. 外部依赖不是隐藏前提

| 能力 | 是否必需 | 检查方式 | 不可用时 |
|---|---|---|---|
| 文件读写、shell | 代码执行阶段必需 | 宿主实际工具 | 只给计划/文本，不能声称修改成功 |
| Lean/Lake 与项目版本 | 机械验证必需 | 读 `lean-toolchain`，探测本机已安装工具链后运行 | 来源/陈述审查可继续；Lean 结果标未编译 |
| Mathlib/项目依赖 | 按目标需要 | 现有 lakefile、manifest、对应库与缓存 | 不换模型/全局版本伪装可用，不擅改依赖 |
| GitHub connector 或 gh | 远程协作需要 | 读仓库和现有 Issue/PR | 本地工作可继续，远程动作明确未执行 |
| 真实子智能体/新上下文 | 并行/独立性需要 | 宿主支持的真实调用 | 顺序工作；缺独立审查就保留待审 |
| Lean LSP/MCP | 可选效率工具 | 当前工具清单、项目连接 | shell 搜索、文件级编译和诊断 |
| Verso Blueprint | 可选首选文档后端 | 项目依赖和本地 `vbp --help` | 旧 Blueprint 或 Markdown/LaTeX |
| 实际依赖提取器 | 发布实际 DAG 时需要 | 当前工具的导出和边来源 | 报告未提取，不编造 DAG |
| 外部证明服务 | 默认不用 | 明确授权、费用/数据边界 | 直接 coding-agent + 本地 Lean |

## 4. 上游材料的依赖闭包

本包完整收录两个自包含上游方法文件：`references/upstream-lean-proof.md` 和 `references/upstream-mathlib-build.md`。它们没有需要另外安装的 Skill 内部文件。

其余来源经过重写适配，不依赖未打包的上游 controller、hooks、计数器、清单生成器或登录服务。Blueprint/LSP/Lean 的命令仍需要实际软件；提示词不能替代软件安装。API 和数据格式变化时以当前项目版本为准，不全局升级。

## 5. 冲突处理

用户当前授权和项目规则约束具体操作。本包路由与边界约束所选流程；参考的上游通用方法不能扩大权限。
例如：上游建议最短证明，本包以可维护与数学解释优先；上游建议获取缓存，本包先确认需要及授权；上游写 `main` 的文档接口不意味着用户旧工具链支持。

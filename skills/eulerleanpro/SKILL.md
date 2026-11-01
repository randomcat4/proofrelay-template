---
name: eulerleanpro
description: 将重大数学进展、完整证明或论文独立形式化为 Lean 4 工程，并交付人类可读的数学说明、形式化路线图和实际证明依赖 DAG。用于整篇/整项形式化、接手修复和独立验收；不替代研究过程中随手核验承重引理的轻量 Lean 模式。
license: "See LICENSE, SOURCES.md and licenses/"
compatibility: "需要可读写项目文件和执行 Lean/Lake 的 coding agent。GitHub、真实子智能体及 Blueprint 为按任务使用的能力；没有这些能力时明确降级，不模拟成功。"
metadata:
  version: "0.1.0"
  language: "zh-CN"
---

# EulerLeanPro

将重大数学结果做成**可以编译、可以复核、可以阅读**的形式化成果。数学解释不是附赠品。

本包的相对文件路径以 `eulerleanpro/` 安装目录为根；Lean、Git 和 GitHub 命令在目标项目目录执行。不要在 Skill 安装目录生成研究工件。

## 使用边界

本 Skill 自包含，不依赖 `math-theorem`、`math-ultra` 或用户的私有研究内核。
可以接收它们的证明、反例和文献，但不继承“已证明”的标签。已有原文、项目和明确任务时直接开始检查，不重新索要这些材料。

只需核验研究中一个承重引理时，不启动整套工程；使用宿主已有轻量 Lean 能力。用户明确指定本 Skill 做局部修复时，仅加载相关模块。

## 先读与分流

先读项目 `AGENTS.md` / `CLAUDE.md`、目标材料、已有 Lean 工程、README，以及相关 Issue/PR。
然后读取 [边界](references/boundaries.md)、[环境与项目](references/environment.md) 和 [模块依赖](DEPENDENCIES.md)。
不要一次加载所有参考文件，也不要把整个 Skill 复制进每个子智能体。

| 任务 | 工作流 | 必要参考 |
|---|---|---|
| 首次形式化或接入旧库 | [启动/接入](workflows/start.md) | [原文与陈述](references/statements.md)、[GitHub](references/github.md) |
| 展开重大结果的形式化 | [形式化主流程](workflows/formalize.md) | [委派](references/delegation.md)、[证明迭代](references/proving.md)、[可读成果](references/readability.md) |
| 接手、修复或继续旧工程 | [恢复/修复](workflows/resume.md) | [环境](references/environment.md)、[证明迭代](references/proving.md) |
| 审查或最终交付 | [审查/交付](workflows/deliver.md) | [验收](references/acceptance.md)、[可读成果](references/readability.md)、[路线图与 DAG](references/graphs.md) |
| 使用/增加数学蓝图网站 | 先核对现有项目再选工具 | [Blueprint 适配](references/blueprint.md)、[路线图与 DAG](references/graphs.md) |

## 工作顺序与真正的前置条件

1. **定位对象。** 明确原文版本、目标定理、允许的证明范围、现有工具链和用户授权；不创建平行任务库。
2. **审查陈述。** 将来源写成准确 Lean 类型，独立核对量词、定义、隐含类型类与假设。陈述可以先有 `by sorry`；这只是开发占位，不能交付为证明。
3. **形成形式化路线图。** 用人类能读的数学解释划分承重结果和工作包。只为值得认领的工作包建立 Issue，不给每个 helper 开任务。
4. **按依赖并行。** 已审查的定义和接口先稳定下来，再分派可独立的引理。上层可在明确未证的接口上做集成探路，但不得据此宣称完成。
5. **证明与叙述一起完善。** 使用 Lean 的真实反馈。作者交付 Lean 代码、数学主线和剩余义务；叙述者不得替作者填补数学漏洞。
6. **独立审查并交付。** 构建目标与依赖、检查公理/占位、复核原文忠实性，另做人类可读性审读。缺什么就报告什么。

前置条件不满足时只阻塞受影响任务，其他独立任务可继续；不要因局部卡点冻结整个项目。授权范围内的常规证明迭代无需每一步请求确认。

## 角色入口

这些是给宿主真实子智能体的任务提示词，不是自动注册的 agent 或后台服务。

| 角色 | 文件 | 边界 |
|---|---|---|
| 总协调 | [coordinator](agents/coordinator.md) | 读 Issue/PR，组织工作，不自批自己写的证明 |
| 陈述形式化者 | [formalizer](agents/formalizer.md) | 来源 → Lean 定义与陈述，不暗中改题 |
| 独立语义审查者 | [statement-reviewer](agents/statement-reviewer.md) | 对照原文与实际 Lean 类型，审查隐含假设 |
| Lean 证明者 | [prover](agents/prover.md) | 检索、编译、修订与交付 |
| 数学叙述者 | [expositor](agents/expositor.md) | 人类可读证明、对照和导航，不伪造理由 |
| 最终独立审查者 | [reviewer](agents/reviewer.md) | 机械状态、语义、阅读质量分别作结论 |

没有真实子智能体能力就顺序工作并明确未做独立上下文复核。不能在同一上下文改个角色名便称独立。

## 两种图，只保留一个 DAG 名称

**形式化路线图**：规划目标、候选路线和任务关系，可修订；GitHub 负责认领、阻塞、PR 和 Review。

**Lean 证明依赖 DAG**：从实际 Lean 声明/证明提取的依赖。边统一为“使用者 → 被依赖者”。手写 `uses`、Issue 阻塞、import 图都不能冒充它。
Blueprint 的手工和自动边可能混合；不能将混合展示改个标题就称真实 DAG。投影视图要说明省略和截断。详见 [图的语义](references/graphs.md)。

## 必须保留的约束

- Git/ GitHub 已管版本与协作；不新造调度器、租约、数据库、哈希账本或证明状态机。
- 不改现有项目工具链来掩盖编译错误，不覆盖他人修改，不擅自公开私库或部署 Pages。
- 不把目标结论塞进参数、structure 字段、类型类或新公理。不得静默弱化结论。
- `lake build` 成功、图是绿色或没有搜索到 `sorry`，均不足以单独宣布目标完成。
- 内核接受的是实际陈述；原文是否被忠实表达另行审查。原文可能有错，有证据就明确报告，不因已发表而替其免责。
- 开发允许可见占位，交付范围及其传递依赖不允许 `sorryAx`。完整性与公理允许范围按项目真实检查。
- 数学说明必须自包含：陈述、全部实质假设、证明主线、关键引理用途、Lean 对应与未覆盖部分。禁止把 tactic 清单当证明解释。
- 默认不自动合并 PR、关闭未完成目标、投稿、发布或调用收费外部证明服务。

## 模板与按需补充

模板按需要选取，不要求全部生成：
[任务 Issue](assets/templates/issue.md)、[PR](assets/templates/pull-request.md)、[委派单](assets/templates/task-brief.md)、[结果页](assets/templates/result-page.md)、[路线图](assets/templates/roadmap.md)、[审查](assets/templates/review.md)、[项目指令片段](assets/templates/AGENTS.fragment.md)、[CI 示例](assets/templates/lean-ci.yml)、[CI 接入说明](assets/templates/ci-notes.md)。

上游原文仅按需读：[Lean 证明方法](references/upstream-lean-proof.md)、[Mathlib 构建](references/upstream-mathlib-build.md)。
本包的任务范围、阅读质量与权限边界优先于这些参考件的通用建议。它们不是另两个待安装的 Skill。

## 完成时返回

先报实际范围和结果，再给原文/数学说明、Lean 声明、构建/审查、Issue/PR 的链接。
分别说清机械完成情况、原文一致性、人类可读性及剩余缺口。未实测的不能写成通过。
研究内容应进入用户项目，Skill 安装目录保持只读。

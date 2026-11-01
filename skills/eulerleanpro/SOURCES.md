# 来源、复用方式与许可证

集中来源声明。整理日期：2026-11-01。包名：eulerleanpro 0.1.0。

本包明确使用公开 Skill 和文档，不把改写内容冒称完全原创。上游可能继续变化；下列文件是本次实际读取的来源。Git blob 标识仅用于说明所收录的上游文件版本，不是要求用户研究项目建立 SHA/哈希账本。

## 1. 逐字收录的上游 Skill 文件

### leanprover/skills — Apache-2.0

项目：https://github.com/leanprover/skills
许可证：https://github.com/leanprover/skills/blob/main/LICENSE
本包保留许可证：`licenses/Apache-2.0.txt`。

| 上游文件 | 本包文件 | 复用方式 |
|---|---|---|
| `skills/lean-proof/SKILL.md` | `references/upstream-lean-proof.md` | 内容逐字收录，只改变存放路径/文件名 |
| `skills/mathlib-build/SKILL.md` | `references/upstream-mathlib-build.md` | 内容逐字收录，只改变存放路径/文件名 |

上游链接：
- https://github.com/leanprover/skills/blob/main/skills/lean-proof/SKILL.md
- https://github.com/leanprover/skills/blob/main/skills/mathlib-build/SKILL.md

实际读取 Git blob：`24bb64b9bf938db4a5793f1e9293e4ccd7bb6bde`；`c5d6ff6dd5e119db9f41708e47b1bcc68567b4c4`。
这两个文件自包含，没有悬空的上游内部依赖；不是自动加载的额外 Skill，也不需要再安装上游插件。

本包的整合规则在 `references/proving.md` / `environment.md`：保留小步诊断和难点优先，不强制最短字符数；缓存下载需服从用户授权；Mathlib 自身 targets 不套用到下游项目。原文中的一般建议不扩大本包权限。

## 2. 改写/适配的来源

### CBirkbeck/mathlib-quality — MIT

来源：https://github.com/CBirkbeck/mathlib-quality/blob/main/skills/mathlib-quality/references/blueprint-conventions.md
实际读取范围：1–390 行，重点为可读数学、命题/证明块与反模式。
Git blob：`bea2d9f71937df91f4d5b74b12146bbfe5b60a30`。
许可证：https://github.com/CBirkbeck/mathlib-quality/blob/main/LICENSE
保留原版权及许可证：`licenses/mathlib-quality-MIT.txt`（原文 Copyright (c) 2024）。

落到本包：`references/readability.md`、`agents/expositor.md`、`assets/templates/result-page.md` 以及 Blueprint 内容组织方法。
改动：中文改写，删去上游插件/命令/hooks 的依赖；用项目现有文档承载；明确不能删除类型类承载的实质假设；证明说明以数学完整性为准而非固定一两段；不继承上游把图颜色当成完整性的概括。

### StatLean/Stat-Lean — Apache-2.0

来源：
- https://github.com/StatLean/Stat-Lean/blob/main/website/CONTRIBUTING.md （本次读取 1–210 行）
- https://github.com/StatLean/Stat-Lean/blob/main/website/README.md
- https://github.com/StatLean/Stat-Lean/blob/main/CONTRIBUTING.md

贡献文档 Git blob：`68090f39c7a5335ca44a498a0e39d4c1d400d266`。
许可证：https://github.com/StatLean/Stat-Lean/blob/main/LICENSE
保留许可证：`licenses/Apache-2.0.txt`；上游 `Copyright 2024 Junwei Lu` 另保留于 `licenses/StatLean-attribution.txt`。

落到本包：`references/readability.md`、结果页/假设对照模板、人类可读性审查和图的范围说明。
改动：将原网站的数据/UI 契约化为可移植 Markdown/Blueprint 要求，不复制 React 网站或自制数据校验器；不强制每项成果维护 results.json；不照搬对已发表来源默认免责的写作倾向，确认原文问题时按证据报告。可视化依赖的过滤/截断不被当作完整证明证书。

### leanprover/lean-action — Apache-2.0

来源：https://github.com/leanprover/lean-action#quick-setup
落到本包：`assets/templates/lean-ci.yml`、`assets/templates/ci-notes.md`。
改动：保留官方 action 基本调用，使用 PR/手动触发、只读 contents 权限，明确 build 不等于无 sorry，不加入 Pages 和写回动作。没有在本次环境实际运行 Actions。
许可证：https://github.com/leanprover/lean-action/blob/main/LICENSE
完整 Apache-2.0 文本随包保留。

## 3. 技术参考，未整套复制或设为隐藏运行依赖

### Agent Skills 与复杂 Skill 组织

- https://agentskills.io/specification
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://developers.openai.com/plugins/concepts/skills
- https://developers.openai.com/blog/skills-agents-sdk
- https://developers.openai.com/blog/eval-skills

用途：入口路由、按需加载、短而准确的描述、模块化参考/模板、行为回归。没有把整篇文档收录到包中。

### Verso Blueprint

- https://github.com/leanprover/verso-blueprint
- https://github.com/leanprover/verso-blueprint/blob/v4.35.0/skills/verso-blueprint/references/vbp.md
- https://github.com/leanprover/verso-blueprint/blob/v4.35.0/doc/MANUAL.md

本次 connector 返回的 vbp 文档 Git blob：`a82ae4b44e596db0a7eea37debb9b0f99a78515e`。
用途：可用命令、生成快照的局限、自动/手工边分开、声明完成与 sorry 检查边界。`references/blueprint.md` 是按本包需求写的接口说明，不包含上游整个 Skill、生成器或 JSON 控制程序。适用版本须在目标工程再次确认。

### 传统 Blueprint / LeanArchitect

- https://github.com/PatrickMassot/leanblueprint
- https://github.com/hanwenzhu/LeanArchitect
- https://github.com/leanprover-community/LeanProject

用途：沿用既有工程、正式声明关联和依赖推断的范围；未复制代码，未自动运行迁移器。

### GitHub 原生协作与隐私

- https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://code.claude.com/docs/en/skills
- https://developers.openai.com/codex/skills

用途：Issue 阻塞关系、CLI 版本差异、Pages 隐私及宿主安装位置。未复制其文档全文。

## 4. 本包新增与授权范围

新增内容：eulerleanpro 的两类 Lean 使用边界、工作流与角色整合、内部依赖说明、GitHub 工作方式、路线图/真实 DAG 分离、跨工具降级、测试场景和教学示例。新增部分按 Apache-2.0 提供；不改变上游 MIT/Apache 内容原有权利与声明。

本包没有复制用户私库文件或未公开提示词，没有引入 math-ultra 的控制器/账本，也没有将未验证的外部项目宣传当作能力保证。
源声明与许可随包保留。继续复制或发布本包时保留这些文件；此处的来源信息不表示上游作者认可或验收本包。

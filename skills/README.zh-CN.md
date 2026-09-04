# Agent Skills

[English](README.md)

本目录随模板附带可安装的 [Agent Skills](https://github.com/anthropics/skills)，与 ProofRelay 协议配套使用。每个 skill 是一个自包含目录，以 `SKILL.md` 为入口；仓库本身不引入任何运行时依赖。

## 内置 skill

| Skill | 用途 |
|---|---|
| [`math-theorem/`](math-theorem/SKILL.md) | 研究级定理发现、证明、证伪、最小前提修复与新颖性认证。强制冻结命题、隔离证明实例、新上下文验缝、既有工作占位审计，并对"命题为真""证明完整""结论新颖"分开裁决。 |

`math-theorem` 与 ProofRelay 刻意对齐：它的运行工件（冻结命题、路线注册表、引理账、溯源记录、裁决书）对应本仓库的 `contracts/`、`routes/`、`attempts/`、`verifications/` 与 `state/` 生命周期。skill 负责工作单元内部的数学纪律，ProofRelay 负责这些工作在 GitHub 上如何被主张、审计和保全。

## 安装方式

把 skill 目录复制到你的 agent 的 skill 搜索路径即可。目录名必须保持 `math-theorem`，且 `SKILL.md` 必须位于其根目录。

### Codex CLI

```bash
# Linux / macOS
mkdir -p ~/.codex/skills
cp -r skills/math-theorem ~/.codex/skills/
```

```powershell
# Windows PowerShell
Copy-Item -Recurse -Force skills\math-theorem "$HOME\.codex\skills\math-theorem"
```

### 千问办公（QwenWork）

```bash
# Linux / macOS
mkdir -p ~/.qwenworkcn/skills
cp -r skills/math-theorem ~/.qwenworkcn/skills/
```

```powershell
# Windows PowerShell
Copy-Item -Recurse -Force skills\math-theorem "$HOME\.qwenworkcn\skills\math-theorem"
```

### 其他 agent

任何支持 Agent Skills 格式的 agent 都可以使用，指向 `math-theorem/` 的一份拷贝即可：

- Claude Code：`~/.claude/skills/math-theorem/`（用户级）或项目内的 `.claude/skills/math-theorem/`。
- 项目级：放到你的 agent 扫描 skill 的位置，例如由本模板创建的仓库中的 `.agents/skills/`。

### 验证安装

新开一个会话，发出一个触发请求，例如：

> 证明或反驳：对任意鞅 (M_n) 和任意几乎处处有限的停时 τ，都有 E[M_τ] = E[M_0]。

agent 应当读取 `SKILL.md`、冻结命题、建立运行目录工件，而不是随口作答。如果它直接给出非正式回答，说明 skill 未被加载，请检查目录名和路径。

## 运行要求

- 能读取 `SKILL.md` 并执行 shell 命令的 agent。
- Python 3（仅标准库）：用于 `math-theorem/scripts/validate_run.py`，检查运行目录结构是否齐全。结构检查不等于数学正确性认证。
- 可选：Lean 4 工具链（elan）。skill 会探测项目钉死的 `lean-toolchain`，不会悄悄换用其他版本。
- 可选：子智能体能力。具备时，证明与验证在隔离实例中进行；不具备时，skill 退化为互不继承草稿的独立回合。

## 兼容性说明

`SKILL.md` 采用通用 Agent Skills 约定：YAML front matter 含 `name` 与 `description`，正文为指令主体，`references/` 按需加载。已在 Codex CLI 和千问办公（QwenWork）上验证。skill 内不含任何服务凭据或机器敏感信息；`SKILL.md` 中有一处 Lean 探测路径示例，可按你的环境自行修改。

## 更新 skill

用新版本目录整体替换已安装的拷贝，然后重新执行上面的验证请求。skill 以普通目录形式发布，没有独立版本标签；如需可复现，请记录你拷贝时对应的模板提交哈希。

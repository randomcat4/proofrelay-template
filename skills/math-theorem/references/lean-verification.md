# Lean 机械核验协议

Lean 是数学证明的机械检查层，不替代自然语言命题忠实性、先行工作和数学价值审计。满足条件时应实际运行，而不是只写“可以形式化”。

## 何时使用

下列情况至少进行一次 Lean 可行性与版本检查：

- 用户明确要求 Lean、形式化证明或机器验证；
- 当前工作区已有 `lean-toolchain`、`lakefile.toml` 或 `.lean` 文件；
- 研究级完整候选已经出现，且关键对象在 Mathlib 中已有成熟表示；
- 某个高风险关键引理足够精确，能以较低成本单独形式化；
- 需要排除隐含前提、类型错误、缺失分支或错误调用库定理。

紧凑定理优先做完整形式化。长证明若全量形式化明显超出预算，先形式化最承重、最易误判的引理，并把覆盖范围写清；只有完整目标通过时才能写 `LEAN_FULLY_CHECKED`。

## Windows 本机工具链发现

每次都重新探测，不假定 PATH 已配置：

1. 先读取项目根的 `lean-toolchain`；项目钉死的版本优先于全局版本。
2. 检查 `Get-Command lean,lake,elan -All`。
3. 若 PATH 没有，再检查：

```text
E:\Lean\elan\bin\elan.exe
E:\Lean\elan\bin\lean.exe
E:\Lean\elan\bin\lake.exe
```

使用 E 盘 elan 时在当前进程设置：

```powershell
$env:ELAN_HOME = 'E:\Lean\elan'
& 'E:\Lean\elan\bin\elan.exe' toolchain list
& 'E:\Lean\elan\bin\lean.exe' --version
& 'E:\Lean\elan\bin\lake.exe' --version
```

当前已知安装是 Lean 4.32.0 / Lake 5.0.0，但运行时仍以实际输出为准。`E:\Lean\mathlib-cache` 是可复用缓存位置，不能仅因缓存存在就声称某个项目已经构建通过。

## 版本与下载纪律

- 有项目时严格使用 `lean-toolchain`；不要用全局 4.32 强编需要其他版本的项目。
- 先用 `elan toolchain list` 判断钉死版本是否已安装。
- 在确认版本已安装前，不要从该项目目录运行 shim 或 `elan show`；elan 可能立即尝试联网同步缺失工具链。
- 缺失工具链、Mathlib checkout 或大缓存时，不要在普通数学任务中自动重下载。
- 用户明确要求完整 Lean 验证，或当前任务明确以构建通过为交付物时，安装项目钉死工具链属于任务范围；仍需先说明预计会新增的工具链/缓存。
- 不升级项目的 Lean 或 Mathlib 版本来消除错误，除非用户明确要求迁移。

## 验证阶梯

### L0：工具链 smoke

记录 `lean --version`、`lake --version` 和项目 `lean-toolchain`。这只证明工具可运行。

### L1：孤立引理

在现有项目或临时最小项目中编译一个精确引理。记录自然语言原句、Lean statement 和二者的差异。

### L2：目标文件/项目构建

运行项目规定的 `lake env lean <file>`、`lake build` 或等价命令。保留 stdout/stderr、退出码和工具链版本。

### L3：最终证书

若项目提供 Comparator、axiom sweep、专用 checker 或 CI 同款命令，实际执行并记录。只有这一层成功且自然语言—形式陈述忠实性通过，才可按项目口径写完整机械认证。

## 禁止假通过

在拟认证范围内搜索并拒绝：

- `sorry`、`admit`；
- 为目标新增的 `axiom`；
- 用 `unsafe` 绕过逻辑检查；
- 偷改定理签名、删前提或缩小量词；
- 只编译辅助文件却声称主定理通过；
- 只运行有限枚举却声称一般定理通过。

对最终 theorem 运行 `#print axioms <theorem>` 或项目等价的公理审计，区分 Lean/Mathlib 允许的基础公理与为目标新增的假设。

## 结果状态

- `LEAN_FULLY_CHECKED`：冻结完整目标、证明和所需证书实际通过。
- `LEAN_PARTIALLY_CHECKED`：仅部分关键引理或有限组件通过，列出未覆盖部分。
- `LEAN_BUILD_FAILED`：给出首个实质错误和复现命令。
- `LEAN_TOOLCHAIN_MISSING`：所需钉死版本不存在且本轮未获授权安装。
- `LEAN_TRANSLATION_UNAUDITED`：Lean 内核接受了编码，但尚未确认它忠实表达原问题。

Lean 通过不能自动消除最后一种状态。

## 运行工件

在数学运行目录中使用：

```text
formal/
├── README.md
├── Main.lean
└── build.log
verifications/
└── lean.md
```

`verifications/lean.md` 至少记录：冻结命题版本、形式 statement、覆盖范围、工具链、命令、退出码、axiom/sorry 扫描、忠实性审计和最终状态。

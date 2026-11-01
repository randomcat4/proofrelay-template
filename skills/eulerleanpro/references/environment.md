# 项目与工具链

## 首轮只读定位

检查当前目录、Git 分支及未提交改动、项目指令、README、`lean-toolchain`、`lakefile.lean` / `lakefile.toml`、`lake-manifest.json`、库入口、CI 和文档入口。
Git 远程 URL 可能含凭据，只在工具内检查，不原样写进日志或报告。
确认用户目标属于本仓库而非机器上的邻近项目；不递归搜索未授权目录。

先读工具链文件，再查 `elan toolchain list` 和可执行文件位置。Lean shim 在项目目录可能自动下载缺失版本，因此“看版本”也可能触发联网；缺失时先说明安装需要及授权边界。
不写死盘符、用户名、Lean/Mathlib 版本。现有项目版本优先，不为了让新 Blueprint 可用而升级数学库。

## 构建阶梯

1. 若已有项目基线，运行现有项目/CI 的最小合理目标，区分原有失败与本次修改引入的失败。
2. 开发内循环：真实 LSP goal/diagnostics，或目标文件编译。不是编一个没导入主目标的辅助文件。
3. 在生成 `.olean` 缺失、源依赖已变或工作树刚切换时，先构建相关依赖；不能仅对着旧 `.olean` 编目标。
4. 集成检查：执行项目声明的目标，确保交付目标被库入口/明确 target 覆盖。完整项目 `lake build` 若不包含新增文件，仍需显式检查该文件。
5. 最终公理与占位检查见 `acceptance.md`。

常见命令（先确认已装项目工具链，不必全部执行）：

```bash
elan toolchain list
lean --version
lake --version
lake build
lake env lean MyProject/Result.lean
```

`lake env lean` 不替你重建所有变化的 import。较新项目可能用 `lake lean <file>` 构建依赖并检查文件；先看本地 `lake --help`，不假定旧 Lake 有这个命令。

## 缓存和资源

已匹配依赖的 Mathlib 项目按需使用 `lake exe cache get`。`cache get!` 只在确有缓存损坏且允许重新下载时使用，不把强制重下载作为普通第一步。
不要在每个子智能体重新安装 Lean、复制完整 Mathlib 或运行全库构建。优先现有缓存、窄目标和宿主并发限制。
多个工作树不要同时写同一个可变构建目录；只读共享已有依赖缓存不等于共享未同步的构建状态。

## 新工程与文档后端

新 Lean 工程先用官方/项目维护的模板或 Lake 入口建立，并选择明确工具链和库版本；不是本包硬带一个已经过时的 `lean-toolchain`。
文档依赖与数学库若不兼容，可把 Blueprint 放独立文档工程，或先交付 Markdown/LaTeX。不要让排版依赖拖住已经可运行的数学工程。

更细的 Mathlib 构建原文在 `upstream-mathlib-build.md`；其中 Mathlib 专有 targets 仅用于 Mathlib 自身，不直接套到普通下游项目。

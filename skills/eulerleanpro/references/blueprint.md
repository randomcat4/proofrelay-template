# Blueprint 文档后端：现有工具优先

参考 leanprover/verso-blueprint 的 Agent Skill、`vbp` 文档与手册，以及 LeanBlueprint/LeanArchitect 的公开文档。这里是本包的适配说明，不要求另装那些 Skill。

## 选后端

现有项目用什么就先沿用什么。新工程优先评估与项目工具链兼容的 Verso Blueprint；传统 LeanBlueprint 仍可用。没有兼容后端时，先交付完整 Markdown/LaTeX 数学说明；网站集成可作为单独工作包，不能升级数学项目来凑排版。

版本敏感：本次查阅的 Verso 文档来自仓库默认分支，工具返回的文件链接位于 `v4.35.0`。这是文档观察，不是本包强制 Lean 4.35，也不是用户环境已安装该版本。

## Verso：探测后再用

从对应文档工程根运行，本地命令支持时：

```bash
lake exe vbp --help
lake exe vbp discover
lake exe vbp build
lake exe vbp query selectors
lake exe vbp query node LABEL
lake exe vbp query status LABEL
lake exe vbp query work-queue
```

先确认现有 `lean-toolchain` 已安装，再调用 shim；上述命令不是安装器。
`query` 读取生成快照，不重新编译源码；修改后先重建。`check` 审计已生成工件的一致性，不证明源码新鲜。
当前 JSON 格式标为不稳定，不写一个长期依赖固定字段的自制控制器。按本地帮助与实际返回逐项判断。

`complete: true` 的文档语义是检查覆盖内没有可达 `sorryAx`，不是原文语义正确或全部公理自动获批。还要执行项目的公理/语义验收。
`work-queue` 只是候选下一步信息；读 Issue/PR 后再决定认领，不能据此重复派发。

## 组织可读内容

先写完整数学内容，再选择项目现有 chapter 模式，关联准确的 Lean 完全限定名。
外部声明关联可以避免在纯数学库里添加文档依赖；不强制为所有 Lean 源加 Blueprint import。
语法示意（需放进实际项目的 Verso 文档上下文，不是可单独编译的文件）：

```text
:::theorem "main-result" (lean := "MyProject.mainResult")
这里用项目的数学记号写自包含陈述。
:::

:::proof "main-result"
这里解释数学主线，并在承重引理处给出对应链接。
:::
```

Verso 数学语法不同于普通 Markdown 的 `$...$`，应沿用项目模板和已验证示例。不要自动把 Markdown 原样塞进 `.lean`。
同一个结果可关联 Issue/PR（支持相应字段的版本使用 `issue_url` / `pr_url`）；这些链接不意味着实时同步状态。

`uses` 用于数学依赖，`bpref` 用于普通参考链接。手写依赖归路线图；自动关联依赖仍按 `graphs.md` 检查来源，不把整个混合图称真实 DAG。

## 传统 LeanBlueprint / LeanArchitect

若已有工具链，沿用项目 `leanblueprint web` / `checkdecls` 等命令。`checkdecls` 验证声明名称存在，不等于证明无占位或语义匹配。
传统 `\leanok` 是手工标记，不能代替实际检查。`\discussion{N}` 可关联讨论 Issue。
已有 LeanArchitect 项目可以使用其声明属性与导出，但人工指定依赖仍属于路线图信息。不要在未经检查的树上运行批量迁移脚本。

## 私库输出

默认本地生成与本地预览，或保存到有访问控制且在保留期内的 CI artifact。后者不是永久归档，需要在项目内保留可重建的源。
GitHub 私库不保证 Pages 私有；无明确发布授权，不复制上游模板里的 Pages 部署 workflow，不启动公网服务。
本地服务器只绑定 loopback；访问控制仍按机器与项目要求设置。

## 人类可读性的最低退路

没有网页后端不等于可以只交 Lean。交付 `result-page.md` 的完整数学说明、实际声明链接与假设对照。
图工具缺失时明确说明实际 DAG 尚未提取；可以交路线图，但不能冒充已经自动生成的依赖视图。

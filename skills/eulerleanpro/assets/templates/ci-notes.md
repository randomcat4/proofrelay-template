# CI 示例的接入边界

`lean-ci.yml` 来自官方 Lean action 的最小构建方式，删去自动主分支触发，增加只读权限与明确边界。本包未在 GitHub Actions 执行它。
先检查仓库现有 CI，不用重复 workflow 覆盖它。示例假定 Lean 项目在仓库根且已有有效 `lean-toolchain` 与 Lake 配置；monorepo 应按当前 action 文档配置项目位置。
版本标签来自本次读取的官方 README，不代表要求升级用户工具链。Action 本身有网络/缓存行为；在运行前核对项目的依赖获取政策。

它只做构建，不发布 Pages，不上传论文，不写回状态，不创建 PR，也不建立模型 API。
Lean 普通 build 可以在有 `sorry` 时成功。因此最终目标还需要项目既有的公理/占位检查、语义审查和可读性审查，不能把这个绿勾称为完整认证。

CI 实际运行的配置与用户项目策略为准。严禁为运行 fork 代码使用带高权限的 `pull_request_target`。

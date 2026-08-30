# 模板初始化

[English](setup.md)

1. 替换 `state/PROJECT_STATE.json`、状态账和冻结目标中的 `REPLACE_ME`。
2. 选择稳定项目 ID 和受保护分支。
3. 定义目标版本、已接受前提、非目标与权限边界。
4. 按影响设置验证数量；默认路线级 1 名、项目级 2 名。
5. 审查 `config/policy.json` 的秘密模式并增加项目专用禁区。
6. 运行 `python scripts/print_label_commands.py`，审查后执行生成的 `gh label create` 命令。
7. 启用分支保护：要求 PR、`validate` 检查、解决对话，禁止强推和删除；条件允许时同样约束管理员。
8. 为 `state/`、`contracts/` 和 `.github/` 配置 CODEOWNERS 或规则集。
9. 本地运行校验器与测试，再建立初始化 PR。
10. 在 GitHub 设置中把仓库标为模板。

只有项目化替换完成且校验通过后才删除示例占位。不能因为来源项目使用本地材料，就擅自加入受版权保护论文、私有数据或凭据。

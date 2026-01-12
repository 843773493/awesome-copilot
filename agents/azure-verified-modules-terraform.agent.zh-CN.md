

---
description: "使用 Azure 验证模块 (AVM) 创建、更新或审查 Azure 基础设施即代码 (IaC)。"
name: "Azure AVM Terraform 模式"
tools: ["changes", "codebase", "edit/editFiles", "extensions", "fetch", "findTestFiles", "githubRepo", "new", "openSimpleBrowser", "problems", "runCommands", "runTasks", "runTests", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "usages", "vscodeAPI", "microsoft.docs.mcp", "azure_get_deployment_best_practices", "azure_get_schema_for_Bicep"]
---

# Azure AVM Terraform 模式

使用 Terraform 的 Azure 验证模块 (AVM) 通过预构建模块强制实施 Azure 最佳实践。

## 发现模块

- Terraform 注册表：搜索 "avm" + 资源，按 Partner 标签筛选。
- AVM 索引：`https://azure.github.io/Azure-Verified-Modules/indexes/terraform/tf-resource-modules/`

## 使用方法

- **示例**：复制示例，将 `source = "../../"` 替换为 `source = "Azure/avm-res-{service}-{resource}/azurerm"`，添加 `version`，设置 `enable_telemetry`。
- **自定义**：复制部署说明，设置输入参数，固定 `version`。

## 版本控制

- 端点：`https://registry.terraform.io/v1/modules/Azure/{module}/azurerm/versions`

## 源地址

- 注册表：`https://registry.terraform.io/modules/Azure/{module}/azurerm/latest`
- GitHub：`https://github.com/Azure/terraform-azurerm-avm-res-{service}-{resource}`

## 命名规范

- 资源：Azure/avm-res-{service}-{resource}/azurerm
- 模式：Azure/avm-ptn-{pattern}/azurerm
- 工具：Azure/avm-utl-{utility}/azurerm

## 最佳实践

- 固定模块和提供者的版本
- 从官方示例开始
- 审查输入参数和输出结果
- 启用遥测
- 使用 AVM 工具模块
- 遵循 AzureRM 提供者的要求
- 在进行任何更改后始终运行 `terraform fmt` 和 `terraform validate`
- 使用 `azure_get_deployment_best_practices` 工具获取部署指导
- 使用 `microsoft.docs.mcp` 工具查找 Azure 服务特定的指导

## GitHub Copilot 代理的自定义说明

**重要**：当 GitHub Copilot 代理或 GitHub Copilot 编码代理在此仓库中工作时，必须执行以下本地单元测试以符合 PR 检查要求。未运行这些测试会导致 PR 验证失败：

```bash
./avm pre-commit
./avm tflint
./avm pr-check
```

这些命令必须在创建或更新任何拉取请求之前运行，以确保符合 Azure 验证模块标准并防止 CI/CD 流水线失败。
有关 AVM 流程的更多信息，请参阅 [Azure 验证模块贡献文档](https://azure.github.io/Azure-Verified-Modules/contributing/terraform/testing/)。
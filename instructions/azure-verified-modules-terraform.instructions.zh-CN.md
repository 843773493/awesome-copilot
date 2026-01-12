

---
description: 'Azure 验证模块（AVM）和 Terraform'
applyTo: '**/*.terraform, **/*.tf, **/*.tfvars, **/*.tfstate, **/*.tflint.hcl, **/*.tf.json, **/*.tfvars.json'
---

# Azure 验证模块（AVM）Terraform

## 概述

Azure 验证模块（AVM）是遵循 Azure 最佳实践的预构建、测试和验证的 Terraform 和 Bicep 模块。使用这些模块可以放心地创建、更新或审查 Azure 基础设施即代码（IaC）。

## GitHub Copilot 代理的自定义说明

**重要提示**：当 GitHub Copilot 代理或 GitHub Copilot 编码代理在处理此仓库时，必须执行以下本地单元测试以符合 PR 检查要求。未运行这些测试将导致 PR 验证失败：

```bash
./avm pre-commit
./avm tflint
./avm pr-check
```

这些命令必须在创建或更新任何拉取请求之前运行，以确保符合 Azure 验证模块标准并防止 CI/CD 管道失败。
有关 AVM 流程的更多细节，请参阅 [Azure 验证模块贡献文档](https://azure.github.io/Azure-Verified-Modules/contributing/terraform/testing/)。

**未运行这些测试将导致 PR 验证失败并阻止成功合并。**

## 模块发现

### Terraform 注册表

- 搜索 "avm" + 资源名称
- 通过 "Partner" 标签筛选以查找官方 AVM 模块
- 示例：搜索 "avm storage account" → 通过 Partner 筛选

### 官方 AVM 索引

> **注意**：以下链接始终指向主分支上的 CSV 文件的最新版本。按设计，这意味着文件可能会随时间变化。如果您需要某个时间点的版本，请考虑在 URL 中使用特定的发布标签。

- **Terraform 资源模块**：`https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformResourceModules.csv`
- **Terraform 模式模块**：`https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformPatternModules.csv`
- **Terraform 工具模块**：`https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformUtilityModules.csv`

## Terraform 模块使用

### 从示例中使用

1. 从模块文档中复制示例代码
2. 将 `source = "../../"` 替换为 `source = "Azure/avm-res-{service}-{resource}/azurerm"`
3. 添加 `version = "~> 1.0"`（使用最新可用版本）
4. 设置 `enable_telemetry = true`

### 从头开始创建

1. 从模块文档中复制部署说明
2. 配置必需和可选的输入参数
3. 固定模块版本
4. 启用遥测

### 示例用法

```hcl
module "storage_account" {
  source  = "Azure/avm-res-storage-storageaccount/azurerm"
  version = "~> 0.1"

  enable_telemetry    = true
  location            = "East US"
  name                = "mystorageaccount"
  resource_group_name = "my-rg"

  # 其他配置...
}
```

## 命名规范

### 模块类型

- **资源模块**：`Azure/avm-res-{service}-{resource}/azurerm`
  - 示例：`Azure/avm-res-storage-storageaccount/azurerm`
- **模式模块**：`Azure/avm-ptn-{pattern}/azurerm`
  - 示例：`Azure/avm-ptn-aks-enterprise/azurerm`
- **工具模块**：`Azure/avm-utl-{utility}/azurerm`
  - 示例：`Azure/avm-utl-regions/azurerm`

### 服务命名

- 使用 kebab-case 命名服务和资源
- 遵循 Azure 服务名称（例如：`storage-storageaccount`, `network-virtualnetwork`）

## 版本管理

### 查看可用版本

- 接口：`https://registry.terraform.io/v1/modules/Azure/{module}/azurerm/versions`
- 示例：`https://registry.terraform.io/v1/modules/Azure/avm-res-storage-storageaccount/azurerm/versions`

### 版本固定最佳实践

- 使用悲观版本约束：`version = "~> 1.0"`
- 生产环境中固定到特定版本：`version = "1.2.3"`
- 升级前始终查看版本日志

## 模块源

### Terraform 注册表

- **URL 模式**：`https://registry.terraform.io/modules/Azure/{module}/azurerm/latest`
- **示例**：`https://registry.terraform.io/modules/Azure/avm-res-storage-storageaccount/azurerm/latest`

### GitHub 仓库

- **URL 模式**：`https://github.com/Azure/terraform-azurerm-avm-{type}-{service}-{resource}`
- **示例**：
  - 资源模块：`https://github.com/Azure/terraform-azurerm-avm-res-storage-storageaccount`
  - 模式模块：`https://github.com/Azure/terraform-azurerm-avm-ptn-aks-enterprise`

## 开发最佳实践

### 模块使用

- ✅ **始终** 固定模块和提供者的版本
- ✅ **从官方示例** 开始使用模块文档中的示例
- ✅ **在实现前** 审查所有输入和输出
- ✅ **启用遥测**：`enable_telemetry = true`
- ✅ **使用 AVM 工具模块** 处理常见模式
- ✅ **遵循 AzureRM 提供者的要求和约束**

### 代码质量

- ✅ **在更改后始终运行** `terraform fmt`
- ✅ **在更改后始终运行** `terraform validate`
- ✅ **使用有意义的变量名和描述**
- ✅ **添加适当的标签和元数据**
- ✅ **文档化复杂配置**

### 验证要求

在创建或更新任何拉取请求之前：

```bash
# 格式化代码
terraform fmt -recursive

# 验证语法
terraform validate

# AVM 特定验证（必需）
./avm pre-commit
./avm tflint
./avm pr-check
```

## 工具集成

### 使用可用工具

- **部署指导**：使用 `azure_get_deployment_best_practices` 工具
- **服务文档**：使用 `microsoft.docs.mcp` 工具获取 Azure 服务特定指导
- **模式信息**：使用 `azure_get_schema_for_Bicep` 获取 Bicep 资源模式

### GitHub Copilot 集成

在处理 AVM 仓库时：

1. 在创建新资源前始终检查现有模块
2. 使用官方示例作为起点
3. 在提交前运行所有验证测试
4. 文档化任何自定义或对示例的偏离

## 常见模式

### 资源组模块

```hcl
module "resource_group" {
  source  = "Azure/avm-res-resources-resourcegroup/azurerm"
  version = "~> 0.1"

  enable_telemetry = true
  location         = var.location
  name            = var.resource_group_name
}
```

### 虚拟网络模块

```hcl
module "virtual_network" {
  source  = "Azure/avm-res-network-virtualnetwork/azurerm"
  version = "~> 0.1"

  enable_telemetry    = true
  location            = module.resource_group.location
  name                = var.vnet_name
  resource_group_name = module.resource_group.name
  address_space       = ["10.0.0.0/16"]
}
```

## 常见问题排查

### 常见问题

1. **版本冲突**：始终检查模块和提供者版本之间的兼容性
2. **缺少依赖项**：确保所有必需资源首先被创建
3. **验证失败**：在提交前运行 AVM 验证工具
4. **文档**：始终参考最新的模块文档

### 支持资源

- **AVM 文档**：`https://azure.github.io/Azure-Verified-Modules/`
- **GitHub 问题**：在特定模块的 GitHub 仓库中报告问题
- **社区**：Azure Terraform 提供者 GitHub 讨论区

## 合规性检查清单

在提交任何与 AVM 相关的代码前：

- [ ] 模块版本已固定
- [ ] 遥测已启用
- [ ] 代码已格式化（`terraform fmt`）
- [ ] 代码已验证（`terraform validate`）
- [ ] AVM pre-commit 检查通过（`./avm pre-commit`）
- [ ] TFLint 检查通过（`./avm tflint`）
- [ ] AVM PR 检查通过（`./avm pr-check`）
- [ ] 文档已更新
- [ ] 示例已测试并正常运行
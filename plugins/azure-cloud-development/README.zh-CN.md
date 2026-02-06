# Azure 与云开发插件

全面的 Azure 云开发工具，包括基础设施即代码、无服务器函数、架构模式和成本优化，用于构建可扩展的云应用。

## 安装

```bash
# 使用 Copilot CLI
copilot plugin install azure-cloud-development@awesome-copilot
```

## 包含内容

### 命令（斜杠命令）

| 命令 | 描述 |
|------|------|
| `/azure-cloud-development:azure-resource-health-diagnose` | 分析 Azure 资源健康状况，从日志和遥测数据中诊断问题，并为已识别的问题创建修复计划。 |
| `/azure-cloud-development:az-cost-optimize` | 分析应用中使用的 Azure 资源（基础设施即代码文件和/或目标资源组中的资源）并优化成本 - 为识别到的优化项创建 GitHub 问题。 |

### 代理

| 代理 | 描述 |
|------|------|
| `azure-principal-architect` | 提供基于 Azure 高质量架构框架原则和 Microsoft 最佳实践的 Azure 主体架构专家指导。 |
| `azure-saas-architect` | 提供基于 Azure 高质量架构框架 SaaS 原则和 Microsoft 最佳实践的 Azure SaaS 架构专家指导，专注于多租户应用程序。 |
| `azure-logic-apps-expert` | 提供针对 Azure 逻辑应用开发的专家指导，专注于工作流设计、集成模式和基于 JSON 的工作流定义语言。 |
| `azure-verified-modules-bicep` | 使用 Azure 验证模块 (AVM) 创建、更新或审查基于 Bicep 的 Azure 基础设施即代码 (IaC)。 |
| `azure-verified-modules-terraform` | 使用 Azure 验证模块 (AVM) 创建、更新或审查基于 Terraform 的 Azure 基础设施即代码 (IaC)。 |
| `terraform-azure-planning` | 作为 Azure Terraform 基础设施即代码任务的实施规划者进行操作。 |
| `terraform-azure-implement` | 作为 Azure Terraform 基础设施即代码编码专家，创建和审查 Azure 资源的 Terraform 代码。 |

## 来源

此插件是 [Awesome Copilot](https://github.com/github/awesome-copilot) 的一部分，这是一个由社区驱动的 GitHub Copilot 扩展集合。

## 许可证

MIT

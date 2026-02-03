---
name: terraform-azurerm-set-diff-analyzer
description: 用于分析 AzureRM Provider 的 Terraform plan JSON 输出，以区分集合类型属性引起的假阳性差异（仅顺序变化）和实际资源变化。在审查 Azure 资源（如应用网关、负载均衡器、防火墙、前端门、网络安全组等）的 Terraform plan 输出时使用，这些资源的集合类型属性会导致因内部顺序变化而产生误报差异。
license: MIT
---

# Terraform AzureRM 集合差异分析器

一种识别由 AzureRM Provider 的集合类型属性引起的 Terraform 计划中的“假阳性差异”并将其与实际变化区分开的技能。

## 使用场景

- `terraform plan` 显示大量变化，但你仅添加/删除了一个元素
- 应用网关、负载均衡器、网络安全组等显示“所有元素已更改”
- 你希望在 CI/CD 中自动过滤假阳性差异

## 背景

Terraform 的集合类型通过位置而非键进行比较，因此在添加或删除元素时，所有元素都会显示为“已更改”。这是 Terraform 的一个普遍问题，但在使用集合类型属性较多的 AzureRM 资源（如应用网关、负载均衡器和网络安全组）中尤为明显。

这些“假阳性差异”实际上不会影响资源，但会使审查 Terraform 计划输出变得困难。

## 前提条件

- Python 3.8+

如果 Python 不可用，请通过您的包管理器安装（例如，`apt install python3`，`brew install python3`）或从 [python.org](https://www.python.org/downloads/) 安装。

## 基本用法

```bash
# 1. 生成 plan JSON 输出
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json

# 2. 分析
python scripts/analyze_plan.py plan.json
```

## 常见问题排查

- **`python: command not found`**: 请改用 `python3`，或安装 Python
- **`ModuleNotFoundError`**: 脚本仅使用标准库；请确保已安装 Python 3.8+

## 详细文档

- [scripts/README.md](scripts/README.md) - 所有选项、输出格式、退出代码、CI/CD 示例
- [references/azurerm_set_attributes.md](references/azurerm_set_attributes.md) - 支持的资源和属性

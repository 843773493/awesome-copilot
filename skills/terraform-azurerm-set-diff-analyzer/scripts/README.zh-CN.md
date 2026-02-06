# Terraform AzureRM Set差异分析脚本

一个用于分析Terraform计划JSON文件并识别AzureRM Set类型属性中“误报差异”的Python脚本。

## 概述

AzureRM提供者的Set类型属性（如`backend_address_pool`、`security_rule`等）不保证顺序，因此在添加或删除元素时，所有元素都会显示为“已更改”。此脚本能够区分这类“误报差异”与实际的更改。

### 使用场景

- 作为**Agent技能**（推荐）
- 作为**CLI工具**手动执行
- 用于**CI/CD流水线**的自动化分析

## 前提条件

- Python 3.8或更高版本
- 不需要额外安装包（仅使用标准库）

## 使用方法

### 基本用法

```bash
# 从文件读取
python analyze_plan.py plan.json

# 从标准输入读取
terraform show -json plan.tfplan | python analyze_plan.py
```

### 选项

| 选项 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--format` | `-f` | 输出格式（markdown/json/summary） | markdown |
| `--exit-code` | `-e` | 根据更改返回退出码 | false |
| `--quiet` | `-q` | 抑制警告 | false |
| `--verbose` | `-v` | 显示详细警告 | false |
| `--ignore-case` | - | 不区分大小写比较值 | false |
| `--attributes` | - | 自定义属性定义文件路径 | （内置） |
| `--include` | - | 过滤要分析的资源（可指定多个） | （全部） |
| `--exclude` | - | 过滤要排除的资源（可指定多个） | （无） |

### 退出码（启用`--exit-code`时）

| 代码 | 含义 |
|------|------|
| 0 | 无更改，或仅顺序更改 |
| 1 | 实际的Set属性更改 |
| 2 | 资源替换（删除 + 创建） |
| 3 | 错误 |

## 输出格式

### Markdown（默认）

适用于PR评论和报告的人类可读格式。

```bash
python analyze_plan.py plan.json --format markdown
```

### JSON

用于程序化处理的结构化数据。

```bash
python analyze_plan.py plan.json --format json
```

示例输出：
```json
{
  "summary": {
    "order_only_count": 3,
    "actual_set_changes_count": 1,
    "replace_count": 0
  },
  "has_real_changes": true,
  "resources": [...],
  "warnings": []
}
```

### 总结

用于CI/CD日志的一行摘要。

```bash
python analyze_plan.py plan.json --format summary
```

示例输出：
```
🟢 3 仅顺序 | 🟡 1 Set更改
```

## CI/CD流水线使用

### GitHub Actions

```yaml
name: Terraform计划分析

on:
  pull_request:
    paths:
      - '**.tf'

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: 设置Terraform
        uses: hashicorp/setup-terraform@v3
        
      - name: Terraform初始化与计划
        run: |
          terraform init
          terraform plan -out=plan.tfplan
          terraform show -json plan.tfplan > plan.json
          
      - name: 分析Set差异
        run: |
          python path/to/analyze_plan.py plan.json --format markdown > analysis.md
          
      - name: 添加PR评论
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          path: analysis.md
```

### GitHub Actions（带退出码的门控）

```yaml
      - name: 分析并门控
        run: |
          python path/to/analyze_plan.py plan.json --exit-code --format summary
        # 在退出码为2时失败（资源替换）
        continue-on-error: false
```

### Azure Pipelines

```yaml
- task: TerraformCLI@0
  inputs:
    command: 'plan'
    commandOptions: '-out=plan.tfplan'

- script: |
    terraform show -json plan.tfplan > plan.json
    python scripts/analyze_plan.py plan.json --format markdown > $(Build.ArtifactStagingDirectory)/analysis.md
  displayName: '分析计划'

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: '$(Build.ArtifactStagingDirectory)/analysis.md'
    artifactName: 'plan-analysis'
```

### 过滤示例

仅分析特定资源：
```bash
python analyze_plan.py plan.json --include application_gateway --include load_balancer
```

排除特定资源：
```bash
python analyze_plan.py plan.json --exclude virtual_network
```

## 解析结果

| 类别 | 含义 | 推荐操作 |
|------|------|----------|
| 🟢 仅顺序 | 误报差异，无实际更改 | 可安全忽略 |
| 🟡 实际更改 | Set元素被添加/删除/修改 | 审查内容，通常为原地更新 |
| 🔴 资源替换 | 删除 + 创建 | 检查停机影响 |

## 自定义属性定义

默认使用`references/azurerm_set_attributes.json`，但可以指定自定义定义文件：

```bash
python analyze_plan.py plan.json --attributes /path/to/custom_attributes.json
```

有关定义文件格式，请参阅`references/azurerm_set_attributes.md`。

## 局限性

- 仅支持AzureRM资源（`azurerm_*`）
- 某些资源/属性可能不被支持
- 包含`after_unknown`的属性（apply后确定的值）比较可能不完整
- 敏感属性（被遮蔽）比较可能不完整

## 相关文档

- [SKILL.md](../SKILL.md) - 作为Agent技能的使用方法
- [azurerm_set_attributes.md](../references/azurerm_set_attributes.md) - 属性定义参考

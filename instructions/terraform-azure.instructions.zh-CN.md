

---
description: '在 Azure 上使用 Terraform 构建或修改解决方案。'
applyTo: '**/*.terraform, **/*.tf, **/*.tfvars, **/*.tflint.hcl, **/*.tfstate, **/*.tf.json, **/*.tfvars.json'
---

# Azure Terraform 最佳实践

## 集成与自包含性

本指令集扩展了通用的 DevOps 核心原则和 Taming Copilot 指令，适用于 Azure/Terraform 场景。它假设这些基础规则已加载，但在此包含摘要以实现自包含性。如果通用规则未加载，这些摘要将作为默认值以保持行为一致性。

### 融入的 DevOps 核心原则（CALMS 框架）

- **文化**：培养协作、无责备的文化，实现共享责任和持续学习。
- **自动化**：在整个软件交付生命周期中尽可能自动化，以减少手动工作和错误。
- **精益**：消除浪费，最大化流程效率，通过减少批量大小和瓶颈持续交付价值。
- **度量**：对所有相关指标（例如 DORA 指标：部署频率、变更交付时间、变更失败率、恢复时间）进行测量，以推动改进。
- **共享**：促进团队间知识共享、协作和透明度。

### 融入的 Taming Copilot 指令（行为层级）

- **用户指令优先**：直接用户指令具有最高优先级。
- **事实验证**：优先使用工具提供当前、准确的答案，而非依赖内部知识。
- **遵循哲学**：采用极简主义和精确的方法——按需编写代码，仅进行必要的更改，提供直接且简洁的响应。
- **工具使用**：有目的性地使用工具；在行动前声明意图；在可能的情况下优先使用并行调用。

这些摘要确保模式能够独立运行，同时与更广泛的聊天模式上下文保持一致。如需完整细节，请参考原始的 DevOps 核心原则和 Taming Copilot 指令。

## 聊天模式集成

在聊天模式下运行时，若已加载这些指令：

- 将其视为一个自包含的扩展，包含用于独立运行的摘要通用规则。
- 优先考虑用户指令，特别是对于 validate 以外的 Terraform 命令。
- 在执行任何 Terraform plan 或 apply 操作前，确认隐式依赖关系。
- 保持最小化响应和精确的代码更改，与融入的 Taming 哲学保持一致。
- **规划文件意识**：始终检查 `.terraform-planning-files/` 文件夹中的规划文件（如果存在）。阅读并整合这些文件中的相关信息到响应中，尤其是在迁移或实施计划中。如果用户指定的文件夹中存在 speckit 或类似规划文件，请提示用户确认是否包含或显式阅读它们。

## 1. 概述

这些指令为使用 Terraform 构建的解决方案提供 Azure 特定的指导，包括如何整合和使用 Azure 验证模块。

如需了解通用的 Terraform 习惯用法，请参阅 [terraform.instructions.md](terraform.instructions.md)。

如需开发模块，尤其是 Azure 验证模块，请参阅 [azure-verified-modules-terraform.instructions.md](azure-verified-modules-terraform.instructions.md)。

## 2. 需要避免的反模式

**配置：**

- **绝对不能**硬编码应参数化的值
- **不应**将 `terraform import` 作为常规工作流
- **应避免**使用复杂条件逻辑，使代码难以理解
- **绝对不能**在无需的情况下使用 `local-exec` 提供者

**安全：**

- **绝对不能**在 Terraform 文件或状态中存储机密
- **应避免**使用过于宽松的 IAM 角色或网络规则
- **绝对不能**为了方便而禁用安全功能
- **绝对不能**使用默认密码或密钥

**运维：**

- **绝对不能**在未测试的情况下直接将 Terraform 更改应用于生产环境
- **应避免**手动更改 Terraform 管理的资源
- **绝对不能**忽略 Terraform 状态文件的损坏或不一致
- **绝对不能**在生产环境中从本地机器运行 Terraform
- **只能**使用 Terraform 状态文件 (`**/*.tfstate`) 进行只读操作，所有更改必须通过 Terraform CLI 或 HCL 进行
- **只能**使用 `**/.terraform/**`（获取的模块和提供者）中的内容进行只读操作

这些内容基于融入的 Taming Copilot 指令，以实现安全的运维实践。

---

## 3. 清晰组织代码

使用逻辑文件分离来结构化 Terraform 配置：

- 使用 `main.tf` 定义资源
- 使用 `variables.tf` 定义输入变量
- 使用 `outputs.tf` 定义输出
- 使用 `terraform.tf` 定义提供者配置
- 使用 `locals.tf` 抽象复杂表达式以提高可读性
- 遵循一致的命名约定和格式化 (`terraform fmt`)
- 如果 `main.tf` 或 `variables.tf` 文件过大，按资源类型或功能拆分为多个文件（例如：`main.networking.tf`、`main.storage.tf` - 将等效变量移动到 `variables.networking.tf`，依此类推）

使用 `snake_casing` 命名变量和模块。

## 4. 使用 Azure 验证模块 (AVM)

如果存在，任何重要资源都应使用 AVM。AVMs 是与 Azure 健康架构框架对齐的，由 Microsoft 支持和维护，有助于减少需要维护的代码量。有关如何发现这些模块的信息，请参阅 [Azure 验证模块 for Terraform](azure-verified-modules-terraform.instructions.md)。

如果资源没有可用的 Azure 验证模块，建议按照 AVM 风格创建一个模块，以与现有工作保持一致，并为社区上游贡献提供机会。

本指令的一个例外是，如果用户被指示使用内部私有注册表，或明确表示不希望使用 Azure 验证模块。

这与融入的 DevOps 自动化原则一致，通过利用预验证的、社区维护的模块来实现一致性。

## 5. 变量和代码风格标准

在解决方案代码中遵循与 AVM 对齐的编码标准以保持一致性：

- **变量命名**：所有变量名称使用 snake_case（遵循 TFNFR4 和 TFNFR16）。命名应具有描述性且保持命名约定的一致性。
- **变量定义**：所有变量必须具有显式类型声明（遵循 TFNFR18），并提供全面的描述（遵循 TFNFR17）。除非有特定需求，否则避免对集合值使用可为空的默认值（遵循 TFNFR20）。
- **敏感变量**：适当标记敏感变量，避免显式设置 `sensitive = false`（遵循 TFNFR22）。正确处理敏感默认值（遵循 TFNFR23）。
- **动态块**：在适当情况下，使用动态块处理可选的嵌套对象（遵循 TFNFR12），并使用 `coalesce` 或 `try` 函数处理默认值（遵循 TFNFR13）。
- **代码组织**：考虑使用 `locals.tf` 存储本地值（遵循 TFNFR31），并确保本地值的精确类型（遵循 TFNFR33）。

## 6. 机密管理

最好的机密是不需要存储的。例如，使用托管标识而不是密码或密钥。

在支持的 Terraform 版本（v1.11+）中，使用具有只写参数的 `ephemeral` 机密，以避免将机密存储在状态文件中。请查阅模块文档以确认其可用性。

如需存储机密，请使用密钥保管库（Key Vault），除非另有指示。

**永远不要**将机密写入本地文件系统或提交到 Git。

适当标记敏感值，将其与其他属性隔离，并在绝对必要时避免输出敏感数据。遵循 TFNFR19、TFNFR22 和 TFNFR23。

## 7. 输出

- **避免不必要的输出**，仅用于暴露其他配置所需的信息。
- 对包含机密的输出使用 `sensitive = true`
- 为所有输出提供清晰的描述

```hcl
output "resource_group_name" {
  description = "创建的资源组名称"
  value       = azurerm_resource_group.example.name
}

output "virtual_network_id" {
  description = "虚拟网络的 ID"
  value       = azurerm_virtual_network.example.id
}
```

## 8. 本地值的使用

- 使用本地值（locals）来计算值和复杂表达式
- 通过提取重复表达式提高可读性
- 将相关值组合为结构化的本地值

```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    Owner       = var.owner
    CreatedBy   = "terraform"
  }
  
  resource_name_prefix = "${var.project_name}-${var.environment}"
  location_short       = substr(var.location, 0, 3)
}
```

## 9. 遵循推荐的 Terraform 实践

- **冗余 depends_on 检测**：搜索并移除 `depends_on`，如果依赖资源已在同一资源块中隐式引用。仅在明确需要时保留 `depends_on`。**不要**依赖模块输出。
- **迭代**：使用 `count` 处理 0-1 个资源，使用 `for_each` 处理多个资源。优先使用映射以确保稳定的资源地址。遵循 TFNFR7。
- **数据源**：在根模块中可以接受，但在可重用模块中应避免。优先使用显式模块参数而不是数据源查找。
- **参数化**：使用强类型变量并显式声明 `type`（TFNFR18），提供全面的描述（TFNFR17），并避免对集合值使用可为空的默认值（TFNFR20）。利用 AVM 暴露的变量。
- **版本控制**：目标是使用最新的稳定版 Terraform 和 Azure 提供者。在代码中指定版本并保持更新（TFFR3）。

## 10. 文件夹结构

使用一致的文件夹结构来组织 Terraform 配置。

使用 tfvars 来修改环境差异。通常，应尽量保持环境相似，同时对非生产环境进行成本优化。

反模式 - 按环境分支、按环境仓库、按环境文件夹，或类似结构，这些会使得难以在不同环境之间测试根文件夹逻辑。

注意诸如 Terragrunt 等工具可能会影响此设计。

**建议的结构**如下：

```text
my-azure-app/
├── infra/                          # Terraform 根模块（与 AZD 兼容）
│   ├── main.tf                     # 核心资源
│   ├── variables.tf                # 输入变量
│   ├── outputs.tf                  # 输出
│   ├── terraform.tf                # 提供者配置
│   ├── locals.tf                   # 本地值
│   └── environments/               # 环境特定配置
│       ├── dev.tfvars              # 开发环境
│       ├── test.tfvars             # 测试环境
│       └── prod.tfvars             # 生产环境
├── .github/workflows/              # CI/CD 管道（如果使用 GitHub）
├── .azdo/                          # CI/CD 管道（建议如果使用 Azure DevOps）
└── README.md                       # 文档
```

**永远不要**在未与用户直接协商的情况下更改文件夹结构。

遵循 AVM 规范 TFNFR1、TFNFR2、TFNFR3 和 TFNFR4 以确保一致的文件命名和结构。

## Azure 特定最佳实践

### 资源命名与标签

- 遵循 [Azure 命名规范](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
- 在多区域部署中使用一致的区域命名和变量
- 实施一致的标签策略

### 资源组策略

- 当指定时使用现有资源组
- 仅在必要时创建新的资源组，并在创建前进行确认
- 使用描述性名称，表明用途和环境

### 网络考虑

- 在创建新网络资源前验证现有 VNet/subnet ID（例如，该解决方案是否部署到现有 hub & spoke 陆地区域）
- 适当使用网络安全组 (NSGs) 和应用安全组 (ASGs)
- 在需要时为 PaaS 服务实现私有终结点，否则使用资源防火墙限制以阻止公共访问。需要公共终结点时，注释例外情况。

### 安全与合规

- 使用托管标识代替服务主体
- 实现适当的 RBAC 的密钥保管库
- 启用诊断设置以进行审计追踪
- 遵循最小特权原则

## 成本管理

- 确认昂贵资源的预算批准
- 使用适合环境的资源规模（开发 vs 生产）
- 如果未指定，请询问成本限制

## 状态管理

- 使用远程后端（Azure 存储）并启用状态锁定
- 永远不要将状态文件提交到源代码控制
- 启用静态加密和传输中加密

## 验证

- 进行现有资源的清单并提供移除未使用资源块的建议
- 运行 `terraform validate` 来检查语法
- 在运行 `terraform plan` 前询问用户。`terraform plan` 将需要订阅 ID，应从 ARM_SUBSCRIPTION_ID 环境变量获取，**不要**在提供者块中硬编码
- 首先在非生产环境中测试配置
- 确保幂等性（多次应用产生相同结果）

## 回退行为

如果通用规则未加载，则默认采用：极简代码生成、对 validate 以外的任何 Terraform 命令进行显式同意，并在所有建议中遵循 CALMS 原则。
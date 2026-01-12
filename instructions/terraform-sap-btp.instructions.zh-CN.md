

---
description: 'SAP Business Technology Platform（SAP BTP）上的 Terraform 习惯用法和指南。'
applyTo: '**/*.tf, **/*.tfvars, **/*.tflint.hcl, **/*.tf.json, **/*.tfvars.json'
---

# Terraform 在 SAP BTP 上的最佳实践与规范

## 核心原则

保持 Terraform 代码简洁、模块化、可重复使用、安全且可审计。
始终对 Terraform HCL 进行版本控制，绝不要对生成的 state 文件进行版本控制。

## 安全性

强制要求：
- 使用最新稳定版 Terraform CLI 和 provider 版本；主动升级以获取安全补丁。
- 绝不要提交密钥、凭证、证书、Terraform state 或 plan 输出等敏感信息。
- 将所有秘密变量和输出标记为 `sensitive = true`。
- 优先使用临时/只写 provider 认证（Terraform >= 1.11），以确保密钥不会持久化存储在 state 中。
- 最小化敏感输出；仅输出下游自动化真正需要的信息。
- 在 CI 中持续使用 `tfsec`、`trivy`、`checkov`（至少选择一个）进行扫描。
- 定期审查 provider 凭证，轮换密钥，并在支持的情况下启用 MFA。

## 模块化

结构清晰且高效：
- 按逻辑域（例如：权限、服务实例）进行拆分 – 不按环境拆分。
- 仅使用模块封装可重用的多资源模式；避免使用单资源封装模块。
- 保持模块层级扁平；避免深度嵌套和循环依赖。
- 通过 `outputs` 仅暴露必要的跨模块数据（在需要时标记为敏感）。

## 可维护性

追求显式 > 隐式。
- 注释说明“为什么”，而不是“是什么”；避免重复描述显而易见的资源属性。
- 使用变量参数化，而不是硬编码；仅在合理时提供默认值。
- 优先使用数据源查询已有的外部基础设施；不要在同一个根模块中用于刚创建的资源，应使用输出。
- 避免在通用可重用模块中使用数据源；应要求输入参数。
- 移除未使用的/低效的数据源；它们会降低计划（plan）执行的速度。
- 使用 `locals` 来集中处理派生或重复的表达式，以统一逻辑。

## 风格与格式

### 通用
- 资源、变量、输出的描述性、一致性的名称。
- 变量和本地值使用 snake_case。
- 使用 2 个空格缩进；运行 `terraform fmt -recursive`。

### 布局与文件

推荐结构：
```text
my-sap-btp-app/
├── infra/                      # 根模块
│   ├── main.tf                 # 核心资源（大型文件时按域拆分）
│   ├── variables.tf            # 输入参数
│   ├── outputs.tf              # 输出结果
│   ├── provider.tf             # provider 配置
│   ├── locals.tf               # 本地/派生值
│   └── environments/           # 环境变量文件
│       ├── dev.tfvars
│       ├── test.tfvars
│       └── prod.tfvars
├── .github/workflows/          # 持续集成/持续交付（如使用 GitHub）
└── README.md                   # 文档说明
```

规则：
- 不要为每个环境创建单独的分支/仓库/文件夹（反模式）。
- 保持环境漂移最小；仅在 *.tfvars 文件中编码差异。
- 将过大的 `main.tf` / `variables.tf` 拆分为逻辑命名的片段（例如：`main_services.tf`、`variables_services.tf`）。
  保持命名一致性。

### 资源块组织

顺序（从上到下）：可选的 `depends_on`，然后是 `count`/`for_each`，接着是属性，最后是 `lifecycle`。
- 仅在 Terraform 无法推断依赖关系时使用 `depends_on`（例如：数据源需要权限）。
- 使用 `count` 表示可选的单个资源；使用 `for_each` 表示通过映射键值对创建的多个实例，以确保稳定的地址。
- 分组属性：必填项在前，可选项在后；逻辑部分之间用空行分隔。
- 在同一节中按字母顺序排列，以加快扫描速度。

### 变量
- 每个变量：显式 `type`，非空 `description`。
- 优先使用具体类型（如 `object`、`map(string)` 等），而不是 `any`。
- 避免对集合使用 null 默认值；改用空列表/空映射。

### 本地值（locals）
- 集中处理计算或重复的表达式。
- 将相关值分组到对象本地值中，以增强内聚性。

### 输出（outputs）
- 仅暴露下游模块/自动化所需的资源。
- 标记密钥为 `sensitive = true`。
- 始终提供清晰的 `description`。

### 格式化与检查
- 运行 `terraform fmt -recursive`（CI 中为必选项）。
- 在提交前/CI 中强制执行 `tflint`（可选 `terraform validate`）。

## 文档说明

强制要求：
- 所有变量和输出必须包含 `description` 和 `type`。
- 提供简洁的根目录 `README.md`：用途、前提条件、认证模型、使用方法（初始化/计划/应用）、测试和回滚。
- 使用 `terraform-docs` 生成模块文档（如可能，添加到 CI 中）。
- 仅在需要澄清非显而易见的决策或约束时添加注释。

## 状态管理
- 使用支持锁定的远程后端（如 Terraform Cloud、AWS S3、GCS、Azure Storage）。避免使用 SAP BTP 对象存储（其功能不足以可靠地实现状态锁定和安全性）。
- 绝不要提交 `*.tfstate` 或备份文件。
- 加密静态和传输中的状态；通过最小特权原则限制访问。

## 验证
- 在提交前运行 `terraform validate`（语法和内部检查）。
- 在执行 `terraform plan` 前与用户确认（需要认证和全局账户子域）。通过环境变量或 tfvars 提供认证；绝不要在 provider 块中内联密钥。
- 首先在非生产环境测试；确保应用是幂等的。

## 测试
- 使用 Terraform 测试框架（`*.tftest.hcl`）对模块逻辑和不变量进行测试。
- 覆盖成功和失败路径；保持测试无状态/幂等。
- 在可行的情况下优先使用模拟外部数据源。

## SAP BTP 提供商特定指南

指南：
- 使用 `data "btp_subaccount_service_plan"` 解析服务计划 ID，并引用该数据源的 `serviceplan_id`。

示例：
```terraform
data "btp_subaccount_service_plan" "example" {
  subaccount_id = var.subaccount_id
  service_name  = "your_service_name"
  plan_name     = "your_plan_name"
}

resource "btp_subaccount_service_instance" "example" {
  subaccount_id  = var.subaccount_id
  serviceplan_id = data.btp_subaccount_service_plan.example.id
  name           = "my-example-instance"
}
```

显式依赖（提供商无法推断）：
```terraform
resource "btp_subaccount_entitlement" "example" {
  subaccount_id = var.subaccount_id
  service_name  = "your_service_name"
  plan_name     = "your_plan_name"
}

data "btp_subaccount_service_plan" "example" {
  subaccount_id = var.subaccount_id
  service_name  = "your_service_name"
  plan_name     = "your_plan_name"
  depends_on    = [btp_subaccount_entitlement.example]
}
```

订阅也依赖于权限；当提供商无法通过属性（如 `service_name`/`plan_name` 与 `app_name`）推断关联时，添加 `depends_on`。

## 工具集成

### HashiCorp Terraform MCP 服务器
使用 Terraform MCP 服务器进行交互式模式查找、资源块起草和验证。
1. 安装并运行服务器（参见 https://github.com/mcp/hashicorp/terraform-mcp-server）。
2. 在您的 Copilot / MCP 客户端配置中将其添加为工具。
3. 在编写代码前查询提供商模式（例如：列出资源、数据源）。
4. 生成草稿资源块，然后手动调整以符合命名和标签标准。
5. 验证计划摘要（绝不要包含密钥）；在执行 `apply` 前与审查者确认差异。

### Terraform 注册表
参考 SAP BTP 提供商文档：https://registry.terraform.io/providers/SAP/btp/latest/docs，以获取权威的资源和数据源字段。如不确定，可交叉验证 MCP 响应与注册表文档。

## 反模式（避免）

配置：
- 硬编码环境特定值（使用变量和 tfvars）。
- 频繁使用 `terraform import`（仅用于迁移）。
- 降低清晰度的复杂条件逻辑和动态块。
- 除不可避免的集成缺口外，避免使用 `local-exec` 提供商。
- 除非有明确理由，否则不要在同一个根模块中混合使用 SAP BTP 提供商和 Cloud Foundry 提供商（拆分为独立模块）。

安全性：
- 在 HCL、state 或 VCS 中存储密钥。
- 为了速度而禁用加密、验证或扫描。
- 使用默认密码/密钥或在不同环境中重复使用凭证。

操作性：
- 在未进行非生产环境验证的情况下直接对生产环境进行应用。
- 在 Terraform 外手动修改状态。
- 忽略状态不一致或损坏的迹象。
- 从不受控的本地笔记本电脑运行生产环境应用（使用 CI/CD 或批准的运行器）。
- 从原始 `*.tfstate` 读取业务数据，而不是使用输出或数据源。

所有更改必须通过 Terraform CLI + HCL 流转，绝不要手动修改状态。
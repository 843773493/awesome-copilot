---
name: azure-deployment-preflight
description: '对 Azure 上的 Bicep 部署执行全面的预部署验证，包括模板语法验证、假设分析和权限检查。在任何 Azure 部署之前使用此技能，可预览更改、识别潜在问题并确保部署成功。当用户提及部署到 Azure、验证 Bicep 文件、检查部署权限、预览基础设施更改、运行假设分析或准备 azd provision 时激活此技能。'
---

# Azure 部署预部署验证

此技能在执行前验证 Bicep 部署，支持 Azure CLI (`az`) 和 Azure Developer CLI (`azd`) 工作流。

## 何时使用此技能

- 在部署基础设施到 Azure 之前
- 在准备或审查 Bicep 文件时
- 预览部署将带来的更改
- 验证部署权限是否充足
- 在运行 `azd up`、`azd provision` 或 `az deployment` 命令之前

## 验证流程

按照以下步骤依次执行。即使前一步骤失败，也继续执行下一步骤——在最终报告中捕获所有问题。

### 步骤 1：检测项目类型

通过检查项目标识符来确定部署工作流：

1. **检查是否存在 azd 项目**：在项目根目录查找 `azure.yaml`
   - 如果找到 → 使用 **azd 工作流**
   - 如果未找到 → 使用 **az CLI 工作流**

2. **定位 Bicep 文件**：查找所有 `.bicep` 文件以进行验证
   - 对于 azd 项目：首先检查 `infra/` 目录，然后检查项目根目录
   - 对于独立项目：使用用户指定的文件或搜索常见位置 (`infra/`、`deploy/`、项目根目录)

3. **自动检测参数文件**：为每个 Bicep 文件查找匹配的参数文件：
   - `<filename>.bicepparam`（Bicep 参数 - 推荐）
   - `<filename>.parameters.json`（JSON 参数）
   - `parameters.json` 或 `parameters/<env>.json` 在同一目录中

### 步骤 2：验证 Bicep 语法

在尝试部署验证之前，运行 Bicep CLI 检查模板语法：

```bash
bicep build <bicep-file> --stdout
```

**需要捕获的内容：**
- 带有行号和列号的语法错误
- 警告信息
- 构建成功/失败状态

**如果未安装 Bicep CLI：**
- 在报告中记录该问题
- 继续执行步骤 3（Azure 在假设分析期间会验证语法）

### 步骤 3：运行预部署验证

根据步骤 1 检测到的项目类型选择适当的验证方式。

#### 对于 azd 项目（存在 `azure.yaml`）

使用 `azd provision --preview` 来验证部署：

```bash
azd provision --preview
```

如果指定了环境或存在多个环境：
```bash
azd provision --preview --environment <env-name>
```

#### 对于独立 Bicep 项目（无 `azure.yaml`）

从 Bicep 文件的 `targetScope` 声明中确定部署范围：

| 目标作用域 | 命令 |
|------------|------|
| `resourceGroup`（默认） | `az deployment group what-if` |
| `subscription` | `az deployment sub what-if` |
| `managementGroup` | `az deployment mg what-if` |
| `tenant` | `az deployment tenant what-if` |

**首先使用 Provider 验证级别运行：**

```bash
# 资源组作用域（最常见的）
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider

# 订阅作用域
az deployment sub what-if \
  --location <location> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider

# 管理组作用域
az deployment mg what-if \
  --location <location> \
  --management-group-id <mg-id> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider

# 租户作用域
az deployment tenant what-if \
  --location <location> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider
```

**回退策略：**

如果 `--validation-level Provider` 因权限错误（RBAC）失败，尝试使用 `ProviderNoRbac`：

```bash
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file <bicep-file> \
  --validation-level ProviderNoRbac
```

在报告中注明回退情况——用户可能缺乏完整的部署权限。

### 步骤 4：捕获假设分析结果

解析假设分析输出以分类资源更改：

| 更改类型 | 符号 | 含义 |
|----------|------|------|
| 创建 | `+` | 将创建新资源 |
| 删除 | `-` | 将删除资源 |
| 修改 | `~` | 资源属性将更改 |
| 无更改 | `=` | 资源未更改 |
| 忽略 | `*` | 资源未被分析（达到限制） |
| 部署 | `!` | 将部署资源（更改未知） |

对于修改的资源，捕获具体的属性更改。

### 步骤 5：生成报告

在 **项目根目录** 创建名为 `preflight-report.md` 的 Markdown 报告文件。

使用 [references/REPORT-TEMPLATE.md](references/REPORT-TEMPLATE.md) 中的模板结构。

**报告部分：**
1. **摘要** - 总体状态、时间戳、验证的文件、目标作用域
2. **执行的工具** - 运行的命令、版本、使用的验证级别
3. **问题** - 所有错误和警告及其严重程度和修复建议
4. **假设分析结果** - 需要创建/修改/删除/未更改的资源
5. **建议** - 可操作的下一步骤

## 必需信息

在运行验证之前，需收集以下信息：

| 信息 | 用于 | 如何获取 |
|------|------|----------|
| 资源组 | `az deployment group` | 询问用户或检查现有的 `.azure/` 配置 |
| 订阅 | 所有部署 | 使用 `az account show` 或询问用户 |
| 位置 | Sub/MG/Tenant 作用域 | 询问用户或使用配置中的默认位置 |
| 环境 | azd 项目 | 使用 `azd env list` 或询问用户 |

如果缺少必需信息，请在继续前提示用户。

## 错误处理

详见 [references/ERROR-HANDLING.md](references/ERROR-HANDLING.md) 中的详细错误处理指南。

**关键原则：** 即使发生错误，也继续执行验证。所有问题将汇总到最终报告中。

| 错误类型 | 处理方式 |
|----------|----------|
| 未登录 | 在报告中记录，建议执行 `az login` 或 `azd auth login` |
| 权限被拒绝 | 回退到 `ProviderNoRbac`，在报告中注明 |
| Bicep 语法错误 | 包含所有错误，继续验证其他文件 |
| 工具未安装 | 在报告中记录，跳过该验证步骤 |
| 资源组未找到 | 在报告中记录，建议创建资源组 |

## 工具要求

此技能使用以下工具：

- **Azure CLI** (`az`) - 推荐使用版本 2.76.0+ 以支持 `--validation-level`
- **Azure Developer CLI** (`azd`) - 用于包含 `azure.yaml` 的项目
- **Bicep CLI** (`bicep`) - 用于语法验证
- **Azure MCP 工具** - 用于文档查询和最佳实践

开始前检查工具可用性：
```bash
az --version
azd version
bicep --version
```

## 示例工作流程

1. 用户： "在我运行部署之前验证我的 Bicep 部署"
2. Agent 检测到 `azure.yaml` → azd 项目
3. Agent 找到 `infra/main.bicep` 和 `infra/main.bicepparam`
4. Agent 运行 `bicep build infra/main.bicep --stdout`
5. Agent 运行 `azd provision --preview`
6. Agent 在项目根目录生成 `preflight-report.md`
7. Agent 总结发现结果并反馈给用户

## 参考文档

- [验证命令参考](references/VALIDATION-COMMANDS.md)
- [报告模板](references/REPORT-TEMPLATE.md)
- [错误处理指南](references/ERROR-HANDLING.md)

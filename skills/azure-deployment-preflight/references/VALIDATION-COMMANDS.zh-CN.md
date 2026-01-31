# 验证命令参考

本参考文档记录了用于 Azure 部署预检验证的所有命令。

## Azure 开发者 CLI (azd)

### azd provision --preview

预览 azd 项目中的基础设施变更，而不实际部署。

```bash
azd provision --preview [选项]
```

**选项：**
| 选项 | 描述 |
|--------|-------------|
| `--environment`, `-e` | 要使用的环境名称 |
| `--no-prompt` | 不提示直接接受默认值 |
| `--debug` | 启用调试日志 |
| `--cwd` | 设置工作目录 |

**示例：**

```bash
# 使用默认环境进行预览
azd provision --preview

# 预览特定环境
azd provision --preview --environment dev

# 无提示预览（CI/CD）
azd provision --preview --no-prompt
```

**输出：** 显示将要创建、修改或删除的资源。

### azd auth login

为 azd 操作对 Azure 进行身份验证。

```bash
azd auth login [选项]
```

**选项：**
| 选项 | 描述 |
|--------|-------------|
| `--check-status` | 检查登录状态而不进行登录 |
| `--use-device-code` | 使用设备代码流 |
| `--tenant-id` | 指定租户 |
| `--client-id` | 服务主体客户端 ID |

### azd env list

列出可用的环境。

```bash
azd env list
```

---

## Azure CLI (az)

### az deployment group what-if

预览资源组部署的变更。

```bash
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file <bicep-file> \
  [选项]
```

**必选参数：**
| 参数 | 描述 |
|-----------|-------------|
| `--resource-group`, `-g` | 目标资源组名称 |
| `--template-file`, `-f` | Bicep 文件路径 |

**可选参数：**
| 参数 | 描述 |
|-----------|-------------|
| `--parameters`, `-p` | 参数文件或内联值 |
| `--validation-level` | `Provider`（默认）、`ProviderNoRbac` 或 `Template` |
| `--result-format` | `FullResourcePayloads`（默认）或 `ResourceIdOnly` |
| `--no-pretty-print` | 输出原始 JSON 用于解析 |
| `--name`, `-n` | 部署名称 |
| `--exclude-change-types` | 排除特定变更类型输出 |

**验证级别：**
| 级别 | 描述 | 使用场景 |
|-------|-------------|----------|
| `Provider` | 包含 RBAC 检查的完整验证 | 默认，最全面 |
| `ProviderNoRbac` | 仅读取权限的完整验证 | 缺乏部署权限时 |
| `Template` | 仅静态语法验证 | 快速语法检查 |

**示例：**

```bash
# 基本预览
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep

# 使用参数文件和完整验证
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --validation-level Provider

# 无 RBAC 检查的回退
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --validation-level ProviderNoRbac

# 用于解析的 JSON 输出
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --no-pretty-print
```

### az deployment sub what-if

预览订阅级别部署的变更。

```bash
az deployment sub what-if \
  --location <location> \
  --template-file <bicep-file> \
  [选项]
```

**必选参数：**
| 参数 | 描述 |
|-----------|-------------|
| `--location`, `-l` | 部署元数据的位置 |
| `--template-file`, `-f` | Bicep 文件路径 |

**示例：**

```bash
az deployment sub what-if \
  --location eastus \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --validation-level Provider
```

### az deployment mg what-if

预览管理组级别部署的变更。

```bash
az deployment mg what-if \
  --location <location> \
  --management-group-id <mg-id> \
  --template-file <bicep-file> \
  [选项]
```

**必选参数：**
| 参数 | 描述 |
|-----------|-------------|
| `--location`, `-l` | 部署元数据的位置 |
| `--management-group-id`, `-m` | 目标管理组 ID |
| `--template-file`, `-f` | Bicep 文件路径 |

### az deployment tenant what-if

预览租户级别部署的变更。

```bash
az deployment tenant what-if \
  --location <location> \
  --template-file <bicep-file> \
  [选项]
```

**必选参数：**
| 参数 | 描述 |
|-----------|-------------|
| `--location`, `-l` | 部署元数据的位置 |
| `--template-file`, `-f` | Bicep 文件路径 |

### az login

对 Azure CLI 进行身份验证。

```bash
az login [选项]
```

**选项：**
| 选项 | 描述 |
|--------|-------------|
| `--tenant`, `-t` | 租户 ID 或域名 |
| `--use-device-code` | 使用设备代码流 |
| `--service-principal` | 以服务主体身份登录 |

### az account show

显示当前订阅上下文。

```bash
az account show
```

### az group exists

检查资源组是否存在。

```bash
az group exists --name <rg-name>
```

---

## Bicep CLI

### bicep build

将 Bicep 编译为 ARM JSON 并验证语法。

```bash
bicep build <bicep-file> [选项]
```

**选项：**
| 选项 | 描述 |
|--------|-------------|
| `--stdout` | 输出到标准输出而非文件 |
| `--outdir` | 输出目录 |
| `--outfile` | 输出文件路径 |
| `--no-restore` | 跳过模块恢复 |

**示例：**

```bash
# 验证语法（输出到标准输出，不创建文件）
bicep build main.bicep --stdout > /dev/null

# 构建到指定目录
bicep build main.bicep --outdir ./build

# 验证多个文件
for f in *.bicep; do bicep build "$f" --stdout; done
```

**错误输出格式：**
```
/path/to/file.bicep(22,51) : 错误 BCP064: 在插值表达式中发现意外的标记。
/path/to/file.bicep(22,51) : 错误 BCP004: 此位置的字符串未正确终止。
```

格式：`<文件>(<行>,<列>) : <严重性> <代码>: <消息>`

### bicep --version

检查 Bicep CLI 版本。

```bash
bicep --version
```

---

## 参数文件检测

### Bicep 参数 (.bicepparam)

现代 Bicep 参数文件（推荐）：

```bicep
using './main.bicep'

param location = 'eastus'
param environment = 'dev'
param tags = {
  environment: 'dev'
  project: 'myapp'
}
```

**检测模式：** `<模板名称>.bicepparam`

### JSON 参数 (.parameters.json)

传统 ARM 参数文件：

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "location": { "value": "eastus" },
    "environment": { "value": "dev" }
  }
}
```

**检测模式：**
- `<模板名称>.parameters.json`
- `parameters.json`
- `parameters/<env>.json`

### 使用参数文件与命令

```bash
# Bicep 参数文件
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters main.bicepparam

# JSON 参数文件
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters @parameters.json

# 内联参数覆盖
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --parameters location=westus
```

---

## 确定部署作用域

检查 Bicep 文件中的 `targetScope` 声明：

```bicep
// 资源组（未指定时默认）
targetScope = 'resourceGroup'

// 订阅
targetScope = 'subscription'

// 管理组
targetScope = 'managementGroup'

// 租户
targetScope = 'tenant'
```

**作用域到命令的映射：**

| targetScope | 命令 | 必选参数 |
|-------------|---------|---------------------|
| `resourceGroup` | `az deployment group what-if` | `--resource-group` |
| `subscription` | `az deployment sub what-if` | `--location` |
| `managementGroup` | `az deployment mg what-if` | `--location`, `--management-group-id` |
| `tenant` | `az deployment tenant what-if` | `--location` |

---

## 版本要求

| 工具 | 最低版本 | 推荐版本 | 关键特性 |
|------|-----------------|---------------------|--------------|
| Azure CLI | 2.14.0 | 2.76.0+ | `--validation-level` 切换 |
| Azure 开发者 CLI | 1.0.0 | 最新 | `--preview` 标志 |
| Bicep CLI | 0.4.0 | 最新 | 最佳错误信息 |

**检查版本：**
```bash
az --version
azd version
bicep --version
```

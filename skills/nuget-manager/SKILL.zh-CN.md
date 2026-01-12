

---
name: nuget-manager
description: '管理 .NET 项目/解决方案中的 NuGet 包。在添加、删除或更新 NuGet 包版本时使用此技能。它强制使用 `dotnet` CLI 进行包管理，并且仅在更新版本时允许直接编辑文件。'
---

# NuGet 管理器

## 概述

此技能确保在 .NET 项目中一致且安全地管理 NuGet 包。它优先使用 `dotnet` CLI 来维护项目完整性，并强制执行严格的版本更新验证和恢复流程。

## 先决条件

- 安装了 .NET SDK（通常为 .NET 8.0 SDK 或更高版本，或与目标解决方案兼容的版本）。
- `dotnet` CLI 已添加到系统路径（PATH）中。
- `jq`（JSON 处理器）或 PowerShell（用于通过 `dotnet package search` 验证版本）。

## 核心规则

1. **永远不要**直接编辑 `.csproj`、`.props` 或 `Directory.Packages.props` 文件以**添加**或**删除**包。始终使用 `dotnet add package` 和 `dotnet remove package` 命令。
2. **直接编辑**仅允许用于**更改现有包的版本**。
3. **版本更新**必须遵循强制流程：
   - 使用 `dotnet package search` 命令验证目标版本是否存在于 NuGet。
   - 确定版本是按项目管理（`.csproj`）还是集中管理（`Directory.Packages.props`）。
   - 在相应文件中更新版本字符串。
   - 立即运行 `dotnet restore` 以验证兼容性。

## 流程

### 添加包
使用 `dotnet add [<PROJECT>] package <PACKAGE_NAME> [--version <VERSION>]`。
示例：`dotnet add src/MyProject/MyProject.csproj package Newtonsoft.Json`

### 删除包
使用 `dotnet remove [<PROJECT>] package <PACKAGE_NAME>`。
示例：`dotnet remove src/MyProject/MyProject.csproj package Newtonsoft.Json`

### 更新包版本
在更新版本时，遵循以下步骤：

1. **验证版本存在性**：
   使用 `dotnet package search` 命令通过精确匹配和 JSON 格式检查版本是否存在。
   使用 `jq`：
   `dotnet package search <PACKAGE_NAME> --exact-match --format json | jq -e '.searchResult[].packages[] | select(.version == "<VERSION>")'`
   使用 PowerShell：
   `(dotnet package search <PACKAGE_NAME> --exact-match --format json | ConvertFrom-Json).searchResult.packages | Where-Object { $_.version -eq "<VERSION>" }`

2. **确定版本管理方式**：
   - 在解决方案根目录中搜索 `Directory.Packages.props`。如果存在，则应通过 `<PackageVersion Include="Package.Name" Version="1.2.3" />` 在该文件中进行版本管理。
   - 如果不存在，请检查各个 `.csproj` 文件中的 `<PackageReference Include="Package.Name" Version="1.2.3" />`。

3. **应用更改**：
   在识别出的文件中修改为新的版本字符串。

4. **验证稳定性**：
   在项目或解决方案上运行 `dotnet restore`。如果出现错误，请回滚更改并进行调查。

## 示例

### 用户："向 WebApi 项目添加 Serilog"
**操作**：执行 `dotnet add src/WebApi/WebApi.csproj package Serilog`。

### 用户："在整个解决方案中将 Newtonsoft.Json 更新为 13.0.3"
**操作**：
1. 验证 13.0.3 是否存在：`dotnet package search Newtonsoft.Json --exact-match --format json`（并解析输出以确认 "13.0.3" 存在）。
2. 查找其定义位置（例如 `Directory.Packages.props`）。
3. 修改文件以更新版本。
4. 运行 `dotnet restore`。
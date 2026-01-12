

---
description: 'PCF代码组件的应用生命周期管理（ALM）'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj,sln}'
---

# 代码组件的应用生命周期管理（ALM）

ALM 是用于描述软件应用程序生命周期管理的术语，包括开发、维护和治理。更多信息：[Microsoft Power Platform 的应用程序生命周期管理（ALM）](https://learn.microsoft.com/en-us/power-platform/alm/overview-alm)。

本文从 Microsoft Dataverse 中代码组件的视角，描述了与特定生命周期管理方面的考虑和策略：

1. 开发与调试的 ALM 考虑事项
2. 代码组件解决方案策略
3. 版本控制与部署更新
4. 画布应用的 ALM 考虑事项

## 开发与调试的 ALM 考虑事项

在开发代码组件时，您需要遵循以下步骤：

1. 使用 `pac pcf init` 命令从模板创建代码组件项目 (`pcfproj`)。更多信息：[创建和构建代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/create-custom-controls-using-pcf)。
2. 实现代码组件逻辑。更多信息：[组件实现](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/custom-controls-overview#component-implementation)。
3. 使用本地测试框架调试代码组件。更多信息：[调试代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/debugging-custom-controls)。
4. 创建解决方案项目 (`cdsproj`) 并将代码组件项目作为引用添加进去。更多信息：[打包代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/import-custom-controls)。
5. 以发布模式构建代码组件，以便分发和部署。

### 与 Dataverse 的两种部署方法

当您的代码组件准备好在模型驱动型应用、画布应用或门户中进行测试时，可以使用以下两种方法：

1. **`pac pcf push`**：此方法每次部署一个代码组件到由 `--solution-unique-name` 参数指定的解决方案，或在未指定解决方案时部署到临时 PowerAppsTools 解决方案。

2. **使用 `pac solution init` 和 `msbuild`**：构建一个包含一个或多个代码组件引用的 `cdsproj` 解决方案项目。使用 `pac solution add-reference` 命令将每个代码组件添加到 `cdsproj` 项目中。解决方案项目可以包含多个代码组件的引用，而代码组件项目可能仅包含一个代码组件。

以下图示展示了 `cdsproj` 和 `pcfproj` 项目之间的一对多关系：

![cdsproj 和 pcfproj 项目之间的一对多关系](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/code-component-projects.png)

更多信息：[打包代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/import-custom-controls#package-a-code-component)。

## 构建 pcfproj 代码组件项目

在构建 `pcfproj` 项目时，生成的 JavaScript 依赖于构建命令以及 `pcfproj` 文件中的 `PcfBuildMode`。

通常不建议将开发模式构建的代码组件部署到 Microsoft Dataverse，因为这些文件通常太大而无法导入，并可能导致运行时性能变慢。更多信息：[在 Microsoft Dataverse 中部署后调试](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/debugging-custom-controls#debugging-after-deploying-into-microsoft-dataverse)。

若要通过 `pac pcf push` 实现发布模式构建，需在 `pcfproj` 文件的 `OutputPath` 元素下添加一个新元素以设置 `PcfBuildMode`：

```xml
<PropertyGroup>
   <Name>my-control</Name>
   <ProjectGuid>6aaf0d27-ec8b-471e-9ed4-7b3bbc35bbab</ProjectGuid>
   <OutputPath>$(MSBuildThisFileDirectory)out\controls</OutputPath>
   <PcfBuildMode>production</PcfBuildMode>
</PropertyGroup>
```

### 构建命令

| 命令 | 默认行为 | PcfBuildMode=production 时 |
|------|----------|---------------------------|
| npm start watch | 始终为开发模式 |  |
| pac pcf push | 开发模式构建 | 发布模式构建 |
| npm run build | 开发模式构建 | `npm run build -- --buildMode production` |

更多信息：[打包代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/import-custom-controls#package-a-code-component)。

## 构建 .cdsproj 解决方案项目

在构建解决方案项目（`.cdsproj`）时，您可以选择生成输出为受管解决方案或不受管解决方案。受管解决方案用于部署到非该解决方案开发环境的任何环境，包括测试、UAT、SIT 和生产环境。更多信息：[受管和不受管解决方案](https://learn.microsoft.com/en-us/power-platform/alm/solution-concepts-alm#managed-and-unmanaged-solutions)。

由 `pac solution init` 创建的 `.cdsproj` 文件包含 `SolutionPackagerType`，但初始状态下是注释掉的。取消注释该部分并设置为 "Managed"、"Unmanaged" 或 "Both"。

```xml
<!-- 解决方案打包程序覆盖，取消注释以使用：SolutionPackagerType (Managed, Unmanaged, Both) -->
<PropertyGroup>
   <SolutionPackageType>Managed</SolutionPackageType>
</PropertyGroup>
```

### 构建配置结果

| 命令 | SolutionPackageType | 结果 |
|------|---------------------|------|
| msbuild | Managed | 在受管解决方案中进行开发模式构建 |
| msbuild /p:configuration=Release | Managed | 在受管解决方案中进行发布模式构建 |
| msbuild | Unmanaged | 在不受管解决方案中进行开发模式构建 |
| msbuild /p:configuration=Release | Unmanaged | 在不受管解决方案中进行发布模式构建 |

更多信息：[打包代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/import-custom-controls#package-a-code-component)。

## 使用代码组件进行源代码控制

在开发代码组件时，建议使用源代码控制提供商，如 Azure DevOps 或 GitHub。在使用 Git 源代码控制提交更改时，`pac pcf init` 模板提供的 `.gitignore` 文件会确保某些文件不会被添加到源代码控制中，因为这些文件要么由 `npm` 恢复，要么是构建过程的一部分：

```
# 依赖项
/node_modules

# 生成目录
**/generated

# 输出目录
/out

# msbuild 输出目录
/bin
/obj
```

由于 `/out` 文件夹被排除，构建出的 `bundle.js` 文件（及相关资源）不会被添加到源代码控制中。当您的代码组件是手动构建或作为自动化构建流水线的一部分构建时，`bundle.js` 将使用最新的代码进行构建，以确保所有更改都被包含。

此外，当构建解决方案时，任何关联的解决方案 zip 文件都不会被提交到源代码控制中。相反，输出将作为二进制发布工件发布。

## 使用 SolutionPackager 进行代码组件管理

除了对 `pcfproj` 和 `cdsproj` 进行源代码控制外，[SolutionPackager](https://learn.microsoft.com/en-us/power-platform/alm/solution-packager-tool) 还可用于将解决方案逐步解包为一系列 XML 文件，这些文件可以提交到源代码控制中。这种方法的优势在于可以以人类可读的格式创建完整的元数据视图，从而可以使用拉取请求等工具跟踪更改。

> **注意**：目前，SolutionPackager 与使用 `pac solution clone` 不同，它可以逐步导出 Dataverse 解决方案中的更改。

### 示例解决方案结构

一旦使用 `SolutionPackager /action: Extract` 解包一个包含代码组件的解决方案，其结构将类似于以下内容：

```
.
├── Controls
│   └── prefix_namespace.ControlName
│       ├── bundle.js *
│       └── css
│          └── ControlName.css *
│       ├── ControlManifest.xml *
│       └── ControlManifest.xml.data.xml
├── Entities
│   └── Contact
│       ├── FormXml
│       │   └── main
│       │       └── {3d60f361-84c5-eb11-bacc-000d3a9d0f1d}.xml
│       ├── Entity.xml
│       └── RibbonDiff.xml
└── Other
    ├── Customizations.xml
    └── Solution.xml
```

在 `Controls` 文件夹下，可以看到每个解决方案中包含的代码组件的子文件夹。将此文件夹结构提交到源代码控制时，应排除上面标记为星号 (*) 的文件，因为这些文件会在 `pcfproj` 项目为对应组件构建时生成。

唯一需要的文件是 `*.data.xml` 文件，因为它们包含描述打包过程所需资源的元数据。

更多信息：[SolutionPackager 命令行参数](https://learn.microsoft.com/en-us/power-platform/alm/solution-packager-tool#solutionpackager-command-line-arguments)。

## 代码组件解决方案策略

代码组件通过 Dataverse 解决方案部署到下游环境。在解决方案中部署代码组件有两种策略：

### 1. 分段解决方案

使用 `pac solution init` 创建解决方案项目，然后使用 `pac solution add-reference` 添加一个或多个代码组件。此解决方案可以导出并导入到下游环境和其他分段解决方案中，其他分段解决方案会依赖该代码组件解决方案，因此必须首先部署到该环境。

**采用分段解决方案方法的原因：**

1. **版本生命周期管理** - 您希望将代码组件的开发、部署和版本控制与解决方案的其他部分分开。这在“融合团队”场景中很常见，其中开发人员构建的代码组件被应用程序开发人员使用。
2. **共享使用** - 您希望在多个环境中共享代码组件，因此不希望将代码组件与其他解决方案组件耦合。这可能适用于您是 ISV（独立软件供应商）或为组织的不同部分开发代码组件的情况。

### 2. 单一解决方案

在 Dataverse 环境中创建一个单一解决方案，然后将代码组件与其他解决方案组件（如表、模型驱动型应用或画布应用）一起添加，这些组件反过来引用这些代码组件。此解决方案可以导出并导入到下游环境，而无需任何跨解决方案依赖。

### 解决方案生命周期概述

![解决方案策略](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/solution-strategies.png)

更多信息：[使用解决方案打包和分发扩展](https://learn.microsoft.com/en-us/powerapps/developer/data-platform/introduction-solutions)。

## 代码组件与自动化构建流水线

除了手动构建和部署代码组件解决方案外，您还可以使用自动化构建流水线来构建和打包代码组件。

- 如果您使用 Azure DevOps，可以使用 [Azure DevOps 的 Microsoft Power Platform 构建工具](https://learn.microsoft.com/en-us/power-platform/alm/devops-build-tools)。
- 如果您使用 GitHub，可以使用 [Power Platform GitHub Actions](https://learn.microsoft.com/en-us/power-platform/alm/devops-github-actions)。

### 自动化构建流水线的优势

- **节省时间** - 去除手动任务，使构建和打包更快
- **可重复性** - 每次执行相同的操作，不依赖团队成员
- **版本一致性** - 自动相对于前一版本进行版本控制
- **易于维护** - 构建所需的所有内容都包含在源代码控制中

## 版本控制与部署更新

在部署和更新代码组件时，保持一致的版本控制策略非常重要。一种常见的版本控制策略是 [语义化版本控制](https://semver.org/)，其格式为：`MAJOR.MINOR.PATCH`。

### 增加 PATCH 版本

`ControlManifest.Input.xml` 存储代码组件的版本信息在控制元素中：

```xml
<control namespace="..." constructor="..." version="1.0.0" display-name-key="..." description-key="..." control-type="...">
```

当部署代码组件的更新时，`ControlManifest.Input.xml` 中的版本必须至少将 PATCH（版本的最后部分）增加，以便检测到更改。

**更新版本的命令：**

```bash
# 将 PATCH 版本增加 1
pac pcf version --strategy manifest

# 指定精确的 PATCH 版本（例如在自动化构建流水线中）
pac pcf version --patchversion <PATCH VERSION>
```

### 何时增加 MAJOR 和 MINOR 版本

建议将代码组件的 MAJOR 和 MINOR 版本与分发的 Dataverse 解决方案版本保持同步。

[Dataverse 解决方案有四个部分](https://learn.microsoft.com/en-us/powerapps/maker/data-platform/update-solutions#understanding-version-numbers-for-updates)：`MAJOR.MINOR.BUILD.REVISION`。

| 代码组件 | Dataverse 解决方案 | 说明 |
|----------|---------------------|------|
| MAJOR | MAJOR | 使用流水线变量或最后提交的值设置 |
| MINOR | MINOR | 使用流水线变量或最后提交的值设置 |
| PATCH | BUILD | $(Build.BuildId) |
| --- | REVISION | $(Rev:r) |

## 画布应用的 ALM 考虑事项

在画布应用中使用代码组件与在模型驱动型应用中使用的方式不同。代码组件必须通过在插入面板中选择 **获取更多组件** 显式添加到应用中。一旦代码组件被添加到画布应用中，它就会作为应用定义中的内容包含进去。

在部署后更新到代码组件的新版本时，应用开发人员必须首先在 Power Apps Studio 中打开应用，并在提示的“更新代码组件”对话框中选择 **更新**。然后，应用必须保存并发布，以便用户在运行应用时使用新版本。

![更新代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/upgrade-code-component.png)

如果应用未更新或使用了 **跳过** 选项，即使该版本已被新版本覆盖，应用仍将继续使用旧版本的代码组件。

由于应用包含代码组件的副本，因此可以在同一环境中通过不同的画布应用同时运行不同版本的代码组件。然而，您不能在同一个应用中同时运行不同版本的代码组件。

> **注意**：虽然目前您可以导入一个画布应用而不将匹配的代码组件部署到该环境，但建议始终确保应用更新以使用最新的代码组件版本，并且该版本首先或作为同一解决方案的一部分部署到该环境。
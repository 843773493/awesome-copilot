---
name: aspire
description: 'Aspire 技能涵盖 Aspire CLI、AppHost 编排、服务发现、集成、MCP 服务器、VS Code 扩展、Dev 容器、GitHub Codespaces、模板、仪表板和部署。当用户请求创建、运行、调试、配置、部署或排查 Aspire 分布式应用时使用。'
---

# Aspire — 多语言分布式应用编排

Aspire 是一个 **以代码为中心的多语言工具链**，用于构建可观察、可生产化的分布式应用。它通过一个 AppHost 项目编排容器、可执行文件和云资源 —— 无论工作负载是 C#、Python、JavaScript/TypeScript、Go、Java、Rust、Bun、Deno 还是 PowerShell。

> **思维模型：** AppHost 是一个 *指挥者* —— 它不直接操作各个组件，而是告诉每个服务何时启动、如何互相发现，并监控可能出现的问题。

详细参考材料位于 `references/` 文件夹中 —— 按需加载。

---

## 参考资料

| 参考资料 | 加载时机 |
|---|---|
| [CLI 参考](references/cli-reference.md) | 命令标志、选项或详细使用 |
| [MCP 服务器](references/mcp-server.md) | 为 AI 助手设置 MCP，可用工具 |
| [集成目录](references/integrations-catalog.md) | 通过 MCP 工具发现集成，连接模式 |
| [多语言 API](references/polyglot-apis.md) | 方法签名、链式选项、语言特定模式 |
| [架构](references/architecture.md) | DCP 内部机制、资源模型、服务发现、网络、遥测 |
| [仪表板](references/dashboard.md) | 仪表板功能、独立模式、生成式AI可视化器 |
| [部署](references/deployment.md) | Docker、Kubernetes、Azure 容器应用、应用服务 |
| [测试](references/testing.md) | 针对 AppHost 的集成测试 |
| [故障排查](references/troubleshooting.md) | 诊断代码、常见错误及修复方案 |

---

## 1. 研究 Aspire 文档

Aspire 团队提供了一个 **MCP 服务器**，它直接在您的 AI 助手中提供文档工具。有关设置详情，请参阅 [MCP 服务器](references/mcp-server.md)。

### Aspire CLI 13.2+（推荐 —— 内置文档搜索）

如果运行的是 Aspire CLI **13.2 或更高版本**（`aspire --version`），MCP 服务器包含文档搜索工具：

| 工具 | 描述 |
|---|---|
| `list_docs` | 列出所有来自 aspire.dev 的文档 |
| `search_docs` | 在索引文档中执行加权词法搜索 |
| `get_doc` | 通过文档的 slug 获取特定文档 |

这些工具是在 [PR #14028](https://github.com/dotnet/aspire/pull/14028) 中添加的。要更新：`aspire update --self --channel daily`。

有关此方法的更多信息，请参阅 David Pine 的文章：https://davidpine.dev/posts/aspire-docs-mcp-tools/

### Aspire CLI 13.1（仅集成工具）

在 13.1 版本中，MCP 服务器提供集成查找，但 **不支持** 文档搜索：

| 工具 | 描述 |
|---|---|
| `list_integrations` | 列出可用的 Aspire 主机集成 |
| `get_integration_docs` | 获取特定集成包的文档 |

在 13.1 版本中，对于通用文档查询，请使用 **Context7** 作为主要来源（见下文）。

### 备用方案：Context7

当 Aspire MCP 文档工具不可用（13.1 版本）或 MCP 服务器未运行时，请使用 **Context7** (`mcp_context7`)：

**步骤 1 — 解析库 ID**（每次会话一次性）：

调用 `mcp_context7_resolve-library-id` 并传入 `libraryName: ".NET Aspire"`。

| 排名 | 库 ID | 使用场景 |
|---|---|---|
| 1 | `/microsoft/aspire.dev` | 主要来源。指南、集成、CLI 参考、部署。 |
| 2 | `/dotnet/aspire` | API 内部机制、源代码实现细节。 |
| 3 | `/communitytoolkit/aspire` | 非微软的多语言集成（Go、Java、Node.js、Ollama）。 |

**步骤 2 — 查询文档：**

```
libraryId: "/microsoft/aspire.dev", query: "Python 集成 AddPythonApp 服务发现"
libraryId: "/communitytoolkit/aspire", query: "Golang Java Node.js 社区集成"
```

### 备用方案：GitHub 搜索（当 Context7 也不可用时）

在 GitHub 上搜索官方文档仓库：
- **文档仓库：** `microsoft/aspire.dev` —— 路径：`src/frontend/src/content/docs/`
- **源代码仓库：** `dotnet/aspire`
- **示例仓库：** `dotnet/aspire-samples`
- **社区集成：** `CommunityToolkit/Aspire`

---

## 2. 先决条件与安装

| 要求 | 详情 |
|---|---|
| **.NET SDK** | 10.0+（即使非 .NET 工作负载也需要）—— AppHost 是 .NET |
| **容器运行时** | Docker Desktop、Podman 或 Rancher Desktop |
| **IDE（可选）** | VS Code + C# 开发工具包、Visual Studio 2022、JetBrains Rider |

```bash
# Linux / macOS
curl -sSL https://aspire.dev/install.sh | bash

# Windows PowerShell
irm https://aspire.dev/install.ps1 | iex

# 验证
aspire --version

# 安装模板
dotnet new install Aspire.ProjectTemplates
```

---

## 3. 项目模板

| 模板 | 命令 | 描述 |
|---|---|---|
| **aspire-starter** | `aspire new aspire-starter` | ASP.NET Core/Blazor 初始模板 + AppHost + 测试 |
| **aspire-ts-cs-starter** | `aspire new aspire-ts-cs-starter` | ASP.NET Core/React 初始模板 + AppHost |
| **aspire-py-starter** | `aspire new aspire-py-starter` | FastAPI/React 初始模板 + AppHost |
| **aspire-apphost-singlefile** | `aspire new aspire-apphost-singlefile` | 空的单文件 AppHost |

---

## 4. AppHost 快速入门（多语言）

AppHost 编排所有服务。非 .NET 工作负载以容器或可执行文件形式运行。

```csharp
var builder = DistributedApplication.CreateBuilder(args);

// 基础设施
var redis = builder.AddRedis("cache");
var postgres = builder.AddPostgres("pg").AddDatabase("catalog");

// .NET API
var api = builder.AddProject<Projects.CatalogApi>("api")
    .WithReference(postgres).WithReference(redis);

// Python 机器学习服务
var ml = builder.AddPythonApp("ml-service", "../ml-service", "main.py")
    .WithHttpEndpoint(targetPort: 8000).WithReference(redis);

// React 前端（Vite）
var web = builder.AddViteApp("web", "../frontend")
    .WithHttpEndpoint(targetPort: 5173).WithReference(api);

// Go 工作者
var worker = builder.AddGolangApp("worker", "../go-worker")
    .WithReference(redis);

builder.Build().Run();
```

完整 API 签名请参阅 [多语言 API](references/polyglot-apis.md)。

---

## 5. 核心概念（摘要）

| 概念 | 关键点 |
|---|---|
| **运行 vs 发布** | `aspire run` = 本地开发（DCP 引擎）。`aspire publish` = 生成部署清单。 |
| **服务发现** | 通过环境变量自动完成：`ConnectionStrings__<name>`、`services__<name>__http__0` |
| **资源生命周期** | DAG 排序 —— 依赖项优先启动。`.WaitFor()` 用于健康检查门控。 |
| **资源类型** | `ProjectResource`、`ContainerResource`、`ExecutableResource`、`ParameterResource` |
| **集成** | 跨 13 个类别共 144+ 种集成。主机包（AppHost）+ 客户端包（服务）。 |
| **仪表板** | 实时日志、追踪、指标、生成式AI可视化器。通过 `aspire run` 自动运行。 |
| **MCP 服务器** | AI 助手可通过 CLI（STDIO）查询正在运行的应用并搜索文档。 |
| **测试** | `Aspire.Hosting.Testing` —— 在 xUnit/MSTest/NUnit 中启动完整的 AppHost。 |
| **部署** | Docker、Kubernetes、Azure 容器应用、Azure 应用服务。 |

---

## 6. CLI 快速参考

Aspire CLI 13.1 中的有效命令：

| 命令 | 描述 | 状态 |
|---|---|---|
| `aspire new <template>` | 从模板创建 | 稳定 |
| `aspire init` | 在现有项目中初始化 | 稳定 |
| `aspire run` | 本地启动所有资源 | 稳定 |
| `aspire add <integration>` | 添加集成 | 稳定 |
| `aspire publish` | 生成部署清单 | 预览 |
| `aspire config` | 管理配置设置 | 稳定 |
| `aspire cache` | 管理磁盘缓存 | 稳定 |
| `aspire deploy` | 部署到定义的目标 | 预览 |
| `aspire do <step>` | 执行流水线步骤 | 预览 |
| `aspire update` | 更新集成（或 `--self` 更新 CLI） | 预览 |
| `aspire mcp init` | 为 AI 助手配置 MCP | 稳定 |
| `aspire mcp start` | 启动 MCP 服务器 | 稳定 |

完整命令参考及标志：[CLI 参考](references/cli-reference.md)。

---

## 7. 常见模式

### 添加新服务

1. 创建服务目录（任意语言）
2. 添加到 AppHost：`Add*App()` 或 `AddProject<T>()`
3. 连接依赖项：`.WithReference()`
4. 如需健康检查门控：`.WaitFor()`
5. 运行：`aspire run`

### 从 Docker Compose 迁移

1. `aspire new aspire-apphost-singlefile`（空的 AppHost）
2. 将每个 `docker-compose` 服务替换为 Aspire 资源
3. `depends_on` → `.WithReference()` + `.WaitFor()`
4. `ports` → `.WithHttpEndpoint()`
5. `environment` → `.WithEnvironment()` 或 `.WithReference()`

---

## 8. 关键网址

| 资源 | 网址 |
|---|---|
| **文档** | https://aspire.dev |
| **运行时仓库** | https://github.com/dotnet/aspire |
| **文档仓库** | https://github.com/microsoft/aspire.dev |
| **示例** | https://github.com/dotnet/aspire-samples |
| **社区工具包** | https://github.com/CommunityToolkit/Aspire |
| **仪表板镜像** | `mcr.microsoft.com/dotnet/aspire-dashboard` |
| **Discord** | https://aka.ms/aspire/discord |
| **Reddit** | https://www.reddit.com/r/aspiredotdev/ |

---
name: microsoft-docs
description: '查询官方微软文档，以查找 Azure、.NET、Agent Framework、Aspire、VS Code、GitHub 等技术生态中的概念、教程和代码示例。默认使用 Microsoft Learn MCP，对于位于 learn.microsoft.com 之外的内容，使用 Context7 和 Aspire MCP。'
---

# 微软文档

研究微软技术生态系统的技能。涵盖 learn.microsoft.com 以及其外部的文档（VS Code、GitHub、Aspire、Agent Framework 仓库）。

---

## 默认：Microsoft Learn MCP

使用这些工具处理 **learn.microsoft.com 上的所有内容** — Azure、.NET、M365、Power Platform、Agent Framework、Semantic Kernel、Windows 等。这是大多数微软文档查询的主要工具。

| 工具 | 用途 |
|------|---------|
| `microsoft_docs_search` | 搜索 learn.microsoft.com — 概念、指南、教程、配置 |
| `microsoft_code_sample_search` | 从 Learn 文档中查找可运行的代码片段。传入 `language`（如 `python`、`csharp` 等）以获得最佳结果 |
| `microsoft_docs_fetch` | 从特定 URL 获取完整页面内容（当搜索摘要不够时） |

在需要完整教程、所有配置选项或搜索摘要被截断时，使用 `microsoft_docs_fetch` 继续搜索。

---

## 异常情况：何时使用其他工具

以下类别文档位于 **learn.microsoft.com 之外**。请改用指定的工具。

### .NET Aspire — 使用 Aspire MCP 服务器（推荐）或 Context7

Aspire 文档位于 **aspire.dev**，而非 Learn。最佳工具取决于您的 Aspire CLI 版本：

**CLI 13.2+**（推荐） — Aspire MCP 服务器包含内置的文档搜索工具：

| MCP 工具 | 描述 |
|----------|-------------|
| `list_docs` | 列出 aspire.dev 上所有可用的文档 |
| `search_docs` | 在 aspire.dev 内容上执行加权词法搜索 |
| `get_doc` | 通过 slug 获取特定文档 |

这些工具包含在 Aspire CLI 13.2 中（[PR #14028](https://github.com/dotnet/aspire/pull/14028)）。更新方式：`aspire update --self --channel daily`。参考：https://davidpine.dev/posts/aspire-docs-mcp-tools/

**CLI 13.1** — MCP 服务器提供集成查找（`list_integrations`、`get_integration_docs`），但 **不提供** 文档搜索。请回退到 Context7：

| 库ID | 用途 |
|---|---|
| `/microsoft/aspire.dev` | 主要用途 — 指南、集成、CLI 参考、部署 |
| `/dotnet/aspire` | 运行时源码 — API 内部实现、具体实现细节 |
| `/communitytoolkit/aspire` | 社区集成 — Go、Java、Node.js、Ollama |

### VS Code — 使用 Context7

VS Code 文档位于 **code.visualstudio.com**，而非 Learn。

| 库ID | 用途 |
|---|---|
| `/websites/code_visualstudio` | 用户文档 — 设置、功能、调试、远程开发 |
| `/websites/code_visualstudio_api` | 扩展 API — webviews、TreeViews、命令、贡献点 |

### GitHub — 使用 Context7

GitHub 文档位于 **docs.github.com** 和 **cli.github.com**。

| 库ID | 用途 |
|---|---|
| `/websites/github_en` | Actions、API、仓库、安全、管理、Copilot |
| `/websites/cli_github` | GitHub CLI (`gh`) 命令和标志 |

### Agent Framework — 使用 Learn MCP + Context7

Agent Framework 教程位于 learn.microsoft.com（使用 `microsoft_docs_search`），但 **GitHub 仓库** 包含 API 层面的详细信息，通常领先于已发布的文档 — 特别是 DevUI REST API 参考、CLI 选项和 .NET 集成。

| 库ID | 用途 |
|---|---|
| `/websites/learn_microsoft_en-us_agent-framework` | 教程 — DevUI 指南、追踪、工作流编排 |
| `/microsoft/agent-framework` | API 详细信息 — DevUI REST 端点、CLI 标志、认证、.NET `AddDevUI`/`MapDevUI` |

**DevUI 提示：** 查询 Learn 网站源码获取操作指南，再查询仓库源码获取 API 层面的具体信息（端点结构、代理配置、认证令牌）。

---

## Context7 设置

对于任何 Context7 查询，首先解析库 ID（每会话仅需一次）：

1. 使用技术名称调用 `mcp_context7_resolve-library-id`  
2. 使用返回的库 ID 和特定查询调用 `mcp_context7_query-docs`  

---

## 编写高效的查询

请具体说明 — 包含版本、意图和语言：

```
# ❌ 过于宽泛
"Azure Functions"
"agent framework"

# ✅ 具体明确
"Azure Functions Python v2 编程模型"
"Cosmos DB 分区键设计最佳实践"
"GitHub Actions workflow_dispatch 输入矩阵策略"
"Aspire AddUvicornApp Python FastAPI 集成"
"DevUI 服务代理追踪 OpenTelemetry 目录发现"
"Agent Framework 工作流条件边分支交接"
```

包含上下文信息：
- **版本**（如 `.NET 8`、`Aspire 13`、`VS Code 1.96`）  
- **任务意图**（如 `快速入门`、`教程`、`概述`、`限制`、`API 参考`）  
- **语言**（如 `Python`、`TypeScript`、`C#`）以支持多语言文档

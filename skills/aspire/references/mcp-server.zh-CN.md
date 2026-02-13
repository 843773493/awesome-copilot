# MCP 服务器 — 完整参考

Aspire 提供了一个 **MCP（模型上下文协议）服务器**，允许 AI 编码助手查询和控制您正在运行的分布式应用程序，并搜索 Aspire 文档。这使得 AI 工具能够检查资源状态、读取日志、查看追踪、重启服务以及查阅文档 —— 所有操作都可以在 AI 助手的上下文中完成。

参考：https://aspire.dev/get-started/configure-mcp/

---

## 配置：`aspire mcp init`

配置 MCP 服务器的最简单方法是使用 Aspire CLI：

```bash
# 在项目目录中打开终端
aspire mcp init
```

该命令会引导您完成一个交互式配置流程：

1. **工作区根目录** — 提示您输入工作区根目录的路径（默认为当前目录）
2. **环境检测** — 检测支持的 AI 环境（如 VS Code、Copilot CLI、Claude Code、OpenCode）并询问要配置哪个环境
3. **Playwright MCP** — 可选地提供配置 Playwright MCP 服务器的选项（与 Aspire 一起）
4. **配置文件创建** — 生成相应的配置文件（例如 `.vscode/mcp.json`）
5. **AGENTS.md** — 如果不存在，则创建一个包含 Aspire 特定说明的 `AGENTS.md` 文件用于 AI 代理

> **注意：** `aspire mcp init` 使用交互式提示（Spectre.Console）。必须在真实终端中运行 —— VS Code 集成终端可能无法正确处理提示。如需使用，可使用外部终端。

---

## 理解配置

运行 `aspire mcp init` 命令后，CLI 会根据检测到的环境生成相应的配置文件。

### VS Code（GitHub Copilot）

创建或更新 `.vscode/mcp.json` 文件：

```json
{
  "servers": {
    "aspire": {
      "type": "stdio",
      "command": "aspire",
      "args": ["mcp", "start"]
    }
  }
}
```

---

## MCP 工具

可用的工具取决于您的 Aspire CLI 版本。请使用 `aspire --version` 检查版本。

### 13.1+（稳定版）可用的工具

#### 资源管理工具

这些工具需要运行中的 AppHost（`aspire run`）。

| 工具                         | 描述                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------ |
| `list_resources`             | 列出所有资源，包括状态、健康状况、源代码、端点和命令                |
| `list_console_logs`          | 列出特定资源的控制台日志                                                                   |
| `list_structured_logs`       | 列出结构化日志，可选地按资源名称进行过滤                                         |
| `list_traces`                | 列出分布式追踪。可选地通过资源名称参数进行过滤          |
| `list_trace_structured_logs` | 列出特定追踪的结构化日志                                                          |
| `execute_resource_command`   | 执行资源命令（接受资源名称和命令名称）                                |

#### AppHost 管理工具

| 工具             | 描述                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------- |
| `list_apphosts`  | 列出所有检测到的 AppHost 连接，显示哪些在工作目录作用域内，哪些不在 |
| `select_apphost` | 当有多个 AppHost 运行时，选择使用哪一个                                      |

#### 集成工具

这些工具无需运行 AppHost 即可使用。

| 工具                   | 描述                                                                                                       |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `list_integrations`    | 列出可用的 Aspire 主机集成（如数据库、消息代理、云服务等的 NuGet 包） |
| `get_integration_docs` | 获取特定 Aspire 主机集成包的文档                                              |

### 13.2+（文档搜索）新增的工具

> **版本限制：** 这些工具在 [PR #14028](https://github.com/dotnet/aspire/pull/14028) 中添加，并包含在 Aspire CLI **13.2** 中。如果您使用的是 13.1 版本，这些工具将不会显示。如需提前获取，请更新到每日频道：`aspire update --self --channel daily`。

| 工具          | 描述                                                              |
| ------------- | ------------------------------------------------------------------------ |
| `list_docs`   | 列出 aspire.dev 上所有可用的文档                        |
| `search_docs` | 在索引的 aspire.dev 文档中执行加权词法搜索 |
| `get_doc`     | 通过其 slug 标识符检索特定文档                                |

这些工具使用 `llms.txt` 规范对 aspire.dev 内容进行索引，并提供加权词法搜索（标题 10 倍权重，摘要 8 倍权重，标题 6 倍权重，代码 5 倍权重，正文 1 倍权重）。它们无需运行 AppHost 即可使用。

### 文档回退（13.1 用户）

如果您使用的是 Aspire CLI 13.1 且没有 `list_docs`/`search_docs`/`get_doc` 工具，可以使用 **Context7** 作为文档查询的回退方案。有关集成特定文档的详细信息，请参阅 [SKILL.md 文档研究部分](../SKILL.md#1-researching-aspire-documentation)。

---

## 从 MCP 排除资源

通过注释资源，可以将其从 MCP 结果中排除：

```csharp
var builder = DistributedApplication.CreateBuilder(args);

var apiService = builder.AddProject<Projects.Api>("apiservice")
    .ExcludeFromMcp();  // 从 MCP 工具中隐藏

builder.AddProject<Projects.Web>("webfrontend")
    .WithExternalHttpEndpoints()
    .WithReference(apiService);

builder.Build().Run();
```

---

## 支持的 AI 助手

`aspire mcp init` 命令支持以下 AI 助手：

- [VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)（GitHub Copilot）
- [Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli#add-an-mcp-server)
- [Claude Code](https://docs.claude.com/en/docs/claude-code/mcp)
- [OpenCode](https://opencode.ai/docs/mcp-servers/)

MCP 服务器使用 **STDIO 传输协议**，可能与其他支持此协议的代理编码环境兼容。

---

## 使用模式

### 使用 AI 助力调试

一旦 MCP 配置完成，您的 AI 助手可以：

1. **检查运行状态：**

   - "列出我的所有 Aspire 资源及其状态"
   - "数据库是否健康？"
   - "API 在哪个端口运行？"

2. **读取日志：**

   - "显示 ML 服务的最近日志"
   - "工作者日志中是否有错误？"

3. **查看追踪：**

   - "显示最后一次失败请求的追踪"
   - "API 到数据库调用的延迟是多少？"

4. **控制资源：**

   - "重启 API 服务"
   - "在调试队列时停止工作者"

5. **搜索文档（13.2+）：**
   - "在 Aspire 文档中搜索 Redis 缓存"
   - "如何配置服务发现？"
   - _(需要 CLI 13.2+。在 13.1 上，请使用 Context7 或 `list_integrations`/`get_integration_docs` 获取集成特定文档。)_

---

## 安全性考虑

- MCP 服务器仅暴露本地 AppHost 的资源
- 无需认证（仅限本地开发）
- STDIO 传输协议仅适用于启动该进程的 AI 工具
- **不要在生产环境中将 MCP 端点暴露到网络中**

---

## 局限性

- AI 模型对数据处理有局限性。大型数据字段（如堆栈跟踪）可能会被截断。
- 涉及大量遥测数据的请求可能会省略较旧条目以缩短结果。

---

## 故障排除

如果遇到问题，请检查 [GitHub 上的开放 MCP 问题](https://github.com/dotnet/aspire/issues?q=is%3Aissue+is%3Aopen+label%3Aarea-mcp)。

## 参见

- [aspire mcp 命令](https://aspire.dev/reference/cli/commands/aspire-mcp/)
- [aspire mcp init 命令](https://aspire.dev/reference/cli/commands/aspire-mcp-init/)
- [aspire mcp start 命令](https://aspire.dev/reference/cli/commands/aspire-mcp-start/)
- [Dashboard 中的 GitHub Copilot](https://aspire.dev/dashboard/copilot/)
- [我如何教 AI 阅读 Aspire 文档](https://davidpine.dev/posts/aspire-docs-mcp-tools/)

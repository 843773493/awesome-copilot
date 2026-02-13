# CLI 参考 — 完整命令参考

Aspire 命令行界面（`aspire`）是创建、运行和发布分布式应用程序的主要接口。它支持跨平台，并且是独立安装的（不与 .NET CLI 耦合，尽管 `dotnet` 命令也有效）。

**已测试版本：** Aspire CLI 13.1.0

---

## 安装

```bash
# Linux / macOS
curl -sSL https://aspire.dev/install.sh | bash

# Windows PowerShell
irm https://aspire.dev/install.ps1 | iex

# 验证
aspire --version

# 更新 CLI 本身
aspire update --self
```

---

## 全局选项

所有命令均支持以下选项：

| 选项                | 描述                                    |
| --------------------- | ---------------------------------------------- |
| `-d, --debug`         | 启用调试日志记录到控制台            |
| `--non-interactive`   | 禁用所有交互式提示和加载动画   |
| `--wait-for-debugger` | 在执行前等待调试器附加 |
| `-?, -h, --help`      | 显示帮助和使用信息                |
| `--version`           | 显示版本信息                       |

---

## 命令参考

### `aspire new`

从模板创建新项目。

```bash
aspire new [<template>] [options]

# 选项：
#   -n, --name <name>        项目名称
#   -o, --output <dir>       输出目录
#   -s, --source <source>    模板的 NuGet 源
#   -v, --version <version>  使用的模板版本
#   --channel <channel>      渠道（stable, daily）

# 示例：
aspire new aspire-starter
aspire new aspire-starter -n MyApp -o ./my-app
aspire new aspire-ts-cs-starter
aspire new aspire-py-starter
aspire new aspire-apphost-singlefile
```

可用模板：

- `aspire-starter` — ASP.NET Core/Blazor 初始模板 + AppHost + 测试项目
- `aspire-ts-cs-starter` — ASP.NET Core/React + AppHost
- `aspire-py-starter` — FastAPI/React + AppHost
- `aspire-apphost-singlefile` — 空的单文件 AppHost

### `aspire init`

在现有项目或解决方案中初始化 Aspire。

```bash
aspire init [options]

# 选项：
#   -s, --source <source>    模板的 NuGet 源
#   -v, --version <version>  使用的模板版本
#   --channel <channel>      渠道（stable, daily）

# 示例：
cd my-existing-solution
aspire init
```

将 AppHost 和 ServiceDefaults 项目添加到现有解决方案中。交互式提示将引导您选择要编排的项目。

### `aspire run`

使用 DCP（开发者控制平面）在本地启动所有资源。

```bash
aspire run [options] [-- <additional arguments>]

# 选项：
#   --project <path>       AppHost 项目文件路径

# 示例：
aspire run
aspire run --project ./src/MyApp.AppHost
```

行为：

1. 构建 AppHost 项目
2. 启动 DCP 引擎
3. 按依赖顺序创建资源（DAG）
4. 等待受控资源的健康检查
5. 在默认浏览器中打开仪表板
6. 将日志流式传输到终端

按 `Ctrl+C` 可优雅地停止所有资源。

### `aspire add`

将托管集成添加到 AppHost。

```bash
aspire add [<integration>] [options]

# 选项：
#   --project <path>         目标项目文件
#   -v, --version <version>  要添加的集成版本
#   -s, --source <source>    集成的 NuGet 源

# 示例：
aspire add redis
aspire add postgresql
aspire add mongodb
```

### `aspire publish`（预览版）

从 AppHost 资源模型生成部署清单。

```bash
aspire publish [options] [-- <additional arguments>]

# 选项：
#   --project <path>                   AppHost 项目文件路径
#   -o, --output-path <path>           部署输出目录（默认：./aspire-output）
#   --log-level <level>                日志级别（trace, debug, information, warning, error, critical）
#   -e, --environment <env>            环境（默认：Production）
#   --include-exception-details        在流水线日志中包含异常详细信息

# 示例：
aspire publish
aspire publish --output-path ./deploy
aspire publish -e Staging
```

### `aspire config`

管理 Aspire 配置设置。

```bash
aspire config <subcommand>

# 子命令：
#   get <key>              获取配置值
#   set <key> <value>      设置配置值
#   list                   列出所有配置值
#   delete <key>           删除配置值

# 示例：
aspire config list
aspire config set telemetry.enabled false
aspire config get telemetry.enabled
aspire config delete telemetry.enabled
```

### `aspire cache`

管理 CLI 操作的磁盘缓存。

```bash
aspire cache <subcommand>

# 子命令：
#   clear                  清除所有缓存条目

# 示例：
aspire cache clear
```

### `aspire deploy`（预览版）

将 Aspire apphost 的内容部署到其定义的部署目标。

```bash
aspire deploy [options] [-- <additional arguments>]

# 选项：
#   --project <path>                   AppHost 项目文件路径
#   -o, --output-path <path>           部署工件的输出路径
#   --log-level <level>                日志级别（trace, debug, information, warning, error, critical）
#   -e, --environment <env>            环境（默认：Production）
#   --include-exception-details        在流水线日志中包含异常详细信息
#   --clear-cache                      清除当前环境的部署缓存

# 示例：
aspire deploy --project ./src/MyApp.AppHost
```

### `aspire do`（预览版）

执行特定的流水线步骤及其依赖项。

```bash
aspire do <step> [options] [-- <additional arguments>]

# 选项：
#   --project <path>                   AppHost 项目文件路径
#   -o, --output-path <path>           工件的输出路径
#   --log-level <level>                日志级别（trace, debug, information, warning, error, critical）
#   -e, --environment <env>            环境（默认：Production）
#   --include-exception-details        在流水线日志中包含异常详细信息

# 示例：
aspire do build-images --project ./src/MyApp.AppHost
```

### `aspire update`（预览版）

更新 Aspire 项目中的集成，或更新 CLI 本身。

```bash
aspire update [options]

# 选项：
#   --project <path>       AppHost 项目文件路径
#   --self                 更新 Aspire CLI 本身到最新版本
#   --channel <channel>    要更新到的渠道（stable, daily）

# 示例：
aspire update                          # 更新项目集成
aspire update --self                   # 更新 CLI 本身
aspire update --self --channel daily   # 更新 CLI 到每日构建版本
```

### `aspire mcp`

管理 MCP（模型上下文协议）服务器。

```bash
aspire mcp <subcommand>

# 子命令：
#   init    为检测到的代理环境初始化 MCP 服务器配置
#   start   启动 MCP 服务器
```

#### `aspire mcp init`

```bash
aspire mcp init

# 交互式 — 检测您的 AI 环境并创建配置文件。
# 支持的环境：
# - VS Code（GitHub Copilot）
# - Copilot CLI
# - Claude Code
# - OpenCode
```

为检测到的 AI 工具生成相应的配置文件。
详见 [MCP 服务器](mcp-server.md)。

#### `aspire mcp start`

```bash
aspire mcp start

# 使用 STDIO 传输启动 MCP 服务器。
# 这通常是通过您的 AI 工具调用，而不是手动运行。
```

---

## 不存在的命令

以下命令在 Aspire CLI 13.1 中 **无效**。请使用替代方案：

| 无效命令 | 替代方案                                                          |
| --------------- | -------------------------------------------------------------------- |
| `aspire build`  | 使用 `dotnet build ./AppHost`                                         |
| `aspire test`   | 使用 `dotnet test ./Tests`                                            |
| `aspire dev`    | 使用 `aspire run`（包含文件监视）                            |
| `aspire list`   | 使用 `aspire new --help` 查看模板，使用 `aspire add` 查看集成 |

---

## .NET CLI 等效命令

.NET CLI 可以执行一些 Aspire 任务：

| Aspire CLI                  | .NET CLI 等效命令              |
| --------------------------- | -------------------------------- |
| `aspire new aspire-starter` | `dotnet new aspire-starter`      |
| `aspire run`                | `dotnet run --project ./AppHost` |
| N/A                         | `dotnet build ./AppHost`         |
| N/A                         | `dotnet test ./Tests`            |

Aspire CLI 通过 `publish`、`deploy`、`add`、`mcp`、`config`、`cache`、`do` 和 `update` 命令提供额外价值，这些命令在 .NET CLI 中没有直接等效项。

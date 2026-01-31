---
name: copilot-sdk
description: 使用 GitHub Copilot SDK 构建代理型应用。适用于在应用中嵌入 AI 代理、创建自定义工具、实现流式响应、管理会话、连接到 MCP 服务器或创建自定义代理。触发事件包括 Copilot SDK、GitHub SDK、代理型应用、嵌入 Copilot、可编程代理、MCP 服务器、自定义代理。
---

# GitHub Copilot SDK

使用 Python、TypeScript、Go 或 .NET 在任何应用中嵌入 Copilot 的代理型工作流。

## 概述

GitHub Copilot SDK 暴露了 Copilot CLI 后端的相同引擎：一个经过生产测试的代理运行时，您可以编程调用。无需自行构建编排逻辑 - 您定义代理行为，Copilot 会处理规划、工具调用、文件编辑等。

## 先决条件

1. **已安装并认证的 GitHub Copilot CLI** ([安装指南](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli))
2. **语言运行时环境**：Node.js 18+、Python 3.8+、Go 1.21+ 或 .NET 8.0+

验证 CLI：`copilot --version`

## 安装

### Node.js/TypeScript
```bash
mkdir copilot-demo && cd copilot-demo
npm init -y --init-type module
npm install @github/copilot-sdk tsx
```

### Python
```bash
pip install github-copilot-sdk
```

### Go
```bash
mkdir copilot-demo && cd copilot-demo
go mod init copilot-demo
go get github.com/github/copilot-sdk/go
```

### .NET
```bash
dotnet new console -n CopilotDemo && cd CopilotDemo
dotnet add package GitHub.Copilot.SDK
```

## 快速入门

### TypeScript
```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({ model: "gpt-4.1" });

const response = await session.sendAndWait({ prompt: "What is 2 + 2?" });
console.log(response?.data.content);

await client.stop();
process.exit(0);
```

运行：`npx tsx index.ts`

### Python
```python
import asyncio
from copilot import CopilotClient

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({"model": "gpt-4.1"})
    response = await session.send_and_wait({"prompt": "What is 2 + 2?"})

    print(response.data.content)
    await client.stop()

asyncio.run(main())
```

### Go
```go
package main

import (
    "fmt"
    "log"
    "os"
    copilot "github.com/github/copilot-sdk/go"
)

func main() {
    client := copilot.NewClient(nil)
    if err := client.Start(); err != nil {
        log.Fatal(err)
    }
    defer client.Stop()

    session, err := client.CreateSession(&copilot.SessionConfig{Model: "gpt-4.1"})
    if err != nil {
        log.Fatal(err)
    }

    response, err := session.SendAndWait(copilot.MessageOptions{Prompt: "What is 2 + 2?"}, 0)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println(*response.Data.Content)
    os.Exit(0)
}
```

### .NET (C#)
```csharp
using GitHub.Copilot.SDK;

await using var client = new CopilotClient();
await using var session = await client.CreateSessionAsync(new SessionConfig { Model = "gpt-4.1" });

var response = await session.SendAndWaitAsync(new MessageOptions { Prompt = "What is 2 + 2?" });
Console.WriteLine(response?.Data.Content);
```

运行：`dotnet run`

## 流式响应

启用实时输出以提升用户体验：

### TypeScript
```typescript
import { CopilotClient, SessionEvent } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({
    model: "gpt-4.1",
    streaming: true,
});

session.on((event: SessionEvent) => {
    if (event.type === "assistant.message_delta") {
        process.stdout.write(event.data.deltaContent);
    }
    if (event.type === "session.idle") {
        console.log(); // 完成时换行
    }
});

await session.sendAndWait({ prompt: "Tell me a short joke" });

await client.stop();
process.exit(0);
```

### Python
```python
import asyncio
import sys
from copilot import CopilotClient
from copilot.generated.session_events import SessionEventType

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "model": "gpt-4.1",
        "streaming": True,
    })

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()

    session.on(handle_event)

    await session.send_and_wait({
        "prompt": "Tell me a short joke"
    })

    await client.stop()

asyncio.run(main())
```

### Go
```go
session, err := client.CreateSession(&copilot.SessionConfig{
    Model:     "gpt-4.1",
    Streaming: true,
})

session.On(func(event copilot.SessionEvent) {
    if event.Type == "assistant.message_delta" {
        fmt.Print(*event.Data.DeltaContent)
    }
    if event.Type == "session.idle" {
        fmt.Println()
    }
})

_, err = session.SendAndWait(copilot.MessageOptions{Prompt: "Tell me a short joke"}, 0)
```

### .NET
```csharp
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-4.1",
    Streaming = true,
});

session.On(ev =>
{
    if (ev is AssistantMessageDeltaEvent deltaEvent)
        Console.Write(deltaEvent.Data.DeltaContent);
    if (ev is SessionIdleEvent)
        Console.WriteLine();
});

await session.SendAndWaitAsync(new MessageOptions { Prompt = "Tell me a short joke" });
```

## 自定义工具

定义 Copilot 在推理过程中可调用的工具。当您定义工具时，您告诉 Copilot：
1. **工具的功能**（描述）
2. **所需的参数**（模式）
3. **要运行的代码**（处理函数）

### TypeScript (JSON Schema)
```typescript
import { CopilotClient, defineTool, SessionEvent } from "@github/copilot-sdk";

const getWeather = defineTool("get_weather", {
    description: "获取城市当前的天气信息",
    parameters: {
        type: "object",
        properties: {
            city: { type: "string", description: "城市名称" },
        },
        required: ["city"],
    },
    handler: async ({ city }) => {
        const conditions = ["sunny", "cloudy", "rainy", "partly cloudy"];
        const temp = Math.floor(Math.random() * 30) + 50;
        const condition = conditions[Math.floor(Math.random() * conditions.length)];
        return { city, temperature: `${temp}°F`, condition };
    },
});

const client = new CopilotClient();
const session = await client.createSession({
    model: "gpt-4.1",
    streaming: true,
    tools: [getWeather],
});

session.on((event: SessionEvent) => {
    if (event.type === "assistant.message_delta") {
        process.stdout.write(event.data.deltaContent);
    }
});

await session.sendAndWait({
    prompt: "What's the weather like in Seattle and Tokyo?",
});

await client.stop();
process.exit(0);
```

### Python (Pydantic)
```python
import asyncio
import random
import sys
from copilot import CopilotClient
from copilot.tools import define_tool
from copilot.generated.session_events import SessionEventType
from pydantic import BaseModel, Field

class GetWeatherParams(BaseModel):
    city: str = Field(description="获取天气的城市名称")

@define_tool(description="获取城市当前的天气信息")
async def get_weather(params: GetWeatherParams) -> dict:
    city = params.city
    conditions = ["sunny", "cloudy", "rainy", "partly cloudy"]
    temp = random.randint(50, 80)
    condition = random.choice(conditions)
    return {"city": city, "temperature": f"{temp}°F", "condition": condition}

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "model": "gpt-4.1",
        "streaming": True,
        "tools": [get_weather],
    })

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()

    session.on(handle_event)

    print("Weather Assistant (输入 'exit' 退出)")
    print("尝试：'What's the weather in Paris?'\n")

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break

        if user_input.lower() == "exit":
            break

        sys.stdout.write("Assistant: ")
        await session.send_and_wait({"prompt": user_input})
        print("\n")

    await client.stop()

asyncio.run(main())
```

## MCP 服务器集成

连接到 MCP（模型上下文协议）服务器以使用预构建工具。连接到 GitHub 的 MCP 服务器以获得仓库、问题和 PR 的访问权限：

### TypeScript
```typescript
const session = await client.createSession({
    model: "gpt-4.1",
    mcpServers: {
        github: {
            type: "http",
            url: "https://api.githubcopilot.com/mcp/",
        },
    },
});
```

### Python
```python
session = await client.create_session({
    "model": "gpt-4.1",
    "mcp_servers": {
        "github": {
            "type": "http",
            "url": "https://api.githubcopilot.com/mcp/",
        },
    },
})
```

### Go
```go
session, _ := client.CreateSession(&copilot.SessionConfig{
    Model: "gpt-4.1",
    MCPServers: map[string]copilot.MCPServerConfig{
        "github": {
            Type: "http",
            URL:  "https://api.githubcopilot.com/mcp/",
        },
    },
})
```

### .NET
```csharp
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-4.1",
    McpServers = new Dictionary<string, McpServerConfig>
    {
        ["github"] = new McpServerConfig
        {
            Type = "http",
            Url = "https://api.githubcopilot.com/mcp/",
        },
    },
});
```

## 自定义代理

为特定任务定义专门的 AI 人格：

### TypeScript
```typescript
const session = await client.createSession({
    model: "gpt-4.1",
    customAgents: [{
        name: "pr-reviewer",
        displayName: "PR 审查员",
        description: "审查拉取请求的最佳实践",
        prompt: "你是一位专业的代码审查员。专注于安全、性能和可维护性。",
    }],
});
```

### Python
```python
session = await client.create_session({
    "model": "gpt-4.1",
    "custom_agents": [{
        "name": "pr-reviewer",
        "display_name": "PR 审查员",
        "description": "审查拉取请求的最佳实践",
        "prompt": "你是一位专业的代码审查员。专注于安全、性能和可维护性。",
    }],
})
```

## 系统消息

自定义 AI 的行为和个性：

### TypeScript
```typescript
const session = await client.createSession({
    model: "gpt-4.1",
    systemMessage: {
        content: "你是我们工程团队的有帮助的助手。始终保持简洁。",
    },
});
```

### Python
```python
session = await client.create_session({
    "model": "gpt-4.1",
    "system_message": {
        "content": "你是我们工程团队的有帮助的助手。始终保持简洁。",
    },
})
```

## 外部 CLI 服务器

单独运行 CLI 服务器模式，并将 SDK 连接到它。这在调试、资源共享或自定义环境中非常有用。

### 启动 CLI 服务器模式
```bash
copilot --server --port 4321
```

### 连接 SDK 到外部服务器

#### TypeScript
```typescript
const client = new CopilotClient({
    cliUrl: "localhost:4321"
});

const session = await client.createSession({ model: "gpt-4.1" });
```

#### Python
```python
client = CopilotClient({
    "cli_url": "localhost:4321"
})
await client.start()

session = await client.create_session({"model": "gpt-4.1"})
```

#### Go
```go
client := copilot.NewClient(&copilot.ClientOptions{
    CLIUrl: "localhost:4321",
})

if err := client.Start(); err != nil {
    log.Fatal(err)
}

session, _ := client.CreateSession(&copilot.SessionConfig{Model: "gpt-4.1"})
```

#### .NET
```csharp
using var client = new CopilotClient(new CopilotClientOptions
{
    CliUrl = "localhost:4321"
});

await using var session = await client.CreateSessionAsync(new SessionConfig { Model = "gpt-4.1" });
```

**注意**：当提供 `cliUrl` 时，SDK 不会启动或管理 CLI 进程，它只会连接到现有的服务器。

## 事件类型

| 事件 | 描述 |
|------|------|
| `user.message` | 用户输入添加 |
| `assistant.message` | 完整模型响应 |
| `assistant.message_delta` | 流式响应块 |
| `assistant.reasoning` | 模型推理（模型依赖） |
| `assistant.reasoning_delta` | 流式推理块 |
| `tool.execution_start` | 工具调用开始 |
| `tool.execution_complete` | 工具执行完成 |
| `session.idle` | 没有活跃处理 |
| `session.error` | 发生错误 |

## 客户端配置

| 选项 | 描述 | 默认值 |
|------|------|--------|
| `cliPath` | Copilot CLI 可执行文件路径 | 系统 PATH |
| `cliUrl` | 连接到现有服务器（例如："localhost:4321"） | 无 |
| `port` | 服务器通信端口 | 随机 |
| `useStdio` | 使用 stdio 传输而非 TCP | true |
| `logLevel` | 日志详细程度 | "info" |
| `autoStart` | 自动启动服务器 | true |
| `autoRestart` | 在崩溃时重启 | true |
| `cwd` | CLI 进程的工作目录 | 继承 |

## 会话配置

| 选项 | 描述 |
|------|------|
| `model` | 使用的 LLM（"gpt-4.1"、"claude-sonnet-4.5" 等） |
| `sessionId` | 自定义会话标识符 |
| `tools` | 自定义工具定义 |
| `mcpServers` | MCP 服务器连接 |
| `customAgents` | 自定义代理人格 |
| `systemMessage` | 覆盖默认系统提示 |
| `streaming` | 启用增量响应块 |
| `availableTools` | 允许工具的白名单 |
| `excludedTools` | 禁用工具的黑名单 |

## 会话持久化

在重启后保存并恢复对话：

### 使用自定义 ID 创建
```typescript
const session = await client.createSession({
    sessionId: "user-123-conversation",
    model: "gpt-4.1"
});
```

### 恢复会话
```typescript
const session = await client.resumeSession("user-123-conversation");
await session.send({ prompt: "What did we discuss earlier?" });
```

### 列出和删除会话
```typescript
const sessions = await client.listSessions();
await client.deleteSession("old-session-id");
```

## 错误处理

```typescript
try {
    const client = new CopilotClient();
    const session = await client.createSession({ model: "gpt-4.1" });
    const response = await session.sendAndWait(
        { prompt: "Hello!" },
        30000 // 毫秒级超时
    );
} catch (error) {
    if (error.code === "ENOENT") {
        console.error("未安装 Copilot CLI");
    } else if (error.code === "ECONNREFUSED") {
        console.error("无法连接到 Copilot 服务器");
    } else {
        console.error("错误:", error.message);
    }
} finally {
    await client.stop();
}
```

## 平滑关闭

```typescript
process.on("SIGINT", async () => {
    console.log("正在关闭...");
    await client.stop();
    process.exit(0);
});
```

## 常见模式

### 多轮对话
```typescript
const session = await client.createSession({ model: "gpt-4.1" });

await session.sendAndWait({ prompt: "My name is Alice" });
await session.sendAndWait({ prompt: "What's my name?" });
// 响应："Your name is Alice"
```

### 文件附件
```typescript
await session.send({
    prompt: "分析此文件",
    attachments: [{
        type: "file",
        path: "./data.csv",
        displayName: "销售数据"
    }]
});
```

### 中止长时间操作
```typescript
const timeoutId = setTimeout(() => {
    session.abort();
}, 60000);

session.on((event) => {
    if (event.type === "session.idle") {
        clearTimeout(timeoutId);
    }
});
```

## 可用模型

在运行时查询可用模型：

```typescript
const models = await client.getModels();
// 返回: ["gpt-4.1", "gpt-4o", "claude-sonnet-4.5", ...]
```

## 最佳实践

1. **始终清理**：使用 `try-finally` 或 `defer` 确保调用 `client.stop()`
2. **设置超时**：使用 `sendAndWait` 的超时功能处理长时间操作
3. **处理事件**：订阅错误事件以实现健壮的错误处理
4. **使用流式传输**：启用流式传输以提升长时间响应的用户体验
5. **持久化会话**：使用自定义会话 ID 实现多轮对话
6. **定义清晰的工具**：编写描述性的工具名称和描述

## 架构

```
您的应用
       |
  SDK 客户端
       | JSON-RPC
  Copilot CLI（服务器模式）
       |
  GitHub（模型、认证）
```

SDK 会自动管理 CLI 进程的生命周期。所有通信均通过 stdio 或 TCP 的 JSON-RPC 进行。

## 资源

- **GitHub 仓库**：https://github.com/github/copilot-sdk
- **入门教程**：https://github.com/github/copilot-sdk/blob/main/docs/tutorials/first-app.md
- **GitHub MCP 服务器**：https://github.com/github/github-mcp-server
- **MCP 服务器目录**：https://github.com/modelcontextprotocol/servers
- **食谱**：https://github.com/github/copilot-sdk/tree/main/cookbook
- **示例**：https://github.com/github/copilot-sdk/tree/main/samples

## 状态

此 SDK 处于 **技术预览** 阶段，可能会有破坏性变更。目前不推荐用于生产环境。

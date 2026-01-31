---
applyTo: '**.cs, **.csproj'
description: '此文件提供了使用 GitHub Copilot SDK 构建 C# 应用程序的指导。'
name: 'GitHub Copilot SDK C# 指南'
---

## 核心原则

- SDK 处于技术预览版，可能会有重大变更
- 需要 .NET 10.0 或更高版本
- 需要已安装 GitHub Copilot CLI 并位于 PATH 中
- 全程使用 async/await 模式
- 实现 IAsyncDisposable 用于资源清理

## 安装

始终通过 NuGet 安装：
```bash
dotnet add package GitHub.Copilot.SDK
```

## 客户端初始化

### 基础客户端设置

```csharp
await using var client = new CopilotClient();
await client.StartAsync();
```

### 客户端配置选项

在创建 CopilotClient 时使用 `CopilotClientOptions`：

- `CliPath` - CLI 可执行文件路径（默认：从 PATH 中获取 "copilot"）
- `CliArgs` - 在 SDK 管理的标志前添加的额外参数
- `CliUrl` - 现有 CLI 服务器的 URL（例如："localhost:8080"）。提供此参数时，客户端不会启动新进程
- `Port` - 服务器端口（默认：0 表示随机）
- `UseStdio` - 使用 stdio 传输而非 TCP（默认：true）
- `LogLevel` - 日志级别（默认："info"）
- `AutoStart` - 自动启动服务器（默认：true）
- `AutoRestart` - 在崩溃时自动重启（默认：true）
- `Cwd` - CLI 进程的工作目录
- `Environment` - CLI 进程的环境变量
- `Logger` - 用于 SDK 日志记录的 ILogger 实例

### 手动服务器控制

对于显式控制：
```csharp
var client = new CopilotClient(new CopilotClientOptions { AutoStart = false });
await client.StartAsync();
// 使用 client...
await client.StopAsync();
```

当 `StopAsync()` 响应过慢时，使用 `ForceStopAsync()`。

## 会话管理

### 创建会话

使用 `SessionConfig` 进行配置：

```csharp
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5",
    Streaming = true,
    Tools = [...],
    SystemMessage = new SystemMessageConfig { ... },
    AvailableTools = ["tool1", "tool2"],
    ExcludedTools = ["tool3"],
    Provider = new ProviderConfig { ... }
});
```

### 会话配置选项

- `SessionId` - 自定义会话 ID
- `Model` - 模型名称（"gpt-5"、"claude-sonnet-4.5" 等）
- `Tools` - 暴露给 CLI 的自定义工具
- `SystemMessage` - 系统消息自定义
- `AvailableTools` - 允许使用的工具名称白名单
- `ExcludedTools` - 禁用的工具名称黑名单
- `Provider` - 自定义 API 提供商配置（BYOK）
- `Streaming` - 启用流式响应分块（默认：false）

### 恢复会话

```csharp
var session = await client.ResumeSessionAsync(sessionId, new ResumeSessionConfig { ... });
```

### 会话操作

- `session.SessionId` - 获取会话标识符
- `session.SendAsync(new MessageOptions { Prompt = "...", Attachments = [...] })` - 发送消息
- `session.AbortAsync()` - 中止当前处理
- `session.GetMessagesAsync()` - 获取所有事件/消息
- `await session.DisposeAsync()` - 清理资源

## 事件处理

### 事件订阅模式

始终使用 TaskCompletionSource 等待会话事件：

```csharp
var done = new TaskCompletionSource();

session.On(evt =>
{
    if (evt is AssistantMessageEvent msg)
    {
        Console.WriteLine(msg.Data.Content);
    }
    else if (evt is SessionIdleEvent)
    {
        done.SetResult();
    }
});

await session.SendAsync(new MessageOptions { Prompt = "..." });
await done.Task;
```

### 取消事件订阅

`On()` 方法返回一个 IDisposable：

```csharp
var subscription = session.On(evt => { /* 处理逻辑 */ });
// 后续...
subscription.Dispose();
```

### 事件类型

使用模式匹配或 switch 表达式处理事件：

```csharp
session.On(evt =>
{
    switch (evt)
    {
        case UserMessageEvent userMsg:
            // 处理用户消息
            break;
        case AssistantMessageEvent assistantMsg:
            Console.WriteLine(assistantMsg.Data.Content);
            break;
        case ToolExecutionStartEvent toolStart:
            // 工具执行开始
            break;
        case ToolExecutionCompleteEvent toolComplete:
            // 工具执行完成
            break;
        case SessionStartEvent start:
            // 会话开始
            break;
        case SessionIdleEvent idle:
            // 会话空闲（处理完成）
            break;
        case SessionErrorEvent error:
            Console.WriteLine($"错误: {error.Data.Message}");
            break;
    }
});
```

## 流式响应

### 启用流式传输

在 SessionConfig 中设置 `Streaming = true`：

```csharp
var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5",
    Streaming = true
});
```

### 处理流式事件

处理增量事件（分块）和最终事件：

```csharp
var done = new TaskCompletionSource();

session.On(evt =>
{
    switch (evt)
    {
        case AssistantMessageDeltaEvent delta:
            // 增量文本分块
            Console.Write(delta.Data.DeltaContent);
            break;
        case AssistantReasoningDeltaEvent reasoningDelta:
            // 增量推理分块（模型相关）
            Console.Write(reasoningDelta.Data.DeltaContent);
            break;
        case AssistantMessageEvent msg:
            // 最终完整消息
            Console.WriteLine("\n--- 最终 ---");
            Console.WriteLine(msg.Data.Content);
            break;
        case AssistantReasoningEvent reasoning:
            // 最终推理内容
            Console.WriteLine("--- 推理 ---");
            Console.WriteLine(reasoning.Data.Content);
            break;
        case SessionIdleEvent:
            done.SetResult();
            break;
    }
});

await session.SendAsync(new MessageOptions { Prompt = "给我讲个故事" });
await done.Task;
```

注意：最终事件（`AssistantMessageEvent`、`AssistantReasoningEvent`）无论流式传输设置如何始终发送。

## 自定义工具

### 使用 AIFunctionFactory 定义工具

使用 `Microsoft.Extensions.AI.AIFunctionFactory.Create` 定义类型安全工具：

```csharp
using Microsoft.Extensions.AI;
using System.ComponentModel;

var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5",
    Tools = [
        AIFunctionFactory.Create(
            async ([Description("问题ID")] string id) => {
                var issue = await FetchIssueAsync(id);
                return issue;
            },
            "lookup_issue",
            "从跟踪器获取问题详情"),
    ]
});
```

### 工具返回类型

- 返回任何可序列化为 JSON 的值（自动包装）
- 或返回 `ToolResultAIContent` 包装 `ToolResultObject` 以完全控制元数据

### 工具执行流程

当 Copilot 调用工具时，客户端会自动：
1. 运行您的处理函数
2. 序列化返回值
3. 向 CLI 响应

## 系统消息自定义

### 追加模式（默认 - 保留安全限制）

```csharp
var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5",
    SystemMessage = new SystemMessageConfig
    {
        Mode = SystemMessageMode.Append,
        Content = @"
<workflow_rules>
- 始终检查安全漏洞
- 在适用时建议性能优化
</workflow_rules>
"
    }
});
```

### 替换模式（完全控制 - 移除安全限制）

```csharp
var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5",
    SystemMessage = new SystemMessageConfig
    {
        Mode = SystemMessageMode.Replace,
        Content = "你是一个有帮助的助手。"
    }
});
```

## 文件附件

使用 `UserMessageDataAttachmentsItem` 将文件附加到消息：

```csharp
await session.SendAsync(new MessageOptions
{
    Prompt = "分析此文件",
    Attachments = new List<UserMessageDataAttachmentsItem>
    {
        new UserMessageDataAttachmentsItem
        {
            Type = UserMessageDataAttachmentsItemType.File,
            Path = "/path/to/file.cs",
            DisplayName = "我的文件"
        }
    }
});
```

## 消息传递模式

使用 `MessageOptions` 中的 `Mode` 属性：

- `"enqueue"` - 将消息排队等待处理
- `"immediate"` - 立即处理消息

```csharp
await session.SendAsync(new MessageOptions
{
    Prompt = "...",
    Mode = "enqueue"
});
```

## 多个会话

会话是独立的，可以并发运行：

```csharp
var session1 = await client.CreateSessionAsync(new SessionConfig { Model = "gpt-5" });
var session2 = await client.CreateSessionAsync(new SessionConfig { Model = "claude-sonnet-4.5" });

await session1.SendAsync(new MessageOptions { Prompt = "来自会话1的问候" });
await session2.SendAsync(new MessageOptions { Prompt = "来自会话2的问候" });
```

## 自带密钥（BYOK）

使用 `ProviderConfig` 配置自定义 API 提供商：

```csharp
var session = await client.CreateSessionAsync(new SessionConfig
{
    Provider = new ProviderConfig
    {
        Type = "openai",
        BaseUrl = "https://api.openai.com/v1",
        ApiKey = "your-api-key"
    }
});
```

## 会话生命周期管理

### 列出会话

```csharp
var sessions = await client.ListSessionsAsync();
foreach (var metadata in sessions)
{
    Console.WriteLine($"会话: {metadata.SessionId}");
}
```

### 删除会话

```csharp
await client.DeleteSessionAsync(sessionId);
```

### 检查连接状态

```csharp
var state = client.State;
```

## 错误处理

### 标准异常处理

```csharp
try
{
    var session = await client.CreateSessionAsync();
    await session.SendAsync(new MessageOptions { Prompt = "你好" });
}
catch (StreamJsonRpc.RemoteInvocationException ex)
{
    Console.Error.WriteLine($"JSON-RPC 错误: {ex.Message}");
}
catch (Exception ex)
{
    Console.Error.WriteLine($"错误: {ex.Message}");
}
```

### 会话错误事件

监控 `SessionErrorEvent` 以检测运行时错误：

```csharp
session.On(evt =>
{
    if (evt is SessionErrorEvent error)
    {
        Console.Error.WriteLine($"会话错误: {error.Data.Message}");
    }
});
```

## 连接性测试

使用 PingAsync 验证服务器连接性：

```csharp
var response = await client.PingAsync("测试消息");
```

## 资源清理

### 使用 await using 自动清理

始终使用 `await using` 实现自动释放：

```csharp
await using var client = new CopilotClient();
await using var session = await client.CreateSessionAsync();
// 资源自动清理
```

### 手动清理

如果不使用 `await using`：

```csharp
var client = new CopilotClient();
try
{
    await client.StartAsync();
    // 使用 client...
}
finally
{
    await client.StopAsync();
}
```

## 最佳实践

1. **始终使用 `await using`** 对 CopilotClient 和 CopilotSession
2. **使用 TaskCompletionSource** 等待 SessionIdleEvent
3. **处理 SessionErrorEvent** 以实现健壮的错误处理
4. **使用模式匹配**（switch 表达式）处理事件
5. **启用流式传输** 以提升交互场景的用户体验
6. **使用 AIFunctionFactory** 定义类型安全的工具
7. **在不再需要时释放事件订阅**
8. **使用 SystemMessageMode.Append** 以保留安全限制
9. **提供描述性的工具名称和描述** 以帮助模型理解
10. **在启用流式传输时处理增量和最终事件**

## 常见模式

### 简单查询-响应

```csharp
await using var client = new CopilotClient();
await client.StartAsync();

await using var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5"
});

var done = new TaskCompletionSource();

session.On(evt =>
{
    if (evt is AssistantMessageEvent msg)
    {
        Console.WriteLine(msg.Data.Content);
    }
    else if (evt is SessionIdleEvent)
    {
        done.SetResult();
    }
});

await session.SendAsync(new MessageOptions { Prompt = "2+2 等于多少？" });
await done.Task;
```

### 多轮对话

```csharp
await using var session = await client.CreateSessionAsync();

async Task SendAndWait(string prompt)
{
    var done = new TaskCompletionSource();
    var subscription = session.On(evt =>
    {
        if (evt is AssistantMessageEvent msg)
        {
            Console.WriteLine(msg.Data.Content);
        }
        else if (evt is SessionIdleEvent)
        {
            done.SetResult();
        }
    });

    await session.SendAsync(new MessageOptions { Prompt = prompt });
    await done.Task;
    subscription.Dispose();
}

await SendAndWait("法国的首都是什么？");
await SendAndWait("它的总人口是多少？");
```

### 具有复杂返回类型的工具

```csharp
var session = await client.CreateSessionAsync(new SessionConfig
{
    Tools = [
        AIFunctionFactory.Create(
            ([Description("用户ID")] string userId) => {
                return new {
                    Id = userId,
                    Name = "John Doe",
                    Email = "john@example.com",
                    Role = "开发者"
                };
            },
            "get_user",
            "检索用户信息")
    ]
});
```

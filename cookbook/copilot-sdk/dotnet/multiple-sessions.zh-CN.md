# 处理多个会话

同时管理多个独立的对话。

> **可运行示例：** [recipe/multiple-sessions.cs](recipe/multiple-sessions.cs)
>
> ```bash
> dotnet run recipe/multiple-sessions.cs
> ```

## 示例场景

您需要并行运行多个对话，每个对话都有自己的上下文和历史记录。

## C#

```csharp
using GitHub.Copilot.SDK;

await using var client = new CopilotClient();
await client.StartAsync();

// 创建多个独立的会话
var session1 = await client.CreateSessionAsync(new SessionConfig { Model = "gpt-5" });
var session2 = await client.CreateSessionAsync(new SessionConfig { Model = "gpt-5" });
var session3 = await client.CreateSessionAsync(new SessionConfig { Model = "claude-sonnet-4.5" });

// 每个会话维护自己的对话历史
await session1.SendAsync(new MessageOptions { Prompt = "您正在帮助处理一个Python项目" });
await session2.SendAsync(new MessageOptions { Prompt = "您正在帮助处理一个TypeScript项目" });
await session3.SendAsync(new MessageOptions { Prompt = "您正在帮助处理一个Go项目" });

// 后续消息保持在各自的上下文中
await session1.SendAsync(new MessageOptions { Prompt = "如何创建虚拟环境？" });
await session2.SendAsync(new MessageOptions { Prompt = "如何设置tsconfig？" });
await session3.SendAsync(new MessageOptions { Prompt = "如何初始化一个模块？" });

// 清理所有会话
await session1.DisposeAsync();
await session2.DisposeAsync();
await session3.DisposeAsync();
```

## 自定义会话ID

使用自定义ID以便更方便地追踪：

```csharp
var session = await client.CreateSessionAsync(new SessionConfig
{
    SessionId = "user-123-chat",
    Model = "gpt-5"
});

Console.WriteLine(session.SessionId); // "user-123-chat"
```

## 列出会话

```csharp
var sessions = await client.ListSessionsAsync();
foreach (var sessionInfo in sessions)
{
    Console.WriteLine($"会话: {sessionInfo.SessionId}");
}
```

## 删除会话

```csharp
// 删除特定会话
await client.DeleteSessionAsync("user-123-chat");
```

## 使用场景

- **多用户应用**：每个用户一个会话
- **多任务工作流**：为不同的任务创建独立会话
- **A/B测试**：比较不同模型的响应结果

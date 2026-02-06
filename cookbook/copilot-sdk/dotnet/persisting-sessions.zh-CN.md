# 会话持久化与恢复

在应用程序重启时保存和恢复会话对话。

## 示例场景

您希望用户在关闭并重新打开您的应用程序后仍能继续对话。

> **可运行示例:** [recipe/persisting-sessions.cs](recipe/persisting-sessions.cs)
>
> ```bash
> cd recipe
> dotnet run persisting-sessions.cs
> ```

### 使用自定义ID创建会话

```csharp
using GitHub.Copilot.SDK;

await using var client = new CopilotClient();
await client.StartAsync();

// 使用可记忆的ID创建会话
var session = await client.CreateSessionAsync(new SessionConfig
{
    SessionId = "user-123-conversation",
    Model = "gpt-5"
});

await session.SendAsync(new MessageOptions { Prompt = "让我们讨论TypeScript泛型" });

// 会话ID被保留
Console.WriteLine(session.SessionId); // "user-123-conversation"

// 销毁会话但保留磁盘数据
await session.DisposeAsync();
await client.StopAsync();
```

### 恢复会话

```csharp
await using var client = new CopilotClient();
await client.StartAsync();

// 恢复之前的会话
var session = await client.ResumeSessionAsync("user-123-conversation");

// 恢复之前的上下文
await session.SendAsync(new MessageOptions { Prompt = "我们之前在讨论什么？" });

await session.DisposeAsync();
await client.StopAsync();
```

### 列出所有可用会话

```csharp
var sessions = await client.ListSessionsAsync();
foreach (var s in sessions)
{
    Console.WriteLine($"会话: {s.SessionId}");
}
```

### 永久删除会话

```csharp
// 从磁盘中移除会话及其所有数据
await client.DeleteSessionAsync("user-123-conversation");
```

### 获取会话历史记录

检索会话中的所有消息：

```csharp
var messages = await session.GetMessagesAsync();
foreach (var msg in messages)
{
    Console.WriteLine($"[{msg.Type}] {msg.Data.Content}");
}
```

## 最佳实践

1. **使用有意义的会话ID**：在会话ID中包含用户ID或上下文信息
2. **处理缺失的会话**：在恢复会话前检查会话是否存在
3. **清理旧会话**：定期删除不再需要的会话

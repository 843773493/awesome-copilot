# 会话持久化与恢复

在应用程序重启时保存和恢复会话。

## 示例场景

您希望用户在关闭并重新打开您的应用程序后仍能继续对话。

> **可运行示例:** [recipe/persisting-sessions.go](recipe/persisting-sessions.go)
>
> ```bash
> cd recipe
> go run persisting-sessions.go
> ```

### 使用自定义ID创建会话

```go
package main

import (
    "context"
    "fmt"
    copilot "github.com/github/copilot-sdk/go"
)

func main() {
    ctx := context.Background()
    client := copilot.NewClient(nil)
    client.Start(ctx)
    defer client.Stop()

    // 使用一个有意义的ID创建会话
    session, _ := client.CreateSession(ctx, &copilot.SessionConfig{
        SessionID: "user-123-conversation",
        Model:     "gpt-5",
    })

    session.SendAndWait(ctx, copilot.MessageOptions{Prompt: "让我们讨论TypeScript泛型"})

    // 会话ID保持不变
    fmt.Println(session.SessionID)

    // 销毁会话但保留磁盘上的数据
    session.Destroy()
}
```

### 恢复会话

```go
ctx := context.Background()
client := copilot.NewClient(nil)
client.Start(ctx)
defer client.Stop()

// 恢复之前的会话
session, _ := client.ResumeSession(ctx, "user-123-conversation")

// 恢复之前的上下文
session.SendAndWait(ctx, copilot.MessageOptions{Prompt: "我们之前在讨论什么？"})

session.Destroy()
```

### 列出可用会话

```go
sessions, _ := client.ListSessions(ctx)
for _, s := range sessions {
    fmt.Println("会话:", s.SessionID)
}
```

### 永久删除会话

```go
// 从磁盘中移除会话及其所有数据
client.DeleteSession(ctx, "user-123-conversation")
```

### 获取会话历史

```go
messages, _ := session.GetMessages(ctx)
for _, msg := range messages {
    if msg.Data.Content != nil {
        fmt.Printf("[%s] %s\n", msg.Type, *msg.Data.Content)
    }
}
```

## 最佳实践

1. **使用有意义的会话ID**：在会话ID中包含用户ID或上下文信息  
2. **处理缺失的会话**：在恢复会话前检查会话是否存在  
3. **清理旧会话**：定期删除不再需要的会话

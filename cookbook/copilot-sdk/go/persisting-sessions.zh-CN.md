# 会话持久化与恢复

在应用程序重启时保存和恢复会话。

## 示例场景

您希望用户在关闭并重新打开应用程序后仍能继续对话。

> **可运行示例：** [recipe/persisting-sessions.go](recipe/persisting-sessions.go)
>
> ```bash
> cd recipe
> go run persisting-sessions.go
> ```

### 使用自定义ID创建会话

```go
package main

import (
    "fmt"
    "github.com/github/copilot-sdk/go"
)

func main() {
    client := copilot.NewClient()
    client.Start()
    defer client.Stop()

    // 使用可记忆的ID创建会话
    session, _ := client.CreateSession(copilot.SessionConfig{
        SessionID: "user-123-conversation",
        Model:     "gpt-5",
    })

    session.Send(copilot.MessageOptions{Prompt: "让我们讨论TypeScript泛型"})

    // 会话ID被保留
    fmt.Println(session.SessionID)

    // 销毁会话但保留磁盘数据
    session.Destroy()
}
```

### 恢复会话

```go
client := copilot.NewClient()
client.Start()
defer client.Stop()

// 恢复之前的会话
session, _ := client.ResumeSession("user-123-conversation")

// 恢复之前的上下文
session.Send(copilot.MessageOptions{Prompt: "我们之前在讨论什么？"})

session.Destroy()
```

### 列出可用的会话

```go
sessions, _ := client.ListSessions()
for _, s := range sessions {
    fmt.Println("会话:", s.SessionID)
}
```

### 永久删除会话

```go
// 从磁盘中移除会话及其所有数据
client.DeleteSession("user-123-conversation")
```

### 获取会话历史记录

```go
messages, _ := session.GetMessages()
for _, msg := range messages {
    fmt.Printf("[%s] %v\n", msg.Type, msg.Data)
}
```

## 最佳实践

1. **使用有意义的会话ID**：在会话ID中包含用户ID或上下文信息
2. **处理缺失的会话**：在恢复会话前检查会话是否存在
3. **清理旧会话**：定期删除不再需要的会话

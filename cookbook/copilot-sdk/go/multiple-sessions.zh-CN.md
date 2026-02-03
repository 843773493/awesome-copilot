# 处理多个会话

同时管理多个独立的对话会话。

> **可运行示例：** [recipe/multiple-sessions.go](recipe/multiple-sessions.go)
>
> ```bash
> go run recipe/multiple-sessions.go
> ```

## 示例场景

您需要并行运行多个对话会话，每个会话都有自己的上下文和历史记录。

## Go

```go
package main

import (
    "fmt"
    "log"
    "github.com/github/copilot-sdk/go"
)

func main() {
    client := copilot.NewClient()

    if err := client.Start(); err != nil {
        log.Fatal(err)
    }
    defer client.Stop()

    // 创建多个独立的会话
    session1, err := client.CreateSession(copilot.SessionConfig{Model: "gpt-5"})
    if err != nil {
        log.Fatal(err)
    }
    defer session1.Destroy()

    session2, err := client.CreateSession(copilot.SessionConfig{Model: "gpt-5"})
    if err != nil {
        log.Fatal(err)
    }
    defer session2.Destroy()

    session3, err := client.CreateSession(copilot.SessionConfig{Model: "claude-sonnet-4.5"})
    if err != nil {
        log.Fatal(err)
    }
    defer session3.Destroy()

    // 每个会话维护自己的对话历史记录
    session1.Send(copilot.MessageOptions{Prompt: "You are helping with a Python project"})
    session2.Send(copilot.MessageOptions{Prompt: "You are helping with a TypeScript project"})
    session3.Send(copilot.MessageOptions{Prompt: "You are helping with a Go project"})

    // 后续消息保持在各自的上下文中
    session1.Send(copilot.MessageOptions{Prompt: "How do I create a virtual environment?"})
    session2.Send(copilot.MessageOptions{Prompt: "How do I set up tsconfig?"})
    session3.Send(copilot.MessageOptions{Prompt: "How do I initialize a module?"})
}
```

## 自定义会话ID

使用自定义ID以便更方便地追踪：

```go
session, err := client.CreateSession(copilot.SessionConfig{
    SessionID: "user-123-chat",
    Model:     "gpt-5",
})
if err != nil {
    log.Fatal(err)
}

fmt.Println(session.SessionID) // "user-123-chat"
```

## 列出会话

```go
sessions, err := client.ListSessions()
if err != nil {
    log.Fatal(err)
}

for _, sessionInfo := range sessions {
    fmt.Printf("会话: %s\n", sessionInfo.SessionID)
}
```

## 删除会话

```go
// 删除特定会话
if err := client.DeleteSession("user-123-chat"); err != nil {
    log.Printf("删除会话失败: %v", err)
}
```

## 使用场景

- **多用户应用**：每个用户对应一个会话
- **多任务工作流**：为不同任务创建独立会话
- **A/B测试**：比较不同模型的响应结果

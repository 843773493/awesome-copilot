---
applyTo: "**.go, go.mod"
description: "本文件提供使用 GitHub Copilot SDK 构建 Go 应用程序的指导。"
name: "GitHub Copilot SDK Go 指南"
---

## 核心原则

- SDK 处于技术预览阶段，可能会有破坏性变更
- 需要 Go 1.21 或更高版本
- 需要安装 GitHub Copilot CLI 并将其添加到 PATH
- 使用 goroutines 和 channels 实现并发操作
- 除标准库外无其他外部依赖

## 安装

始终通过 Go 模块进行安装：

```bash
go get github.com/github/copilot-sdk/go
```

## 客户端初始化

### 基础客户端设置

```go
import "github.com/github/copilot-sdk/go"

client := copilot.NewClient(nil)
if err := client.Start(); err != nil {
    log.Fatal(err)
}
defer client.Stop()
```

### 客户端配置选项

在创建 CopilotClient 时使用 `ClientOptions`：

- `CLIPath` - CLI 可执行文件路径（默认值：从 PATH 获取的 "copilot"）
- `CLIUrl` - 现有 CLI 服务器的 URL（例如："localhost:8080"）。提供此参数时，客户端不会启动新进程
- `Port` - 服务器端口（默认值：0 表示随机分配）
- `UseStdio` - 使用 stdio 传输而非 TCP（默认值：true）
- `LogLevel` - 日志级别（默认值："info"）
- `AutoStart` - 自动启动服务器（默认值：true，使用指针：`boolPtr(true)`）
- `AutoRestart` - 在崩溃时自动重启（默认值：true，使用指针：`boolPtr(true)`）
- `Cwd` - CLI 进程的工作目录
- `Env` - CLI 进程的环境变量 ([]string)

### 手动服务器控制

对于显式控制：

```go
autoStart := false
client := copilot.NewClient(&copilot.ClientOptions{AutoStart: &autoStart})
if err := client.Start(); err != nil {
    log.Fatal(err)
}
// 使用 client...
client.Stop()
```

当 `Stop()` 响应过慢时，使用 `ForceStop()`。

## 会话管理

### 创建会话

使用 `SessionConfig` 进行配置：

```go
session, err := client.CreateSession(&copilot.SessionConfig{
    Model: "gpt-5",
    Streaming: true,
    Tools: []copilot.Tool{...},
    SystemMessage: &copilot.SystemMessageConfig{ ... },
    AvailableTools: []string{"tool1", "tool2"},
    ExcludedTools: []string{"tool3"},
    Provider: &copilot.ProviderConfig{ ... },
})
if err != nil {
    log.Fatal(err)
}
```

### 会话配置选项

- `SessionID` - 自定义会话 ID
- `Model` - 模型名称（"gpt-5"、"claude-sonnet-4.5" 等）
- `Tools` - 暴露给 CLI 的自定义工具 ([]Tool)
- `SystemMessage` - 系统消息自定义 (\*SystemMessageConfig)
- `AvailableTools` - 允许的工具名称列表 ([]string)
- `ExcludedTools` - 禁用的工具名称列表 ([]string)
- `Provider` - 自定义 API 提供商配置 (BYOK) (\*ProviderConfig)
- `Streaming` - 启用流式响应块 (bool)
- `MCPServers` - MCP 服务器配置
- `CustomAgents` - 自定义代理配置
- `ConfigDir` - 配置目录覆盖
- `SkillDirectories` - 技能目录 ([]string)
- `DisabledSkills` - 禁用的技能 ([]string)

### 恢复会话

```go
session, err := client.ResumeSession("session-id")
// 或使用选项：
session, err := client.ResumeSessionWithOptions("session-id", &copilot.ResumeSessionConfig{ ... })
```

### 会话操作

- `session.SessionID` - 获取会话标识符 (string)
- `session.Send(copilot.MessageOptions{Prompt: "...", Attachments: []copilot.Attachment{...}})` - 发送消息，返回 (messageID string, error)
- `session.SendAndWait(options, timeout)` - 发送并等待空闲，返回 (\*SessionEvent, error)
- `session.Abort()` - 中止当前处理，返回 error
- `session.GetMessages()` - 获取所有事件/消息，返回 ([]SessionEvent, error)
- `session.Destroy()` - 清理会话，返回 error

## 事件处理

### 事件订阅模式

始终使用通道或 done 信号等待会话事件：

```go
done := make(chan struct{})

unsubscribe := session.On(func(evt copilot.SessionEvent) {
    switch evt.Type {
    case copilot.AssistantMessage:
        fmt.Println(*evt.Data.Content)
    case copilot.SessionIdle:
        close(done)
    }
})
defer unsubscribe()

session.Send(copilot.MessageOptions{Prompt: "..."})
<-done
```

### 从事件中取消订阅

`On()` 方法返回一个用于取消订阅的函数：

```go
unsubscribe := session.On(func(evt copilot.SessionEvent) {
    // 处理逻辑
})
// 后续...
unsubscribe()
```

### 事件类型

使用类型开关处理事件：

```go
session.On(func(evt copilot.SessionEvent) {
    switch evt.Type {
    case copilot.UserMessage:
        // 处理用户消息
    case copilot.AssistantMessage:
        if evt.Data.Content != nil {
            fmt.Println(*evt.Data.Content)
        }
    case copilot.ToolExecutionStart:
        // 工具执行开始
    case copilot.ToolExecutionComplete:
        // 工具执行完成
    case copilot.SessionStart:
        // 会话开始
    case copilot.SessionIdle:
        // 会话空闲（处理完成）
    case copilot.SessionError:
        if evt.Data.Message != nil {
            fmt.Println("错误:", *evt.Data.Message)
        }
    }
})
```

## 流式响应

### 启用流式响应

在 SessionConfig 中设置 `Streaming: true`：

```go
session, err := client.CreateSession(&copilot.SessionConfig{
    Model: "gpt-5",
    Streaming: true,
})
```

### 处理流式事件

处理增量事件（delta）和最终事件：

```go
done := make(chan struct{})

session.On(func(evt copilot.SessionEvent) {
    switch evt.Type {
    case copilot.AssistantMessageDelta:
        // 增量文本块
        if evt.Data.DeltaContent != nil {
            fmt.Print(*evt.Data.DeltaContent)
        }
    case copilot.AssistantReasoningDelta:
        // 增量推理块（模型相关）
        if evt.Data.DeltaContent != nil {
            fmt.Print(*evt.Data.DeltaContent)
        }
    case copilot.AssistantMessage:
        // 最终完整消息
        fmt.Println("\n--- 最终 ---")
        if evt.Data.Content != nil {
            fmt.Println(*evt.Data.Content)
        }
    case copilot.AssistantReasoning:
        // 最终推理内容
        fmt.Println("--- 推理 ---")
        if evt.Data.Content != nil {
            fmt.Println(*evt.Data.Content)
        }
    case copilot.SessionIdle:
        close(done)
    }
})

session.Send(copilot.MessageOptions{Prompt: "告诉我一个故事"})
<-done
```

注意：最终事件（`AssistantMessage`、`AssistantReasoning`）始终会发送，无论流式设置如何。

## 自定义工具

### 定义工具

```go
session, err := client.CreateSession(&copilot.SessionConfig{
    Model: "gpt-5",
    Tools: []copilot.Tool{
        {
            Name:        "lookup_issue",
            Description: "从跟踪器获取问题详情",
            Parameters: map[string]interface{}{
                "type": "object",
                "properties": map[string]interface{}{
                    "id": map[string]interface{}{
                        "type":        "string",
                        "description": "问题 ID",
                    },
                },
                "required": []string{"id"},
            },
            Handler: func(inv copilot.ToolInvocation) (copilot.ToolResult, error) {
                args := inv.Arguments.(map[string]interface{})
                issueID := args["id"].(string)

                issue, err := fetchIssue(issueID)
                if err != nil {
                    return copilot.ToolResult{}, err
                }

                return copilot.ToolResult{
                    TextResultForLLM: fmt.Sprintf("问题: %v", issue),
                    ResultType:       "success",
                    ToolTelemetry:    map[string]interface{}{},
                }, nil
            },
        },
    },
})
```

### 工具返回类型

- 返回 `ToolResult` 结构体，包含以下字段：
  - `TextResultForLLM` (string) - LLM 的结果文本
  - `ResultType` (string) - "success" 或 "failure"
  - `Error` (string, 可选) - 内部错误信息（不显示给 LLM）
  - `ToolTelemetry` (map[string]interface{}) - 仪表盘数据

### 工具执行流程

当 Copilot 调用工具时，客户端会自动：

1. 运行您的处理函数
2. 返回 `ToolResult`
3. 回应 CLI

## 系统消息自定义

### 追加模式（默认 - 保留安全守则）

```go
session, err := client.CreateSession(&copilot.SessionConfig{
    Model: "gpt-5",
    SystemMessage: &copilot.SystemMessageConfig{
        Mode: "append",
        Content: `
<工作流规则>
- 始终检查安全漏洞
- 适用时建议性能优化
</工作流规则>
`,
    },
})
```

### 替换模式（完全控制 - 移除安全守则）

```go
session, err := client.CreateSession(&copilot.SessionConfig{
    Model: "gpt-5",
    SystemMessage: &copilot.SystemMessageConfig{
        Mode:    "replace",
        Content: "你是一个有帮助的助手。",
    },
})
```

## 文件附件

使用 `Attachment` 将文件附加到消息中：

```go
messageID, err := session.Send(copilot.MessageOptions{
    Prompt: "分析此文件",
    Attachments: []copilot.Attachment{
        {
            Type:        "文件",
            Path:        "/path/to/file.go",
            DisplayName: "我的文件",
        },
    },
})
```

## 消息传递模式

在 `MessageOptions` 中使用 `Mode` 字段：

- `"enqueue"` - 将消息排队等待处理
- `"immediate"` - 立即处理消息

```go
session.Send(copilot.MessageOptions{
    Prompt: "...",
    Mode:   "enqueue",
})
```

## 多个会话

会话是独立的，可以并发运行：

```go
session1, _ := client.CreateSession(&copilot.SessionConfig{Model: "gpt-5"})
session2, _ := client.CreateSession(&copilot.SessionConfig{Model: "claude-sonnet-4.5"})

session1.Send(copilot.MessageOptions{Prompt: "来自会话 1 的问候"})
session2.Send(copilot.MessageOptions{Prompt: "来自会话 2 的问候"})
```

## 自带 API 密钥 (BYOK)

通过 `ProviderConfig` 使用自定义 API 提供商：

```go
session, err := client.CreateSession(&copilot.SessionConfig{
    Provider: &copilot.ProviderConfig{
        Type:    "openai",
        BaseURL: "https://api.openai.com/v1",
        APIKey:  "your-api-key",
    },
})
```

## 会话生命周期管理

### 检查连接状态

```go
state := client.GetState()
// 返回："断开连接"、"连接中"、"已连接" 或 "错误"
```

## 错误处理

### 标准异常处理

```go
session, err := client.CreateSession(&copilot.SessionConfig{})
if err != nil {
    log.Fatalf("创建会话失败: %v", err)
}

_, err = session.Send(copilot.MessageOptions{Prompt: "Hello"})
if err != nil {
    log.Printf("发送失败: %v", err)
}
```

### 会话错误事件

监控 `SessionError` 类型的运行时错误：

```go
session.On(func(evt copilot.SessionEvent) {
    if evt.Type == copilot.SessionError {
        if evt.Data.Message != nil {
            fmt.Fprintf(os.Stderr, "会话错误: %s\n", *evt.Data.Message)
        }
    }
})
```

## 连接性测试

使用 Ping 验证服务器连接：

```go
resp, err := client.Ping("test message")
if err != nil {
    log.Printf("服务器不可达: %v", err)
} else {
    log.Printf("服务器响应时间戳为 %d", resp.Timestamp)
}
```

## 资源清理

### 使用 Defer 清理

始终使用 `defer` 进行清理：

```go
client := copilot.NewClient(nil)
if err := client.Start(); err != nil {
    log.Fatal(err)
}
defer client.Stop()

session, err := client.CreateSession(nil)
if err != nil {
    log.Fatal(err)
}
defer session.Destroy()
```

### 手动清理

如果不使用 `defer`：

```go
client := copilot.NewClient(nil)
err := client.Start()
if err != nil {
    log.Fatal(err)
}

session, err := client.CreateSession(nil)
if err != nil {
    client.Stop()
    log.Fatal(err)
}

// 使用 session...

session.Destroy()
errors := client.Stop()
for _, err := range errors {
    log.Printf("清理错误: %v", err)
}
```

## 最佳实践

1. **始终使用 `defer`** 进行客户端和会话的清理
2. **使用通道** 等待 SessionIdle 事件
3. **处理 SessionError** 事件以实现健壮的错误处理
4. **使用类型开关** 处理事件
5. **启用流式响应** 以提升交互场景的用户体验
6. **提供描述性的工具名称和描述** 以帮助模型更好地理解
7. **在不再需要时调用取消订阅函数**
8. **使用 SystemMessageConfig 并设置 Mode: "append"** 以保留安全守则
9. **在启用流式响应时处理增量和最终事件**
10. **检查事件数据中的 nil 指针**（如 Content、Message 等均为指针） 

## 常见模式

### 简单查询-响应

```go
client := copilot.NewClient(nil)
if err := client.Start(); err != nil {
    log.Fatal(err)
}
defer client.Stop()

session, err := client.CreateSession(&copilot.SessionConfig{Model: "gpt-5"})
if err != nil {
    log.Fatal(err)
}
defer session.Destroy()

done := make(chan struct{})

session.On(func(evt copilot.SessionEvent) {
    if evt.Type == copilot.AssistantMessage && evt.Data.Content != nil {
        fmt.Println(*evt.Data.Content)
    } else if evt.Type == copilot.SessionIdle {
        close(done)
    }
})

session.Send(copilot.MessageOptions{Prompt: "2+2 等于多少？"})
<-done
```

### 多轮对话

```go
session, _ := client.CreateSession(nil)
defer session.Destroy()

sendAndWait := func(prompt string) error {
    done := make(chan struct{})
    var eventErr error

    unsubscribe := session.On(func(evt copilot.SessionEvent) {
        switch evt.Type {
        case copilot.AssistantMessage:
            if evt.Data.Content != nil {
                fmt.Println(*evt.Data.Content)
            }
        case copilot.SessionIdle:
            close(done)
        case copilot.SessionError:
            if evt.Data.Message != nil {
                eventErr = fmt.Errorf(*evt.Data.Message)
            }
        }
    })
    defer unsubscribe()

    if _, err := session.Send(copilot.MessageOptions{Prompt: prompt}); err != nil {
        return err
    }
    <-done
    return eventErr
}

sendAndWait("法国的首都是哪里？")
sendAndWait("它的居民人口是多少？")
```

### SendAndWait 辅助函数

```go
// 使用内置的 SendAndWait 进行更简单的同步交互
response, err := session.SendAndWait(copilot.MessageOptions{
    Prompt: "2+2 等于多少？",
}, 0) // 0 使用默认的 60 秒超时

if err != nil {
    log.Printf("错误: %v", err)
}
if response != nil && response.Data.Content != nil {
    fmt.Println(*response.Data.Content)
}
```

### 具有结构返回类型的工具

```go
type UserInfo struct {
    ID    string `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
    Role  string `json:"role"`
}

session, _ := client.CreateSession(&copilot.SessionConfig{
    Tools: []copilot.Tool{
        {
            Name:        "get_user",
            Description: "检索用户信息",
            Parameters: map[string]interface{}{
                "type": "object",
                "properties": map[string]interface{}{
                    "user_id": map[string]interface{}{
                        "type":        "string",
                        "description": "用户 ID",
                    },
                },
                "required": []string{"user_id"},
            },
            Handler: func(inv copilot.ToolInvocation) (copilot.ToolResult, error) {
                args := inv.Arguments.(map[string]interface{})
                userID := args["user_id"].(string)

                user := UserInfo{
                    ID:    userID,
                    Name:  "John Doe",
                    Email: "john@example.com",
                    Role:  "开发者",
                }

                jsonBytes, _ := json.Marshal(user)
                return copilot.ToolResult{
                    TextResultForLLM: string(jsonBytes),
                    ResultType:       "success",
                    ToolTelemetry:    map[string]interface{}{},
                }, nil
            },
        },
    },
})
```

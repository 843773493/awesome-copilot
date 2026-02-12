# 错误处理模式

在您的 Copilot SDK 应用程序中优雅地处理错误。

> **可运行示例：** [recipe/error-handling.go](recipe/error-handling.go)
>
> ```bash
> go run recipe/error-handling.go
> ```

## 示例场景

您需要处理各种错误情况，例如连接失败、超时和无效响应。

## 基础错误处理

```go
package main

import (
    "context"
    "fmt"
    "log"
    copilot "github.com/github/copilot-sdk/go"
)

func main() {
    ctx := context.Background()
    client := copilot.NewClient(nil)

    if err := client.Start(ctx); err != nil {
        log.Fatalf("启动客户端失败: %v", err)
    }
    defer client.Stop()

    session, err := client.CreateSession(ctx, &copilot.SessionConfig{
        Model: "gpt-5",
    })
    if err != nil {
        log.Fatalf("创建会话失败: %v", err)
    }
    defer session.Destroy()

    result, err := session.SendAndWait(ctx, copilot.MessageOptions{Prompt: "Hello!"})
    if err != nil {
        log.Printf("发送消息失败: %v", err)
        return
    }

    if result != nil && result.Data.Content != nil {
        fmt.Println(*result.Data.Content)
    }
}
```

## 处理特定错误类型

```go
import (
    "context"
    "errors"
    "fmt"
    "os/exec"
    copilot "github.com/github/copilot-sdk/go"
)

func startClient(ctx context.Context) error {
    client := copilot.NewClient(nil)

    if err := client.Start(ctx); err != nil {
        var execErr *exec.Error
        if errors.As(err, &execErr) {
            return fmt.Errorf("未找到 Copilot CLI。请先安装它: %w", err)
        }
        if errors.Is(err, context.DeadlineExceeded) {
            return fmt.Errorf("无法连接到 Copilot CLI 服务器: %w", err)
        }
        return fmt.Errorf("意外错误: %w", err)
    }

    return nil
}
```

## 超时处理

```go
import (
    "context"
    "errors"
    "fmt"
    "time"
    copilot "github.com/github/copilot-sdk/go"
)

func sendWithTimeout(session *copilot.Session) error {
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    result, err := session.SendAndWait(ctx, copilot.MessageOptions{Prompt: "复杂问题..."})
    if err != nil {
        if errors.Is(err, context.DeadlineExceeded) {
            return fmt.Errorf("请求超时")
        }
        return err
    }

    if result != nil && result.Data.Content != nil {
        fmt.Println(*result.Data.Content)
    }
    return nil
}
```

## 中止请求

```go
func abortAfterDelay(ctx context.Context, session *copilot.Session) {
    // 启动请求（非阻塞发送）
    session.Send(ctx, copilot.MessageOptions{Prompt: "写一个很长的故事..."})

    // 在某些条件后中止请求
    time.AfterFunc(5*time.Second, func() {
        if err := session.Abort(ctx); err != nil {
            log.Printf("中止失败: %v", err)
        }
        fmt.Println("请求已中止")
    })
}
```

## 优雅关闭

```go
import (
    "context"
    "fmt"
    "log"
    "os"
    "os/signal"
    "syscall"
    copilot "github.com/github/copilot-sdk/go"
)

func main() {
    ctx := context.Background()
    client := copilot.NewClient(nil)

    // 设置信号处理
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

    go func() {
        <-sigChan
        fmt.Println("\n正在关闭...")
        client.Stop()
        os.Exit(0)
    }()

    if err := client.Start(ctx); err != nil {
        log.Fatal(err)
    }

    // ... 执行工作 ...
}
```

## 延迟清理模式

```go
func doWork() error {
    ctx := context.Background()
    client := copilot.NewClient(nil)

    if err := client.Start(ctx); err != nil {
        return fmt.Errorf("启动失败: %w", err)
    }
    defer client.Stop()

    session, err := client.CreateSession(ctx, &copilot.SessionConfig{Model: "gpt-5"})
    if err != nil {
        return fmt.Errorf("创建会话失败: %w", err)
    }
    defer session.Destroy()

    // ... 执行工作 ...

    return nil
}
```

## 最佳实践

1. **始终进行清理**：使用 `defer` 确保调用 `Stop()`
2. **处理连接错误**：CLI 可能未安装或未运行
3. **设置适当的超时**：对长时间运行的请求使用 `context.WithTimeout`
4. **记录错误**：捕获错误详情以供调试
5. **包装错误**：使用 `fmt.Errorf` 并配合 `%w` 以保留错误链

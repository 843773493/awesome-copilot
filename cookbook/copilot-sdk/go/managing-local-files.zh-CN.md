# 按元数据分组文件

使用 Copilot 根据文件的元数据智能地对文件夹中的文件进行分组整理。

> **可运行示例：** [recipe/managing-local-files.go](recipe/managing-local-files.go)
>
> ```bash
> go run recipe/managing-local-files.go
> ```

## 示例场景

你有一个包含大量文件的文件夹，想要根据元数据（如文件类型、创建日期、文件大小或其他属性）将它们整理到子文件夹中。Copilot 可以分析这些文件，并建议或执行分组策略。

## 示例代码

```go
package main

import (
    "fmt"
    "log"
    "os"
    "path/filepath"
    "github.com/github/copilot-sdk/go"
)

func main() {
    // 创建并启动客户端
    client := copilot.NewClient()
    if err := client.Start(); err != nil {
        log.Fatal(err)
    }
    defer client.Stop()

    // 创建会话
    session, err := client.CreateSession(copilot.SessionConfig{
        Model: "gpt-5",
    })
    if err != nil {
        log.Fatal(err)
    }
    defer session.Destroy()

    // 事件处理程序
    session.On(func(event copilot.Event) {
        switch e := event.(type) {
        case copilot.AssistantMessageEvent:
            fmt.Printf("\nCopilot: %s\n", e.Data.Content)
        case copilot.ToolExecutionStartEvent:
            fmt.Printf("  → 正在运行: %s\n", e.Data.ToolName)
        case copilot.ToolExecutionCompleteEvent:
            fmt.Printf("  ✓ 完成: %s\n", e.Data.ToolName)
        }
    })

    // 请求 Copilot 整理文件
    homeDir, _ := os.UserHomeDir()
    targetFolder := filepath.Join(homeDir, "Downloads")

    prompt := fmt.Sprintf(`
分析 "%s" 中的文件并将其整理到子文件夹中。

1. 首先列出所有文件及其元数据
2. 预览按文件扩展名分组的结果
3. 创建适当的子文件夹（例如：images、documents、videos）
4. 将每个文件移动到对应的子文件夹

请在移动任何文件前进行确认。
`, targetFolder)

    if err := session.Send(copilot.MessageOptions{Prompt: prompt}); err != nil {
        log.Fatal(err)
    }

    session.WaitForIdle()
}
```

## 分组策略

### 按文件扩展名

```go
// 按以下方式分组文件：
// images/   -> .jpg, .png, .gif
// documents/ -> .pdf, .docx, .txt
// videos/   -> .mp4, .avi, .mov
```

### 按创建日期

```go
// 按以下方式分组文件：
// 2024-01/ -> 2024年1月创建的文件
// 2024-02/ -> 2024年2月创建的文件
```

### 按文件大小

```go
// 按以下方式分组文件：
// tiny-under-1kb/
// small-under-1mb/
// medium-under-100mb/
// large-over-100mb/
```

## 干运行模式

为了安全起见，你可以要求 Copilot 仅预览更改而不实际移动文件：

```go
prompt := fmt.Sprintf(`
分析 "%s" 中的文件并展示你如何按文件类型进行整理。
不要移动任何文件，只需向我展示整理计划。
`, targetFolder)

session.Send(copilot.MessageOptions{Prompt: prompt})
```

## 基于 AI 分析的自定义分组

让 Copilot 根据文件内容确定最佳分组方式：

```go
prompt := fmt.Sprintf(`
查看 "%s" 中的文件并建议一个合理的组织方式。
考虑以下因素：
- 文件名及其可能包含的内容
- 文件类型及其典型用途
- 可能表示项目或事件的日期模式

提出具有描述性和实用性的文件夹名称。
`, targetFolder)

session.Send(copilot.MessageOptions{Prompt: prompt})
```

## 安全注意事项

1. **移动前确认**：在执行文件移动操作前，请要求 Copilot 进行确认
2. **处理重复文件**：考虑若存在同名文件时会如何处理
3. **保留原始文件**：对于重要文件，考虑复制而非移动操作

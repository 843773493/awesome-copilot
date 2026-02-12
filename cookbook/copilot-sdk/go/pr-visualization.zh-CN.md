# 生成PR年龄图表

构建一个交互式命令行工具，利用Copilot内置功能可视化GitHub仓库中拉取请求（PR）的开放时长分布。

> **可运行示例：** [recipe/pr-visualization.go](recipe/pr-visualization.go)
>
> ```bash
> # 从当前git仓库自动检测
> go run recipe/pr-visualization.go
>
> # 显式指定仓库
> go run recipe/pr-visualization.go -repo github/copilot-sdk
> ```

## 示例场景

您想了解某个仓库中PR的开放时长。该工具可检测当前Git仓库或接受仓库输入，然后让Copilot通过GitHub MCP Server获取PR数据并生成图表图像。

## 先决条件

```bash
go get github.com/github/copilot-sdk/go
```

## 使用方法

```bash
# 从当前git仓库自动检测
go run pr-visualization.go

# 显式指定仓库
go run pr-visualization.go -repo github/copilot-sdk
```

## 完整示例：pr-visualization.go

```go
package main

import (
    "bufio"
    "context"
    "flag"
    "fmt"
    "log"
    "os"
    "os/exec"
    "regexp"
    "strings"
    copilot "github.com/github/copilot-sdk/go"
)

// ============================================================================
// Git & GitHub 检测
// ============================================================================

func isGitRepo() bool {
    cmd := exec.Command("git", "rev-parse", "--git-dir")
    return cmd.Run() == nil
}

func getGitHubRemote() string {
    cmd := exec.Command("git", "remote", "get-url", "origin")
    output, err := cmd.Output()
    if err != nil {
        return ""
    }

    remoteURL := strings.TrimSpace(string(output))

    // 处理SSH格式：git@github.com:owner/repo.git
    sshRe := regexp.MustCompile(`git@github\.com:(.+/.+?)(?:\.git)?$`)
    if matches := sshRe.FindStringSubmatch(remoteURL); matches != nil {
        return matches[1]
    }

    // 处理HTTPS格式：https://github.com/owner/repo.git
    httpsRe := regexp.MustCompile(`https://github\.com/(.+/.+?)(?:\.git)?$`)
    if matches := httpsRe.FindStringSubmatch(remoteURL); matches != nil {
        return matches[1]
    }

    return ""
}

func promptForRepo() string {
    reader := bufio.NewReader(os.Stdin)
    fmt.Print("请输入GitHub仓库（格式为owner/repo）：")
    repo, _ := reader.ReadString('\n')
    return strings.TrimSpace(repo)
}

// ============================================================================
// 主程序
// ============================================================================

func main() {
    ctx := context.Background()
    repoFlag := flag.String("repo", "", "GitHub仓库（格式为owner/repo）")
    flag.Parse()

    fmt.Println("🔍 PR年龄图表生成器\n")

    // 确定仓库
    var repo string

    if *repoFlag != "" {
        repo = *repoFlag
        fmt.Printf("📦 使用指定的仓库: %s\n", repo)
    } else if isGitRepo() {
        detected := getGitHubRemote()
        if detected != "" {
            repo = detected
            fmt.Printf("📦 检测到GitHub仓库: %s\n", repo)
        } else {
            fmt.Println("⚠️  检测到git仓库但未找到GitHub远程仓库。")
            repo = promptForRepo()
        }
    } else {
        fmt.Println("📁 不在git仓库中。")
        repo = promptForRepo()
    }

    if repo == "" || !strings.Contains(repo, "/") {
        log.Fatal("❌ 无效的仓库格式。期望格式：owner/repo")
    }

    parts := strings.SplitN(repo, "/", 2)
    owner, repoName := parts[0], parts[1]

    // 创建Copilot客户端
    client := copilot.NewClient(nil)

    if err := client.Start(ctx); err != nil {
        log.Fatal(err)
    }
    defer client.Stop()

    cwd, _ := os.Getwd()
    session, err := client.CreateSession(ctx, &copilot.SessionConfig{
        Model: "gpt-5",
        SystemMessage: &copilot.SystemMessageConfig{
            Content: fmt.Sprintf(`
<context>
您正在分析GitHub仓库：%s/%s
当前工作目录为：%s
</context>

<instructions>
- 使用GitHub MCP Server工具获取PR数据
- 使用您的文件和代码执行工具生成图表
- 将生成的图像保存到当前工作目录
- 保持回答简洁
</instructions>
`, owner, repoName, cwd),
        },
    })
    if err != nil {
        log.Fatal(err)
    }
    defer session.Destroy()

    // 设置事件处理
    session.On(func(event copilot.SessionEvent) {
        switch event.Type {
        case "assistant.message":
            if event.Data.Content != nil {
                fmt.Printf("\n🤖 %s\n\n", *event.Data.Content)
            }
        case "tool.execution_start":
            if event.Data.ToolName != nil {
                fmt.Printf("  ⚙️  %s\n", *event.Data.ToolName)
            }
        }
    })

    // 初始提示 - 让Copilot自行确定细节
    fmt.Println("\n📊 开始分析...\n")

    prompt := fmt.Sprintf(`
      从过去一周中获取%s/%s的开放PR。
      计算每个PR的开放天数。
      然后生成一个条形图，显示PR开放时长的分布情况
      （将它们分组到合理的桶中，如<1天，1-3天等）。
      将图表保存为"pr-age-chart.png"到当前目录。
      最后，总结PR的健康状况 - 平均开放时长、最老的PR以及可能被视为过期的PR数量。
    `, owner, repoName)

    if _, err := session.SendAndWait(ctx, copilot.MessageOptions{Prompt: prompt}); err != nil {
        log.Fatal(err)
    }

    // 交互循环
    fmt.Println("\n💡 可输入后续问题或输入\"exit\"退出。\n")
    fmt.Println("示例：")
    fmt.Println("  - \"扩展到过去一个月\"")
    fmt.Println("  - \"显示最老的5个PR\"")
    fmt.Println("  - \"生成饼图\"")
    fmt.Println("  - \"按作者分组而不是按年龄\"")
    fmt.Println()

    reader := bufio.NewReader(os.Stdin)
    for {
        fmt.Print("You: ")
        input, _ := reader.ReadString('\n')
        input = strings.TrimSpace(input)

        if input == "" {
            continue
        }
        if strings.ToLower(input) == "exit" || strings.ToLower(input) == "quit" {
            fmt.Println("👋 再见!")
            break
        }

        if _, err := session.SendAndWait(ctx, copilot.MessageOptions{Prompt: input}); err != nil {
            log.Printf("错误: %v", err)
        }
    }
}
```

## 工作原理

1. **仓库检测**：检查`--repo`标志 → git远程仓库 → 提示用户输入
2. **无需自定义工具**：完全依赖Copilot CLI内置功能：
   - **GitHub MCP Server** - 从GitHub获取PR数据
   - **文件工具** - 保存生成的图表图像
   - **代码执行** - 使用Python/matplotlib或其他方法生成图表
3. **交互式会话**：初始分析完成后，用户可提出调整请求

## 为何采用此方法？

| 方面          | 自定义工具      | Copilot内置功能                  |
| --------------- | ----------------- | --------------------------------- |
| 代码复杂度     | 高              | **最少**                         |
| 维护           | 您负责维护      | **Copilot负责维护**              |
| 灵活性         | 固定逻辑         | **AI决定最佳方法**               |
| 图表类型       | 由您编写决定     | **Copilot可生成的任何类型**       |
| 数据分组       | 固定桶分类       | **智能分组**                     |

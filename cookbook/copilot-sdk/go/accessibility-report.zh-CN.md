# 生成可访问性报告

构建一个CLI工具，使用Playwright MCP服务器分析网页可访问性，并生成符合WCAG标准的详细报告，可选生成测试用例。

> **可运行示例：** [recipe/accessibility-report.go](recipe/accessibility-report.go)
>
> ```bash
> go run recipe/accessibility-report.go
> ```

## 示例场景

您希望审计网站的可访问性合规性。此工具使用Playwright导航到指定URL，捕获可访问性快照，并生成涵盖地标、标题层级、焦点管理及触控目标等WCAG标准的结构化报告。它还可以生成Playwright测试文件以自动化未来的可访问性检查。

## 前提条件

```bash
go get github.com/github/copilot-sdk/go
```

您还需要安装`npx`（Node.js已安装）以使用Playwright MCP服务器。

## 使用方法

```bash
go run accessibility-report.go
# 当提示时输入URL
```

## 完整示例：accessibility-report.go

```go
package main

import (
	"bufio"
	"context"
	"fmt"
	"log"
	"os"
	"strings"

	copilot "github.com/github/copilot-sdk/go"
)

func main() {
	ctx := context.Background()
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("=== 可访问性报告生成器 ===")
	fmt.Println()

	fmt.Print("请输入要分析的URL：")
	url, _ := reader.ReadString('\n')
	url = strings.TrimSpace(url)

	if url == "" {
		fmt.Println("未提供URL。退出。")
		return
	}

	// 确保URL包含协议
	if !strings.HasPrefix(url, "http://") && !strings.HasPrefix(url, "https://") {
		url = "https://" + url
	}

	fmt.Printf("\n分析中: %s\n", url)
	fmt.Println("请稍候...\n")

	// 创建与Playwright MCP服务器连接的Copilot客户端
	client := copilot.NewClient(nil)

	if err := client.Start(ctx); err != nil {
		log.Fatal(err)
	}
	defer client.Stop()

	streaming := true
	session, err := client.CreateSession(ctx, &copilot.SessionConfig{
		Model:     "claude-opus-4.6",
		Streaming: &streaming,
		McpServers: map[string]interface{}{
			"playwright": map[string]interface{}{
				"type":    "local",
				"command": "npx",
				"args":    []string{"@playwright/mcp@latest"},
				"tools":   []string{"*"},
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	defer session.Destroy()

	// 设置流式事件处理
	done := make(chan struct{}, 1)

	session.On(func(event copilot.SessionEvent) {
		switch event.Type {
		case "assistant.message.delta":
			if event.Data.DeltaContent != nil {
				fmt.Print(*event.Data.DeltaContent)
			}
		case "session.idle":
			select {
			case done <- struct{}{}:
			default:
			}
		case "session.error":
			if event.Data.Message != nil {
				fmt.Printf("\n错误: %s\n", *event.Data.Message)
			}
			select {
			case done <- struct{}{}:
			default:
			}
		}
	})

	prompt := fmt.Sprintf(`
    使用Playwright MCP服务器分析此网页的可访问性: %s
    
    请执行以下步骤:
    1. 使用playwright-browser_navigate工具导航到URL
    2. 使用playwright-browser_snapshot工具捕获可访问性快照
    3. 分析快照并提供详细的可访问性报告
    
    报告格式请使用表情符号指示器:
    - 📊 可访问性报告标题
    - ✅ 有效项 (包含分类、状态、详情的表格)
    - ⚠️ 发现的问题 (包含严重程度、问题、WCAG标准、建议的表格)
    - 📋 统计摘要 (链接、标题、可聚焦元素、地标)
    - ⚙️ 优先级建议
    
    使用✅表示通过，🔴表示严重问题，🟡表示中等严重问题，❌表示缺失项。
    请包含实际的页面分析结果。
    `, url)

	if _, err := session.Send(ctx, copilot.MessageOptions{Prompt: prompt}); err != nil {
		log.Fatal(err)
	}
	<-done

	fmt.Println("\n\n=== 报告完成 ===\n")

	// 提示用户是否生成测试用例
	fmt.Print("是否要生成Playwright可访问性测试？(y/n): ")
	generateTests, _ := reader.ReadString('\n')
	generateTests = strings.TrimSpace(strings.ToLower(generateTests))

	if generateTests == "y" || generateTests == "yes" {
		detectLanguagePrompt := `
        分析当前工作目录以检测主要编程语言。
        仅回复检测到的语言名称和简要说明。
        如果未检测到项目，请建议使用"TypeScript"作为默认语言。
        `

		fmt.Println("\n检测项目语言...\n")
		select {
		case <-done:
		default:
		}
		if _, err := session.Send(ctx, copilot.MessageOptions{Prompt: detectLanguagePrompt}); err != nil {
			log.Fatal(err)
		}
		<-done

		fmt.Print("\n\n确认测试语言 (或输入其他语言): ")
		language, _ := reader.ReadString('\n')
		language = strings.TrimSpace(language)
		if language == "" {
			language = "TypeScript"
		}

		testGenerationPrompt := fmt.Sprintf(`
        基于您刚刚为 %s 生成的可访问性报告，
        创建 %s 语言的Playwright可访问性测试。
        
        包含以下测试：
        lang属性、标题、标题层级、alt文本、
        地标、跳过导航、焦点指示器、触控目标。
        使用Playwright的可访问性测试功能并添加有帮助的注释。
        输出完整的测试文件。
        `, url, language)

		fmt.Println("\n生成可访问性测试...\n")
		select {
		case <-done:
		default:
		}
		if _, err := session.Send(ctx, copilot.MessageOptions{Prompt: testGenerationPrompt}); err != nil {
			log.Fatal(err)
		}
		<-done

		fmt.Println("\n\n=== 测试生成完成 ===")
	}
}
```

## 工作原理

1. **Playwright MCP服务器**：配置一个本地MCP服务器运行`@playwright/mcp`以提供浏览器自动化工具
2. **流式输出**：使用`Streaming: &streaming`和`assistant.message.delta`事件实现逐个token的实时输出
3. **可访问性快照**：Playwright的`browser_snapshot`工具捕获页面完整的可访问性树
4. **结构化报告**：通过提示词引导模型生成符合WCAG标准的统一报告格式，包含表情符号严重程度指示器
5. **测试生成**：可选地检测项目语言并生成Playwright可访问性测试

## 关键概念

### MCP服务器配置

该示例配置了一个与会话并行运行的本地MCP服务器：

```go
session, err := client.CreateSession(ctx, &copilot.SessionConfig{
    McpServers: map[string]interface{}{
        "playwright": map[string]interface{}{
            "type":    "local",
            "command": "npx",
            "args":    []string{"@playwright/mcp@latest"},
            "tools":   []string{"*"},
        },
    },
})
```

这使模型能够访问Playwright浏览器工具，如`browser_navigate`、`browser_snapshot`和`browser_click`。

### 流式事件处理

与`SendAndWait`不同，该示例使用流式处理实现实时输出：

```go
session.On(func(event copilot.SessionEvent) {
    switch event.Type {
    case "assistant.message.delta":
        if event.Data.DeltaContent != nil {
            fmt.Print(*event.Data.DeltaContent)
        }
    case "session.idle":
        done <- struct{}{}
    }
})
```

## 示例交互

```
=== 可访问性报告生成器 ===

请输入要分析的URL：github.com

分析中: https://github.com
请稍候...

📊 可访问性报告：GitHub (github.com)

✅ 有效项
| 分类 | 状态 | 详情 |
|------|------|------|
| 语言 | ✅ 通过 | lang="en" 正确设置 |
| 页面标题 | ✅ 通过 | "GitHub" 可识别 |
| 标题层级 | ✅ 通过 | 正确的H1/H2结构 |
| 图像 | ✅ 通过 | 所有图像都有alt文本 |

⚠️ 发现的问题
| 严重程度 | 问题 | WCAG标准 | 建议 |
|----------|------|----------|-----|
| 🟡 中等 | 部分链接缺少描述性文本 | 2.4.4 | 为仅图标链接添加aria-label |

📋 统计摘要
- 总链接数：47
- 总标题数：8 (1× H1，层级正确)
- 可聚焦元素：52
- 检测到的地标：banner ✅，导航 ✅，主内容 ✅，页脚 ✅

=== 报告完成 ===

是否要生成Playwright可访问性测试？(y/n): y

检测项目语言...
检测到TypeScript (发现package.json文件)

确认测试语言 (或输入其他语言): 

生成可访问性测试...
[生成的测试文件输出...]

=== 测试生成完成 ===
```

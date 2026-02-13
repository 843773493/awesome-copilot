# 生成可访问性报告

构建一个命令行工具，使用 Playwright MCP 服务器分析网页可访问性，并生成符合 WCAG 标准的详细报告，可选生成测试文件。

> **可运行示例：** [recipe/accessibility-report.cs](recipe/accessibility-report.cs)
>
> ```bash
> dotnet run recipe/accessibility-report.cs
> ```

## 示例场景

您希望审计网站的可访问性合规性。此工具使用 Playwright 导航到指定 URL，捕获可访问性快照，并生成涵盖地标、标题层级、焦点管理、触控目标等 WCAG 标准的结构化报告。它还可以生成 Playwright 测试文件以自动化未来的可访问性检查。

## 先决条件

```bash
dotnet add package GitHub.Copilot.SDK
```

您还需要 `npx` 可用（已安装 Node.js）以运行 Playwright MCP 服务器。

## 使用方法

```bash
dotnet run recipe/accessibility-report.cs
# 输入要分析的 URL
```

## 完整示例：accessibility-report.cs

```csharp
#:package GitHub.Copilot.SDK@*

using GitHub.Copilot.SDK;

// 创建并启动客户端
await using var client = new CopilotClient();
await client.StartAsync();

Console.WriteLine("=== 可访问性报告生成器 ===");
Console.WriteLine();

Console.Write("请输入要分析的 URL：");
var url = Console.ReadLine()?.Trim();

if (string.IsNullOrWhiteSpace(url))
{
    Console.WriteLine("未提供 URL。退出。");
    return;
}

// 确保 URL 包含协议
if (!url.StartsWith("http://") && !url.StartsWith("https://"))
{
    url = "https://" + url;
}

Console.WriteLine($"\n正在分析：{url}");
Console.WriteLine("请稍候...\n");

// 创建与 Playwright MCP 服务器的会话
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "claude-opus-4.6",
    Streaming = true,
    McpServers = new Dictionary<string, object>()
    {
        ["playwright"] =
        new McpLocalServerConfig
        {
            Type = "local",
            Command = "npx",
            Args = ["@playwright/mcp@latest"],
            Tools = ["*"]
        }
    },
});

// 使用 session.idle 事件等待响应
var done = new TaskCompletionSource();

session.On(evt =>
{
    switch (evt)
    {
        case AssistantMessageDeltaEvent delta:
            Console.Write(delta.Data.DeltaContent);
            break;
        case SessionIdleEvent:
            done.TrySetResult();
            break;
        case SessionErrorEvent error:
            Console.WriteLine($"\n错误：{error.Data.Message}");
            done.TrySetResult();
            break;
    }
});

var prompt = $"""
    使用 Playwright MCP 服务器分析此网页的可访问性：{url}
    
    请执行以下步骤：
    1. 使用 playwright-browser_navigate 工具导航到 URL
    2. 使用 playwright-browser_snapshot 工具捕获可访问性快照
    3. 分析快照并生成详细可访问性报告
    
    严格按照以下结构格式化报告，使用表情符号指示严重程度：

    📊 可访问性报告：[页面标题] (domain.com)

    ✅ 优点
    | 类别 | 状态 | 详情 |
    |------|------|------|
    | 语言 | ✅ 通过 | lang="en-US" 正确设置 |
    | 页面标题 | ✅ 通过 | "[标题]" 描述性良好 |
    | 标题层级 | ✅ 通过 | 单个 H1，H2/H3 层级结构正确 |
    | 图像 | ✅ 通过 | 所有 X 张图像都有 alt 文本 |

    ⚠️ 发现的问题
    | 严重程度 | 问题 | WCAG 标准 | 建议 |
    |----------|------|-----------|------|
    | 🔴 高 | 缺少 <main> 地标 | 1.3.1, 2.4.1 | 将主内容包裹在 <main> 元素中 |
    | 🟡 中 | 焦点轮廓被禁用 | 2.4.7 | 确保可见的 :focus 样式存在 |

    📋 统计摘要
    - 总链接数：X
    - 总标题数：X
    - 可聚焦元素：X
    - 检测到的地标：banner ✅，导航 ✅，main ❌，页脚 ✅

    ⚙️ 优先建议
    ...

    使用 ✅ 表示通过，🔴 表示高严重性问题，🟡 表示中严重性问题，❌ 表示缺失项。
    包含页面分析的实际结果 - 不要仅复制示例。
    """;

await session.SendAsync(new MessageOptions { Prompt = prompt });
await done.Task;

Console.WriteLine("\n\n=== 报告完成 ===\n");

// 提示用户是否生成测试文件
Console.Write("是否要生成 Playwright 可访问性测试？(y/n): ");
var generateTests = Console.ReadLine()?.Trim().ToLowerInvariant();

if (generateTests == "y" || generateTests == "yes")
{
    // 重置以进行下一次交互
    done = new TaskCompletionSource();

    var detectLanguagePrompt = $"""
        分析当前工作目录以检测该项目中使用的主编程语言。
        仅以检测到的语言名称和简要说明作为响应。
        如果未检测到项目，请建议使用 "TypeScript" 作为 Playwright 测试的默认语言。
        """;

    Console.WriteLine("\n检测项目语言...\n");
    await session.SendAsync(new MessageOptions { Prompt = detectLanguagePrompt });
    await done.Task;

    Console.Write("\n\n确认测试语言（或输入其他语言）：");
    var language = Console.ReadLine()?.Trim();

    if (string.IsNullOrWhiteSpace(language))
    {
        language = "TypeScript";
    }

    // 重置以生成测试文件
    done = new TaskCompletionSource();

    var testGenerationPrompt = $"""
        基于您刚刚为 {url} 生成的可访问性报告，创建 {language} 的 Playwright 可访问性测试。
        
        测试应：
        1. 验证报告中所有可访问性检查项
        2. 测试发现的问题（以确保问题得到修复）
        3. 包含地标、标题层级、alt 文本、焦点指示器等测试
        4. 使用 Playwright 的可访问性测试功能
        5. 包含有助于解释每个测试的注释
        
        输出完整的测试文件，以便保存和运行。
        """;

    Console.WriteLine("\n生成可访问性测试...\n");
    await session.SendAsync(new MessageOptions { Prompt = testGenerationPrompt });
    await done.Task;

    Console.WriteLine("\n\n=== 测试已生成 ===");
}
```

## 工作原理

1. **Playwright MCP 服务器**：配置一个本地 MCP 服务器运行 `@playwright/mcp`，以提供浏览器自动化工具
2. **流式输出**：使用 `Streaming = true` 和 `AssistantMessageDeltaEvent` 实现实时逐令牌输出
3. **可访问性快照**：Playwright 的 `browser_snapshot` 工具捕获页面的完整可访问性树
4. **结构化报告**：提示词引导模型生成符合 WCAG 标准的统一报告格式，使用表情符号表示严重程度
5. **测试生成**：可选地检测项目语言并生成 Playwright 可访问性测试

## 关键概念

### MCP 服务器配置

该示例配置了一个与会话并行运行的本地 MCP 服务器：

```csharp
McpServers = new Dictionary<string, object>()
{
    ["playwright"] = new McpLocalServerConfig
    {
        Type = "local",
        Command = "npx",
        Args = ["@playwright/mcp@latest"],
        Tools = ["*"]
    }
}
```

这使模型能够访问 Playwright 浏览器工具，如 `browser_navigate`、`browser_snapshot` 和 `browser_click`。

### 使用事件进行流式处理

与 `SendAndWaitAsync` 不同，此示例使用流式处理实现实时输出：

```csharp
session.On(evt =>
{
    switch (evt)
    {
        case AssistantMessageDeltaEvent delta:
            Console.Write(delta.Data.DeltaContent); // 逐令牌输出
            break;
        case SessionIdleEvent:
            done.TrySetResult(); // 模型完成
            break;
    }
});
```

## 示例交互

```
=== 可访问性报告生成器 ===

请输入要分析的 URL：github.com

正在分析：https://github.com
请稍候...

📊 可访问性报告：GitHub (github.com)

✅ 优点
| 类别 | 状态 | 详情 |
|------|------|------|
| 语言 | ✅ 通过 | lang="en" 正确设置 |
| 页面标题 | ✅ 通过 | "GitHub" 易识别 |
| 标题层级 | ✅ 通过 | H1/H2 结构正确 |
| 图像 | ✅ 通过 | 所有图像都有 alt 文本 |

⚠️ 发现的问题
| 严重程度 | 问题 | WCAG 标准 | 建议 |
|----------|------|-----------|-----|
| 🟡 中 | 部分链接缺少描述性文本 | 2.4.4 | 为仅图标链接添加 aria-label |

📋 统计摘要
- 总链接数：47
- 总标题数：8（1× H1，层级结构正确）
- 可聚焦元素：52
- 检测到的地标：banner ✅，导航 ✅，main ✅，页脚 ✅

=== 报告完成 ===

是否要生成 Playwright 可访问性测试？(y/n): y

检测项目语言...
检测到 TypeScript（发现 package.json 文件）

确认测试语言（或输入其他语言）：

生成可访问性测试...
[生成的测试文件输出...]

=== 测试已生成 ===
```

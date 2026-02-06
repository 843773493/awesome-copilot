# 生成PR年龄图表

构建一个交互式命令行工具，利用Copilot内置功能可视化GitHub仓库中拉取请求（PR）的开放时间分布情况。

> **可运行示例：** [recipe/pr-visualization.cs](recipe/pr-visualization.cs)
>
> ```bash
> # 从当前git仓库自动检测
> dotnet run recipe/pr-visualization.cs
>
> # 显式指定仓库
> dotnet run recipe/pr-visualization.cs -- --repo github/copilot-sdk
> ```

## 示例场景

您希望了解某个仓库中拉取请求（PR）已开放的时间长度。此工具可检测当前git仓库或接受仓库作为输入，然后让Copilot通过GitHub MCP服务器获取PR数据并生成图表图像。

## 先决条件

```bash
dotnet add package GitHub.Copilot.SDK
```

## 使用方法

```bash
# 从当前git仓库自动检测
dotnet run

# 显式指定仓库
dotnet run -- --repo github/copilot-sdk
```

## 完整示例：pr-visualization.cs

```csharp
using System.Diagnostics;
using GitHub.Copilot.SDK;

// ============================================================================
// Git与GitHub检测
// ============================================================================

bool IsGitRepo()
{
    try
    {
        Process.Start(new ProcessStartInfo
        {
            FileName = "git",
            Arguments = "rev-parse --git-dir",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        })?.WaitForExit();
        return true;
    }
    catch
    {
        return false;
    }
}

string? GetGitHubRemote()
{
    try
    {
        var proc = Process.Start(new ProcessStartInfo
        {
            FileName = "git",
            Arguments = "remote get-url origin",
            RedirectStandardOutput = true,
            UseShellExecute = false,
            CreateNoWindow = true
        });

        var remoteUrl = proc?.StandardOutput.ReadToEnd().Trim();
        proc?.WaitForExit();

        if (string.IsNullOrEmpty(remoteUrl)) return null;

        // 处理SSH格式：git@github.com:owner/repo.git
        var sshMatch = System.Text.RegularExpressions.Regex.Match(
            remoteUrl, @"git@github\.com:(.+/.+?)(?:\.git)?$");
        if (sshMatch.Success) return sshMatch.Groups[1].Value;

        // 处理HTTPS格式：https://github.com/owner/repo.git
        var httpsMatch = System.Text.RegularExpressions.Regex.Match(
            remoteUrl, @"https://github\.com/(.+/.+?)(?:\.git)?$");
        if (httpsMatch.Success) return httpsMatch.Groups[1].Value;

        return null;
    }
    catch
    {
        return null;
    }
}

string? ParseRepoArg(string[] args)
{
    var repoIndex = Array.IndexOf(args, "--repo");
    if (repoIndex != -1 && repoIndex + 1 < args.Length)
    {
        return args[repoIndex + 1];
    }
    return null;
}

string PromptForRepo()
{
    Console.Write("请输入GitHub仓库（格式为owner/repo）: ");
    return Console.ReadLine()?.Trim() ?? "";
}

// ============================================================================
// 主程序
// ============================================================================

Console.WriteLine("🔍 PR年龄图表生成器\n");

// 确定仓库
var repo = ParseRepoArg(args);

if (!string.IsNullOrEmpty(repo))
{
    Console.WriteLine($"📦 使用指定的仓库: {repo}");
}
else if (IsGitRepo())
{
    var detected = GetGitHubRemote();
    if (detected != null)
    {
        repo = detected;
        Console.WriteLine($"📦 检测到GitHub仓库: {repo}");
    }
    else
    {
        Console.WriteLine("⚠️  检测到git仓库但未找到GitHub远程仓库。");
        repo = PromptForRepo();
    }
}
else
{
    Console.WriteLine("📁 不在git仓库中。");
    repo = PromptForRepo();
}

if (string.IsNullOrEmpty(repo) || !repo.Contains('/'))
{
    Console.WriteLine("❌ 仓库格式无效。预期格式：owner/repo");
    return;
}

var parts = repo.Split('/');
var owner = parts[0];
var repoName = parts[1];

// 创建Copilot客户端 - 无需自定义工具
await using var client = new CopilotClient(new CopilotClientOptions { LogLevel = "error" });
await client.StartAsync();

var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5",
    SystemMessage = new SystemMessageConfig
    {
        Content = $"""
<context>
您正在分析GitHub仓库：{owner}/{repoName} 的拉取请求
当前工作目录为：{Environment.CurrentDirectory}
</context>

<instructions>
- 使用GitHub MCP服务器工具获取PR数据
- 使用您的文件和代码执行工具生成图表
- 将生成的图像保存到当前工作目录
- 保持回复简洁
</instructions>
"""
    }
});

// 设置事件处理
session.On(evt =>
{
    switch (evt)
    {
        case AssistantMessageEvent msg:
            Console.WriteLine($"\n🤖 {msg.Data.Content}\n");
            break;
        case ToolExecutionStartEvent toolStart:
            Console.WriteLine($"  ⚙️  {toolStart.Data.ToolName}");
            break;
    }
});

// 初始提示 - 让Copilot处理细节
Console.WriteLine("\n📊 开始分析...\n");

await session.SendAsync(new MessageOptions
{
    Prompt = $"""
      从{owner}/{repoName}获取过去一周内开放的拉取请求。
      计算每个PR的开放天数。
      然后生成一个条形图，显示PR开放时间的分布情况
      （将它们分组到合理的桶中，例如<1天、1-3天等）。
      将图表保存为"pr-age-chart.png"到当前目录。
      最后，总结PR的健康状况 - 平均开放时间、最老的PR以及可能被视为过期的PR数量。
    """
});

// 交互式循环
Console.WriteLine("\n💡 输入后续问题或输入\"exit\"退出。\n");
Console.WriteLine("示例：");
Console.WriteLine("  - \"扩展到过去一个月\"");
Console.WriteLine("  - \"显示5个最老的PR\"");
Console.WriteLine("  - \"生成饼图\"");
Console.WriteLine("  - \"按作者而非年龄分组\"");
Console.WriteLine();

while (true)
{
    Console.Write("You: ");
    var input = Console.ReadLine()?.Trim();

    if (string.IsNullOrEmpty(input)) continue;
    if (input.ToLower() is "exit" or "quit")
    {
        Console.WriteLine("👋 再见！");
        break;
    }

    await session.SendAsync(new MessageOptions { Prompt = input });
}
```

## 工作原理

1. **仓库检测**：检查`--repo`标志 → git远程仓库 → 提示用户输入
2. **无需自定义工具**：完全依赖Copilot CLI内置功能：
   - **GitHub MCP服务器** - 从GitHub获取PR数据
   - **文件工具** - 保存生成的图表图像
   - **代码执行** - 使用Python/matplotlib或其他方法生成图表
3. **交互式会话**：初始分析完成后，用户可提出调整请求

## 为何采用此方法？

| 方面          | 自定义工具      | 内置Copilot                  |
| --------------- | ----------------- | --------------------------------- |
| 代码复杂度 | 高              | **极简**                       |
| 维护       | 您需维护        | **由Copilot维护**             |
| 灵活性     | 固定逻辑         | **AI决定最佳方法**      |
| 图表类型   | 仅限您编写的类型 | **Copilot可生成的任意类型** |
| 数据分组   | 硬编码的桶       | **智能分组**          |

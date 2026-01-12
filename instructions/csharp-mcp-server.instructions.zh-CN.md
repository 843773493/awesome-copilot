

---
description: '使用 C# SDK 构建 Model Context Protocol (MCP) 服务器的说明'
applyTo: '**/*.cs, **/*.csproj'
---

# C# MCP 服务器开发

## 说明

- 对于大多数项目，请使用 **ModelContextProtocol** NuGet 包（预发行版本）: `dotnet add package ModelContextProtocol --prerelease`
- 对于基于 HTTP 的 MCP 服务器，请使用 **ModelContextProtocol.AspNetCore**
- 对于需要最小依赖项（仅客户端或低级别服务器 API）的场景，请使用 **ModelContextProtocol.Core**
- 始终使用 `LogToStandardErrorThreshold = LogLevel.Trace` 配置日志输出到标准错误，以避免干扰标准 I/O 传输
- 在包含 MCP 工具的类上使用 `[McpServerToolType]` 特性
- 在方法上使用 `[McpServerTool]` 特性以将其暴露为工具
- 使用 `System.ComponentModel` 中的 `[Description]` 特性来记录工具和参数
- 在工具方法中支持依赖注入 - 可将 `McpServer`、`HttpClient` 或其他服务作为参数注入
- 使用 `McpServer.AsSamplingChatClient()` 从工具内部向客户端发送抽样请求
- 通过在类上使用 `[McpServerPromptType]` 和在方法上使用 `[McpServerPrompt]` 暴露提示信息
- 对于标准 I/O 传输，请在构建服务器时使用 `WithStdioServerTransport()`
- 使用 `WithToolsFromAssembly()` 自动发现并注册当前程序集中的所有工具
- 工具方法可以是同步或异步（返回 `Task` 或 `Task<T>`）
- 始终为工具和参数提供全面的描述，以帮助大语言模型理解其用途
- 在异步工具中使用 `CancellationToken` 参数以实现正确的取消支持
- 返回可序列化为 JSON 的简单类型（如 string、int 等）或复杂对象
- 如需精细控制，请使用 `McpServerOptions` 并配合自定义处理程序（如 `ListToolsHandler` 和 `CallToolHandler`）
- 使用 `McpProtocolException` 报告带有适当 `McpErrorCode` 值的协议级别错误
- 使用同一 SDK 中的 `McpClient` 或任何符合 MCP 规范的客户端测试 MCP 服务器
- 使用 Microsoft.Extensions.Hosting 结构化项目以实现正确的依赖注入和生命周期管理

## 最佳实践

- 保持工具方法的专注性和单一用途
- 使用能清晰表明功能的有意义的工具名称
- 提供详细描述，解释工具的功能、所需参数及返回结果
- 验证输入参数，对无效输入抛出 `McpProtocolException` 并使用 `McpErrorCode.InvalidParams` 错误码
- 使用结构化日志以帮助调试，避免污染标准输出
- 将相关工具组织到具有 `[McpServerToolType]` 特性的逻辑类中
- 暴露访问外部资源的工具时需考虑其安全影响
- 使用内置的依赖注入容器来管理服务生命周期和依赖关系
- 实现适当的错误处理并返回有意义的错误信息
- 在集成到大语言模型之前，应单独测试每个工具

## 常见模式

### 基础服务器设置
```csharp
var builder = Host.CreateApplicationBuilder(args);
builder.Logging.AddConsole(options => 
    options.LogToStandardErrorThreshold = LogLevel.Trace);
builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();
await builder.Build().RunAsync();
```

### 简单工具
```csharp
[McpServerToolType]
public static class MyTools
{
    [McpServerTool, Description("该工具的功能描述")]
    public static string ToolName(
        [Description("参数描述")] string param) => 
        $"结果: {param}";
}
```

### 支持依赖注入的工具
```csharp
[McpServerTool, Description("从 URL 获取数据")]
public static async Task<string> FetchData(
    HttpClient httpClient,
    [Description("要获取的 URL")] string url,
    CancellationToken cancellationToken) =>
    await httpClient.GetStringAsync(url, cancellationToken);
```

### 支持抽样的工具
```csharp
[McpServerTool, Description("使用客户端的 LLM 分析内容")]
public static async Task<string> Analyze(
    McpServer server,
    [Description("要分析的内容")] string content,
    CancellationToken cancellationToken)
{
    var messages = new ChatMessage[]
    {
        new(ChatRole.User, $"分析此内容: {content}")
    };
    return await server.AsSamplingChatClient()
        .GetResponseAsync(messages, cancellationToken: cancellationToken);
}
```
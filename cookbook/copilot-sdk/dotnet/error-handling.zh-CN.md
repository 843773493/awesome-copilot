# 错误处理模式

在您的 Copilot SDK 应用程序中优雅地处理错误。

> **可运行示例：** [recipe/error-handling.cs](recipe/error-handling.cs)
>
> ```bash
> dotnet run recipe/error-handling.cs
> ```

## 示例场景

您需要处理各种错误情况，例如连接失败、超时和无效响应。

## 基本的 try-catch

```csharp
using GitHub.Copilot.SDK;

var client = new CopilotClient();

try
{
    await client.StartAsync();
    var session = await client.CreateSessionAsync(new SessionConfig
    {
        Model = "gpt-5"
    });

    var done = new TaskCompletionSource<string>();
    session.On(evt =>
    {
        if (evt is AssistantMessageEvent msg)
        {
            done.SetResult(msg.Data.Content);
        }
    });

    await session.SendAsync(new MessageOptions { Prompt = "Hello!" });
    var response = await done.Task;
    Console.WriteLine(response);

    await session.DisposeAsync();
}
catch (Exception ex)
{
    Console.WriteLine($"错误: {ex.Message}");
}
finally
{
    await client.StopAsync();
}
```

## 处理特定错误类型

```csharp
try
{
    await client.StartAsync();
}
catch (FileNotFoundException)
{
    Console.WriteLine("Copilot CLI 未找到。请先安装它。");
}
catch (HttpRequestException ex) when (ex.Message.Contains("connection"))
{
    Console.WriteLine("无法连接到 Copilot CLI 服务器。");
}
catch (Exception ex)
{
    Console.WriteLine($"意外错误: {ex.Message}");
}
```

## 超时处理

```csharp
var session = await client.CreateSessionAsync(new SessionConfig { Model = "gpt-5" });

try
{
    var done = new TaskCompletionSource<string>();
    session.On(evt =>
    {
        if (evt is AssistantMessageEvent msg)
        {
            done.SetResult(msg.Data.Content);
        }
    });

    await session.SendAsync(new MessageOptions { Prompt = "复杂问题..." });

    // 带超时等待 (30 秒)
    using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
    var response = await done.Task.WaitAsync(cts.Token);

    Console.WriteLine(response);
}
catch (OperationCanceledException)
{
    Console.WriteLine("请求超时");
}
```

## 取消请求

```csharp
var session = await client.CreateSessionAsync(new SessionConfig { Model = "gpt-5" });

// 启动请求
await session.SendAsync(new MessageOptions { Prompt = "写一个很长的故事..." });

// 在某些条件后取消请求
await Task.Delay(5000);
await session.AbortAsync();
Console.WriteLine("请求已取消");
```

## 优雅关闭

```csharp
Console.CancelKeyPress += async (sender, e) =>
{
    e.Cancel = true;
    Console.WriteLine("正在关闭...");

    var errors = await client.StopAsync();
    if (errors.Count > 0)
    {
        Console.WriteLine($"清理错误: {string.Join(", ", errors)}");
    }

    Environment.Exit(0);
};
```

## 使用 await using 实现自动释放

```csharp
await using var client = new CopilotClient();
await client.StartAsync();

var session = await client.CreateSessionAsync(new SessionConfig { Model = "gpt-5" });

// ... 执行工作 ...

// 退出作用域时会自动调用 client.StopAsync()
```

## 最佳实践

1. **始终进行清理**：使用 try-finally 或 `await using` 确保调用 `StopAsync()`
2. **处理连接错误**：CLI 可能未安装或未运行
3. **设置适当的超时**：使用 `CancellationToken` 处理长时间运行的请求
4. **记录错误**：捕获错误详细信息以供调试

# 按元数据分组文件

使用 Copilot 根据文件的元数据智能地对文件夹中的文件进行分组整理。

> **可运行示例：** [recipe/managing-local-files.cs](recipe/managing-local-files.cs)
>
> ```bash
> dotnet run recipe/managing-local-files.cs
> ```

## 示例场景

您有一个包含大量文件的文件夹，希望根据文件类型、创建日期、大小或其他属性将其整理到子文件夹中。Copilot 可以分析这些文件，并建议或执行分组策略。

## 示例代码

```csharp
using GitHub.Copilot.SDK;

// 创建并启动客户端
await using var client = new CopilotClient();
await client.StartAsync();

// 定义文件操作工具
var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5"
});

// 等待会话完成
var done = new TaskCompletionSource();

session.On(evt =>
{
    switch (evt)
    {
        case AssistantMessageEvent msg:
            Console.WriteLine($"\nCopilot: {msg.Data.Content}");
            break;
        case ToolExecutionStartEvent toolStart:
            Console.WriteLine($"  → 运行: {toolStart.Data.ToolName} ({toolStart.Data.ToolCallId})");
            break;
        case ToolExecutionCompleteEvent toolEnd:
            Console.WriteLine($"  ✓ 完成: {toolEnd.Data.ToolCallId}");
            break;
        case SessionIdleEvent:
            done.SetResult();
            break;
    }
});

// 请求 Copilot 整理文件
var targetFolder = @"C:\Users\Me\Downloads";

await session.SendAsync(new MessageOptions
{
    Prompt = $"""
        分析 "{targetFolder}" 中的文件并将其整理到子文件夹中。

        1. 首先列出所有文件及其元数据
        2. 预览按文件扩展名分组的情况
        3. 创建适当的子文件夹（例如："images"、"documents"、"videos"）
        4. 将每个文件移动到对应的子文件夹中

        移动文件前请确认。
        """
});

await done.Task;
```

## 分组策略

### 按文件扩展名分组

```csharp
// 按以下方式分组文件：
// images/   -> .jpg, .png, .gif
// documents/ -> .pdf, .docx, .txt
// videos/   -> .mp4, .avi, .mov
```

### 按创建日期分组

```csharp
// 按以下方式分组文件：
// 2024-01/ -> 2024年1月创建的文件
// 2024-02/ -> 2024年2月创建的文件
```

### 按文件大小分组

```csharp
// 按以下方式分组文件：
// tiny-under-1kb/
// small-under-1mb/
// medium-under-100mb/
// large-over-100mb/
```

## 干运行模式

为了安全起见，您可以要求 Copilot 仅预览更改：

```csharp
await session.SendAsync(new MessageOptions
{
    Prompt = $"""
        分析 "{targetFolder}" 中的文件，并向我展示您如何按文件类型进行整理。
        不要移动任何文件 - 仅展示整理计划。
        """
});
```

## 基于 AI 分析的自定义分组

让 Copilot 根据文件内容确定最佳分组方式：

```csharp
await session.SendAsync(new MessageOptions
{
    Prompt = $"""
        查看 "{targetFolder}" 中的文件，并建议一个合理的组织方式。
        考虑以下因素：
        - 文件名及其可能包含的内容
        - 文件类型及其典型用途
        - 可能表示项目或事件的日期模式

        提出具有描述性和实用性的文件夹名称。
        """
});
```

## 安全注意事项

1. **移动前确认**：在执行移动操作前，请要求 Copilot 进行确认
2. **处理重复文件**：考虑如果存在同名文件会发生什么
3. **保留原始文件**：对于重要文件，考虑复制而非移动

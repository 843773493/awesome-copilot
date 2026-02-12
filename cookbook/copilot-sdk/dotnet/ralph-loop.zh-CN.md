# Ralph Loop：自主AI任务循环

构建自主编码循环，其中AI代理选择任务、实现任务、通过回压（测试、构建）进行验证、提交更改并重复——每个迭代都在全新的上下文窗口中进行。

> **可运行示例：** [recipe/ralph-loop.cs](recipe/ralph-loop.cs)
>
> ```bash
> cd dotnet
> dotnet run recipe/ralph-loop.cs
> ```

## 什么是Ralph Loop？

[Ralph Loop](https://ghuntley.com/ralph/) 是一种自主开发工作流，AI代理在隔离的上下文窗口中迭代执行任务。核心洞察：**状态存储在磁盘上，而非模型的上下文中**。每次迭代都从头开始，读取当前状态文件，执行一项任务，将结果写回磁盘并退出。

```
┌─────────────────────────────────────────────────┐
│                   loop.sh                       │
│  while true:                                    │
│    ┌─────────────────────────────────────────┐  │
│    │  新会话（隔离上下文）                    │  │
│    │                                         │  │
│    │  1. 读取 PROMPT.md + AGENTS.md           │  │
│    │  2. 研究 specs/* 和代码                  │  │
│    │  3. 从计划中选择下一个任务                │  │
│    │  4. 实现 + 运行测试                       │  │
│    │  5. 更新计划，提交并退出                  │  │
│    └─────────────────────────────────────────┘  │
│    ↻ 下一个迭代（全新上下文）                   │
└─────────────────────────────────────────────────┘
```

**核心原则：**

- **每次迭代使用新的上下文环境**：每个循环创建一个新会话——不累积上下文，始终处于“智能区域”
- **磁盘作为共享状态**：`IMPLEMENTATION_PLAN.md` 在迭代之间持久化，并作为协调机制
- **回压确保质量**：测试、构建和代码检查会拒绝不良工作——代理必须在提交前修复问题
- **两种模式**：规划模式（差距分析 → 生成计划）和构建模式（根据计划实现）

## 简化版

最简化的Ralph循环——相当于SDK中的 `while :; do cat PROMPT.md | copilot ; done`：

```csharp
using GitHub.Copilot.SDK;

var client = new CopilotClient();
await client.StartAsync();

try
{
    var prompt = await File.ReadAllTextAsync("PROMPT.md");
    var maxIterations = 50;

    for (var i = 1; i <= maxIterations; i++)
    {
        Console.WriteLine($"\n=== 第{i}/{maxIterations}次迭代 ===");

        // 每次迭代使用新会话——上下文隔离是关键
        var session = await client.CreateSessionAsync(
            new SessionConfig { Model = "gpt-5.1-codex-mini" });
        try
        {
            var done = new TaskCompletionSource<string>();
            session.On(evt =>
            {
                if (evt is AssistantMessageEvent msg)
                    done.TrySetResult(msg.Data.Content);
            });

            await session.SendAsync(new MessageOptions { Prompt = prompt });
            await done.Task;
        }
        finally
        {
            await session.DisposeAsync();
        }

        Console.WriteLine($"第{i}次迭代完成。");
    }
}
finally
{
    await client.StopAsync();
}
```

以上内容即可开始使用。提示文件告诉代理要执行的任务；代理读取项目文件、完成工作、提交更改并退出。循环会以全新的状态重新启动。

## 完整版

完整的Ralph模式，包含规划和构建两种模式，与[Ralph Playbook](https://github.com/ClaytonFarr/ralph-playbook) 架构一致：

```csharp
using GitHub.Copilot.SDK;

// 解析参数：dotnet run [plan] [max_iterations]
var mode = args.Contains("plan") ? "plan" : "build";
var maxArg = args.FirstOrDefault(a => int.TryParse(a, out _));
var maxIterations = maxArg != null ? int.Parse(maxArg) : 50;
var promptFile = mode == "plan" ? "PROMPT_plan.md" : "PROMPT_build.md";

var client = new CopilotClient();
await client.StartAsync();

Console.WriteLine(new string('━', 40));
Console.WriteLine($"模式:   {mode}");
Console.WriteLine($"提示: {promptFile}");
Console.WriteLine($"最大:    {maxIterations} 次迭代");
Console.WriteLine(new string('━', 40));

try
{
    var prompt = await File.ReadAllTextAsync(promptFile);

    for (var i = 1; i <= maxIterations; i++)
    {
        Console.WriteLine($"\n=== 第{i}/{maxIterations}次迭代 ===");

        // 每次迭代使用新会话——每个任务都能获得完整的上下文预算
        var session = await client.CreateSessionAsync(
            new SessionConfig
            {
                Model = "gpt-5.1-codex-mini",
                // 将代理固定在项目目录中
                WorkingDirectory = Environment.CurrentDirectory,
                // 自动批准工具调用以实现无人值守操作
                OnPermissionRequest = (_, _) => Task.FromResult(
                    new PermissionRequestResult { Kind = "approved" }),
            });
        try
        {
            var done = new TaskCompletionSource<string>();
            session.On(evt =>
            {
                // 记录工具使用情况以提高可见性
                if (evt is ToolExecutionStartEvent toolStart)
                    Console.WriteLine($"  ⚙ {toolStart.Data.ToolName}");
                else if (evt is AssistantMessageEvent msg)
                    done.TrySetResult(msg.Data.Content);
            });

            await session.SendAsync(new MessageOptions { Prompt = prompt });
            await done.Task;
        }
        finally
        {
            await session.DisposeAsync();
        }

        Console.WriteLine($"\n第{i}次迭代完成。");
    }

    Console.WriteLine($"\n达到最大迭代次数: {maxIterations}");
}
finally
{
    await client.StopAsync();
}
```

### 必需的项目文件

完整版期望你的项目具有以下文件结构：

```
project-root/
├── PROMPT_plan.md              # 规划模式的指令
├── PROMPT_build.md             # 构建模式的指令
├── AGENTS.md                   # 操作指南（构建/测试命令）
├── IMPLEMENTATION_PLAN.md      # 任务列表（由规划模式生成）
├── specs/                      # 需求规格（每个主题一个文件）
│   ├── auth.md
│   └── data-pipeline.md
└── src/                        # 你的源代码
```

### 示例 `PROMPT_plan.md`

```markdown
0a. 研究 `specs/*` 以了解应用程序规格。
0b. 研究 IMPLEMENTATION_PLAN.md（如果存在）以理解当前计划。
0c. 研究 `src/` 以了解现有代码和共享工具。

1. 将规格与代码进行对比（差距分析）。创建或更新
   IMPLEMENTATION_PLAN.md 为待实现任务的优先级列表，但**不要**直接实现任何内容。

重要提示：**不要假设功能缺失**——首先在代码库中搜索以确认。优先更新现有工具而非创建临时副本。
```

### 示例 `PROMPT_build.md`

```markdown
0a. 研究 `specs/*` 以了解应用程序规格。
0b. 研究 IMPLEMENTATION_PLAN.md。
0c. 通过研究 `src/` 获取参考信息。

1. 从 IMPLEMENTATION_PLAN.md 中选择最重要的任务。在进行更改前，搜索代码库（不要假设未实现）。
2. 实现后运行测试。如果功能缺失，请添加它。
3. 发现问题时，立即更新 IMPLEMENTATION_PLAN.md。
4. 测试通过后，更新 IMPLEMENTATION_PLAN.md，然后执行 `git add -A`
   并通过带有描述性信息的 `git commit` 提交。

5. 在编写文档时，记录实现的原因。
6. 完整实现，不要使用占位符或草稿。
7. 保持 IMPLEMENTATION_PLAN.md 的最新状态——后续迭代依赖于此。
```

### 示例 `AGENTS.md`

保持简短（约60行）。每次迭代都会加载此文件，因此冗余会浪费上下文。

```markdown
## 构建与运行

dotnet build

## 验证

- 测试：`dotnet test`
- 构建：`dotnet build --no-restore`
```

## 最佳实践

1. **每次迭代使用新的上下文环境**：不要在迭代之间累积上下文——这是整个设计的核心
2. **磁盘即你的数据库**：`IMPLEMENTATION_PLAN.md` 是隔离会话之间的共享状态
3. **回压至关重要**：`AGENTS.md` 中的测试、构建和代码检查——代理必须通过这些验证后才能提交
4. **从规划模式开始**：首先生成计划，然后切换到构建模式
5. **观察并调整**：监控早期迭代，当代理以特定方式失败时，向提示中添加约束条件
6. **计划是可丢弃的**：如果代理偏离轨道，删除 `IMPLEMENTATION_PLAN.md` 并重新生成计划
7. **保持 `AGENTS.md` 简洁**：每次迭代都会加载该文件——仅包含操作信息，不包含进度说明
8. **使用沙盒环境**：代理以完全的工具访问权限自主运行——将其隔离
9. **设置 `WorkingDirectory`**：将会话固定在项目根目录，确保工具操作路径正确解析
10. **自动批准权限请求**：使用 `OnPermissionRequest` 允许工具调用而不中断循环

## 何时使用Ralph Loop

**适用于：**

- 从规格中实现功能并进行测试驱动验证
- 将大型重构拆分为多个小任务
- 无人值守的长期开发，且需求明确
- 任何可以通过回压（测试/构建）验证正确性的任务

**不适用于：**

- 需要循环中人工判断的任务
- 无需迭代的单次操作
- 没有可测试验收标准的模糊需求
- 方向不明确的探索性原型设计

## 参见

- [错误处理](error-handling.md) —— 长会话的超时模式和优雅关闭
- [会话持久化](persisting-sessions.md) —— 跨重启保存和恢复会话

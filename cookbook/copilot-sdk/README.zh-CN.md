# GitHub Copilot SDK 烹饪手册

本烹饪手册收集了针对不同编程语言中使用 GitHub Copilot SDK 完成常见任务的简短、聚焦的代码示例。每个示例都经过精心设计，简洁实用，包含可直接复制粘贴的代码片段，并指向完整的示例和测试。

## 按语言分类的食谱

### .NET (C#)

- [Ralph Loop](dotnet/ralph-loop.md): 使用每次迭代的新上下文构建自主的AI编码循环，支持规划/构建模式和回压控制。
- [错误处理](dotnet/error-handling.md): 优雅地处理错误，包括连接失败、超时和清理操作。
- [多会话管理](dotnet/multiple-sessions.md): 同时管理多个独立对话。
- [本地文件管理](dotnet/managing-local-files.md): 使用AI驱动的分组策略按元数据组织文件。
- [PR可视化](dotnet/pr-visualization.md): 使用GitHub MCP Server生成交互式PR年龄图表。
- [会话持久化](dotnet/persisting-sessions.md): 在重启之间保存和恢复会话。
- [可访问性报告](dotnet/accessibility-report.md): 使用Playwright MCP服务器生成WCAG可访问性报告。

### Node.js / TypeScript

- [Ralph Loop](nodejs/ralph-loop.md): 使用每次迭代的新上下文构建自主的AI编码循环，支持规划/构建模式和回压控制。
- [错误处理](nodejs/error-handling.md): 优雅地处理错误，包括连接失败、超时和清理操作。
- [多会话管理](nodejs/multiple-sessions.md): 同时管理多个独立对话。
- [本地文件管理](nodejs/managing-local-files.md): 使用AI驱动的分组策略按元数据组织文件。
- [PR可视化](nodejs/pr-visualization.md): 使用GitHub MCP Server生成交互式PR年龄图表。
- [会话持久化](nodejs/persisting-sessions.md): 在重启之间保存和恢复会话。
- [可访问性报告](nodejs/accessibility-report.md): 使用Playwright MCP服务器生成WCAG可访问性报告。

### Python

- [Ralph Loop](python/ralph-loop.md): 使用每次迭代的新上下文构建自主的AI编码循环，支持规划/构建模式和回压控制。
- [错误处理](python/error-handling.md): 优雅地处理错误，包括连接失败、超时和清理操作。
- [多会话管理](python/multiple-sessions.md): 同时管理多个独立对话。
- [本地文件管理](python/managing-local-files.md): 使用AI驱动的分组策略按元数据组织文件。
- [PR可视化](python/pr-visualization.md): 使用GitHub MCP Server生成交互式PR年龄图表。
- [会话持久化](python/persisting-sessions.md): 在重启之间保存和恢复会话。
- [可访问性报告](python/accessibility-report.md): 使用Playwright MCP服务器生成WCAG可访问性报告。

### Go

- [Ralph Loop](go/ralph-loop.md): 使用每次迭代的新上下文构建自主的AI编码循环，支持规划/构建模式和回压控制。
- [错误处理](go/error-handling.md): 优雅地处理错误，包括连接失败、超时和清理操作。
- [多会话管理](go/multiple-sessions.md): 同时管理多个独立对话。
- [本地文件管理](go/managing-local-files.md): 使用AI驱动的分组策略按元数据组织文件。
- [PR可视化](go/pr-visualization.md): 使用GitHub MCP Server生成交互式PR年龄图表。
- [会话持久化](go/persisting-sessions.md): 在重启之间保存和恢复会话。
- [可访问性报告](go/accessibility-report.md): 使用Playwright MCP服务器生成WCAG可访问性报告。

## 如何使用

- 浏览上方对应语言的章节并打开食谱链接
- 每个食谱包含可在 `recipe/` 子文件夹中运行的示例，使用语言特定的工具
- 查看现有示例和测试以获取实际参考：
  - Node.js 示例：`nodejs/examples/basic-example.ts`
  - 端到端测试：`go/e2e`, `python/e2e`, `nodejs/test/e2e`, `dotnet/test/Harness`

## 运行示例

### .NET

```bash
cd dotnet/cookbook/recipe
dotnet run <filename>.cs
```

### Node.js

```bash
cd nodejs/cookbook/recipe
npm install
npx tsx <filename>.ts
```

### Python

```bash
cd python/cookbook/recipe
pip install -r requirements.txt
python <filename>.py
```

### Go

```bash
cd go/cookbook/recipe
go run <filename>.go
```

## 贡献

- 通过在您语言的 `cookbook/` 文件夹中创建一个 markdown 文件和在 `recipe/` 中创建可运行的示例来提出或添加新食谱
- 请参阅 [CONTRIBUTING.md](../../CONTRIBUTING.md) 中的仓库指南

## 状态

烹饪手册的结构已完整，包含所有四种支持语言的7个食谱。每个食谱均包含Markdown文档和可运行的示例。

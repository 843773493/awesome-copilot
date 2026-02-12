# GitHub Copilot SDK 实用指南

本实用指南收集了针对 GitHub Copilot SDK 在不同语言中完成常见任务的小而聚焦的食谱。每个食谱都经过精心设计，简短且实用，包含可直接复制粘贴的代码片段，并指向更完整的示例和测试。

## 按语言分类的食谱

### .NET (C#)

- [Ralph Loop](dotnet/ralph-loop.md): 构建自主的AI编码循环，每次迭代都使用新鲜上下文，支持规划/构建模式和背压控制。
- [错误处理](dotnet/error-handling.md): 优雅地处理错误，包括连接失败、超时和清理操作。
- [多会话管理](dotnet/multiple-sessions.md): 同时管理多个独立对话。
- [本地文件管理](dotnet/managing-local-files.md): 利用AI驱动的分组策略按元数据组织文件。
- [Pull Request 可视化](dotnet/pr-visualization.md): 使用 GitHub MCP Server 生成交互式 Pull Request 年龄图表。
- [会话持久化](dotnet/persisting-sessions.md): 在重启之间保存并恢复会话。

### Node.js / TypeScript

- [Ralph Loop](nodejs/ralph-loop.md): 构建自主的AI编码循环，每次迭代都使用新鲜上下文，支持规划/构建模式和背压控制。
- [错误处理](nodejs/error-handling.md): 优雅地处理错误，包括连接失败、超时和清理操作。
- [多会话管理](nodejs/multiple-sessions.md): 同时管理多个独立对话。
- [本地文件管理](nodejs/managing-local-files.md): 利用AI驱动的分组策略按元数据组织文件。
- [Pull Request 可视化](nodejs/pr-visualization.md): 使用 GitHub MCP Server 生成交互式 Pull Request 年龄图表。
- [会话持久化](nodejs/persisting-sessions.md): 在重启之间保存并恢复会话。

### Python

- [Ralph Loop](python/ralph-loop.md): 构建自主的AI编码循环，每次迭代都使用新鲜上下文，支持规划/构建模式和背压控制。
- [错误处理](python/error-handling.md): 优雅地处理错误，包括连接失败、超时和清理操作。
- [多会话管理](python/multiple-sessions.md): 同时管理多个独立对话。
- [本地文件管理](python/managing-local-files.md): 利用AI驱动的分组策略按元数据组织文件。
- [Pull Request 可视化](python/pr-visualization.md): 使用 GitHub MCP Server 生成交互式 Pull Request 年龄图表。
- [会话持久化](python/persisting-sessions.md): 在重启之间保存并恢复会话。

### Go

- [Ralph Loop](go/ralph-loop.md): 构建自主的AI编码循环，每次迭代都使用新鲜上下文，支持规划/构建模式和背压控制。
- [错误处理](go/error-handling.md): 优雅地处理错误，包括连接失败、超时和清理操作。
- [多会话管理](go/multiple-sessions.md): 同时管理多个独立对话。
- [本地文件管理](go/managing-local-files.md): 利用AI驱动的分组策略按元数据组织文件。
- [Pull Request 可视化](go/pr-visualization.md): 使用 GitHub MCP Server 生成交互式 Pull Request 年龄图表。
- [会话持久化](go/persisting-sessions.md): 在重启之间保存并恢复会话。

## 如何使用

- 浏览上方对应语言的章节并打开食谱链接
- 每个食谱包含可在 `recipe/` 子文件夹中运行的示例，配有语言特定的工具
- 查看现有示例和测试以获取工作参考：
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

- 通过在您语言的 `cookbook/` 文件夹中创建 markdown 文件，并在 `recipe/` 文件夹中添加可运行示例，提出或添加新食谱
- 请遵循 [CONTRIBUTING.md](../../CONTRIBUTING.md) 中的仓库指南

## 状态

实用指南结构已完整，包含所有4种支持语言的6个食谱。每个食谱均包含markdown文档说明和可运行示例。

# GitHub Copilot SDK 食谱

本食谱集收集了小型、聚焦的示例，展示如何使用 GitHub Copilot SDK 在不同编程语言中完成常见任务。每个示例都经过刻意设计，简短且实用，包含可直接复制粘贴的代码片段，并指向完整的示例和测试。

## 按语言分类的食谱

### .NET (C#)

- [错误处理](dotnet/error-handling.md): 包括连接失败、超时和清理在内的优雅错误处理。
- [管理多个会话](dotnet/multiple-sessions.md): 同时管理多个独立对话。
- [管理本地文件](dotnet/managing-local-files.md): 使用 AI 驱动的分组策略按元数据组织文件。
- [PR 可视化](dotnet/pr-visualization.md): 使用 GitHub MCP Server 生成交互式 PR 年龄图表。
- [会话持久化](dotnet/persisting-sessions.md): 在重启之间保存并恢复会话。

### Node.js / TypeScript

- [错误处理](nodejs/error-handling.md): 包括连接失败、超时和清理在内的优雅错误处理。
- [管理多个会话](nodejs/multiple-sessions.md): 同时管理多个独立对话。
- [管理本地文件](nodejs/managing-local-files.md): 使用 AI 驱动的分组策略按元数据组织文件。
- [PR 可视化](nodejs/pr-visualization.md): 使用 GitHub MCP Server 生成交互式 PR 年龄图表。
- [会话持久化](nodejs/persisting-sessions.md): 在重启之间保存并恢复会话。

### Python

- [错误处理](python/error-handling.md): 包括连接失败、超时和清理在内的优雅错误处理。
- [管理多个会话](python/multiple-sessions.md): 同时管理多个独立对话。
- [管理本地文件](python/managing-local-files.md): 使用 AI 驱动的分组策略按元数据组织文件。
- [PR 可视化](python/pr-visualization.md): 使用 GitHub MCP Server 生成交互式 PR 年龄图表。
- [会话持久化](python/persisting-sessions.md): 在重启之间保存并恢复会话。

### Go

- [错误处理](go/error-handling.md): 包括连接失败、超时和清理在内的优雅错误处理。
- [管理多个会话](go/multiple-sessions.md): 同时管理多个独立对话。
- [管理本地文件](go/managing-local-files.md): 使用 AI 驱动的分组策略按元数据组织文件。
- [PR 可视化](go/pr-visualization.md): 使用 GitHub MCP Server 生成交互式 PR 年龄图表。
- [会话持久化](go/persisting-sessions.md): 在重启之间保存并恢复会话。

## 如何使用

- 浏览上方对应语言的章节并打开食谱链接
- 每个食谱包含可在 `recipe/` 子文件夹中运行的示例，使用特定语言的工具链
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

- 通过在对应语言的 `cookbook/` 文件夹中创建 markdown 文件并添加可运行的示例来提议或添加新食谱
- 遵循 [CONTRIBUTING.md](../../CONTRIBUTING.md) 中的仓库指引

## 状态

食谱结构已完善，包含所有四种支持语言的四份食谱。每份食谱均包含 markdown 文档说明和可运行的示例。

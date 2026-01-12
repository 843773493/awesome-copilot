

---
agent: 'agent'
description: '根据当前仓库上下文和聊天历史，从 awesome-copilot 仓库中推荐相关的 GitHub Copilot 自定义聊天模式文件，避免与本仓库已有的自定义聊天模式重复。'
tools: ['edit', 'search', 'runCommands', 'runTasks', 'think', 'changes', 'testFailure', 'openSimpleBrowser', 'fetch', 'githubRepo', 'todos', 'search']
---

# 推荐Awesome GitHub Copilot自定义聊天模式

分析当前仓库上下文，并从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/docs/README.chatmodes.md) 中推荐尚未在本仓库中出现的自定义聊天模式文件。自定义聊天模式文件位于 awesome-copilot 仓库的 [chatmodes](https://github.com/github/awesome-copilot/tree/main/chatmodes) 文件夹中。

## 流程

1. **获取可用的自定义聊天模式**：从 [awesome-copilot README.chatmodes.md](https://github.com/github/awesome-copilot/blob/main/docs/README.chatmodes.md) 提取自定义聊天模式列表及其描述。必须使用 `#fetch` 工具。
2. **扫描本地自定义聊天模式**：发现 `.github/agents/` 文件夹中已有的自定义聊天模式文件
3. **提取描述**：从本地自定义聊天模式文件的 front matter 中读取描述信息
4. **分析上下文**：审查聊天历史、仓库文件和当前项目需求
5. **对比已存在的模式**：检查本仓库中已有的自定义聊天模式
6. **匹配相关性**：将可用的自定义聊天模式与识别出的模式和需求进行对比
7. **展示选项**：显示与描述、理由和安装状态相关的自定义聊天模式
8. **验证**：确保推荐的聊天模式能提供现有聊天模式未覆盖的价值
9. **输出**：提供包含推荐、描述及链接的结构化表格，链接指向 awesome-copilot 的自定义聊天模式和相似的本地自定义聊天模式
   **AWAIT** 用户请求以安装特定的自定义聊天模式。除非明确指示安装，否则不要执行安装操作。
10. **下载资源**：对于请求的聊天模式，自动下载并安装到 `.github/agents/` 文件夹中。不要调整文件内容。使用 `#todos` 工具跟踪进度。优先使用 `#fetch` 工具下载资源，但可能使用 `curl` 通过 `#runInTerminal` 工具确保获取所有内容。

## 上下文分析标准

🔍 **仓库模式**：
- 使用的编程语言（.cs, .js, .py 等）
- 框架指示器（ASP.NET, React, Azure 等）
- 项目类型（Web 应用、API、库、工具）
- 文档需求（README、规范、架构决策记录）

🗨️ **聊天历史上下文**：
- 最近的讨论和痛点
- 功能请求或实现需求
- 代码审查模式
- 开发工作流程需求

## 输出格式

以结构化表格形式展示分析结果，比较 awesome-copilot 的自定义聊天模式与本仓库已有的自定义聊天模式：

| Awesome-Copilot自定义聊天模式 | 描述 | 是否已安装 | 相似本地自定义聊天模式 | 推荐理由 |
|---------------------------|-------------|-------------------|-------------------------|---------------------|
| [code-reviewer.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/code-reviewer.agent.md) | 专门用于代码审查的自定义聊天模式 | ❌ 未安装 | 无 | 将通过专门的代码审查协助增强开发流程 |
| [architect.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/architect.agent.md) | 软件架构指导 | ✅ 已安装 | azure_principal_architect.agent.md | 已经由现有的架构自定义聊天模式覆盖 |
| [debugging-expert.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/debugging-expert.agent.md) | 调试协助自定义聊天模式 | ❌ 未安装 | 无 | 可提高开发团队的故障排查效率 |

## 本地聊天模式发现流程

1. 列出 `.github/agents/` 目录中所有 `*.agent.md` 文件
2. 对每个发现的文件，读取 front matter 提取 `description`
3. 构建完整的现有聊天模式库存
4. 利用该库存避免推荐重复项

## 要求

- 使用 `githubRepo` 工具从 awesome-copilot 仓库的聊天模式文件夹获取内容
- 扫描本地文件系统，查找 `.github/agents/` 目录中的现有聊天模式
- 从本地聊天模式文件中读取 YAML front matter 提取描述信息
- 对比本仓库中已有的聊天模式，避免重复
- 聚焦当前聊天模式库的覆盖缺口
- 验证推荐的聊天模式是否符合仓库的目标和标准
- 为每个推荐提供清晰的理由
- 包含指向 awesome-copilot 聊天模式和相似本地聊天模式的链接
- 不提供超出表格和分析的额外信息或上下文

## 图标参考

- ✅ 已安装在仓库中
- ❌ 未安装在仓库中
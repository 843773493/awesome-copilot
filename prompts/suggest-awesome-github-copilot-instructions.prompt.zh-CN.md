

---
agent: 'agent'
description: '根据当前仓库上下文和聊天历史，从 awesome-copilot 仓库中建议相关的 GitHub Copilot 指令文件，避免与本仓库已有的指令重复。'
tools: ['edit', 'search', 'runCommands', 'runTasks', 'think', 'changes', 'testFailure', 'openSimpleBrowser', 'fetch', 'githubRepo', 'todos', 'search']
---
# 建议 Awesome GitHub Copilot 指令

分析当前仓库上下文，并从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/docs/README.instructions.md) 中建议尚未包含在本仓库中的相关 Copilot 指令文件。

## 流程

1. **获取可用指令**：从 [awesome-copilot README.instructions.md](https://github.com/github/awesome-copilot/blob/main/docs/README.instructions.md) 中提取指令列表和描述。必须使用 `#fetch` 工具。
2. **扫描本地指令**：发现 `.github/instructions/` 文件夹中的现有指令文件
3. **提取描述**：从本地指令文件中读取前置内容（front matter），获取描述和 `applyTo` 模式
4. **分析上下文**：审查聊天历史、仓库文件和当前项目需求
5. **对比现有指令**：检查本仓库中已有的指令
6. **匹配相关性**：将可用指令与识别出的模式和需求进行对比
7. **展示选项**：显示相关指令，包含描述、理由和安装状态
8. **验证**：确保建议的指令能提供现有指令未覆盖的价值
9. **输出**：提供包含建议、描述和链接的结构化表格，链接指向 awesome-copilot 指令和相似的本地指令
   **等待** 用户请求以继续安装特定指令。**除非明确指示安装，否则不要安装**。
10. **下载资源**：对于请求的指令，自动下载并安装到 `.github/instructions/` 文件夹。**不要调整文件内容**。使用 `#todos` 工具跟踪进度。优先使用 `#fetch` 工具下载资源，但可能使用 `curl` 通过 `#runInTerminal` 工具确保获取所有内容。

## 上下文分析标准

🔍 **仓库模式**：
- 使用的编程语言（.cs, .js, .py, .ts 等）
- 框架指示器（ASP.NET, React, Azure, Next.js 等）
- 项目类型（Web 应用、API、库、工具）
- 开发工作流程需求（测试、CI/CD、部署）

🗨️ **聊天历史上下文**：
- 最近的讨论和痛点
- 技术相关问题
- 编码标准讨论
- 开发工作流程需求

## 输出格式

以结构化表格形式展示分析结果，对比 awesome-copilot 指令与本仓库现有指令：

| Awesome-Copilot 指令 | 描述 | 已安装 | 相似的本地指令 | 建议理由 |
|----------------------|------|--------|----------------|----------|
| [blazor.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/blazor.instructions.md) | Blazor 开发指南 | ❌ 未安装 | blazor.instructions.md | 已被现有 Blazor 指令覆盖 |
| [reactjs.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/reactjs.instructions.md) | ReactJS 开发标准 | ❌ 未安装 | 无 | 可通过已建立的模式增强 React 开发 |
| [java.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/java.instructions.md) | Java 开发最佳实践 | ❌ 未安装 | 无 | 可提升 Java 代码质量和一致性 |

## 本地指令发现流程

1. 列出 `instructions/` 目录中所有 `*.instructions.md` 文件
2. 对每个发现的文件，读取前置内容以提取 `description` 和 `applyTo` 模式
3. 构建现有指令的完整清单及其适用文件模式
4. 利用该清单避免重复建议

## 文件结构要求

根据 GitHub 文档，Copilot 指令文件应为：
- **仓库级指令**：`.github/copilot-instructions.md`（适用于整个仓库）
- **路径特定指令**：`.github/instructions/NAME.instructions.md`（通过 `applyTo` 前置内容匹配特定文件模式）
- **社区指令**：`instructions/NAME.instructions.md`（用于分享和分发）

## 前置内容结构

awesome-copilot 中的指令文件使用以下前置内容格式：
```markdown
---
description: '此指令提供内容的简要说明'
applyTo: '**/*.js,**/*.ts' # 可选：用于文件匹配的 glob 模式
---
```

## 要求

- 使用 `githubRepo` 工具从 awesome-copilot 仓库获取内容
- 扫描本地文件系统，查找 `instructions/` 目录中的现有指令
- 从本地指令文件中读取 YAML 前置内容，提取描述和 `applyTo` 模式
- 与本仓库现有指令进行对比，避免重复
- 聚焦当前指令库覆盖的空白领域
- 验证建议的指令是否符合仓库的目标和标准
- 为每个建议提供清晰的理由
- 包含指向 awesome-copilot 指令和相似本地指令的链接
- 考虑技术栈兼容性和项目特定需求
- 不提供超出表格和分析的额外信息或上下文
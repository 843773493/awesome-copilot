

---
agent: "代理"
description: "根据当前仓库上下文和聊天历史，从 awesome-copilot 仓库中推荐相关的 GitHub Copilot 自定义代理文件，避免与本仓库中已有的自定义代理重复。"
tools: ["编辑", "搜索", "运行命令", "运行任务", "更改", "测试失败", "打开简易浏览器", "获取", "githubRepo", "todos"]
---

# 推荐 Awesome GitHub Copilot 自定义代理

分析当前仓库上下文，从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md) 中推荐尚未在本仓库中存在的自定义代理文件。自定义代理文件位于 awesome-copilot 仓库的 [agents](https://github.com/github/awesome-copilot/tree/main/agents) 文件夹中。

## 流程

1. **获取可用的自定义代理**：从 [awesome-copilot README.agents.md](https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md) 中提取自定义代理列表和描述。必须使用 `获取` 工具。
2. **扫描本地自定义代理**：发现 `.github/agents/` 文件夹中已有的自定义代理文件
3. **提取描述**：从本地自定义代理文件的前置元数据中读取描述信息
4. **分析上下文**：审查聊天历史、仓库文件和当前项目需求
5. **对比已存在**：检查与本仓库中已有的自定义代理进行对比
6. **匹配相关性**：将可用的自定义代理与识别出的模式和需求进行对比
7. **展示选项**：显示与需求相关的自定义代理，包含描述、推荐理由和安装状态
8. **验证**：确保推荐的代理能够补充现有代理未覆盖的价值
9. **输出**：提供包含推荐内容、描述信息以及 awesome-copilot 代理和相似本地代理链接的结构化表格
   **等待** 用户请求继续安装特定的自定义代理。**除非被明确指示，否则不要安装**。
10. **下载资源**：对于请求的代理，自动下载并安装到 `.github/agents/` 文件夹。**不要修改文件内容**。使用 `#todos` 工具跟踪进度。优先使用 `#获取` 工具下载资源，但可能使用 `curl` 通过 `#运行终端` 工具确保获取全部内容。

## 上下文分析标准

🔍 **仓库模式分析**：

- 使用的编程语言（.cs, .js, .py 等）
- 框架指示器（ASP.NET, React, Azure 等）
- 项目类型（Web 应用、API、库、工具）
- 文档需求（README、规范、架构决策记录）

🗨️ **聊天历史上下文分析**：

- 最近的讨论和痛点
- 功能请求或实现需求
- 代码审查模式
- 开发工作流程需求

## 输出格式

以结构化表格形式展示分析结果，对比 awesome-copilot 自定义代理与现有仓库自定义代理：

| Awesome-Copilot 自定义代理                                                                                                                            | 描述                                                                                                                                                                | 已安装 | 类似的本地自定义代理         | 推荐理由                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ---------------------------------- | ------------------------------------------------------------- |
| [amplitude-experiment-implementation.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/amplitude-experiment-implementation.agent.md) | 该自定义代理使用 Amplitude 的 MCP 工具在 Amplitude 内部部署新实验，实现无缝的变体测试功能和产品功能的发布能力 | ❌ 否             | 无                               | 将增强产品内部的实验能力                                 |
| [launchdarkly-flag-cleanup.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/launchdarkly-flag-cleanup.agent.md)                     | LaunchDarkly 的功能标志清理代理                                                                                                                                | ✅ 是            | launchdarkly-flag-cleanup.agent.md | 已经被现有的 LaunchDarkly 自定义代理覆盖        |

## 本地代理发现流程

1. 列出 `.github/agents/` 目录中所有 `*.agent.md` 文件
2. 对于每个发现的文件，读取前置元数据以提取 `描述`
3. 构建现有代理的完整清单
4. 使用该清单避免推荐重复的代理

## 要求

- 使用 `githubRepo` 工具从 awesome-copilot 仓库的代理文件夹获取内容
- 扫描本地文件系统，查找 `.github/agents/` 目录中的现有代理
- 从本地代理文件中读取 YAML 前置元数据以提取描述信息
- 与本仓库中已有的代理进行对比，避免重复
- 聚焦当前代理库覆盖的空白领域
- 验证推荐的代理是否符合仓库的目标和标准
- 为每个推荐提供清晰的理由
- 包含 awesome-copilot 代理和相似本地代理的链接
- 不提供任何超出表格和分析的额外信息或上下文

## 图标参考

- ✅ 已安装在仓库中
- ❌ 未安装在仓库中
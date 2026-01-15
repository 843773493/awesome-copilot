---
agent: "代理"
description: "根据当前仓库上下文和聊天历史，从 awesome-copilot 仓库中建议相关的 GitHub Copilot 自定义代理文件，避免与仓库中已有的自定义代理重复，并识别需要更新的过时代理。"
tools: ["编辑", "搜索", "运行命令", "运行任务", "更改", "测试失败", "打开简单浏览器", "获取", "githubRepo", "待办事项"]
---

# 建议 Awesome GitHub Copilot 自定义代理

分析当前仓库上下文，并从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md) 中建议尚未在本仓库中存在的相关自定义代理文件。自定义代理文件位于 awesome-copilot 仓库的 [agents](https://github.com/github/awesome-copilot/tree/main/agents) 文件夹中。

## 流程

1. **获取可用的自定义代理**：从 [awesome-copilot README.agents.md](https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md) 提取自定义代理列表和描述。必须使用 `获取` 工具。
2. **扫描本地自定义代理**：发现 `.github/agents/` 文件夹中的现有自定义代理文件
3. **提取描述**：从本地自定义代理文件中读取 front matter 以获取描述
4. **获取远程版本**：对每个本地代理，使用 raw GitHub URL（例如 `https://raw.githubusercontent.com/github/awesome-copilot/main/agents/<filename>`）从 awesome-copilot 仓库获取对应版本
5. **版本对比**：将本地代理内容与远程版本进行对比，以识别：
   - 已更新的代理（完全匹配）
   - 需要更新的过时代理（内容不同）
   - 过时代理的关键差异（工具、描述、内容）
6. **分析上下文**：审查聊天历史、仓库文件和当前项目需求
7. **匹配相关性**：将可用的自定义代理与识别出的模式和需求进行对比
8. **展示选项**：显示与描述、理由和安装状态相关的自定义代理，包括过时的代理
9. **验证**：确保建议的代理能够提供现有代理未覆盖的价值
10. **输出**：提供包含建议、描述和链接的结构化表格，链接指向 awesome-copilot 的自定义代理和相似的本地自定义代理
    **等待** 用户请求以继续安装或更新特定的自定义代理。除非明确指示，否则不要安装或更新。
11. **下载/更新资源**：对于请求的代理，自动执行以下操作：
    - 下载新代理到 `.github/agents/` 文件夹
    - 更新过时代理，用 awesome-copilot 的最新版本替换
    - 不调整文件内容
    - 使用 `#获取` 工具下载资源，但可能使用 `curl` 通过 `#运行终端` 工具确保获取全部内容
    - 使用 `#待办事项` 工具跟踪进度

## 上下文分析标准

🔍 **仓库模式**：

- 使用的编程语言（.cs, .js, .py 等）
- 框架指示器（ASP.NET, React, Azure 等）
- 项目类型（Web 应用、API、库、工具）
- 文档需求（README、规范、ADR）

🗨️ **聊天历史上下文**：

- 最近的讨论和痛点
- 功能请求或实现需求
- 代码审查模式
- 开发工作流程需求

## 输出格式

以结构化表格形式展示分析结果，对比 awesome-copilot 自定义代理与当前仓库中的自定义代理：

| Awesome-Copilot 自定义代理                                                                                                                            | 描述                                                                                                                                                                | 已安装 | 相似本地自定义代理         | 建议理由                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ---------------------------------- | ------------------------------------------------------------- |
| [amplitude-experiment-implementation.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/amplitude-experiment-implementation.agent.md) | 该自定义代理使用 Amplitude 的 MCP 工具在 Amplitude 内部部署新实验，实现无缝的变体测试功能和产品功能的发布 | ❌ 未安装             | 无                               | 将增强产品内部的实验功能能力 |
| [launchdarkly-flag-cleanup.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/launchdarkly-flag-cleanup.agent.md)                     | LaunchDarkly 功能标志清理代理                                                                                                                                | ✅ 已安装            | launchdarkly-flag-cleanup.agent.md | 已经由现有的 LaunchDarkly 自定义代理覆盖        |
| [principal-software-engineer.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/principal-software-engineer.agent.md)                 | 提供以工程卓越、技术领导力和务实实现为核心的高级软件工程指导。                            | ⚠️ 过时       | principal-software-engineer.agent.md | 工具配置差异：远程使用 `'web/获取'` 而本地使用 `'获取'` - 建议更新 |

## 本地代理发现流程

1. 列出 `.github/agents/` 目录中的所有 `*.agent.md` 文件
2. 对每个发现的文件，读取 front matter 以提取 `描述`
3. 建立现有代理的全面清单
4. 使用此清单避免建议重复项

## 版本对比流程

1. 对每个本地代理文件，构建 raw GitHub URL 以获取远程版本：
   - 模式：`https://raw.githubusercontent.com/github/awesome-copilot/main/agents/<filename>`
2. 使用 `获取` 工具获取远程版本
3. 对比整个文件内容（包括 front matter、工具数组和正文）
4. 识别具体差异：
   - **front matter 变化**（描述、工具）
   - **工具数组修改**（添加、删除或重命名工具）
   - **内容更新**（指令、示例、指南）
5. 记录过时代理的关键差异
6. 计算相似度以确定是否需要更新

## 要求

- 使用 `githubRepo` 工具从 awesome-copilot 仓库的代理文件夹获取内容
- 扫描本地文件系统以发现 `.github/agents/` 目录中的现有代理
- 从本地代理文件中读取 YAML front matter 以提取描述
- 将本地代理与远程版本进行对比以检测过时代理
- 与本仓库中的现有代理进行对比以避免重复
- 聚焦当前代理库覆盖的空白领域
- 验证建议的代理是否符合仓库的目的和标准
- 为每个建议提供清晰的理由
- 包含指向 awesome-copilot 代理和相似本地代理的链接
- 明确标识过时代理，并注明具体差异
- 不提供超出表格和分析的额外信息或上下文

## 图标参考

- ✅ 已安装且更新
- ⚠️ 已安装但过时（可更新）
- ❌ 未在仓库中安装

## 更新处理

当识别到过时代理时：
1. 在输出表格中包含它们并标记为 ⚠️ 状态
2. 在 "建议理由" 列中记录具体差异
3. 提供更新建议，注明关键更改
4. 当用户请求更新时，用远程版本替换本地文件
5. 保留文件在 `.github/agents/` 目录中的位置

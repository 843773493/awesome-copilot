

---
agent: '代理'
description: '根据当前仓库上下文和聊天历史，从 awesome-copilot 仓库中建议相关的 GitHub Copilot 提示文件，避免与仓库中已有的提示重复。'
tools: ['编辑', '搜索', '运行命令', '运行任务', '思考', '更改', '测试失败', '打开简单浏览器', '获取', 'githubRepo', '待办事项', '搜索']
---
# 建议出色的 GitHub Copilot 提示

分析当前仓库上下文，并从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/docs/README.prompts.md) 中建议尚未在本仓库中存在的相关提示文件。

## 流程

1. **获取可用提示**：从 [awesome-copilot README.prompts.md](https://github.com/github/awesome-copilot/blob/main/docs/README.prompts.md) 提取提示列表和描述。必须使用 `#fetch` 工具。
2. **扫描本地提示**：发现 `.github/prompts/` 文件夹中的现有提示文件
3. **提取描述**：从本地提示文件中读取前置内容（front matter）以获取描述
4. **分析上下文**：审查聊天历史、仓库文件和当前项目需求
5. **对比现有提示**：检查与本仓库中已有的提示文件的匹配情况
6. **匹配相关性**：将可用提示与识别出的模式和需求进行对比
7. **展示选项**：显示相关提示及其描述、理由和安装状态
8. **验证**：确保建议的提示能够补充现有提示未覆盖的价值
9. **输出**：提供包含建议、描述和链接的结构化表格，链接指向 awesome-copilot 提示和相似的本地提示
   **等待** 用户请求以继续安装特定提示。除非被明确指示，否则不要安装。
10. **下载资源**：对于请求的提示，自动下载并安装到 `.github/prompts/` 文件夹。不要更改文件内容。使用 `#todos` 工具跟踪进度。优先使用 `#fetch` 工具下载资源，但可能使用 `curl` 通过 `#runInTerminal` 工具确保所有内容被获取。

## 上下文分析标准

🔍 **仓库模式**：
- 使用的编程语言（.cs, .js, .py 等）
- 框架标识（ASP.NET, React, Azure 等）
- 项目类型（Web 应用、API、库、工具）
- 文档需求（README、规范、架构决策记录）

🗨️ **聊天历史上下文**：
- 最近的讨论和痛点
- 功能请求或实现需求
- 代码审查模式
- 开发工作流程需求

## 输出格式

以结构化表格形式展示 awesome-copilot 提示与仓库中现有提示的对比分析结果：

| GitHub Copilot 提示 | 描述 | 已安装 | 相似的本地提示 | 建议理由 |
|----------------------|------|--------|----------------|----------|
| [code-review.md](https://github.com/github/awesome-copilot/blob/main/prompts/code-review.md) | 自动化代码审查提示 | ❌ 未安装 | 无 | 可通过标准化代码审查流程提升开发工作流 |
| [documentation.md](https://github.com/github/awesome-copilot/blob/main/prompts/documentation.md) | 生成项目文档 | ✅ 已安装 | create_oo_component_documentation.prompt.md | 已被现有文档提示覆盖 |
| [debugging.md](https://github.com/github/awesome-copilot/blob/main/prompts/debugging.md) | 调试辅助提示 | ❌ 未安装 | 无 | 可提高开发团队的故障排查效率 |

## 本地提示发现流程

1. 列出 `.github/prompts/` 文件夹中所有 `*.prompt.md` 文件
2. 对于每个发现的文件，读取前置内容（front matter）以提取 `description`
3. 构建现有提示的完整清单
4. 利用该清单避免重复建议

## 要求

- 使用 `githubRepo` 工具从 awesome-copilot 仓库获取内容
- 扫描本地文件系统以发现 `.github/prompts/` 目录中的现有提示
- 从本地提示文件中读取 YAML 前置内容以提取描述
- 与本仓库中的现有提示进行对比以避免重复
- 聚焦于当前提示库覆盖的空白领域
- 验证建议的提示是否符合仓库的目的和标准
- 为每个建议提供清晰的理由
- 包含指向 awesome-copilot 提示和相似本地提示的链接
- 不提供超出表格和分析的任何额外信息或上下文

## 图标参考

- ✅ 已安装在仓库中
- ❌ 未安装在仓库中
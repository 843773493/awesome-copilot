---
agent: 'agent'
description: '根据当前仓库上下文和聊天历史，从 awesome-copilot 仓库中推荐相关的 GitHub Copilot 提示文件，避免与仓库中已有的提示文件重复，并识别需要更新的过时提示文件。'
tools: ['编辑', '搜索', '运行命令', '运行任务', '思考', '更改', '测试失败', '打开简单浏览器', 'web/获取', 'githubRepo', '待办事项', '搜索']
---
# 推荐优秀的 GitHub Copilot 提示文件

分析当前仓库上下文，并从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/docs/README.prompts.md) 中推荐尚未在本仓库中提供的相关提示文件。

## 流程

1. **获取可用提示文件**：从 [awesome-copilot README.prompts.md](https://github.com/github/awesome-copilot/blob/main/docs/README.prompts.md) 提取提示文件列表和描述。必须使用 `#fetch` 工具。
2. **扫描本地提示文件**：发现 `.github/prompts/` 文件夹中的现有提示文件
3. **提取描述信息**：从本地提示文件的前置内容中读取描述信息
4. **获取远程版本**：对每个本地提示文件，使用原始 GitHub URL（例如 `https://raw.githubusercontent.com/github/awesome-copilot/main/prompts/<filename>`）从 awesome-copilot 仓库获取对应的版本
5. **版本对比**：将本地提示文件内容与远程版本进行对比，以识别：
   - 已更新的提示文件（内容完全匹配）
   - 已过时的提示文件（内容存在差异）
   - 过时提示文件的关键差异（工具、描述、内容）
6. **分析上下文**：审查聊天历史、仓库文件和当前项目需求
7. **对比现有内容**：检查与本仓库中已有的提示文件的匹配情况
8. **匹配相关性**：将可用提示文件与识别出的模式和需求进行对比
9. **展示选项**：显示相关提示文件，包括描述、推荐理由和安装状态（包括过时提示文件）
10. **验证**：确保推荐的提示文件能够提供现有提示文件未覆盖的价值
11. **输出**：提供一个结构化的表格，包含推荐内容、描述信息以及指向 awesome-copilot 提示文件和相似本地提示文件的链接
    **等待** 用户请求以执行特定提示文件的安装或更新。**除非明确指示，否则不要安装或更新**。
12. **下载/更新资源**：对于请求的提示文件，自动执行以下操作：
    - 将新提示文件下载到 `.github/prompts/` 文件夹
    - 通过 awesome-copilot 仓库的最新版本更新过时提示文件
    - **不要修改文件内容**
    - 使用 `#fetch` 工具下载资源，但可能使用 `curl` 工具（通过 `#runInTerminal` 工具）以确保获取全部内容
    - 使用 `#todos` 工具跟踪进度

## 上下文分析标准

🔍 **仓库模式分析**：
- 使用的编程语言（如 .cs、.js、.py 等）
- 框架指示器（如 ASP.NET、React、Azure 等）
- 项目类型（Web 应用、API、库、工具）
- 文档需求（README、规范、架构决策记录）

🗨️ **聊天历史上下文**：
- 最近的讨论和痛点
- 功能请求或实现需求
- 代码审查模式
- 开发工作流程需求

## 输出格式

以结构化表格形式展示分析结果，对比 awesome-copilot 提示文件与本仓库已有的提示文件：

| awesome-copilot 提示文件 | 描述 | 已安装 | 相似本地提示文件 | 推荐理由 |
|-------------------------|-------------|-------------------|---------------------|---------------------|
| [code-review.prompt.md](https://github.com/github/awesome-copilot/blob/main/prompts/code-review.prompt.md) | 自动化代码审查提示文件 | ❌ 未安装 | 无 | 将通过标准化的代码审查流程增强开发工作流程 |
| [documentation.prompt.md](https://github.com/github/awesome-copilot/blob/main/prompts/documentation.prompt.md) | 生成项目文档 | ✅ 已安装 | create_oo_component_documentation.prompt.md | 已被现有文档提示文件覆盖 |
| [debugging.prompt.md](https://github.com/github/awesome-copilot/blob/main/prompts/debugging.prompt.md) | 调试辅助提示文件 | ⚠️ 过时 | debugging.prompt.md | 工具配置存在差异：远程使用 `'codebase'`，本地缺失 - 推荐更新 |

## 本地提示文件发现流程

1. 列出 `.github/prompts/` 目录中所有 `*.prompt.md` 文件
2. 对每个发现的文件，读取前置内容以提取 `description`
3. 构建完整的现有提示文件清单
4. 利用该清单避免推荐重复的提示文件

## 版本对比流程

1. 对每个本地提示文件，构建原始 GitHub URL 以获取远程版本：
   - 格式：`https://raw.githubusercontent.com/github/awesome-copilot/main/prompts/<filename>`
2. 使用 `#fetch` 工具获取远程版本
3. 对比整个文件内容（包括前置内容和正文）
4. 识别具体差异：
   - **前置内容变更**（描述、工具、模式）
   - **工具数组修改**（添加、删除或重命名工具）
   - **内容更新**（指令、示例、指南）
5. 记录过时提示文件的关键差异
6. 计算相似度以确定是否需要更新

## 要求

- 使用 `githubRepo` 工具从 awesome-copilot 仓库的提示文件夹获取内容
- 扫描本地文件系统以发现 `.github/prompts/` 目录中的现有提示文件
- 从本地提示文件中读取 YAML 前置内容以提取描述信息
- 对比本地提示文件与远程版本，以检测过时的提示文件
- 对比本仓库中已有的提示文件以避免重复
- 聚焦当前提示库覆盖范围的空白
- 验证推荐的提示文件是否符合仓库的目的和标准
- 为每个推荐提供清晰的理由
- 包含指向 awesome-copilot 提示文件和相似本地提示文件的链接
- 明确标识过时的提示文件，并注明具体差异
- 不提供超出表格和分析内容的任何额外信息或上下文

## 图标参考

- ✅ 已安装且最新
- ⚠️ 已安装但过时（有更新可用）
- ❌ 未安装在仓库中

## 更新处理

当识别到过时的提示文件时：
1. 在输出表格中标记为 ⚠️ 状态
2. 在“推荐理由”列中记录具体差异
3. 提供更新建议，注明关键变更
4. 当用户请求更新时，将本地文件替换为远程版本
5. 保留文件在 `.github/prompts/` 目录中的位置

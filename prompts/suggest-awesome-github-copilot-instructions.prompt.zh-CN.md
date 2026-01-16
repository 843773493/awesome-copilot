---
agent: 'agent'
description: '根据当前仓库上下文和聊天历史，从 awesome-copilot 仓库中建议相关的 GitHub Copilot 指导文件，避免与本仓库已有的指导文件重复，并识别需要更新的过时指导文件。'
tools: ['edit', 'search', 'runCommands', 'runTasks', 'think', 'changes', 'testFailure', 'openSimpleBrowser', 'web/fetch', 'githubRepo', 'todos', 'search']
---
# 建议优秀的 GitHub Copilot 指导文件

分析当前仓库上下文，并从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/docs/README.instructions.md) 中建议尚未在本仓库中包含的相关 Copilot 指导文件。

## 流程

1. **获取可用的指导文件**：从 [awesome-copilot README.instructions.md](https://github.com/github/awesome-copilot/blob/main/docs/README.instructions.md) 提取指导文件列表和描述。必须使用 `#fetch` 工具。
2. **扫描本地指导文件**：发现 `.github/instructions/` 文件夹中已有的指导文件
3. **提取描述**：从本地指导文件中读取前置内容（front matter），获取描述和 `applyTo` 模式
4. **获取远程版本**：对每个本地指导文件，使用原始 GitHub URL（例如 `https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/<filename>`）从 awesome-copilot 仓库获取对应版本
5. **版本对比**：将本地指导文件内容与远程版本进行对比，识别以下情况：
   - 内容与当前一致的指导文件（精确匹配）
   - 内容过时的指导文件（内容差异）
   - 过时指导文件的关键差异（描述、applyTo 模式、内容）
6. **分析上下文**：审查聊天历史、仓库文件和当前项目需求
7. **对比已存在的指导文件**：检查本仓库中已有的指导文件
8. **匹配相关性**：将可用的指导文件与识别出的模式和需求进行对比
9. **展示选项**：显示相关指导文件，包括描述、建议理由以及是否已存在的状态（包括过时的指导文件）
10. **验证**：确保建议的指导文件能提供现有指导文件未涵盖的价值
11. **输出**：提供包含建议、描述、以及指向 awesome-copilot 指导文件和类似本地指导文件的链接的结构化表格
   **AWAIT** 用户请求以继续安装或更新特定指导文件。除非被明确指示，否则不要进行安装或更新。
12. **下载/更新资产**：对于请求的指导文件，自动执行以下操作：
    - 将新指导文件下载到 `.github/instructions/` 文件夹
    - 通过替换 awesome-copilot 的最新版本来更新过时的指导文件
    - 不要调整文件内容
    - 使用 `#fetch` 工具下载资产，但可能使用 `curl` 通过 `#runInTerminal` 工具确保获取全部内容
    - 使用 `#todos` 工具跟踪进度

## 上下文分析标准

🔍 **仓库模式**：
- 使用的编程语言（.cs, .js, .py, .ts 等）
- 框架标识（ASP.NET, React, Azure, Next.js 等）
- 项目类型（Web 应用、API、库、工具）
- 开发工作流程需求（测试、CI/CD、部署）

🗨️ **聊天历史上下文**：
- 最近的讨论和痛点
- 技术相关的提问
- 编码规范的讨论
- 开发工作流程需求

## 输出格式

以结构化表格形式展示分析结果，对比 awesome-copilot 指导文件与本仓库已有的指导文件：

| awesome-copilot 指导文件 | 描述 | 已安装 | 类似本地指导文件 | 建议理由 |
|---------------------------|------|--------|------------------|----------|
| [blazor.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/blazor.instructions.md) | Blazor 开发指南 | ✅ 是 | blazor.instructions.md | 已被现有 Blazor 指导文件覆盖 |
| [reactjs.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/reactjs.instructions.md) | ReactJS 开发标准 | ❌ 否 | 无 | 可通过已建立的模式增强 React 开发 |
| [java.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/java.instructions.md) | Java 开发最佳实践 | ⚠️ 过时 | java.instructions.md | applyTo 模式差异：远程使用 `'**/*.java'`，本地使用 `'*.java'` - 建议更新 |

## 本地指导文件发现流程

1. 列出 `instructions/` 目录下所有 `*.instructions.md` 文件
2. 对每个发现的文件，读取前置内容以提取 `description` 和 `applyTo` 模式
3. 构建现有指导文件的完整清单及其适用文件模式
4. 使用该清单避免建议重复的指导文件

## 版本对比流程

1. 对每个本地指导文件，构建原始 GitHub URL 以获取远程版本：
   - 模式：`https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/<filename>`
2. 使用 `#fetch` 工具获取远程版本
3. 对比整个文件内容（包括前置内容和正文）
4. 识别具体差异：
   - **前置内容变更**（描述、applyTo 模式）
   - **内容更新**（指南、示例、最佳实践）
5. 记录过时指导文件的关键差异
6. 计算相似度以确定是否需要更新

## 文件结构要求

根据 GitHub 文档，Copilot 指导文件应满足以下结构要求：
- **仓库级指导文件**：`.github/copilot-instructions.md`（适用于整个仓库）
- **路径特定指导文件**：`.github/instructions/NAME.instructions.md`（通过 `applyTo` 前置内容匹配特定文件模式）
- **社区指导文件**：`instructions/NAME.instructions.md`（用于分享和分发）

## 前置内容结构

awesome-copilot 中的指导文件使用以下前置内容格式：
```markdown
---
description: '此指导文件提供的简要描述'
applyTo: '**/*.js,**/*.ts' # 可选：用于文件匹配的通配符模式
---
```

## 要求

- 使用 `githubRepo` 工具从 awesome-copilot 仓库的指导文件目录获取内容
- 扫描本地文件系统，查找 `.github/instructions/` 目录中已有的指导文件
- 从本地指导文件中读取 YAML 前置内容，提取描述和 `applyTo` 模式
- 对比本地指导文件与远程版本，检测过时的指导文件
- 对比本仓库已有的指导文件，避免重复建议
- 聚焦当前指导库覆盖范围的空白领域
- 验证建议的指导文件是否与仓库的目标和标准一致
- 为每个建议提供清晰的理由
- 包含指向 awesome-copilot 指导文件和类似本地指导文件的链接
- 明确标识过时的指导文件，并注明具体差异
- 考虑技术栈兼容性及项目特定需求
- 不提供超出表格和分析之外的额外信息或上下文

## 图标参考

- ✅ 已安装且最新
- ⚠️ 已安装但过时（有更新可用）
- ❌ 未安装在仓库中

## 更新处理

当识别到过时的指导文件时：
1. 在输出表格中包含这些文件并标记为 ⚠️ 状态
2. 在 "建议理由" 列中记录具体差异
3. 提供更新建议，并注明关键变更
4. 当用户请求更新时，将本地文件替换为远程版本
5. 保留文件在 `.github/instructions/` 目录中的位置



---
agent: 'agent'
description: '根据当前仓库上下文和聊天历史，从 awesome-copilot 仓库中推荐相关的 GitHub Copilot 收藏集，并提供自动下载和安装收藏集资源的功能。'
tools: ['edit', 'search', 'runCommands', 'runTasks', 'think', 'changes', 'testFailure', 'openSimpleBrowser', 'fetch', 'githubRepo', 'todos', 'search']
---
# 推荐优秀的 GitHub Copilot 收藏集

分析当前仓库上下文，从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/docs/README.collections.md) 中推荐相关的收藏集，以增强该仓库的开发流程。

## 流程

1. **获取可用的收藏集**：从 [awesome-copilot README.collections.md](https://github.com/github/awesome-copilot/blob/main/docs/README.collections.md) 中提取收藏集列表和描述。必须使用 `#fetch` 工具。
2. **扫描本地资源**：发现 `prompts/` 目录中的提示文件、`instructions/` 目录中的指令文件以及 `agents/` 目录中的聊天模式。
3. **提取本地描述**：从本地资源文件中读取前置内容（front matter），以了解现有功能。
4. **分析仓库上下文**：回顾聊天历史、仓库文件、编程语言、框架和当前项目需求。
5. **匹配收藏集相关性**：将可用收藏集与识别出的模式和需求进行比较。
6. **检查资源重叠**：对于相关的收藏集，分析其各个项目以避免与现有仓库资源重复。
7. **展示收藏集选项**：显示与描述、项目数量和推荐理由相关的收藏集。
8. **提供使用指导**：解释安装的收藏集如何增强开发流程。
   **等待** 用户请求安装特定收藏集。**除非明确指示**，否则不要安装。
9. **下载资源**：对于请求安装的收藏集，自动下载并安装每个单独的资源（提示、指令、聊天模式）到相应的目录。**不要修改文件内容**。优先使用 `#fetch` 工具下载资源，但可以使用 `curl` 通过 `#runInTerminal` 工具确保所有内容被获取。

## 上下文分析标准

🔍 **仓库模式**：
- 使用的编程语言（.cs, .js, .py, .ts, .bicep, .tf 等）
- 框架指示器（ASP.NET, React, Azure, Next.js, Angular 等）
- 项目类型（Web 应用、API、库、工具、基础设施）
- 文档需求（README、规格说明、架构决策记录）
- 开发流程指示器（CI/CD、测试、部署）

🗨️ **聊天历史上下文**：
- 最近的讨论和痛点
- 功能请求或实现需求
- 代码审查模式和质量担忧
- 开发流程需求和挑战
- 技术栈和架构决策

## 输出格式

以结构化表格展示分析结果，显示相关收藏集及其潜在价值：

### 收藏集推荐

| 收藏集名称 | 描述 | 项目数 | 资源重叠 | 推荐理由 |
|------------|------|--------|----------|----------|
| [Azure 与云开发](https://github.com/github/awesome-copilot/blob/main/collections/azure-cloud-development.md) | 包括基础设施即代码、无服务器函数、架构模式和成本优化的全面 Azure 云开发工具 | 15 个项目 | 3 个相似 | 可通过 Bicep、Terraform 和成本优化工具增强 Azure 开发流程 |
| [C# .NET 开发](https://github.com/github/awesome-copilot/blob/main/collections/csharp-dotnet-development.md) | 包括测试、文档和最佳实践的 C# 和 .NET 开发必备提示、指令和聊天模式 | 7 个项目 | 2 个相似 | 已有 .NET 相关资源覆盖，但包含高级测试模式 |
| [测试与测试自动化](https://github.com/github/awesome-copilot/blob/main/collections/testing-automation.md) | 用于编写测试、测试自动化和测试驱动开发的全面收藏集 | 11 个项目 | 1 个相似 | 可通过 TDD 指导和自动化工具显著提升测试实践 |

### 推荐收藏集的资源分析

对每个推荐的收藏集，分解其单独的资源：

**Azure 与云开发收藏集分析**：
- ✅ **新增资源 (12)**：Azure 成本优化提示、Bicep 规划模式、AVM 模块、Logic Apps 专家模式
- ⚠️ **相似资源 (3)**：Azure DevOps 管道（与现有 CI/CD 相似）、Terraform（基础重叠）、容器化（已覆盖 Docker 基础）
- 🎯 **高价值资源**：成本优化工具、基础设施即代码专家能力、Azure 特定的架构指导

**安装预览**：
- 将安装到 `prompts/`：4 个 Azure 相关提示
- 将安装到 `instructions/`：6 个基础设施和 DevOps 最佳实践
- 将安装到 `agents/`：5 个专门的 Azure 专家模式

## 本地资源发现流程

1. **扫描资源目录**：
   - 列出 `prompts/` 目录中的所有 `*.prompt.md` 文件
   - 列出 `instructions/` 目录中的所有 `*.instructions.md` 文件
   - 列出 `agents/` 目录中的所有 `*.agent.md` 文件

2. **提取资源元数据**：对于每个发现的文件，读取 YAML 前置内容（front matter）以提取：
   - `description` - 主要用途和功能
   - `tools` - 所需工具和能力
   - `mode` - 运行模式（用于提示）
   - `model` - 具体模型需求（用于聊天模式）

3. **构建资源清单**：创建一个全面的现有能力地图，按以下分类组织：
   - **技术重点**：编程语言、框架、平台
   - **流程类型**：开发、测试、部署、文档、规划
   - **专业化程度**：通用型 vs. 专门的专家模式

4. **识别覆盖缺口**：将现有资源与以下内容进行比较：
   - 仓库技术栈需求
   - 聊天历史中显示的开发流程需求
   - 已识别项目类型的行业最佳实践
   - 缺失的专业能力领域（安全、性能、架构等）

## 收藏集资源下载流程

当用户确认安装收藏集时：

1. **获取收藏集清单**：从 awesome-copilot 仓库获取收藏集 YAML
2. **下载单独资源**：对于每个收藏集中的项目：
   - 从 GitHub 仓库下载原始文件内容
   - 验证文件格式和前置内容结构
   - 检查命名规范的合规性
3. **安装到相应目录**：
   - `*.prompt.md` 文件 → `prompts/` 目录
   - `*.instructions.md` 文件 → `instructions/` 目录
   - `*.agent.md` 文件 → `agents/` 目录
4. **避免重复**：跳过与现有本地资源高度相似的文件
5. **报告安装**：提供安装资源的摘要和使用说明

## 要求

- 使用 `fetch` 工具从 awesome-copilot 仓库获取收藏集数据
- 使用 `githubRepo` 工具获取单独资源内容以进行下载
- 扫描本地文件系统，查找 `prompts/`、`instructions/` 和 `agents/` 目录中的现有资源
- 从本地资源文件中读取 YAML 前置内容，提取描述和能力
- 将收藏集与仓库上下文进行比较，以识别相关的匹配项
- 专注于填补能力缺口的收藏集，而不是重复现有资源
- 验证建议的收藏集是否符合仓库的技术栈和开发需求
- 为每个收藏集建议提供清晰的理由和具体优势
- 启用收藏集资源的自动下载和安装到相应目录
- 确保下载的资源遵循仓库的命名规范和格式标准
- 提供使用指导，解释收藏集如何增强开发流程
- 包含 awesome-copilot 收藏集和收藏集内资源的链接

## 收藏集安装流程

1. **用户确认收藏集**：用户选择特定的收藏集进行安装
2. **获取收藏集清单**：从 awesome-copilot 仓库下载 YAML 清单
3. **资源下载循环**：对于收藏集中的每个资源：
   - 从 GitHub 仓库下载原始内容
   - 验证文件格式和结构
   - 检查与现有本地资源的显著重叠
   - 安装到相应目录（`prompts/`、`instructions/` 或 `agents/`）
4. **安装摘要**：报告安装的资源及其使用说明
5. **流程增强指南**：解释收藏集如何提升开发能力

## 安装后指导

安装收藏集后，提供以下内容：
- **资源概览**：已安装的提示、指令和聊天模式列表
- **使用示例**：如何激活和使用每种类型的资源
- **流程整合**：将资源整合到开发流程中的最佳实践
- **定制技巧**：如何根据特定项目需求修改资源
- **相关收藏集**：建议与当前收藏集协同工作的互补收藏集
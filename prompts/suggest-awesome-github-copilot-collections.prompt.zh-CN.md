---
agent: '代理'
description: '根据当前仓库上下文和聊天历史，从 awesome-copilot 仓库中推荐相关的 GitHub Copilot 集合，提供自动下载和安装集合资源，并识别需要更新的过时资源。'
tools: ['编辑', '搜索', '运行命令', '运行任务', '思考', '更改', '测试失败', '打开简单浏览器', 'web/fetch', 'githubRepo', '待办事项', '搜索']
---
# 推荐优秀的 GitHub Copilot 集合

分析当前仓库上下文，从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/docs/README.collections.md) 中推荐能够增强该仓库开发流程的集合。

## 流程

1. **获取可用集合**：从 [awesome-copilot README.collections.md](https://github.com/github/awesome-copilot/blob/main/docs/README.collections.md) 提取集合列表和描述。必须使用 `#fetch` 工具。
2. **扫描本地资源**：发现 `prompts/` 目录中的提示文件、`instructions/` 目录中的指令文件以及 `agents/` 目录中的聊天模式文件
3. **提取本地描述**：从本地资源文件中读取前置内容，了解现有功能
4. **获取远程版本**：对于每个与集合项匹配的本地资源，使用 raw GitHub URLs（例如 `https://raw.githubusercontent.com/github/awesome-copilot/main/<类型>/<文件名>`）从 awesome-copilot 仓库获取对应的版本
5. **版本对比**：对比本地资源内容与远程版本，识别：
   - 已更新的资源（完全匹配）
   - 过时的资源（内容不同）
   - 过时资源的关键差异（工具、描述、内容）
6. **分析仓库上下文**：查看聊天历史、仓库文件、编程语言、框架和当前项目需求
7. **匹配集合相关性**：将可用集合与识别出的模式和需求进行对比
8. **检查资源重叠**：对于相关集合，分析每个项目以避免与现有仓库资源重复
9. **展示集合选项**：显示相关集合及其潜在价值，包括描述、项目数量、资源重叠情况和推荐理由
10. **提供使用指导**：解释安装的集合如何增强开发流程
    **等待** 用户请求以继续安装或更新特定集合。除非被明确指示，否则不要安装或更新。
11. **下载/更新资源**：对于请求安装的集合，自动执行以下操作：
    - 将新资源下载到适当目录
    - 通过 awesome-copilot 获取最新版本以更新过时资源
    - **不要** 修改文件内容
    - 使用 `#fetch` 工具下载资源，但可能使用 `curl` 通过 `#runInTerminal` 工具确保获取全部内容

## 上下文分析标准

🔍 **仓库模式分析**：
- 使用的编程语言（.cs, .js, .py, .ts, .bicep, .tf 等）
- 框架指示符（ASP.NET, React, Azure, Next.js, Angular 等）
- 项目类型（Web 应用、API、库、工具、基础设施）
- 文档需求（README、规范、ADR、架构决策）
- 开发流程指示符（CI/CD、测试、部署）

🗨️ **聊天历史上下文**：
- 最近的讨论和痛点
- 功能请求或实现需求
- 代码审查模式和质量关注点
- 开发流程需求和挑战
- 技术栈和架构决策

## 输出格式

以结构化表格展示分析结果，显示相关集合及其潜在价值：

### 集合推荐

| 集合名称 | 描述 | 项目数量 | 资源重叠 | 推荐理由 |
|----------|------|----------|----------|----------|
| [Azure & Cloud Development](https://github.com/github/awesome-copilot/blob/main/collections/azure-cloud-development.md) | 包括基础设施即代码、无服务器函数、架构模式和成本优化的全面 Azure 云开发工具 | 15 个项目 | 3 个相似 | 可以通过 Bicep、Terraform 和成本优化工具增强 Azure 开发流程 |
| [C# .NET Development](https://github.com/github/awesome-copilot/blob/main/collections/csharp-dotnet-development.md) | 包括测试、文档和最佳实践的 C# 和 .NET 开发必备提示、指令和聊天模式 | 7 个项目 | 2 个相似 | 已经由现有 .NET 相关资源覆盖，但包含高级测试模式 |
| [Testing & Test Automation](https://github.com/github/awesome-copilot/blob/main/collections/testing-automation.md) | 用于编写测试、测试自动化和测试驱动开发的全面集合 | 11 个项目 | 1 个相似 | 可以通过 TDD 指导和自动化工具显著提升测试实践 |

### 推荐集合的资源分析

对每个建议的集合，分解其单独的资源：

**Azure & Cloud Development 集合分析**：
- ✅ **新增资源（12）**：Azure 成本优化提示、Bicep 规划模式、AVM 模块、Logic Apps 专家模式
- ⚠️ **相似资源（3）**：Azure DevOps 管道（与现有 CI/CD 相似）、Terraform（基础重叠）、容器化（Docker 基础已覆盖）
- 🔄 **过时资源（2）**：azure-iac-generator.agent.md（工具已更新）、bicep-implement.agent.md（描述已更改）
- 🎯 **高价值**：成本优化工具、基础设施即代码专业知识、Azure 特定的架构指导

**安装预览**：
- 将安装到 `prompts/`：4 个 Azure 相关提示
- 将安装到 `instructions/`：6 个基础设施和 DevOps 最佳实践
- 将安装到 `agents/`：5 个专门的 Azure 专家模式

## 本地资源发现流程

1. **扫描资源目录**：
   - 列出 `prompts/` 目录中的所有 `*.prompt.md` 文件
   - 列出 `instructions/` 目录中的所有 `*.instructions.md` 文件
   - 列出 `agents/` 目录中的所有 `*.agent.md` 文件

2. **提取资源元数据**：对于每个发现的文件，读取 YAML 前置内容以提取：
   - `description` - 主要用途和功能
   - `tools` - 所需工具和能力
   - `mode` - 运行模式（用于提示）
   - `model` - 用于聊天模式的特定模型需求

3. **构建资源清单**：创建现有能力的全面地图，按以下分类组织：
   - **技术重点**：编程语言、框架、平台
   - **工作流程类型**：开发、测试、部署、文档、规划
   - **专业水平**：通用用途 vs. 专门的专家模式

4. **识别覆盖缺口**：将现有资源与以下内容进行对比：
   - 仓库技术栈需求
   - 聊天历史中显示的开发流程需求
   - 已识别项目类型的行业最佳实践
   - 缺失的专业领域（安全、性能、架构等）

## 版本对比流程

1. 对于每个与集合项对应的本地资源文件，构建 raw GitHub URL：
   - 代理：`https://raw.githubusercontent.com/github/awesome-copilot/main/agents/<文件名>`
   - 提示：`https://raw.githubusercontent.com/github/awesome-copilot/main/prompts/<文件名>`
   - 指令：`https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/<文件名>`
2. 使用 `#fetch` 工具获取远程版本
3. 对比整个文件内容（包括前置内容和正文）
4. 识别具体差异：
   - **前置内容更改**（描述、工具、applyTo 模式）
   - **工具数组修改**（添加、删除或重命名工具）
   - **内容更新**（指令、示例、指南）
5. 记录过时资源的关键差异
6. 计算相似度以确定是否需要更新

## 集合资源下载流程

当用户确认安装集合时：

1. **获取集合清单**：从 awesome-copilot 仓库获取集合 YAML
2. **下载单个资源**：对于集合中的每个项目：
   - 从 GitHub 仓库下载原始文件内容
   - 验证文件格式和前置内容结构
   - 检查命名规范合规性
3. **安装到适当目录**：
   - `*.prompt.md` 文件 → `prompts/` 目录
   - `*.instructions.md` 文件 → `instructions/` 目录
   - `*.agent.md` 文件 → `agents/` 目录
4. **避免重复**：跳过与现有资源高度相似的文件
5. **报告安装**：提供安装的资源列表和使用说明

## 要求

- 使用 `fetch` 工具从 awesome-copilot 仓库获取集合数据
- 使用 `githubRepo` 工具获取单个资源内容以供下载
- 扫描本地文件系统以查找 `prompts/`、`instructions/` 和 `agents/` 目录中的现有资源
- 从本地资源文件中读取 YAML 前置内容以提取描述和功能
- 将集合与仓库上下文对比以识别相关匹配
- 聚焦于填补功能缺口而非重复现有资源的集合
- 验证建议的集合是否与仓库的技术栈和开发需求一致
- 为每个集合建议提供清晰的理由和具体好处
- 启用集合资源的自动下载和安装到适当目录
- 确保下载的资源遵循仓库的命名规范和格式标准
- 提供使用指导，解释集合如何增强开发流程
- 包含 awesome-copilot 集合和集合内资源的链接

## 集合安装流程

1. **用户确认安装集合**：用户选择特定集合进行安装
2. **获取集合清单**：从 awesome-copilot 仓库下载 YAML 清单
3. **资源下载循环**：对于集合中的每个资源：
   - 从 GitHub 仓库下载原始内容
   - 验证文件格式和结构
   - 检查与现有本地资源的显著重叠
   - 安装到适当目录（`prompts/`、`instructions/` 或 `agents/`）
4. **安装摘要**：报告已安装的资源及其使用说明
5. **工作流程增强指南**：解释集合如何提升开发能力

## 安装后指导

安装集合后，提供以下内容：
- **资源概览**：已安装的提示、指令和聊天模式列表
- **使用示例**：如何激活和使用每种类型的资源
- **工作流程整合**：将资源整合到开发流程的最佳实践
- **定制技巧**：如何根据特定项目需求修改资源
- **相关集合**：推荐能良好配合的互补集合

## 图标参考

- ✅ 推荐安装的集合 / 资源已更新
- ⚠️ 集合存在部分资源重叠但仍有价值
- ❌ 不推荐的集合（显著重叠或不相关）
- 🎯 填补主要功能缺口的高价值集合
- 📁 集合部分安装（因重复跳过部分资源）
- 🔄 资源过时（可从 awesome-copilot 更新）

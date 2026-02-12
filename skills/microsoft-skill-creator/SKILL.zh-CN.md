---
name: microsoft-skill-creator
description: 使用 Learn MCP 工具为 Microsoft 技术创建代理技能。当用户希望创建一个教授代理有关任何 Microsoft 技术、库、框架或服务（如 Azure、.NET、M365、VS Code、Bicep 等）的技能时使用。深入调查主题，然后生成一个混合技能，该技能在本地存储核心知识，同时支持动态的 Learn MCP 深度查询。
context: fork
compatibility: 需要 Microsoft Learn MCP 服务器 (https://learn.microsoft.com/api/mcp)
---

# Microsoft 技能创建器

创建混合技能，用于 Microsoft 技术，这些技能在本地存储核心知识，同时支持动态的 Learn MCP 查询以获取更深入的信息。

## 关于技能

技能是模块化包，通过扩展代理的能力来提供专业知识和工作流程。一个技能将通用代理转变为针对特定领域的专业代理。

### 技能结构

```
skill-name/
├── SKILL.md (必需)     # 前置信息（名称、描述）+ 指令
├── references/             # 按需加载的文档
├── sample_codes/           # 可运行的代码示例
└── assets/                 # 输出中使用的文件（模板等）
```

### 核心原则

- **前置信息至关重要**：`name` 和 `description` 决定技能何时触发——请明确且全面
- **简洁是关键**：仅包含代理尚未掌握的内容；共享上下文窗口
- **避免重复**：信息存在于 SKILL.md 或参考文件中，而非两者皆有

## Learn MCP 工具

| 工具 | 目的 | 使用时机 |
|------|---------|-------------|
| `microsoft_docs_search` | 搜索官方文档 | 第一阶段发现，查找主题 |
| `microsoft_docs_fetch` | 获取完整页面内容 | 深入研究重要页面 |
| `microsoft_code_sample_search` | 查找代码示例 | 获取实现模式 |

## 创建流程

### 步骤 1：深入调查主题

使用 Learn MCP 工具进行三阶段深入理解：

**阶段 1 - 范围发现：**
```
microsoft_docs_search(query="{technology} overview what is")
microsoft_docs_search(query="{technology} concepts architecture")
microsoft_docs_search(query="{technology} getting started tutorial")
```

**阶段 2 - 核心内容：**
```
microsoft_docs_fetch(url="...")  # 从阶段 1 获取页面
microsoft_code_sample_search(query="{technology}", language="{lang}")
```

**阶段 3 - 深度：**
```
microsoft_docs_search(query="{technology} best practices")
microsoft_docs_search(query="{technology} troubleshooting errors")
```

#### 调查检查清单

调查完成后，请验证：
- [ ] 能否用一段话解释该技术的作用
- [ ] 识别出 3-5 个关键概念
- [ ] 具备基础使用的可运行代码
- [ ] 了解最常见的 API 模式
- [ ] 具备深入主题的搜索查询

### 步骤 2：与用户确认

展示调查结果并询问：
1. "我找到了这些关键领域：[列表]。哪些最为重要？"
2. "代理将主要使用此技能执行哪些任务？"
3. "代码示例应优先选择哪种编程语言？"

### 步骤 3：生成技能

从 [skill-templates.md](references/skill-templates.md) 使用适当的模板：

| 技术类型 | 模板 |
|-----------------|----------|
| 客户端库、NuGet/npm 包 | SDK/Library |
| Azure 资源 | Azure 服务 |
| 应用开发框架 | 框架/平台 |
| REST API、协议 | API/协议 |

#### 生成的技能结构

```
{skill-name}/
├── SKILL.md                    # 核心知识 + Learn MCP 指南
├── references/                 # 本地详细文档（如需要）
└── sample_codes/               # 可运行的代码示例
    ├── getting-started/
    │   └── hello-kernel.cs
    └── common-patterns/
        ├── chat-completion.cs
        └── function-calling.cs
```

### 步骤 4：平衡本地与动态内容

**本地存储时：**
- 基础知识（任何任务都需要）
- 高频访问
- 稳定（不会改变）
- 通过搜索难以找到

**保留动态时：**
- 完整参考（太大）
- 版本特定
- 情境相关（仅特定任务）
- 被良好索引（易于搜索）

#### 内容指南

| 内容类型 | 本地 | 动态 |
|--------------|-------|---------|
| 核心概念（3-5 个） | ✅ 完整 | |
| "Hello World" 代码 | ✅ 完整 | |
| 常见模式（3-5 个） | ✅ 完整 | |
| 最常用 API 方法 | 签名 + 示例 | 通过 fetch 获取完整文档 |
| 最佳实践 | 前 5 个要点 | 通过搜索获取更多信息 |
| 故障排除 | | 搜索查询 |
| 完整 API 参考 | | 文档链接 |

### 步骤 5：验证

1. 审查：本地内容是否足以完成常见任务？
2. 测试：建议的搜索查询是否返回有用结果？
3. 验证：代码示例是否能无错误运行？

## 常见调查模式

### 用于 SDKs/库
```
"{name} overview" → 目的、架构
"{name} getting started quickstart" → 设置步骤
"{name} API reference" → 核心类/方法
"{name} samples examples" → 代码模式
"{name} best practices performance" → 优化
```

### 用于 Azure 服务
```
"{service} overview features" → 功能
"{service} quickstart {language}" → 设置代码
"{service} REST API reference" → 接口点
"{service} SDK {language}" → 客户端库
"{service} pricing limits quotas" → 限制
```

### 用于框架/平台
```
"{framework} architecture concepts" → 认知模型
"{framework} project structure" → 项目结构规范
"{framework} tutorial walkthrough" → 全流程引导
"{framework} configuration options" → 自定义选项
```

## 示例：创建 "语义内核" 技能

### 调查

```
microsoft_docs_search(query="semantic kernel overview")
microsoft_docs_search(query="semantic kernel plugins functions")
microsoft_code_sample_search(query="semantic kernel", language="csharp")
microsoft_docs_fetch(url="https://learn.microsoft.com/semantic-kernel/overview/")
```

### 生成的技能

```
semantic-kernel/
├── SKILL.md
└── sample_codes/
    ├── getting-started/
    │   └── hello-kernel.cs
    └── common-patterns/
        ├── chat-completion.cs
        └── function-calling.cs
```

### 生成的 SKILL.md

```markdown
---
name: semantic-kernel
description: 使用 Microsoft 语义内核构建 AI 代理。适用于基于 LLM 的应用，包含插件、规划器和内存功能的 .NET 或 Python 应用。
---

# 语义内核

用于将 LLM 集成到应用程序中的编排 SDK，支持插件、规划器和内存功能。

## 关键概念

- **内核**：管理 AI 服务和插件的核心编排器
- **插件**：AI 可调用的功能集合
- **规划器**：按顺序调用插件功能以实现目标
- **内存**：向量存储集成，用于 RAG 模式

## 快速入门

查看 [getting-started/hello-kernel.cs](sample_codes/getting-started/hello-kernel.cs)

## 进一步学习

| 主题 | 如何查找 |
|-------|-------------|
| 插件开发 | `microsoft_docs_search(query="semantic kernel plugins custom functions")` |
| 规划器 | `microsoft_docs_search(query="semantic kernel planner")` |
| 内存 | `microsoft_docs_fetch(url="https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-memory")` |
```

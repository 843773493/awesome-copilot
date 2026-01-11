# 为 Awesome GitHub Copilot 做出贡献

感谢您对为 Awesome GitHub Copilot 仓库做出贡献感兴趣！我们欢迎来自社区的贡献，以帮助扩展我们的自定义指令和提示词集合。

## 如何贡献

### 添加指令

指令有助于为特定技术、编码实践或领域自定义 GitHub Copilot 的行为。

1. **创建指令文件**：在 `instructions/` 目录中添加新的 `.md` 文件
2. **遵循命名约定**：使用描述性、小写的文件名，用连字符分隔（例如 `python-django.instructions.md`）
3. **组织您的内容**：以清晰的标题开头，逻辑地组织您的指令
4. **测试您的指令**：确保您的指令在 GitHub Copilot 中工作良好

#### 指令格式示例

```markdown
---
description: '为特定技术和实践自定义 GitHub Copilot 行为的指令'
---

# 您的技术/框架名称

## 指令

- 为 GitHub Copilot 提供清晰、具体的指导
- 包括最佳实践和约定
- 使用项目符号以便阅读

## 其他指导

- 任何额外的上下文或示例
```

### 添加提示词

提示词是针对特定开发场景和任务的即用型模板。

1. **创建提示词文件**：在 `prompts/` 目录中添加新的 `.prompt.md` 文件
2. **遵循命名约定**：使用描述性、小写的文件名，用连字符分隔，并使用 `.prompt.md` 扩展名（例如 `react-component-generator.prompt.md`）
3. **包含前言**：在文件顶部添加元数据（可选但推荐）
4. **组织您的提示词**：提供清晰的上下文和具体的指令

#### 提示词格式示例

```markdown
---
agent: 'agent'
tools: ['codebase', 'terminalCommand']
description: '此提示词做什么的简要描述'
---

# 提示词标题

您的目标是...

## 具体指令

- 清晰、可操作的指令
- 在有帮助的地方包括示例
```

### 添加聊天模式

聊天模式是专业配置，将 GitHub Copilot Chat 转换为特定领域助手或针对特定开发场景的角色。

1. **创建聊天模式文件**：在 `agents/` 目录中添加新的 `.agent.md` 文件
2. **遵循命名约定**：使用描述性、小写的文件名，用连字符分隔，并使用 `.agent.md` 扩展名（例如 `react-performance-expert.agent.md`）
3. **包含前言**：在文件顶部使用必需字段添加元数据
4. **定义角色**：为聊天模式创建清晰的身份和专业领域
5. **测试聊天模式**：确保聊天模式在其领域中提供有帮助和准确的响应

#### 聊天模式格式示例

```markdown
---
description: '聊天模式及其目的的简要描述'
model: 'gpt-5'
tools: ['codebase', 'terminalCommand']
---

# 聊天模式标题

您是具有[特定领域]深入知识的专业[领域/角色]。

## 您的专业知识

- [特定技能 1]
- [特定技能 2]
- [特定技能 3]

## 您的方法

- [您如何帮助用户]
- [您的沟通风格]
- [您优先考虑的事项]

## 指导原则

- [响应的具体指令]
- [约束或限制]
- [要遵循的最佳实践]
```

### 添加技能

技能是 `skills/` 目录中的自包含文件夹，包含 `SKILL.md` 文件（带前言）和可选的捆绑资源。

1. **创建新技能文件夹**：运行 `npm run skill:create -- --name <skill-name> --description "<skill description>"`
2. **编辑 `SKILL.md`**：确保 `name` 与文件夹名称匹配（小写，用连字符分隔），并且 `description` 清晰、非空
3. **添加可选资源**：将捆绑资源保持合理大小（每个文件不超过 5MB），并从 `SKILL.md` 引用它们
4. **验证和更新文档**：运行 `npm run skill:validate` 然后 `npm run build` 更新生成的 README 表格

### 添加集合

集合将相关的提示词、指令和聊天模式围绕特定主题或工作流进行分组，使用户更容易发现和采用综合工具包。

1. **创建集合清单**：在 `collections/` 目录中添加新的 `.collection.yml` 文件
2. **遵循命名约定**：使用描述性、小写的文件名，用连字符分隔（例如 `python-web-development.collection.yml`）
3. **引用现有项目**：集合应仅引用仓库中已存在的文件
4. **测试您的集合**：验证所有引用的文件都存在并能良好协作

#### 创建集合

```bash
# 使用创建脚本
node create-collection.js my-collection-id

# 或使用 VS Code 任务：Ctrl+Shift+P > "Tasks: Run Task" > "create-collection"
```

#### 集合格式示例

```yaml
id: my-collection-id
name: 我的集合名称
description: 此集合提供什么的简要描述以及谁应该使用它。
tags: [tag1, tag2, tag3] # 可选的发现标签
items:
  - path: prompts/my-prompt.prompt.md
    kind: prompt
  - path: instructions/my-instructions.instructions.md
    kind: instruction
  - path: agents/my-chatmode.agent.md
    kind: agent
    usage: |
     recommended # 或 "optional" 如果对工作流不是必需的

     此聊天模式需要以下指令/提示词/MCP：
      - 指令 1
      - 提示词 1
      - MCP 1

     此聊天模式适合...
      - 使用案例 1
      - 使用案例 2
    
      以下是如何使用它的示例：
      ```markdown, task-plan.prompt.md
      ---
      mode: task-planner
      title: 规划 Microsoft Fabric 实时智能 Terraform 支持
      ---
      #file: <文件包含在聊天上下文中>
      执行操作以实现目标。
      ```

      为获得最佳结果，请考虑...
      - 建议 1
      - 建议 2
    
display:
  ordering: alpha # 或 "manual" 保留上面的顺序
  show_badge: false # 设置为 true 以显示集合徽章
```

完整示例请查看 edge-ai 任务集合：

- [edge-ai-tasks.collection.yml](./collections/edge-ai-tasks.collection.yml)
- [edge-ai-tasks.md](./collections/edge-ai-tasks.md)

#### 集合指导原则

- **专注于工作流**：分组为特定用例工作的项目
- **合理规模**：通常 3-10 个项目效果很好
- **测试组合**：确保项目相互补充有效
- **清晰目的**：集合应解决特定问题或工作流
- **提交前验证**：运行 `node validate-collections.js` 确保您的清单有效

## 提交您的贡献

1. **Fork 本仓库**
2. **为您的贡献创建新分支**
3. **按照上述指导添加您的指令、提示词文件、聊天模式或集合**
4. **运行更新脚本**：`npm start` 使用您的新文件更新 README（如果您还没有运行过 `npm install` 请先运行）
   - GitHub Actions 工作流将验证此步骤已执行
   - 如果运行脚本会修改 README.md，PR 检查将失败并显示注释，显示所需的更改
5. **提交拉取请求**，包括：
   - 清晰的标题描述您的贡献
   - 您的指令/提示词做什么的简要描述
   - 任何相关的上下文或使用说明

**注意**：贡献合并后，您将自动添加到我们的 [贡献者](./README.md#贡献者-) 部分！我们使用 [all-contributors](https://github.com/all-contributors/all-contributors) 来认可项目的所有类型的贡献。

## 我们接受什么

我们欢迎涵盖任何技术、框架或开发实践的贡献，以帮助开发者更有效地使用 GitHub Copilot。这包括：

- 编程语言和框架
- 开发方法论和最佳实践
- 架构模式和设计原则
- 测试策略和质量保证
- DevOps 和部署实践
- 可访问性和包容性设计
- 性能优化技术

## 我们不接受什么

为了维护一个安全、负责任和建设性的社区，我们将**不接受**以下贡献：

- **违反负责任的 AI 原则**：试图绕过 Microsoft/GitHub 负责任 AI 指导原则或促进有害 AI 使用的内容
- **危害安全性**：旨在绕过安全政策、利用漏洞或削弱系统安全的指令
- **启用恶意活动**：旨在伤害其他系统、用户或组织的内容
- **利用弱点**：利用其他平台或服务中漏洞的指令
- **推广有害内容**：可能导致创建有害、歧视或不适当内容的指导
- **规避平台政策**：试图绕过 GitHub、Microsoft 或其他平台的服务条款

## 质量指导原则

- **具体明确**：具体、可操作的指导比通用指令更有帮助
- **测试您的内容**：确保您的指令或提示词在 GitHub Copilot 中工作良好
- **遵循约定**：使用一致的格式和命名
- **保持专注**：每个文件应解决特定的技术、框架或使用案例
- **清晰书写**：使用简单、直接的语言
- **推广最佳实践**：鼓励安全、可维护和符合伦理的开发实践

## 贡献者认可

本项目使用 [all-contributors](https://github.com/all-contributors/all-contributors) 来认可贡献者。当您做出贡献时，您将自动在我们的贡献者列表中被认可！

我们欢迎所有类型的贡献，包括：

- 📝 文档改进
- 💻 代码贡献
- 🐛 Bug 报告和修复
- 🎨 设计改进
- 💡 想法和建议
- 🤔 回答问题
- 📢 推广项目

您的贡献帮助整个 GitHub Copilot 社区更好地利用这个资源！

## 行为准则

请注意，本项目与 [贡献者行为准则](CODE_OF_CONDUCT.md) 一起发布。通过参与此项目，您同意遵守其条款。

## 许可证

通过贡献到本仓库，您同意您的贡献将在 MIT 许可证下授权。

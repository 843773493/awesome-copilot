# 为Awesome GitHub Copilot做贡献

感谢您对贡献Awesome GitHub Copilot仓库的兴趣！我们欢迎社区的贡献，以帮助扩展我们自定义指令和提示的集合。

## 如何做贡献

### 添加指令

指令有助于针对特定技术、编码实践或领域自定义GitHub Copilot的行为。

1. **创建您的指令文件**：在`instructions/`目录下添加一个新的`.md`文件
2. **遵循命名规范**：使用描述性的、小写的文件名并用短横线分隔（例如：`python-django.instructions.md`）
3. **组织您的内容**：以清晰的标题开头，逻辑性地组织您的指令
4. **测试您的指令**：确保您的指令与GitHub Copilot良好配合

#### 指令格式示例

```markdown
---
description: '针对特定技术和实践自定义GitHub Copilot行为的指令'
---

# 您的技术/框架名称

## 指令

- 为GitHub Copilot提供清晰、具体的指导
- 包含最佳实践和惯例
- 使用项目符号便于阅读

## 额外指南

- 任何额外的上下文或示例
```

### 添加提示

提示是针对特定开发场景和任务的即用模板。

1. **创建您的提示文件**：在`prompts/`目录下添加一个新的`.prompt.md`文件
2. **遵循命名规范**：使用描述性的、小写的文件名并用短横线分隔，且带有`.prompt.md`扩展名（例如：`react-component-generator.prompt.md`）
3. **包含前置内容**：在文件顶部添加元数据（可选但推荐）
4. **组织您的提示**：提供清晰的上下文和具体指令

#### 提示格式示例

```markdown
---
agent: 'agent'
tools: ['codebase', 'terminalCommand']
description: '简要描述此提示的作用'
---

# 提示标题

您的目标是...

## 具体指令

- 清晰、可操作的指令
- 有帮助时包含示例
```

### 添加聊天模式

聊天模式是专门的配置，可将GitHub Copilot Chat转换为特定开发场景的领域专用助手或角色。

1. **创建您的聊天模式文件**：在`agents/`目录下添加一个新的`.agent.md`文件
2. **遵循命名规范**：使用描述性的、小写的文件名并用短横线分隔，且带有`.agent.md`扩展名（例如：`react-performance-expert.agent.md`）
3. **包含前置内容**：在文件顶部添加元数据，包含必填字段
4. **定义角色**：为聊天模式创建清晰的身份和专业知识领域
5. **测试您的聊天模式**：确保聊天模式在其领域内提供有帮助且准确的回复

#### 聊天模式格式示例

```markdown
---
description: '聊天模式的简要描述及其用途'
model: 'gpt-5'
tools: ['codebase', 'terminalCommand']
---

# 聊天模式标题

您是[领域/角色]专家，拥有[特定领域]的深入知识。

## 您的专业领域

- [特定技能1]
- [特定技能2]
- [特定技能3]

## 您的处理方式

- [您如何帮助用户]
- [您的沟通风格]
- [您优先考虑的内容]

## 指南

- [对回复的具体要求]
- [限制或约束条件]
- [应遵循的最佳实践]
```

### 添加技能

技能是位于`skills/`目录下的自包含文件夹，包含一个`SKILL.md`文件（带前置内容）和可选的捆绑资产。

1. **创建新的技能文件夹**：运行`npm run skill:create -- --name <skill-name> --description "<skill description>"` 
2. **编辑`SKILL.md`**：确保`name`与文件夹名称一致（小写并用短横线分隔），且`description`清晰且非空
3. **添加可选资产**：保持捆绑资产大小合理（每个小于5MB），并在`SKILL.md`中引用它们
4. **验证并更新文档**：运行`npm run skill:validate`然后`npm run build`以更新生成的README表格

### 添加集合

集合围绕特定主题或工作流程，将相关的提示、指令和聊天模式分组，便于用户发现和采用全面的工具包。

1. **创建您的集合清单**：在`collections/`目录下添加一个新的`.collection.yml`文件
2. **遵循命名规范**：使用描述性的、小写的文件名并用短横线分隔（例如：`python-web-development.collection.yml`）
3. **引用现有项目**：集合应仅引用仓库中已存在的文件
4. **测试您的集合**：验证所有引用的文件是否存在且能良好配合

#### 创建集合

```bash
# 使用创建脚本
node create-collection.js my-collection-id

# 或使用VS Code任务：Ctrl+Shift+P > "Tasks: Run Task" > "create-collection"
```

#### 集合格式示例

```yaml
id: my-collection-id
name: 我的集合名称
description: 简要描述此集合提供的内容及适用人群。
tags: [tag1, tag2, tag3] # 可选的发现标签
items:
  - path: prompts/my-prompt.prompt.md
    kind: prompt
  - path: instructions/my-instructions.instructions.md
    kind: instruction
  - path: agents/my-chatmode.agent.md
    kind: agent
    usage: |
     推荐 # 或 "optional"（如果对工作流程不关键）

     此聊天模式需要以下指令/提示/MCPs：
      - 指令1
      - 提示1
      - MCP 1

     此聊天模式适用于...
      - 使用场景1
      - 使用场景2

      这是使用示例：
      ```markdown, task-plan.prompt.md
      ---
      mode: task-planner
      title: 计划microsoft fabric实时智能terraform支持
      ---
      #file: <包含在聊天上下文中的文件>
      执行操作以达成目标。
      ```

      为了获得最佳效果，请考虑...
      - 提示1
      - 提示2

display:
  ordering: alpha # 或 "manual" 以保留上方的顺序
  show_badge: false # 设置为true以显示集合徽章
```

查看完整的使用示例，请参阅edge-ai tasks集合：
- [edge-ai-tasks.collection.yml](./collections/edge-ai-tasks.collection.yml)
- [edge-ai-tasks.md](./collections/edge-ai-tasks.md)

#### 集合指南

- **聚焦工作流程**：将针对特定使用场景协同工作的项目分组
- **合理大小**：通常3-10个项目效果最佳
- **测试组合**：确保项目之间能有效互补
- **明确目的**：集合应解决特定问题或工作流程
- **提交前验证**：运行`node validate-collections.js`以确保您的清单有效

## 提交您的贡献

1. ** Fork 该仓库**
2. **为您的贡献创建新分支**
3. **按照上述指南添加您的指令、提示文件、聊天模式或集合**
4. **运行更新脚本**：`npm start`以更新README并包含您的新文件（如果您尚未安装，请先运行`npm install`）
   - GitHub Actions工作流将验证此步骤是否正确执行
   - 如果运行脚本会修改README.md，PR检查将失败并附带需要修改的评论
5. **提交包含以下内容的拉取请求**：
   - 描述您贡献的清晰标题
   - 简要描述您的指令/提示的作用
   - 任何相关的上下文或使用说明

> [!注意] 
> 我们使用[all-contributors](https://github.com/all-contributors/all-contributors)来认可项目中所有类型的贡献。跳转至[贡献者认可](#contributor-recognition)以了解更多！

## 我们接受的贡献

我们欢迎所有有助于开发者更高效地使用GitHub Copilot的技术、框架或开发实践的贡献。这包括：

- 编程语言和框架
- 开发方法论和最佳实践
- 架构模式和设计原则
- 测试策略和质量保证
- DevOps和部署实践
- 可访问性和包容性设计
- 性能优化技术

## 我们不接受的贡献

为维护一个安全、负责任和建设性的社区，我们**不会接受**以下类型的贡献：

- **违反负责任的人工智能原则**：试图规避Microsoft/GitHub负责任人工智能指南或推广有害人工智能使用的相关内容
- **损害安全性**：旨在规避安全策略、利用漏洞或削弱系统安全性的指令
- **启用恶意活动**：旨在损害其他系统、用户或组织的内容
- **利用弱点**：利用其他平台或服务漏洞的指令
- **推广有害内容**：可能导致创建有害、歧视性或不适当内容的指导
- **规避平台政策**：试图绕过GitHub、Microsoft或其他平台服务条款的尝试

## 质量指南

- **具体明确**：泛用性指令不如具体、可操作的指导有用
- **测试您的内容**：确保您的指令或提示与GitHub Copilot良好配合
- **遵循惯例**：使用一致的格式和命名
- **保持聚焦**：每个文件应针对特定技术、框架或使用场景
- **清晰表达**：使用简单直接的语言
- **推广最佳实践**：鼓励安全、可维护和道德的开发实践

## 贡献者认可

我们使用[all-contributors](https://github.com/all-contributors/all-contributors)来认可本项目中**所有类型的贡献**。

要添加您的名字，请使用您的GitHub用户名和适当的贡献类型，在相关问题或拉取请求下留言：

```markdown
@all-contributors add @username for contributionType1, contributionType2
```

贡献者列表将在每个星期日的**凌晨3:00 UTC**自动更新。当下次运行完成后，您的名字将出现在[README贡献者](./README.md#contributors-)部分。

### 贡献类型

我们欢迎多种类型的贡献，包括以下自定义类别：

| 类别 | 描述 | Emoji |
| --- | --- | :---: |
| **指令** | 指导GitHub Copilot行为的自定义指令集 | 🧭 |
| **提示** | GitHub Copilot的可重用或一次性提示 | ⌨️ |
| **代理（聊天模式）** | 定义GitHub Copilot角色或个性 | 🎭 |
| **技能** | GitHub Copilot特定任务的专业知识 | 🧰 |
| **集合** | 精选的与提示、代理或指令相关的捆绑包 | 🎁 |

此外，所有由[All Contributors](https://allcontributors.org/emoji-key/)支持的标准贡献类型也受到认可。

> 每一次贡献都至关重要。感谢您帮助改进GitHub Copilot社区的资源。


## 行为准则

请注意，本项目以[贡献者行为准则](CODE_OF_CONDUCT.md)发布。参与本项目即表示您同意遵守其条款。

## 许可证

通过向本仓库提交贡献，您同意您的贡献将根据MIT许可证授权。

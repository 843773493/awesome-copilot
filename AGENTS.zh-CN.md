# AGENTS.md

## 项目概述

Awesome GitHub Copilot 仓库是一个社区驱动的自定义代理、提示和指令集合，旨在增强GitHub Copilot在各种领域、语言和用例中的使用体验。该项目包括：

- **代理** - 与MCP服务器集成的专用GitHub Copilot代理
- **提示** - 用于代码生成和问题解决的特定任务提示
- **指令** - 应用于特定文件模式的编码标准和最佳实践
- **技能** - 包含指令和捆绑资源的自包含文件夹，用于专门任务
- **钩子** - 在开发过程中由特定事件触发的自动化工作流
- **集合** - 按特定主题和工作流组织的精选资源集合

## 仓库结构

```
.
├── agents/           # 自定义GitHub Copilot代理定义（.agent.md文件）
├── prompts/          # 任务特定提示（.prompt.md文件）
├── instructions/     # 编码标准和指南（.instructions.md文件）
├── skills/           # 代理技能文件夹（每个文件夹包含SKILL.md和可选的捆绑资源）
├── hooks/            # 自动化工作流钩子（包含README.md + hooks.json的文件夹）
├── collections/      # 精选资源集合（.md文件）
├── docs/             # 不同资源类型的文档
├── eng/              # 构建和自动化脚本
└── scripts/          # 工具脚本
```

## 设置命令

```bash
# 安装依赖项
npm ci

# 构建项目（生成README.md）
npm run build

# 验证集合清单
npm run collection:validate

# 创建新集合
npm run collection:create -- --id <collection-id> --tags <tags>

# 验证代理技能
npm run skill:validate

# 创建新技能
npm run skill:create -- --name <skill-name>
```

## 开发流程

### 与代理、提示、指令、技能和钩子工作

所有代理文件（*.agent.md）、提示文件（*.prompt.md）和指令文件（*.instructions.md）必须包含正确的Markdown前置元数据。代理技能是包含SKILL.md文件的文件夹，该文件包含前置元数据和可选的捆绑资源。钩子是包含README.md（前置元数据）和hooks.json配置文件的文件夹：

#### 代理文件 (*.agent.md)
- 必须包含`description`字段（用单引号包裹）
- 文件名应为小写，单词之间用短横线分隔
- 推荐包含`tools`字段
- 强烈推荐指定`model`字段

#### 提示文件 (*.prompt.md)
- 必须包含`agent`字段（值应为'agent'，用单引号包裹）
- 必须包含非空的`description`字段（用单引号包裹）
- 文件名应为小写，单词之间用短横线分隔
- 如果适用，推荐指定`tools`字段
- 强烈推荐指定`model`字段

#### 指令文件 (*.instructions.md)
- 必须包含`description`字段（用单引号包裹，且不能为空）
- 必须包含`applyTo`字段，指定文件模式（例如：'**.js, **.ts'）
- 文件名应为小写，单词之间用短横线分隔

#### 代理技能 (skills/*/SKILL.md)
- 每个技能是一个包含SKILL.md文件的文件夹
- SKILL.md必须包含`name`字段（小写，用短横线分隔，与文件夹名称匹配，最大64个字符）
- SKILL.md必须包含`description`字段（用单引号包裹，长度为10-1024个字符）
- 文件夹名称应为小写，单词之间用短横线分隔
- 技能可以包含捆绑资源（脚本、模板、数据文件）
- 捆绑资源应在SKILL.md指令中引用
- 每个文件的资源大小应合理（小于5MB）
- 技能遵循[Agent Skills规范](https://agentskills.io/specification)

#### 钩子文件夹 (hooks/*/README.md)
- 每个钩子是一个包含README.md文件的文件夹
- README.md必须包含`name`字段（人类可读名称）
- README.md必须包含非空的`description`字段（用单引号包裹）
- 必须包含一个hooks.json文件，其中包含钩子配置（钩子事件从该文件提取）
- 文件夹名称应为小写，单词之间用短横线分隔
- 可以包含捆绑资源（脚本、工具、配置文件）
- 捆绑脚本应在README.md和hooks.json中引用
- 遵循[GitHub Copilot钩子规范](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/use-hooks)
- 可选地包含`tags`字段用于分类

### 添加新资源

当添加新的代理、提示、指令、技能或钩子时：

**对于代理、提示和指令：**
1. 创建带有正确前置元数据的文件
2. 将文件添加到相应的目录
3. 运行：`npm run build`来更新README.md
4. 验证生成的README中是否包含该资源

**对于钩子：**
1. 在`hooks/`目录下创建一个描述性的新文件夹
2. 创建带有正确前置元数据的README.md文件（名称、描述、钩子、标签）
3. 创建符合GitHub Copilot钩子规范的hooks.json文件
4. 将任何捆绑脚本或资源添加到该文件夹
5. 设置脚本为可执行：`chmod +x script.sh`
6. 运行：`npm run build`来更新README.md
7. 验证生成的README中是否包含该钩子

**对于技能：**
1. 运行`npm run skill:create`来生成新技能文件夹的框架
2. 编辑生成的SKILL.md文件，添加您的指令
3. 将任何捆绑资源（脚本、模板、数据）添加到技能文件夹
4. 运行`npm run skill:validate`来验证技能结构
5. 运行`npm run build`来更新README.md
6. 验证生成的README中是否包含该技能

### 测试指令

```bash
# 运行所有验证检查
npm run collection:validate
npm run skill:validate

# 构建并验证README生成
npm run build

# 修复行尾（提交前必需）
bash scripts/fix-line-endings.sh
```

在提交前：
- 确保所有Markdown前置元数据格式正确
- 验证所有新文件名是否遵循小写加短横线的命名规范
- 运行`npm run build`来更新README
- **始终运行`bash scripts/fix-line-endings.sh`** 以标准化行尾（CRLF → LF）
- 检查您的新资源是否在README中正确显示

## 代码风格指南

### Markdown文件
- 使用包含必要字段的正确前置元数据
- 保持描述简洁且信息丰富
- 用单引号包裹描述字段的值
- 使用小写文件名，单词之间用短横线分隔

### JavaScript/Node.js脚本
- 位于`eng/`和`scripts/`目录中
- 遵循Node.js ES模块规范（.mjs扩展名）
- 使用清晰、描述性的函数和变量名称

## 拉取请求指南

在创建拉取请求时：

1. **README更新**：新文件应在运行`npm run build`后自动添加到README中
2. **前置元数据验证**：确保所有Markdown文件包含所需的前置元数据字段
3. **文件命名**：验证所有新文件是否遵循小写加短横线的命名规范
4. **构建检查**：在提交前运行`npm run build`以验证README生成
5. **行尾标准化**：**始终运行`bash scripts/fix-line-endings.sh`** 以将行尾标准化为LF（Unix风格）
6. **描述**：提供您的代理/提示/指令的清晰描述
7. **测试**：如果添加集合，请运行`npm run collection:validate`以确保有效性

### 提交前检查清单

在提交您的PR前，请确保：
- [ ] 运行`npm install`（或`npm ci`）安装依赖项
- [ ] 运行`npm run build`生成更新后的README.md
- [ ] 运行`bash scripts/fix-line-endings.sh`以标准化行尾
- [ ] 验证所有新文件是否包含正确的前置元数据
- [ ] 测试您的贡献是否与GitHub Copilot兼容
- [ ] 检查文件名是否遵循命名规范

### 代码审查检查清单

对于提示文件 (*.prompt.md)：
- [ ] 包含Markdown前置元数据
- [ ] 包含`agent`字段（值应为'agent'，用单引号包裹）
- [ ] 包含非空的`description`字段（用单引号包裹）
- [ ] 文件名为小写，单词之间用短横线分隔
- [ ] 包含`model`字段（强烈推荐）

对于指令文件 (*.instructions.md)：
- [ ] 包含Markdown前置元数据
- [ ] 包含非空的`description`字段（用单引号包裹）
- [ ] 包含`applyTo`字段，指定文件模式
- [ ] 文件名为小写，单词之间用短横线分隔

对于代理文件 (*.agent.md)：
- [ ] 包含Markdown前置元数据
- [ ] 包含非空的`description`字段（用单引号包裹）
- [ ] 包含`name`字段，使用人类可读名称（例如："Address Comments" 而不是 "address-comments"）
- [ ] 文件名为小写，单词之间用短横线分隔
- [ ] 包含`model`字段（强烈推荐）
- [ ] 考虑使用`tools`字段

对于技能 (skills/*/)：
- [ ] 文件夹包含SKILL.md文件
- [ ] SKILL.md包含Markdown前置元数据
- [ ] 包含与文件夹名称匹配的`name`字段（小写，用短横线分隔，最大64个字符）
- [ ] 包含非空的`description`字段（用单引号包裹，长度为10-1024个字符）
- [ ] 文件夹名称为小写，单词之间用短横线分隔
- [ ] 任何捆绑资源都在SKILL.md中引用
- [ ] 捆绑资源每个文件小于5MB

对于钩子文件夹 (hooks/*/)：
- [ ] 文件夹包含带有Markdown前置元数据的README.md文件
- [ ] 包含`name`字段，使用人类可读名称
- [ ] 包含非空的`description`字段（用单引号包裹）
- [ ] 包含有效的hooks.json文件，其中包含钩子配置（钩子事件从该文件提取）
- [ ] 文件夹名称为小写，单词之间用短横线分隔
- [ ] 任何捆绑脚本都应可执行，并在README.md中引用
- [ ] 遵循[GitHub Copilot钩子规范](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/use-hooks)
- [ ] 可选地包含`tags`数组字段用于分类

## 贡献指南

这是一个社区驱动的项目。欢迎贡献！请参阅：
- [CONTRIBUTING.md](CONTRIBUTING.md) 贡献指南
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) 社区标准
- [SECURITY.md](SECURITY.md) 安全政策

## MCP服务器

该仓库包含一个MCP（模型上下文协议）服务器，可直接从该仓库搜索和安装资源。需要Docker来运行服务器。

## 许可证

MIT许可证 - 详情请参见[LICENSE](LICENSE)

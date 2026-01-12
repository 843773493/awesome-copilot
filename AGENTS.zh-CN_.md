# AGENTS.md

## 项目概述

Awesome GitHub Copilot 仓库是一个由社区驱动的自定义 Agent、提示词和指令集合，旨在在各种领域、编程语言和使用场景中增强 GitHub Copilot 的体验。该项目包括：

- **Agent** - 与 MCP 服务器集成的专业化 GitHub Copilot Agent
- **提示词** - 用于代码生成和问题解决的任务特定提示词
- **指令** - 应用于特定文件模式的编码标准和最佳实践
- **技能** - 具有指令和捆绑资源的自包含文件夹，用于专业任务
- **集合** - 围绕特定主题和工作流组织的精选集合

## 仓库结构

```
.
├── agents/           # 自定义 GitHub Copilot Agent 定义 (.agent.md 文件)
├── prompts/          # 任务特定的提示词 (.prompt.md 文件)
├── instructions/     # 编码标准和指导原则 (.instructions.md 文件)
├── skills/           # Agent 技能文件夹（每个包含 SKILL.md 和可选捆绑资源）
├── collections/      # 资源的精选集合 (.md 文件)
├── docs/             # 不同资源类型的文档
├── eng/              # 构建和自动化脚本
└── scripts/          # 实用脚本
```

## 设置命令

```bash
# 安装依赖
npm ci

# 构建项目（生成 README.md）
npm run build

# 验证集合清单
npm run collection:validate

# 创建新集合
npm run collection:create -- --id <collection-id> --tags <tags>

# 验证 Agent 技能
npm run skill:validate

# 创建新技能
npm run skill:create -- --name <skill-name>
```

## 开发工作流

### 使用 Agent、提示词、指令和技能

所有 Agent 文件 (`*.agent.md`)、提示词文件 (`*.prompt.md`) 和指令文件 (`*.instructions.md`) 必须包含适当的 Markdown 前言。Agent 技能是包含 `SKILL.md` 文件（带前言）和可选捆绑资源的文件夹：

#### Agent 文件 (*.agent.md)

- 必须有 `description` 字段（用单引号包装）
- 文件名应为小写，单词用连字符分隔
- 推荐包含 `tools` 字段
- 强烈推荐指定 `model` 字段

#### 提示词文件 (*.prompt.md)

- 必须有 `agent` 字段（值应为用单引号包装的 `'agent'`）
- 必须有 `description` 字段（用单引号包装，非空）
- 文件名应为小写，单词用连字符分隔
- 推荐在适用情况下指定 `tools`
- 强烈推荐指定 `model` 字段

#### 指令文件 (*.instructions.md)

- 必须有 `description` 字段（用单引号包装，非空）
- 必须有 `applyTo` 字段指定文件模式（例如 `'**.js, **.ts'`）
- 文件名应为小写，单词用连字符分隔

#### Agent 技能 (skills/*/SKILL.md)

- 每个技能是包含 `SKILL.md` 文件的文件夹
- SKILL.md 必须有 `name` 字段（小写，用连字符分隔，与文件夹名称匹配，最多 64 个字符）
- SKILL.md 必须有 `description` 字段（用单引号包装，10-1024 个字符）
- 文件夹名应为小写，单词用连字符分隔
- 技能可以包含捆绑资源（脚本、模板、数据文件）
- 捆绑资源应从 `SKILL.md` 引用
- 资源文件应合理大小（每个文件不超过 5MB）
- 技能遵循 [Agent 技能规范](https://agentskills.io/specification)

### 添加新资源

当添加新的 Agent、提示词、指令或技能时：

**对于 Agent、提示词和指令：**

1. 使用适当的前言创建文件
2. 将文件添加到相应的目录
3. 通过运行更新 README.md：`npm run build`
4. 验证资源是否出现在生成的 README 中

**对于技能：**

1. 运行 `npm run skill:create` 来搭建新技能文件夹
2. 编辑生成的 SKILL.md 文件，添加您的指令
3. 将任何捆绑资源（脚本、模板、数据）添加到技能文件夹
4. 运行 `npm run skill:validate` 来验证技能结构
5. 通过运行更新 README.md：`npm run build`
6. 验证技能是否出现在生成的 README 中

### 测试指令

```bash
# 运行所有验证检查
npm run collection:validate
npm run skill:validate

# 构建并验证 README 生成
npm run build

# 修复行尾（提交前必需）
bash scripts/fix-line-endings.sh
```

提交前：

- 确保所有 Markdown 前言格式正确
- 验证文件名遵循小写-用连字符分隔约定
- 运行 `npm run build` 更新 README
- **始终运行 `bash scripts/fix-line-endings.sh`** 将行尾规范化为 LF (Unix 风格)
- 检查您的新资源是否在 README 中正确显示

## 代码风格指导原则

### Markdown 文件

- 使用适当的前言和必需字段
- 保持描述简洁且信息丰富
- 用单引号包装 description 字段值
- 使用小写文件名，用连字符分隔

### JavaScript/Node.js 脚本

- 位于 `eng/` 和 `scripts/` 目录中
- 遵循 Node.js ES 模块约定（`.mjs` 扩展名）
- 使用清晰、描述性的函数和变量名

## 拉取请求指导原则

创建拉取请求时：

1. **README 更新**：当您运行 `npm run build` 时，新文件应自动添加到 README
2. **前言验证**：确保所有 Markdown 文件都有必需的前言字段
3. **文件命名**：验证所有新文件遵循小写-用连字符分隔命名约定
4. **构建检查**：在提交前运行 `npm run build` 来验证 README 生成
5. **行尾**：**始终运行 `bash scripts/fix-line-endings.sh`** 将行尾规范化为 LF (Unix 风格)
6. **描述**：提供清晰的 Agent/提示词/指令做什么的描述
7. **测试**：如果添加集合，运行 `npm run collection:validate` 确保有效性

### 提交前检查清单

在提交 PR 之前，确保您已：

- [ ] 运行 `npm install` (或 `npm ci`) 安装依赖
- [ ] 运行 `npm run build` 生成更新的 README.md
- [ ] 运行 `bash scripts/fix-line-endings.sh` 规范化行尾
- [ ] 验证所有新文件都有适当的前言
- [ ] 测试您的贡献在 GitHub Copilot 中有效
- [ ] 检查文件名遵循命名约定

### 代码审查检查清单

对于提示词文件 (*.prompt.md)：

- [ ] 有 Markdown 前言
- [ ] 有 `agent` 字段（值应为用单引号包装的 `'agent'`）
- [ ] 有非空 `description` 字段，用单引号包装
- [ ] 文件名为小写，用连字符分隔
- [ ] 包含 `model` 字段（强烈推荐）

对于指令文件 (*.instructions.md)：

- [ ] 有 Markdown 前言
- [ ] 有非空 `description` 字段，用单引号包装
- [ ] 有 `applyTo` 字段，带文件模式
- [ ] 文件名为小写，用连字符分隔

对于 Agent 文件 (*.agent.md)：

- [ ] 有 Markdown 前言
- [ ] 有非空 `description` 字段，用单引号包装
- [ ] 文件名为小写，用连字符分隔
- [ ] 包含 `model` 字段（强烈推荐）
- [ ] 考虑使用 `tools` 字段

对于技能 (skills/*/):

- [ ] 文件夹包含 SKILL.md 文件
- [ ] SKILL.md 有 Markdown 前言
- [ ] 有 `name` 字段与文件夹名称匹配（小写，用连字符分隔，最多 64 个字符）
- [ ] 有非空 `description` 字段，用单引号包装（10-1024 个字符）
- [ ] 文件夹名为小写，用连字符分隔
- [ ] 任何捆绑资源在 SKILL.md 中引用
- [ ] 捆绑资源不超过 5MB 每个文件

## 贡献

这是一个由社区驱动的项目。欢迎贡献！请查看：

- [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指导原则
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) 了解社区标准
- [SECURITY.md](SECURITY.md) 了解安全政策

## MCP 服务器

该仓库包括一个 MCP (Model Context Protocol) 服务器，提供从本仓库直接搜索和安装资源的提示词。需要 Docker 才能运行服务器。

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

# AGENTS.md

## 项目概述

Awesome GitHub Copilot 仓库是一个社区驱动的项目，收集了自定义代理、提示和指令，旨在提升 GitHub Copilot 在不同领域、语言和使用场景中的体验。该项目包括：

- **代理** - 与 MCP 服务器集成的专用 GitHub Copilot 代理
- **提示** - 用于代码生成和问题解决的特定任务提示
- **指令** - 应用于特定文件模式的编码标准和最佳实践
- **技能** - 包含指令和捆绑资源的自包含文件夹，用于专门任务
- **集合** - 按特定主题和工作流程整理的精选资源集合

## 仓库结构

```
.
├── agents/           # 自定义 GitHub Copilot 代理定义文件（.agent.md 文件）
├── prompts/          # 任务特定提示文件（.prompt.md 文件）
├── instructions/     # 编码标准和指南文件（.instructions.md 文件）
├── skills/           # 代理技能文件夹（每个文件夹包含 SKILL.md 文件和可选的捆绑资源）
├── collections/      # 精选资源集合文件（.md 文件）
├── docs/             # 不同资源类型的文档
├── eng/              # 构建和自动化脚本
└── scripts/          # 工具脚本
```

## 设置命令

```bash
# 安装依赖项
npm ci

# 构建项目（生成 README.md）
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

## 开发工作流程

### 与代理、提示、指令和技能的协作

所有代理文件（*.agent.md）、提示文件（*.prompt.md）和指令文件（*.instructions.md）必须包含正确的 Markdown 前置资料。代理技能是包含 `SKILL.md` 文件（含前置资料和可选捆绑资源）的文件夹：

#### 代理文件 (*.agent.md)

- 必须包含 `description` 字段（用单引号包裹）
- 文件名应为全小写，单词间用短横线分隔
- 建议包含 `tools` 字段
- 强烈建议指定 `model` 字段

#### 提示文件 (*.prompt.md)

- 必须包含 `agent` 字段（值应为 `'agent'`，用单引号包裹）
- 必须包含非空的 `description` 字段（用单引号包裹）
- 文件名应为全小写，单词间用短横线分隔
- 如适用，建议指定 `tools` 字段
- 强烈建议指定 `model` 字段

#### 指令文件 (*.instructions.md)

- 必须包含 `description` 字段（用单引号包裹，且不能为空）
- 必须包含 `applyTo` 字段，指定文件模式（例如：'**.js,**.ts'）
- 文件名应为全小写，单词间用短横线分隔

#### 代理技能 (skills/*/SKILL.md)

- 每个技能是一个文件夹，包含一个 `SKILL.md` 文件
- `SKILL.md` 必须包含 `name` 字段（全小写，用短横线分隔，与文件夹名称匹配，最大 64 个字符）
- `SKILL.md` 必须包含 `description` 字段（用单引号包裹，长度为 10-1024 个字符）
- 文件夹名称应为全小写，单词间用短横线分隔
- 技能可以包含捆绑资源（脚本、模板、数据文件）
- 捆绑资源应在 `SKILL.md` 指令中引用
- 每个文件的捆绑资源大小应合理（小于 5MB）
- 技能遵循 [代理技能规范](https://agentskills.io/specification)

### 添加新资源

当添加新的代理、提示、指令或技能时：

**对于代理、提示和指令：**

1. 创建包含正确前置资料的文件
2. 将文件添加到相应的目录
3. 运行：`npm run build` 更新 README.md
4. 验证生成的 README 中是否包含该资源

**对于技能：**

1. 运行 `npm run skill:create` 来生成新的技能文件夹
2. 编辑生成的 SKILL.md 文件，添加您的指令
3. 将任何捆绑资源（脚本、模板、数据）添加到技能文件夹中
4. 运行 `npm run skill:validate` 来验证技能结构
5. 运行 `npm run build` 更新 README.md
6. 验证生成的 README 中是否正确显示了该技能

### 指令测试

```bash
# 运行所有验证检查
npm run collection:validate
npm run skill:validate

# 构建并验证 README 生成
npm run build

# 修复行尾符（提交前必需）
bash scripts/fix-line-endings.sh
```

提交前请确保：

- 所有 Markdown 前置资料格式正确
- 所有新文件名遵循全小写与短横线分隔的命名规范
- 运行 `npm run build` 更新 README
- **始终运行 `bash scripts/fix-line-endings.sh`** 以将行尾符标准化为 LF（Unix 风格）
- 验证新资源在 README 中的显示是否正确

## 代码风格指南

### Markdown 文件

- 使用包含必要字段的正确前置资料
- 保持描述简洁且信息丰富
- 用单引号包裹描述字段的值
- 使用全小写文件名，单词间用短横线分隔

### JavaScript/Node.js 脚本

- 位于 `eng/` 和 `scripts/` 目录中
- 遵循 Node.js ES 模块规范（.mjs 扩展名）
- 使用清晰、描述性的函数和变量名称

## 提交 Pull Request 的指南

创建 Pull Request 时：

1. **README 更新**：新文件在运行 `npm run build` 后应自动添加到 README 中
2. **前置资料验证**：确保所有 Markdown 文件包含必要的前置资料字段
3. **文件命名**：验证所有新文件遵循全小写与短横线分隔的命名规范
4. **构建检查**：提交前运行 `npm run build` 验证 README 生成
5. **行尾符**：**始终运行 `bash scripts/fix-line-endings.sh`** 以将行尾符标准化为 LF（Unix 风格）
6. **描述**：提供您的代理/提示/指令的功能清晰描述
7. **测试**：如果添加了集合，请运行 `npm run collection:validate` 确保其有效性

### 提交前的检查清单

在提交 Pull Request 前，请确保：

- [X] 运行 `npm install`（或 `npm ci`）安装依赖项
- [ ] 运行 `npm run build` 生成更新后的 README.md
- [ ] 运行 `bash scripts/fix-line-endings.sh` 标准化行尾符
- [ ] 验证所有新文件包含正确的前置资料
- [ ] 测试您的贡献是否与 GitHub Copilot 兼容
- [ ] 检查文件名是否遵循命名规范

### 代码审查检查清单

对于提示文件 (*.prompt.md)：

- [ ] 包含 Markdown 前置资料
- [ ] 包含 `agent` 字段（值应为 `'agent'`，用单引号包裹）
- [ ] 包含非空的 `description` 字段（用单引号包裹）
- [ ] 文件名为全小写，单词间用短横线分隔
- [ ] 包含 `model` 字段（强烈建议）

对于指令文件 (*.instructions.md)：

- [ ] 包含 Markdown 前置资料
- [ ] 包含非空的 `description` 字段（用单引号包裹）
- [ ] 包含 `applyTo` 字段，指定文件模式
- [ ] 文件名为全小写，单词间用短横线分隔

对于代理文件 (*.agent.md)：

- [ ] 包含 Markdown 前置资料
- [ ] 包含非空的 `description` 字段（用单引号包裹）
- [ ] 文件名为全小写，单词间用短横线分隔
- [ ] 包含 `model` 字段（强烈建议）
- [ ] 考虑使用 `tools` 字段

对于技能 (skills/*/)：

- [ ] 文件夹包含 SKILL.md 文件
- [ ] SKILL.md 包含 Markdown 前置资料
- [ ] 包含 `name` 字段，与文件夹名称匹配（全小写，用短横线分隔，最大 64 个字符）
- [ ] 包含非空的 `description` 字段（用单引号包裹，长度为 10-1024 个字符）
- [ ] 文件夹名称为全小写，单词间用短横线分隔
- [ ] 所有捆绑资源在 SKILL.md 中引用
- [ ] 捆绑资源每个文件大小不超过 5MB

## 贡献指南

这是一个社区驱动的项目。欢迎贡献！请参阅：

- [贡献指南](CONTRIBUTING.md)
- [社区规范](CODE_OF_CONDUCT.md)
- [安全政策](SECURITY.md)

## MCP 服务器

该仓库包含一个 MCP（模型上下文协议）服务器，可直接从该仓库搜索和安装资源。需要 Docker 来运行服务器。

## 许可证

MIT 许可证 - 详情请参见 [LICENSE](LICENSE)

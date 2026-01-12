

---
description: '创建高质量GitHub Copilot Agent技能的指南'
applyTo: '**/.github/skills/**/SKILL.md, **/.claude/skills/**/SKILL.md'
---

# Agent技能文件指南

创建有效且可移植的Agent技能的说明，这些技能可以增强GitHub Copilot的专用功能、工作流和捆绑资源。

## 什么是Agent技能？

Agent技能是包含指令和捆绑资源的自包含文件夹，用于教授AI代理特定功能。与自定义指令（定义编码标准）不同，技能可以启用任务特定的工作流，包括脚本、示例、模板和参考数据。

关键特性：
- **可移植**：可在VS Code、Copilot CLI和Copilot编码代理中使用
- **渐进式加载**：仅在与用户请求相关时加载
- **资源捆绑**：可以包含脚本、模板、示例和指令
- **按需激活**：根据提示的相关性自动激活

## 目录结构

技能存储在特定位置：

| 位置 | 作用域 | 推荐 |
|------|--------|------|
| `.github/skills/<skill-name>/` | 项目/仓库 | 推荐用于项目技能 |
| `.claude/skills/<skill-name>/` | 项目/仓库 | 旧版，用于向后兼容 |
| `~/.github/skills/<skill-name>/` | 个人（用户级） | 推荐用于个人技能 |
| `~/.claude/skills/<skill-name>/` | 个人（用户级） | 旧版，用于向后兼容 |

每个技能**必须**拥有自己的子目录，其中至少包含一个`SKILL.md`文件。

## 必需的SKILL.md格式

### 前置信息（必需）

```yaml
---
name: webapp-testing
description: 使用Playwright测试本地Web应用程序的工具包。在被要求验证前端功能、调试UI行为、捕获浏览器截图、检查视觉回归或查看浏览器控制台日志时使用。支持Chrome、Firefox和WebKit浏览器。
license: 完整条款请参见LICENSE.txt
---
```

| 字段 | 是否必需 | 约束 |
|------|----------|------|
| `name` | 是 | 小写，空格用短横线，最大64个字符（例如，`webapp-testing`） |
| `description` | 是 | 清晰描述功能和使用场景，最大1024个字符 |
| `license` | 否 | 参考LICENSE.txt（例如，`完整条款请参见LICENSE.txt`）或SPDX标识符 |

### 描述最佳实践

**关键**：`description`字段是自动发现技能的主要机制。Copilot仅通过`name`和`description`来决定是否加载技能。如果描述模糊，该技能将永远不会被激活。

**描述中应包含的内容：**
1. **技能**的功能（能力）
2. **何时**使用它（特定触发条件、场景、文件类型或用户请求）
3. **用户**可能在提示中提到的**关键词**

**好的描述：**
```yaml
description: 使用Playwright测试本地Web应用程序的工具包。在被要求验证前端功能、调试UI行为、捕获浏览器截图、检查视觉回归或查看浏览器控制台日志时使用。支持Chrome、Firefox和WebKit浏览器。
```

**差的描述：**
```yaml
description: Web测试辅助工具
```

差的描述失败的原因：
- 没有具体触发条件（Copilot何时加载这个技能？）
- 没有关键词（哪些用户提示会匹配？）
- 没有功能（它实际上能做什么？）

### 正文内容

正文包含Copilot在技能激活后加载的详细说明。推荐的章节：

| 章节 | 目的 |
|------|------|
| `# 标题` | 简要概述该技能能实现什么 |
| `## 何时使用此技能` | 列出使用场景（强化描述触发条件） |
| `## 前提条件` | 必要的工具、依赖项和环境设置 |
| `## 分步工作流` | 常见任务的编号步骤 |
| `## 故障排除` | 常见问题和解决方案表格 |
| `## 参考资料` | 捆绑文档或外部资源的链接 |

## 捆绑资源

技能可以包含Copilot按需访问的附加文件：

### 支持的资源类型

| 文件夹 | 目的 | 是否加载到上下文中 | 示例文件 |
|--------|------|---------------------|----------|
| `scripts/` | 执行特定操作的可执行自动化脚本 | 在执行时加载 | `helper.py`, `validate.sh`, `build.ts` |
| `references/` | AI代理读取以指导决策的文档 | 是，在被引用时加载 | `api_reference.md`, `workflow-setup.md`（详细工作流，>5步）, `workflow-deployment.md` |
| `assets/` | **直接用于输出的静态文件**（AI代理不修改） | 否 | `logo.png`, `brand-template.pptx`, `custom-font.ttf` |
| `templates/` | **AI代理主动修改的起始代码/框架** | 是，在被引用时加载 | `viewer.html`（插入算法）, `hello-world/`（扩展） |

### 目录结构示例

```
.github/skills/my-skill/
├── SKILL.md              # 必需：主指令
├── LICENSE.txt           # 推荐：许可证条款（通常为Apache 2.0）
├── scripts/              # 可选：可执行自动化脚本
│   ├── helper.py         # Python脚本
│   └── helper.ps1        # PowerShell脚本
├── references/           # 可选：加载到上下文中的文档
│   ├── api_reference.md
│   ├── workflow-setup.md     # 详细工作流（>5步）
│   └── workflow-deployment.md
├── assets/               # 可选：直接用于输出的静态文件
│   ├── baseline.png      # 用于比较的参考图像
│   └── report-template.html
└── templates/            # 可选：AI代理修改的起始代码
    ├── scaffold.py       # AI代理自定义的代码框架
    └── config.template   # AI代理填充值的配置模板
```

> **LICENSE.txt**：创建技能时，请从 https://www.apache.org/licenses/LICENSE-2.0.txt 下载Apache 2.0许可证文本并保存为`LICENSE.txt`。更新附录中的版权年份和所有者信息。

### 资产与模板：关键区别

**资产**是静态资源，**在输出中按原样使用**：
- 一个`logo.png`嵌入到生成的文档中
- 一个`report-template.html`作为输出格式复制
- 一个`custom-font.ttf`应用于文本渲染

**模板**是起始代码/框架，**AI代理主动修改**：
- 一个`scaffold.py`，AI代理插入逻辑
- 一个`config.template`，AI代理根据用户需求填充值
- 一个`hello-world/`项目目录，AI代理扩展新功能

**经验法则**：如果AI代理读取并基于文件内容进行构建 → 放入`templates/`。如果文件在输出中直接使用且不被修改 → 放入`assets/`。

### 在SKILL.md中引用资源

使用相对路径引用技能目录中的文件：

```markdown
## 可用脚本

运行 [辅助脚本](./scripts/helper.py) 来自动化常见任务。

查看 [API参考](./references/api_reference.md) 以获取详细文档。

使用 [模板](./templates/scaffold.py) 作为起点。
```

## 渐进式加载架构

技能采用三级加载机制以提高效率：

| 等级 | 加载内容 | 何时加载 |
|------|----------|----------|
| 1. 发现 | 仅`name`和`description` | 始终加载（轻量级元数据） |
| 2. 指令 | 完整的`SKILL.md`正文 | 当请求与描述匹配时 |
| 3. 资源 | 脚本、示例和文档 | 仅当Copilot引用它们时 |

这意味着：
- 可以安装大量技能而不会消耗上下文
- 每个任务仅加载相关的内容
- 资源仅在需要时加载

## 内容指南

### 写作风格

- 使用祈使语气：如“运行”、“创建”、“配置”（而不是“您应该运行”）
- 具体且可操作
- 包含精确的命令和参数
- 在合适的地方展示预期输出
- 保持各部分聚焦且易于扫描

### 脚本要求

包含脚本时，优先选择跨平台语言：

| 语言 | 使用场景 |
|------|----------|
| Python | 复杂自动化、数据处理 |
| pwsh | PowerShell Core脚本 |
| Node.js | 基于JavaScript的工具 |
| Bash/Shell | 简单自动化任务 |

最佳实践：
- 包含帮助/使用文档（`--help`标志）
- 用清晰的信息优雅处理错误
- 避免存储凭证或秘密
- 尽可能使用相对路径

### 何时捆绑脚本

在技能中包含脚本时：
- 代理可能重复编写相同代码
- 需要确定性的可靠性（例如文件操作、API调用）
- 复杂逻辑通过预测试而非每次生成更有效
- 操作具有独立的自包含目的，可独立发展
- 可测试性很重要 — 脚本可以单元测试和验证
- 预期可预测的行为优于动态生成

脚本使操作能够进化：即使简单操作，如果可能变得复杂、需要一致的行为或未来扩展性，也应作为脚本实现。

### 安全性考虑

- 脚本依赖现有的凭证助手（不存储凭证）
- 仅在破坏性操作时包含`--force`标志
- 在不可逆操作前警告用户
- 文档任何网络操作或外部调用

## 常见模式

### 参数表模式

清晰地记录参数：

```markdown
| 参数 | 是否必需 | 默认值 | 描述 |
|------|----------|--------|------|
| `--input` | 是 | - | 要处理的输入文件或URL |
| `--action` | 是 | - | 要执行的操作 |
| `--verbose` | 否 | `false` | 启用详细输出 |
```

## 验证检查清单

在发布技能前，请确认以下事项：

- [ ] `SKILL.md`包含有效的前置信息，其中包含`name`和`description`
- [ ] `name`为小写，使用短横线分隔空格，长度不超过64个字符
- [ ] `description`清晰说明**功能**、**使用场景**和相关**关键词**
- [ ] 正文包含使用场景、前提条件和分步工作流
- [ ] `SKILL.md`正文保持在500行以内（将大内容拆分为`references/`文件夹）
- [ ] 大于5步的工作流拆分为`references/`文件夹，并从`SKILL.md`中提供清晰链接
- [ ] 脚本包含帮助文档和错误处理
- [ ] 所有资源引用使用相对路径
- [ ] 不包含硬编码的凭证或秘密

## 工作流执行模式

在执行多步骤工作流时，创建一个TODO列表，其中每个步骤引用相关文档：

```markdown
## TODO
- [ ] 步骤1：配置环境 - 请参见 [workflow-setup.md](./references/workflow-setup.md#environment)
- [ ] 步骤2：构建项目 - 请参见 [workflow-setup.md](./references/workflow-setup.md#build)
- [ ] 步骤3：部署到测试环境 - 请参见 [workflow-deployment.md](./references/workflow-deployment.md#staging)
- [ ] 步骤4：运行验证 - 请参见 [workflow-deployment.md](./references/workflow-deployment.md#validation)
- [ ] 步骤5：部署到生产环境 - 请参见 [workflow-deployment.md](./references/workflow-deployment.md#production)
```

这确保了可追溯性，并允许在中断后恢复工作流。

## 相关资源

- [Agent技能规范](https://agentskills.io/)
- [VS Code Agent技能文档](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [参考技能仓库](https://github.com/anthropics/skills)
- [Awesome Copilot技能](https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md)
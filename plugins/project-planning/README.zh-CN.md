# 项目规划与管理插件

为开发团队提供的软件项目规划、功能分解、史诗管理、实施计划和任务组织工具及指导。

## 安装

```bash
# 使用 Copilot CLI
copilot plugin install project-planning@awesome-copilot
```

## 包含内容

### 命令（斜杠命令）

| 命令 | 描述 |
|------|------|
| `/project-planning:breakdown-feature-implementation` | 提示创建详细的特性实现计划，遵循 Epoch 单体仓库结构。 |
| `/project-planning:breakdown-feature-prd` | 提示基于史诗创建产品需求文档 (PRD) 用于新功能。 |
| `/project-planning:breakdown-epic-arch` | 提示基于产品需求文档创建史诗的高级技术架构。 |
| `/project-planning:breakdown-epic-pm` | 提示为新史诗创建史诗产品需求文档 (PRD)。该 PRD 将作为生成技术架构规范的输入。 |
| `/project-planning:create-implementation-plan` | 为新功能、重构现有代码或升级包、设计、架构或基础设施创建新的实现计划文件。 |
| `/project-planning:update-implementation-plan` | 使用新或更新的需求更新现有的实现计划文件，以提供新功能、重构现有代码或升级包、设计、架构或基础设施。 |
| `/project-planning:create-github-issues-feature-from-implementation-plan` | 使用 feature_request.yml 或 chore_request.yml 模板，从实现计划阶段创建 GitHub 问题。 |
| `/project-planning:create-technical-spike` | 创建时间限制的技术冲刺文档，用于在实施前研究和解决关键开发决策。 |

### 代理

| 代理 | 描述 |
|------|------|
| `task-planner` | 任务规划器，用于创建可操作的实现计划 - 由 microsoft/edge-ai 提供 |
| `task-researcher` | 任务研究专家，用于全面的项目分析 - 由 microsoft/edge-ai 提供 |
| `planner` | 为新功能或重构现有代码生成实现计划。 |
| `plan` | 专注于实施前深入分析的战略规划与架构助手。帮助开发者理解代码库、明确需求并制定全面的实施策略。 |
| `prd` | 生成详细说明用户故事、验收标准、技术考量和指标的 Markdown 格式产品需求文档 (PRD)。可选地，在用户确认后创建 GitHub 问题。 |
| `implementation-plan` | 为新功能或重构现有代码生成实现计划。 |
| `research-technical-spike` | 通过全面调查和受控实验系统地研究和验证技术冲刺文档。 |

## 来源

此插件是 [Awesome Copilot](https://github.com/github/awesome-copilot) 的一部分，这是一个社区驱动的 GitHub Copilot 扩展集合。

## 许可证

MIT

# Gem 团队多智能体编排

一个用于复杂项目执行的模块化多智能体团队，支持基于DAG的规划、并行执行、TDD验证和自动化测试。

**标签:** 多智能体, 编排, DAG规划, 并行执行, TDD, 验证, 自动化, 安全

## 本集合中的项目

| 标题 | 类型 | 描述 | MCP 服务器 |
| ----- | ---- | ----------- | ----------- |
| [Gem 编排器](../agents/gem-orchestrator.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-orchestrator.agent.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-orchestrator.agent.md) | 智能体 | 协调多智能体工作流，通过 runSubagent 分配任务并综合结果 [查看使用方法](#gem-orchestrator) |  |
| [Gem 研究员](../agents/gem-researcher.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-researcher.agent.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-researcher.agent.md) | 智能体 | 研究专家：收集代码库上下文，识别相关文件/模式，返回结构化研究成果 [查看使用方法](#gem-researcher) |  |
| [Gem 规划器](../agents/gem-planner.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-planner.agent.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-planner.agent.md) | 智能体 | 基于研究结果创建 DAG 规划，包含事前分析和任务分解 [查看使用方法](#gem-planner) |  |
| [Gem 实施者](../agents/gem-implementer.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-implementer.agent.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-implementer.agent.md) | 智能体 | 执行 TDD 代码更改，确保验证，维护代码质量 [查看使用方法](#gem-implementer) |  |
| [Gem Chrome 测试员](../agents/gem-chrome-tester.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-chrome-tester.agent.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-chrome-tester.agent.md) | 智能体 | 通过 Chrome DevTools 自动化浏览器测试和 UI/UX 验证 [查看使用方法](#gem-chrome-tester) |  |
| [Gem DevOps](../agents/gem-devops.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-devops.agent.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-devops.agent.md) | 智能体 | 管理容器、CI/CD 流水线和基础设施部署 [查看使用方法](#gem-devops) |  |
| [Gem 审查员](../agents/gem-reviewer.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-reviewer.agent.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-reviewer.agent.md) | 智能体 | 关键任务的安全守门人——应用 OWASP 扫描、密钥检测和合规性验证 [查看使用方法](#gem-reviewer) |  |
| [Gem 文档编写器](../agents/gem-documentation-writer.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-documentation-writer.agent.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fgem-documentation-writer.agent.md) | 智能体 | 生成技术文档、图表，并保持代码与文档的一致性 [查看使用方法](#gem-documentation-writer) |  |

## 集合使用方法

### Gem 编排器

推荐

编排器是协调多智能体工作流的核心枢纽，通过 runSubagent 分配任务并综合结果。它不直接执行任务，而是管理整体工作流。

该智能体适用于：
- 协调复杂的多智能体工作流
- 管理任务分配和并行执行
- 综合多个智能体的结果
- 维护 plan.yaml 状态

为了获得最佳效果，建议：
- 任何复杂项目都从编排器开始
- 提供清晰的目标和约束条件
- 执行前审查 plan.yaml
- 使用 walkthrough 总结跟踪进度

---

### Gem 研究员

推荐

研究员收集代码库上下文，识别相关文件/模式，并返回结构化研究成果。通常由编排器调用以聚焦特定领域。

该智能体适用于：
- 理解代码库结构和模式
- 识别特定功能的相关文件
- 在进行更改前收集上下文
- 研究技术依赖项

为了获得最佳效果，建议：
- 指定清晰的研究领域或问题
- 提供关于目标的上下文信息
- 并行使用多个研究员处理不同领域

---

### Gem 规划器

推荐

规划器基于研究结果创建 DAG 规划，进行事前分析，提交审批，并根据反馈迭代优化。它将研究发现综合为结构化计划。

该智能体适用于：
- 将复杂目标分解为原子任务
- 创建任务依赖关系（DAG）
- 运行事前分析以识别风险
- 执行前获取审批

为了获得最佳效果，建议：
- 提供研究员的清晰研究结果
- 审批前仔细审查计划
- 如果计划不理想，要求迭代优化
- 使用 plan_review 工具进行协作规划

---

### Gem 实施者

推荐

实施者执行 TDD 代码更改，确保验证通过，并维护代码质量。它遵循严格的 TDD 纪律，使用验证命令。

该智能体适用于：
- 采用 TDD 纪律实现功能
- 先写测试再写代码
- 确保验证命令通过
- 维护代码质量

为了获得最佳效果，建议：
- 始终提供验证命令
- 遵循 TDD：红绿重构
- 每次编辑后检查 get_errors
- 保持更改的最小化和聚焦

---

### Gem Chrome 测试员

可选

Chrome 测试员通过 Chrome DevTools 自动化浏览器测试和 UI/UX 验证。它需要 Chrome DevTools MCP 服务器。

该智能体适用于：
- 自动化浏览器测试
- UI/UX 验证
- 捕获截图和快照
- 测试 Web 应用程序

为了获得最佳效果，建议：
- 确保已安装 Chrome DevTools MCP 服务器
- 提供清晰的测试场景
- 使用快照进行调试
- 在不同视口尺寸下测试

---

### Gem DevOps

可选

DevOps 智能体管理容器、CI/CD 流水线和基础设施部署。它处理基础设施即代码和部署自动化。

该智能体适用于：
- 设置 CI/CD 流水线
- 管理容器（Docker、Kubernetes）
- 基础设施部署
- DevOps 自动化

为了获得最佳效果，建议：
- 提供清晰的基础设施需求
- 遵循基础设施即代码最佳实践
- 在本地测试流水线
- 记录部署过程

---

### Gem 审查员

推荐

审查员是关键任务的安全守门人，应用 OWASP 扫描、密钥检测和合规性验证。

该智能体适用于：
- 安全代码审查
- OWASP 顶级 10 扫描
- 密钥和 PII 检测
- 合规性验证

为了获得最佳效果，建议：
- 对所有关键安全更改使用审查员
- 仔细审查审查结果
- 解决所有安全问题
- 保持文档更新

---

### Gem 文档编写器

可选

文档编写器生成技术文档、图表，并保持代码与文档的一致性。

该智能体适用于：
- 生成技术文档
- 创建图表
- 保持文档与代码同步
- API 文档

为了获得最佳效果，建议：
- 提供清晰的上下文和需求
- 审查生成的文档以确保准确性
- 随代码更改更新文档
- 使用一致的文档风格

---

*本集合包含 8 个精选项目用于 **Gem 团队多智能体编排**。*

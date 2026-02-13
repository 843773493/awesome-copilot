# Gem 团队多智能体编排插件

一个模块化的多智能体团队，用于复杂项目的执行，具备基于DAG的规划、并行执行、TDD验证和自动化测试功能。

## 安装

```bash
# 使用 Copilot CLI
copilot plugin install gem-team@awesome-copilot
```

## 包含内容

### 智能体

| 智能体 | 描述 |
|--------|------|
| `gem-orchestrator` | 协调多智能体工作流，委派任务，通过 runSubagent 合成结果 |
| `gem-researcher` | 研究专家：收集代码库上下文，识别相关文件/模式，返回结构化结果 |
| `gem-planner` | 从研究结果中创建基于DAG的计划，进行预演分析和任务分解 |
| `gem-implementer` | 执行 TDD 代码更改，确保验证，维护质量 |
| `gem-chrome-tester` | 通过 Chrome DevTools 自动化浏览器测试，UI/UX 验证 |
| `gem-devops` | 管理容器、CI/CD 流水线和基础设施部署 |
| `gem-reviewer` | 关键任务的安全守门人——OWASP、密钥、合规性 |
| `gem-documentation-writer` | 生成技术文档、图表，保持代码与文档的一致性 |

## 来源

此插件是 [Awesome Copilot](https://github.com/github/awesome-copilot) 的一部分，这是一个由社区驱动的 GitHub Copilot 扩展集合。

## 许可证

MIT

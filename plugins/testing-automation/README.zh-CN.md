# 测试与测试自动化插件

涵盖编写测试、测试自动化和测试驱动开发的全面集合，包括单元测试、集成测试和端到端测试策略。

## 安装

```bash
# 使用 Copilot CLI
copilot plugin install testing-automation@awesome-copilot
```

## 包含内容

### 命令（斜杠命令）

| 命令 | 描述 |
|------|------|
| `/testing-automation:playwright-explore-website` | 使用 Playwright MCP 进行网站探索测试 |
| `/testing-automation:playwright-generate-test` | 基于场景使用 Playwright MCP 生成测试 |
| `/testing-automation:csharp-nunit` | 获取 NUnit 单元测试的最佳实践，包括数据驱动测试 |
| `/testing-automation:java-junit` | 获取 JUnit 5 单元测试的最佳实践，包括数据驱动测试 |
| `/testing-automation:ai-prompt-engineering-safety-review` | 全面的 AI 提示工程安全审查和改进建议。分析提示的安全性、偏见、安全漏洞和有效性，同时提供详细的改进建议，涵盖广泛框架、测试方法和教育内容。 |

### 代理

| 代理 | 描述 |
|------|------|
| `tdd-red` | 通过在实现存在之前根据 GitHub 问题上下文编写描述所需行为的失败测试来指导测试先行开发。 |
| `tdd-green` | 实现满足 GitHub 问题需求的最小代码，使失败测试通过，而不过度设计。 |
| `tdd-refactor` | 在保持绿色测试和 GitHub 问题合规的同时，提高代码质量，应用安全最佳实践，并增强设计。 |
| `playwright-tester` | Playwright 测试模式 |

## 源码

此插件是 [Awesome Copilot](https://github.com/github/awesome-copilot) 的一部分，这是一个社区驱动的 GitHub Copilot 扩展集合。

## 许可证

MIT

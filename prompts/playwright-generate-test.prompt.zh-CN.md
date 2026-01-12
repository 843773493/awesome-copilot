

---
agent: 代理
description: '基于场景使用 Playwright MCP 生成 Playwright 测试'
tools: ['变更', '代码库搜索', '编辑文件', '获取', '问题', '运行命令', '运行任务', '运行测试', '搜索', '搜索结果', '终端最后命令', '终端选区命令', '测试失败', 'playwright/*']
model: 'Claude Sonnet 4.5'
---

# 使用 Playwright MCP 进行测试生成

您的目标是在完成所有规定步骤后，根据提供的场景生成一个 Playwright 测试。

## 具体指示

- 您将获得一个场景，需要根据该场景生成 Playwright 测试。如果用户未提供场景，您需要要求其提供。
- **不要在完成所有规定步骤之前或仅基于场景生成测试代码**。
- **必须使用 Playwright MCP 提供的工具逐个执行步骤**。
- 仅在所有步骤完成后，根据消息历史记录生成基于 `@playwright/test` 的 Playwright TypeScript 测试
- 将生成的测试文件保存在 tests 目录中
- 执行测试文件并迭代直到测试通过
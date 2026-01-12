

---
agent: agent
description: '使用 Playwright MCP 进行网站测试探索'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'fetch', 'findTestFiles', 'problems', 'runCommands', 'runTasks', 'runTests', 'search', 'search/searchResults', 'runCommands/terminalLastCommand', 'runCommands/terminalSelection', 'testFailure', 'playwright']
model: 'Claude Sonnet 4'
---

# 网站测试探索

您的目标是探索网站并识别关键功能。

## 具体指令

1. 使用 Playwright MCP 服务器访问提供的 URL。如果未提供 URL，请要求用户提供一个。
2. 识别并交互3-5个核心功能或用户流程。
3. 记录用户交互、相关UI元素（及其定位器）以及预期结果。
4. 在完成时关闭浏览器上下文。
5. 提供简明扼要的总结。
6. 根据探索结果提出并生成测试用例。
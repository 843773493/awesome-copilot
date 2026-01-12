

---
描述：'使用验收标准、技术考量、边界情况和非功能性需求来精炼需求或问题'
工具: [ 'list_issues','githubRepo', 'search', 'add_issue_comment','create_issue','create_issue_comment','update_issue','delete_issue','get_issue', 'search_issues']
---

# 需求或问题精炼聊天模式

当激活此模式时，GitHub Copilot 可以分析现有问题，并通过以下结构化细节对其进行补充：

- 包含上下文和背景信息的详细描述
- 可测试格式的验收标准
- 技术考量及依赖项
- 潜在的边界情况和风险
- 预期的非功能性需求（NFR）

## 操作步骤
1. 阅读问题描述并理解上下文。
2. 修改问题描述以包含更多细节。
3. 添加可测试格式的验收标准。
4. 包含技术考量及依赖项。
5. 添加潜在的边界情况和风险。
6. 提供工作量估算的建议。
7. 审核精炼后的需求并进行必要的调整。

## 使用方法

要激活需求精炼模式：

1. 在提示中引用现有问题，格式为 `refine <issue_URL>`
2. 使用模式：`refine-issue`

## 输出

Copilot 将修改问题描述并为其添加结构化细节。
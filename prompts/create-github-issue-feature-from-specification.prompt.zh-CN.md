

---
agent: 'agent'
description: '根据规范文件中的功能请求创建 GitHub 问题，使用 feature_request.yml 模板。'
tools: ['search/codebase', 'search', 'github', 'create_issue', 'search_issues', 'update_issue']
---
# 从规范创建 GitHub 问题

为位于 `${file}` 的规范文件创建 GitHub 问题。

## 流程

1. 分析规范文件以提取需求
2. 使用 `search_issues` 检查现有问题
3. 使用 `create_issue` 创建新问题或使用 `update_issue` 更新现有问题
4. 使用 `feature_request.yml` 模板（若无则使用默认模板）

## 要求

- 为完整规范创建一个单独的问题
- 明确的标题以标识规范
- 仅包含规范要求的更改
- 在创建前与现有问题进行核对

## 问题内容

- 标题：从规范中提取的功能名称
- 描述：问题陈述、提出的解决方案和上下文
- 标签：feature, enhancement（视情况而定）
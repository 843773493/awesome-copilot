

---
agent: 'agent'
description: '根据实施计划阶段使用 feature_request.yml 或 chore_request.yml 模板创建 GitHub 问题。'
tools: ['search/codebase', 'search', 'github', 'create_issue', 'search_issues', 'update_issue']
---
# 从实施计划创建 GitHub 问题

根据 `${file}` 文件中的实施计划创建 GitHub 问题。

## 流程

1. 分析计划文件以识别各个阶段
2. 使用 `search_issues` 检查现有问题
3. 使用 `create_issue` 为每个阶段创建新问题，或使用 `update_issue` 更新现有问题
4. 使用 `feature_request.yml` 或 `chore_request.yml` 模板（若未找到则回退到默认模板）

## 要求

- 每个实施阶段对应一个独立的问题
- 标题和描述需清晰且结构化
- 仅包含计划中要求的变更内容
- 创建前需与现有问题进行核对

## 问题内容

- 标题：从实施计划中提取的阶段名称
- 描述：阶段详情、需求及上下文信息
- 标签：根据问题类型（功能/任务）选择合适的标签
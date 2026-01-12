

---
agent: 'agent'
description: '使用 feature_request.yml 模板为规范文件中未实现的需求创建 GitHub Issues。'
tools: ['search/codebase', 'search', 'github', 'create_issue', 'search_issues', 'update_issue']
---
# 根据未满足的规范要求创建 GitHub Issues

在 `${file}` 文件中为规范中的未实现需求创建 GitHub Issues。

## 流程

1. 分析规范文件以提取所有需求
2. 检查代码库中每个需求的实现状态
3. 使用 `search_issues` 搜索现有 Issues 以避免重复
4. 为每个未实现的需求使用 `create_issue` 创建新 Issues
5. 使用 `feature_request.yml` 模板（若无则使用默认模板）

## 要求

- 每个未实现的规范需求对应一个 Issues
- 明确需求 ID 与描述的映射关系
- 包含实现指导和验收标准
- 创建前需核对现有 Issues

## Issues 内容

- 标题：需求 ID 和简要描述
- 描述：详细需求、实现方法和上下文
- 标签：功能需求、增强功能（视情况而定）

## 实现检查

- 在代码库中搜索相关代码模式
- 检查 `/spec/` 目录下的相关规范文件
- 验证需求未被部分实现
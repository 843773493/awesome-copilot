---
名称: microsoft-docs  
描述: 查询微软官方文档以了解概念、查找教程并学习服务的工作原理。适用于 Azure、.NET、Microsoft 365、Windows、Power Platform 和所有微软技术。从 learn.microsoft.com 和其他微软官方网站获取准确且最新的信息——架构概述、快速入门、配置指南、限制和最佳实践。  
兼容性: 需要 Microsoft Learn MCP Server (https://learn.microsoft.com/api/mcp)  
---

# 微软文档

## 工具

| 工具 | 用途 |
|------|---------|
| `microsoft_docs_search` | 查找文档—概念、指南、教程、配置 |
| `microsoft_docs_fetch` | 获取完整页面内容（当搜索摘要不够时） |

## 何时使用

- **理解概念** — "Cosmos DB 的分区机制是如何工作的？"
- **学习服务** — "Azure Functions 概述", "Container Apps 架构"
- **查找教程** — "快速入门", "入门指南", "逐步指南"
- **配置选项** — "App Service 配置设置"
- **限制与配额** — "Azure OpenAI 速率限制", "Service Bus 配额"
- **最佳实践** — "Azure 安全最佳实践"

## 查询有效性

良好的查询应具体：

```
# ❌ 过于宽泛
"Azure Functions"

# ✅ 具体
"Azure Functions Python v2 编程模型"
"Cosmos DB 分区键设计最佳实践"
"Container Apps KEDA 扩展规则"
```

包含上下文：
- **版本**（当相关时，如 `.NET 8`、`EF Core 8`）
- **任务意图**（`quickstart`、`tutorial`、`overview`、`limits`）
- **平台**（针对多平台文档，如 `Linux`、`Windows`）

## 何时获取完整页面

在搜索后获取完整页面，适用于以下情况：
- **教程** — 需要完整的逐步说明
- **配置指南** — 需要列出所有选项
- **深入探讨** — 用户希望获得全面覆盖
- **搜索摘要被截断** — 需要完整上下文

## 为何使用此工具

- **准确性** — 使用实时文档，而非可能过时的训练数据
- **完整性** — 教程包含所有步骤，而非片段
- **权威性** — 来自微软官方文档

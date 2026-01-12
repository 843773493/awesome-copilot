

---
description: '创建和管理 awesome-copilot 集合的指南'
applyTo: 'collections/*.collection.yml'
---

# 集合开发

## 集合指南

在 awesome-copilot 仓库中处理集合时：

- 在提交之前，始终使用 `node validate-collections.js` 验证集合
- 遵循已建立的 YAML 模式进行集合清单的编写
- 仅引用仓库中已存在的文件
- 使用描述性的集合 ID，仅包含小写字母、数字和短横线
- 保持集合专注于特定的工作流程或主题
- 测试所有引用项是否能够良好协作

## 集合结构

- **必填字段**：id、name、description、items
- **可选字段**：tags、display
- **项目要求**：路径必须存在，kind 必须与文件扩展名匹配
- **显示选项**：排序方式（按字母顺序/手动）、show_badge（true/false）

## 验证规则

- 所有集合的集合 ID 必须唯一
- 文件路径必须存在且与项目类型匹配
- 标签必须仅使用小写字母、数字和短横线
- 集合必须包含 1-50 个项目
- 描述必须为 1-500 个字符

## 最佳实践

- 将 3-10 个相关项目分组以实现最佳可用性  
- 使用清晰、描述性的名称和描述
- 添加相关标签以提高可发现性
- 测试集合所启用的完整工作流程
- 确保项目之间能够有效互补

## 文件组织

- 集合不需要重新组织文件
- 项目可以位于仓库的任何位置
- 使用相对于仓库根目录的路径
- 保持现有的目录结构（prompts/、instructions/、agents/）

## 生成流程

- 集合通过 `npm start` 自动生成 README 文件
- 单个集合页面在 collections/ 目录中创建
- 主集合概览生成为 README.collections.md
- 每个项目会自动生成 VS Code 安装徽章
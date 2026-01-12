

---
name: github-issues
description: '使用MCP工具创建、更新和管理GitHub问题。当用户想要创建错误报告、功能请求或任务问题，更新现有问题，添加标签/指派者/里程碑，或管理问题工作流时，使用此技能。触发词包括“创建一个问题”、“提交错误”、“请求功能”、“更新问题X”或任何GitHub问题管理任务。'
---

# GitHub问题

使用`@modelcontextprotocol/server-github` MCP服务器管理GitHub问题。

## 可用的MCP工具

| 工具 | 用途 |
|------|---------|
| `mcp__github__create_issue` | 创建新问题 |
| `mcp__github__update_issue` | 更新现有问题 |
| `mcp__github__get_issue` | 获取问题详情 |
| `mcp__github__search_issues` | 搜索问题 |
| `mcp__github__add_issue_comment` | 添加评论 |
| `mcp__github__list_issues` | 列出仓库问题 |

## 工作流程

1. **确定操作类型**：创建、更新还是查询？
2. **收集上下文**：获取仓库信息、现有标签、里程碑（如需）
3. **构建内容**：使用 [references/templates.md](references/templates.md) 中的适当模板
4. **执行**：调用相应的MCP工具
5. **确认**：向用户报告问题链接

## 创建问题

### 必填参数

```
owner: 仓库所有者（组织或用户）
repo: 仓库名称  
title: 清晰、可操作的标题
body: 结构化的Markdown内容
```

### 可选参数

```
labels: ["错误", "增强功能", "文档更新", ...]
assignees: ["username1", "username2"]
milestone: 里程碑编号（整数）
```

### 标题规范

- 当有帮助时以类型前缀开头：`[错误]`、`[功能]`、`[文档]`
- 具体且可操作
- 字符数控制在72个以内
- 示例：
  - `[错误] 使用SSO时登录页面崩溃`
  - `[功能] 添加深色模式支持`
  - `为认证模块添加单元测试`

### 正文结构

始终使用 [references/templates.md](references/templates.md) 中的模板。根据问题类型选择：

| 用户请求 | 模板 |
|--------------|----------|
| 错误、故障、无法运行 | 错误报告 |
| 功能、增强、添加、新功能 | 功能请求 |
| 任务、琐事、重构、更新 | 任务 |

## 更新问题

使用 `mcp__github__update_issue`，参数包括：

```
owner, repo, issue_number（必填）
title, body, state, labels, assignees, milestone（可选 - 仅需更改的字段）
```

状态值：`open`（开放）、`closed`（关闭）

## 示例

### 示例1：错误报告

**用户**："创建一个错误问题 - 使用SSO时登录页面崩溃"

**操作**：调用 `mcp__github__create_issue`，参数为：
```json
{
  "owner": "github",
  "repo": "awesome-copilot",
  "title": "[错误] 使用SSO时登录页面崩溃",
  "body": "## 描述\n用户尝试通过SSO进行认证时，登录页面崩溃。\n\n## 复现步骤\n1. 导航到登录页面\n2. 点击'通过SSO登录'\n3. 页面崩溃\n\n## 预期行为\nSSO认证应完成并重定向到仪表板。\n\n## 实际行为\n页面无响应并显示错误。\n\n## 环境\n- 浏览器：[待填写]\n- 操作系统：[待填写]\n\n## 其他上下文\n由用户报告。",
  "labels": ["错误"]
}
```

### 示例2：功能请求

**用户**："创建一个深色模式功能请求，优先级为高"

**操作**：调用 `mcp__github__create_issue`，参数为：
```json
{
  "owner": "github",
  "repo": "awesome-copilot",
  "title": "[功能] 添加深色模式支持",
  "body": "## 概述\n添加深色模式主题选项以提升用户体验和可访问性。\n\n## 动机\n- 减少低光环境下的眼睛疲劳\n- 用户日益期待此功能\n- 提升可访问性\n\n## 建议方案\n实现主题切换功能并检测系统偏好。\n\n## 可接受标准\n- [ ] 设置中添加切换开关\n- [ ] 保存用户偏好\n- [ ] 默认尊重系统偏好\n- [ ] 所有UI组件支持两种主题\n\n## 已考虑的替代方案\n未指定。\n\n## 其他上下文\n高优先级请求。",
  "labels": ["增强功能", "高优先级"]
}
```

## 常用标签

在适用时使用以下标准标签：

| 标签 | 用于 |
|-------|---------|
| `错误` | 某些功能无法正常工作 |
| `增强功能` | 新功能或改进 |
| `文档更新` | 文档更新 |
| `good first issue` | 新手友好 |
| `help wanted` | 需要额外关注 |
| `问题` | 需要更多信息 |
| `wontfix` | 不予处理 |
| `duplicate` | 已存在 |
| `high-priority` | 紧急问题 |

## 提示

- 始终在创建问题前确认仓库上下文
- 在信息缺失时询问而非猜测
- 已知时链接相关问题：`相关问题 #123`
- 更新时，先获取当前问题以保留未更改字段
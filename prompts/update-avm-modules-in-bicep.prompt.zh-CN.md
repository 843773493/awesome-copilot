

---
agent: 'agent'
description: '将 Bicep 文件中的 Azure 验证模块 (AVM) 更新为最新版本。'
tools: ['search/codebase', 'think', 'changes', 'fetch', 'search/searchResults', 'todos', 'edit/editFiles', 'search', 'runCommands', 'bicepschema', 'azure_get_schema_for_Bicep']
---
# 更新 Bicep 文件中的 Azure 验证模块

将 Bicep 文件 `${file}` 更新为使用最新的 Azure 验证模块 (AVM) 版本。仅对非破坏性变更显示进度更新。除最终输出表格和摘要外，不输出其他信息。

## 流程

1. **扫描**: 从 `${file}` 中提取 AVM 模块及其当前版本
1. **识别**: 列出所有唯一 AVM 模块，通过匹配 `avm/res/{service}/{resource}` 使用 `#search` 工具
1. **检查**: 使用 `#fetch` 工具从 MCR 获取每个 AVM 模块的最新版本：`https://mcr.microsoft.com/v2/bicep/avm/res/{service}/{resource}/tags/list`
1. **比较**: 解析语义版本以识别需要更新的 AVM 模块
1. **审查**: 对于破坏性变更，使用 `#fetch` 工具获取文档：`https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}`
1. **更新**: 使用 `#editFiles` 工具应用版本更新和参数变更
1. **验证**: 使用 `#runCommands` 工具运行 `bicep lint` 和 `bicep build` 以确保符合规范。
1. **输出**: 以表格形式汇总变更，并在下方提供更新摘要。

## 工具使用

如果可用，始终使用工具 `#search`、`#searchResults`、`#fetch`、`#editFiles`、`#runCommands`、`#todos`。避免编写代码执行任务。

## 破坏性变更政策

⚠️ **如更新涉及以下内容，请暂停以获得批准**：

- 不兼容的参数更改
- 安全/合规性修改
- 行为变更

## 输出格式

仅以表格形式显示结果，并使用图标：

```markdown
| 模块 | 当前版本 | 最新版本 | 状态 | 操作 | 文档 |
|------|----------|----------|------|------|------|
| avm/res/compute/vm | 0.1.0 | 0.2.0 | 🔄 | 已更新 | [📖](链接) |
| avm/res/storage/account | 0.3.0 | 0.3.0 | ✅ | 当前版本 | [📖](链接) |

### 更新摘要

描述所作的更新，任何需要手动审查的内容或遇到的问题。
```

## 图标

- 🔄 已更新
- ✅ 当前版本
- ⚠️ 需要人工审查
- ❌ 失败
- 📖 文档

## 要求

- 仅使用 MCR 标签 API 进行版本发现
- 解析 JSON 标签数组并按语义化版本控制排序
- 保持 Bicep 文件的合法性及 lint 合规性
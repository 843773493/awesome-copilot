

---
name: azure-role-selector
description: 当用户需要根据所需权限为标识分配合适角色时，此代理可以帮助他们理解哪种角色能满足需求并实现最小权限访问，以及如何将该角色分配给标识。
allowed-tools: ['Azure MCP/documentation', 'Azure MCP/bicepschema', 'Azure MCP/extension_cli_generate', 'Azure MCP/get_bestpractices']
---
使用 'Azure MCP/documentation' 工具查找与用户希望分配给标识的所需权限相匹配的最小角色定义（如果找不到内置角色满足所需权限，请使用 'Azure MCP/extension_cli_generate' 工具创建具有所需权限的自定义角色定义）。使用 'Azure MCP/extension_cli_generate' 工具生成分配该角色给标识所需的 CLI 命令，并使用 'Azure MCP/bicepschema' 和 'Azure MCP/get_bestpractices' 工具提供一个 Bicep 代码片段，用于添加角色分配。
---
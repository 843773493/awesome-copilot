

# 🎯 代理技能

代理技能是包含指令和捆绑资源的自包含文件夹，用于增强AI在特定任务中的能力。基于[代理技能规范](https://agentskills.io/specification)，每个技能包含一个`SKILL.md`文件，其中包含详细的指令，代理可按需加载这些指令。

与其它基础元素不同，代理技能支持捆绑的资源（脚本、代码示例、参考数据），这些资源在执行特定任务时可供代理使用。
### 如何使用代理技能

**包含内容：**
- 每个技能是一个包含 `SKILL.md` 指令文件的文件夹
- 技能可能包含辅助脚本、代码模板或参考数据
- 技能遵循代理技能规范以实现最大程度的兼容性

**使用时机：**
- 技能适用于需要捆绑资源的复杂且可重复的工作流程
- 在需要代码模板、辅助工具或参考数据时使用技能
- 技能提供渐进式披露功能，仅在特定任务需要时加载

**使用方法：**
- 浏览下方的技能表以查找相关功能
- 将技能文件夹复制到本地技能目录
- 在提示中引用技能，或让代理自动发现它们

| 名称 | 描述 | 捆绑资源 |
| ---- | ----------- | -------------- |
| [appinsights-instrumentation](../skills/appinsights-instrumentation/SKILL.md) | 对网络应用进行仪器化，将其有用的遥测数据发送到 Azure 应用洞察 | `LICENSE.txt`<br />`examples/appinsights.bicep`<br />`references/ASPNETCORE.md`<br />`references/AUTO.md`<br />`references/NODEJS.md`<br />`references/PYTHON.md`<br />`scripts/appinsights.ps1` |
| [azure-role-selector](../skills/azure-role-selector/SKILL.md) | 当用户需要根据所需权限确定应分配给身份的角色时，此代理可以帮助他们理解如何选择具有最小特权访问权限的角色，并指导如何应用该角色。 | `LICENSE.txt` |
| [github-issues](../skills/github-issues/SKILL.md) | 使用MCP工具创建、更新和管理GitHub问题。当用户希望创建错误报告、功能请求或任务问题，更新现有问题，添加标签/指派者/里程碑，或管理问题工作流时，使用此技能。触发词包括“创建问题”、“提交错误”、“请求功能”、“更新问题X”或任何GitHub问题管理任务。 | `references/templates.md` |
| [nuget-manager](../skills/nuget-manager/SKILL.md) | 管理.NET项目/解决方案中的NuGet包。在添加、删除或更新NuGet包版本时使用此技能。它强制使用`dotnet` CLI进行包管理，并仅在更新版本时提供严格的直接文件编辑流程。 | 无 |
| [snowflake-semanticview](../skills/snowflake-semanticview/SKILL.md) | 使用Snowflake CLI（snow）创建、修改和验证Snowflake语义视图。当被要求使用CREATE/ALTER SEMANTIC VIEW构建或排查语义视图/语义层定义时，或验证语义视图DDL与Snowflake通过CLI进行交互时，或指导Snowflake CLI安装和连接配置时使用。 | 无 |
| [vscode-ext-commands](../skills/vscode-ext-commands/SKILL.md) | 在VS Code扩展中贡献命令的指南。指示命名规范、可见性、本地化及其他相关属性，遵循VS Code扩展开发指南、库和最佳实践 | 无 |
| [vscode-ext-localization](../skills/vscode-ext-localization/SKILL.md) | 遵循VS Code扩展开发指南、库和最佳实践的VS Code扩展正确本地化的指南 | 无 |
| [web-design-reviewer](../skills/web-design-reviewer/SKILL.md) | 该技能可对本地或远程运行的网站进行视觉检查，以识别并修复设计问题。触发词包括“审查网站设计”、“检查UI”、“修复布局”、“查找设计问题”。检测响应式设计、可访问性、视觉一致性及布局破坏等问题，并在源代码层面进行修复。 | `references/framework-fixes.md`<br />`references/visual-checklist.md` |
| [webapp-testing](../skills/webapp-testing/SKILL.md) | 使用Playwright与本地Web应用程序进行交互和测试的工具包。支持验证前端功能、调试UI行为、捕获浏览器截图以及查看浏览器日志。 | `test-helper.js` |
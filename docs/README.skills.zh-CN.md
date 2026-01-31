# 🎯 Agent技能

Agent技能是包含指令和捆绑资源的独立文件夹，用于增强AI在特定任务中的能力。基于[Agent技能规范](https://agentskills.io/specification)，每个技能包含一个`SKILL.md`文件，其中详细说明了代理在需要时加载的指令。

与其它基础元素不同，技能支持捆绑资产（脚本、代码示例、参考数据），代理在执行特定任务时可以利用这些资源。

### 如何使用Agent技能

**包含内容：**

- 每个技能是一个文件夹，包含一个`SKILL.md`指令文件
- 技能可能包含辅助脚本、代码模板或参考数据
- 技能遵循Agent技能规范以实现最大程度的兼容性

**使用时机：**

- 技能适用于需要捆绑资源的复杂、可重复的工作流程
- 当您需要代码模板、辅助工具或参考数据时使用技能
- 技能提供渐进式披露机制——仅在特定任务需要时加载

**使用方法：**

- 浏览下方技能表以查找相关功能
- 将技能文件夹复制到本地技能目录
- 在提示中引用技能，或让代理自动发现技能

| 名称 | 描述 | 捆绑资源 |
| ---- | ----------- | -------------- |
| [appinsights-instrumentation](../skills/appinsights-instrumentation/SKILL.md) | 使用SWA CLI为Web应用进行仪器化，将有用的遥测数据发送到Azure App Insights | `LICENSE.txt`<br />`SKILL.zh-CN.md`<br />`examples/appinsights.bicep`<br />`references/ASPNETCORE.md`<br />`references/ASPNETCORE.zh-CN.md`<br />`references/AUTO.md`<br />`references/AUTO.zh-CN.md`<br />`references/NODEJS.md`<br />`references/NODEJS.zh-CN.md`<br />`references/PYTHON.md`<br />`references/PYTHON.zh-CN.md`<br />`scripts/appinsights.ps1` |
| [azure-resource-visualizer](../skills/azure-resource-visualizer/SKILL.md) | 分析Azure资源组并生成详细的Mermaid架构图，展示各个资源之间的关系。当用户请求其Azure资源的图表或需要理解资源之间关系时使用此技能 | `LICENSE.txt`<br />`SKILL.zh-CN.md`<br />`assets/template-architecture.md`<br />`assets/template-architecture.zh-CN.md` |
| [azure-role-selector](../skills/azure-role-selector/SKILL.md) | 当用户需要根据所需权限为身份分配角色时，此代理帮助他们理解如何以最小特权访问的方式满足需求，并指导如何应用该角色 | `LICENSE.txt`<br />`SKILL.zh-CN.md` |
| [azure-static-web-apps](../skills/azure-static-web-apps/SKILL.md) | 使用SWA CLI帮助创建、配置和部署Azure静态Web应用。当部署静态站点到Azure、设置SWA本地开发、配置staticwebapp.config.json、添加Azure Functions API到SWA，或设置GitHub Actions CI/CD用于静态Web应用时使用 | 无 |
| [github-issues](../skills/github-issues/SKILL.md) | 使用MCP工具创建、更新和管理GitHub问题。当用户需要创建错误报告、功能请求或任务问题，更新现有问题，添加标签/指派者/里程碑，或管理问题工作流时使用此技能。触发请求包括“创建问题”、“提交错误”、“请求功能”、“更新问题X”或任何GitHub问题管理任务 | `SKILL.zh-CN.md`<br />`references/templates.md`<br />`references/templates.zh-CN.md` |
| [make-skill-template](../skills/make-skill-template/SKILL.md) | 从提示或通过复制此模板来创建新的GitHub Copilot Agent技能。当被要求“创建技能”、“制作新技能”、“生成技能框架”或构建包含捆绑资源的专用AI能力时使用 | 生成带有正确前置内容、目录结构和可选脚本/参考/资产文件夹的SKILL.md文件 |
| [microsoft-code-reference](../skills/microsoft-code-reference/SKILL.md) | 查询Microsoft API参考，查找可用的代码示例，并验证SDK代码是否正确。当使用Azure SDKs、.NET库或Microsoft API时使用——查找正确的方法、检查参数、获取可用示例或排查错误。通过查询官方文档来识别虚构的方法、错误的签名和过时的模式 | 无 |
| [microsoft-docs](../skills/microsoft-docs/SKILL.md) | 查询官方Microsoft文档以理解概念、查找教程并学习服务的工作原理。适用于Azure、.NET、Microsoft 365、Windows、Power Platform及所有Microsoft技术。从learn.microsoft.com和其他官方Microsoft网站获取准确且最新的信息——架构概述、快速入门、配置指南、限制和最佳实践 | 无 |
| [nuget-manager](../skills/nuget-manager/SKILL.md) | 管理.NET项目/解决方案中的NuGet包。当需要添加、删除或更新NuGet包版本时使用此技能。它强制使用`dotnet` CLI进行包管理，并在更新版本时仅允许严格地直接编辑文件 | `SKILL.zh-CN.md` |
| [snowflake-semanticview](../skills/snowflake-semanticview/SKILL.md) | 使用Snowflake CLI（snow）创建、修改和验证Snowflake语义视图。当被要求使用CREATE/ALTER SEMANTIC VIEW构建或排查语义视图/语义层定义时使用，或验证语义视图DDL与Snowflake的CLI交互，或指导Snowflake CLI的安装和连接配置时使用 | `SKILL.zh-CN.md` |
| [vscode-ext-commands](../skills/vscode-ext-commands/SKILL.md) | 贡献VS Code扩展命令的指南。指示命名规范、可见性、本地化及其他相关属性，遵循VS Code扩展开发指南、库和最佳实践 | `SKILL.zh-CN.md` |
| [vscode-ext-localization](../skills/vscode-ext-localization/SKILL.md) | 遵循VS Code扩展开发指南、库和最佳实践，关于正确本地化VS Code扩展的指南 | `SKILL.zh-CN.md` |
| [web-design-reviewer](../skills/web-design-reviewer/SKILL.md) | 该技能可对本地或远程运行的网站进行视觉检查，以识别并修复设计问题。触发请求包括“审查网站设计”、“检查用户界面”、“修复布局”、“查找设计问题”。检测响应式设计、可访问性、视觉一致性及布局破坏问题，并在源代码层面执行修复 | `SKILL.zh-CN.md`<br />`references/framework-fixes.md`<br />`references/framework-fixes.zh-CN.md`<br />`references/visual-checklist.md`<br />`references/visual-checklist.zh-CN.md` |
| [webapp-testing](../skills/webapp-testing/SKILL.md) | 使用Playwright与本地Web应用进行交互和测试的工具集。支持验证前端功能、调试用户界面行为、捕获浏览器截图和查看浏览器日志 | `SKILL.zh-CN.md`<br />`test-helper.js` |

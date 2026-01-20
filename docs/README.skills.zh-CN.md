# 🎯 智能体技能

智能体技能是包含指令和捆绑资源的独立文件夹，这些资源可增强AI在特定任务中的能力。根据[智能体技能规范](https://agentskills.io/specification)，每个技能包含一个`SKILL.md`文件，其中包含详细的指导说明，智能体可按需加载这些说明。

与其它基础单元不同，智能体技能支持捆绑资产（如脚本、代码示例、参考数据），这些资产可在执行特定任务时被智能体使用。
### 如何使用智能体技能

**包含内容：**
- 每个技能是一个包含`SKILL.md`指令文件的文件夹
- 技能可能包含辅助脚本、代码模板或参考数据
- 技能遵循智能体技能规范以实现最大兼容性

**适用场景：**
- 技能适用于需要捆绑资源的复杂、可重复的工作流程
- 当您需要代码模板、辅助工具或参考数据配合指令时使用技能
- 技能提供渐进式披露机制 - 仅在特定任务需要时加载

**使用方法：**
- 浏览下方技能列表以查找相关功能
- 将技能文件夹复制到本地技能目录
- 在提示中引用技能，或让智能体自动发现技能

| 名称 | 描述 | 捆绑资产 |
| ---- | ----------- | -------------- |
| [appinsights-instrumentation](../skills/appinsights-instrumentation/SKILL.md) | 对网络应用进行仪器化，将其有用的遥测数据发送到 Azure 应用洞察（App Insights） | `LICENSE.txt`<br />`SKILL.zh-CN.md`<br />`examples/appinsights.bicep`<br />`references/ASPNETCORE.md`<br />`references/ASPNETCORE.zh-CN.md`<br />`references/AUTO.md`<br />`references/AUTO.zh-CN.md`<br />`references/NODEJS.md`<br />`references/NODEJS.zh-CN.md`<br />`references/PYTHON.md`<br />`references/PYTHON.zh-CN.md`<br />`scripts/appinsights.ps1` |
| [azure-resource-visualizer](../skills/azure-resource-visualizer/SKILL.md) | 分析 Azure 资源组并生成详细的 Mermaid 架构图，展示各个资源之间的关系。当用户要求绘制 Azure 资源图或帮助理解资源间关系时使用此技能。 | `LICENSE.txt`<br />`SKILL.zh-CN.md`<br />`assets/template-architecture.md`<br />`assets/template-architecture.zh-CN.md` |
| [azure-role-selector](../skills/azure-role-selector/SKILL.md) | 当用户询问应为某个身份分配何种角色以满足特定权限需求时，此智能体帮助用户理解如何选择具有最小特权访问的合适角色，并指导如何应用该角色。 | `LICENSE.txt`<br />`SKILL.zh-CN.md` |
| [github-issues](../skills/github-issues/SKILL.md) | 使用 MCP 工具创建、更新和管理 GitHub 问题。当用户需要创建错误报告、功能请求或任务问题，更新现有问题，添加标签/分配者/里程碑，或管理问题工作流时使用此技能。触发请求包括 "创建问题"、"提交错误"、"请求功能"、"更新问题 X" 或任何 GitHub 问题管理任务。 | `SKILL.zh-CN.md`<br />`references/templates.md`<br />`references/templates.zh-CN.md` |
| [nuget-manager](../skills/nuget-manager/SKILL.md) | 管理 .NET 项目/解决方案中的 NuGet 包。当需要添加、删除或更新 NuGet 包版本时使用此技能。它强制使用 `dotnet` CLI 进行包管理，并在更新版本时仅允许严格直接文件编辑。 | `SKILL.zh-CN.md` |
| [snowflake-semanticview](../skills/snowflake-semanticview/SKILL.md) | 使用 Snowflake CLI（snow）创建、修改和验证 Snowflake 语义视图。当被要求构建或排查语义视图/语义层定义（使用 CREATE/ALTER SEMANTIC VIEW），通过 CLI 验证语义视图 DDL 与 Snowflake 的兼容性，或指导 Snowflake CLI 安装和连接配置时使用此技能。 | `SKILL.zh-CN.md` |
| [vscode-ext-commands](../skills/vscode-ext-commands/SKILL.md) | 为 VS Code 扩展贡献命令的指南。指示命名规范、可见性、本地化等其他相关属性，遵循 VS Code 扩展开发指南、库和最佳实践 | `SKILL.zh-CN.md` |
| [vscode-ext-localization](../skills/vscode-ext-localization/SKILL.md) | 遵循 VS Code 扩展开发指南、库和最佳实践，对 VS Code 扩展进行正确本地化的指南 | `SKILL.zh-CN.md` |
| [web-design-reviewer](../skills/web-design-reviewer/SKILL.md) | 该技能可对本地或远程运行的网站进行视觉检查，以识别和修复设计问题。触发请求包括 "审查网站设计"、"检查 UI"、"修复布局"、"查找设计问题"。检测响应式设计、可访问性、视觉一致性及布局破坏等问题，并在源代码层面执行修复。 | `SKILL.zh-CN.md`<br />`references/framework-fixes.md`<br />`references/framework-fixes.zh-CN.md`<br />`references/visual-checklist.md`<br />`references/visual-checklist.zh-CN.md` |
| [webapp-testing](../skills/webapp-testing/SKILL.md) | 使用 Playwright 与本地 Web 应用进行交互和测试的工具包。支持验证前端功能、调试 UI 行为、捕获浏览器截图和查看浏览器日志。 | `SKILL.zh-CN.md`<br />`test-helper.js` |

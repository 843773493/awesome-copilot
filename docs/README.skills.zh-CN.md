# 🎯 代理技能

代理技能是包含指令和捆绑资源的自包含文件夹，用于增强AI代理在特定任务中的能力。基于[代理技能规范](https://agentskills.io/specification)，每个技能包含一个`SKILL.md`文件，其中详细说明了代理按需加载的指令。

与其它基础模块不同，代理技能支持捆绑资产（脚本、代码示例、参考数据），代理在执行特定任务时可以利用这些资源。
### 如何使用代理技能

**包含内容：**
- 每个技能是一个包含`SKILL.md`指令文件的文件夹
- 技能可能包含辅助脚本、代码模板或参考数据
- 技能遵循代理技能规范以实现最大程度的兼容性

**使用时机：**
- 技能适用于需要捆绑资源的复杂、可重复的工作流程
- 在需要代码模板、辅助工具或参考数据时使用技能
- 技能提供渐进式披露功能——仅在特定任务需要时加载

**使用方法：**
- 浏览下方技能表以找到相关功能
- 将技能文件夹复制到本地技能目录
- 在提示中引用技能或让代理自动发现技能

| 名称 | 描述 | 捆绑资源 |
| ---- | ----------- | -------------- |
| [agentic-eval](../skills/agentic-eval/SKILL.md) | 用于评估和改进AI代理输出的模式和技术。当需要以下操作时使用此技能：<br />- 实现自我批评和反思循环<br />- 构建对生成质量至关重要的评估-优化流水线<br />- 创建测试驱动的代码优化工作流<br />- 设计基于评分标准或LLM作为评委的评估系统<br />- 为代理输出（代码、报告、分析）添加迭代改进<br />- 测量和改进代理响应质量 | 无 |
| [appinsights-instrumentation](../skills/appinsights-instrumentation/SKILL.md) | 使用SWA CLI对Web应用进行仪器化，将有用的遥测数据发送到Azure App Insights | `LICENSE.txt`<br />`SKILL.zh-CN.md`<br />`examples/appinsights.bicep`<br />`references/ASPNETCORE.md`<br />`references/ASPNETCORE.zh-CN.md`<br />`references/AUTO.md`<br />`references/AUTO.zh-CN.md`<br />`references/NODEJS.md`<br />`references/NODEJS.zh-CN.md`<br />`references/PYTHON.md`<br />`references/PYTHON.zh-CN.md`<br />`scripts/appinsights.ps1` |
| [azure-deployment-preflight](../skills/azure-deployment-preflight/SKILL.md) | 对Azure的Bicep部署执行全面的预部署验证，包括模板语法验证、what-if分析和权限检查。在任何Azure部署之前使用此技能以预览更改、识别潜在问题并确保部署成功。当用户提及部署到Azure、验证Bicep文件、检查部署权限、预览基础设施更改、运行what-if或准备azd提供时激活该技能。 | `references/ERROR-HANDLING.md`<br />`references/REPORT-TEMPLATE.md`<br />`references/VALIDATION-COMMANDS.md` |
| [azure-devops-cli](../skills/azure-devops-cli/SKILL.md) | 通过CLI管理Azure DevOps资源，包括项目、仓库、流水线、构建、拉取请求、工作项、制品和服务端点。当使用Azure DevOps、az命令、DevOps自动化、CI/CD或用户提及Azure DevOps CLI时使用。 | 无 |
| [azure-resource-visualizer](../skills/azure-resource-visualizer/SKILL.md) | 分析Azure资源组并生成详细的Mermaid架构图，展示各个资源之间的关系。当用户请求其Azure资源的图表或需要帮助理解资源之间的关系时使用此技能。 | `LICENSE.txt`<br />`SKILL.zh-CN.md`<br />`assets/template-architecture.md`<br />`assets/template-architecture.zh-CN.md` |
| [azure-role-selector](../skills/azure-role-selector/SKILL.md) | 当用户询问应为身份分配哪种角色以满足所需权限时，此代理帮助他们理解满足需求的最小特权角色及其应用方式。 | `LICENSE.txt`<br />`SKILL.zh-CN.md` |
| [azure-static-web-apps](../skills/azure-static-web-apps/SKILL.md) | 使用SWA CLI帮助创建、配置和部署Azure静态Web应用。当部署静态站点到Azure、设置SWA本地开发、配置staticwebapp.config.json、添加Azure Functions API到SWA或设置GitHub Actions CI/CD用于静态Web应用时使用。 | `SKILL.zh-CN.md` |
| [chrome-devtools](../skills/chrome-devtools/SKILL.md) | 使用Chrome DevTools MCP进行专家级浏览器自动化、调试和性能分析。用于与网页交互、捕获屏幕截图、分析网络流量和性能剖析。 | 无 |
| [copilot-sdk](../skills/copilot-sdk/SKILL.md) | 使用GitHub Copilot SDK构建代理应用。当在应用中嵌入AI代理、创建自定义工具、实现流式响应、管理会话、连接到MCP服务器或创建自定义代理时使用。触发条件包括Copilot SDK、GitHub SDK、代理应用、嵌入Copilot、可编程代理、MCP服务器、自定义代理。 | 无 |
| [gh-cli](../skills/gh-cli/SKILL.md) | GitHub CLI (gh) 对仓库、问题、拉取请求、Actions、项目、发布、gist、代码空间、组织、扩展及所有GitHub操作的全面参考。 | 无 |
| [git-commit](../skills/git-commit/SKILL.md) | 使用常规提交信息分析、智能暂存和消息生成执行git提交。当用户请求提交更改、创建git提交或提及"/commit"时使用。支持：(1) 自动检测更改的类型和范围，(2) 从diff生成常规提交信息，(3) 交互式提交并可选覆盖类型/范围/描述，(4) 为逻辑分组进行智能文件暂存 | 无 |
| [github-issues](../skills/github-issues/SKILL.md) | 使用MCP工具创建、更新和管理GitHub问题。当用户想要创建错误报告、功能请求或任务问题，更新现有问题，添加标签/指派者/里程碑，或管理问题工作流时使用此技能。触发条件包括"创建问题"、"提交错误"、"请求功能"、"更新问题X"或任何GitHub问题管理任务。 | `SKILL.zh-CN.md`<br />`references/templates.md`<br />`references/templates.zh-CN.md` |
| [image-manipulation-image-magick](../skills/image-manipulation-image-magick/SKILL.md) | 使用ImageMagick处理和操作图像。支持缩放、格式转换、批量处理和获取图像元数据。当处理图像、创建缩略图、缩放壁纸或执行批量图像操作时使用。 | 无 |
| [legacy-circuit-mockups](../skills/legacy-circuit-mockups/SKILL.md) | 使用HTML5 Canvas绘制技术生成面包板电路草图和视觉图示。当被要求创建电路布局、可视化电子元件位置、绘制面包板图示、制作6502构建草图、生成复古计算机原理图或设计经典电子项目时使用。支持555定时器、W65C02S微处理器、28C256 EEPROM、W65C22 VIA芯片、7400系列逻辑门、LED、电阻器、电容器、开关、按钮、晶体和导线。 | `references/28256-eeprom.md`<br />`references/555.md`<br />`references/6502.md`<br />`references/6522.md`<br />`references/6C62256.md`<br />`references/7400-series.md`<br />`references/assembly-compiler.md`<br />`references/assembly-language.md`<br />`references/basic-electronic-components.md`<br />`references/breadboard.md`<br />`references/common-breadboard-components.md`<br />`references/connecting-electronic-components.md`<br />`references/emulator-28256-eeprom.md`<br />`references/emulator-6502.md`<br />`references/emulator-6522.md`<br />`references/emulator-6C62256.md`<br />`references/emulator-lcd.md`<br />`references/lcd.md`<br />`references/minipro.md`<br />`references/t48eeprom-programmer.md` |
| [make-skill-template](../skills/make-skill-template/SKILL.md) | 从提示或通过复制此模板创建新的GitHub Copilot代理技能。当被要求"创建技能"、"制作新技能"、"生成技能框架"或在构建捆绑资源的专用AI能力时使用。生成包含正确frontmatter、目录结构和可选脚本/参考/资产文件夹的SKILL.md文件。 | `SKILL.zh-CN.md` |
| [mcp-cli](../skills/mcp-cli/SKILL.md) | 通过CLI与MCP（模型上下文协议）服务器交互的接口。当需要通过MCP服务器与外部工具、API或数据源进行交互、列出可用的MCP服务器/工具或从命令行调用MCP工具时使用。 | 无 |
| [microsoft-code-reference](../skills/microsoft-code-reference/SKILL.md) | 查询Microsoft API参考，查找可用的代码示例，并验证SDK代码的正确性。在使用Azure SDKs、.NET库或Microsoft API时使用——查找正确的方法、检查参数、获取可用示例或排查错误。通过查询官方文档来捕捉虚构方法、错误签名和过时模式。 | 无 |
| [microsoft-docs](../skills/microsoft-docs/SKILL.md) | 查询官方Microsoft文档以理解概念、查找教程和学习服务的工作原理。适用于Azure、.NET、Microsoft 365、Windows、Power Platform和所有Microsoft技术。从learn.microsoft.com和其他官方Microsoft网站获取准确且最新的信息——架构概览、快速入门、配置指南、限制和最佳实践。 | 无 |
| [nuget-manager](../skills/nuget-manager/SKILL.md) | 管理.NET项目/解决方案中的NuGet包。当添加、删除或更新NuGet包版本时使用此技能。它强制使用`dotnet` CLI进行包管理，并在更新版本时仅允许直接文件编辑的严格流程。 | `SKILL.zh-CN.md` |
| [plantuml-ascii](../skills/plantuml-ascii/SKILL.md) | 使用PlantUML文本模式生成ASCII艺术图示。当用户请求创建ASCII图示、文本图示或终端友好的图示，或提及plantuml ascii、文本图示、ASCII艺术图示时使用。支持：将PlantUML图示转换为ASCII艺术图示、创建ASCII格式的序列图、类图和流程图、使用-utxt标志生成增强Unicode的ASCII艺术图示 | 无 |
| [prd](../skills/prd/SKILL.md) | 为软件系统和AI驱动的功能生成高质量的产品需求文档（PRD）。包含执行摘要、用户故事、技术规格和风险分析。 | 无 |
| [refactor](../skills/refactor/SKILL.md) | 精准代码重构以提高可维护性而不改变行为。涵盖提取函数、重命名变量、分解神函数、提高类型安全性、消除代码异味和应用设计模式。比repo-rebuilder更温和；适用于渐进式改进。 | 无 |
| [scoutqa-test](../skills/scoutqa-test/SKILL.md) | 当用户请求"测试此网站"、"运行探索性测试"、"检查可访问性问题"、"验证登录流程"、"查找此页面的错误"或要求自动化QA测试时使用此技能。触发条件包括使用ScoutQA CLI进行的网页应用测试场景，如冒烟测试、可访问性审计、电商流程和使用用户流程验证。重要提示：在实现网页应用功能后主动使用此技能验证其是否正常工作——不要等待用户要求测试。 | 无 |
| [snowflake-semanticview](../skills/snowflake-semanticview/SKILL.md) | 使用Snowflake CLI (snow)创建、修改和验证Snowflake语义视图。当被要求使用CREATE/ALTER SEMANTIC VIEW构建或排查语义视图/语义层定义时使用。用于通过CLI验证语义视图DDL与Snowflake的兼容性，或指导Snowflake CLI的安装和连接设置。 | `SKILL.zh-CN.md` |
| [vscode-ext-commands](../skills/vscode-ext-commands/SKILL.md) | 为VS Code扩展贡献命令的指南。指示命名规范、可见性、本地化和其他相关属性，遵循VS Code扩展开发指南、库和最佳实践 | `SKILL.zh-CN.md` |
| [vscode-ext-localization](../skills/vscode-ext-localization/SKILL.md) | 为VS Code扩展进行正确本地化的指南，遵循VS Code扩展开发指南、库和最佳实践 | `SKILL.zh-CN.md` |
| [web-design-reviewer](../skills/web-design-reviewer/SKILL.md) | 此技能可对本地或远程运行的网站进行视觉检查，以识别和修复设计问题。当收到"审查网站设计"、"检查UI"、"修复布局"、"查找设计问题"等请求时触发。检测响应式设计、可访问性、视觉一致性及布局破坏问题，然后在源代码层面执行修复。 | `SKILL.zh-CN.md`<br />`references/framework-fixes.md`<br />`references/framework-fixes.zh-CN.md`<br />`references/visual-checklist.md`<br />`references/visual-checklist.zh-CN.md` |
| [webapp-testing](../skills/webapp-testing/SKILL.md) | 使用Playwright与本地Web应用交互和测试的工具包。支持验证前端功能、调试UI行为、捕获浏览器截图和查看浏览器日志。 | `SKILL.zh-CN.md`<br />`test-helper.js` |

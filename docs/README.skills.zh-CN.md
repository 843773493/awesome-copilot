# 🎯 代理技能

代理技能是包含指令和捆绑资源的独立文件夹，用于增强AI代理在特定任务中的能力。基于[代理技能规范](https://agentskills.io/specification)，每个技能包含一个`SKILL.md`文件，其中详细说明了代理按需加载的指令。

与其它基础组件不同，代理技能支持捆绑资产（脚本、代码示例、参考数据），代理在执行特定任务时可以利用这些资产。
### 如何使用代理技能

**包含内容：**
- 每个技能是一个包含`SKILL.md`指令文件的文件夹
- 技能可能包含辅助脚本、代码模板或参考数据
- 技能遵循代理技能规范以实现最大兼容性

**使用时机：**
- 技能适用于复杂且可重复的工作流，这些工作流能够从捆绑资源中受益
- 在需要代码模板、辅助工具或参考数据时使用技能
- 技能提供渐进式披露功能，仅在特定任务需要时加载

**使用方法：**
- 浏览下方技能表以找到相关能力
- 将技能文件夹复制到本地技能目录
- 在提示中引用技能或让代理自动发现它们

| 名称 | 描述 | 捆绑资产 |
| ---- | ----------- | -------------- |
| [agentic-eval](../skills/agentic-eval/SKILL.md) | 用于评估和改进AI代理输出的模式和技术。在以下情况下使用本技能：<br />- 实现自我批评和反思循环<br />- 构建对生成质量至关重要的评估-优化管道<br />- 创建测试驱动的代码优化工作流<br />- 设计基于评分标准或LLM作为裁判的评估系统<br />- 为代理输出（代码、报告、分析）添加迭代改进<br />- 测量和改进代理响应质量 | 无 |
| [appinsights-instrumentation](../skills/appinsights-instrumentation/SKILL.md) | 使用SWA CLI为Web应用配置Azure应用洞察的遥测数据 | `LICENSE.txt`<br />`examples/appinsights.bicep`<br />`references/ASPNETCORE.md`<br />`references/AUTO.md`<br />`references/NODEJS.md`<br />`references/PYTHON.md`<br />`scripts/appinsights.ps1` |
| [aspire](../skills/aspire/SKILL.md) | 覆盖Aspire CLI、AppHost编排、服务发现、集成、MCP服务器、VS Code扩展、Dev Containers、GitHub Codespaces、模板、仪表板和部署的Aspire技能。当用户要求创建、运行、调试、配置、部署或排查Aspire分布式应用时使用本技能。 | `references/architecture.md`<br />`references/cli-reference.md`<br />`references/dashboard.md`<br />`references/deployment.md`<br />`references/integrations-catalog.md`<br />`references/mcp-server.md`<br />`references/polyglot-apis.md`<br />`references/testing.md`<br />`references/troubleshooting.md` |
| [azure-deployment-preflight](../skills/azure-deployment-preflight/SKILL.md) | 对Azure的Bicep部署执行全面的预部署验证，包括模板语法验证、what-if分析和权限检查。在任何Azure部署之前使用本技能以预览更改、识别潜在问题并确保部署成功。当用户提到部署到Azure、验证Bicep文件、检查部署权限、预览基础设施更改、运行what-if或准备azd提供时激活本技能。 | `references/ERROR-HANDLING.md`<br />`references/REPORT-TEMPLATE.md`<br />`references/VALIDATION-COMMANDS.md` |
| [azure-devops-cli](../skills/azure-devops-cli/SKILL.md) | 通过CLI管理Azure DevOps资源，包括项目、仓库、流水线、构建、拉取请求、工作项、制品和服务端点。在使用Azure DevOps、az命令、DevOps自动化、CI/CD或用户提到Azure DevOps CLI时使用本技能。 | 无 |
| [azure-resource-visualizer](../skills/azure-resource-visualizer/SKILL.md) | 分析Azure资源组并生成详细Mermaid架构图，展示各资源之间的关系。当用户要求其Azure资源的图示或帮助理解资源之间的关系时使用本技能。 | `LICENSE.txt`<br />`SKILL.zh-CN.md`<br />`assets/template-architecture.md`<br />`assets/template-architecture.zh-CN.md` |
| [azure-role-selector](../skills/azure-role-selector/SKILL.md) | 当用户询问应为某个身份分配哪种角色以满足所需权限时，本代理帮助其理解哪种角色可以实现最小特权访问，并指导如何应用该角色。 | `LICENSE.txt`<br />`SKILL.zh-CN.md` |
| [azure-static-web-apps](../skills/azure-static-web-apps/SKILL.md) | 使用SWA CLI帮助创建、配置和部署Azure静态Web应用。在部署静态站点到Azure、设置SWA本地开发、配置`staticwebapp.config.json`、添加Azure Functions API到SWA或设置GitHub Actions CI/CD用于静态Web应用时使用本技能。 | `SKILL.zh-CN.md` |
| [chrome-devtools](../skills/chrome-devtools/SKILL.md) | 使用Chrome DevTools MCP进行高级浏览器自动化、调试和性能分析。用于与网页交互、捕获截图、分析网络流量和性能剖析。 | 无 |
| [copilot-cli-quickstart](../skills/copilot-cli-quickstart/SKILL.md) | 当有人希望从零开始学习GitHub Copilot CLI时使用本技能。提供交互式的分步教程，包含开发者和非开发者轨道，以及按需问答。只需说"开始教程"或提出问题即可！注意：本技能专门针对GitHub Copilot CLI，使用CLI专用工具（ask_user、sql、fetch_copilot_cli_documentation）。 | 无 |
| [copilot-sdk](../skills/copilot-sdk/SKILL.md) | 使用GitHub Copilot SDK构建代理应用。在将AI代理嵌入应用、创建自定义工具、实现流式响应、管理会话、连接到MCP服务器或创建自定义代理时使用本技能。触发条件包括Copilot SDK、GitHub SDK、代理应用、嵌入Copilot、可编程代理、MCP服务器、自定义代理。 | 无 |
| [create-web-form](../skills/create-web-form/SKILL.md) | 创建结构良好、可访问的网页表单，涵盖HTML结构、CSS样式、JavaScript交互性、表单验证和服务器端处理的最佳实践。当用户要求"创建表单"、"构建网页表单"、"添加联系表单"、"制作注册表单"或构建任何具有数据处理的HTML表单时使用本技能。涵盖PHP和Python后端、MySQL数据库集成、REST API、XML数据交换、可访问性（ARIA）和渐进式网页应用。 | `references/basic-markdown-to-html.md`<br />`references/basic-markdown.md`<br />`references/code-blocks-to-html.md`<br />`references/code-blocks.md`<br />`references/collapsed-sections-to-html.md`<br />`references/collapsed-sections.md`<br />`references/gomarkdown.md`<br />`references/hugo.md`<br />`references/jekyll.md`<br />`references/marked.md`<br />`references/pandoc.md`<br />`references/tables-to-html.md`<br />`references/tables.md`<br />`references/writing-mathematical-expressions-to-html.md`<br />`references/writing-mathematical-expressions.md` |
| [mcp-cli](../skills/mcp-cli/SKILL.md) | 通过CLI与MCP（模型上下文协议）服务器进行交互的接口。在需要通过MCP服务器与外部工具、API或数据源进行交互、列出可用的MCP服务器/工具或从命令行调用MCP工具时使用本技能。 | 无 |
| [meeting-minutes](../skills/meeting-minutes/SKILL.md) | 生成内部会议的简洁、可执行的会议纪要。包括元数据、与会者、议程、决策、待办事项（负责人 + 截止日期）和后续步骤。 | 无 |
| [microsoft-code-reference](../skills/microsoft-code-reference/SKILL.md) | 查询Microsoft API参考文档，查找可用的代码示例并验证SDK代码是否正确。在使用Azure SDKs、.NET库或Microsoft API时使用本技能——查找正确的方法、检查参数、获取工作示例或排查错误。通过查询官方文档来捕捉虚构的方法、错误的签名和过时的模式。 | 无 |
| [microsoft-docs](../skills/microsoft-docs/SKILL.md) | 查询官方Microsoft文档，查找Azure、.NET、Agent Framework、Aspire、VS Code、GitHub等领域的概念、教程和代码示例。默认使用Microsoft Learn MCP，对于不在learn.microsoft.com上的内容使用Context7和Aspire MCP。 | 无 |
| [microsoft-skill-creator](../skills/microsoft-skill-creator/SKILL.md) | 使用Learn MCP工具创建针对Microsoft技术的代理技能。当用户希望创建一个教授代理任何Microsoft技术、库、框架或服务（如Azure、.NET、M365、VS Code、Bicep等）的技能时使用本技能。深入调查主题后，生成一个混合技能，将关键知识本地存储，同时支持动态深入调查。 | `references/skill-templates.md` |
| [nano-banana-pro-openrouter](../skills/nano-banana-pro-openrouter/SKILL.md) | 通过OpenRouter使用Gemini 3 Pro图像模型生成或编辑图像。适用于仅提示生成图像、图像编辑和多图像合成；支持1K/2K/4K输出。 | `assets/SYSTEM_TEMPLATE`<br />`scripts/generate_image.py` |
| [nuget-manager](../skills/nuget-manager/SKILL.md) | 管理.NET项目/解决方案中的NuGet包。在添加、删除或更新NuGet包版本时使用本技能。它强制使用`dotnet` CLI进行包管理，并在更新版本时仅提供严格的直接文件编辑流程。 | 无 |
| [penpot-uiux-design](../skills/penpot-uiux-design/SKILL.md) | 使用MCP工具在Penpot中创建专业UI/UX设计的全面指南。在以下情况下使用本技能：(1) 为Web、移动或桌面应用创建新的UI/UX设计；(2) 使用组件和令牌构建设计系统；(3) 设计仪表板、表单、导航或着陆页；(4) 应用可访问性标准和最佳实践；(5) 遵循平台指南（iOS、Android、Material Design）；(6) 审查或改进现有Penpot设计以提高可用性。触发条件包括"设计UI"、"创建界面"、"构建布局"、"设计仪表板"、"创建表单"、"设计着陆页"、"使其可访问"、"设计系统"、"组件库"。 | `references/accessibility.md`<br />`references/component-patterns.md`<br />`references/platform-guidelines.md`<br />`references/setup-troubleshooting.md` |
| [plantuml-ascii](../skills/plantuml-ascii/SKILL.md) | 使用PlantUML文本模式生成ASCII艺术图。当用户要求创建ASCII图、基于文本的图、终端友好的图或提及plantuml ascii、文本图、ASCII艺术图时使用本技能。支持：将PlantUML图转换为ASCII艺术、创建ASCII格式的序列图、类图、流程图，以及使用-utxt标志生成增强Unicode的ASCII艺术。 | 无 |
| [powerbi-modeling](../skills/powerbi-modeling/SKILL.md) | 用于构建优化数据模型的Power BI语义建模助手。在使用Power BI语义模型、创建度量、设计星型架构、配置关系、实现RLS或优化模型性能时使用本技能。触发条件包括关于DAX计算、表关系、维度/事实表设计、命名约定、模型文档、基数、跨过滤方向、计算组和数据模型最佳实践的查询。始终使用power-bi-modeling MCP工具连接到当前模型，以理解数据结构后再提供指导。 | `references/MEASURES-DAX.md`<br />`references/PERFORMANCE.md`<br />`references/RELATIONSHIPS.md`<br />`references/RLS.md`<br />`references/STAR-SCHEMA.md` |
| [prd](../skills/prd/SKILL.md) | 为软件系统和AI驱动的功能生成高质量的产品需求文档（PRD）。包括执行摘要、用户故事、技术规格和风险分析。 | 无 |
| [refactor](../skills/refactor/SKILL.md) | 进行手术式代码重构以提高可维护性而不改变行为。涵盖提取函数、重命名变量、拆分god函数、改进类型安全性、消除代码异味并应用设计模式。比repo-rebuilder更温和；适用于渐进式改进。 | 无 |
| [scoutqa-test](../skills/scoutqa-test/SKILL.md) | 当用户要求"测试这个网站"、"运行探索性测试"、"检查可访问性问题"、"验证登录流程"、"在该页面上查找错误"或请求自动化QA测试时使用本技能。触发条件包括使用ScoutQA CLI进行的Web应用测试场景，如冒烟测试、可访问性审计、电子商务流程和用户流程验证。重要提示：在实现Web应用功能后主动使用本技能以验证其是否正常工作——不要等到用户要求测试才使用。 | 无 |
| [snowflake-semanticview](../skills/snowflake-semanticview/SKILL.md) | 使用Snowflake CLI（snow）创建、修改和验证Snowflake语义视图。当用户要求使用CREATE/ALTER SEMANTIC VIEW构建或排查语义视图/语义层定义时使用本技能，以通过CLI验证语义视图DDL，或指导Snowflake CLI安装和连接配置。 | 无 |
| [sponsor-finder](../skills/sponsor-finder/SKILL.md) | 通过GitHub Sponsors查找GitHub仓库依赖项中哪些是可赞助的。使用deps.dev API解析npm、PyPI、Cargo、Go、RubyGems、Maven和NuGet的依赖关系。检查npm资助元数据、FUNDING.yml文件和网络搜索。验证所有链接。显示直接和间接依赖项，并结合OSSF Scorecard健康数据。通过提供GitHub所有者/仓库（例如"expressjs/express"）来调用本技能。 | 无 |
| [terraform-azurerm-set-diff-analyzer](../skills/terraform-azurerm-set-diff-analyzer/SKILL.md) | 分析AzureRM提供者的Terraform计划JSON输出，以区分虚假正向差异（集合类型属性的顺序变化）和实际资源变化。在审查Azure资源（如应用网关、负载均衡器、防火墙、前端门、NSG等）的Terraform计划输出时使用本技能，这些资源由于内部顺序变化可能产生虚假差异。 | `references/azurerm_set_attributes.json`<br />`references/azurerm_set_attributes.md`<br />`scripts/.gitignore`<br />`scripts/README.md`<br />`scripts/analyze_plan.py` |
| [vscode-ext-commands](../skills/vscode-ext-commands/SKILL.md) | 为VS Code扩展贡献命令的指南。指示命名约定、可见性、本地化和其他相关属性，遵循VS Code扩展开发指南、库和最佳实践。 | 无 |
| [vscode-ext-localization](../skills/vscode-ext-localization/SKILL.md) | 遵循VS Code扩展开发指南、库和最佳实践的本地化指南。 | 无 |
| [web-design-reviewer](../skills/web-design-reviewer/SKILL.md) | 本技能可对本地或远程运行的网站进行视觉检查，以识别和修复设计问题。触发请求包括"审查网站设计"、"检查UI"、"修复布局"、"查找设计问题"。检测响应式设计、可访问性、视觉一致性及布局破坏问题，然后在源代码层面进行修复。 | `references/framework-fixes.md`<br />`references/visual-checklist.md` |
| [webapp-testing](../skills/webapp-testing/SKILL.md) | 使用Playwright与本地Web应用进行交互和测试的工具包。支持验证前端功能、调试UI行为、捕获浏览器截图和查看浏览器日志。 | `test-helper.js` |
| [winapp-cli](../skills/winapp-cli/SKILL.md) | 用于构建、打包和部署Windows应用的Windows应用开发CLI（winapp）。当用户要求初始化Windows应用项目、创建MSIX包、生成`AppxManifest.xml`、管理开发证书、添加包身份用于调试、签名包或访问Windows SDK构建工具时使用本技能。支持.NET、C++、Electron、Rust、Tauri及针对Windows的跨平台框架。 | 无 |
| [workiq-copilot](../skills/workiq-copilot/SKILL.md) | 指导Copilot CLI如何使用WorkIQ CLI/MCP服务器查询Microsoft 365 Copilot数据（电子邮件、会议、文档、Teams、人员）以获取实时上下文、摘要和建议。 | 无 |

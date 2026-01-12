

# Kotlin MCP 服务器开发

使用官方 io.modelcontextprotocol:kotlin-sdk 库构建 Model Context Protocol（MCP）服务器的完整工具包。包含最佳实践指南、项目生成提示以及专家聊天模式以提供指导。

**标签:** kotlin, mcp, model-context-protocol, kotlin-multiplatform, 服务器开发, ktor

## 本集合中的项目

| 标题 | 类型 | 描述 | MCP 服务器 |
| ----- | ---- | ----------- | ----------- |
| [Kotlin MCP 服务器开发指南](../instructions/kotlin-mcp-server.instructions.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/instructions?url=vscode%3Achat-instructions%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Finstructions%2Fkotlin-mcp-server.instructions.md)<br />[![在 VS Code 内测版中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/instructions?url=vscode-insiders%3Achat-instructions%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Finstructions%2Fkotlin-mcp-server.instructions.md) | 指南 | 使用官方 io.modelcontextprotocol:kotlin-sdk 库构建 Model Context Protocol（MCP）服务器的最佳实践和模式。 |  |
| [Kotlin MCP 服务器项目生成器](../prompts/kotlin-mcp-server-generator.prompt.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Fkotlin-mcp-server-generator.prompt.md)<br />[![在 VS Code 内测版中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode-insiders%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Fkotlin-mcp-server-generator.prompt.md) | 提示 | 使用官方 io.modelcontextprotocol:kotlin-sdk 库生成一个结构完整、依赖项正确且实现完善的 Kotlin MCP 服务器项目。 |  |
| [Kotlin MCP 服务器开发专家](../agents/kotlin-mcp-expert.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fkotlin-mcp-expert.agent.md)<br />[![在 VS Code 内测版中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fkotlin-mcp-expert.agent.md) | 代理 | 使用官方 SDK 构建 Model Context Protocol（MCP）服务器的专家助手。[查看用法](#kotlin-mcp-server-development-expert) |  |

## 集合用法

### Kotlin MCP 服务器开发专家

推荐

此聊天模式为构建 Kotlin MCP 服务器提供专家指导。

此模式适合以下场景：
- 使用 Kotlin 创建新的 MCP 服务器项目
- 实现类型安全工具，结合协程和 kotlinx.serialization
- 使用 Ktor 设置 stdio 或 SSE 传输
- 调试协程模式和 JSON schema 问题
- 学习 Kotlin MCP 最佳实践（使用官方 SDK）
- 构建多平台 MCP 服务器（JVM、Wasm、iOS）

为获得最佳效果，建议：
- 使用指南文件为 Kotlin MCP 开发设置上下文
- 使用提示生成带有 Gradle 的初始项目结构
- 切换到专家聊天模式以获取详细的实现帮助
- 指定是否需要 stdio 或 SSE/HTTP 传输
- 提供所需工具或功能的详细信息
- 提及是否需要多平台支持或特定目标

---

*此集合包含 3 个精选项目，用于 **Kotlin MCP 服务器开发**。*
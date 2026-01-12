

# Rust MCP 服务器开发

使用官方 rmcp SDK 通过异步/等待（async/await）模式、宏（procedural macros）和类型安全的实现方式，构建高性能的 Model Context Protocol 服务器。

**标签:** rust, mcp, model-context-protocol, 服务器开发, sdk, tokio, 异步, 宏, rmcp

## 此集合中的项目

| 标题 | 类型 | 描述 | MCP 服务器 |
| ----- | ---- | ----------- | ----------- |
| [Rust MCP 服务器开发最佳实践](../instructions/rust-mcp-server.instructions.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/instructions?url=vscode%3Achat-instructions%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Finstructions%2Frust-mcp-server.instructions.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/instructions?url=vscode-insiders%3Achat-instructions%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Finstructions%2Frust-mcp-server.instructions.md) | 指南 | 使用官方 rmcp SDK 通过异步/等待模式构建 Model Context Protocol 服务器的最佳实践 |  |
| [Rust Mcp 服务器生成器](../prompts/rust-mcp-server-generator.prompt.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Frust-mcp-server-generator.prompt.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode-insiders%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Frust-mcp-server-generator.prompt.md) | 提示 | 使用官方 rmcp SDK 生成完整的 Rust Model Context Protocol 服务器项目，包含工具、提示、资源和测试 |  |
| [Rust MCP 专家](../agents/rust-mcp-expert.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Frust-mcp-expert.agent.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Frust-mcp-expert.agent.md) | 代理 | 使用 rmcp SDK 和 tokio 异步运行时的 Rust MCP 服务器开发专家助手 [查看用法](#rust-mcp-expert) |  |

## 集合用法

### Rust MCP 专家

推荐

此聊天模式为构建 MCP 服务器提供专家级指导。

此模式适合以下场景：
- 使用 Rust 创建新的 MCP 服务器项目
- 通过 tokio 运行时实现异步处理程序
- 使用 rmcp 宏进行工具开发
- 配置 stdio、SSE 或 HTTP 传输方式
- 调试异步 Rust 和所有权问题
- 学习使用官方 rmcp SDK 的 Rust MCP 最佳实践
- 通过 Arc 和 RwLock 进行性能优化

为了获得最佳效果，建议：
- 使用指南文件为 Rust MCP 开发设置上下文
- 使用提示生成初始项目结构
- 切换到专家聊天模式以获取详细实现帮助
- 指定所需的传输类型
- 提供有关需要的工具或功能的详细信息
- 提及是否需要 OAuth 认证

---

*此集合包含 3 个精选的项目，用于 **Rust MCP 服务器开发**。*
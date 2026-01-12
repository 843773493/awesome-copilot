

# Python MCP服务器开发

使用官方SDK通过FastMCP构建模型上下文协议 (MCP) 服务器的完整工具包。包含最佳实践指南、生成服务器的提示以及专家聊天模式以提供指导。

**标签:** python, mcp, 模型上下文协议, fastmcp, 服务器开发

## 本集合中的项目

| 标题 | 类型 | 描述 | MCP服务器 |
|-----|----|-----------|-----------|
| [Python MCP服务器开发](../instructions/python-mcp-server.instructions.md)<br />[![在VS Code中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/instructions?url=vscode%3Achat-instructions%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Finstructions%2Fpython-mcp-server.instructions.md)<br />[![在VS Code Insiders中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/instructions?url=vscode-insiders%3Achat-instructions%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Finstructions%2Fpython-mcp-server.instructions.md) | 指南 | 使用Python SDK构建模型上下文协议 (MCP) 服务器的指南 |  |
| [生成Python MCP服务器](../prompts/python-mcp-server-generator.prompt.md)<br />[![在VS Code中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Fpython-mcp-server-generator.prompt.md)<br />[![在VS Code Insiders中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode-insiders%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Fpython-mcp-server-generator.prompt.md) | 提示 | 使用工具、资源和正确配置生成完整的Python MCP服务器项目 |  |
| [Python MCP服务器专家](../agents/python-mcp-expert.agent.md)<br />[![在VS Code中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fpython-mcp-expert.agent.md)<br />[![在VS Code Insiders中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fpython-mcp-expert.agent.md) | 代理 | 用于开发Python模型上下文协议 (MCP) 服务器的专家助手 [查看用法](#python-mcp-server-expert) |  |

## 集合使用说明

### Python MCP服务器专家

推荐

此聊天模式为使用FastMCP构建MCP服务器提供专家指导。

此模式适合以下场景：
- 创建新的Python MCP服务器项目
- 实现带类型工具（使用Pydantic模型和结构化输出）
- 设置stdio或可流式传输的HTTP传输
- 调试类型提示和模式验证问题
- 学习FastMCP的Python MCP最佳实践
- 优化服务器性能和资源管理

为了获得最佳效果，建议：
- 使用指令文件为Python/FastMCP开发设置上下文
- 使用提示生成初始项目结构（使用uv）
- 切换到专家聊天模式以获取详细实现帮助
- 指定是否需要stdio或HTTP传输
- 提供所需工具或功能的详细信息
- 提及是否需要结构化输出、采样或引出功能

---

*此集合包含3个针对**Python MCP服务器开发**的精选项目。*
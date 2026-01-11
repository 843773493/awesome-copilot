# 🤖 Awesome GitHub Copilot 自定义功能集合

[![由 Awesome Copilot 提供支持](https://img.shields.io/badge/Powered_by-Awesome_Copilot-blue?logo=githubcopilot)](https://aka.ms/awesome-github-copilot)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![所有贡献者](https://img.shields.io/badge/all_contributors-93-orange.svg?style=flat-square)](#贡献者-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

由社区创建的自定义 Agent、提示词和指令集合，用于在不同领域、编程语言和使用场景中增强 GitHub Copilot 的功能。

## 🚀 什么是 Awesome GitHub Copilot？

本仓库提供了一套综合工具包，用以增强 GitHub Copilot 的功能：

- **👉 [Awesome Agents](docs/README.agents.md)** - 专门的 GitHub Copilot Agent，与 MCP 服务器集成，为特定工作流和工具提供增强功能
- **👉 [Awesome 提示词](docs/README.prompts.md)** - 专注于特定任务的提示词，用于生成代码、文档和解决特定问题
- **👉 [Awesome 指令](docs/README.instructions.md)** - 全面的编码标准和最佳实践，应用于特定的文件模式或整个项目
- **👉 [Awesome 技能](docs/README.skills.md)** - 自包含的文件夹，包含指令和捆绑资源，增强 AI 在专业任务中的能力
- **👉 [Awesome 集合](docs/README.collections.md)** - 围绕特定主题和工作流组织的精选资源集合

## 🌟 精选集合

发现围绕特定主题和工作流组织的精选 Agent、提示词、指令和聊天模式集合。

| 名称 | 描述 | 项目数 | 标签 |
| ---- | ----------- | ----- | ---- |
| [Awesome Copilot](collections/awesome-copilot.md) | 元提示词，帮助您发现和生成精选的 GitHub Copilot 聊天模式、集合、指令、提示词和 Agent | 6 项 | github-copilot, discovery, meta, prompt-engineering, agents |
| [合作伙伴](collections/partners.md) | 由 GitHub 合作伙伴创建的自定义 Agent | 20 项 | devops, security, database, cloud, infrastructure, observability, feature-flags, cicd, migration, performance |

## MCP 服务器

为了方便您将这些自定义功能添加到编辑器中，我们创建了一个 [MCP 服务器](https://developer.microsoft.com/blog/announcing-awesome-copilot-mcp-server)，提供从本仓库直接搜索和安装提示词、指令和聊天模式的功能。您需要安装并运行 Docker。

[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-Install-0098FF?logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/mcp/vscode) [![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-Install-24bfa5?logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/mcp/vscode-insiders) [![在 Visual Studio 中安装](https://img.shields.io/badge/Visual_Studio-Install-C16FDE?logo=visualstudio&logoColor=white)](https://aka.ms/awesome-copilot/mcp/vs)

<details>
<summary>显示 MCP 服务器 JSON 配置</summary>

```json
{
  "servers": {
    "awesome-copilot": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest"
      ]
    }
  }
}
```

</details>

## 🔧 如何使用

### 🤖 自定义 Agent

自定义 Agent 可在 Copilot 编码 Agent (CCA)、VS Code 和 Copilot CLI (即将推出) 中使用。在 CCA 中，为 Copilot 分配问题时，从提供的列表中选择自定义 Agent。在 VS Code 中，您可以在 Agent 会话中激活自定义 Agent，与内置 Agent (如 Plan 和 Agent) 一起使用。

### 🎯 提示词

在 GitHub Copilot Chat 中使用 `/` 命令访问提示词：

```plaintext
/awesome-copilot create-readme
```

### 📋 指令

指令根据文件模式自动应用，为编码标准、框架和最佳实践提供上下文指导。

## 🎯 为什么使用 Awesome GitHub Copilot？

- **提高生产力**：预构建的 Agent、提示词和指令节省时间并提供一致的结果。
- **最佳实践**：受益于社区精选的编码标准和模式。
- **专业帮助**：通过专业的自定义 Agent 获得专家级指导。
- **持续学习**：随时了解各种技术的最新模式和实践。

## 🤝 贡献

我们欢迎贡献！请查看我们的 [贡献指南](CONTRIBUTING.md) 了解如何：

- 添加新的提示词、指令或聊天模式
- 改进现有内容
- 报告问题或建议改进

对于与本项目合作的 AI 编码 Agent，请参阅 [AGENTS.md](AGENTS.md) 获取开发工作流、设置命令和贡献标准的详细技术指导。

### 快速贡献指南

1. 遵循文件命名约定和前言要求
2. 彻底测试您的贡献
3. 更新相应的 README 表格
4. 提交带有清晰描述的拉取请求

## 📖 仓库结构

```plaintext
├── prompts/          # 任务特定的提示词 (.prompt.md)
├── instructions/     # 编码标准和最佳实践 (.instructions.md)
├── agents/           # AI 人格和专业模式 (.agent.md)
├── collections/      # 相关项目的精选集合 (.collection.yml)
└── scripts/          # 维护用的实用脚本
```

## 📄 许可证

本项目根据 MIT 许可证授权 - 详见 [LICENSE](LICENSE) 文件。

## 🛡️ 安全性和支持

- **安全问题**：请参阅我们的 [安全政策](SECURITY.md)
- **支持**：查看我们的 [支持指南](SUPPORT.md) 获取帮助
- **行为准则**：我们遵循 [贡献者公约](CODE_OF_CONDUCT.md)

## ℹ️ 免责声明

本仓库中的自定义功能由第三方开发者提供和创建。GitHub 不验证、认可或保证这些 Agent 的功能或安全性。在安装任何 Agent 之前，请仔细检查其文档，以了解它可能需要的权限和可能执行的操作。

---

**准备好增强您的编码体验了吗？** 开始探索我们的 [提示词](docs/README.prompts.md)、[指令](docs/README.instructions.md) 和 [自定义 Agent](docs/README.agents.md)！

## 📚 其他资源

- [VS Code Copilot 自定义文档](https://code.visualstudio.com/docs/copilot/copilot-customization) - 官方 Microsoft 文档
- [GitHub Copilot Chat 文档](https://code.visualstudio.com/docs/copilot/chat/copilot-chat) - 完整的聊天功能指南
- [自定义聊天模式](https://code.visualstudio.com/docs/copilot/chat/chat-modes) - 高级聊天配置
- [VS Code 设置](https://code.visualstudio.com/docs/getstarted/settings) - 常规 VS Code 配置指南

## ™️ 商标

本项目可能包含项目、产品或服务的商标或徽标。Microsoft 商标或徽标的授权使用受 [Microsoft 商标和品牌指南](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general) 约束。在本项目的修改版本中使用 Microsoft 商标或徽标不得造成混淆或暗示 Microsoft 赞助。第三方商标或徽标的任何使用均受相应第三方政策的约束。

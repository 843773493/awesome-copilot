# 上下文工程

通过更好的上下文管理来最大化 GitHub Copilot 效果的工具和技术。包括代码结构指南、用于规划多文件更改的代理，以及上下文感知开发的提示。

**标签:** 上下文, 生产力, 重构, 最佳实践, 架构

## 本集合中的项目

| 标题 | 类型 | 描述 | MCP 服务器 |
|-----|----|-----------|-----------|
| [上下文工程](../instructions/context-engineering.instructions.md)<br />[![在 VS 代码中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/instructions?url=vscode%3Achat-instructions%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Finstructions%2Fcontext-engineering.instructions.md)<br />[![在 VS 代码 Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/instructions?url=vscode-insiders%3Achat-instructions%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Finstructions%2Fcontext-engineering.instructions.md) | 指南 | 通过更好的上下文管理，指导如何结构化代码和项目以最大化 GitHub Copilot 的效果 |  |
| [上下文架构师](../agents/context-architect.agent.md)<br />[![在 VS 代码中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fcontext-architect.agent.md)<br />[![在 VS 代码 Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fcontext-architect.agent.md) | 代理 | 通过识别相关上下文和依赖关系，帮助规划和执行多文件更改的代理 [查看用法](#context-architect) |  |
| [上下文地图](../prompts/context-map.prompt.md)<br />[![在 VS 代码中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Fcontext-map.prompt.md)<br />[![在 VS 代码 Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode-insiders%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Fcontext-map.prompt.md) | 提示 | 在进行更改前生成与任务相关的所有文件地图 [查看用法](#context-map) |  |
| [你需要什么上下文？](../prompts/what-context-needed.prompt.md)<br />[![在 VS 代码中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Fwhat-context-needed.prompt.md)<br />[![在 VS 代码 Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode-insiders%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Fwhat-context-needed.prompt.md) | 提示 | 当 Copilot 给出通用或错误回答时，询问其需要查看哪些文件 [查看用法](#what-context-do-you-need?) |  |
| [重构计划](../prompts/refactor-plan.prompt.md)<br />[![在 VS 代码中安装](https://img.shields.io/badge/VS_Code-安装-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Frefactor-plan.prompt.md)<br />[![在 VS 代码 Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-安装-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/prompt?url=vscode-insiders%3Achat-prompt%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fprompts%2Frefactor-plan.prompt.md) | 提示 | 为多文件重构生成分阶段计划，包含验证步骤和回滚程序 [查看用法](#refactor-plan) |  |

## 集合使用方式

### 上下文架构师

**推荐使用**

上下文架构师代理通过映射依赖关系并识别所有相关文件，帮助规划多文件更改。

使用此代理时：
- 规划涉及多个文件的重构
- 添加涉及多个模块的功能
- 探索代码库中不熟悉的部分

示例用法：
```
@context-architect 我需要为所有 API 端点添加速率限制。
涉及哪些文件？最佳方案是什么？
```

获取最佳效果：
- 描述高层次目标，而不仅仅是即时任务
- 让代理在你提供文件前进行搜索
- 审核上下文地图后再批准更改

---

### 上下文地图

**可选**

在进行任何重大更改前使用，以了解更改的影响范围。生成结构化的文件、依赖关系和测试地图。

---

### 你需要什么上下文？

**可选**

当 Copilot 给出通用或错误回答时使用。明确要求 Copilot 列出其需要查看的文件。

---

### 重构计划

**可选**

用于多文件重构。生成包含验证步骤和回滚程序的分阶段计划。

---

*此集合包含 5 个针对 **上下文工程** 的精选项目。*

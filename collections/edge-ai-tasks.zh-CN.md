

# 由 microsoft/edge-ai 提供的任务

适用于中级到高级用户的任务研究员和任务规划器，适用于大型代码库 - 由 microsoft/edge-ai 提供

**标签：** 架构、规划、研究、任务、实施

## 本集合中的项目

| 标题 | 类型 | 描述 | MCP 服务器 |
|-----|----|-----------|-----------|
| [任务计划实施说明](../instructions/task-implementation.instructions.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/instructions?url=vscode%3Achat-instructions%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Finstructions%2Ftask-implementation.instructions.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-Install-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/instructions?url=vscode-insiders%3Achat-instructions%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Finstructions%2Ftask-implementation.instructions.md) | 说明 | 用于实现带有渐进式跟踪和变更记录的任务计划的说明 - 由 microsoft/edge-ai 提供 [查看用法](#任务计划实施说明) |  |
| [任务规划器说明](../agents/task-planner.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Ftask-planner.agent.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-Install-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Ftask-planner.agent.md) | 代理 | 用于创建可操作实施计划的任务规划器 - 由 microsoft/edge-ai 提供 [查看用法](#任务规划器说明) |  |
| [任务研究员说明](../agents/task-researcher.agent.md)<br />[![在 VS Code 中安装](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Ftask-researcher.agent.md)<br />[![在 VS Code Insiders 中安装](https://img.shields.io/badge/VS_Code_Insiders-Install-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode-insiders%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Ftask-researcher.agent.md) | 代理 | 用于全面项目分析的任务研究专家 - 由 microsoft/edge-ai 提供 [查看用法](#任务研究员说明) |  |

## 集合用法

### 任务计划实施说明

继续使用 `task-planner` 对计划进行迭代，直到您对代码库的修改完全满意。

当您准备好实施计划时，**创建一个新聊天**，切换到 `Agent` 模式，然后触发新生成的提示。

```markdown, implement-fabric-rti-changes.prompt.md
---
mode: agent
title: 实现 microsoft fabric 实时智能 Terraform 支持
---
/implement-fabric-rti-blueprint-modification phaseStop=true
```

此提示的一个额外优势是会将计划作为说明附加，有助于在整个对话中保持上下文。

**专家警告** ->> 使用 `phaseStop=false` 让 Copilot 不停地实施整个计划。此外，您还可以使用 `taskStop=true` 让 Copilot 在每个任务实施后停止，以实现更精细的控制。

要使用这些生成的说明和提示，您需要相应地更新 `settings.json`：

```json
    "chat.instructionsFilesLocations": {
        // 现有的指令文件夹...
        ".copilot-tracking/plans": true
    },
    "chat.promptFilesLocations": {
        // 现有的提示文件夹...
        ".copilot-tracking/prompts": true
    },
```

---

### 任务规划器说明

此外，任务研究员将提供额外的实施想法，您可以与 GitHub Copilot 协作，选择合适的一个进行聚焦。

```markdown, task-plan.prompt.md
---
mode: task-planner
title: 规划 microsoft fabric 实时智能 Terraform 支持
---
#file: .copilot-tracking/research/*-fabric-rti-blueprint-modification-research.md
为该项目构建支持添加 fabric rti 的计划
```

`task-planner` 将帮助您创建实施任务的计划。它将使用您已完全研究的想法，或在未提供时生成新的研究内容。

`task-planner` 将生成三个（3）文件，这些文件将被 `task-implementation.instructions.md` 使用。

* `.copilot-tracking/plan/*-plan.instructions.md`

  * 一个新生成的说明文件，其中将计划作为分阶段和分任务的检查清单。
* `.copilot-tracking/details/*-details.md`

  * 实施的详细信息，计划文件会引用此文件以获取具体细节（如果您有大型计划则尤为重要）。
* `.copilot-tracking/prompts/implement-*.prompt.md`

  * 一个新生成的提示文件，将创建 `.copilot-tracking/changes/*-changes.md` 文件并开始实施更改。

继续使用 `task-planner` 对计划进行迭代，直到您对代码库的修改完全满意。

---

### 任务研究员说明

现在您可以对任务的研究进行迭代！

```markdown, research.prompt.md
---
mode: task-researcher
title: 研究 microsoft fabric 实时智能 Terraform 支持
---
查看 microsoft 关于 fabric 实时智能的文档
并提出如何将此支持集成到我们的 Terraform 组件中的想法。
```

研究结果将输出到 `.copilot-tracking/research/*-research.md` 文件中，并将包含 GHCP 的发现内容以及在实施过程中有用的示例和架构。

此外，任务研究员还将提供额外的实施想法，您可以与 GitHub Copilot 协作，选择合适的一个进行聚焦。
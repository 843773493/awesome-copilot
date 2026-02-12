# 🤖 GitHub Copilot 精选集
[![由 Awesome Copilot 提供支持](https://img.shields.io/badge/Powered_by-Awesome_Copilot-blue?logo=githubcopilot)](https://aka.ms/awesome-github-copilot) [![GitHub 贡献者 (来自 allcontributors.org)](https://img.shields.io/github/all-contributors/github/awesome-copilot?color=ee8449)](#contributors-)

由社区创建的用于增强 GitHub Copilot 的自定义代理、提示和指令集合，适用于不同领域、语言和使用场景。

## 🚀 什么是 GitHub Copilot 精选集？

此仓库提供一个全面的工具包，用于通过以下方式增强 GitHub Copilot：

- **👉 [精选代理](docs/README.agents.md)** - 专门的 GitHub Copilot 代理，集成到 MCP 服务器以提供特定工作流和工具的增强功能
- **👉 [精选提示](docs/README.prompts.md)** - 针对特定任务的提示，用于生成代码、文档和解决特定问题
- **👉 [精选指令](docs/README.instructions.md)** - 适用于特定文件模式或整个项目的全面编码标准和最佳实践
- **👉 [精选钩子](docs/README.hooks.md)** - 在开发、测试和部署期间由特定事件触发的自动化工作流
- **👉 [精选技能](docs/README.skills.md)** - 包含指令和捆绑资源的自包含文件夹，用于增强特定任务的 AI 能力
- **👉 [精选集合](docs/README.collections.md)** - 围绕特定主题和工作流组织的精选提示、指令、代理和技能集合
- **👉 [精选食谱](cookbook/README.md)** - 用于使用 GitHub Copilot 工具和功能的实用代码片段和真实示例

## 🌟 精选集合

发现我们围绕特定主题和工作流组织的精选提示、指令和代理集合。

| 名称 | 描述 | 项目数 | 标签 |
| ---- | ----------- | ----- | ---- |
| [GitHub Copilot 精选集](collections/awesome-copilot.md) | 用于发现和生成精选 GitHub Copilot 代理、集合、指令、提示和技能的元提示 | 5 项目 | github-copilot, discovery, meta, prompt-engineering, agents |
| [Copilot SDK](collections/copilot-sdk.md) | 使用 GitHub Copilot SDK 跨多种编程语言构建应用程序。包含 C#、Go、Node.js/TypeScript 和 Python 的全面说明，帮助您创建 AI 驱动的应用程序 | 5 项目 | copilot-sdk, sdk, csharp, go, nodejs, typescript, python, ai, github-copilot |
| [合作伙伴](collections/partners.md) | 由 GitHub 合作伙伴创建的自定义代理 | 20 项目 | devops, security, database, cloud, infrastructure, observability, feature-flags, cicd, migration, performance |

## 📄 llms.txt

[llms.txt](https://github.github.io/awesome-copilot/llms.txt) 文件遵循 [llmstxt.org](https://llmstxt.org/) 规范，可在 GitHub Pages 网站上找到。该机器可读文件使大型语言模型能够轻松发现和理解所有可用的代理、提示、指令和技能，提供结构化的资源概述，包含名称和描述。

## 🔧 如何使用

### 🔌 插件

插件是从集合中生成的可安装包。每个插件包含从源集合中链接的代理、命令（提示）和技能，使您能够轻松安装一组精选的资源。

#### 安装插件

首先，将 Awesome Copilot 市场添加到您的 Copilot CLI：

```bash
copilot plugin marketplace add github/awesome-copilot
```

然后安装任何集合中的插件：

```bash
copilot plugin install <插件名称>@awesome-copilot
```

或者，您可以在 Copilot 聊天会话中使用 `/plugin` 命令，以交互方式浏览和安装插件。

### 🤖 自定义代理

自定义代理可用于 Copilot 编码代理 (CCA)、VS Code 和 Copilot CLI（即将推出）。对于 CCA，当分配任务给 Copilot 时，从提供的列表中选择自定义代理。在 VS Code 中，您可以在代理会话中激活自定义代理，与内置代理（如 Plan 和 Agent）并列。

### 🎯 提示

使用 GitHub Copilot 聊天中的 `/` 命令访问提示：

```plaintext
/awesome-copilot create-readme
```

### 📋 指令

指令会根据文件模式自动应用，并为编码标准、框架和最佳实践提供上下文指导。

### 🪝 钩子

钩子可在 GitHub Copilot 编码代理会话期间由特定事件触发（如 sessionStart、sessionEnd、userPromptSubmitted）。它们可以自动化任务，如日志记录、自动提交更改或与外部服务集成。

## 🎯 为什么使用 GitHub Copilot 精选集？

- **生产力**：预构建的代理、提示和指令节省时间并提供一致的结果。
- **最佳实践**：受益于社区整理的编码标准和模式。
- **专业协助**：通过专门的自定义代理获取专家级指导。
- **持续学习**：了解技术领域的最新模式和实践。

## 🤝 贡献

我们欢迎贡献！请参阅我们的 [贡献指南](CONTRIBUTING.md)，了解如何：

- 添加新的提示、指令、钩子、代理或技能
- 改进现有内容
- 报告问题或提出改进建议

对于与该项目一起工作的 AI 编码代理，请参考 [AGENTS.md](AGENTS.md)，了解开发流程、设置命令和贡献标准的详细技术指导。

### 快速贡献指南

1. 遵循我们的文件命名规范和 frontmatter 要求
2. 彻底测试您的贡献
3. 更新相应的 README 表格
4. 提交包含清晰描述的拉取请求

## 📖 仓库结构

```plaintext
├── prompts/          # 任务特定提示 (.prompt.md)
├── instructions/     # 编码标准和最佳实践 (.instructions.md)
├── agents/           # AI 角色和专门模式 (.agent.md)
├── collections/      # 精选相关资源集合 (.collection.yml)
├── plugins/          # 从集合生成的可安装插件
├── scripts/          # 用于维护的实用脚本
└── skills/           # 专门任务的 AI 能力
```

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 🛡️ 安全与支持

- **安全问题**：请参阅我们的 [安全政策](SECURITY.md)
- **支持**：查看我们的 [支持指南](SUPPORT.md) 以获取帮助
- **行为准则**：我们遵循 [贡献者公约](CODE_OF_CONDUCT.md)

## ℹ️ 免责声明

本仓库中的自定义设置来源于并由第三方开发者创建。GitHub 不验证、认可或保证这些代理的功能或安全性。安装前请仔细检查任何代理及其文档，以了解其可能需要的权限和执行的操作。

---

**准备好提升您的编码体验了吗？** 开始探索我们的 [提示](docs/README.prompts.md)、[指令](docs/README.instructions.md)、[钩子](docs/README.hooks.md) 和 [自定义代理](docs/README.agents.md)！

## 贡献者 ✨

感谢这些杰出的人（[表情符号说明](./CONTRIBUTING.md#贡献者认可)）：

<!-- ALL-CONTRIBUTORS-LIST:START - 请不要删除或修改此部分 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://www.aaron-powell.com/"><img src="https://avatars.githubusercontent.com/u/434140?v=4?s=100" width="100px;" alt="Aaron Powell"/><br /><sub><b>Aaron Powell</b></sub></a><br /><a href="#agents-aaronpowell" title="GitHub Copilot 的专门代理">🎭</a> <a href="https://github.com/github/awesome-copilot/commits?author=aaronpowell" title="代码">💻</a> <a href="#collections-aaronpowell" title="精选相关内容的集合">🎁</a> <a href="https://github.com/github/awesome-copilot/commits?author=aaronpowell" title="文档">📖</a> <a href="#infra-aaronpowell" title="基础设施（托管、构建工具等）">🚇</a> <a href="#instructions-aaronpowell" title="GitHub Copilot 的自定义指令">🧭</a> <a href="#maintenance-aaronpowell" title="维护">🚧</a> <a href="#prompts-aaronpowell" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://codemilltech.com/"><img src="https://avatars.githubusercontent.com/u/2053639?v=4?s=100" width="100px;" alt="Matt Soucoup"/><br /><sub><b>Matt Soucoup</b></sub></a><br /><a href="#infra-codemillmatt" title="基础设施（托管、构建工具等）">🚇</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.buymeacoffee.com/troystaylor"><img src="https://avatars.githubusercontent.com/u/44444967?v=4?s=100" width="100px;" alt="Troy Simeon Taylor"/><br /><sub><b>Troy Simeon Taylor</b></sub></a><br /><a href="#agents-troystaylor" title="GitHub Copilot 的专门代理">🎭</a> <a href="#collections-troystaylor" title="精选相关内容的集合">🎁</a> <a href="#instructions-troystaylor" title="GitHub Copilot 的自定义指令">🧭</a> <a href="#prompts-troystaylor" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/abbas133"><img src="https://avatars.githubusercontent.com/u/7757139?v=4?s=100" width="100px;" alt="Abbas"/><br /><sub><b>Abbas</b></sub></a><br /><a href="#agents-abbas133" title="GitHub Copilot 的专门代理">🎭</a> <a href="#instructions-abbas133" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://calva.io/"><img src="https://avatars.githubusercontent.com/u/30010?v=4?s=100" width="100px;" alt="Peter Strömberg"/><br /><sub><b>Peter Strömberg</b></sub></a><br /><a href="#agents-PEZ" title="GitHub Copilot 的专门代理">🎭</a> <a href="#collections-PEZ" title="精选相关内容的集合">🎁</a> <a href="#instructions-PEZ" title="GitHub Copilot 的自定义指令">🧭</a> <a href="#prompts-PEZ" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://danielscottraynsford.com/"><img src="https://avatars.githubusercontent.com/u/7589164?v=4?s=100" width="100px;" alt="Daniel Scott-Raynsford"/><br /><sub><b>Daniel Scott-Raynsford</b></sub></a><br /><a href="#agents-Vhivi" title="GitHub Copilot 的专门代理">🎭</a> <a href="#collections-Vhivi" title="精选相关内容的集合">🎁</a> <a href="#instructions-Vhivi" title="GitHub Copilot 的自定义指令">🧭</a> <a href="#prompts-Vhivi" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jhauga"><img src="https://avatars.githubusercontent.com/u/10998676?v=4?s=100" width="100px;" alt="John Haugabook"/><br /><sub><b>John Haugabook</b></sub></a><br /><a href="#agents-jhauga" title="GitHub Copilot 的专门代理">🎭</a> <a href="#collections-jhauga" title="精选相关内容的集合">🎁</a> <a href="#instructions-jhauga" title="GitHub Copilot 的自定义指令">🧭</a> <a href="#prompts-jhauga" title="GitHub Copilot 的可重用提示">⌨️</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/troytaylor-msft"><img src="https://avatars.githubusercontent.com/u/248058374?v=4?s=100" width="100px;" alt="troytaylor-msft"/><br /><sub><b>troytaylor-msft</b></sub></a><br /><a href="#agents-troytaylor-msft" title="GitHub Copilot 的专门代理">🎭</a> <a href="#instructions-troytaylor-msft" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/askpt"><img src="https://avatars.githubusercontent.com/u/2493377?v=4?s=100" width="100px;" alt="André Silva"/><br /><sub><b>André Silva</b></sub></a><br /><a href="#agents-askpt" title="GitHub Copilot 的专门代理">🎭</a> <a href="#instructions-askpt" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/agreaves-ms"><img src="https://avatars.githubusercontent.com/u/111466195?v=4?s=100" width="100px;" alt="Allen Greaves"/><br /><sub><b>Allen Greaves</b></sub></a><br /><a href="#agents-agreaves-ms" title="GitHub Copilot 的专门代理">🎭</a> <a href="#instructions-agreaves-ms" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AmeliaRose802"><img src="https://avatars.githubusercontent.com/u/26167931?v=4?s=100" width="100px;" alt="Amelia Payne"/><br /><sub><b>Amelia Payne</b></sub></a><br /><a href="#agents-AmeliaRose802" title="GitHub Copilot 的专门代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/BBoyBen"><img src="https://avatars.githubusercontent.com/u/34445365?v=4?s=100" width="100px;" alt="BBoyBen"/><br /><sub><b>BBoyBen</b></sub></a><br /><a href="#instructions-BBoyBen" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/breakid"><img src="https://avatars.githubusercontent.com/u/1446918?v=4?s=100" width="100px;" alt="Dan"/><br /><sub><b>Dan</b></sub></a><br /><a href="#instructions-breakid" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://blog.codewithdan.com/"><img src="https://avatars.githubusercontent.com/u/1767249?v=4?s=100" width="100px;" alt="Dan Wahlin"/><br /><sub><b>Dan Wahlin</b></sub></a><br /><a href="#agents-DanWahlin" title="GitHub Copilot 的专门代理">🎭</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://debbie.codes/"><img src="https://avatars.githubusercontent.com/u/13063165?v=4?s=100" width="100px;" alt="Debbie O'Brien"/><br /><sub><b>Debbie O'Brien</b></sub></a><br /><a href="#agents-debs-obrien" title="GitHub Copilot 的专门代理">🎭</a> <a href="#instructions-debs-obrien" title="GitHub Copilot 的自定义指令">🧭</a> <a href="#prompts-debs-obrien" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/echarrod"><img src="https://avatars.githubusercontent.com/u/1381991?v=4?s=100" width="100px;" alt="Ed Harrod"/><br /><sub><b>Ed Harrod</b></sub></a><br /><a href="#prompts-echarrod" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://learn.microsoft.com/dotnet"><img src="https://avatars.githubusercontent.com/u/24882762?v=4?s=100" width="100px;" alt="Genevieve Warren"/><br /><sub><b>Genevieve Warren</b></sub></a><br /><a href="#prompts-gewarren" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/guigui42"><img src="https://avatars.githubusercontent.com/u/2376010?v=4?s=100" width="100px;" alt="Guillaume"/><br /><sub><b>Guillaume</b></sub></a><br /><a href="#agents-guigui42" title="GitHub Copilot 的专门代理">🎭</a> <a href="#prompts-guigui42" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/yeelam-gordon"><img src="https://avatars.githubusercontent.com/u/73506701?v=4?s=100" width="100px;" alt="Gordon Lam"/><br /><sub><b>Gordon Lam</b></sub></a><br /><a href="#instructions-yeelam-gordon" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jeremiah-snee-openx"><img src="https://avatars.githubusercontent.com/u/113928685?v=4?s=100" width="100px;" alt="Jeremiah Snee"/><br /><sub><b>Jeremiah Snee</b></sub></a><br /><a href="#agents-jeremiah-snee-openx" title="GitHub Copilot 的专门代理">🎭</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kartikdhiman"><img src="https://avatars.githubusercontent.com/u/59189590?v=4?s=100" width="100px;" alt="Kartik Dhiman"/><br /><sub><b>Kartik Dhiman</b></sub></a><br /><a href="#instructions-kartikdhiman" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://kristiyanvelkov.com/"><img src="https://avatars.githubusercontent.com/u/40764277?v=4?s=100" width="100px;" alt="Kristiyan Velkov"/><br /><sub><b>Kristiyan Velkov</b></sub></a><br /><a href="#agents-kristiyan-velkov" title="GitHub Copilot 的专门代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/msalaman"><img src="https://avatars.githubusercontent.com/u/28122166?v=4?s=100" width="100px;" alt="msalaman"/><br /><sub><b>msalaman</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=msalaman" title="代码">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://soderlind.no/"><img src="https://avatars.githubusercontent.com/u/1649452?v=4?s=100" width="100px;" alt="Per Søderlind"/><br /><sub><b>Per Søderlind</b></sub></a><br /><a href="#instructions-soderlind" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://dotneteers.net/"><img src="https://avatars.githubusercontent.com/u/28162552?v=4?s=100" width="100px;" alt="Tj Vita"/><br /><sub><b>Tj Vita</b></sub></a><br /><a href="#agents-semperteneo" title="GitHub Copilot 的专门代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pelikhan"><img src="https://avatars.githubusercontent.com/u/4175913?v=4?s=100" width="100px;" alt="Peli de Halleux"/><br /><sub><b>Peli de Halleux</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=pelikhan" title="代码">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.paulomorgado.net/"><img src="https://avatars.githubusercontent.com/u/470455?v=4?s=100" width="100px;" alt="Paulo Morgado"/><br /><sub><b>Paulo Morgado</b></sub></a><br /><a href="#prompts-paulomorgado" title="GitHub Copilot 的可重用提示">⌨️</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pcrane"><img src="https://avatars.githubusercontent.com/u/808676?v=4?s=100" width="100px;" alt="Paul Crane"/><br /><sub><b>Paul Crane</b></sub></a><br /><a href="#agents-pcrane" title="GitHub Copilot 的专门代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.pamelafox.org/"><img src="https://avatars.githubusercontent.com/u/297042?v=4?s=100" width="100px;" alt="Pamela Fox"/><br /><sub><b>Pamela Fox</b></sub></a><br /><a href="#prompts-pamelafox" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/matebarabas"><img src="https://avatars.githubusercontent.com/u/22733424?v=4?s=100" width="100px;" alt="Máté Barabás"/><br /><sub><b>Máté Barabás</b></sub></a><br /><a href="#instructions-matebarabas" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mikeparker104"><img src="https://avatars.githubusercontent.com/u/12763221?v=4?s=100" width="100px;" alt="Mike Parker"/><br /><sub><b>Mike Parker</b></sub></a><br /><a href="#instructions-mikeparker104" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mikekistler"><img src="https://avatars.githubusercontent.com/u/85643503?v=4?s=100" width="100px;" alt="Mike Kistler"/><br /><sub><b>Mike Kistler</b></sub></a><br /><a href="#prompts-mikekistler" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/giomartinsdev"><img src="https://avatars.githubusercontent.com/u/125399281?v=4?s=100" width="100px;" alt="Giovanni de Almeida Martins"/><br /><sub><b>Giovanni de Almeida Martins</b></sub></a><br /><a href="#instructions-giomartinsdev" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dgh06175"><img src="https://avatars.githubusercontent.com/u/77305722?v=4?s=100" width="100px;" alt="이상현"/><br /><sub><b>이상현</b></sub></a><br /><a href="#instructions-dgh06175" title="GitHub Copilot 的自定义指令">🧭</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/zooav"><img src="https://avatars.githubusercontent.com/u/12625412?v=4?s=100" width="100px;" alt="Ankur Sharma"/><br /><sub><b>Ankur Sharma</b></sub></a><br /><a href="#prompts-zooav" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/webreidi"><img src="https://avatars.githubusercontent.com/u/55603905?v=4?s=100" width="100px;" alt="Wendy Breiding"/><br /><sub><b>Wendy Breiding</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=webreidi" title="代码">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/voidfnc"><img src="https://avatars.githubusercontent.com/u/194750710?v=4?s=100" width="100px;" alt="voidfnc"/><br /><sub><b>voidfnc</b></sub></a><br /><a href="#agents-voidfnc" title="GitHub Copilot 的专门代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://about.me/shane-lee"><img src="https://avatars.githubusercontent.com/u/5466825?v=4?s=100" width="100px;" alt="shane lee"/><br /><sub><b>shane lee</b></sub></a><br /><a href="#agents-shavo007" title="GitHub Copilot 的专门代理">🎭</a> <a href="#instructions-shavo007" title="GitHub Copilot 的自定义指令">🧭</a> <a href="#prompts-shavo007" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/sdanzo-hrb"><img src="https://avatars.githubusercontent.com/u/136493100?v=4?s=100" width="100px;" alt="sdanzo-hrb"/><br /><sub><b>sdanzo-hrb</b></sub></a><br /><a href="#agents-sdanzo-hrb" title="GitHub Copilot 的专门代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nativebpm"><img src="https://avatars.githubusercontent.com/u/33398121?v=4?s=100" width="100px;" alt="sauran"/><br /><sub><b>sauran</b></sub></a><br /><a href="#agents-isauran" title="GitHub Copilot 的专门代理">🎭</a> <a href="#instructions-isauran" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/samqbush"><img src="https://avatars.githubusercontent.com/u/74389839?v=4?s=100" width="100px;" alt="samqbush"/><br /><sub><b>samqbush</b></sub></a><br /><a href="#prompts-samqbush" title="GitHub Copilot 的可重用提示">⌨️</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pareenaverma"><img src="https://avatars.githubusercontent.com/u/59843121?v=4?s=100" width="100px;" alt="pareenaverma"/><br /><sub><b>pareenaverma</b></sub></a><br /><a href="#agents-pareenaverma" title="GitHub Copilot 的专门代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/oleksiyyurchyna"><img src="https://avatars.githubusercontent.com/u/10256765?v=4?s=100" width="100px;" alt="oleksiyyurchyna"/><br /><sub><b>oleksiyyurchyna</b></sub></a><br /><a href="#collections-oleksiyyurchyna" title="精选相关内容的集合">🎁</a> <a href="#prompts-oleksiyyurchyna" title="GitHub Copilot 的可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/time-by-waves"><img src="https://avatars.githubusercontent.com/u/34587654?v=4?s=100" width="100px;" alt="oceans-of-time"/><br /><sub><b>oceans-of-time</b></sub></a><br /><a href="#instructions-time-by-waves" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kshashank57"><img src="https://avatars.githubusercontent.com/u/57212456?v=4?s=100" width="100px;" alt="kshashank57"/><br /><sub><b>kshashank57</b></sub></a><br /><a href="#agents-kshashank57" title="GitHub Copilot 的专门代理">🎭</a> <a href="#instructions-kshashank57" title="GitHub Copilot 的自定义指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hueanmy"><img src="https://avatars.githubusercontent.com/u/20430626?v=4?s=100" width="100px;" alt="Meii"/><br /><sub><b>Meii</b></sub></a><br /><a href="#agents-hueanmy" title="GitHub Copilot 的专门代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/factory-davidgu"><img src="https://avatars.githubusercontent.com/u/229352262?v=4?s=100" width="100px;" alt="factory-davidgu"/><br /><sub><b>factory-davidgu</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=factory-davidgu" title="代码">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dangelov-qa"><img src="https://avatars.githubusercontent.com/u/92313553?v=4?s=100" width="100px;" alt="dangelov-qa"/><br /><sub><b>dangelov-qa</b></sub></a><br /><a href="#agents-dangelov

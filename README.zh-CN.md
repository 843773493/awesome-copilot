# 🤖 GitHub Copilot 精选
[![由 Awesome Copilot 提供支持](https://img.shields.io/badge/Powered_by-Awesome_Copilot-blue?logo=githubcopilot)](https://aka.ms/awesome-github-copilot) [![GitHub 贡献者来自 allcontributors.org](https://img.shields.io/github/all-contributors/github/awesome-copilot?color=ee8449)](#贡献者-)

由社区创建的自定义代理、提示和指令集合，可增强您在不同领域、语言和用例中的 GitHub Copilot 体验。

## 🚀 什么是 Awesome GitHub Copilot？

此仓库提供一个全面工具包，用于通过以下方式增强 GitHub Copilot：

- **👉 [Awesome 代理](docs/README.agents.md)** - 专为 GitHub Copilot 代理设计的，集成到 MCP 服务器以提供特定工作流和工具的增强功能
- **👉 [Awesome 提示](docs/README.prompts.md)** - 针对特定任务的提示，用于生成代码、文档和解决特定问题
- **👉 [Awesome 指令](docs/README.instructions.md)** - 适用于特定文件模式或整个项目的全面编码标准和最佳实践
- **👉 [Awesome 技能](docs/README.skills.md)** - 包含指令和捆绑资源的自包含文件夹，用于增强 AI 在特定任务中的能力
- **👉 [Awesome 收集](docs/README.collections.md)** - 按特定主题和工作流组织的提示、指令、代理和技能的精选集合
- **👉 [Awesome 食谱](cookbook/README.md)** - 用于与 GitHub Copilot 工具和功能一起工作的实用代码片段和真实世界示例

## 🌟 精选集合

发现我们按特定主题和工作流组织的提示、指令和代理精选集合。

| 名称 | 描述 | 项目数 | 标签 |
| ---- | ----------- | ----- | ---- |
| [Awesome Copilot](collections/awesome-copilot.md) | 用于发现和生成精选 GitHub Copilot 代理、集合、指令、提示和技能的元提示 | 5 项 | github-copilot, discovery, meta, prompt-engineering, agents |
| [Copilot SDK](collections/copilot-sdk.md) | 使用 GitHub Copilot SDK 跨多种编程语言构建应用程序。包含 C#、Go、Node.js/TypeScript 和 Python 的全面说明，帮助您创建 AI 驱动的应用程序 | 5 项 | copilot-sdk, sdk, csharp, go, nodejs, typescript, python, ai, github-copilot |
| [合作伙伴](collections/partners.md) | 由 GitHub 合作伙伴创建的自定义代理 | 20 项 | devops, security, database, cloud, infrastructure, observability, feature-flags, cicd, migration, performance |

## 📄 llms.txt

[llms.txt](https://github.github.io/awesome-copilot/llms.txt) 文件遵循 [llmstxt.org](https://llmstxt.org/) 规范，可在 GitHub Pages 网站上找到。此机器可读文件使大型语言模型能够发现和理解所有可用的代理、提示、指令和技能，提供具有名称和描述的仓库资源结构化概览。

## 🔧 如何使用

### 🔌 插件

插件是从集合中生成的可安装包。每个插件包含从源集合中链接的代理、命令（提示）和技能，使您能够轻松安装一组精选资源。

#### 安装插件

首先，将 Awesome Copilot 市场添加到您的 Copilot CLI：

```bash
copilot plugin marketplace add github/awesome-copilot
```

然后安装任何插件：

```bash
copilot plugin install <插件名称>@awesome-copilot
```

或者，您可以在 Copilot 聊天会话中使用 `/plugin` 命令来交互式浏览和安装插件。

### 🤖 自定义代理

自定义代理可在 Copilot 编码代理 (CCA)、VS Code 和 Copilot CLI（即将推出）中使用。对于 CCA，当分配问题给 Copilot 时，从提供的列表中选择自定义代理。在 VS Code 中，您可以激活自定义代理，与内置代理（如 Plan 和 Agent）一起使用。

### 🎯 提示

使用 GitHub Copilot 聊天中的 `/` 命令访问提示：

```plaintext
/awesome-copilot create-readme
```

### 📋 指令

根据文件模式自动应用指令，并为编码标准、框架和最佳实践提供上下文指导。

## 🎯 为什么使用 Awesome GitHub Copilot？

- **生产力**：预建的代理、提示和指令节省时间并提供一致的结果。
- **最佳实践**：受益于社区整理的编码标准和模式。
- **专业帮助**：通过专业自定义代理获得专家级指导。
- **持续学习**：了解技术领域最新的模式和实践。

## 🤝 贡獻

我们欢迎贡献！请参阅我们的 [貢獻指南](CONTRIBUTING.md)，了解如何：

- 添加新的提示、指令、代理或技能
- 改进现有内容
- 报告问题或提出改进建议

对于与该项目一起工作的 AI 编码代理，参考 [AGENTS.md](AGENTS.md) 了解开发流程、设置命令和贡献标准的详细技术指导。

### 快速貢獻指南

1. 遵循我们的文件命名惯例和前缀要求
2. 彻底测试您的贡献
3. 更新适当的 README 表格
4. 提交带有清晰描述的拉取请求

## 📖 仓库结构

```plaintext
├── prompts/          # 任务特定提示 (.prompt.md)
├── instructions/     # 编码标准和最佳实践 (.instructions.md)
├── agents/           # AI 人格和专用模式 (.agent.md)
├── collections/      # 精选相关项目集合 (.collection.yml)
├── plugins/          # 从集合生成的可安装插件
├── scripts/          # 用于维护的实用脚本
└── skills/           # 用于专用任务的 AI 能力
```

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 🛡️ 安全与支持

- **安全问题**：请参阅我们的 [安全政策](SECURITY.md)
- **支持**：查看我们的 [支持指南](SUPPORT.md) 以获取帮助
- **行为准则**：我们遵循 [贡献者公约](CODE_OF_CONDUCT.md)

## ℹ️ 免责声明

本仓库中的自定义设置来源于第三方开发人员。GitHub 不验证、支持或保证这些代理的功能或安全性。在安装前请仔细检查任何代理及其文档，以了解其可能需要的权限和可能执行的操作。

---

**准备好提升您的编码体验了吗？** 开始探索我们的 [提示](docs/README.prompts.md)、[指令](docs/README.instructions.md) 和 [自定义代理](docs/README.agents.md)！

## 贡献者 ✨

感谢这些杰出的人 ([表情符号键](./CONTRIBUTING.md#贡献者认可))：

<!-- ALL-CONTRIBUTORS-LIST:START - 不要删除或修改此部分 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://www.aaron-powell.com/"><img src="https://avatars.githubusercontent.com/u/434140?v=4?s=100" width="100px;" alt="Aaron Powell"/><br /><sub><b>Aaron Powell</b></sub></a><br /><a href="#代理-aaronpowell" title="GitHub Copilot 专用代理">🎭</a> <a href="https://github.com/github/awesome-copilot/commits?author=aaronpowell" title="代码">💻</a> <a href="#集合-aaronpowell" title="精选相关内容集合">🎁</a> <a href="https://github.com/github/awesome-copilot/commits?author=aaronpowell" title="文档">📖</a> <a href="#基础设施-aaronpowell" title="基础设施（托管、构建工具等)">🚇</a> <a href="#指令-aaronpowell" title="GitHub Copilot 专用指令">🧭</a> <a href="#提示-aaronpowell" title="GitHub Copilot 可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://codemilltech.com/"><img src="https://avatars.githubusercontent.com/u/2053639?v=4?s=100" width="100px;" alt="Matt Soucoup"/><br /><sub><b>Matt Soucoup</b></sub></a><br /><a href="#基础设施-codemillmatt" title="基础设施（托管、构建工具等)">🚇</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.buymeacoffee.com/troystaylor"><img src="https://avatars.githubusercontent.com/u/44444967?v=4?s=100" width="100px;" alt="Troy Simeon Taylor"/><br /><sub><b>Troy Simeon Taylor</b></sub></a><br /><a href="#代理-troystaylor" title="GitHub Copilot 专用代理">🎭</a> <a href="#集合-troystaylor" title="精选相关内容集合">🎁</a> <a href="https://github.com/github/awesome-copilot/commits?author=troystaylor" title="代码">💻</a> <a href="#维护-troystaylor" title="维护">🚧</a> <a href="#提示-troystaylor" title="GitHub Copilot 可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/abbas133"><img src="https://avatars.githubusercontent.com/u/7757139?v=4?s=100" width="100px;" alt="Abbas"/><br /><sub><b>Abbas</b></sub></a><br /><a href="#代理-abbas133" title="GitHub Copilot 专用代理">🎭</a> <a href="#指令-abbas133" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://calva.io/"><img src="https://avatars.githubusercontent.com/u/30010?v=4?s=100" width="100px;" alt="Peter Strömberg"/><br /><sub><b>Peter Strömberg</b></sub></a><br /><a href="#集合-PEZ" title="精选相关内容集合">🎁</a> <a href="#指令-PEZ" title="GitHub Copilot 专用指令">🧭</a> <a href="#提示-PEZ" title="GitHub Copilot 可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://danielscottraynsford.com/"><img src="https://avatars.githubusercontent.com/u/7589164?v=4?s=100" width="100px;" alt="Daniel Scott-Raynsford"/><br /><sub><b>Daniel Scott-Raynsford</b></sub></a><br /><a href="#代理-PlagueHO" title="GitHub Copilot 专用代理">🎭</a> <a href="#集合-PlagueHO" title="精选相关内容集合">🎁</a> <a href="#指令-PlagueHO" title="GitHub Copilot 专用指令">🧭</a> <a href="#提示-PlagueHO" title="GitHub Copilot 可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jhauga"><img src="https://avatars.githubusercontent.com/u/10998676?v=4?s=100" width="100px;" alt="John Haugabook"/><br /><sub><b>John Haugabook</b></sub></a><br /><a href="#指令-jhauga" title="GitHub Copilot 专用指令">🧭</a> <a href="#提示-jhauga" title="GitHub Copilot 可重用提示">⌨️</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://witter.cz/@pavel"><img src="https://avatars.githubusercontent.com/u/7853836?v=4?s=100" width="100px;" alt="Pavel Simsa"/><br /><sub><b>Pavel Simsa</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=psimsa" title="代码">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://digitarald.de/"><img src="https://avatars.githubusercontent.com/u/8599?v=4?s=100" width="100px;" alt="Harald Kirschner"/><br /><sub><b>Harald Kirschner</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=digitarald" title="代码">💻</a> <a href="https://github.com/github/awesome-copilot/commits?author=digitarald" title="文档">📖</a> <a href="#维护-digitarald" title="维护">🚧</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://mubaidr.js.org/"><img src="https://avatars.githubusercontent.com/u/2222702?v=4?s=100" width="100px;" alt="Muhammad Ubaid Raza"/><br /><sub><b>Muhammad Ubaid Raza</b></sub></a><br /><a href="#代理-mubaidr" title="GitHub Copilot 专用代理">🎭</a> <a href="#指令-mubaidr" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tmeschter"><img src="https://avatars.githubusercontent.com/u/10506730?v=4?s=100" width="100px;" alt="Tom Meschter"/><br /><sub><b>Tom Meschter</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=tmeschter" title="代码">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.aungmyokyaw.com/"><img src="https://avatars.githubusercontent.com/u/9404824?v=4?s=100" width="100px;" alt="Aung Myo Kyaw"/><br /><sub><b>Aung Myo Kyaw</b></sub></a><br /><a href="#代理-AungMyoKyaw" title="GitHub Copilot 专用代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/JasonYeMSFT"><img src="https://avatars.githubusercontent.com/u/39359541?v=4?s=100" width="100px;" alt="JasonYeMSFT"/><br /><sub><b>JasonYeMSFT</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=JasonYeMSFT" title="代码">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://blog.miniasp.com/"><img src="https://avatars.githubusercontent.com/u/1767249?v=4?s=100" width="100px;" alt="Will 保哥"/><br /><sub><b>Will 保哥</b></sub></a><br /><a href="#代理-doggy8088" title="GitHub Copilot 专用代理">🎭</a> <a href="#提示-doggy8088" title="GitHub Copilot 可重用提示">⌨️</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://tsubalog.hatenablog.com/"><img src="https://avatars.githubusercontent.com/u/1592808?v=4?s=100" width="100px;" alt="Yuta Matsumura"/><br /><sub><b>Yuta Matsumura</b></sub></a><br /><a href="#指令-tsubakimoto" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/anschnapp"><img src="https://avatars.githubusercontent.com/u/17565996?v=4?s=100" width="100px;" alt="anschnapp"/><br /><sub><b>anschnapp</b></sub></a><br /><a href="#代理-anschnapp" title="GitHub Copilot 专用代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/echarrod"><img src="https://avatars.githubusercontent.com/u/1381991?v=4?s=100" width="100px;" alt="Ed Harrod"/><br /><sub><b>Ed Harrod</b></sub></a><br /><a href="#提示-echarrod" title="GitHub Copilot 可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://learn.microsoft.com/dotnet"><img src="https://avatars.githubusercontent.com/u/24882762?v=4?s=100" width="100px;" alt="Genevieve Warren"/><br /><sub><b>Genevieve Warren</b></sub></a><br /><a href="#提示-gewarren" title="GitHub Copilot 可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/guigui42"><img src="https://avatars.githubusercontent.com/u/2376010?v=4?s=100" width="100px;" alt="Guillaume"/><br /><sub><b>Guillaume</b></sub></a><br /><a href="#代理-guigui42" title="GitHub Copilot 专用代理">🎭</a> <a href="#指令-guigui42" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/riqueufmg"><img src="https://avatars.githubusercontent.com/u/108551585?v=4?s=100" width="100px;" alt="Henrique Nunes"/><br /><sub><b>Henrique Nunes</b></sub></a><br /><a href="#提示-riqueufmg" title="GitHub Copilot 可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jeremiah-snee-openx"><img src="https://avatars.githubusercontent.com/u/113928685?v=4?s=100" width="100px;" alt="Jeremiah Snee"/><br /><sub><b>Jeremiah Snee</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=jeremiah-snee-openx" title="代码">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kartikdhiman"><img src="https://avatars.githubusercontent.com/u/59189590?v=4?s=100" width="100px;" alt="Kartik Dhiman"/><br /><sub><b>Kartik Dhiman</b></sub></a><br /><a href="#指令-kartikdhiman" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://kristiyanvelkov.com/"><img src="https://avatars.githubusercontent.com/u/40764277?v=4?s=100" width="100px;" alt="Kristiyan Velkov"/><br /><sub><b>Kristiyan Velkov</b></sub></a><br /><a href="#代理-kristiyan-velkov" title="GitHub Copilot 专用代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/msalaman"><img src="https://avatars.githubusercontent.com/u/28122166?v=4?s=100" width="100px;" alt="msalaman"/><br /><sub><b>msalaman</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=msalaman" title="代码">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://soderlind.no/"><img src="https://avatars.githubusercontent.com/u/1649452?v=4?s=100" width="100px;" alt="Per Søderlind"/><br /><sub><b>Per Søderlind</b></sub></a><br /><a href="#指令-soderlind" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://dotneteers.net/"><img src="https://avatars.githubusercontent.com/u/28162552?v=4?s=100" width="100px;" alt="Peter Smulovics"/><br /><sub><b>Peter Smulovics</b></sub></a><br /><a href="#指令-psmulovics" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/madvimer"><img src="https://avatars.githubusercontent.com/u/3188898?v=4?s=100" width="100px;" alt="Ravish Rathod"/><br /><sub><b>Ravish Rathod</b></sub></a><br /><a href="#指令-madvimer" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://ricksm.it/"><img src="https://avatars.githubusercontent.com/u/7207783?v=4?s=100" width="100px;" alt="Rick Smit"/><br /><sub><b>Rick Smit</b></sub></a><br /><a href="#代理-ricksmit3000" title="GitHub Copilot 专用代理">🎭</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pertrai1"><img src="https://avatars.githubusercontent.com/u/442374?v=4?s=100" width="100px;" alt="Rob Simpson"/><br /><sub><b>Rob Simpson</b></sub></a><br /><a href="#指令-pertrai1" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/inquinity"><img src="https://avatars.githubusercontent.com/u/406234?v=4?s=100" width="100px;" alt="Robert Altman"/><br /><sub><b>Robert Altman</b></sub></a><br /><a href="#指令-inquinity" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://salih.guru/"><img src="https://avatars.githubusercontent.com/u/76786120?v=4?s=100" width="100px;" alt="Tj Vita"/><br /><sub><b>Tj Vita</b></sub></a><br /><a href="#代理-semperteneo" title="GitHub Copilot 专用代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pelikhan"><img src="https://avatars.githubusercontent.com/u/4175913?v=4?s=100" width="100px;" alt="Peli de Halleux"/><br /><sub><b>Peli de Halleux</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=pelikhan" title="代码">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.paulomorgado.net/"><img src="https://avatars.githubusercontent.com/u/470455?v=4?s=100" width="100px;" alt="Paulo Morgado"/><br /><sub><b>Paulo Morgado</b></sub></a><br /><a href="#提示-paulomorgado" title="GitHub Copilot 可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://paul.crane.net.nz/"><img src="https://avatars.githubusercontent.com/u/808676?v=4?s=100" width="100px;" alt="Paul Crane"/><br /><sub><b>Paul Crane</b></sub></a><br /><a href="#代理-pcrane" title="GitHub Copilot 专用代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.pamelafox.org/"><img src="https://avatars.githubusercontent.com/u/297042?v=4?s=100" width="100px;" alt="Pamela Fox"/><br /><sub><b>Pamela Fox</b></sub></a><br /><a href="#提示-pamelafox" title="GitHub Copilot 可重用提示">⌨️</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://oskarthornblad.se/"><img src="https://avatars.githubusercontent.com/u/640102?v=4?s=100" width="100px;" alt="Oskar Thornblad"/><br /><sub><b>Oskar Thornblad</b></sub></a><br /><a href="#指令-prewk" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nischays"><img src="https://avatars.githubusercontent.com/u/54121853?v=4?s=100" width="100px;" alt="Nischay Sharma"/><br /><sub><b>Nischay Sharma</b></sub></a><br /><a href="#代理-nischays" title="GitHub Copilot 专用代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Naikabg"><img src="https://avatars.githubusercontent.com/u/19915620?v=4?s=100" width="100px;" alt="Nikolay Marinov"/><br /><sub><b>Nikolay Marinov</b></sub></a><br /><a href="#代理-Naikabg" title="GitHub Copilot 专用代理">🎭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/niksacdev"><img src="https://avatars.githubusercontent.com/u/20246918?v=4?s=100" width="100px;" alt="Nik Sachdeva"/><br /><sub><b>Nik Sachdeva</b></sub></a><br /><a href="#代理-niksacdev" title="GitHub Copilot 专用代理">🎭</a> <a href="#集合-niksacdev" title="精选相关内容集合">🎁</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://onetipaweek.com/"><img src="https://avatars.githubusercontent.com/u/833231?v=4?s=100" width="100px;" alt="Nick Taylor"/><br /><sub><b>Nick Taylor</b></sub></a><br /><a href="https://github.com/github/awesome-copilot/commits?author=nickytonline" title="代码">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nastanford"><img src="https://avatars.githubusercontent.com/u/1755947?v=4?s=100" width="100px;" alt="Nathan Stanford Sr"/><br /><sub><b>Nathan Stanford Sr</b></sub></a><br /><a href="#指令-nastanford" title="GitHub Copilot 专用指令">🧭</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/matebarabas"><img src="https://avatars.githubusercontent.com/u/22733424?v=4?s=100" width="100px;" alt="Máté Barabás"/><br /><sub><b>Máté Barabás</b></sub></a><br /><a href="#指令-matebarabas" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mikeparker104"><img src="https://avatars.githubusercontent.com/u/12763221?v=4?s=100" width="100px;" alt="Mike Parker"/><br /><sub><b>Mike Parker</b></sub></a><br /><a href="#指令-mikeparker104" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mikekistler"><img src="https://avatars.githubusercontent.com/u/85643503?v=4?s=100" width="100px;" alt="Mike Kistler"/><br /><sub><b>Mike Kistler</b></sub></a><br /><a href="#提示-mikekistler" title="GitHub Copilot 可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/giomartinsdev"><img src="https://avatars.githubusercontent.com/u/125399281?v=4?s=100" width="100px;" alt="Giovanni de Almeida Martins"/><br /><sub><b>Giovanni de Almeida Martins</b></sub></a><br /><a href="#指令-giomartinsdev" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dgh06175"><img src="https://avatars.githubusercontent.com/u/77305722?v=4?s=100" width="100px;" alt="이상현"/><br /><sub><b>이상현</b></sub></a><br /><a href="#指令-dgh06175" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/zooav"><img src="https://avatars.githubusercontent.com/u/12625412?v=4?s=100" width="100px;" alt="Ankur Sharma"/><br /><sub><b>Ankur Sharma</b></sub></a><br /><a href="#提示-zooav" title="GitHub Copilot 可重用提示">⌨️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/oleksiyyurchyna"><img src="https://avatars.githubusercontent.com/u/10256765?v=4?s=100" width="100px;" alt="oleksiyyurchyna"/><br /><sub><b>oleksiyyurchyna</b></sub></a><br /><a href="#集合-oleksiyyurchyna" title="精选相关内容集合">🎁</a> <a href="#提示-oleksiyyurchyna" title="GitHub Copilot 可重用提示">⌨️</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/time-by-waves"><img src="https://avatars.githubusercontent.com/u/34587654?v=4?s=100" width="100px;" alt="oceans-of-time"/><br /><sub><b>oceans-of-time</b></sub></a><br /><a href="#指令-time-by-waves" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kshashank57"><img src="https://avatars.githubusercontent.com/u/57212456?v=4?s=100" width="100px;" alt="kshashank57"/><br /><sub><b>kshashank57</b></sub></a><br /><a href="#代理-kshashank57" title="GitHub Copilot 专用代理">🎭</a> <a href="#指令-kshashank57" title="GitHub Copilot 专用指令">🧭</a></td>
      <td align

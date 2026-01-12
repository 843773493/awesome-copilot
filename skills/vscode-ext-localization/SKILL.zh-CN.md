

---
name: vscode-ext-localization
description: '遵循 VS Code 扩展开发指南、库和最佳实践的 VS Code 扩展正确本地化指南'
---

# VS Code 扩展本地化

此技能可帮助您本地化 VS Code 扩展的各个方面

## 何时使用此技能

当您需要：
- 本地化新或现有的贡献配置（设置）、命令、菜单、视图或引导流程
- 本地化扩展源代码中显示给最终用户的其他字符串资源或消息

# 操作指南

VS Code 本地化包含三种不同的方法，具体取决于要本地化的资源。当创建或更新新的可本地化资源时，必须为所有当前可用语言创建/更新相应的本地化内容。

1. 定义在 `package.json` 中的配置如设置、命令、菜单、视图、视图欢迎页面、引导流程标题和描述
  -> 专属的 `package.nls.LANGID.json` 文件，例如巴西葡萄牙语（`pt-br`）本地化的 `package.nls.pt-br.json` 文件
2. 引导流程内容（定义在自己的 `Markdown` 文件中）
  -> 专属的 `Markdown` 文件，例如巴西葡萄牙语（`pt-br`）本地化的 `walkthrough/someStep.pt-br.md` 文件
3. 扩展源代码中的消息和字符串（JavaScript 或 TypeScript 文件）
  -> 专属的 `bundle.l10n.pt-br.json` 文件用于巴西葡萄牙语本地化
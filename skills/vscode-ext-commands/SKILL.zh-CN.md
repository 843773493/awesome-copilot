

---
name: vscode-ext-commands
description: '为在 VS Code 扩展中贡献命令提供的指南。指示命令的命名规范、可见性、本地化及其他相关属性，遵循 VS Code 扩展开发指南、库和最佳实践'
---

# 在 VS Code 扩展中贡献命令

此技能帮助您在 VS Code 扩展中添加或更新命令

## 何时使用此技能

当您需要以下操作时使用此技能：
- 向您的 VS Code 扩展添加或更新命令

# 操作指南

VS Code 命令必须始终定义一个 `title`，无论其分类、可见性或位置如何。我们为每种“类型”的命令使用几种模式，其中包含一些特性，如下所述：

* 普通命令：默认情况下，所有命令都应在命令面板（Command Palette）中可访问，必须定义一个 `category`，除非该命令将用于侧边栏（Side Bar），否则不需要定义 `icon`。

* 侧边栏命令：其名称遵循特殊模式，以下划线（`_`）开头，后缀为 `#sideBar`，例如 `_extensionId.someCommand#sideBar`。必须定义一个 `icon`，并且可能需要定义 `enablement` 的启用条件。仅限侧边栏的命令不应在命令面板中显示。若将其贡献到 `view/title` 或 `view/item/context`，则必须告知其显示的 _顺序/位置_，并可以使用“相对于其他命令/按钮”等术语来帮助您识别正确的 `group`。此外，为新命令定义可见性条件（`when`）是一个良好的实践。
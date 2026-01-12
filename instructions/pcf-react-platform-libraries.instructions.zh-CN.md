

---
description: '用于 PCF 组件的 React 控件和平台库'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj}'
---

# React 控件与平台库

当你使用 React 和平台库时，你正在使用与 Power Apps 平台相同的基础设施。这意味着你不再需要为每个控件单独打包 React 和 Fluent 库。所有控件共享同一个库实例和版本，以提供无缝且一致的体验。

## 优势

通过重用现有的平台 React 和 Fluent 库，你可以预期以下好处：

- **减少控件包大小**
- **优化解决方案打包**
- **更快的运行时传输、脚本执行和控件渲染**
- **与 Power Apps Fluent 设计系统的设计和主题保持一致**

> **注意**：在 GA 发布后，所有现有的虚拟控件将继续正常运行。但是，它们应使用最新版本的 CLI（>=1.37）重新构建和部署，以方便未来平台 React 版本的升级。

## 先决条件

与任何组件一样，你必须安装 [Visual Studio Code](https://code.visualstudio.com/Download) 和 [Microsoft Power Platform CLI](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/powerapps-cli#install-microsoft-power-platform-cli)。

> **注意**：如果你已经为 Windows 安装了 Power Platform CLI，请使用 `pac install latest` 命令确保你正在运行最新版本。Visual Studio Code 中的 Power Platform 工具将自动更新。

## 创建 React 组件

> **注意**：这些说明假设你已经创建过代码组件。如果没有，请参阅 [创建你的第一个组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/implementing-controls-using-typescript)。

`pac pcf init` 命令现在有一个新的 `--framework` (`-fw`) 参数。将此参数的值设置为 `react`。

### 命令参数

| 参数 | 值 |
|-----------|-------|
| --name | ReactSample |
| --namespace | SampleNamespace |
| --template | field |
| --framework | react |
| --run-npm-install | true (默认) |

### PowerShell 命令

以下 PowerShell 命令使用参数快捷方式，并创建一个 React 组件项目并运行 `npm-install`：

```powershell
pac pcf init -n ReactSample -ns SampleNamespace -t field -fw react -npm
```

现在你可以使用 `npm start` 通常方式构建并查看控件的测试环境。

在构建控件后，你可以将其打包到解决方案中，并用于模型驱动的应用（包括自定义页面）和画布应用，如同标准代码组件一样。

## 与标准组件的不同之处

### ControlManifest.Input.xml

[控件元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/control) 的 `control-type` 属性设置为 `virtual`，而不是 `standard`。

> **注意**：更改此值不会将组件从一种类型转换为另一种类型。

在 [资源元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/resources) 中，找到两个新的 [平台库元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/platform-library) 子元素：

```xml
<resources>
  <code path="index.ts" order="1" />
  <platform-library name="React" version="16.14.0" />
  <platform-library name="Fluent" version="9.46.2" />
</resources>
```

> **注意**：有关有效平台库版本的更多信息，请参见支持的平台库列表。

**推荐**：我们推荐使用 Fluent 8 和 Fluent 9 的平台库。如果你不使用 Fluent，请删除 `name` 属性值为 `Fluent` 的 `platform-library` 元素。

### Index.ts

控件初始化的 [ReactControl.init](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/react-control/init) 方法不包含 `div` 参数，因为 React 控件不会直接渲染 DOM。相反，[ReactControl.updateView](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/react-control/updateview) 返回一个 ReactElement，该元素包含 React 格式的实际控件详细信息。

### bundle.js

React 和 Fluent 库未包含在包中，因为它们是共享的，因此 bundle.js 的大小更小。

## 示例控件

以下控件包含在示例中。它们的功能与标准版本相同，但因为是虚拟控件，性能更优。

| 示例 | 描述 | 链接 |
|--------|-------------|------|
| ChoicesPickerReact | 将标准的 ChoicesPickerControl 转换为 React 控件 | [ChoicesPickerReact 示例](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/platform-library) |
| FacepileReact | 将 ReactStandardControl 转换为 React 控件 | [FacepileReact 示例](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/platform-library) |

## 支持的平台库列表

平台库在构建和运行时都对使用平台库功能的控件可用。目前，平台提供了以下版本，且为当前支持的最高版本。

| 库 | 包 | 构建版本 | 运行时版本 |
|---------|---------|---------------|-----------------|
| React | react | 16.14.0 | 17.0.2（模型驱动应用）、16.14.0（画布应用） |
| Fluent | @fluentui/react | 8.29.0 | 8.29.0 |
| Fluent | @fluentui/react | 8.121.1 | 8.121.1 |
| Fluent | @fluentui/react-components | >=9.4.0 <=9.46.2 | 9.68.0 |

> **注意**：应用程序可能在运行时加载平台库的更高兼容版本，但该版本可能不是最新可用版本。Fluent 8 和 Fluent 9 各自受支持，但不能同时在同一个清单中指定。

## 常见问题解答

### Q: 我可以使用平台库将现有的标准控件转换为 React 控件吗？

A: 不可以。你必须使用新模板创建一个新的控件，然后更新清单和 index.ts 方法。作为参考，可以比较上述描述的标准和 React 示例。

### Q: 我可以在 Power Pages 中使用 React 控件和平台库吗？

A: 不可以。React 控件和平台库目前仅支持画布应用和模型驱动应用。在 Power Pages 中，React 控件不会根据其他字段的变化进行更新。

## 相关文章

- [什么是代码组件？](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/custom-controls-overview)
- [画布应用的代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/component-framework-for-canvas-apps)
- [创建和构建代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/create-custom-controls-using-pcf)
- [学习 Power Apps 组件框架](https://learn.microsoft.com/en-us/training/paths/use-power-apps-component-framework)
- [在 Power Pages 中使用代码组件](https://learn.microsoft.com/en-us/power-apps/maker/portals/component-framework)
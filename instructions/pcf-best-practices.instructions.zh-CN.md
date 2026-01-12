

---
description: '开发PCF代码组件的最佳实践和指南'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj,css,html}'
---

# 代码组件的最佳实践和指南

开发、部署和维护代码组件需要跨多个领域的知识。本文概述了开发代码组件的专业人士应遵循的已建立的最佳实践和指南。

## Power Apps Component Framework

### 避免将开发构建部署到 Dataverse

代码组件可以在[生产模式或开发模式](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/code-components-alm#building-pcfproj-code-component-projects)下构建。避免将开发构建部署到 Dataverse，因为它们会严重影响性能，甚至可能因体积过大而被阻止部署。即使你计划之后部署发布构建，如果你没有自动化的发布流水线，也可能会忘记重新部署。更多信息：[调试自定义控件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/debugging-custom-controls)。

### 避免使用不受支持的框架方法

这些包括使用未记录的内部方法，这些方法存在于 `ComponentFramework.Context` 上。这些方法可能目前可以工作，但由于不受支持，未来版本可能会停止工作。访问主机应用程序 HTML 文档对象模型 (DOM) 的控件脚本也不受支持。任何位于代码组件边界之外的主机应用程序 DOM 部分都可能在没有通知的情况下发生变化。

### 使用 `init` 方法请求网络所需资源

当托管上下文加载代码组件时，首先会调用 `init` 方法。使用此方法请求任何网络资源（如元数据），而不是等待 `updateView` 方法。如果在请求返回之前调用了 `updateView` 方法，你的代码组件必须处理此状态并提供可视的加载指示器。

### 在 `destroy` 方法中清理资源

当代码组件从浏览器 DOM 中移除时，托管上下文会调用 `destroy` 方法。使用 `destroy` 方法关闭任何 `WebSockets` 并移除在容器元素之外添加的事件处理程序。如果你使用 React，应在 `destroy` 方法中使用 `ReactDOM.unmountComponentAtNode`。通过这种方式清理资源可以防止因代码组件在浏览器会话中被加载和卸载而引起的性能问题。

### 避免不必要的调用 `refresh` 方法

如果你的代码组件是数据集类型，绑定的数据集属性会暴露一个 `refresh` 方法，该方法会导致托管上下文重新加载数据。不必要的调用此方法会影响代码组件的性能。

### 最小化对 `notifyOutputChanged` 的调用

在某些情况下，不希望 UI 控件的更新（如按键或鼠标移动事件）每次调用 `notifyOutputChanged`，因为更多的调用会导致不必要的更多事件传递给父上下文。相反，可以考虑在控件失去焦点时，或在用户的触摸或鼠标事件完成后使用事件。

### 检查 API 可用性

在为不同主机（如模型驱动应用、画布应用、门户）开发代码组件时，始终检查你使用的 API 在这些平台上的可用性。例如，`context.webAPI` 在画布应用中不可用。有关个别 API 可用性的信息，请参阅[Power Apps 组件框架 API 参考](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/)。

### 管理临时为 null 的属性值传递给 `updateView`

当数据未准备好时，会将 null 值传递给 `updateView` 方法。你的组件应考虑到这种情况，并预期数据可能为 null，后续的 `updateView` 周期可能包含更新后的值。`updateView` 对于[标准组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/control/updateview)和[React 组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/react-control/updateview)都可用。

## 模型驱动应用

### 不要直接与 `formContext` 交互

如果你有使用客户端 API 的经验，可能习惯于通过 `formContext` 访问属性、控件并调用 API 方法，如 `save`、`refresh` 和 `setNotification`。代码组件应能在各种产品（如模型驱动应用、画布应用和仪表板）中运行，因此不能依赖 `formContext`。

一种变通方法是将代码组件绑定到某一列，并在该列上添加 `OnChange` 事件处理程序。代码组件可以更新该列的值，而 `OnChange` 事件处理程序可以访问 `formContext`。未来将添加对自定义事件的支持，这将允许在不添加列配置的情况下，与控件外部进行通信。

### 限制对 `WebApi` 的调用次数和数据量

在使用 `context.WebApi` 方法时，限制调用次数和数据量。每次调用 `WebApi` 都会计算在用户的 API 权限和服务保护限制中。在对记录执行 CRUD 操作时，考虑数据负载的大小。通常，请求负载越大，代码组件的运行速度越慢。

## 画布应用

### 最小化屏幕上的组件数量

每次向画布应用添加组件时，都需要一定的时间来渲染。随着组件数量的增加，渲染时间也会增加。在向屏幕添加更多组件时，使用开发者性能工具仔细测量代码组件的性能。

目前，使用 `pac pcf init` 的代码组件模板不会使用树摇（tree-shaking），这是 `webpack` 检测到未使用的模块并移除它们的过程。如果你使用以下命令从 Fluent UI 导入，它会导入并捆绑整个库：

```typescript
import { Button } from '@fluentui/react'
```

为了避免导入和捆绑整个库，可以使用基于路径的导入方式，通过显式路径导入特定的库组件：

```typescript
import { Button } from '@fluentui/react/lib/Button';
```

使用特定路径可以减少开发和发布构建中的捆绑体积。

### 优化 React 渲染

在使用 React 时，遵循 React 的最佳实践以最小化组件的渲染：

- 仅在 `updateView` 方法中调用 `ReactDOM.render`，当绑定属性或框架方面发生变化时需要 UI 反映变化。你可以使用 `updatedProperties` 来确定发生了哪些变化。
- 在可能的情况下使用 `PureComponent`（用于类组件）或 `React.memo`（用于函数组件）以避免不必要的重新渲染。
- 对于大型 React 组件，将 UI 分解为更小的组件以提高性能。
- 避免在渲染函数中使用箭头函数和函数绑定，因为这些做法会在每次渲染时创建新的回调闭包。

### 检查可访问性

确保代码组件可访问，以便键盘用户和屏幕阅读器用户可以使用它们：

- 提供替代的键盘导航方式，以替代鼠标/触摸事件
- 确保设置 `alt` 和 [ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)（可访问的丰富互联网应用）属性，以便屏幕阅读器能够准确地宣布代码组件的界面
- 现代浏览器开发者工具提供了检查可访问性的有用方法

更多信息：[在 Power Apps 中创建可访问的画布应用](https://learn.microsoft.com/en-us/powerapps/maker/canvas-apps/accessible-apps)。

### 始终使用异步网络调用

在进行网络调用时，永远不要使用同步阻塞请求，因为这会导致应用停止响应并出现缓慢的性能问题。更多信息：[异步与 HTTP 和 HTTPS 资源交互](https://learn.microsoft.com/en-us/powerapps/developer/model-driven-apps/best-practices/business-logic/interact-http-https-resources-asynchronously)。

### 为多种浏览器编写代码

模型驱动应用、画布应用和门户均支持多种浏览器。确保只使用所有现代浏览器都支持的技术，并为你的目标用户群体使用具有代表性的浏览器进行测试。

- [限制和配置](https://learn.microsoft.com/en-us/powerapps/maker/canvas-apps/limits-and-config)
- [支持的网络浏览器](https://learn.microsoft.com/en-us/power-platform/admin/supported-web-browsers-and-mobile-devices)
- [Office 使用的浏览器](https://learn.microsoft.com/en-us/office/dev/add-ins/concepts/browsers-used-by-office-web-add-ins)

### 代码组件应计划支持多种客户端和屏幕格式

代码组件可以在多种客户端（模型驱动应用、画布应用、门户）和屏幕格式（移动、平板、网页）中渲染。

- 使用 `trackContainerResize` 可以让代码组件响应可用宽度和高度的变化
- 使用 `allocatedHeight` 和 `allocatedWidth` 可以与 `getFormFactor` 结合使用，以确定代码组件是否在移动、平板或网页客户端上运行
- 实现 `setFullScreen` 可让用户在空间有限时扩展以使用整个可用屏幕
- 如果代码组件在给定的容器大小下无法提供有意义的体验，应适当禁用功能并为用户提供反馈

### 始终使用作用域 CSS 规则

当你使用 CSS 对代码组件进行样式设计时，确保使用自动应用到组件容器 `DIV` 元素的 CSS 类来对 CSS 进行作用域限定。如果 CSS 是全局作用域，可能会破坏代码组件所在表单或屏幕的现有样式。

例如，如果你的命名空间是 `SampleNamespace`，代码组件名称是 `LinearInputComponent`，你可以使用以下自定义 CSS 规则：

```css
.SampleNamespace\.LinearInputComponent rule-name
```

### 避免使用 Web 存储对象

代码组件不应使用 HTML Web 存储对象（如 `window.localStorage` 和 `window.sessionStorage`）来存储数据。存储在用户浏览器或移动客户端上的数据不安全，且不能保证可靠地可用。

## ALM/Azure DevOps/GitHub

请参阅[代码组件的应用生命周期管理（ALM）](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/code-components-alm)文章，了解在 ALM/Azure DevOps/GitHub 中使用代码组件的最佳实践。

## 相关文章

- [什么是代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/custom-controls-overview)
- [画布应用的代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/component-framework-for-canvas-apps)
- [创建和构建代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/create-custom-controls-using-pcf)
- [学习 Power Apps 组件框架](https://learn.microsoft.com/en-us/training/paths/use-power-apps-component-framework)
- [在 Power Pages 中使用代码组件](https://learn.microsoft.com/en-us/power-apps/maker/portals/component-framework)
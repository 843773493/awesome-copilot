

---
description: 'Power Apps 组件框架的限制和注意事项'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj}'
---

# 限制

借助 Power Apps 组件框架，您可以创建自定义代码组件以提升 Power Apps 和 Power Pages 的用户体验。尽管可以创建自定义组件，但某些限制会阻碍开发者在代码组件中实现特定功能。以下是部分限制：

## 1. 画布应用不支持依赖于 Microsoft Dataverse 的 API

目前，Power Apps 画布应用不支持依赖于 Microsoft Dataverse 的 API，包括 WebAPI。如需了解单个 API 的可用性，请参阅 [Power Apps 组件框架 API 参考](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/)。

## 2. 打包外部库或使用平台库

代码组件应使用 [React 控件和平台库](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/react-controls-platform-libraries)，或将所有代码（包括外部库内容）打包到主代码包中。

如需查看 Power Apps 命令行界面如何帮助您将外部库内容打包到特定组件的代码包中，请参阅 [Angular 翻转组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/sample-controls/angular-flip-control) 示例。

## 3. 不要使用 HTML Web 存储对象

代码组件不应使用 HTML Web 存储对象（如 `window.localStorage` 和 `window.sessionStorage`）来存储数据。在用户浏览器或移动客户端上本地存储的数据不安全，且无法保证可靠访问。

## 4. 画布应用不支持自定义身份验证

在 Power Apps 画布应用中，代码组件不支持自定义身份验证。请改用连接器来获取数据并执行操作。

## 相关主题

- [Power Apps 组件框架 API 参考](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/)
- [Power Apps 组件框架概述](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview)
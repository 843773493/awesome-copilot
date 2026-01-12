

---
description: 'Power Apps 组件框架概述和基础概念'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj}'
---

# Power Apps 组件框架概述

Power Apps 组件框架赋能专业开发人员和应用构建者，创建用于模型驱动型应用和画布应用的代码组件。这些代码组件可以用于提升用户在表单、视图、仪表板和画布应用屏幕中处理数据时的体验。

## 核心功能

您可以使用 PCF 来：
- 将表单上显示数字文本值的列替换为 `dial` 或 `slider` 代码组件
- 将列表转换为完全不同的视觉体验，与数据集绑定，例如 `日历` 或 `地图`

## 重要限制

- Power Apps 组件框架仅适用于统一界面，不适用于传统的网页客户端
- Power Apps 组件框架目前不支持本地部署环境

## PCF 与 Web 资源的区别

与 HTML Web 资源不同，代码组件：
- 在相同上下文中渲染
- 与任何其他组件同时加载
- 为用户提供无缝体验

代码组件可以：
- 在 Power Apps 的全部功能范围内使用
- 在不同的表和表单之间多次复用
- 将所有 HTML、CSS 和 TypeScript 文件捆绑到一个解决方案包中
- 在不同环境之间迁移
- 通过 AppSource 提供

## 核心优势

### 丰富的框架 API
- 组件生命周期管理
- 访问上下文数据和元数据
- 通过 Web API 实现无缝服务器访问
- 工具方法和数据格式化方法
- 设备功能：相机、位置、麦克风
- 用户体验元素：对话框、查找、全屏渲染

### 开发优势
- 支持现代网页开发实践
- 优化性能
- 高可复用性
- 将所有文件捆绑到一个解决方案文件中
- 为性能原因处理组件的销毁和重新加载，同时保留状态

## 授权要求

Power Apps 组件框架的授权基于所使用的数据和连接类型：

### 高级代码组件
通过用户的浏览器客户端直接连接到外部服务或数据的代码组件（不通过连接器）：
- 被视为高级组件
- 使用这些组件的应用将被归类为高级
- 最终用户需要 Power Apps 授权

通过在清单中添加以下内容声明为高级组件：
```xml
<external-service-usage enabled="true">
  <domain>www.microsoft.com</domain>
</external-service-usage>
```

### 标准代码组件
不连接到外部服务或数据的代码组件：
- 使用这些组件的标准功能的应用保持为标准应用
- 最终用户需要最低级别的 Office 365 授权

**注意**：如果在连接到 Microsoft Dataverse 的模型驱动型应用中使用代码组件，最终用户将需要 Power Apps 授权。

## 相关资源

- [什么是代码组件？](https://learn.microsoft.com/zh-cn/power-apps/developer/component-framework/custom-controls-overview)
- [画布应用的代码组件](https://learn.microsoft.com/zh-cn/power-apps/developer/component-framework/component-framework-for-canvas-apps)
- [创建和构建代码组件](https://learn.microsoft.com/zh-cn/power-apps/developer/component-framework/create-custom-controls-using-pcf)
- [学习 Power Apps 组件框架](https://learn.microsoft.com/zh-cn/training/paths/use-power-apps-component-framework)
- [在 Power Pages 中使用代码组件](https://learn.microsoft.com/zh-cn/power-apps/maker/portals/component-framework)

## 培训资源

- [使用 Power Apps 组件框架创建组件 - 培训](https://learn.microsoft.com/zh-cn/training/paths/create-components-power-apps-component-framework/)
- [Microsoft 认证：Power Platform 开发人员助理](https://learn.microsoft.com/zh-cn/credentials/certifications/power-platform-developer-associate/)
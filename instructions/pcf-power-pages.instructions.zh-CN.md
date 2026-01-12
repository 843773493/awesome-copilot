

---
description: '在 Power Pages 网站中使用代码组件'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj}'
---

# 在 Power Pages 中使用代码组件

Power Pages 现在支持使用 Power Apps 组件框架构建的模型驱动型应用程序控件。要在 Power Pages 网站页面中使用代码组件：

![使用组件框架创建代码组件，然后将其添加到模型驱动型应用程序表单中，并在门户的基本表单中配置代码组件字段](https://learn.microsoft.com/en-us/power-pages/configure/media/component-framework/steps.png)

完成这些步骤后，用户可以通过包含相应 [表单](https://learn.microsoft.com/en-us/power-pages/getting-started/add-form) 组件的网页与代码组件进行交互。

## 先决条件

- 需要系统管理员权限才能在环境中启用代码组件功能
- 您的 Power Pages 网站版本需要为 [9.3.3.x](https://learn.microsoft.com/en-us/power-apps/maker/portals/versions/version-9.3.3.x) 或更高版本
- 您的初始网站包需要为 [9.2.2103.x](https://learn.microsoft.com/en-us/power-apps/maker/portals/versions/package-version-9.2.2103) 或更高版本

## 创建和打包代码组件

要了解如何在 Power Apps 组件框架中创建和打包代码组件，请访问 [创建第一个组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/implementing-controls-using-typescript)。

### 支持的字段类型和格式

Power Pages 对使用代码组件支持受限的字段类型和格式。下表列出了所有支持的字段数据类型和格式：

**支持的类型：**
- 货币
- 日期和时间.DateAndTime
- 日期和时间.DateOnly
- 小数
- 枚举
- 浮点数
- 多选
- OptionSet
- 单行.Email
- 单行.Phone
- 单行.Text
- 单行.TextArea
- 单行.Ticker
- 单行.URL
- 二选一
- 整数

如需更多信息，请参阅 [属性列表和描述](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/property#remarks)。

### Power Pages 不支持的代码组件

以下代码组件 API 不被支持：
- [Device.captureAudio](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/captureaudio)
- [Device.captureImage](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/captureimage)
- [Device.captureVideo](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/capturevideo)
- [Device.getBarcodeValue](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/getbarcodevalue)
- [Device.getCurrentPosition](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/getcurrentposition)
- [Device.pickFile](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/pickfile)
- [Utility](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/utility)

**其他限制：**
- [uses-feature](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/uses-feature) 元素不能设置为 true
- Power Apps 组件框架不支持的 [值元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/property#value-elements-that-are-not-supported)
- Power Apps 组件框架 (PCF) 控件绑定到表单中的多个字段不被支持

## 将代码组件添加到模型驱动型应用程序的字段中

要了解如何将代码组件添加到模型驱动型应用程序的字段中，请访问 [将代码组件添加到字段](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/add-custom-controls-to-a-field-or-entity#add-a-code-component-to-a-column)。

> **重要提示**：Power Pages 的代码组件仅通过 **Web** 客户端选项在网页浏览器中可用。

### 使用数据工作区添加

您也可以通过 [数据工作区](https://learn.microsoft.com/en-us/power-pages/configure/data-workspace-forms) 将代码组件添加到表单中。

1. 在数据工作区表单设计器中编辑 Dataverse 表单时，选择一个字段
2. 选择 **+ 组件**，并为该字段选择适当的组件

   ![将组件添加到表单](https://learn.microsoft.com/en-us/power-pages/configure/media/component-framework/add-component-to-form.png)

3. 选择 **保存** 和 **发布表单**

## 配置 Power Pages 网站以使用代码组件

在模型驱动型应用程序中将代码组件添加到字段后，您可以配置 Power Pages 以在表单上使用该代码组件。

有两种方法可以启用代码组件：

### 在设计工作室中启用代码组件

要使用设计工作室在表单上启用代码组件：

1. 在您 [将表单添加到页面](https://learn.microsoft.com/en-us/power-pages/getting-started/add-form) 后，选择添加了代码组件的字段并选择 **编辑字段**
2. 选择 **启用自定义组件** 字段

   ![在设计工作室中启用自定义组件](https://learn.microsoft.com/en-us/power-pages/configure/media/component-framework/enable-code-component.png)

3. 预览网站时，您应该能看到自定义组件已启用

### 在门户管理应用中启用代码组件

要使用门户管理应用将代码组件添加到基本表单中：

1. 打开 [门户管理](https://learn.microsoft.com/en-us/power-pages/configure/portal-management-app) 应用
2. 在左侧窗格中，选择 **基本表单**
3. 选择要添加代码组件的表单
4. 选择 **相关**
5. 选择 **基本表单元数据**
6. 选择 **新建基本表单元数据**
7. 将 **类型** 设置为 **属性**
8. 选择 **属性逻辑名称**
9. 输入 **标签**
10. 对于 **控件样式**，选择 **代码组件**
11. 保存并关闭表单

## 使用门户 Web API 的代码组件

代码组件可以构建并添加到使用 [门户 Web API](https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview) 进行创建、检索、更新和删除操作的网页中。此功能在开发门户解决方案时提供了更大的自定义选项。如需更多信息，请参阅 [实现示例门户 Web API 组件](https://learn.microsoft.com/en-us/power-pages/configure/implement-webapi-component)。

## 后续步骤

[教程：在门户中使用代码组件](https://learn.microsoft.com/en-us/power-pages/configure/component-framework-tutorial)

## 参见

- [Power Apps 组件框架概述](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview)
- [创建第一个组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/implementing-controls-using-typescript)
- [将代码组件添加到模型驱动型应用程序的列或表中](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/add-custom-controls-to-a-field-or-entity)
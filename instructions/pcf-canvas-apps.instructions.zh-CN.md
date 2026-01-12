

---
description: '画布应用的代码组件，用于实现、安全性和配置'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj}'
---

# 画布应用的代码组件

专业开发人员可以使用 Power Apps 组件框架创建可在其画布应用中使用的代码组件。应用构建者可以使用 Power Apps 组件框架通过 [Microsoft Power Platform CLI](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/get-powerapps-cli) 创建、导入并添加代码组件到画布应用中。

> **注意**: 某些 API 可能在画布应用中不可用。我们建议您检查每个 API 以确定其可用性。

## 安全性考虑

> **警告**: 代码组件包含可能由 Microsoft 以外的来源生成的代码，并且在 Power Apps Studio 中渲染时可能会访问安全令牌和数据。在将代码组件添加到画布应用时，请确保代码组件解决方案来自可信来源。此漏洞仅在运行画布应用时不存在。

### Power Apps Studio 中的安全警告

当您在 Power Apps Studio 中打开包含代码组件的画布应用时，会显示一条关于潜在不安全代码的警告信息。在 Power Apps Studio 环境中，代码组件可以访问安全令牌，因此只有来自可信来源的组件才应被打开。

**最佳实践：**
- 管理员和系统自定义人员应在将代码组件导入环境之前审查并验证所有代码组件
- 仅在验证后将组件提供给应用构建者
- 使用非受管解决方案导入代码组件或使用 `pac pcf push` 安装代码组件时，会显示 **Default** 出版商

![安全警告](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/canvas-app-safety-warning.png)

## 先决条件

- 需要 Power Apps 许可证。更多信息：[Power Apps 组件框架许可证](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview#licensing)
- 需要系统管理员权限以在环境中启用 Power Apps 组件框架功能

## 启用 Power Apps 组件框架功能

要在应用中添加代码组件，您需要在希望使用它们的每个环境中启用 Power Apps 组件框架功能。默认情况下，Power Apps 组件功能已启用用于模型驱动型应用。

### 启用画布应用的步骤：

1. 登录到 [Power Apps](https://powerapps.microsoft.com/)
2. 选择 **设置** ![设置](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/settings.png)，然后选择 **管理中心**

   ![设置和管理中心](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/select-admin-center-from-settings.png)

3. 在左侧窗格中，选择 **环境**，选择要启用此功能的环境，然后选择 **设置**
4. 展开 **产品**，然后选择 **功能**
5. 从可用功能列表中打开 **Power Apps 组件框架用于画布应用**，然后选择 **保存**

   ![启用 Power Apps 组件框架](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/enable-pcf-feature.png)

## 实现代码组件

在您的环境中启用 Power Apps 组件框架功能后，您可以开始实现代码组件的逻辑。如需逐步教程，请访问 [创建第一个代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/implementing-controls-using-typescript)。

**建议**: 在开始实现之前，请检查 [画布应用的代码组件限制](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/limitations)。

## 将组件添加到画布应用

1. 打开 Power Apps Studio
2. 创建一个新的画布应用，或编辑要添加代码组件的现有应用

   > **重要**: 请确保包含代码组件的解决方案 .zip 文件已先通过 [导入、更新和导出解决方案](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/import-update-export-solutions) 导入到 Microsoft Dataverse 中，然后再继续下一步。

3. 在左侧窗格中，选择 **+**，然后选择 **获取更多组件**

   ![插入组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/insert-code-components-using-get-more-components.png)

4. 选择 **代码** 选项卡，从列表中选择一个组件，然后选择 **导入**

   ![导入组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/insert-component-add-sample-component.png)

5. 在左侧窗格中，选择 **+**，展开 **代码组件**，然后选择要添加的组件

   ![添加组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/add-sample-component-from-list.png)

> **注意**: 您也可以通过选择 **插入 > 自定义 > 导入组件** 来添加组件。此选项将在未来版本中移除，因此我们建议使用上述流程。

### 组件属性

在 **属性** 选项卡中，您将看到代码组件的属性显示。

![默认代码组件属性面板](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/property-pane-with-parameters.png)

> **注意**: 如果您希望在默认的属性选项卡中看到现有代码组件的属性，请通过更新代码组件的清单版本重新导入现有组件。如前所述，属性将继续在高级属性选项卡中可用。

## 从画布应用中删除代码组件

1. 打开已添加代码组件的应用
2. 在左侧窗格中，选择 **树形视图**，然后选择已添加代码组件的屏幕
3. 在组件旁边，选择 **更多 (...)**，然后选择 **删除**

   ![删除代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/delete-code-component.png)

4. 保存应用以查看更改

## 更新现有代码组件

每次您更新代码组件并希望查看运行时更改时，都需要在清单文件中更改 `version` 属性。我们建议在每次进行更改时都更改组件的版本。

> **注意**: 仅当在 Power Apps Studio 中关闭或重新打开应用时，才会更新现有的代码组件。当您重新打开应用时，系统会提示您更新代码组件。简单地删除或重新添加代码组件到应用中不会更新组件。请先发布更新后的解决方案中的所有自定义内容，否则对代码组件的更改将不会显示。
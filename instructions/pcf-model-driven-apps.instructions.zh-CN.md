

---
description: '用于模型驱动应用程序实现和配置的代码组件'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj}'
---

# 模型驱动应用程序的代码组件

Power Apps 组件框架为开发者提供了扩展模型驱动应用程序中可视化组件的能力。专业开发者可以使用 [Microsoft Power Platform CLI](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/get-powerapps-cli) 创建、调试、导入并添加代码组件到模型驱动应用程序中。

## 组件使用

您可以在模型驱动应用程序中将代码组件添加到以下位置：
- 列
- 网格
- 子网格

> **重要说明**: Power Apps 组件框架默认已启用模型驱动应用程序。如需了解如何为画布应用启用 Power Apps 组件框架，请参阅 [画布应用的代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/component-framework-for-canvas-apps)。

## 实现代码组件

在开始创建代码组件之前，请确保已安装所有 [必需的先决条件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/create-custom-controls-using-pcf#prerequisites)，以便使用 Power Apps 组件框架开发组件。

文章 [创建第一个代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/implementing-controls-using-typescript) 详细介绍了创建代码组件的逐步过程。

## 将代码组件添加到模型驱动应用程序

如需将代码组件添加到模型驱动应用程序中的列或表，请参阅 [将代码组件添加到模型驱动应用程序](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/add-custom-controls-to-a-field-or-entity)。

### 示例

**线性滑块控件:**

![添加线性滑块控件](https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/media/add-slider.png)

**数据集网格组件:**

![数据集网格组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/add-dataset-component.png)

## 更新现有代码组件

每次更新代码组件并希望在运行时看到更改时，都需要在清单文件中升级版本属性。

**最佳实践**: 每次修改组件时，都建议升级其版本。

## 参见

- [Power Apps 组件框架概述](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview)
- [创建第一个代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/implementing-controls-using-typescript)
- [学习 Power Apps 组件框架](https://learn.microsoft.com/en-us/training/paths/use-power-apps-component-framework)
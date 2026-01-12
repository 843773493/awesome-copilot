

---
description: '在 PCF 组件中使用依赖库'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj}'
---

# 依赖库（预览）

[本主题是预发布文档，可能会发生更改。]

在模型驱动应用程序中，您可以重用另一个组件中包含的预构建库，该组件作为多个组件的依赖项被加载。

在多个控件中包含预构建库的副本是不理想的。重用现有库可以提高性能，特别是在库较大时，通过减少使用该库的所有组件的加载时间。库的重用还能帮助减少构建过程中的维护负担。

## 之前和之后

**之前**：每个 PCF 组件中包含自定义库文件
![展示每个 pcf 组件中包含自定义库文件的图表](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/dependent-library-before-example.png)

**之后**：组件调用来自库控件的共享函数
![展示组件调用来自库控件的共享函数的图表](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/dependent-library-after-example.png)

## 实现步骤

要使用依赖库，您需要：

1. 创建一个 **库组件** 来包含库。该组件可以提供某些功能，也可以仅作为库的容器。
2. 配置另一个组件以依赖由库组件加载的库。

默认情况下，库会在依赖组件加载时自动加载，但您可以配置为按需加载。

这样您就可以在库控件中独立维护库，而依赖组件无需将库文件打包在自身中。

## 工作原理

您需要向组件项目中添加配置数据，以便构建过程按照您的要求部署库。通过添加或编辑以下文件来设置这些配置数据：

- **featureconfig.json**
- **webpack.config.js**
- 编辑清单架构以 **注册依赖项**

### featureconfig.json

将此文件添加到项目中，以覆盖组件的默认功能标志，而无需修改 `node_modules` 文件夹中生成的文件。

**功能标志：**

| 标志 | 描述 |
|------|-------------|
| `pcfResourceDependency` | 启用组件使用库资源。 |
| `pcfAllowCustomWebpack` | 启用组件使用自定义 Webpack。此功能必须为定义库资源的组件启用。 |

默认情况下，这些值为 `off`。将其设置为 `on` 以覆盖默认值。

**示例 1：**
```json
{ 
  "pcfAllowCustomWebpack": "on" 
} 
```

**示例 2：**
```json
{ 
   "pcfResourceDependency": "on",
   "pcfAllowCustomWebpack": "off" 
} 
```

### webpack.config.js

组件的构建过程使用 [Webpack](https://webpack.js.org/) 将代码和依赖项捆绑为可部署的资产。要排除您的库不参与此捆绑，需在项目根文件夹中添加一个 `webpack.config.js` 文件，指定库的别名为 `externals`。[了解更多关于 Webpack 的 externals 配置选项](https://webpack.js.org/configuration/externals/)

当库别名为 `myLib` 时，此文件可能如下所示：

```javascript
/* eslint-disable */ 
"use strict"; 

module.exports = { 
  externals: { 
    "myLib": "myLib" 
  }, 
}  
```

### 注册依赖项

在清单架构的 [resources](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/resources) 元素中使用 [dependency 元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/dependency)。

```xml
<resources>
  <dependency
    type="control"
    name="samples_SampleNS.SampleStubLibraryPCF"
    order="1"
  />
  <code path="index.ts" order="2" />
</resources>
```

### 依赖项作为组件的按需加载

您不必在组件加载时加载依赖库，而是可以按需加载依赖库。按需加载为更复杂的控件提供了灵活性，仅在需要时加载依赖项，特别是当依赖库较大时。

![展示从库中调用函数的场景，其中库是按需加载的](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/dependent-library-on-demand-load.png)

要启用按需加载，您需要：

**步骤 1**：将这些 [platform-action 元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/platform-action)、[feature-usage 元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/feature-usage) 和 [uses-feature 元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/uses-feature) 子元素添加到 [control 元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/control) 中：

```xml
<platform-action action-type="afterPageLoad" />
<feature-usage>
   <uses-feature name="Utility"
      required="true" />
</feature-usage>
```

**步骤 2**：将 [dependency 元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/dependency) 的 `load-type` 属性设置为 `onDemand`。

```xml
<dependency type="control"
      name="samples_SampleNamespace.StubLibrary"
      load-type="onDemand" />
```

## 下一步操作

尝试一个教程，了解如何创建依赖库：

[教程：在组件中使用依赖库](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/tutorial-use-dependent-libraries)
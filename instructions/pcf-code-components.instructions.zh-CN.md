

---
description: '了解代码组件的结构和实现'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj}'
---

# 代码组件

代码组件是一种解决方案组件，可以包含在解决方案文件中，并导入到不同的环境中。它们可以添加到模型驱动应用和画布应用中。

## 三个核心要素

代码组件由三个要素组成：

1. **清单**
2. **组件实现**
3. **资源**

> **注意**: 使用 Power Apps 组件框架定义和实现代码组件的方式在模型驱动应用和画布应用中是相同的。唯一的区别在于配置部分。

## 清单

清单是 `ControlManifest.Input.xml` 元数据文件，用于定义组件。它是一个 XML 文档，描述以下内容：

- 组件的名称
- 可配置的数据类型，可以是 `字段` 或 `数据集`
- 在组件被添加到应用时可配置的属性
- 组件所需的资源文件列表

### 清单目的

当用户配置代码组件时，清单文件中的数据会过滤可用组件，以便仅显示与当前上下文相关的有效组件。清单文件中定义的属性会作为配置列呈现，使用户能够指定值。这些属性值随后在运行时可供组件使用。

更多信息：[清单架构参考](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/)

## 组件实现

代码组件使用 TypeScript 实现。每个代码组件必须包含一个实现代码组件接口中描述的方法的对象。使用 [Power Platform CLI](https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction) 的 `pac pcf init` 命令可自动生成一个带有占位符实现的 `index.ts` 文件。

### 必须实现的方法

组件对象实现以下生命周期方法：

- **init**（必需）- 页面加载时调用
- **updateView**（必需）- 应用数据更改时调用
- **getOutputs**（可选）- 当用户更改数据时返回值
- **destroy**（必需）- 页面关闭时调用

### 组件生命周期

#### 页面加载

当页面加载时，应用会使用清单中的数据创建一个对象：

```typescript
var obj = new <"清单中的命名空间">.<"清单中的构造函数">();
```

示例：
```typescript
var controlObj = new SampleNameSpace.LinearInputComponent();
```

页面随后初始化组件：

```typescript
controlObj.init(context, notifyOutputChanged, state, container);
```

**初始化参数：**

| 参数 | 描述 |
|------|------|
| `context` | 包含组件配置信息和所有参数。通过 `context.parameters.<清单中属性名称>` 访问输入属性。包含 Power Apps 组件框架 API。 |
| `notifyOutputChanged` | 在组件有新输出可供异步获取时通知框架。 |
| `state` | 包含使用 `setControlState` 方法显式存储的上一次页面加载的组件数据。 |
| `container` | 一个 HTML div 元素，开发者可以将其附加到 UI 的 HTML 元素上。 |

#### 用户更改数据

当用户与组件交互以更改数据时，调用 `init` 方法中传递的 `notifyOutputChanged` 方法。平台随后调用 `getOutputs` 方法，该方法返回用户更改后的值。对于 `字段` 组件，这通常是新的值。

#### 应用更改数据

如果平台更改了数据，它会调用组件的 `updateView` 方法，并将新的上下文对象作为参数传递。此方法应实现以更新组件中显示的值。

#### 页面关闭

当用户离开页面时，代码组件将失去作用域，所有分配给对象的内存都会被清除。然而，某些方法（如事件处理程序）可能会根据浏览器实现保留并占用内存。

**最佳实践：**
- 实现 `setControlState` 方法以在同一次会话中存储信息供下次使用
- 实现 `destroy` 方法以在页面关闭时移除清理代码（如事件处理程序）

## 资源

清单文件中的资源节点指向组件实现其可视化所需的资源。每个代码组件必须至少有一个资源文件来构建其可视化。工具生成的 `index.ts` 文件是一个 `代码` 资源。必须至少包含一个代码资源。

### 其他资源

您可以在清单中定义其他资源文件：

- CSS 文件
- 图像网络资源
- 用于本地化的 Resx 网络资源

更多信息：[resources 元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/resources)

## 相关资源

- [创建和构建代码组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/create-custom-controls-using-pcf)
- [学习如何使用解决方案打包和分发扩展](https://learn.microsoft.com/en-us/power-platform/alm/solution-concepts-alm)


---
description: '在 PCF 组件中定义和处理自定义事件'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj}'
---

# 定义事件（预览）

[此主题是预发布文档，可能会更改。]

在使用 Power Apps Component Framework 构建自定义组件时，一个常见的需求是能够响应控制内部生成的事件。这些事件可以由用户交互或通过代码编程方式触发。例如，应用程序可以包含一个代码组件，允许用户构建产品捆绑包。此组件还可以引发事件，以在应用程序的其他区域显示产品信息。

## 组件数据流

代码组件的常见数据流是数据从宿主应用程序流入控件作为输入，而更新后的数据则从控件流出到宿主表单或页面。此图展示了典型 PCF 组件的标准数据流模式：

![显示从代码组件到绑定字段的数据更新会触发 OnChange 事件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/component-events-onchange-example.png)

从代码组件到绑定字段的数据更新会触发 `OnChange` 事件。对于大多数组件场景，这已经足够，制作人员只需添加一个处理程序来触发后续操作。然而，更复杂的控件可能需要引发非字段更新的事件。事件机制允许代码组件定义具有独立事件处理程序的事件。

## 使用事件

PCF 中的事件机制基于 JavaScript 的标准事件模型。组件可以在清单文件中定义事件，并在代码中引发这些事件。宿主应用程序可以监听这些事件并作出响应。

### 在清单文件中定义事件

组件使用清单文件中的 [event 元素](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/event) 来定义事件。此数据允许相应的宿主应用程序以不同的方式响应事件。

```xml
<property
  name="sampleProperty"
  display-name-key="Property_Display_Key"
  description-key="Property_Desc_Key"
  of-type="SingleLine.Text"
  usage="bound"
  required="true"
/>
<event
  name="customEvent1"
  display-name-key="customEvent1"
  description-key="customEvent1"
/>
<event
  name="customEvent2"
  display-name-key="customEvent2"
  description-key="customEvent2"
/>
```

### 画布应用事件处理

画布应用通过 Power Fx 表达式响应事件：

![显示画布应用设计器中的自定义事件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/custom-events-in-canvas-designer.png)

### 模型驱动应用事件处理

模型驱动应用使用 [addEventHandler 方法](https://learn.microsoft.com/en-us/power-apps/developer/model-driven-apps/clientapi/reference/controls/addeventhandler) 将自定义事件的事件处理程序与组件关联。

```javascript
const controlName1 = "cr116_personid";

this.onLoad = function (executionContext) {
  const formContext = executionContext.getFormContext();

  const sampleControl1 = formContext.getControl(controlName1);
  sampleControl1.addEventHandler("customEvent1", this.onSampleControl1CustomEvent1);
  sampleControl1.addEventHandler("customEvent2", this.onSampleControl1CustomEvent2);
}
```

> **注意**：这些事件在应用程序中的每个代码组件实例上独立发生。

## 为模型驱动应用定义事件

对于模型驱动应用，您可以传递一个有效载荷与事件，从而允许更复杂的场景。例如，在下面的图中，组件在事件中传递一个回调函数，允许脚本处理程序回调到组件。

![在此示例中，组件在事件中传递一个回调函数，允许脚本处理程序回调到组件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/passing-payload-in-events.png)

```javascript
this.onSampleControl1CustomEvent1 = function (params) {
   //alert(`SampleControl1 Custom Event 1: ${params}`);
   alert(`SampleControl1 Custom Event 1`);
}.bind(this);

this.onSampleControl2CustomEvent2 = function (params) {
  alert(`SampleControl2 Custom Event 2: ${params.message}`);
  // 阻止事件的默认操作
  params.callBackFunction();
}
```

## 为画布应用定义事件

制作人员通过在 PCF 控件的属性面板中使用 Power Fx 配置事件。

## 调用事件

了解如何调用事件，请参阅 [事件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/events)。

## 下一步操作

[教程：在组件中定义自定义事件](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/tutorial-define-event)


---
description: 'PCF组件的完整清单架构参考，包含所有可用的XML元素'
applyTo: '**/*.xml'
---

# 清单架构参考

清单文件（`ControlManifest.Input.xml`）是一个元数据文档，用于定义您的代码组件。本参考文档列出了所有可用的清单元素及其用途。

## 根元素

### manifest

包含整个组件定义的根元素。

## 核心元素

### code

指代实现组件逻辑的资源文件。

**属性:**
- `path`: TypeScript/JavaScript实现文件的路径
- `order`: 加载顺序（通常为"1"）

**可用性:** 模型驱动应用、画布应用、门户

### control

定义组件本身，包括命名空间、版本和显示信息。

**关键属性:**
- `namespace`: 组件的命名空间
- `constructor`: 构造函数名称
- `version`: 语义版本（例如："1.0.0"）
- `display-name-key`: 显示名称的资源键
- `description-key`: 描述的资源键
- `control-type`: 控制类型（"standard" 或 "virtual"）

**可用性:** 模型驱动应用、画布应用、门户

## 属性元素

### property

定义组件的输入或输出属性。

**关键属性:**
- `name`: 属性名称
- `display-name-key`: 显示名称的资源键
- `description-key`: 描述的资源键
- `of-type`: 数据类型（例如："SingleLine.Text", "Whole.None", "TwoOptions", "DateAndTime.DateOnly"）
- `usage`: 属性用途（"bound" 或 "input"）
- `required`: 属性是否为必需（true/false）
- `of-type-group`: 对应的类型组引用
- `default-value`: 属性的默认值

**可用性:** 模型驱动应用、画布应用、门户

### type-group

定义属性可以接受的类型组。

**用途:** 允许属性接受多种数据类型

**可用性:** 模型驱动应用、画布应用、门户

## 数据集元素

### data-set

定义用于处理表格数据的数据集属性。

**关键属性:**
- `name`: 数据集名称
- `display-name-key`: 显示名称的资源键
- `description-key`: 描述的资源键

**可用性:** 模型驱动应用（画布应用有局限性）

## 资源元素

### resources

所有资源定义的容器（代码、CSS、图像、本地化）。

**可用性:** 模型驱动应用、画布应用、门户

### css

引用CSS样式表文件。

**属性:**
- `path`: CSS文件的路径
- `order`: 加载顺序

**可用性:** 模型驱动应用、画布应用、门户

### img

引用图像资源。

**属性:**
- `path`: 图像文件的路径

**可用性:** 模型驱动应用、画布应用、门户

### resx

引用用于本地化的资源文件。

**属性:**
- `path`: .resx文件的路径
- `version`: 版本号

**可用性:** 模型驱动应用、画布应用、门户

## 功能使用元素

### uses-feature

声明组件使用特定的平台功能。

**关键属性:**
- `name`: 功能名称（例如："Device.captureImage", "Device.getCurrentPosition", "Utility.lookupObjects", "WebAPI"）
- `required`: 功能是否为必需（true/false）

**常见功能:**
- Device.captureAudio
- Device.captureImage
- Device.captureVideo
- Device.getBarcodeValue
- Device.getCurrentPosition
- Device.pickFile
- Utility.lookupObjects
- WebAPI

**可用性:** 根据功能和平台有所不同

### feature-usage

功能声明的容器。

**可用性:** 模型驱动应用、画布应用

## 依赖元素

### dependency

声明组件所需的外部依赖。

**可用性:** 模型驱动应用、画布应用

### external-service-usage

声明组件使用的外部服务。

**关键属性:**
- `enabled`: 是否启用外部服务使用（true/false）

**可用性:** 模型驱动应用、画布应用

## 库元素

### platform-library

引用平台提供的库（例如：React、Fluent UI）。

**关键属性:**
- `name`: 库名称（例如："React", "Fluent"）
- `version`: 库版本

**可用性:** 模型驱动应用、画布应用

## 事件元素

### event

定义组件可以引发的自定义事件。

**关键属性:**
- `name`: 事件名称
- `display-name-key`: 显示名称的资源键
- `description-key`: 描述的资源键

**可用性:** 模型驱动应用、画布应用

## 操作元素

### platform-action

定义组件可以调用的平台操作。

**可用性:** 模型驱动应用

## 清单示例结构

```xml
<?xml version="1.0" encoding="utf-8" ?>
<manifest>
  <control namespace="SampleNamespace" 
           constructor="SampleControl" 
           version="1.0.0" 
           display-name-key="Sample_Display_Key" 
           description-key="Sample_Desc_Key" 
           control-type="standard">
    
    <!-- 属性 -->
    <property name="sampleProperty" 
              display-name-key="Property_Display_Key" 
              description-key="Property_Desc_Key" 
              of-type="SingleLine.Text" 
              usage="bound" 
              required="true" />
    
    <!-- 类型组示例 -->
    <type-group name="numbers">
      <type>Whole.None</type>
      <type>Currency</type>
      <type>FP</type>
      <type>Decimal</type>
    </type-group>
    
    <property name="numericProperty"
              display-name-key="Numeric_Display_Key"
              of-type-group="numbers"
              usage="bound" />
    
    <!-- 数据集示例 -->
    <data-set name="dataSetProperty" 
              display-name-key="Dataset_Display_Key">
    </data-set>
    
    <!-- 事件 -->
    <event name="onCustomEvent"
           display-name-key="Event_Display_Key"
           description-key="Event_Desc_Key" />
    
    <!-- 资源 -->
    <resources>
      <code path="index.ts" order="1" />
      <css path="css/SampleControl.css" order="1" />
      <img path="img/icon.png" />
      <resx path="strings/SampleControl.1033.resx" version="1.0.0" />
    </resources>
    
    <!-- 功能使用 -->
    <feature-usage>
      <uses-feature name="WebAPI" required="true" />
      <uses-feature name="Device.captureImage" required="false" />
    </feature-usage>
    
    <!-- 平台库 -->
    <platform-library name="React" version="16.8.6" />
    <platform-library name="Fluent" version="8.29.0" />
    
  </control>
</manifest>
```

## 清单验证

清单架构在构建过程中进行验证：
- 缺失必需元素会导致构建错误
- 无效的属性值会被标记
- 使用 `pac pcf` 命令验证清单结构

## 最佳实践

1. **语义版本控制**: 使用语义版本（主版本.次版本.补丁版本）来定义组件版本
2. **本地化键**: 始终使用资源键而不是硬编码字符串
3. **功能声明**: 声明组件使用的所有功能
4. **必需与可选**: 仅在确实需要时标记属性和功能为必需
5. **类型组**: 对于接受多种数字类型的属性使用类型组
6. **数据类型**: 选择最符合需求的特定数据类型
7. **CSS作用域**: 将CSS作用域限定以避免与宿主应用冲突
8. **资源组织**: 将资源分别组织在单独的文件夹中（css/、img/、strings/）

## 数据类型参考

属性的常见 `of-type` 值：

- **文本**: SingleLine.Text, Multiple, SingleLine.TextArea, SingleLine.Email, SingleLine.Phone, SingleLine.Url, SingleLine.Ticker
- **数字**: Whole.None, Currency, FP, Decimal
- **日期/时间**: DateAndTime.DateAndTime, DateAndTime.DateOnly
- **布尔值**: TwoOptions
- **查找**: Lookup.Simple
- **选项集**: OptionSet, MultiSelectOptionSet
- **其他**: Enum

## 平台可用性图例

- ✅ **模型驱动应用**: 完全支持
- ✅ **画布应用**: 支持（可能有局限性）
- ✅ **门户**: 在Power Pages中支持

大多数清单元素在所有平台上都可用，但某些功能（如特定的设备API或平台操作）可能是平台特定的。请始终在目标环境中进行测试。
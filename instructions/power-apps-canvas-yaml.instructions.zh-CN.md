

---
描述：基于 Microsoft Power Apps YAML 模式 v3.0 的 Power Apps 画布应用 YAML 结构全面指南。涵盖 Power Fx 公式、控件结构、数据类型以及源代码控制最佳实践。
applyTo: '**/*.{yaml,yml,md,pa.yaml}'
---

# Power Apps 画布应用 YAML 结构指南

## 概述
本文档提供了关于基于官方 Microsoft Power Apps YAML 模式（v3.0）和 Power Fx 文档的 Power Apps 画布应用 YAML 代码的全面指导。

**官方模式源**：https://raw.githubusercontent.com/microsoft/PowerApps-Tooling/refs/heads/master/schemas/pa-yaml/v3.0/pa.schema.yaml

## Power Fx 设计原则
Power Fx 是 Power Apps 画布应用中使用的公式语言。它遵循以下核心原则：

### 设计原则
- **简单**：使用 Excel 公式中熟悉的概念
- **Excel 一致性**：与 Excel 公式语法和行为保持一致
- **声明式**：描述你想要的内容，而不是如何实现
- **函数式**：避免副作用；大多数函数是纯函数
- **组合性**：通过组合更简单的函数构建复杂逻辑
- **强类型**：类型系统确保数据完整性
- **集成性**：在 Power Platform 中无缝工作

### 语言哲学
Power Fx 促进：
- 通过类似 Excel 的公式实现低代码开发
- 在依赖项更改时自动重新计算
- 通过编译时检查实现类型安全
- 使用函数式编程模式

## 根结构
每个 Power Apps YAML 文件遵循以下顶层结构：

```yaml
App:
  Properties:
    # 应用级属性和公式
    StartScreen: =Screen1

Screens:
  # 屏幕定义

ComponentDefinitions:
  # 自定义组件定义

DataSources:
  # 数据源配置

EditorState:
  # 编辑器元数据（屏幕顺序等）
```

## 1. 应用部分
`App` 部分定义了应用级属性和配置。

```yaml
App:
  Properties:
    StartScreen: =Screen1
    BackEnabled: =false
    # 其他应用属性和 Power Fx 公式
```

### 关键点：
- 包含应用范围内的设置
- 属性使用 Power Fx 公式（以 `=` 开头）
- `StartScreen` 属性通常会被指定

## 2. 屏幕部分
定义应用中的所有屏幕，作为无序映射。

```yaml
Screens:
  Screen1:
    Properties:
      # 屏幕属性
    Children:
      - Label1:
          Control: Label
          Properties:
            Text: ="Hello World"
            X: =10
            Y: =10
      - Button1:
          Control: Button
          Properties:
            Text: ="Click Me"
            X: =10
            Y: =100
```

### 屏幕结构：
- **Properties**：屏幕级属性和公式
- **Children**：屏幕上的控件数组（按 z 轴索引排序）

### 控件定义格式：
```yaml
ControlName:
  Control: ControlType      # 必填：控件类型标识符
  Properties:
    PropertyName: =PowerFxFormula
  # 可选属性：
  Group: GroupName          # 用于在 Studio 中组织控件
  Variant: VariantName      # 控件变体（影响默认属性）
  MetadataKey: Key          # 控件的元数据标识符
  Layout: LayoutName        # 布局配置
  IsLocked: true/false      # 控件是否在编辑器中锁定
  Children: []              # 用于容器控件（按 z 轴索引排序）
```

### 控件版本控制：
你可以使用 `@` 运算符指定控件版本：
```yaml
MyButton:
  Control: Button@2.1.0     # 特定版本
  Properties:
    Text: ="Click Me"

MyLabel:
  Control: Label            # 默认使用最新版本
  Properties:
    Text: ="Hello World"
```

## 3. 控件类型

### 标准控件
常见的第一方控件包括：
- **基础控件**：`Label`, `Button`, `TextInput`, `HTMLText`
- **输入控件**：`Slider`, `Toggle`, `Checkbox`, `Radio`, `Dropdown`, `Combobox`, `DatePicker`, `ListBox`
- **显示控件**：`Image`, `Icon`, `Video`, `Audio`, `PDF viewer`, `Barcode scanner`
- **布局控件**：`Container`, `Rectangle`, `Circle`, `Gallery`, `DataTable`, `Form`
- **图表控件**：`Column chart`, `Line chart`, `Pie chart`
- **高级控件**：`Timer`, `Camera`, `Microphone`, `Add picture`, `Import`, `Export`

### 容器和布局控件
对容器控件及其子控件需特别注意：
```yaml
MyContainer:
  Control: Container
  Properties:
    Width: =300
    Height: =200
    Fill: =RGBA(240, 240, 240, 1)
  Children:
    - Label1:
        Control: Label
        Properties:
          Text: =Parent.InputText
          X: =10         # 相对于容器
          Y: =10         # 相对于容器
    - Button1:
        Control: Button
        Properties:
          Text: ="Container Button"
          X: =10
          Y: =50
```

### 自定义组件
```yaml
MyCustomControl:
  Control: Component
  ComponentName: MyComponent
  Properties:
    X: =10
    Y: =10
    # 自定义组件属性
```

### 代码组件（PCF）
```yaml
MyPCFControl:
  Control: CodeComponent
  ComponentName: publisherprefix_namespace.classname
  Properties:
    X: =10
    Y: =10
```

## 4. 组件定义
定义可重用的自定义组件：

```yaml
ComponentDefinitions:
  MyComponent:
    DefinitionType: CanvasComponent
    Description: "一个可重用的组件"
    AllowCustomization: true
    AccessAppScope: false
    CustomProperties:
      InputText:
        PropertyKind: Input
        DataType: Text
        Description: "输入文本属性"
        Default: ="默认值"
      OutputValue:
        PropertyKind: Output
        DataType: Number
        Description: "输出数值"
    Properties:
      Fill: =RGBA(255, 255, 255, 1)
      Height: =100
      Width: =200
    Children:
      - Label1:
          Control: Label
          Properties:
            Text: =Parent.InputText
```

### 自定义属性类型：
- **输入**：从父控件接收值
- **输出**：向父控件发送值
- **输入函数**：由父控件调用的函数
- **输出函数**：组件中定义的函数
- **事件**：触发父控件的事件
- **动作**：具有副作用的函数

### 数据类型：
- `Text`, `Number`, `Boolean`
- `DateAndTime`, `Color`, `Currency`
- `Record`, `Table`, `Image`
- `VideoOrAudio`, `Screen`

## 5. 数据源
配置数据连接：

```yaml
DataSources:
  MyTable:
    Type: Table
    Parameters:
      TableLogicalName: account

  MyActions:
    Type: Actions
    ConnectorId: shared_office365users
    Parameters:
      # 其他连接器参数
```

### 数据源类型：
- **表**：Dataverse 表或其他表格数据
- **动作**：连接器动作和流程

## 6. 编辑器状态
维护编辑器的组织结构：

```yaml
EditorState:
  ScreensOrder:
    - Screen1
    - Screen2
    - Screen3
  ComponentDefinitionsOrder:
    - MyComponent
    - AnotherComponent
```

## Power Fx 公式指南

### 公式语法：
- 所有公式必须以 `=` 开头
- 不使用前缀的 `+` 或 `=` 符号（不同于 Excel）
- 文本字符串使用双引号：`="Hello World"`
- 属性引用：`ControlName.PropertyName`
- YAML 上下文中不支持注释

### 公式元素：
```yaml
# 字面值
Text: ="静态文本"
X: =42
Visible: =true

# 控件属性引用
Text: =TextInput1.Text
Visible: =Checkbox1.Value

# 函数调用
Text: =Upper(TextInput1.Text)
Items: =Sort(DataSource, Name)

# 复杂表达式
Text: =If(IsBlank(TextInput1.Text), "请输入文本", Upper(TextInput1.Text))
```

### 属性公式与行为公式：
```yaml
# 属性公式（计算值）
Properties:
  Text: =Concatenate("Hello ", User().FullName)
  Visible: =Toggle1.Value

# 行为公式（执行动作 - 使用分号分隔多个动作）
Properties:
  OnSelect: =Set(MyVar, true); Navigate(NextScreen); Notify("完成!")
```

### 高级公式模式：

#### **处理集合**：
```yaml
Properties:
  Items: =Filter(MyCollection, Status = "Active")
  OnSelect: =ClearCollect(MyCollection, DataSource)
  OnSelect: =Collect(MyCollection, {Name: "新项目", Status: "Active"})
```

#### **错误处理**：
```yaml
Properties:
  Text: =IfError(Value(TextInput1.Text), 0)
  OnSelect: =IfError(
    Patch(DataSource, ThisItem, {Field: Value}),
    Notify("更新记录出错", NotificationType.Error)
  )
```

#### **动态属性设置**：
```yaml
Properties:
  Fill: =ColorValue("#" & HexInput.Text)
  Height: =Parent.Height * (Slider1.Value / 100)
  X: =If(Alignment = "Center", (Parent.Width - Self.Width) / 2, 0)
```

## 公式最佳实践

### 公式组织：
- 将复杂公式拆分为更小、更易读的部分
- 使用变量存储中间计算结果
- 通过描述性控件名称对复杂逻辑进行注释
- 将相关计算分组

### 性能优化：
- 在处理大型数据集时使用委托友好的函数
- 避免在频繁更新的属性中使用嵌套公式调用
- 使用集合进行复杂数据转换
- 最小化对外部数据源的调用

## Power Fx 数据类型和操作

### 数据类型分类：

#### **原始类型**：
- **布尔型**：`=true`, `=false`
- **数字型**：`=123`, `=45.67`
- **文本型**：`="Hello World"`
- **日期型**：`=Date(2024, 12, 25)`
- **时间型**：`=Time(14, 30, 0)`
- **日期时间型**：`=Now()`

#### **复杂类型**：
- **颜色型**：`=Color.Red`, `=RGBA(255, 128, 0, 1)`
- **记录型**：`={Name: "John", Age: 30}`
- **表格型**：`=Table({Name: "John"}, {Name: "Jane"})`
- **GUID 型**：`=GUID()`

#### **类型转换**：
```yaml
Properties:
  Text: =Text(123.45, "#,##0.00")        # 数字转文本
  Text: =Value("123.45")                 # 文本转数字
  Text: =DateValue("12/25/2024")         # 文本转日期
  Visible: =Boolean("true")              # 文本转布尔
```

#### **类型检查**：
```yaml
Properties:
  Visible: =Not(IsBlank(OptionalField))
  Visible: =Not(IsError(Value(TextInput1.Text)))
  Visible: =IsNumeric(TextInput1.Text)
```

### 表操作：

#### **创建表格**：
```yaml
Properties:
  Items: =Table(
    {Name: "产品 A", Price: 10.99},
    {Name: "产品 B", Price: 15.99}
  )
  Items: =["选项 1", "选项 2", "选项 3"]  # 单列表格
```

#### **筛选和排序**：
```yaml
Properties:
  Items: =Filter(Products, Price > 10)
  Items: =Sort(Products, Name, Ascending)
  Items: =SortByColumns(Products, "Price", Descending, "Name", Ascending)
```

#### **数据转换**：
```yaml
Properties:
  Items: =AddColumns(Products, "Total", Price * Quantity)
  Items: =RenameColumns(Products, "Price", "Cost")
  Items: =ShowColumns(Products, "Name", "Price")
  Items: =DropColumns(Products, "InternalID")
```

#### **聚合**：
```yaml
Properties:
  Text: =Sum(Products, Price)
  Text: =Average(Products, Rating)
  Text: =Max(Products, Price)
  Text: =CountRows(Products)
```

## 变量和状态管理：

#### **全局变量**：
```yaml
Properties:
  OnSelect: =Set(MyGlobalVar, "Hello World")
  Text: =MyGlobalVar
```

#### **上下文变量**：
```yaml
Properties:
  OnSelect: =UpdateContext({LocalVar: "屏幕特定"})
  OnSelect: =Navigate(NextScreen, None, {PassedValue: 42})
```

#### **集合**：
```yaml
Properties:
  OnSelect: =Clear(TempCollection)
  OnSelect: =Collect(MyCollection, {Name: "新项目"})
  Items: =MyCollection
```

## Power Fx 增强连接器和外部数据

### 连接器集成：
```yaml
DataSources:
  SharePointList:
    Type: Table
    Parameters:
      TableLogicalName: "自定义列表"

  Office365Users:
    Type: Actions
    ConnectorId: shared_office365users
```

### 处理外部数据：
```yaml
Properties:
  Items: =Filter(SharePointList, Status = "Active")
  OnSelect: =Office365Users.SearchUser({searchTerm: SearchInput.Text})
```

### 委托注意事项：
```yaml
Properties:
  # 可委托操作（在服务器端执行）
  Items: =Filter(LargeTable, Status = "Active")    # 高效

  # 不可委托操作（可能下载所有记录）
  Items: =Filter(LargeTable, Len(Description) > 100)  # 会发出警告
```

## 故障排除和常见模式

### 常见错误模式：
```yaml
# 处理空值
Properties:
  Text: =If(IsBlank(OptionalText), "默认", OptionalText)

# 优雅处理错误
Properties:
  Text: =IfError(RiskyOperation(), "备用值")

# 验证输入
Properties:
  Visible: =And(
    Not(IsBlank(NameInput.Text)),
    IsNumeric(AgeInput.Text),
    IsMatch(EmailInput.Text, Email)
  )
```

### 性能优化：
```yaml
# 高效数据加载
Properties:
  Items: =Filter(LargeDataSource, Status = "Active")    # 服务器端筛选

# 使用可委托操作
Properties:
  Items: =Sort(Filter(DataSource, Active), Name)        # 可委托
  # 避免：Sort(DataSource, If(Active, Name, ""))       # 不可委托
```

### 内存管理：
```yaml
# 清除未使用的集合
Properties:
  OnSelect: =Clear(TempCollection)

# 限制数据检索
Properties:
  Items: =FirstN(Filter(DataSource, Status = "Active"), 50)
```

请记住：本指南全面覆盖了 Power Apps 画布应用 YAML 结构和 Power Fx 公式。始终将你的 YAML 验证到官方模式，并在 Power Apps Studio 环境中测试公式。


---
描述：'完整的 PCF API 参考，包含所有接口及其在模型驱动应用和画布应用中的可用性'
适用范围：'**/*.{ts,tsx,js}'
---

# Power Apps 组件框架 API 参考

Power Apps 组件框架提供了一套丰富的 API，使您能够创建强大的代码组件。本参考文档列出了所有可用的接口及其在不同应用类型中的可用性。

## API 可用性

下表展示了 Power Apps 组件框架中所有 API 接口及其在模型驱动应用和画布应用中的可用性。

| API | 模型驱动应用 | 画布应用 |
|-----|------------------|-------------|
| AttributeMetadata | 是 | 否 |
| Client | 是 | 是 |
| Column | 是 | 是 |
| ConditionExpression | 是 | 是 |
| Context | 是 | 是 |
| DataSet | 是 | 是 |
| Device | 是 | 是 |
| Entity | 是 | 是 |
| Events | 是 | 是 |
| Factory | 是 | 是 |
| Filtering | 是 | 是 |
| Formatting | 是 | 是 |
| ImageObject | 是 | 是 |
| Linking | 是 | 是 |
| Mode | 是 | 是 |
| Navigation | 是 | 是 |
| NumberFormattingInfo | 是 | 是 |
| Paging | 是 | 是 |
| Popup | 是 | 是 |
| PopupService | 是 | 是 |
| PropertyHelper | 是 | 是 |
| Resources | 是 | 是 |
| SortStatus | 是 | 是 |
| StandardControl | 是 | 是 |
| UserSettings | 是 | 是 |
| Utility | 是 | 是 |
| WebApi | 是 | 是 |

## 关键 API 命名空间

### 上下文 API 接口

`Context` 对象提供了对所有框架功能的访问，并传递给您的组件生命周期方法。它包含以下内容：

- **Client**：有关客户端的信息（设备类型、网络状态）
- **Device**：设备功能（相机、位置、麦克风）
- **Factory**：用于创建框架对象的工厂方法
- **Formatting**：数字和日期格式化
- **Mode**：组件模式和跟踪
- **Navigation**：导航方法
- **Resources**：访问资源（图片、字符串）
- **UserSettings**：用户设置（区域设置、数字格式、安全角色）
- **Utils**：实用方法（getEntityMetadata、hasEntityPrivilege、lookupObjects）
- **WebApi**：Dataverse Web API 方法

### 数据 API 接口

- **DataSet**：操作表格数据
- **Column**：访问列元数据和数据
- **Entity**：访问记录数据
- **Filtering**：定义数据过滤
- **Linking**：定义关系
- **Paging**：处理数据分页
- **SortStatus**：管理排序

### 用户界面 API 接口

- **Popup**：创建弹窗对话框
- **PopupService**：管理弹窗生命周期
- **Mode**：获取组件渲染模式

### 元数据 API 接口

- **AttributeMetadata**：列元数据（仅限模型驱动应用）
- **PropertyHelper**：属性元数据辅助工具

### 标准控件

- **StandardControl**：所有代码组件的基础接口，包含生命周期方法：
  - `init()`：初始化组件
  - `updateView()`：更新组件 UI
  - `destroy()`：清理资源
  - `getOutputs()`：返回输出值

## 使用指南

### 模型驱动应用与画布应用

由于平台差异，某些 API 仅在模型驱动应用中可用：

- **AttributeMetadata**：仅限模型驱动应用 - 提供详细的列元数据
- 其他大多数 API 在两种平台中均可用

### API 版本兼容性

- 始终检查目标平台（模型驱动或画布）的 API 可用性
- 某些 API 在不同平台中的行为可能不同
- 在目标环境中测试组件以确保兼容性

### 常见模式

1. **访问上下文 API 接口**
   ```typescript
   // 在 init 或 updateView 中
   const userLocale = context.userSettings.locale;
   const isOffline = context.client.isOffline();
   ```

2. **操作 DataSet**
   ```typescript
   // 访问数据集记录
   const records = context.parameters.dataset.records;
   
   // 获取排序列
   const sortedColumns = context.parameters.dataset.sorting;
   ```

3. **使用 WebApi**
   ```typescript
   // 获取记录
   context.webAPI.retrieveMultipleRecords("account", "?$select=name");
   
   // 创建记录
   context.webAPI.createRecord("contact", data);
   ```

4. **设备功能**
   ```typescript
   // 捕获图像
   context.device.captureImage();
   
   // 获取当前位置
   context.device.getCurrentPosition();
   ```

5. **格式化**
   ```typescript
   // 格式化日期
   context.formatting.formatDateLong(date);
   
   // 格式化数字
   context.formatting.formatDecimal(value);
   ```

## 最佳实践

1. **类型安全**：使用 TypeScript 进行类型检查和智能感知
2. **空值检查**：在访问 API 对象前始终检查其是否为 null/undefined
3. **错误处理**：将 API 调用包裹在 try-catch 块中
4. **平台检测**：通过 `context.client.getFormFactor()` 检测平台以适配行为
5. **API 可用性验证**：在使用前确认目标平台的 API 可用性
6. **性能优化**：在适当情况下缓存 API 结果以避免重复调用

## 其他资源

- 如需了解每个 API 的详细文档，请参考 [Power Apps 组件框架 API 参考](https://learn.microsoft.com/power-apps/developer/component-framework/reference/)
- 每个 API 的示例代码可在 [PowerApps-Samples 仓库](https://github.com/microsoft/PowerApps-Samples/tree/master/component-framework) 中找到
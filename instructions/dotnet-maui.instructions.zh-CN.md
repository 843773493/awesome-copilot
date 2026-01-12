

---
描述: '.NET MAUI 组件和应用程序模式'
适用范围: '**/*.xaml, **/*.cs'
---

# .NET MAUI

## .NET MAUI 代码风格和结构

- 编写符合规范且高效的 .NET MAUI 和 C# 代码。
- 遵循 .NET 和 .NET MAUI 的约定。
- 保持 UI（视图）专注于布局和绑定；将逻辑保留在视图模型和服务中。
- 使用 async/await 进行 I/O 操作和长时间运行的任务，以保持 UI 响应。

## 命名规范

- 遵循 PascalCase 命名规则为组件名称、方法名称和公共成员。
- 使用 camelCase 命名规则为私有字段和局部变量。
- 以 "I" 前缀命名接口（例如：IUserService）。

## .NET MAUI 和 .NET 特定指南

- 利用 .NET MAUI 内置的组件生命周期功能（例如 OnAppearing、OnDisappearing）。
- 使用 `{Binding}` 和 MVVM 模式有效进行数据绑定。
- 按照关注点分离原则构建 .NET MAUI 组件和服务。
- 使用仓库目标 .NET SDK 和设置支持的语言版本；除非项目已配置为使用，否则避免要求预览语言功能。

## 关键规则（一致性）

- 永远不要使用 ListView（已弃用）。使用 CollectionView。
- 永远不要使用 TableView（已弃用）。优先使用 CollectionView 或 Grid/VerticalStackLayout 等布局。
- 永远不要使用 Frame（已弃用）。使用 Border 替代。
- 永远不要使用 `*AndExpand` 布局选项（已弃用）。改用 Grid 和显式尺寸设置。
- 永远不要在 StackLayout/VerticalStackLayout/HorizontalStackLayout 内嵌入 ScrollView 或 CollectionView（可能导致滚动和虚拟化问题）。使用 Grid 作为父级布局。
- 永远不要在运行时引用 `.svg` 图像。使用 PNG/JPG 资源。
- 永远不要混合使用 Shell 导航与 NavigationPage/TabbedPage/FlyoutPage。
- 永远不要使用渲染器。使用处理程序。
- 永远不要设置 `BackgroundColor`；使用 `Background`（支持渐变/画刷，是现代 API 的首选）。

## 布局和控件选择

- 优先使用 `VerticalStackLayout`/`HorizontalStackLayout` 而不是 `StackLayout Orientation="..."`（性能更优）。
- 使用 `BindableLayout` 处理小型非滚动列表（≤20 项）。使用 `CollectionView` 处理较大或可滚动的列表。
- 对于复杂布局或需要细分空间的场景，优先使用 `Grid`。
- 对于带有边框/背景的容器，优先使用 `Border` 而不是 `Frame`。

## Shell 导航

- 使用 Shell 作为主要导航宿主。
- 通过 `Routing.RegisterRoute(...)` 注册路由，并使用 `Shell.Current.GoToAsync(...)` 进行导航。
- 在启动时设置 `MainPage` 一次；避免频繁更改。
- 不要在 Shell 内嵌套标签页。

## 错误处理和验证

- 为 .NET MAUI 页面和 API 调用实现适当的错误处理。
- 使用日志记录应用程序级别的错误；对可恢复的失败情况，记录并展示用户友好的消息。
- 在表单中使用 FluentValidation 或 DataAnnotations 实现验证。

## MAUI API 和性能优化

- 优先使用编译绑定以提高性能和正确性。
	- 在 XAML 中，为页面/视图/模板设置 `x:DataType`。
	- 尽可能使用基于表达式的绑定。
	- 考虑在项目设置中启用更严格的 XAML 编译（例如 `MauiStrictXamlCompilation=true`），尤其是在 CI 环境中。
- 避免深度布局嵌套（尤其是嵌套的 StackLayout）。优先使用 Grid 处理复杂布局。
- 保持绑定的意图性：
	- 当值不会改变时使用 `OneTime`。
	- 仅在可编辑值时使用 `TwoWay`。
	- 避免绑定静态常量；直接设置它们。
- 使用 `Dispatcher.Dispatch()` 或 `Dispatcher.DispatchAsync()` 从后台任务更新 UI：
	- 当拥有页面、视图或其他 BindableObject 的引用时，优先使用 `BindableObject.Dispatcher`。
	- 在服务或视图模型中，若无法直接访问 BindableObject，通过 DI 注入 `IDispatcher`。
	- 仅在没有 Dispatcher 可用时使用 `MainThread.BeginInvokeOnMainThread(...)` 作为后备方案。
	- **避免** 已弃用的 `Device.BeginInvokeOnMainThread` 模式。

## 资源和资产

- 将图像放置在 `Resources/Images/`，字体放置在 `Resources/Fonts/`，原始资产放置在 `Resources/Raw/`。
- 以 PNG/JPG 格式引用图像（例如 `<Image Source="logo.png" />`），而不是 `.svg`。
- 使用适当尺寸的图像以避免内存膨胀。

## 状态管理

- 优先使用依赖注入管理的服务处理共享状态和横切关注点；将视图模型的作用域限制在导航/页面生命周期内。

## API 设计和集成

- 使用 HttpClient 或其他适当的服务与外部 API 或自有后端进行通信。
- 使用 try-catch 实现 API 调用的错误处理，并在 UI 中提供适当的用户反馈。

## 存储和机密信息

- 使用 `SecureStorage` 存储机密信息（如令牌、刷新令牌），并通过清除/重置和重新认证处理异常（如不支持的设备、键更改、损坏）。
- 避免将机密信息存储在 Preferences 中。

## 测试和调试

- 使用 xUnit、NUnit 或 MSTest 测试组件和服务。
- 在测试中使用 Moq 或 NSubstitute 对依赖项进行模拟。

## 安全性和身份验证

- 在需要的地方使用 OAuth 或 JWT 令牌实现 MAUI 应用的身份验证和授权。
- 使用 HTTPS 进行所有网络通信，并确保实施正确的 CORS 策略。

## 常见陷阱

- 频繁更改 MainPage 可能导致导航问题。
- 父视图和子视图上同时使用手势识别器可能导致冲突；在需要的地方设置 `InputTransparent = true`。
- 未取消订阅的事件可能导致内存泄漏；始终取消订阅并释放资源。
- 深度嵌套的布局会影响性能；尽量扁平化视觉层次结构。
- 仅在模拟器上测试会遗漏真实设备的边缘情况；应在物理设备上进行测试。
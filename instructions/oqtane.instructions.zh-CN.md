

---
description: 'Oqtane 模块模式'
applyTo: '**/*.razor, **/*.razor.cs, **/*.razor.css'
---

## Blazor 代码风格和结构

- 编写符合规范且高效的 Blazor 和 C# 代码。
- 遵循 .NET 和 Blazor 的约定。
- 在基于组件的 UI 开发中适当使用 Razor 组件。
- 在基于组件的 UI 开发中适当使用 Blazor 组件。
- 对于小型组件，优先使用内联函数，但将复杂逻辑分离到代码后端或服务类中。
- 在适用的情况下使用 async/await 来确保非阻塞的 UI 操作。

## 命名约定

- 组件名称、方法名称和公共成员使用 PascalCase。
- 私有字段和局部变量使用 camelCase。
- 接口名称前缀使用 "I"（例如：IUserService）。

## Blazor 和 .NET 特定指南

- 利用 Blazor 内置的组件生命周期功能（例如：OnInitializedAsync、OnParametersSetAsync）。
- 有效使用 @bind 进行数据绑定。
- 在 Blazor 中使用依赖注入来管理服务。
- 按职责分离原则结构化 Blazor 组件和服务。
- 始终使用最新版本的 C#，目前包括 C# 13 的特性如记录类型、模式匹配和全局 using。

## Oqtane 特定指南

- 查看 [主 Oqtane 仓库](https://github.com/oqtane/oqtane.framework) 中的基础类和模式。
- 按照客户端-服务器模式进行模块开发。
- 客户端项目在 modules 文件夹中包含多个模块。
- 每个客户端模块中的操作都是独立的 Razor 文件，继承自 ModuleBase，其中 index.razor 是默认操作。
- 对于复杂的客户端处理（如获取数据），创建一个继承自 ServiceBase 的服务类，并将其放在 services 文件夹中。每个模块对应一个服务类。
- 客户端服务应使用 ServiceBase 方法调用服务器端点。
- 服务器项目包含 MVC 控制器，每个控制器对应一个模块，与客户端服务调用相匹配。每个控制器将调用由 DI 管理的服务器端服务或存储库。
- 服务器项目使用存储库模式进行模块开发，每个模块对应一个存储库类以匹配控制器。

## 错误处理和验证

- 为 Blazor 页面和 API 调用实现适当的错误处理。
- 使用 Oqtane 基础类中的内置日志记录方法。
- 在后端使用日志记录进行错误跟踪，并考虑在 Blazor 中使用如 ErrorBoundary 等工具捕获 UI 层的错误。
- 在表单中使用 FluentValidation 或 DataAnnotations 实现验证。

## Blazor API 和性能优化

- 根据项目需求优化使用 Blazor 服务器端或 WebAssembly。
- 对可能阻塞主线程的 API 调用或 UI 操作使用异步方法（async/await）。
- 通过减少不必要的渲染和高效使用 StateHasChanged() 来优化 Razor 组件。
- 通过避免不必要的重新渲染来最小化组件渲染树，必要时使用 ShouldRender()。
- 使用 EventCallbacks 高效处理用户交互，触发事件时仅传递最小数据。

## 缓存策略

- 对于频繁使用的数据，实施内存缓存，尤其是在 Blazor 服务器应用中。使用 IMemoryCache 来实现轻量级缓存方案。
- 对于 Blazor WebAssembly，利用 localStorage 或 sessionStorage 缓存应用状态以在用户会话之间保持数据。
- 对于需要跨多个用户或客户端共享状态的大型应用，考虑分布式缓存策略（如 Redis 或 SQL Server 缓存）。
- 缓存 API 调用，存储响应以避免在数据不太可能变化时重复调用，从而提升用户体验。

## 状态管理库

- 使用 Blazor 内置的级联参数和事件回调进行组件间的基本状态共享。
- 在适当情况下使用 Oqtane 基础类中的内置状态管理，如 PageState 和 SiteState。
- 在应用复杂度增加时，避免添加额外的依赖项如 Fluxor 或 BlazorState。
- 对于 Blazor WebAssembly 的客户端状态持久化，考虑使用 Blazored.LocalStorage 或 Blazored.SessionStorage 来在页面重新加载之间保持状态。
- 对于服务器端 Blazor，使用作用域服务和 StateContainer 模式来管理用户会话中的状态，同时减少重新渲染。

## API 设计和集成

- 使用服务基类方法与外部 API 或服务器项目后端进行通信。
- 使用 try-catch 处理 API 调用中的错误，并在 UI 中提供适当的用户反馈。

## 在 Visual Studio 中的测试和调试

- 所有单元测试和集成测试应在 Visual Studio Enterprise 中进行。
- 使用 xUnit、NUnit 或 MSTest 测试 Blazor 组件和服务。
- 使用 Moq 或 NSubstitute 在测试中模拟依赖项。
- 使用浏览器开发者工具和 Visual Studio 的调试工具调试 Blazor UI 问题以及后端和服务器端问题。
- 对于性能分析和优化，依赖于 Visual Studio 的诊断工具。

## 安全性和身份验证

- 使用 Oqtane 基础类成员（如 User.Roles）实现身份验证和授权。
- 所有网络通信使用 HTTPS，并确保实施正确的 CORS 策略。
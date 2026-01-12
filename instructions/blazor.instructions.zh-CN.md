

---
description: 'Blazor 组件和应用程序模式'
applyTo: '**/*.razor, **/*.razor.cs, **/*.razor.css'
---

## Blazor 代码风格和结构

- 编写符合 Blazor 和 C# 语法规则且高效的代码。
- 遵循 .NET 和 Blazor 的规范。
- 在基于组件的 UI 开发中适当使用 Razor 组件。
- 对于小型组件，优先使用内联函数，但将复杂逻辑分离到代码后端或服务类中。
- 在适用的情况下使用 Async/await 以确保非阻塞的 UI 操作。

## 命名规范

- 对于组件名称、方法名称和公共成员，遵循 PascalCase 命名规范。
- 对于私有字段和局部变量，使用 camelCase 命名规范。
- 接口名称以 "I" 前缀（例如：IUserService）。

## Blazor 和 .NET 特定指南

- 利用 Blazor 内置的组件生命周期功能（例如：OnInitializedAsync、OnParametersSetAsync）。
- 使用 @bind 实现高效的数据绑定。
- 在 Blazor 中利用依赖注入来管理服务。
- 根据关注点分离原则来组织 Blazor 组件和服务。
- 始终使用最新版本的 C#，目前包括 C# 13 特性，如记录类型、模式匹配和全局 using 语句。

## 错误处理和验证

- 为 Blazor 页面和 API 调用实现适当的错误处理。
- 在后端使用日志记录错误跟踪，并考虑使用 ErrorBoundary 等工具捕获 Blazor 的 UI 层错误。
- 在表单中使用 FluentValidation 或 DataAnnotations 实现验证。

## Blazor API 和性能优化

- 根据项目需求，优化使用 Blazor 服务器端或 WebAssembly。
- 对于可能阻塞主线程的 API 调用或 UI 操作，使用异步方法（async/await）。
- 通过减少不必要的渲染并高效使用 StateHasChanged() 来优化 Razor 组件。
- 通过避免不必要的重新渲染来最小化组件渲染树，适当使用 ShouldRender()。
- 使用 EventCallbacks 高效处理用户交互，并在触发事件时仅传递必要数据。

## 缓存策略

- 对于频繁使用的数据，尤其是 Blazor 服务器应用，实现内存缓存。使用 IMemoryCache 来处理轻量级缓存方案。
- 对于 Blazor WebAssembly，使用 localStorage 或 sessionStorage 在用户会话之间缓存应用程序状态。
- 对于需要在多个用户或客户端之间共享状态的大型应用程序，考虑使用分布式缓存策略（如 Redis 或 SQL Server 缓存）。
- 通过存储响应来缓存 API 调用，以避免在数据不太可能变化时重复调用，从而提升用户体验。

## 状态管理库

- 使用 Blazor 内置的 Cascading Parameters 和 EventCallbacks 实现组件间的简单状态共享。
- 当应用程序复杂度增加时，使用 Fluxor 或 BlazorState 等库实现高级状态管理方案。
- 对于 Blazor WebAssembly 的客户端状态持久化，考虑使用 Blazored.LocalStorage 或 Blazored.SessionStorage 来在页面重新加载之间保持状态。
- 对于服务器端 Blazor，使用作用域服务和 StateContainer 模式来管理用户会话中的状态，同时减少重新渲染。

## API 设计和集成

- 使用 HttpClient 或其他适当的服务与外部 API 或自有后端进行通信。
- 使用 try-catch 实现 API 调用的错误处理，并在 UI 中提供适当的用户反馈。

## 在 Visual Studio 中的测试和调试

- 所有单元测试和集成测试应在 Visual Studio Enterprise 中进行。
- 使用 xUnit、NUnit 或 MSTest 测试 Blazor 组件和服务。
- 在测试期间使用 Moq 或 NSubstitute 来模拟依赖项。
- 使用浏览器开发者工具和 Visual Studio 的调试工具来调试 Blazor UI 问题以及后端和服务器端问题。
- 对于性能分析和优化，依赖 Visual Studio 的诊断工具。

## 安全性和认证

- 在需要的地方使用 ASP.NET Identity 或 JWT 令牌实现 Blazor 应用的认证和授权。
- 所有网络通信使用 HTTPS，并确保正确实施 CORS 策略。

## API 文档和 Swagger

- 使用 Swagger/OpenAPI 为您的后端 API 服务生成 API 文档。
- 确保模型和 API 方法的 XML 文档以增强 Swagger 文档。
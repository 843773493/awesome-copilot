

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems']
description: '获取 C# 异步编程的最佳实践'
---

# C# 异步编程最佳实践

你的目标是帮助我遵循 C# 中异步编程的最佳实践。

## 命名规范

- 所有异步方法都应使用 'Async' 后缀
- 在适用情况下，异步方法名应与其同步版本对应（例如：`GetDataAsync()` 对应 `GetData()`）

## 返回类型

- 方法返回值时使用 `Task<T>`
- 方法不返回值时使用 `Task`
- 在高性能场景中考虑使用 `ValueTask<T>` 以减少内存分配
- 除非是事件处理程序，否则避免异步方法返回 `void`

## 异常处理

- 在 `await` 表达式周围使用 try/catch 块
- 避免在异步方法中捕获并忽略异常
- 在适当情况下使用 `ConfigureAwait(false)` 以防止库代码中的死锁
- 使用 `Task.FromException()` 传播异常，而非在异步 Task 返回方法中直接抛出

## 性能优化

- 使用 `Task.WhenAll()` 并行执行多个任务
- 使用 `Task.WhenAny()` 实现超时或获取首个完成的任务
- 避免在仅传递任务结果时使用不必要的 async/await
- 考虑使用取消令牌（cancellation tokens）处理长时间运行的操作

## 常见陷阱

- 绝对不要在异步代码中使用 `.Wait()`、`.Result` 或 `.GetAwaiter().GetResult()`
- 避免混合使用阻塞和异步代码
- 不要创建 async void 方法（事件处理程序除外）
- 始终等待 Task 返回的方法

## 实现模式

- 为长时间运行的操作实现异步命令模式
- 使用异步流（IAsyncEnumerable<T>）异步处理序列
- 考虑基于任务的异步模式（TAP）用于公共 API

在审查我的 C# 代码时，请识别这些问题并提出符合这些最佳实践的改进建议。
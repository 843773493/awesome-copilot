

---
agent: 'agent'
description: '确保 .NET/C# 代码符合该解决方案/项目的最佳实践。'
---
# .NET/C# 最佳实践

您的任务是确保 ${selection} 中的 .NET/C# 代码符合该解决方案/项目的特定最佳实践。这包括：

## 文档与结构

- 为所有公共类、接口、方法和属性创建全面的 XML 文档注释
- 在 XML 注释中包含参数描述和返回值描述
- 遵循已建立的命名空间结构：{Core|Console|App|Service}.{Feature}

## 设计模式与架构

- 使用主构造函数语法进行依赖注入（例如：`public class MyClass(IDependency dependency)`）
- 使用泛型基类实现命令处理模式（例如：`CommandHandler<TOptions>`）
- 通过清晰的命名约定实现接口隔离（以 'I' 前缀命名接口）
- 使用工厂模式进行复杂对象的创建

## 依赖注入与服务

- 使用构造函数依赖注入并通过 ArgumentNullException 进行空值检查
- 为服务注册适当的生命周期（单例、作用域、瞬态）
- 使用 Microsoft.Extensions.DependencyInjection 模式
- 为服务实现接口以支持可测试性

## 资源管理与本地化

- 使用 ResourceManager 管理本地化消息和错误字符串
- 将 LogMessages 和 ErrorMessages 分离为不同的资源文件
- 通过 `_resourceManager.GetString("MessageKey")` 访问资源

## 异步/等待模式

- 使用 async/await 处理所有 I/O 操作和长时间运行的任务
- 从异步方法返回 Task 或 Task<T>
- 在适当的位置使用 ConfigureAwait(false)
- 正确处理异步异常

## 测试标准

- 使用 MSTest 框架并结合 FluentAssertions 进行断言
- 遵循 AAA 模式（Arrange, Act, Assert）
- 使用 Moq 模拟依赖项
- 测试成功和失败场景
- 包含空参数验证测试

## 配置与设置

- 使用带有数据注释的强类型配置类
- 实现验证属性（Required, NotEmptyOrWhitespace）
- 使用 IConfiguration 绑定进行设置管理
- 支持 appsettings.json 配置文件

## 语义内核与 AI 集成

- 使用 Microsoft.SemanticKernel 进行 AI 操作
- 实现适当的内核配置和服务注册
- 处理 AI 模型设置（如 ChatCompletion、Embedding 等）
- 使用结构化输出模式以确保 AI 响应的可靠性

## 错误处理与日志记录

- 使用 Microsoft.Extensions.Logging 实现结构化日志记录
- 包含带有有意义上下文的范围日志
- 抛出具有描述性信息的特定异常
- 使用 try-catch 块处理预期的失败场景

## 性能与安全性

- 在适用时使用 C# 12+ 特性和 .NET 8 优化
- 实现适当的输入验证和清理
- 使用参数化查询进行数据库操作
- 遵循安全编码实践进行 AI/ML 操作

## 代码质量

- 确保符合 SOLID 原则
- 通过基类和实用工具避免代码重复
- 使用反映领域概念的有意义名称
- 保持方法专注且内聚
- 实现适当的资源处置模式
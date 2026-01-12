

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems', 'search']
description: '获取XUnit单元测试的最佳实践，包括数据驱动测试'
---

# XUnit最佳实践

您的目标是帮助我编写高效的XUnit单元测试，涵盖标准测试和数据驱动测试方法。

## 项目设置

- 使用独立的测试项目，命名遵循 `[ProjectName].Tests` 的规范
- 引用 Microsoft.NET.Test.Sdk、xunit 和 xunit.runner.visualstudio 包
- 创建与被测试类对应的测试类（例如：`CalculatorTests` 对应 `Calculator`）
- 使用 .NET SDK 测试命令：使用 `dotnet test` 运行测试

## 测试结构

- 不需要测试类属性（与 MSTest/NUnit 不同）
- 使用 `[Fact]` 属性进行基于事实的简单测试
- 遵循 Arrange-Act-Assert（AAA）模式
- 使用 `MethodName_Scenario_ExpectedBehavior` 模式命名测试
- 使用构造函数进行设置，使用 `IDisposable.Dispose()` 进行清理
- 使用 `IClassFixture<T>` 在同一类中的测试之间共享上下文
- 使用 `ICollectionFixture<T>` 在多个测试类之间共享上下文

## 标准测试

- 保持测试专注于单一行为
- 避免在一个测试方法中测试多个行为
- 使用清晰的断言来表达意图
- 仅包含验证测试用例所需的断言
- 使测试独立且幂等（可按任意顺序运行）
- 避免测试之间的依赖关系

## 数据驱动测试

- 使用 `[Theory]` 结合数据源属性
- 使用 `[InlineData]` 提供内联测试数据
- 使用 `[MemberData]` 提供基于方法的测试数据
- 使用 `[ClassData]` 提供基于类的测试数据
- 通过实现 `DataAttribute` 创建自定义数据属性
- 在数据驱动测试中使用有意义的参数名称

## 断言

- 使用 `Assert.Equal` 进行值相等性验证
- 使用 `Assert.Same` 进行引用相等性验证
- 使用 `Assert.True`/`Assert.False` 验证布尔条件
- 使用 `Assert.Contains`/`Assert.DoesNotContain` 验证集合
- 使用 `Assert.Matches`/`Assert.DoesNotMatch` 进行正则表达式模式匹配
- 使用 `Assert.Throws<T>` 或 `await Assert.ThrowsAsync<T>` 验证异常
- 使用流畅断言库进行更易读的断言

## 模拟与隔离

- 考虑结合使用 Moq 或 NSubstitute 与 XUnit
- 模拟依赖项以隔离被测试单元
- 使用接口来促进模拟操作
- 对于复杂的测试设置，考虑使用依赖注入容器

## 测试组织

- 按功能或组件分组测试
- 使用 `[Trait("Category", "CategoryName")]` 进行分类
- 使用集合固定装置将具有共享依赖项的测试分组
- 考虑使用输出辅助工具 (`ITestOutputHelper`) 进行测试诊断
- 在事实/理论属性中使用 `Skip = "原因"` 条件性跳过测试
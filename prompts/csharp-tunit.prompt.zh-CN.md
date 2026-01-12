

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems', 'search']
description: '获取 TUnit 单元测试的最佳实践，包括数据驱动测试'
---

# TUnit 最佳实践

你的目标是帮助我编写有效的单元测试，涵盖标准测试和数据驱动测试方法。

## 项目设置

- 使用独立的测试项目，命名遵循 `[ProjectName].Tests` 的规范
- 引用 TUnit 包和 TUnit.Assertions 以使用流畅断言
- 创建与被测试类同名的测试类（例如：`CalculatorTests` 对应 `Calculator`）
- 使用 .NET SDK 测试命令：`dotnet test` 来运行测试
- TUnit 要求 .NET 8.0 或更高版本

## 测试结构

- 不需要测试类属性（如 xUnit/NUnit）
- 使用 `[Test]` 属性标记测试方法（不同于 xUnit 的 `[Fact]`）
- 遵循 Arrange-Act-Assert（AAA）模式
- 使用 `MethodName_Scenario_ExpectedBehavior` 模式命名测试
- 使用生命周期钩子：`[Before(Test)]` 用于设置，`[After(Test)]` 用于清理
- 使用 `[Before(Class)]` 和 `[After(Class)]` 用于同一类中测试的共享上下文
- 使用 `[Before(Assembly)]` 和 `[After(Assembly)]` 用于不同测试类之间的共享上下文
- TUnit 支持高级生命周期钩子，如 `[Before(TestSession)]` 和 `[After(TestSession)]`

## 标准测试

- 保持测试专注于单一行为
- 避免在一个测试方法中测试多个行为
- 使用 TUnit 的流畅断言语法 `await Assert.That()`
- 仅包含验证测试用例所需的断言
- 确保测试独立且幂等（可以按任意顺序运行）
- 避免测试相互依赖（如需，使用 `[DependsOn]` 属性）

## 数据驱动测试

- 使用 `[Arguments]` 属性用于内联测试数据（等同于 xUnit 的 `[InlineData]`）
- 使用 `[MethodData]` 用于基于方法的测试数据（等同于 xUnit 的 `[MemberData]`）
- 使用 `[ClassData]` 用于基于类的测试数据
- 通过实现 `ITestDataSource` 创建自定义数据源
- 在数据驱动测试中使用有意义的参数名称
- 可以在同一个测试方法上应用多个 `[Arguments]` 属性

## 断言

- 使用 `await Assert.That(value).IsEqualTo(expected)` 来验证值相等性
- 使用 `await Assert.That(value).IsSameReferenceAs(expected)` 来验证引用相等性
- 使用 `await Assert.That(value).IsTrue()` 或 `await Assert.That(value).IsFalse()` 来验证布尔条件
- 使用 `await Assert.That(collection).Contains(item)` 或 `await Assert.That(collection).DoesNotContain(item)` 来验证集合
- 使用 `await Assert.That(value).Matches(pattern)` 进行正则表达式模式匹配
- 使用 `await Assert.That(action).Throws<TException>()` 或 `await Assert.That(asyncAction).ThrowsAsync<TException>()` 来测试异常
- 使用 `.And` 运算符链式断言：`await Assert.That(value).IsNotNull().And.IsEqualTo(expected)`
- 使用 `.Or` 运算符表示替代条件：`await Assert.That(value).IsEqualTo(1).Or.IsEqualTo(2)`
- 使用 `.Within(tolerance)` 进行带容差的 DateTime 和数值比较
- 所有断言均为异步操作，必须使用 `await` 等待结果

## 高级功能

- 使用 `[Repeat(n)]` 重复执行测试多次
- 使用 `[Retry(n)]` 在失败时自动重试
- 使用 `[ParallelLimit<T>]` 控制并行执行的限制
- 使用 `[Skip("reason")]` 条件性地跳过测试
- 使用 `[DependsOn(nameof(OtherTest))]` 创建测试依赖关系
- 使用 `[Timeout(milliseconds)]` 设置测试超时时间
- 通过继承 TUnit 的基础属性来创建自定义属性

## 测试组织

- 按功能或组件分组测试
- 使用 `[Category("CategoryName")]` 进行测试分类
- 使用 `[DisplayName("Custom Test Name")]` 设置自定义测试名称
- 考虑使用 `TestContext` 获取测试诊断信息
- 使用条件属性如自定义 `[WindowsOnly]` 进行平台特定测试

## 性能与并行执行

- TUnit 默认并行运行测试（不同于 xUnit 需要显式配置）
- 使用 `[NotInParallel]` 禁用特定测试的并行执行
- 使用 `[ParallelLimit<T>]` 配合自定义限制类控制并发
- 同一类中的测试默认按顺序执行
- 使用 `[Repeat(n)]` 与 `[ParallelLimit<T>]` 进行负载测试场景

## 从 xUnit 迁移

- 将 `[Fact]` 替换为 `[Test]`
- 将 `[Theory]` 替换为 `[Test]`，并使用 `[Arguments]` 提供数据
- 将 `[InlineData]` 替换为 `[Arguments]`
- 将 `[MemberData]` 替换为 `[MethodData]`
- 将 `Assert.Equal` 替换为 `await Assert.That(actual).IsEqualTo(expected)`
- 将 `Assert.True` 替换为 `await Assert.That(condition).IsTrue()`
- 将 `Assert.Throws<T>` 替换为 `await Assert.That(action).Throws<T>()`
- 将构造函数/IDisposable 替换为 `[Before(Test)]`/`[After(Test)]`
- 将 `IClassFixture<T>` 替换为 `[Before(Class)]`/`[After(Class)]`

**为什么选择 TUnit 而不是 xUnit？**

TUnit 提供了现代、快速且灵活的测试体验，具备 xUnit 缺乏的高级功能，如异步断言、更精细的生命周期钩子以及改进的数据驱动测试能力。TUnit 的流畅断言提供了更清晰、更表达力强的测试验证方式，特别适合复杂 .NET 项目。
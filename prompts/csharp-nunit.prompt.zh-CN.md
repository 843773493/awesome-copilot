

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems', 'search']
description: '获取 NUnit 单元测试的最佳实践，包括数据驱动测试'
---

# NUnit 最佳实践

您的目标是帮助我编写高效的 NUnit 单元测试，涵盖标准测试和数据驱动测试方法。

## 项目设置

- 使用独立的测试项目，命名遵循 `[ProjectName].Tests` 规范
- 引用 Microsoft.NET.Test.Sdk、NUnit 和 NUnit3TestAdapter 包
- 创建与被测试类同名的测试类（例如：`CalculatorTests` 用于 `Calculator`）
- 使用 .NET SDK 测试命令：`dotnet test` 用于运行测试

## 测试结构

- 使用 `[TestFixture]` 属性标记测试类
- 使用 `[Test]` 属性标记测试方法
- 遵循 Arrange-Act-Assert (AAA) 模式
- 使用 `MethodName_Scenario_ExpectedBehavior` 模式命名测试
- 使用 `[SetUp]` 和 `[TearDown]` 实现每项测试的设置和清理
- 使用 `[OneTimeSetUp]` 和 `[OneTimeTearDown]` 实现每类测试的设置和清理
- 使用 `[SetUpFixture]` 实现程序集级别的设置和清理

## 标准测试

- 保持测试聚焦于单一行为
- 避免在一个测试方法中测试多个行为
- 使用清晰的断言表达测试意图
- 仅包含验证测试用例所需的断言
- 确保测试用例独立且可重复运行（可按任意顺序执行）
- 避免测试用例之间的依赖关系

## 数据驱动测试

- 使用 `[TestCase]` 用于内联测试数据
- 使用 `[TestCaseSource]` 用于程序生成的测试数据
- 使用 `[Values]` 用于简单参数组合
- 使用 `[ValueSource]` 用于基于属性或方法的测试数据源
- 使用 `[Random]` 用于随机数值测试
- 使用 `[Range]` 用于连续数值测试
- 使用 `[Combinatorial]` 或 `[Pairwise]` 用于组合多个参数

## 断言

- 使用 `Assert.That` 并结合约束模型（推荐的 NUnit 风格）
- 使用约束如 `Is.EqualTo`、`Is.SameAs`、`Contains.Item`
- 使用 `Assert.AreEqual` 进行简单值相等性验证（经典风格）
- 使用 `CollectionAssert` 进行集合比较
- 使用 `StringAssert` 进行字符串特定断言
- 使用 `Assert.Throws<T>` 或 `Assert.ThrowsAsync<T>` 验证异常
- 在断言中使用描述性消息以明确失败原因

## 模拟与隔离

- 考虑结合 NUnit 使用 Moq 或 NSubstitute
- 模拟依赖项以隔离被测试单元
- 使用接口来便于模拟
- 考虑使用依赖注入容器进行复杂测试设置

## 测试组织

- 按功能或组件分组测试
- 使用 `[Category("分类名称")]` 指定分类
- 必要时使用 `[Order]` 控制测试执行顺序
- 使用 `[Author("开发者名称")]` 标记测试所有者
- 使用 `[Description]` 提供额外的测试信息
- 考虑使用 `[Explicit]` 标记不应自动运行的测试
- 使用 `[Ignore("原因")]` 暂时跳过测试
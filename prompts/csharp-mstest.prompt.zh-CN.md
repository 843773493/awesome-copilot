

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems', 'search']
description: '获取MSTest单元测试的最佳实践，包括数据驱动测试'
---

# MSTest最佳实践

您的目标是帮助我使用MSTest编写有效的单元测试，涵盖标准测试和数据驱动测试方法。

## 项目设置

- 使用独立的测试项目，命名规范为`[ProjectName].Tests`
- 引用MSTest包
- 创建与被测试类对应的测试类（例如，为`Calculator`创建`CalculatorTests`）
- 使用.NET SDK测试命令：`dotnet test`用于运行测试

## 测试结构

- 使用`[TestClass]`属性定义测试类
- 使用`[TestMethod]`属性定义测试方法
- 遵循准备-执行-断言（AAA）模式
- 使用`MethodName_Scenario_ExpectedBehavior`的命名模式为测试命名
- 使用`[TestInitialize]`和`[TestCleanup]`进行单个测试的设置和清理
- 使用`[ClassInitialize]`和`[ClassCleanup]`进行类级别的设置和清理
- 使用`[AssemblyInitialize]`和`[AssemblyCleanup]`进行程序集级别的设置和清理

## 标准测试

- 确保每个测试专注于单一行为
- 避免在一个测试方法中测试多个行为
- 使用清晰的断言来表达意图
- 仅包含验证测试用例所需的断言
- 使测试独立且幂等（可以按任意顺序运行）
- 避免测试之间的依赖关系

## 数据驱动测试

- 使用`[TestMethod]`结合数据源属性
- 使用`[DataRow]`用于内联测试数据
- 使用`[DynamicData]`用于程序生成的测试数据
- 使用`[TestProperty]`为测试添加元数据
- 在数据驱动测试中使用有意义的参数名称

## 断言

- 使用`Assert.AreEqual`进行值相等性验证
- 使用`Assert.AreSame`进行引用相等性验证
- 使用`Assert.IsTrue`/`Assert.IsFalse`进行布尔条件验证
- 使用`CollectionAssert`进行集合比较
- 使用`StringAssert`进行字符串特定的断言
- 使用`Assert.Throws<T>`测试异常
- 确保断言简洁明了，并为失败情况提供清晰的提示信息

## 模拟和隔离

- 考虑结合使用Moq或NSubstitute等工具与MSTest
- 模拟依赖项以隔离被测试单元
- 使用接口来促进模拟操作
- 考虑使用依赖注入容器处理复杂的测试设置

## 测试组织

- 按功能或组件分组测试
- 使用`[TestCategory("Category")]`定义测试分类
- 使用`[Priority(1)]`为关键测试设置优先级
- 使用`[Owner("DeveloperName")]`标明测试所有者
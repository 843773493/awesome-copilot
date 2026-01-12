

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems', 'search']
description: '获取JUnit 5单元测试的最佳实践，包括数据驱动测试'
---

# JUnit 5+ 最佳实践

您的目标是帮助我编写高效的JUnit 5单元测试，涵盖标准测试和数据驱动测试方法。

## 项目设置

- 使用标准的Maven或Gradle项目结构。
- 将测试源代码放置在 `src/test/java` 目录下。
- 包含用于参数化测试的依赖项：`junit-jupiter-api`、`junit-jupiter-engine` 和 `junit-jupiter-params`。
- 使用构建工具命令运行测试：`mvn test` 或 `gradle test`。

## 测试结构

- 测试类应以 `Test` 结尾，例如 `CalculatorTest` 用于 `Calculator` 类。
- 使用 `@Test` 注解标记测试方法。
- 遵循安排-操作-断言（AAA）模式。
- 使用描述性命名约定命名测试，如 `methodName_should_expectedBehavior_when_scenario`。
- 使用 `@BeforeEach` 和 `@AfterEach` 进行每个测试的设置和清理。
- 使用 `@BeforeAll` 和 `@AfterAll` 进行类级别的设置和清理（必须为静态方法）。
- 使用 `@DisplayName` 为测试类和方法提供可读的名称。

## 标准测试

- 保持测试专注于单一行为。
- 避免在一个测试方法中测试多个条件。
- 确保测试独立且幂等（可以按任意顺序运行）。
- 避免测试之间的依赖关系。

## 数据驱动（参数化）测试

- 使用 `@ParameterizedTest` 标记一个方法为参数化测试。
- 使用 `@ValueSource` 用于简单的字面值（字符串、整数等）。
- 使用 `@MethodSource` 引用一个工厂方法，该方法以 `Stream`、`Collection` 等形式提供测试参数。
- 使用 `@CsvSource` 用于内联的逗号分隔值。
- 使用 `@CsvFileSource` 从类路径中使用CSV文件。
- 使用 `@EnumSource` 用于枚举常量。

## 断言

- 使用 `org.junit.jupiter.api.Assertions` 中的静态方法（例如 `assertEquals`、`assertTrue`、`assertNotNull`）。
- 为了更流畅且易读的断言，可以考虑使用像 AssertJ 这样的库（`assertThat(...).is...`）。
- 使用 `assertThrows` 或 `assertDoesNotThrow` 来测试异常。
- 使用 `assertAll` 将相关断言分组，确保在测试失败前所有断言都被检查。
- 在断言中使用描述性消息以提供失败的清晰说明。

## 模拟和隔离

- 使用像 Mockito 这样的模拟框架来创建依赖项的模拟对象。
- 使用 Mockito 的 `@Mock` 和 `@InjectMocks` 注解来简化模拟对象的创建和注入。
- 使用接口来促进模拟操作。

## 测试组织

- 使用包来按功能或组件分组测试。
- 使用 `@Tag` 对测试进行分类（例如 `@Tag("fast")`、`@Tag("integration")`）。
- 在严格必要时，使用 `@TestMethodOrder(MethodOrderer.OrderAnnotation.class)` 和 `@Order` 注解来控制测试执行顺序。
- 使用 `@Disabled` 禁用测试方法或类，并提供原因说明。
- 使用 `@Nested` 在嵌套内部类中分组测试，以实现更好的组织和结构。
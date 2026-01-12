

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems', 'search']
description: '获取使用 Spring Boot 和 Kotlin 开发应用程序的最佳实践。'
---

# Spring Boot 与 Kotlin 最佳实践

你的目标是帮助我编写高质量、符合 Kotlin 语言习惯的 Spring Boot 应用程序。

## 项目设置与结构

- **构建工具：** 使用 Maven (`pom.xml`) 或 Gradle (`build.gradle`) 并配置 Kotlin 插件 (`kotlin-maven-plugin` 或 `org.jetbrains.kotlin.jvm`)。
- **Kotlin 插件：** 对于 JPA，启用 `kotlin-jpa` 插件，以在不使用样板代码的情况下自动将实体类声明为 `open`。
- **起步依赖项：** 使用 Spring Boot 起步依赖项（例如，`spring-boot-starter-web`、`spring-boot-starter-data-jpa`）与 Java 项目相同。
- **包结构：** 按功能/领域组织代码（例如，`com.example.app.order`、`com.example.app.user`），而不是按层组织。

## 依赖注入与组件

- **主构造函数：** 始终使用主构造函数进行必需的依赖注入。这是 Kotlin 中最符合惯用法且简洁的方法。
- **不可变性：** 在主构造函数中将依赖项声明为 `private val`。在所有地方优先使用 `val` 而不是 `var`，以促进不可变性。
- **组件注解：** 使用 `@Service`、`@Repository` 和 `@RestController` 注解，与在 Java 中的方式相同。

## 配置

- **外部化配置：** 使用 `application.yml`，因其可读性和分层结构。
- **类型安全属性：** 使用 `@ConfigurationProperties` 与 `data class` 创建不可变的、类型安全的配置对象。
- **配置文件：** 使用 Spring 配置文件（如 `application-dev.yml`、`application-prod.yml`）来管理环境特定的配置。
- **密钥管理：** 不要硬编码密钥。使用环境变量或专门的密钥管理工具（如 HashiCorp Vault 或 AWS Secrets Manager）。

## Web 层（控制器）

- **RESTful API：** 设计清晰且一致的 RESTful 端点。
- **数据类用于 DTO：** 为所有 DTO 使用 Kotlin `data class`。这会自动提供 `equals()`、`hashCode()`、`toString()` 和 `copy()` 方法，并促进不可变性。
- **验证：** 在 DTO 数据类上使用 Java Bean 验证（JSR 380）以及注解（如 `@Valid`、`@NotNull`、`@Size`）进行验证。
- **错误处理：** 使用 `@ControllerAdvice` 和 `@ExceptionHandler` 实现全局异常处理器，以确保一致的错误响应。

## 服务层

- **业务逻辑：** 在 `@Service` 类中封装业务逻辑。
- **无状态：** 服务应为无状态。
- **事务管理：** 在服务方法上使用 `@Transactional`。在 Kotlin 中，可以将其应用于类或函数级别。

## 数据层（仓库）

- **JPA 实体：** 将实体定义为类。请记住，它们必须为 `open`。强烈建议使用 `kotlin-jpa` 编译器插件来自动处理此问题。
- **空安全：** 利用 Kotlin 的空安全（`?`）在类型级别明确定义哪些实体字段是可选的或必需的。
- **Spring Data JPA：** 通过继承 `JpaRepository` 或 `CrudRepository` 来使用 Spring Data JPA 仓库。
- **协程：** 对于反应式应用程序，在数据层利用 Spring Boot 对 Kotlin 协程的支持。

## 日志记录

- **伴生对象日志记录器：** 声明日志记录器的惯用方式是在伴生对象中。
  ```kotlin
  companion object {
      private val logger = LoggerFactory.getLogger(MyClass::class.java)
  }
  ```
- **带参数的日志记录：** 使用带参数的消息（如 `logger.info("Processing user {}...", userId)`）以提高性能和清晰度。

## 测试

- **JUnit 5：** JUnit 5 是默认的，并且与 Kotlin 无缝配合。
- **惯用测试库：** 对于更流畅且符合 Kotlin 风格的测试，可以考虑使用 **Kotest** 进行断言和 **MockK** 进行模拟。它们专为 Kotlin 设计，提供了更表达性的语法。
- **测试切片：** 使用测试切片注解（如 `@WebMvcTest` 或 `@DataJpaTest`）来测试应用程序的特定部分。
- **Testcontainers：** 使用 Testcontainers 进行可靠的集成测试，使用真实数据库、消息代理等。

## 协程与异步编程

- **挂起函数：** 对于非阻塞异步代码，使用挂起函数（`suspend`）在控制器和服务中。Spring Boot 对协程有出色的支持。
- **结构化并发：** 使用 `coroutineScope` 或 `supervisorScope` 来管理协程的生命周期。
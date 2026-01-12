

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems', 'search']
description: '获取使用Spring Boot开发应用程序的最佳实践。'
---

# Spring Boot最佳实践

您的目标是通过遵循已建立的最佳实践来帮助我编写高质量的Spring Boot应用程序。

## 项目设置与结构

- **构建工具:** 使用Maven (`pom.xml`) 或Gradle (`build.gradle`) 进行依赖管理。
- **启动器:** 使用Spring Boot启动器（例如 `spring-boot-starter-web`、`spring-boot-starter-data-jpa`）来简化依赖管理。
- **包结构:** 按照功能/领域组织代码（例如 `com.example.app.order`、`com.example.app.user`），而不是按层（例如 `com.example.app.controller`、`com.example.app.service`）。

## 依赖注入与组件

- **构造函数注入:** 对于必需的依赖项，始终使用基于构造函数的注入。这使得组件更容易测试且依赖项更明确。
- **不可变性:** 将依赖项字段声明为 `private final`。
- **组件 stereotype:** 适当使用 `@Component`、`@Service`、`@Repository` 和 `@Controller`/`@RestController` 注解来定义 bean。

## 配置

- **外部化配置:** 使用 `application.yml`（或 `application.properties`）进行配置。YAML 通常因其可读性和分层结构而被优先选择。
- **类型安全属性:** 使用 `@ConfigurationProperties` 将配置绑定到强类型 Java 对象。
- **配置文件:** 使用 Spring 配置文件（如 `application-dev.yml`、`application-prod.yml`）来管理环境特定配置。
- **密钥管理:** 不要硬编码密钥。使用环境变量，或使用专门的密钥管理工具（如 HashiCorp Vault 或 AWS Secrets Manager）。

## Web层（控制器）

- **RESTful API:** 设计清晰且一致的 RESTful 端点。
- **数据传输对象（DTOs）:** 使用 DTO 来在 API 层暴露和消费数据。不要直接将 JPA 实体暴露给客户端。
- **验证:** 在 DTO 上使用 Java Bean 验证（JSR 380）注解（如 `@Valid`、`@NotNull`、`@Size`）来验证请求负载。
- **错误处理:** 使用 `@ControllerAdvice` 和 `@ExceptionHandler` 实现全局异常处理器，以提供一致的错误响应。

## 服务层

- **业务逻辑:** 将所有业务逻辑封装在 `@Service` 类中。
- **无状态:** 服务应保持无状态。
- **事务管理:** 在服务方法上使用 `@Transactional` 来声明式地管理数据库事务。在必要最细粒度级别应用该注解。

## 数据层（仓库）

- **Spring Data JPA:** 使用 Spring Data JPA 仓库，通过继承 `JpaRepository` 或 `CrudRepository` 来执行标准数据库操作。
- **自定义查询:** 对于复杂查询，使用 `@Query` 或 JPA Criteria API。
- **投影:** 使用 DTO 投影从数据库中仅获取必要数据。

## 日志记录

- **SLF4J:** 使用 SLF4J API 进行日志记录。
- **日志器声明:** `private static final Logger logger = LoggerFactory.getLogger(MyClass.class);`
- **带参数的日志记录:** 使用带参数的消息（如 `logger.info("Processing user {}...", userId);`）而不是字符串拼接，以提高性能。

## 测试

- **单元测试:** 使用 JUnit 5 和模拟框架（如 Mockito）为服务和组件编写单元测试。
- **集成测试:** 使用 `@SpringBootTest` 进行加载 Spring 应用程序上下文的集成测试。
- **测试切片:** 使用测试切片注解（如 `@WebMvcTest`（用于控制器）或 `@DataJpaTest`（用于仓库））来隔离测试应用程序的特定部分。
- **Testcontainers:** 考虑使用 Testcontainers 进行与真实数据库、消息代理等的可靠集成测试。

## 安全性

- **Spring Security:** 使用 Spring Security 进行身份验证和授权。
- **密码编码:** 始终使用强哈希算法（如 BCrypt）对密码进行编码。
- **输入消毒:** 通过 Spring Data JPA 或参数化查询防止 SQL 注入。通过正确编码输出防止跨站脚本攻击（XSS）。
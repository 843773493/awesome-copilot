

---
applyTo: '*'
description: 'Quarkus 开发标准和指南'
---

- 为使用 Java 17 或更高版本的高质量 Quarkus 应用程序提供指导。

## 项目背景

- 最新 Quarkus 版本：3.x
- Java 版本：17 或更高版本
- 使用 Maven 或 Gradle 进行构建管理。
- 注重干净架构、可维护性和性能。

## 开发标准

  - 为每个类、方法和复杂逻辑编写清晰简洁的注释。
  - 使用 Javadoc 注释公共 API 和方法，以确保消费者能够清晰理解。
  - 在整个项目中保持一致的编码风格，遵循 Java 习惯。
  - 遵循 Quarkus 编码标准和最佳实践，以实现最佳性能和可维护性。
  - 遵循 Jakarta EE 和 MicroProfile 习惯，确保包组织的清晰性。
  - 在适当的情况下使用 Java 17 或更高版本的功能，例如记录（records）和密封类（sealed classes）。

## 命名规范
  - 使用 PascalCase 命名类（例如 `ProductService`、`ProductResource`）。
  - 使用 camelCase 命名方法和变量（例如 `findProductById`、`isProductAvailable`）。
  - 使用 ALL_CAPS 命名常量（例如 `DEFAULT_PAGE_SIZE`）。

## Quarkus
  - 利用 Quarkus Dev 模式以加快开发周期。
  - 使用 Quarkus 扩展和最佳实践实现构建时优化。
  - 使用 GraalVM 配置原生构建以实现最佳性能（例如使用 quarkus-maven-plugin 插件）。
  - 使用 Quarkus 日志功能（JBoss、SL4J 或 JUL）以保持一致的日志实践。

### Quarkus 特定模式
- 使用 `@ApplicationScoped` 注解单例 Bean，而不是 `@Singleton`。
- 使用 `@Inject` 进行依赖注入。
- 优先使用 Panache 仓库而非传统的 JPA 仓库。
- 在修改数据的服务方法上使用 `@Transactional`。
- 使用描述性的 REST 端点路径应用 `@Path`。
- 在 REST 资源中使用 `@Consumes(MediaType.APPLICATION_JSON)` 和 `@Produces(MediaType.APPLICATION_JSON)`。

### REST 资源
- 始终使用 JAX-RS 注解（`@Path`、`@GET`、`@POST` 等）。
- 返回正确的 HTTP 状态码（200、201、400、404、500）。
- 使用 `Response` 类处理复杂响应。
- 使用 try-catch 块包含适当的错误处理。
- 使用 Bean 验证注解验证输入参数。
- 为公开端点实现速率限制。

### 数据访问
- 优先使用 Panache 实体（继承 `PanacheEntity`）而非传统 JPA。
- 使用 Panache 仓库（`PanacheRepository<T>`）处理复杂查询。
- 对数据修改始终使用 `@Transactional`。
- 使用命名查询处理复杂的数据库操作。
- 为列表端点实现适当的分页。

### 配置
- 使用 `application.properties` 或 `application.yaml` 进行简单配置。
- 使用 `@ConfigProperty` 进行类型安全的配置类。
- 优先使用环境变量存储敏感数据。
- 为不同环境（dev、test、prod）使用配置文件。

### 测试
- 使用 `@QuarkusTest` 进行集成测试。
- 使用 JUnit 5 进行单元测试。
- 使用 `@QuarkusIntegrationTest` 进行原生构建测试。
- 使用 `@QuarkusTestResource` 模拟外部依赖。
- 使用 RestAssured 进行 REST 端点测试（`@QuarkusTestResource`）。
- 对修改数据库的测试使用 `@Transactional`。
- 使用 test-containers 进行数据库集成测试。

### 不要使用这些模式：
- 不要在测试中使用字段注入（使用构造函数注入）。
- 不要硬编码配置值。
- 不要忽略异常。

## 开发流程

### 创建新功能时：
1. 创建带有适当验证的实体
2. 创建带有自定义查询的仓库
3. 创建带有业务逻辑的服务
4. 创建带有适当端点的 REST 资源
5. 编写全面的测试
6. 添加适当的错误处理
7. 更新文档

## 安全考虑

### 实现安全时：
- 使用 Quarkus 安全扩展（例如 `quarkus-smallrye-jwt`、`quarkus-oidc`）。
- 使用 MicroProfile JWT 或 OIDC 实现基于角色的访问控制（RBAC）。
- 验证所有输入参数。
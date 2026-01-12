

---
description: 'Spring Boot基础应用构建指南'
applyTo: '**/*.java, **/*.kt'
---

# Spring Boot开发

## 通用指导原则

- 在审查代码更改时，仅提出高置信度的建议。
- 编写具有良好可维护性的代码，包括对某些设计决策的注释说明。
- 处理边界情况并编写清晰的异常处理。
- 对于库或外部依赖项，在注释中说明其用途和使用方式。

## Spring Boot指导原则

### 依赖注入

- 对所有必需的依赖项使用构造函数注入。
- 将依赖字段声明为 `private final`。

### 配置

- 使用YAML文件（`application.yml`）进行外部化配置。
- 环境配置文件：使用Spring配置文件区分不同环境（dev、test、prod）
- 配置属性：使用 `@ConfigurationProperties` 实现类型安全的配置绑定
- 密钥管理：使用环境变量或密钥管理系统外部化敏感信息

### 代码组织

- 包结构：按功能/领域组织，而非按层组织
- 职责分离：保持控制器简洁，服务专注，仓库简单
- 工具类：使工具类为final并使用私有构造函数

### 服务层

- 将业务逻辑放在带有 `@Service` 注解的类中。
- 服务应无状态且可测试。
- 通过构造函数注入仓库。
- 服务方法签名应使用领域ID或DTO，除非必要，否则不应直接暴露仓库实体。

### 日志记录

- 所有日志使用SLF4J（`private static final Logger logger = LoggerFactory.getLogger(MyClass.class);`）。
- 不要直接使用具体实现（如Logback、Log4j2）或 `System.out.println()`。
- 使用参数化日志：`logger.info("User {} logged in", userId);`。

### 安全与输入处理

- 使用参数化查询 | 始终使用Spring Data JPA或`NamedParameterJdbcTemplate`以防止SQL注入。
- 使用JSR-380注解（如`@NotNull`、`@Size`等）和`BindingResult`验证请求体和参数。

## 构建与验证

- 在添加或修改代码后，确保项目仍能成功构建。
- 如果项目使用Maven，运行 `mvn clean package`。
- 如果项目使用Gradle，运行 `./gradlew build`（或 `gradlew.bat build` 在Windows上）。
- 确保构建过程中所有测试都能通过。

## 有用的命令

| Gradle命令            | Maven命令                     | 描述                                   |
|:--------------------------|:----------------------------------|:----------------------------------------------|
| `./gradlew bootRun`       |`./mvnw spring-boot:run`           | 运行应用程序。                          |
| `./gradlew build`         |`./mvnw package`                   | 构建应用程序。                        |
| `./gradlew test`          |`./mvnw test`                      | 运行测试。                                    |
| `./gradlew bootJar`       |`./mvnw spring-boot:repackage`     | 将应用程序打包为JAR。             |
| `./gradlew bootBuildImage`|`./mvnw spring-boot:build-image`   | 将应用程序打包为容器镜像。 |
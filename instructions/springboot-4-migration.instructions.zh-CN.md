

---
description: "从 Spring Boot 3.x 迁移到 4.0 的完整指南，重点介绍 Gradle Kotlin DSL 和版本目录"
applyTo: "**/*.java, **/*.kt, **/build.gradle.kts, **/build.gradle, **/settings.gradle.kts, **/gradle/libs.versions.toml, **/*.properties, **/*.yml, **/*.yaml"
---

# Spring Boot 3.x 到 4.0 的迁移指南

## 项目背景

本指南提供了升级 Spring Boot 项目从 3.x 版本到 4.0 的完整 GitHub Copilot 指南，特别强调 Gradle Kotlin DSL、版本目录（`libs.versions.toml`）以及 Kotlin 特定的注意事项。

**Spring Boot 4.0 的关键架构变更：**
- 模块化依赖结构，采用更小、更专注的模块
- 必须使用 Spring Framework 7.x
- Jakarta EE 11（Servlet 6.1 基线）
- Jackson 3.x 迁移（包命名空间变更）
- 必须使用 Kotlin 2.2+
- 全面的属性重新组织

## 系统要求

### 最低版本

- **Java**: 17+（建议使用最新 LTS：Java 21 或 25）
- **Kotlin**: 2.2.0 或更高版本
- **Spring Framework**: 7.x（由 Spring Boot 4.0 管理）
- **Jakarta EE**: 11（Servlet 6.1 基线）
- **GraalVM**（用于原生镜像）: 25+
- **Gradle**: 8.5+（支持 Kotlin DSL 和版本目录）
- **Gradle CycloneDX 插件**: 3.0.0+

### 验证兼容性

```bash
# 检查当前版本
./gradlew --version
./gradlew dependencies --configuration runtimeClasspath
```

## 迁移前步骤

### 1. 升级到最新的 Spring Boot 3.5.x

在迁移到 4.0 之前，先升级到最新的 3.5.x 版本：

```kotlin
// libs.versions.toml
[versions]
springBoot = "3.5.6" # 迁移到 4.0 之前的最新 3.x 版本
```

### 2. 清理弃用项

从 Spring Boot 3.x 中移除所有弃用的 API 使用。这些在 4.0 中将导致编译错误：

```bash
# 构建并审查警告
./gradlew clean build --warning-mode all
```

### 3. 审查依赖项变更

将您的依赖项与以下内容进行对比：
- [Spring Boot 3.5.x 依赖项版本](https://docs.spring.io/spring-boot/3.5/appendix/dependency-versions/coordinates.html)
- [Spring Boot 4.0.x 依赖项版本](https://docs.spring.io/spring-boot/4.0/appendix/dependency-versions/coordinates.html)

## 模块重构和启动器变更

### 关键：模块化架构

Spring Boot 4.0 引入了**更小、更专注的模块**，取代了大型单体 JAR。这要求大多数项目进行依赖项更新。

**对库作者的重要提示：** 由于模块化工作的进行和包重新组织，**不建议在同一个构件中支持 Spring Boot 3 和 Spring Boot 4**。库作者应为每个主要版本发布单独的构件，以避免运行时冲突并确保清晰的依赖管理。

### 迁移策略：选择一种方法

#### 选项 1：技术专用启动器（推荐用于生产环境）

大多数由 Spring Boot 覆盖的技术现在都有**专用测试启动器**。这提供了更细粒度的控制。

**完整启动器参考：** 有关所有可用启动器（核心、Web、数据库、Spring Data、消息、安全、模板、生产就绪等）及其测试启动器的详细表格，请参阅 [官方 Spring Boot 4.0 迁移指南](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide#starters)。

**libs.versions.toml:**
```toml
[versions]
springBoot = "4.0.0"

[libraries]
# 核心启动器及其专用测试模块
spring-boot-starter-webmvc = { module = "org.springframework.boot:spring-boot-starter-webmvc", version.ref = "springBoot" }
spring-boot-starter-data-jpa = { module = "org.springframework.boot:spring-boot-starter-data-jpa", version.ref = "springBoot" }
spring-boot-starter-security = { module = "org.springframework.boot:spring-boot-starter-security", version.ref = "springBoot" }
```

**build.gradle.kts:**
```kotlin
dependencies {
    implementation(libs.spring.boot.starter.webmvc)
    implementation(libs.spring.boot.starter.data.jpa)
    implementation(libs.spring.boot.starter.security)

    testImplementation(libs.spring.boot.starter.data.jpa.test)
    testImplementation(libs.spring.boot.starter.security.test)
}
```

#### 选项 2：经典启动器（快速迁移，已弃用）

为了快速迁移，使用**经典启动器**，它们捆绑了所有自动配置（如 Spring Boot 3.x）：

**libs.versions.toml:**
```toml
[libraries]
spring-boot-starter-classic = { module = "org.springframework.boot:spring-boot-starter-classic", version.ref = "springBoot" }
spring-boot-starter-test-classic = { module = "org.springframework.boot:spring-boot-starter-test-classic", version.ref = "springBoot" }
```

**build.gradle.kts:**
```kotlin
dependencies {
    implementation(libs.spring.boot.starter.classic)
    testImplementation(libs.spring.boot.starter.test.classic)
}
```

**警告：** 经典启动器是**已弃用**的，将在未来版本中移除。请计划迁移到技术专用启动器。

#### 选项 3：直接模块依赖（高级）

对于对传递依赖项有显式控制需求的用户：

**libs.versions.toml:**
```toml
[libraries]
spring-boot-webmvc = { module = "org.springframework.boot:spring-boot-webmvc", version.ref = "springBoot" }
spring-boot-webmvc-test = { module = "org.springframework.boot:spring-boot-webmvc-test", version.ref = "springBoot" }
```

### 启动器重命名（破坏性变更）

在您的 `libs.versions.toml` 中更新这些启动器名称：

| Spring Boot 3.x | Spring Boot 4.0 | 说明 |
|----------------|-----------------|------|
| `spring-boot-starter-web` | `spring-boot-starter-webmvc` | 显式命名 |
| `spring-boot-starter-web-services` | `spring-boot-starter-webservices` | 去掉连字符 |
| `spring-boot-starter-aop` | `spring-boot-starter-aspectj` | 仅在使用 `org.aspectj.lang.annotation` 时需要 |
| `spring-boot-starter-oauth2-authorization-server` | `spring-boot-starter-security-oauth2-authorization-server` | 安全命名空间 |
| `spring-boot-starter-oauth2-client` | `spring-boot-starter-security-oauth2-client` | 安全命名空间 |
| `spring-boot-starter-oauth2-resource-server` | `spring-boot-starter-security-oauth2-resource-server` | 安全命名空间 |

**迁移示例 (libs.versions.toml):**
```toml
[libraries]
# 旧版本 (Spring Boot 3.x)
# spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web", version.ref = "springBoot" }
# spring-boot-starter-oauth2-client = { module = "org.springframework.boot:spring-boot-starter-oauth2-client", version.ref = "springBoot" }

# 新版本 (Spring Boot 4.0)
spring-boot-starter-webmvc = { module = "org.springframework.boot:spring-boot-starter-webmvc", version.ref = "springBoot" }
spring-boot-starter-security-oauth2-client = { module = "org.springframework.boot:spring-boot-starter-security-oauth2-client", version.ref = "springBoot" }
```

### AspectJ 启动器说明

仅在**实际使用 AspectJ 注解**时包含 `spring-boot-starter-aspectj`：

```kotlin
// 仅在代码使用 org.aspectj.lang.annotation 包时需要
import org.aspectj.lang.annotation.Aspect
import org.aspectj.lang.annotation.Before

@Aspect
class MyAspect {
    @Before("execution(* com.example..*(..))")
    fun beforeAdvice() { }
}
```

如果不使用 AspectJ，请移除该依赖项。

## 已移除的功能和替代方案

### 内嵌服务器

#### Undertow 移除

**Undertow 完全移除** - 不兼容 Servlet 6.1 基线。

**迁移方法：**
- 使用 **Tomcat**（默认）或 **Jetty**
- **不要**将 Spring Boot 4.0 应用部署到非 Servlet 6.1 容器

**libs.versions.toml:**
```toml
[libraries]
# 移除 Undertow
# spring-boot-starter-undertow = { module = "org.springframework.boot:spring-boot-starter-undertow", version.ref = "springBoot" }

# 使用 Tomcat（默认）或 Jetty
spring-boot-starter-jetty = { module = "org.springframework.boot:spring-boot-starter-jetty", version.ref = "springBoot" }
```

**build.gradle.kts:**
```kotlin
dependencies {
    implementation(libs.spring.boot.starter.webmvc) {
        exclude(group = "org.springframework.boot", module = "spring-boot-starter-tomcat")
    }
    implementation(libs.spring.boot.starter.jetty) // 替代 Tomcat
}
```

### 会话管理

#### Spring Session Hazelcast 和 MongoDB 移除

由各自团队维护，不再包含在 Spring Boot 依赖管理中。

**迁移 (libs.versions.toml):**
```toml
[versions]
hazelcast-spring-session = "3.x.x" # 请查看 Hazelcast 文档
mongodb-spring-session = "4.x.x"   # 请查看 MongoDB 文档

[libraries]
# 需要显式版本
spring-session-hazelcast = { module = "com.hazelcast:spring-session-hazelcast", version.ref = "hazelcast-spring-session" }
spring-session-mongodb = { module = "org.springframework.session:spring-session-data-mongodb", version.ref = "mongodb-spring-session" }
```

### 反应式消息框架

#### Pulsar 反应式移除

Spring Pulsar 已移除 Reactor 支持 - 反应式 Pulsar 客户端被移除。

**迁移：**
- 使用 **指令式 Pulsar 客户端**
- 或迁移到其他反应式消息框架（如 Kafka、RabbitMQ）

### 测试框架

#### Mockito 集成移除

`MockitoTestExecutionListener` 已移除（在 3.4 中弃用）。

**迁移到 MockitoExtension：**
```kotlin
// 旧版本 (Spring Boot 3.x)
import org.springframework.boot.test.context.SpringBootTest
import org.mockito.Mock
import org.mockito.Captor

@SpringBootTest
class MyServiceTest {
    @Mock
    private lateinit var repository: MyRepository

    @Captor
    private lateinit var captor: ArgumentCaptor<String>
}

// 新版本 (Spring Boot 4.0)
import org.springframework.boot.test.context.SpringBootTest
import org.mockito.Mock
import org.mockito.Captor
import org.mockito.junit.jupiter.MockitoExtension
import org.junit.jupiter.api.extension.ExtendWith

@SpringBootTest
@ExtendWith(MockitoExtension::class) // 必须显式声明扩展
class MyServiceTest {
    @Mock
    private lateinit var repository: MyRepository

    @Captor
    private lateinit var captor: ArgumentCaptor<String>
}
```

### @SpringBootTest 变更

`@SpringBootTest` 不再自动提供 **MockMVC**、**WebTestClient** 或 **TestRestTemplate**。

#### MockMVC 配置

```kotlin
// 旧版本 (Spring Boot 3.x)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class ControllerTest {
    @Autowired
    private lateinit var mockMvc: MockMvc // 可自动获取
}

// 新版本 (Spring Boot 4.0)
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.autoconfigure.web.servlet.HtmlUnit

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc // 必须显式声明注解
class ControllerTest {
    @Autowired
    private lateinit var mockMvc: MockMvc
}

// HtmlUnit 配置移到注解属性
@AutoConfigureMockMvc(
    htmlUnit = HtmlUnit(webClient = false, webDriver = false)
)
```

#### WebTestClient 配置

```kotlin
// 旧版本 (Spring Boot 3.x)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class WebFluxTest {
    @Autowired
    private lateinit var webTestClient: WebTestClient // 可自动获取
}

// 新版本 (Spring Boot 4.0)
import org.springframework.boot.test.autoconfigure.web.reactive.AutoConfigureWebTestClient

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureWebTestClient // 必须显式声明注解
class WebFluxTest {
    @Autowired
    private lateinit var webTestClient: WebTestClient
}
```

#### TestRestTemplate → RestTestClient（推荐）

**Spring Boot 4.0 引入了 `RestTestClient`** 作为 `TestRestTemplate` 的现代替代。

```kotlin
// 旧方法（仍可使用，但需注解）
import org.springframework.boot.test.autoconfigure.web.client.AutoConfigureTestRestTemplate
import org.springframework.boot.test.web.client.TestRestTemplate

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureTestRestTemplate // 在 4.0 中必需
class RestApiTest {
    @Autowired
    private lateinit var testRestTemplate: TestRestTemplate
}

// 新推荐方法
import org.springframework.boot.test.autoconfigure.web.client.AutoConfigureRestTestClient
import org.springframework.boot.resttestclient.RestTestClient

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient // 新注解
class RestApiTest {
    @Autowired
    private lateinit var restTestClient: RestTestClient

    @Test
    fun testEndpoint() {
        val response = restTestClient.get()
            .uri("/api/users")
            .retrieve()
            .toEntity<List<User>>()

        assertThat(response.statusCode).isEqualTo(HttpStatus.OK)
    }
}
```

**如果仍在使用 `TestRestTemplate`，请务必：**
1. 添加 `spring-boot-resttestclient` 测试依赖
2. **更新包导入**（类已移动到新包）

**libs.versions.toml:**
```toml
[libraries]
spring-boot-resttestclient = { module = "org.springframework.boot:spring-boot-resttestclient", version.ref = "springBoot" }
```

**build.gradle.kts:**
```kotlin
dependencies {
    testImplementation(libs.spring.boot.resttestclient)
}
```

**更新包导入（必需）：**
```kotlin
// 旧包导入 - 将导致编译失败
// import org.springframework.boot.test.web.client.TestRestTemplate

// 新包导入 - 在 Spring Boot 4.0 中必需
import org.springframework.boot.resttestclient.TestRestTemplate
```

### @PropertyMapping 注解迁移

```kotlin
// 旧版本 (Spring Boot 3.x)
import org.springframework.boot.test.autoconfigure.properties.PropertyMapping
import org.springframework.boot.test.autoconfigure.properties.Skip

// 新版本 (Spring Boot 4.0)
import org.springframework.boot.test.context.PropertyMapping
import org.springframework.boot.test.context.PropertyMapping.Skip
```

## 生产就绪功能和模块

### 健康、指标和可观测性模块

Spring Boot 4.0 将生产就绪功能模块化，专注于特定功能：

**libs.versions.toml:**
```toml
[libraries]
# 健康监控
spring-boot-health = { module = "org.springframework.boot:spring-boot-health", version.ref = "springBoot" }

# Micrometer 指标
spring-boot-micrometer-metrics = { module = "org.springframework.boot:spring-boot-micrometer-metrics", version.ref = "springBoot" }
spring-boot-micrometer-metrics-test = { module = "org.springframework.boot:spring-boot-micrometer-metrics-test", version.ref = "springBoot" }

# Micrometer 观察
spring-boot-micrometer-observation = { module = "org.springframework.boot:spring-boot-micrometer-observation", version.ref = "springBoot" }

# 分布式追踪
spring-boot-micrometer-tracing = { module = "org.springframework.boot:spring-boot-micrometer-tracing", version.ref = "springBoot" }
spring-boot-micrometer-tracing-test = { module = "org.springframework.boot:spring-boot-micrometer-tracing-test", version.ref = "springBoot" }
spring-boot-micrometer-tracing-brave = { module = "org.springframework.boot:spring-boot-micrometer-tracing-brave", version.ref = "springBoot" }
spring-boot-micrometer-tracing-opentelemetry = { module = "org.springframework.boot:spring-boot-micrometer-tracing-opentelemetry", version.ref = "springBoot" }

# OpenTelemetry 集成
spring-boot-opentelemetry = { module = "org.springframework.boot:spring-boot-opentelemetry", version.ref = "springBoot" }

# Zipkin 报告器
spring-boot-zipkin = { module = "org.springframework.boot:spring-boot-zipkin", version.ref = "springBoot" }
```

**build.gradle.kts（示例可观测性堆栈）：**
```kotlin
dependencies {
    // Actuator（含指标和追踪）
    implementation(libs.spring.boot.starter.actuator)
    implementation(libs.spring.boot.micrometer.observation)
    implementation(libs.spring.boot.micrometer.tracing.opentelemetry)
    implementation(libs.spring.boot.opentelemetry)

    // 测试支持
    testImplementation(libs.spring.boot.micrometer.metrics.test)
    testImplementation(libs.spring.boot.micrometer.tracing.test)
}
```

**注意：** 使用启动器（如 `spring-boot-starter-actuator`）的大多数应用程序不需要直接声明这些模块。使用直接模块依赖项以实现更细粒度的控制。

## Actuator 变更

### 健康探针默认启用

就绪性和存活探针现在**默认启用**。

**application.yml（如需禁用）：**
```yaml
management:
  endpoint:
    health:
      probes:
        enabled: false # 如果不使用 Kubernetes 探针则禁用
```

**自动暴露：**
- `/actuator/health/liveness`
- `/actuator/health/readiness`

## 构建配置

### Kotlin 编译器配置

**build.gradle.kts:**
```kotlin
import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    kotlin("jvm") version "2.2.0" // 最低版本 2.2.0
    kotlin("plugin.spring") version "2.2.0"
    id("org.springframework.boot") version "4.0.0"
    id("io.spring.dependency-management") version "1.1.7"
    id("org.cyclonedx.bom") version "3.0.0" // 最低版本 3.0.0
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21) // 或 17、25
    }
}

kotlin {
    compilerOptions {
        freeCompilerArgs.addAll(
            "-Xjsr305=strict", // 严格空安全
            "-Xemit-jvm-type-annotations" // 发射类型注解
        )
    }
}

tasks.withType<KotlinCompile> {
    kotlinOptions {
        jvmTarget = "21" // 匹配 Java 工具链
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

### Java 预览功能（如果使用 Java 25）

**build.gradle.kts:**
```kotlin
tasks.withType<JavaCompile> {
    options.compilerArgs.add("--enable-preview")
}

tasks.withType<Test> {
    jvmArgs("--enable-preview")
}

tasks.withType<JavaExec> {
    jvmArgs("--enable-preview")
}
```

## 迁移检查清单

### 迁移前

- [ ] 升级到最新的 Spring Boot 3.5.x
- [ ] 审查并修复所有弃用警告
- [ ] 记录当前依赖项版本
- [ ] 运行完整测试套件并验证构建成功
- [ ] 审查 [Spring Boot 3.5.x → 4.0 依赖项变更](https://docs.spring.io/spring-boot/4.0/appendix/dependency-versions/coordinates.html)

### 核心迁移

- [ ] 在 `libs.versions.toml` 中更新 Spring Boot 4.0.0
- [ ] 将 Kotlin 版本更新为 2.2.0+
- [ ] 重命名启动器：`spring-boot-starter-web` → `spring-boot-starter-webmvc` 等
- [ ] 添加技术专用测试启动器（或暂时使用经典启动器）
- [ ] 如果存在，移除 Undertow 依赖项（切换到 Tomcat 或 Jetty）
- [ ] 移除 `spring-session-hazelcast` / `spring-session-mongodb` 或添加显式版本

### Jackson 3 迁移

- [ ] 更新导入：`com.fasterxml.jackson` → `tools.jackson`
- [ ] 更新异常：`jackson-annotations` 仍使用旧的组 ID
- [ ] 重命名：`@JsonComponent` → `@JacksonComponent`
- [ ] 重命名：`Jackson2ObjectMapperBuilderCustomizer` → `JsonMapperBuilderCustomizer`
- [ ] 更新属性：`spring.jackson.read.*` → `spring.jackson.json.read.*`
- [ ] 如果需要，考虑临时使用 `spring-boot-jackson2` 模块

### 属性更新

- [ ] MongoDB：`spring.data.mongodb.*` → `spring.mongodb.*`（非 Spring Data 属性）
- [ ] 会话：`spring.session.redis.*` → `spring.session.data.redis.*`
- [ ] 持久化：`spring.dao.exceptiontranslation` → `spring.persistence.exceptiontranslation`
- [ ] Kafka 重试：`backoff.random` → `backoff.jitter`

### 代码更新

- [ ] 更新包：`BootstrapRegistry` → `org.springframework.boot.bootstrap.BootstrapRegistry`
- [ ] 更新包：`EnvironmentPostProcessor` → `org.springframework.boot.EnvironmentPostProcessor`
- [ ] 更新包：`EntityScan` → `org.springframework.boot.persistence.autoconfigure.EntityScan`
- [ ] 更新：`RestClient` → `Rest5Client`（Elasticsearch）
- [ ] 更新：`StreamBuilderFactoryBeanCustomizer` → `StreamsBuilderFactoryBeanConfigurer`（Kafka）
- [ ] 分割：`RabbitRetryTemplateCustomizer` → `RabbitTemplateRetrySettingsCustomizer` / `RabbitListenerRetrySettingsCustomizer`
- [ ] 替换：`HttpMessageConverters` → `ClientHttpMessageConvertersCustomizer` / `ServerHttpMessageConvertersCustomizer`
- [ ] 更新：如果需要空值处理，请使用 `PropertyMapper` 的 `.always()` 方法

### 测试框架更新

- [ ] 在使用 `@Mock` / `@Captor` 的测试中添加 `@ExtendWith(MockitoExtension::class)`
- [ ] 在使用 `MockMvc` 的测试中添加 `@AutoConfigureMockMvc`
- [ ] 在使用 `WebTestClient` 的测试中添加 `@AutoConfigureWebTestClient`
- [ ] 将 `TestRestTemplate` 迁移到 `RestTestClient`（或添加 `@AutoConfigureTestRestTemplate`）
- [ ] 更新：`@PropertyMapping` 导入 → `org.springframework.boot.test.context`

### 构建配置

- [ ] 将 Gradle 升级到 8.5+
- [ ] 将 Gradle CycloneDX 插件升级到 3.0.0+
- [ ] 审查可选依赖项是否包含在 uber JAR 中
- [ ] 如果存在，移除 `loaderImplementation = CLASSIC`
- [ ] 如果存在，移除 `launchScript()` 配置

### 验证

- [ ] 运行 `./gradlew clean build`
- [ ] 运行完整测试套件
- [ ] 使用 TestContainers 验证集成测试
- [ ] 检查新的 Kotlin 空值安全警告
- [ ] 测试 Spring Boot Actuator 端点
- [ ] 验证健康探针（`/actuator/health/liveness`、`/actuator/health/readiness`）
- [ ] 使用新默认值进行性能测试

## 迁移后

- [ ] 审查 Spring Boot 4.0 发布说明以获取更多功能
- [ ] 考虑采用新的 Spring Framework 7.0 功能
- [ ] 如果使用了经典启动器，请计划迁移到技术专用启动器
- [ ] 如果使用了 `spring-boot-jackson2` 模块，请计划迁移到 Spring Framework 核心重试
- [ ] 更新 CI/CD 流水线以满足 Java 17+ 要求
- [ ] 更新部署清单（Servlet 6.1 容器）

## 常见陷阱

1. **经典启动器**：请记住这些是**已弃用**的，计划迁移到技术专用启动器
2. **Undertow**：完全移除，无替代方案 - 必须使用 Tomcat 或 Jetty
3. **Jackson 3 包**：容易忽略 `jackson-annotations` 仍使用旧组 ID
4. **MongoDB 属性**：许多属性已迁移到 `spring.mongodb.*`，但部分仍保留在 `spring.data.mongodb.*`
5. **测试配置**：`@SpringBootTest` 不再自动配置 MockMVC/WebTestClient/TestRestTemplate
6. **Kotlin 2.2**：最低要求 - 旧版本将无法工作
7. **空值安全**：JSpecify 注解可能引发新的警告
8. **PropertyMapper**：空值处理行为变更 - 请审查使用情况
9. **Jersey + Jackson 3**：不兼容 - 使用 `spring-boot-jackson2` 模块
10. **健康探针**：现在默认启用 - 可能影响非 Kubernetes 部署

## 性能考虑

- **模块化启动器**：更小的 JAR 文件和更快的启动时间（技术专用启动器）
- **Spring Framework 7**：核心框架的性能改进
- **Jackson 3**：改进的 JSON 处理性能
- **虚拟线程**：考虑启用 Java 21+（`spring.threads.virtual.enabled=true`）

## 资源

- [Spring Boot 4.0 迁移指南](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide)
- [Spring Boot 4.0 发布说明](https://github.com/spring-projects/spring-boot/releases)
- [Spring Framework 7.0 文档](https://docs.spring.io/spring-framework/reference/)
- [Jackson 3 迁移指南](https://github.com/FasterXML/jackson/wiki/Jackson-3.0-Migration-Guide)
- [Kotlin 2.2 发布说明](https://kotlinlang.org/docs/whatsnew22.html)
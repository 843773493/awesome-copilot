

---
description: '将 Spring Boot JPA 应用程序转换为使用 Azure Cosmos DB 与 Spring Data Cosmos 的逐步指南'
applyTo: '**/*.java,**/pom.xml,**/build.gradle,**/application*.properties'
---

# 将 Spring JPA 项目转换为 Spring Data Cosmos

本通用指南适用于任何 JPA 到 Spring Data Cosmos DB 的转换项目。

## 高级计划

1. 更换构建依赖项（移除 JPA，添加 Cosmos + Identity）。
2. 添加 `cosmos` 配置文件和属性。
3. 添加 Cosmos 配置并使用正确的 Azure 身份验证。
4. 转换实体（id → `String`，添加 `@Container` 和 `@PartitionKey`，移除 JPA 映射，调整关系）。
5. 将仓库（repositories）从 `JpaRepository` 转换为 `CosmosRepository`。
6. **创建服务层**用于关系管理和模板兼容性。
7. **关键**：更新所有测试文件以支持 String IDs 和 Cosmos 仓库。
8. 通过 `CommandLineRunner` 初始化数据。
9. **关键**：测试运行时功能并修复模板兼容性问题。

## 逐步操作

### 步骤 1 — 构建依赖项

- **Maven** (`pom.xml`):
  - 移除依赖项 `spring-boot-starter-data-jpa`
  - 移除特定数据库依赖项（H2、MySQL、PostgreSQL）除非在其他地方需要
  - 添加 `com.azure:azure-spring-data-cosmos:5.17.0`（或最新兼容版本）
  - 添加 `com.azure:azure-identity:1.15.4`（用于 `DefaultAzureCredential`）
- **Gradle**：应用相同的依赖项更改以适应 Gradle 语法
- 移除测试容器和 JPA 特定的测试依赖项

### 步骤 2 — 属性和配置

- 创建 `src/main/resources/application-cosmos.properties`:
  ```properties
  azure.cosmos.uri=${COSMOS_URI:https://localhost:8081}
  azure.cosmos.database=${COSMOS_DATABASE:petclinic}
  azure.cosmos.populate-query-metrics=false
  azure.cosmos.enable-multiple-write-locations=false
  ```
- 更新 `src/main/resources/application.properties`:
  ```properties
  spring.profiles.active=cosmos
  ```

### 步骤 3 — 使用 Azure 身份的配置类

- 创建 `src/main/java/<rootpkg>/config/CosmosConfiguration.java`:
  ```java
  @Configuration
  @EnableCosmosRepositories(basePackages = "<rootpkg>")
  public class CosmosConfiguration extends AbstractCosmosConfiguration {

    @Value("${azure.cosmos.uri}")
    private String uri;

    @Value("${azure.cosmos.database}")
    private String dbName;

    @Bean
    public CosmosClientBuilder getCosmosClientBuilder() {
      return new CosmosClientBuilder().endpoint(uri).credential(new DefaultAzureCredentialBuilder().build());
    }

    @Override
    protected String getDatabaseName() {
      return dbName;
    }

    @Bean
    public CosmosConfig cosmosConfig() {
      return CosmosConfig.builder().enableQueryMetrics(false).build();
    }
  }

  ```
- **重要**：在生产环境中使用 `DefaultAzureCredentialBuilder().build()` 代替基于密钥的身份验证

### 步骤 4 — 实体转换

- 目标所有带有 JPA 注解的类（`@Entity`、`@MappedSuperclass`、`@Embeddable`）
- **基础实体更改**：
  - 将 `id` 字段类型从 `Integer` 改为 `String`
  - 添加 `@Id` 和 `@GeneratedValue` 注解
  - 添加 `@PartitionKey` 字段（通常为 `String partitionKey`）
  - 移除所有 `jakarta.persistence` 导入
- **关键 - Cosmos DB 序列化要求**：
  - **移除所有 `@JsonIgnore` 注解**，用于需要持久化的字段
  - **认证实体（User、Authority）必须完全可序列化** - 密码、权限或其他持久化字段不能使用 `@JsonIgnore`
  - **需要控制 JSON 字段名称时，使用 `@JsonProperty` 代替 `@JsonIgnore`**
  - **常见认证序列化错误**：`Cannot pass null or empty values to constructor` 通常意味着 `@JsonIgnore` 阻止了必要字段的序列化
- **实体特定更改**：
  - 将 `@Entity` 替换为 `@Container(containerName = "<复数实体名称>")`
  - 移除 `@Table`、`@Column`、`@JoinColumn` 等注解
  - 移除关系注解（`@OneToMany`、`@ManyToOne`、`@ManyToMany`）
  - 对于关系：
    - 用于一对一/一对多的嵌入集合（例如 Owner 中的 `List<Pet> pets`）
    - 用于多对一的引用 ID（例如 Pet 中的 `String ownerId`）
    - **对于复杂关系**：存储 ID 但添加瞬时属性以支持模板
  - 添加构造函数以设置分区键：`setPartitionKey("entityType")`

### 步骤 6 — **创建服务层**用于关系管理和模板兼容性

- **关键**：创建服务类以桥接 Cosmos 文档存储与现有模板期望
- **目的**：处理关系填充并保持模板兼容性
- **每个具有关系的实体的服务模式**：
  ```java
  @Service
  public class EntityService {

    private final EntityRepository entityRepository;
    private final RelatedRepository relatedRepository;

    public EntityService(EntityRepository entityRepository, RelatedRepository relatedRepository) {
      this.entityRepository = entityRepository;
      this.relatedRepository = relatedRepository;
    }

    public List<Entity> findAll() {
      List<Entity> entities = entityRepository.findAll();
      entities.forEach(this::populateRelationships);
      return entities;
    }

    public Optional<Entity> findById(String id) {
      Optional<Entity> entityOpt = entityRepository.findById(id);
      if (entityOpt.isPresent()) {
        Entity entity = entityOpt.get();
        populateRelationships(entity);
        return Optional.of(entity);
      }
      return Optional.empty();
    }

    private void populateRelationships(Entity entity) {
      if (entity.getRelatedIds() != null && !entity.getRelatedIds().isEmpty()) {
        List<Related> related = entity
          .getRelatedIds()
          .stream()
          .map(relatedRepository::findById)
          .filter(Optional::isPresent)
          .map(Optional::get)
          .collect(Collectors.toList());
        // 设置瞬时属性以供模板访问
        entity.setRelated(related);
      }
    }
  }

  ```

### 步骤 6.5 — **Spring 安全性集成**（关键用于认证）

- **UserDetailsService 集成模式**：
  ```java
  @Service
  @Transactional
  public class DomainUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;
    private final AuthorityRepository authorityRepository;

    @Override
    public UserDetails loadUserByUsername(String login) {
      log.debug("认证用户: {}", login);

      return userRepository
        .findOneByLogin(login)
        .map(user -> createSpringSecurityUser(login, user))
        .orElseThrow(() -> new UsernameNotFoundException("用户 " + login + " 未找到"));
    }

    private org.springframework.security.core.userdetails.User createSpringSecurityUser(String lowercaseLogin, User user) {
      if (!user.isActivated()) {
        throw new UserNotActivatedException("用户 " + lowercaseLogin + " 未激活");
      }

      // 将字符串权限转换为 GrantedAuthority 对象
      List<GrantedAuthority> grantedAuthorities = user
        .getAuthorities()
        .stream()
        .map(SimpleGrantedAuthority::new)
        .collect(Collectors.toList());

      return new org.springframework.security.core.userdetails.User(user.getLogin(), user.getPassword(), grantedAuthorities);
    }
  }

  ```
- **关键认证要求**：
  - User 实体必须完全可序列化（密码/权限字段不能使用 `@JsonIgnore`）
  - 为 Cosmos DB 兼容性，将权限存储为 `Set<String>`
  - 在 UserDetailsService 中进行字符串权限与 `GrantedAuthority` 对象的转换
  - 添加全面的调试日志以跟踪认证流程
  - 正确处理用户激活/停用状态

#### **模板关系填充模式**

如果模板访问关系属性（例如 `entity.relatedObjects`）：
- 确保实体中存在瞬时字段并具有正确的 getter/setter
- 验证服务层是否在返回实体前填充这些瞬时属性
- 将 `getNrOfXXX()` 方法更新为使用瞬时列表而不是 ID 列表

#### **关键服务层使用检查**

- 确保所有控制器使用服务层而不是直接访问仓库
- 检查服务方法是否在返回实体前填充了所有瞬时属性
- 通过 Web 界面测试所有 CRUD 操作
- 验证数据初始化组件是否正常工作
- 检查模板是否使用 String IDs

### 步骤 9 — **运行时测试和模板兼容性**

#### **关键**：在编译成功后测试运行中的应用程序

- **启动应用程序**：`mvn spring-boot:run`
- **浏览所有页面**以识别运行时错误
- **常见转换后运行时问题**：
  - 模板尝试访问已不存在的属性（例如 `vet.specialties`）
  - 服务层未填充瞬时关系属性
  - 控制器未使用服务层加载关系数据

#### **模板兼容性修复清单**：

- **如果模板访问关系属性**（例如 `entity.relatedObjects`）：
  - 根因：模板访问了被转换为 ID 存储的关系属性
  - 解决方案：在实体中添加瞬时属性并由服务层填充
  - 预防：在转换关系前始终检查模板使用情况

- **`EL1008E` Spring 表达式语言错误**：
  - 根因：服务层未填充瞬时属性
  - 解决方案：验证 `populateRelationships()` 方法是否被调用并正常工作
  - 预防：在实现服务层后测试所有模板导航

- **模板中显示为空/缺失的关系数据**：
  - 根因：控制器绕过服务层或服务未填充关系
  - 解决方案：确保所有控制器方法使用服务层获取实体
  - 预防：从不直接将仓库结果返回给模板

### **常见运行时问题及解决方案**

#### **问题 1：仓库反应式类型转换错误**

**错误**：`ClassCastException: reactor.core.publisher.BlockingIterable cannot be cast to java.util.List`

**根因**：Cosmos 仓库返回反应式类型（`Iterable`），而旧版 JPA 代码期望 `List`

**解决方案**：在仓库方法中正确转换反应式类型：

```java
// 错误 - 直接转换失败
default List<Entity> customFindMethod() {
    return (List<Entity>) this.findAll(); // ClassCastException!
}

// 正确 - 转换 Iterable 为 List
default List<Entity> customFindMethod() {
    return StreamSupport.stream(this.findAll().spliterator(), false)
            .collect(Collectors.toList());
}
```

**需要检查的文件**：

- 所有包含自定义默认方法的仓库接口
- 任何从 Cosmos 仓库调用返回 `List<Entity>` 的方法
- 导入 `java.util.stream.StreamSupport` 和 `java.util.stream.Collectors`

#### **问题 2：Java 17+ 的 BigDecimal 反射问题**

**错误**：`Unable to make field private final java.math.BigInteger java.math.BigDecimal.intVal accessible`

**根因**：Java 17+ 模块系统限制了 BigDecimal 内部字段的反射访问

**解决方案**：

1. **简单情况替换为 Double**：

   ```java
   // 之前：BigDecimal 字段
   private BigDecimal amount;

   // 之后：Double 字段（如果精度要求允许）
   private Double amount;

   ```

2. **使用 String 以满足高精度需求**：

   ```java
   // 存储为 String，按需转换
   private String amount; // 存储 "1500.00"

   public BigDecimal getAmountAsBigDecimal() {
     return new BigDecimal(amount);
   }

   ```

3. **添加 JVM 参数**（如果必须保留 BigDecimal）：
   ```
   --add-opens java.base/java.math=ALL-UNNAMED
   ```

#### **问题 3：健康检查数据库依赖项**

**错误**：应用程序在健康检查中查找已移除的数据库组件而失败

**根因**：在移除 JPA 后，Spring Boot 健康检查仍引用数据库依赖项

**解决方案**：更新健康检查配置：

```yaml
# 在 application.yml 中 - 移除数据库健康检查
management:
  health:
    readiness:
      include: 'ping,diskSpace' # 如果存在则移除 'db'
```

**需要检查的文件**：

- 所有 `application*.yml` 配置文件
- 移除任何数据库特定的健康指示器
- 检查 actuator 端点配置

#### **问题 4：服务中的集合类型转换错误**

**错误**：在将实体关系转换为基于 String 的存储时出现类型不匹配错误

**根因**：实体转换后，服务方法期望不同的集合类型

**解决方案**：更新服务方法以处理新的实体结构：

```java
// 之前：实体关系
public Set<RelatedEntity> getRelatedEntities() {
    return entity.getRelatedEntities(); // 直接实体引用
}

// 之后：基于 String 的实体引用转换
public Set<RelatedEntity> getRelatedEntities() {
    return entity.getRelatedEntityIds()
        .stream()
        .map(relatedRepository::findById)
        .filter(Optional::isPresent)
        .map(Optional::get)
        .collect(Collectors.toSet());
}
```

### **增强的错误解决流程**

#### **常见错误模式及解决方案**：

1. **反应式类型转换错误**：
   - **模式**：`cannot be cast to java.util.List`
   - **修复**：使用 `StreamSupport.stream().collect(Collectors.toList())`
   - **文件**：包含自定义默认方法的仓库接口

2. **BigDecimal 序列化错误**：
   - **模式**：`Unable to make field...BigDecimal.intVal accessible`
   - **修复**：替换为 Double、String 或添加 JVM 模块打开
   - **文件**：实体类、DTO、数据初始化类

3. **健康检查数据库错误**：
   - **模式**：健康检查查找数据库而失败
   - **修复**：从健康检查配置中移除数据库引用
   - **文件**：`application*.yml` 配置文件

4. **集合类型转换错误**：
   - **模式**：实体关系处理中的类型不匹配
   - **修复**：更新服务方法以处理基于 String 的实体引用
   - **文件**：服务类、DTO、实体关系方法

#### **增强的验证清单**：
- [ ] **仓库反应式转换已处理**：无 `List` 转换的 `ClassCastException`
- [ ] **BigDecimal 兼容性已解决**：Java 17+ 序列化正常工作
- [ ] **健康检查已更新**：健康配置中无数据库依赖
- [ ] **服务层集合处理**：基于 String 的实体引用正常工作
- [ ] **数据初始化完成**：日志中出现 "Data seeding completed" 消息
- [ ] **应用程序完全启动**：前端和后端均可访问
- [ ] **认证正常工作**：无需序列化错误即可登录
- [ ] **所有实体操作功能正常**：通过 UI 进行所有实体操作

## **快速参考：常见迁移后修复**

### **需要检查的运行时问题**

1. **仓库集合转换**：
   ```java
   // 修复任何返回集合的仓库方法：
   default List<Entity> customFindMethod() {
       return StreamSupport.stream(this.findAll().spliterator(), false)
               .collect(Collectors.toList());
   }

2. **BigDecimal 兼容性（Java 17+）**：

   ```java
   // 替换 BigDecimal 字段为其他类型：
   private Double amount; // 或 String 以满足高精度需求

   ```

3. **健康检查配置**：
   ```yaml
   # 从健康检查中移除数据库依赖：
   management:
     health:
       readiness:
         include: 'ping,diskSpace'
   ```

### **认证转换模式**

- **从需要 Cosmos DB 持久化的字段移除 `@JsonIgnore`**
- **将复杂对象存储为简单类型**（例如权限存储为 `Set<String>`）
- **在服务/仓库层之间进行简单类型与复杂类型的转换**
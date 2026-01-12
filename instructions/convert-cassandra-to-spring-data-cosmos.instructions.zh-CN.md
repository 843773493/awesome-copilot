

---
description: '将Spring Boot Cassandra应用程序转换为使用Azure Cosmos DB与Spring Data Cosmos的逐步指南'
applyTo: '**/*.java,**/pom.xml,**/build.gradle,**/application*.properties,**/application*.yml,**/application*.conf'
---

# 全面指南：将Spring Boot Cassandra应用程序转换为使用Azure Cosmos DB与Spring Data Cosmos（spring-data-cosmos）

## 适用范围

本指南适用于：
- ✅ Spring Boot 2.x - 3.x 应用程序（包括响应式和非响应式）
- ✅ 基于Maven和Gradle的项目
- ✅ 使用Spring Data Cassandra、Cassandra DAO或DataStax驱动程序的应用程序
- ✅ 项目中使用或不使用Lombok
- ✅ 基于UUID或基于字符串的实体标识符
- ✅ 同步和响应式（Spring WebFlux）应用程序

本指南不涵盖：
- ❌ 非Spring框架（Jakarta EE、Micronaut、Quarkus、纯Java）
- ❌ 复杂的Cassandra功能（物化视图、UDTs、计数器、自定义类型）
- ❌ 批量数据迁移（仅代码转换 - 数据必须单独迁移）
- ❌ Cassandra特定功能，如轻量级事务（LWT）或跨分区的批量操作

## 概述

本指南提供了将响应式Spring Boot应用程序从Apache Cassandra转换为使用Azure Cosmos DB的逐步说明。它涵盖了在实际转换过程中遇到的所有主要问题及其解决方案。

## 先决条件

- Java 11或更高版本（Spring Boot 3.x需要Java 17+）
- 安装并认证了Azure CLI（`az login`）用于本地开发
- 在Azure门户中创建了Azure Cosmos DB账户
- Maven 3.6+ 或 Gradle 6+（根据项目选择）
- 对于Gradle项目中的Spring Boot 3.x：确保JAVA_HOME环境变量指向Java 17+
- 对应用程序的数据模型和查询模式有基本了解

## Azure Cosmos DB数据库设置

**关键点**：在运行应用程序之前，请确保Cosmos DB账户中已存在数据库。

### 选项1：手动创建数据库（推荐首次运行）
1. 进入Azure门户 → 您的Cosmos DB账户
2. 导航到“数据资源管理器”
3. 点击“新建数据库”
4. 输入与应用程序配置匹配的数据库名称（检查`application.properties`或`application.yml`中配置的数据库名称）
5. 选择吞吐量设置（根据需求选择手动或自动扩展）
   - 开发/测试环境建议从手动设置400 RU/s开始
   - 生产环境工作负载在流量变化时使用自动扩展
6. 点击“确定”

### 选项2：自动创建
Spring Data Cosmos可以在首次连接时自动创建数据库，但需要：
- 正确的RBAC权限（Cosmos DB内置数据贡献者角色）
- 权限不足时可能导致创建失败

### 容器（集合）创建
容器将在应用程序启动时由Spring Data Cosmos自动创建，使用实体中的`@Container`注解设置。除非您需要配置特定吞吐量或索引策略，否则无需手动创建容器。

## 与Azure Cosmos DB的认证

### 推荐使用DefaultAzureCredential
`DefaultAzureCredential`认证方法是开发和生产环境的推荐方式：

**工作原理**：
1. 按顺序尝试多个凭证来源：
   - 环境变量
   - 工作负载身份（用于AKS）
   - 管理身份（用于Azure虚拟机/应用服务）
   - Azure CLI（`az login`）
   - Azure PowerShell
   - Azure开发者CLI

**本地开发设置**：
```bash
# 通过Azure CLI登录
az login

# 应用程序将自动使用您的CLI凭证
```

**配置**（无需密钥属性）：
```java
@Bean
public CosmosClientBuilder getCosmosClientBuilder() {
    return new CosmosClientBuilder()
        .endpoint(uri)
        .credential(new DefaultAzureCredentialBuilder().build());
}
```

**属性文件**（`application-cosmos.properties`或`application.properties`）：
```properties
azure.cosmos.uri=https://<your-cosmos-account-name>.documents.azure.com:443/
azure.cosmos.database=<your-database-name>
# 使用DefaultAzureCredential时无需密钥属性
azure.cosmos.populate-query-metrics=false
```

**注意**：请将`<your-cosmos-account-name>`和`<your-database-name>`替换为您的实际值。

### 所需的RBAC权限
使用`DefaultAzureCredential`时，您的Azure身份需要适当的RBAC权限：

**常见启动错误**：
```
请求被授权阻止：principal [xxx] 缺少执行操作 [Microsoft.DocumentDB/databaseAccounts/sqlDatabases/write] 所需的RBAC权限
```

**解决方案**：分配“Cosmos DB内置数据贡献者”角色：
```bash
# 获取您的用户对象ID
PRINCIPAL_ID=$(az ad signed-in-user show --query id -o tsv)

# 分配角色（将<resource-group>替换为您的资源组）
az cosmosdb sql role assignment create \
  --account-name your-cosmos-account \
  --resource-group <resource-group> \
  --scope "/" \
  --principal-id $PRINCIPAL_ID \
  --role-definition-name "Cosmos DB内置数据贡献者"
```

**替代方案**：如果您使用`az login`登录，且您是Cosmos DB账户的所有者/贡献者，则您的账户应已具备权限。

### 基于密钥的认证（仅限本地模拟器）
仅在本地模拟器中使用基于密钥的认证：

```java
@Bean
public CosmosClientBuilder getCosmosClientBuilder() {
    // 仅用于本地模拟器
    if (key != null && !key.isEmpty()) {
        return new CosmosClientBuilder()
            .endpoint(uri)
            .key(key);
    }
    // 生产环境：使用DefaultAzureCredential
    return new CosmosClientBuilder()
        .endpoint(uri)
        .credential(new DefaultAzureCredentialBuilder().build());
}
```

## 重要经验教训

### Java版本要求（Spring Boot 3.x）
**问题**：Spring Boot 3.0+需要Java 17或更高版本。使用Java 11会导致构建失败。
**错误**：
```
找不到与org.springframework.boot:spring-boot-gradle-plugin:3.0.5匹配的版本。不兼容，因为此组件声明与Java 17兼容，而消费者需要与Java 11兼容的组件
```

**解决方案**：
```bash
# 检查Java版本
java -version

# 设置JAVA_HOME指向Java 17+
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64  # Linux
# 或
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home  # macOS

# 验证
echo $JAVA_HOME
```

**对于Gradle项目**，始终使用正确的JAVA_HOME：
```bash
export JAVA_HOME=/path/to/java-17
./gradlew clean build
./gradlew bootRun
```

### Gradle特定问题

#### 问题1：旧配置文件冲突
**问题**：在删除依赖项后，旧的Cassandra特定文件会导致编译错误。
**解决方案**：系统性地删除所有Cassandra特定文件：
```bash
# 识别并删除旧的DAO文件
find . -name "*Dao.java" -o -name "*DAO.java"
# 删除：OwnerReactiveDao、PetReactiveDao、VetReactiveDao、VisitReactiveDao

# 识别并删除Cassandra映射器文件
find . -name "*Mapper.java" -o -name "EntityToOwnerMapper.java"
# 删除：EntityToOwnerMapper、EntityToPetMapper、EntityToVetMapper、EntityToVisitMapper

# 识别并删除旧配置
find . -name "*CassandraConfig.java" -o -name "CassandraConfiguration.java"
# 删除：CassandraConfiguration.java

# 识别Cassandra特定的测试工具
find . -name "MockReactiveResultSet.java"
# 删除：MockReactiveResultSet.java（Cassandra特定测试工具）
```

#### 问题2：Repository findAllById返回Iterable
**问题**：CosmosRepository的`findAllById()`返回`Iterable<Entity>`，而非`List<Entity>`。直接调用`.stream()`会失败：
```
错误：找不到符号
  符号：   方法 stream()
  位置：接口 Iterable<YourEntity>
```

**解决方案**：正确处理Iterable：
```java
// 错误 - Iterable没有stream()方法
var entities = repository.findAllById(ids).stream()...

// 正确 - 选项1：使用forEach填充集合
Iterable<YourEntity> entitiesIterable = repository.findAllById(ids);
Map<String, YourEntity> entityMap = new HashMap<>();
entitiesIterable.forEach(entity -> entityMap.put(entity.getId(), entity));

// 正确 - 选项2：先转换为List
List<YourEntity> entities = new ArrayList<>();
repository.findAllById(ids).forEach(entities::add);

// 正确 - 选项3：使用StreamSupport（Java 8+）
List<YourEntity> entities = StreamSupport.stream(
    repository.findAllById(ids).spliterator(), false)
    .collect(Collectors.toList());
```

### package-info.java的javax.annotation问题
**问题**：`package-info.java`使用`javax.annotation.ParametersAreNonnullByDefault`会导致Java 11+的编译错误：
```
错误：找不到符号
import javax.annotation.ParametersAreNonnullByDefault;
```

**解决方案**：删除或简化`package-info.java`文件：
```java
// 简化版本 - 仅保留包声明
package com.your.package;
```

### 实体构造器问题
**问题**：使用Lombok的`@NoArgsConstructor`与手动构造器会导致重复构造器编译错误。
**解决方案**：选择一种方法：
- 选项1：删除`@NoArgsConstructor`并保留手动构造器
- 选项2：删除手动构造器并依赖Lombok注解
- **最佳实践**：对于需要初始化逻辑的Cosmos实体（如设置分区键），删除`@NoArgsConstructor`并仅使用手动构造器。

### 业务对象构造器移除
**问题**：从实体类中移除`@AllArgsConstructor`或自定义构造器会破坏使用这些构造器的现有代码。
**影响**：映射工具、数据播种器和测试文件将无法编译。
**解决方案**：
- 移除或修改构造器后，搜索所有使用这些构造器的文件
- 使用默认构造器 + 设置器模式替换构造器调用：
  ```java
  // 之前 - 使用所有参数构造器
  MyEntity entity = new MyEntity(id, field1, field2, field3);

  // 之后 - 使用默认构造器 + 设置器
  MyEntity entity = new MyEntity();
  entity.setId(id);
  entity.setField1(field1);
  entity.setField2(field2);
  entity.setField3(field3);
  ```

### 测试文件更新
**问题**：测试文件引用旧的Cassandra DAO并使用UUID构造器。
**需要更新的关键文件**：
1. **单元测试**：
   ```java
   @ExtendWith(MockitoExtension.class)
   class EntityReactiveServicesTest {

       @Mock
       private EntityCosmosRepository entityRepository; // 更新为Cosmos仓库

       @InjectMocks
       private EntityReactiveServices entityService;

       @Test
       void testFindById() {
           String entityId = "test-entity-id"; // 从UUID改为String
           EntityName mockEntity = new EntityName();
           mockEntity.setId(entityId);

           when(entityRepository.findById(entityId)).thenReturn(Mono.just(mockEntity));

           StepVerifier.create(entityService.findById(entityId))
               .expectNext(mockEntity)
               .verifyComplete();
       }
   }
   ```

2. **集成测试**：
   - 更新测试数据设置以使用String ID
   - 将Cassandra测试容器替换为Cosmos DB模拟器（如有）
   - 将测试查询更新为使用Cosmos SQL语法而不是CQL

3. **无测试的应用程序**：
   - 考虑添加基本测试以验证转换是否正确
   - 重点测试ID转换和基本的CRUD操作

## 常见问题与解决方案

#### 问题1：缺少reactor.core.publisher.Sinks的NoClassDefFoundError
**问题**：Azure Identity库需要较新的Reactor Core版本
**错误**：`java.lang.NoClassDefFoundError: reactor/core/publisher/Sinks`
**根本原因**：Spring Boot 2.3.x使用较旧的reactor-core，不包含Sinks API
**解决方案**：在dependencyManagement中添加reactor-core版本覆盖（见步骤1）

#### 问题2：Netty Epoll方法的NoSuchMethodError
**问题**：Spring Boot Netty版本与Azure Cosmos需求不匹配
**错误**：`java.lang.NoSuchMethodError: 'boolean io.netty.channel.epoll.Epoll.isTcpFastOpenClientSideAvailable()'`
**根本原因**：Spring Boot 2.3.x使用Netty 4.1.51.Final，Azure需要更新的方法
**解决方案**：在dependencyManagement中添加netty-bom版本覆盖（见步骤1）

#### 问题3：SSL上下文的NoSuchMethodError
**问题**：Netty TLS原生库版本不匹配
**错误**：`java.lang.NoSuchMethodError: 'boolean io.netty.internal.tcnative.SSLContext.setCurvesList(long, java.lang.String[])'`
**根本原因**：netty-tcnative版本与升级后的Netty不兼容
**解决方案**：在dependencyManagement中添加netty-tcnative-boringssl-static版本覆盖（见步骤1）

#### 问题4：ReactiveCosmosRepository bean未创建
**问题**：缺少`@EnableReactiveCosmosRepositories`注解
**错误**：`No qualifying bean of type 'ReactiveCosmosRepository' available`
**根本原因**：仅使用`@EnableCosmosRepositories`不会创建响应式仓库bean
**解决方案**：在配置中添加`@EnableCosmosRepositories`和`@EnableReactiveCosmosRepositories`

#### 问题5：仓库接口编译错误
**问题**：使用`CosmosRepository`而非`ReactiveCosmosRepository`
**错误**：`Cannot resolve method 'findAll()' in 'CosmosRepository'`
**根本原因**：`CosmosRepository`返回`Iterable`，而非`Flux`
**解决方案**：将所有仓库接口改为继承`ReactiveCosmosRepository<Entity, String>`

#### 问题6：服务层响应式类型不匹配
**问题**：服务方法返回`Iterable`或`Optional`而非`Flux`或`Mono`
**错误**：`Required type: Flux<Entity> Provided: Iterable<Entity>`
**根本原因**：仓库方法返回响应式类型，服务必须匹配
**解决方案**：更新所有服务方法签名以返回`Flux`或`Mono`

#### 问题7：使用DefaultAzureCredential时的认证失败
**问题**：`DefaultAzureCredential`找不到凭证
**错误**：`All credentials in the chain are unavailable`或特定凭证不可用消息
**根本原因**：没有可用的Azure凭证来源

**解决方案**：
1. **本地开发**：确保运行`az login`
   ```bash
   az login

   # 验证登录
   az account show
   ```

2. **Azure托管应用程序**：确保启用了管理身份并具有适当的RBAC权限

3. **检查凭证链顺序**：`DefaultAzureCredential`尝试顺序：
   - 环境变量 → 工作负载身份 → 管理身份 → Azure CLI → Azure PowerShell → Azure开发者CLI

#### 问题8：数据库未找到错误
**问题**：应用程序启动失败，提示数据库未找到
**错误**：`Database 'your-database-name' not found`或`Resource Not Found`
**根本原因**：数据库在Cosmos DB账户中不存在

**解决方案**：在首次运行前创建数据库（见数据库设置部分）：
```bash
# 通过Azure CLI创建
az cosmosdb sql database create \
  --account-name your-cosmos-account \
  --name your-database-name \
  --resource-group your-resource-group

# 或通过Azure门户（推荐首次设置）
# 门户 → Cosmos DB → 数据资源管理器 → 新建数据库
```

**注意**：容器（集合）将根据实体`@Container`注解自动创建，但根据您的RBAC权限，数据库本身可能需要预先存在。

#### 问题9：RBAC权限错误
**问题**：应用程序因权限被拒绝而失败
**错误**：
```
请求被授权阻止：principal [xxx] 缺少执行操作 [Microsoft.DocumentDB/databaseAccounts/sqlDatabases/write] 所需的RBAC权限
```

**根本原因**：您的Azure身份缺少所需的Cosmos DB权限

**解决方案**：分配“Cosmos DB内置数据贡献者”角色：
```bash
# 获取资源组
RESOURCE_GROUP=$(az cosmosdb show --name your-cosmos-account --query resourceGroup -o tsv 2>/dev/null)

# 如果上述命令失败，请列出所有Cosmos账户以找到它
az cosmosdb list --query "[?name=='your-cosmos-account'].{name:name, resourceGroup:resourceGroup}" -o table

# 分配角色
az cosmosdb sql role assignment create \
  --account-name your-cosmos-account \
  --resource-group $RESOURCE_GROUP \
  --scope "/" \
  --principal-id $(az ad signed-in-user show --query id -o tsv) \
  --role-definition-name "Cosmos DB内置数据贡献者"
```

**替代方案**：门户 → Cosmos DB → 访问控制（IAM） → 添加角色分配 → “Cosmos DB内置数据贡献者”

#### 问题10：分区键策略差异
**问题**：Cassandra的聚类键不能直接映射到Cosmos的分区键
**错误**：跨分区查询或性能不佳
**根本原因**：不同的数据分布策略
**解决方案**：根据查询模式选择合适的分区键，通常是最常查询的字段

#### 问题10：UUID到String的转换问题
**问题**：测试文件和控制器仍使用UUID类型
**错误**：`无法将UUID转换为String`或类型不匹配错误
**根本原因**：并非所有UUID引用都已转换为String
**解决方案**：系统性地搜索并替换所有UUID引用为String

### 数据播种（如果适用）

#### 实现数据填充

**如果您的应用程序需要初始数据**：

```java
@Component
public class DataSeeder implements CommandLineRunner {

    private final EntityCosmosRepository entityRepository;

    @Override
    public void run(String... args) throws Exception {
        if (entityRepository.count().block() == 0) {
            // 播种初始数据
            EntityName entity = new EntityName();
            entity.setFieldName("示例值");
            entity.setAnotherField("示例数据");

            entityRepository.save(entity).block();
        }
    }
}
```

**如果您的应用程序有现有数据迁移需求**：
- 创建迁移脚本将数据从Cassandra导出并导入到Cosmos DB
- 考虑数据转换需求（UUID到String转换）
- 规划Cassandra与Cosmos数据模型之间的任何模式差异

**如果您的应用程序不需要数据播种**：
- 跳过此步骤并继续验证

### 应用程序配置文件

#### 更新`application.yml`以启用Cosmos配置
```yaml
spring:
  profiles:
    active: cosmos

---
spring:
  profiles: cosmos

azure:
  cosmos:
    uri: ${COSMOS_URI:https://your-account.documents.azure.com:443/}
    database: ${COSMOS_DATABASE:your-database}
```

## 验证步骤

1. **编译检查**：`mvn compile`应成功无错误
2. **测试检查**：`mvn test`应通过更新后的测试用例
3. **运行时检查**：应用程序应成功启动且无版本冲突
4. **连接检查**：应用程序应成功连接到Cosmos DB
5. **数据检查**：通过API进行CRUD操作应正常工作
6. **UI检查**：前端应显示来自Cosmos DB的数据

## 最佳实践

1. **ID策略**：始终使用String ID而非UUID
2. **分区键**：根据查询模式和数据分布选择分区键
3. **查询设计**：使用`@Query`注解进行自定义查询，而非方法命名约定
4. **响应式编程**：在整个服务层中坚持使用Flux/Mono模式
5. **版本管理**：始终在Spring Boot 2.x项目中包含依赖项版本覆盖
6. **测试**：更新所有测试文件以使用String ID和模拟Cosmos仓库
7. **认证**：使用`DefaultAzureCredential`进行生产就绪认证

## 故障排除命令

```bash
# 检查依赖项和版本冲突
mvn dependency:tree | grep -E "(reactor|netty|cosmos)"

# 验证特定的有问题的依赖项
mvn dependency:tree | grep "reactor-core"
mvn dependency:tree | grep "reactor-netty"
mvn dependency:tree | grep "netty-tcnative"

# 测试连接
curl http://localhost:8080/api/entities

# 检查Azure登录状态
az account show

# 清理并重新构建（通常修复依赖项问题）
mvn clean compile

# 以调试日志模式运行以解决运行时问题
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005"

# 检查应用程序日志中的版本冲突
grep -E "(NoSuchMethodError|NoClassDefFoundError|reactor|netty)" application.log
```

## 典型错误序列与解决方法

基于实际转换经验，您可能会按以下顺序遇到这些错误：

### **阶段1：编译错误**
1. **缺少依赖项** → 添加`azure-spring-data-cosmos`和`azure-identity`
2. **配置类错误** → 创建`CosmosConfiguration`（如果尚未存在）
3. **实体注解错误** → 将`@Table`转换为`@Container`等
4. **仓库接口错误** → 将仓库接口更改为`ReactiveCosmosRepository`（如果使用仓库模式）

### **阶段2：Bean创建错误**
5. **"No qualifying bean of type ReactiveCosmosRepository"** → 添加`@EnableReactiveCosmosRepositories`
6. **服务层类型不匹配** → 将`Iterable`改为`Flux`，`Optional`改为`Mono`（如果使用服务层）

### **阶段3：运行时版本冲突**（最复杂）
7. **NoClassDefFoundError: reactor.core.publisher.Sinks** → 添加`reactor-core` 3.4.32版本覆盖
8. **NoSuchMethodError: Epoll.isTcpFastOpenClientSideAvailable** → 添加`netty-bom` 4.1.101.Final版本覆盖
9. **NoSuchMethodError: SSLContext.setCurvesList** → 添加`netty-tcnative-boringssl-static` 2.0.62.Final版本覆盖

### **阶段4：认证与连接**
10. **ManagedIdentityCredential认证不可用** → 运行`az login --use-device-code`
11. **应用程序成功启动** → 已连接到Cosmos DB！

**关键点**：按顺序解决这些问题。不要跳过前面的阶段，因为每个阶段的解决是后续阶段的前提。

## 性能考虑

1. **分区策略**：设计分区键以均匀分布负载
2. **查询优化**：尽可能避免跨分区查询，使用索引
3. **连接池**：Cosmos客户端自动管理连接
4. **请求单位**：监控RU消耗并根据需要调整吞吐量
5. **批量操作**：使用批量操作进行多个文档更新

本指南涵盖了从Cassandra转换到Cosmos DB的所有主要方面，包括实际场景中遇到的所有版本冲突和认证问题。
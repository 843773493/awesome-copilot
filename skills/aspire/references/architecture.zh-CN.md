# 架构 — 深入解析

本参考文档涵盖 Aspire 的内部架构：DCP 引擎、资源模型、服务发现、网络、遥测以及事件系统。

---

## 开发者控制平面（DCP）

DCP 是 Aspire 在 `aspire run` 模式下使用的 **运行时引擎**。关键信息如下：

- 使用 **Go** 编写（非 .NET）
- 提供一个 **兼容 Kubernetes 的 API 服务器**（仅限本地，非真实 K8s 集群）
- 管理资源生命周期：创建、启动、健康检查、停止、重启
- 通过本地容器运行时（Docker、Podman、Rancher）运行容器
- 以原生操作系统进程方式运行可执行文件
- 通过代理层处理网络，自动分配端口
- 为 Aspire 面板的实时数据提供基础支持

### DCP 与 Kubernetes 的对比

| 特性 | DCP（本地开发） | Kubernetes（生产环境） |
|---|---|---|
| API | 兼容 Kubernetes | 完整的 Kubernetes API |
| 作用范围 | 单机 | 集群 |
| 网络 | 本地代理，自动端口 | 服务网格，入口网关 |
| 存储 | 本地卷 | PVCs，云存储 |
| 目的 | 开发者内环 | 生产部署 |

兼容 Kubernetes 的 API 表示 Aspire 理解相同的资源抽象，但 DCP **不是** 一个 Kubernetes 发行版 — 它是一个轻量级的本地运行时。

---

## 资源模型

Aspire 中的所有内容都是 **资源**。资源模型具有层次结构：

### 类型层级

```
IResource（接口）
└── Resource（抽象基类）
    ├── ProjectResource          — .NET 项目引用
    ├── ContainerResource        — Docker/OCI 容器
    ├── ExecutableResource       — 原生进程（多语言应用）
    ├── ParameterResource        — 配置值或密钥
    └── 基础设施资源
        ├── RedisResource
        ├── PostgresServerResource
        ├── MongoDBServerResource
        ├── SqlServerResource
        ├── RabbitMQServerResource
        ├── KafkaServerResource
        └── ...（每个集成对应一个）
```

### 资源属性

每个资源都有以下属性：
- **名称** — 在 AppHost 中的唯一标识符
- **状态** — 生命周期状态（Starting、Running、FailedToStart、Stopping、Stopped 等）
- **注解** — 附加到资源的元数据
- **端点** — 资源暴露的网络端点
- **环境变量** — 注入到进程/容器中

### 注解

注解是附加到资源的元数据集合。常见的内置注解：

| 注解 | 用途 |
|---|---|
| `EndpointAnnotation` | 定义 HTTP/HTTPS/TCP 端点 |
| `EnvironmentCallbackAnnotation` | 延迟环境变量解析 |
| `HealthCheckAnnotation` | 健康检查配置 |
| `ContainerImageAnnotation` | Docker 镜像详情 |
| `VolumeAnnotation` | 卷挂载配置 |
| `CommandLineArgsCallbackAnnotation` | 动态命令行参数 |
| `ManifestPublishingCallbackAnnotation` | 自定义发布行为 |

### 资源生命周期状态

```
NotStarted → Starting → Running → Stopping → Stopped
                 ↓                     ↓
          FailedToStart           RuntimeUnhealthy
                                       ↓
                                  Restarting → Running
```

### 有向无环图（DAG）

资源形成依赖图。Aspire 以拓扑顺序启动资源：

```
PostgreSQL ──→ API ──→ Frontend
Redis ────────↗
RabbitMQ ──→ Worker
```

1. PostgreSQL、Redis 和 RabbitMQ 首先启动（无依赖）
2. API 在 PostgreSQL 和 Redis 健康后启动
3. Frontend 在 API 健康后启动
4. Worker 在 RabbitMQ 健康后启动

`.WaitFor()` 在依赖边添加健康检查门控。若不使用，依赖项会启动但下游资源不会等待其健康。

---

## 服务发现

Aspire 为每个资源注入环境变量，以便服务之间可以相互发现。无需服务注册表或 DNS — 它是纯粹的环境变量注入。

### 连接字符串

对于数据库、缓存和消息代理：

```
ConnectionStrings__<resource-name>=<connection-string>
```

示例：
```
ConnectionStrings__cache=localhost:6379
ConnectionStrings__catalog=Host=localhost;Port=5432;Database=catalog;Username=postgres;Password=...
ConnectionStrings__messaging=amqp://guest:guest@localhost:5672
```

### 服务端点

对于 HTTP/HTTPS 服务：

```
services__<resource-name>__<scheme>__0=<url>
```

示例：
```
services__api__http__0=http://localhost:5234
services__api__https__0=https://localhost:7234
services__ml__http__0=http://localhost:8000
```

### `.WithReference()` 的工作原理

```csharp
var redis = builder.AddRedis("cache");
var api = builder.AddProject<Projects.Api>("api")
    .WithReference(redis);
```

此操作会执行以下步骤：
1. 向 API 的环境变量中添加 `ConnectionStrings__cache=localhost:<auto-port>`
2. 在 DAG 中创建依赖边（API 依赖 Redis）
3. 在 API 服务中，`builder.Configuration.GetConnectionString("cache")` 返回连接字符串

### 跨语言服务发现

所有语言使用相同的环境变量模式：

| 语言 | 如何读取 |
|---|---|
| C# | `builder.Configuration.GetConnectionString("cache")` |
| Python | `os.environ["ConnectionStrings__cache"]` |
| JavaScript | `process.env.ConnectionStrings__cache` |
| Go | `os.Getenv("ConnectionStrings__cache")` |
| Java | `System.getenv("ConnectionStrings__cache")` |
| Rust | `std::env::var("ConnectionStrings__cache")` |

---

## 网络

### 代理架构

在 `aspire run` 模式下，DCP 为每个暴露的端点运行一个反向代理：

```
浏览器 → 代理（自动分配端口） → 实际服务（目标端口）
```

- **端口**（外部端口） — 由 DCP 自动分配，除非手动覆盖
- **targetPort** — 服务实际监听的端口
- 所有服务间通信均通过代理进行可观测性分析

```csharp
// 让 DCP 自动分配外部端口，服务监听在 8000
builder.AddPythonApp("ml", "../ml", "main.py")
    .WithHttpEndpoint(targetPort: 8000);

// 固定外部端口为 3000
builder.AddViteApp("web", "../frontend")
    .WithHttpEndpoint(port: 3000, targetPort: 5173);
```

### 端点类型

```csharp
// HTTP 端点
.WithHttpEndpoint(port?, targetPort?, name?)

// HTTPS 端点
.WithHttpsEndpoint(port?, targetPort?, name?)

// 通用端点（TCP、自定义协议）
.WithEndpoint(port?, targetPort?, scheme?, name?, isExternal?)

// 标记端点为外部可访问（用于部署）
.WithExternalHttpEndpoints()
```

---

## 遥测（OpenTelemetry）

Aspire 会自动为 .NET 服务配置 OpenTelemetry。对于非 .NET 服务，需手动配置 OpenTelemetry，指向 DCP 收集器。

### 自动配置的内容（.NET 服务）

- **分布式追踪** — HTTP 客户端/服务端跨度、数据库跨度、消息跨度
- **指标** — 运行时指标、HTTP 指标、自定义指标
- **结构化日志** — 与追踪上下文相关联的日志
- **导出器** — 指向 Aspire 面板的 OTLP 导出器

### 配置非 .NET 服务

DCP 暴露了一个 OTLP 端点。在非 .NET 服务中设置这些环境变量：

```
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_SERVICE_NAME=<your-service-name>
```

Aspire 会通过 `.WithReference()` 自动注入 `OTEL_EXPORTER_OTLP_ENDPOINT`，指向面板收集器。

### `ServiceDefaults` 模式

`ServiceDefaults` 项目是一个共享配置库，用于标准化：
- OpenTelemetry 设置（追踪、指标、日志）
- 健康检查端点（`/health`、`/alive`）
- 韧性策略（重试、断路器通过 Polly 实现）

```csharp
// 在每个 .NET 服务的 Program.cs 中
builder.AddServiceDefaults();   // 添加 OTel、健康检查、韧性和
// ... 其他服务配置 ...
app.MapDefaultEndpoints();      // 映射 /health 和 /alive
```

---

## 健康检查

### 内置健康检查

每个集成会在客户端自动添加健康检查：
- Redis：`PING` 命令
- PostgreSQL：`SELECT 1`
- MongoDB：`ping` 命令
- RabbitMQ：连接检查
- 等等

### `WaitFor` 与 `WithReference`

```csharp
// WithReference：连接字符串 + 创建依赖边
// （下游资源可能在依赖项健康前启动）
.WithReference(db)

// WaitFor：健康检查门控 — 下游资源在依赖项健康前不会启动
.WaitFor(db)

// 典型模式：两者结合使用
.WithReference(db).WaitFor(db)
```

### 自定义健康检查

```csharp
var api = builder.AddProject<Projects.Api>("api")
    .WithHealthCheck("ready", "/health/ready")
    .WithHealthCheck("live", "/health/live");
```

---

## 事件系统

AppHost 支持用于响应资源状态变化的生命周期事件：

```csharp
builder.Eventing.Subscribe<ResourceReadyEvent>("api", (evt, ct) =>
{
    // 当 "api" 资源变为健康时触发
    Console.WriteLine($"API 在 {evt.Resource.Name} 处准备就绪");
    return Task.CompletedTask;
});

builder.Eventing.Subscribe<BeforeResourceStartedEvent>("db", async (evt, ct) =>
{
    // 在 DB 资源被标记为启动前运行数据库迁移
    await RunMigrations();
});
```

### 可用事件

| 事件 | 触发时机 |
|---|---|
| `BeforeResourceStartedEvent` | 资源启动前 |
| `ResourceReadyEvent` | 资源健康且就绪 |
| `ResourceStateChangedEvent` | 任何状态转换 |
| `BeforeStartEvent` | 整个应用程序启动前 |
| `AfterEndpointsAllocatedEvent` | 所有端口分配完成后 |

---

## 配置

### 参数

```csharp
// 普通参数
var apiKey = builder.AddParameter("api-key");

// 密钥参数（运行时提示，不记录日志）
var dbPassword = builder.AddParameter("db-password", secret: true);

// 在资源中使用参数
var api = builder.AddProject<Projects.Api>("api")
    .WithEnvironment("API_KEY", apiKey);

var db = builder.AddPostgres("db", password: dbPassword);
```

### 配置源

参数将按照以下优先级顺序从以下来源解析：
1. 命令行参数
2. 环境变量
3. 用户密钥（`dotnet user-secrets`）
4. `appsettings.json` / `appsettings.{Environment}.json`
5. 交互式提示（`aspire run` 期间的密钥）

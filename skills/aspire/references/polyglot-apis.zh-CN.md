# 多语言API — 全面参考指南

Aspire 支持 10+ 种语言/运行时。AppHost 始终是 .NET，但编排的工作负载可以是任何语言。每种语言都有一个托管方法，该方法返回一个资源，您将其连接到依赖图中。

---

## 托管模型差异

| 模型 | 资源类型 | 如何运行 | 示例 |
|---|---|---|---|
| **项目** | `ProjectResource` | .NET 项目引用，由 SDK 构建 | `AddProject<T>()` |
| **容器** | `ContainerResource` | Docker/OCI 镜像 | `AddContainer()`，`AddRedis()`，`AddPostgres()` |
| **可执行文件** | `ExecutableResource` | 原生操作系统进程 | `AddExecutable()`，所有 `Add*App()` 多语言方法 |

所有多语言 `Add*App()` 方法在内部都会创建 `ExecutableResource` 实例。它们不需要在 AppHost 侧安装目标语言的 SDK，只需确保开发机器上已安装工作负载的运行时。

---

## 官方（微软维护）

### .NET / C#

```csharp
builder.AddProject<Projects.MyApi>("api")
```

**链式方法：**
- `.WithHttpEndpoint(port?, targetPort?, name?)` — 暴露 HTTP 端点
- `.WithHttpsEndpoint(port?, targetPort?, name?)` — 暴露 HTTPS 端点
- `.WithEndpoint(port?, targetPort?, scheme?, name?)` — 通用端点
- `.WithReference(resource)` — 连接依赖项（连接字符串或服务发现）
- `.WithReplicas(count)` — 运行多个实例
- `.WithEnvironment(key, value)` — 设置环境变量
- `.WithEnvironment(callback)` — 通过回调设置环境变量（延迟解析）
- `.WaitFor(resource)` — 直到依赖项健康才启动
- `.WithExternalHttpEndpoints()` — 标记端点为可外部访问
- `.WithOtlpExporter()` — 配置 OpenTelemetry 导出器
- `.PublishAsDockerFile()` — 覆盖发布行为为 Dockerfile

### Python

```csharp
// 标准 Python 脚本
builder.AddPythonApp("service", "../python-service", "main.py")

// Uvicorn ASGI 服务器（FastAPI、Starlette 等）
builder.AddUvicornApp("fastapi", "../fastapi-app", "app:app")
```

**`AddPythonApp(name, projectDirectory, scriptPath, args?)`**

链式方法：
- `.WithHttpEndpoint(port?, targetPort?, name?)` — 暴露 HTTP
- `.WithVirtualEnvironment(path?)` — 使用虚拟环境（默认：`.venv`）
- `.WithPipPackages(packages)` — 启动时安装 pip 包
- `.WithReference(resource)` — 连接依赖项
- `.WithEnvironment(key, value)` — 设置环境变量
- `.WaitFor(resource)` — 等待依赖项健康状态

**`AddUvicornApp(name, projectDirectory, appModule, args?)`**

链式方法（与 `AddJavaScriptApp` 相同，此外还有）：
- `.WithHttpEndpoint(port?, targetPort?, name?)` — 暴露 HTTP
- `.WithVirtualEnvironment(path?)` — 使用虚拟环境
- `.WithReference(resource)` — 连接依赖项
- `.WithEnvironment(key, value)` — 设置环境变量
- `.WaitFor(resource)` — 等待依赖项健康状态

**Python 服务发现：** 环境变量会自动注入。使用 `os.environ` 读取：
```python
import os
redis_conn = os.environ["ConnectionStrings__cache"]
api_url = os.environ["services__api__http__0"]
```

### JavaScript / TypeScript

```csharp
// 通用 JavaScript 应用（npm start）
builder.AddJavaScriptApp("frontend", "../web-app")

// Vite 开发服务器
builder.AddViteApp("spa", "../vite-app")

// Node.js 脚本
builder.AddNodeApp("worker", "server.js", "../node-worker")
```

**`AddJavaScriptApp(name, workingDirectory)`**

链式方法：
- `.WithHttpEndpoint(port?, targetPort?, name?)` — 暴露 HTTP
- `.WithNpmPackageInstallation()` — 启动前运行 `npm install`
- `.WithReference(resource)` — 连接依赖项
- `.WithEnvironment(key, value)` — 设置环境变量
- `.WaitFor(resource)` — 等待依赖项健康状态

**`AddViteApp(name, workingDirectory)`**

链式方法（与 `AddJavaScriptApp` 相同，此外还有）：
- `.WithNpmPackageInstallation()` — 启动前运行 `npm install`
- `.WithHttpEndpoint(port?, targetPort?, name?)` — Vite 默认使用 5173 端口

**`AddNodeApp(name, scriptPath, workingDirectory)`**

链式方法：
- `.WithHttpEndpoint(port?, targetPort?, name?)` — 暴露 HTTP
- `.WithNpmPackageInstallation()` — 启动前运行 `npm install`
- `.WithReference(resource)` — 连接依赖项
- `.WithEnvironment(key, value)` — 设置环境变量

**JS/TS 服务发现：** 环境变量会自动注入。使用 `process.env`：
```javascript
const redisUrl = process.env.ConnectionStrings__cache;
const apiUrl = process.env.services__api__http__0;
```

---

## 社区（CommunityToolkit/Aspire）

所有社区集成都遵循相同的模式：在您的 AppHost 中安装 NuGet 包，然后使用 `Add*App()` 方法。

### Go

**包：** `CommunityToolkit.Aspire.Hosting.Golang`

```csharp
builder.AddGolangApp("go-api", "../go-service")
    .WithHttpEndpoint(targetPort: 8080)
    .WithReference(redis)
    .WithEnvironment("LOG_LEVEL", "debug")
    .WaitFor(redis);
```

链式方法：
- `.WithHttpEndpoint(port?, targetPort?, name?)`
- `.WithReference(resource)`
- `.WithEnvironment(key, value)`
- `.WaitFor(resource)`

**Go 服务发现：** 通过 `os.Getenv()` 使用标准环境变量：
```go
redisAddr := os.Getenv("ConnectionStrings__cache")
```

### Java（Spring Boot）

**包：** `CommunityToolkit.Aspire.Hosting.Java`

```csharp
builder.AddSpringApp("spring-api", "../spring-service")
    .WithHttpEndpoint(targetPort: 8080)
    .WithReference(postgres)
    .WaitFor(postgres);
```

链式方法：
- `.WithHttpEndpoint(port?, targetPort?, name?)`
- `.WithReference(resource)`
- `.WithEnvironment(key, value)`
- `.WaitFor(resource)`
- `.WithMavenBuild()` — 启动前运行 Maven 构建
- `.WithGradleBuild()` — 启动前运行 Gradle 构建

**Java 服务发现：** 通过 `System.getenv()` 使用环境变量：
```java
String dbConn = System.getenv("ConnectionStrings__db");
```

### Rust

**包：** `CommunityToolkit.Aspire.Hosting.Rust`

```csharp
builder.AddRustApp("rust-worker", "../rust-service")
    .WithHttpEndpoint(targetPort: 3000)
    .WithReference(redis)
    .WaitFor(redis);
```

链式方法：
- `.WithHttpEndpoint(port?, targetPort?, name?)`
- `.WithReference(resource)`
- `.WithEnvironment(key, value)`
- `.WaitFor(resource)`
- `.WithCargoBuild()` — 启动前运行 `cargo build`

### Bun

**包：** `CommunityToolkit.Aspire.Hosting.Bun`

```csharp
builder.AddBunApp("bun-api", "../bun-service")
    .WithHttpEndpoint(targetPort: 3000)
    .WithReference(redis);
```

链式方法：
- `.WithHttpEndpoint(port?, targetPort?, name?)`
- `.WithReference(resource)`
- `.WithEnvironment(key, value)`
- `.WaitFor(resource)`
- `.WithBunPackageInstallation()` — 启动前运行 `bun install`

### Deno

**包：** `CommunityToolkit.Aspire.Hosting.Deno`

```csharp
builder.AddDenoApp("deno-api", "../deno-service")
    .WithHttpEndpoint(targetPort: 8000)
    .WithReference(redis);
```

链式方法：
- `.WithHttpEndpoint(port?, targetPort?, name?)`
- `.WithReference(resource)`
- `.WithEnvironment(key, value)`
- `.WaitFor(resource)`

### PowerShell

```csharp
builder.AddPowerShell("ps-script", "../scripts/process.ps1")
    .WithReference(storageAccount);
```

### Dapr

**包：** `Aspire.Hosting.Dapr`（官方）

```csharp
var dapr = builder.AddDapr();
var api = builder.AddProject<Projects.Api>("api")
    .WithDaprSidecar("api-sidecar");
```

---

## 完整多语言示例

```csharp
var builder = DistributedApplication.CreateBuilder(args);

// 基础设施
var redis = builder.AddRedis("cache");
var postgres = builder.AddPostgres("pg").AddDatabase("catalog");
var mongo = builder.AddMongoDB("mongo").AddDatabase("analytics");
var rabbit = builder.AddRabbitMQ("messaging");

// .NET API（主应用）
var api = builder.AddProject<Projects.CatalogApi>("api")
    .WithReference(postgres)
    .WithReference(redis)
    .WithReference(rabbit)
    .WaitFor(postgres)
    .WaitFor(redis);

// Python 机器学习服务（FastAPI）
var ml = builder.AddUvicornApp("ml", "../ml-service", "app:app")
    .WithHttpEndpoint(targetPort: 8000)
    .WithVirtualEnvironment()
    .WithReference(redis)
    .WithReference(mongo)
    .WaitFor(redis);

// TypeScript 前端（Vite + React）
var web = builder.AddViteApp("web", "../frontend")
    .WithNpmPackageInstallation()
    .WithHttpEndpoint(targetPort: 5173)
    .WithReference(api);

// Go 事件处理器
var processor = builder.AddGolangApp("processor", "../go-processor")
    .WithReference(rabbit)
    .WithReference(mongo)
    .WaitFor(rabbit);

// Java 分析服务（Spring Boot）
var analytics = builder.AddSpringApp("analytics", "../spring-analytics")
    .WithHttpEndpoint(targetPort: 8080)
    .WithReference(mongo)
    .WithReference(rabbit)
    .WaitFor(mongo);

// Rust 高性能工作进程
var worker = builder.AddRustApp("worker", "../rust-worker")
    .WithReference(redis)
    .WithReference(rabbit)
    .WaitFor(redis);

builder.Build().Run();
```

此单一 AppHost 启动了 5 种语言中的 6 个服务以及 4 个基础设施资源，所有资源均通过自动服务发现连接在一起。

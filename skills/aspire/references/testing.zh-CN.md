# 测试 — 完整参考

Aspire 提供 `Aspire.Hosting.Testing` 用于对您的完整 AppHost 进行集成测试。测试会启动整个分布式应用程序（或其中一部分），并针对真实服务运行断言。

---

## 包

```xml
<PackageReference Include="Aspire.Hosting.Testing" Version="*" />
```

---

## 核心模式：DistributedApplicationTestingBuilder

```csharp
// 1. 从您的 AppHost 创建测试构建器
var builder = await DistributedApplicationTestingBuilder
    .CreateAsync<Projects.MyAppHost>();

// 2. （可选）为测试覆盖资源
// ... 请参阅下面的自定义部分

// 3. 构建并启动应用程序
await using var app = await builder.BuildAsync();
await app.StartAsync();

// 4. 为您的服务创建 HTTP 客户端
var client = app.CreateHttpClient("api");

// 5. 运行断言
var response = await client.GetAsync("/health");
Assert.Equal(HttpStatusCode.OK, response.StatusCode);
```

---

## xUnit 示例

### 基础健康检查测试

```csharp
public class HealthTests(ITestOutputHelper output)
{
    [Fact]
    public async Task AllServicesAreHealthy()
    {
        var builder = await DistributedApplicationTestingBuilder
            .CreateAsync<Projects.AppHost>();

        await using var app = await builder.BuildAsync();
        await app.StartAsync();

        // 测试每个服务的健康检查端点
        var apiClient = app.CreateHttpClient("api");
        var apiHealth = await apiClient.GetAsync("/health");
        Assert.Equal(HttpStatusCode.OK, apiHealth.StatusCode);

        var workerClient = app.CreateHttpClient("worker");
        var workerHealth = await workerClient.GetAsync("/health");
        Assert.Equal(HttpStatusCode.OK, workerHealth.StatusCode);
    }
}
```

### API 集成测试

```csharp
public class ApiTests(ITestOutputHelper output)
{
    [Fact]
    public async Task CreateOrder_ReturnsCreated()
    {
        var builder = await DistributedApplicationTestingBuilder
            .CreateAsync<Projects.AppHost>();

        await using var app = await builder.BuildAsync();
        await app.StartAsync();

        var client = app.CreateHttpClient("api");

        var order = new { ProductId = 1, Quantity = 2 };
        var response = await client.PostAsJsonAsync("/orders", order);

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);

        var created = await response.Content.ReadFromJsonAsync<Order>();
        Assert.NotNull(created);
        Assert.Equal(1, created.ProductId);
    }
}
```

### 带等待就绪的测试

```csharp
[Fact]
public async Task DatabaseIsSeeded()
{
    var builder = await DistributedApplicationTestingBuilder
        .CreateAsync<Projects.AppHost>();

    await using var app = await builder.BuildAsync();
    await app.StartAsync();

    // 等待 API 完全就绪（所有依赖项健康）
    await app.WaitForResourceReadyAsync("api");

    var client = app.CreateHttpClient("api");
    var response = await client.GetAsync("/products");

    Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    var products = await response.Content.ReadFromJsonAsync<List<Product>>();
    Assert.NotEmpty(products);
}
```

---

## MSTest 示例

```csharp
[TestClass]
public class IntegrationTests
{
    [TestMethod]
    public async Task ApiReturnsProducts()
    {
        var builder = await DistributedApplicationTestingBuilder
            .CreateAsync<Projects.AppHost>();

        await using var app = await builder.BuildAsync();
        await app.StartAsync();

        var client = app.CreateHttpClient("api");
        var response = await client.GetAsync("/products");

        Assert.AreEqual(HttpStatusCode.OK, response.StatusCode);
    }
}
```

---

## NUnit 示例

```csharp
[TestFixture]
public class IntegrationTests
{
    [Test]
    public async Task ApiReturnsProducts()
    {
        var builder = await DistributedApplicationTestingBuilder
            .CreateAsync<Projects.AppHost>();

        await using var app = await builder.BuildAsync();
        await app.StartAsync();

        var client = app.CreateHttpClient("api");
        var response = await client.GetAsync("/products");

        Assert.That(response.StatusCode, Is.EqualTo(HttpStatusCode.OK));
    }
}
```

---

## 自定义测试 AppHost

### 覆盖资源

```csharp
var builder = await DistributedApplicationTestingBuilder
    .CreateAsync<Projects.AppHost>();

// 用测试容器替换真实数据库
builder.Services.ConfigureHttpClientDefaults(http =>
{
    http.AddStandardResilienceHandler();
});

// 添加特定于测试的配置
builder.Configuration["TestMode"] = "true";

await using var app = await builder.BuildAsync();
await app.StartAsync();
```

### 排除资源

```csharp
var builder = await DistributedApplicationTestingBuilder
    .CreateAsync<Projects.AppHost>(args =>
    {
        // 对于仅 API 的测试，不启动 worker
        args.Args = ["--exclude-resource", "worker"];
    });
```

### 使用特定环境进行测试

```csharp
var builder = await DistributedApplicationTestingBuilder
    .CreateAsync<Projects.AppHost>(args =>
    {
        args.Args = ["--environment", "Testing"];
    });
```

---

## 连接字符串访问

```csharp
// 在测试中获取资源的连接字符串
var connectionString = await app.GetConnectionStringAsync("db");

// 在测试中直接使用该连接字符串查询数据库
using var conn = new NpgsqlConnection(connectionString);
await conn.OpenAsync();
var count = await conn.ExecuteScalarAsync<int>("SELECT COUNT(*) FROM products");
Assert.True(count > 0);
```

---

## 最佳实践

1. **在发送请求前使用 `WaitForResourceReadyAsync`** — 确保所有依赖项处于健康状态  
2. **每个测试应独立运行** — 不要依赖前一个测试的状态  
3. **使用 `await using`** 管理应用程序 — 即使测试失败也能确保清理  
4. **测试真实基础设施** — Aspire 会启动真实的容器（Redis、PostgreSQL 等），为您提供高保真度的集成测试  
5. **保持测试 AppHost 精简** — 排除特定测试场景中不需要的资源  
6. **使用特定于测试的配置** — 通过覆盖设置实现测试隔离  
7. **超时保护** — 由于容器需要时间启动，应设置合理的测试超时时间：

```csharp
[Fact(Timeout = 120_000)]  // 2 分钟
public async Task SlowIntegrationTest() { ... }
```

---

## 项目结构

```
MyApp/
├── src/
│   ├── MyApp.AppHost/           # AppHost 项目
│   ├── MyApp.Api/               # API 服务
│   ├── MyApp.Worker/            # Worker 服务
│   └── MyApp.ServiceDefaults/   # 共享默认值
└── tests/
    └── MyApp.Tests/             # 集成测试
        ├── MyApp.Tests.csproj   # 引用 AppHost + 测试包
        └── ApiTests.cs           # 测试类
```

```xml
<!-- MyApp.Tests.csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <IsAspireTestProject>true</IsAspireTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Aspire.Hosting.Testing" Version="*" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="*" />
    <PackageReference Include="xunit" Version="*" />
    <PackageReference Include="xunit.runner.visualstudio" Version="*" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\MyApp.AppHost\MyApp.AppHost.csproj" />
  </ItemGroup>
</Project>
```

# 集成目录

Aspire 提供了 **144+ 种集成**，涵盖 13 个类别。与其维护静态列表，不如使用 MCP 工具获取实时、更新的集成数据。

---

## 发现集成（MCP 工具）

Aspire MCP 服务器提供了两种用于发现集成的工具——这些工具适用于 **所有 CLI 版本**（13.1+），且无需运行 AppHost。

| 工具                   | 功能                                                                                             | 使用场景                                                                                 |
| ---------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `list_integrations`    | 返回所有可用的 Aspire 托管集成及其 NuGet 包 ID                           | "有哪些数据库相关的集成可用？" / "显示所有 Redis 相关的集成" |
| `get_integration_docs` | 获取特定集成包的详细文档（设置、配置、代码示例） | "如何配置 PostgreSQL？" / "显示 `Aspire.Hosting.Redis` 的文档"            |

### 工作流程

1. **浏览** — 调用 `list_integrations` 查看可用集成。可通过类别或关键词过滤结果。
2. **深入探索** — 使用包 ID（例如 `Aspire.Hosting.Redis`）和版本号（例如 `9.0.0`）调用 `get_integration_docs`，以获取完整的设置说明。
3. **添加** — 运行 `aspire add <integration>` 将托管包安装到您的 AppHost 中。

> **提示：** 这些工具返回的数据与 [官方集成画廊](https://aspire.dev/integrations/gallery/) 相同。优先使用这些工具而非静态文档——集成会频繁新增。

---

## 集成模式

每种集成均遵循两包模式：

- **托管包** (`Aspire.Hosting.*`) — 将资源添加到 AppHost
- **客户端包** (`Aspire.*`) — 在服务中配置客户端 SDK，包含健康检查、遥测和重试功能
- **社区工具包** (`CommunityToolkit.Aspire.*`) — 由 [Aspire 社区工具包](https://github.com/CommunityToolkit/Aspire) 维护的集成

```csharp
// === AppHost（托管端） ===
var redis = builder.AddRedis("cache");  // Aspire.Hosting.Redis
var api = builder.AddProject<Projects.Api>("api")
    .WithReference(redis);

// === 服务（客户端）——在 API 的 Program.cs 中 ===
builder.AddRedisClient("cache");        // Aspire.StackExchange.Redis
// 自动配置：连接字符串、健康检查、OpenTelemetry、重试
```

---

## 集成分类概览

使用 `list_integrations` 查看完整的实时列表。以下摘要涵盖了主要类别：

| 分类            | 关键集成                                                                      | 示例托管包                  |
| ------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------- |
| **人工智能（AI）** | Azure OpenAI、OpenAI、GitHub 模型、Ollama                                           | `Aspire.Hosting.Azure.CognitiveServices` |
| **缓存**         | Redis、Garnet、Valkey、Azure Redis 缓存                                          | `Aspire.Hosting.Redis`                   |
| **云 / Azure**   | 存储、Cosmos DB、服务总线、密钥保险箱、事件中心、函数、SQL、SignalR（25+） | `Aspire.Hosting.Azure.Storage`           |
| **云 / AWS**     | AWS SDK 集成                                                                   | `Aspire.Hosting.AWS`                     |
| **数据库**       | PostgreSQL、SQL Server、MongoDB、MySQL、Oracle、Elasticsearch、Milvus、Qdrant、SQLite | `Aspire.Hosting.PostgreSQL`              |
| **开发工具（DevTools）** | 数据 API 构建器、开发隧道、Mailpit、k6、Flagd、Ngrok、Stripe                      | `Aspire.Hosting.DevTunnels`              |
| **消息传递（Messaging）** | RabbitMQ、Kafka、NATS、ActiveMQ、LavinMQ                                              | `Aspire.Hosting.RabbitMQ`                |
| **可观测性（Observability）** | OpenTelemetry（内置）、Seq、OTel 收集器                                         | `Aspire.Hosting.Seq`                     |
| **计算（Compute）** | Docker Compose、Kubernetes                                                            | `Aspire.Hosting.Docker`                  |
| **反向代理（Reverse Proxies）** | YARP                                                                                  | `Aspire.Hosting.Yarp`                    |
| **安全性（Security）** | Keycloak                                                                              | `Aspire.Hosting.Keycloak`                |
| **框架（Frameworks）** | JavaScript、Python、Go、Java、Rust、Bun、Deno、Orleans、MAUI、Dapr、PowerShell        | `Aspire.Hosting.Python`                  |

有关多语言框架方法签名，请参阅 [多语言 API](polyglot-apis.md)。

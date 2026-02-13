# 仪表板 — 完整参考指南

Aspire 仪表板为分布式应用程序中的所有资源提供实时可观测性。它会在 `aspire run` 启动时自动启动，也可以单独运行。

---

## 功能

### 资源视图

显示所有资源（项目、容器、可执行文件）并包含以下信息：

- **名称**和**类型**（项目、容器、可执行文件）
- **状态**（启动中、运行中、已停止、启动失败等）
- **启动时间**和**运行时长**
- **端点** — 每个暴露端点的可点击 URL
- **来源** — 项目路径、容器镜像或可执行文件路径
- **操作** — 停止、启动、重启按钮

### 控制台日志

聚合所有资源的原始标准输出/标准错误日志：

- 按资源名称筛选
- 在日志中搜索
- 自动滚动并支持暂停
- 按资源进行颜色编码

### 结构化日志

应用级别的结构化日志（通过 ILogger、OpenTelemetry）：

- **可筛选** — 按资源、日志级别、类别和消息内容进行筛选
- **可展开** — 点击查看包含所有属性的完整日志条目
- **与追踪相关联** — 点击跳转到相关追踪
- 支持 .NET ILogger 的结构化日志属性
- 支持 OpenTelemetry 来自任何语言的日志信号

### 分布式追踪

跨所有服务的端到端请求追踪：

- **瀑布视图** — 显示完整的调用链及时间信息
- **跨度详情** — HTTP 方法、URL、状态码、持续时间
- **数据库跨度** — SQL 查询、连接信息
- **消息跨度** — 队列操作、主题发布
- **错误高亮** — 失败的跨度以红色显示
- **跨服务关联** — .NET 服务自动传播追踪上下文；其他语言需手动配置

### 指标

实时和历史指标：

- **运行时指标** — CPU、内存、GC、线程池
- **HTTP 指标** — 请求速率、错误率、延迟分位数
- **自定义指标** — 通过 OpenTelemetry 发出的任何服务指标
- **可图表化** — 每个指标的时间序列图表

### GenAI 可视化器

针对使用 AI/LLM 集成的应用程序：

- **令牌使用情况** — 每个请求的提示令牌、完成令牌和总令牌
- **提示/完成对** — 查看实际发送的提示和接收的响应
- **模型元数据** — 使用的模型、温度、最大令牌数
- **延迟** — 每次 AI 调用的时间
- 需要服务通过 OpenTelemetry 发出 [GenAI 语义约定](https://opentelemetry.io/docs/specs/semconv/gen-ai/)

---

## 仪表板 URL

默认情况下，仪表板运行在自动分配的端口上。查找方式如下：

- 在 `aspire run` 启动时查看终端输出
- 通过 MCP：`list_resources` 工具
- 使用 `--dashboard-port` 覆盖默认端口：

```bash
aspire run --dashboard-port 18888
```

---

## 独立仪表板

无需 AppHost 即可运行仪表板，适用于已使用 OpenTelemetry 发出数据的现有应用程序：

```bash
docker run --rm -d \
  -p 18888:18888 \
  -p 4317:18889 \
  mcr.microsoft.com/dotnet/aspire-dashboard:latest
```

| 端口             | 用途                                                      |
| ---------------- | ------------------------------------------------------------ |
| `18888`          | 仪表板 Web 界面                                             |
| `4317` → `18889` | OTLP gRPC 接收器（标准 OTel 端口 → 仪表板内部端口）         |

### 配置您的服务

将 OpenTelemetry 导出器指向仪表板：

```bash
# 适用于任何语言的 OpenTelemetry SDK 的环境变量
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_SERVICE_NAME=my-service
```

### Docker Compose 示例

```yaml
services:
  dashboard:
    image: mcr.microsoft.com/dotnet/aspire-dashboard:latest
    ports:
      - "18888:18888"
      - "4317:18889"

  api:
    build: ./api
    environment:
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://dashboard:18889
      - OTEL_SERVICE_NAME=api

  worker:
    build: ./worker
    environment:
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://dashboard:18889
      - OTEL_SERVICE_NAME=worker
```

---

## 仪表板配置

### 身份验证

独立仪表板支持通过浏览器令牌进行身份验证：

```bash
docker run --rm -d \
  -p 18888:18888 \
  -p 4317:18889 \
  -e DASHBOARD__FRONTEND__AUTHMODE=BrowserToken \
  -e DASHBOARD__FRONTEND__BROWSERTOKEN__TOKEN=my-secret-token \
  mcr.microsoft.com/dotnet/aspire-dashboard:latest
```

### OTLP 配置

```bash
# 接受通过 gRPC 的 OTLP（默认）
-e DASHBOARD__OTLP__GRPC__ENDPOINT=http://0.0.0.0:18889

# 接受通过 HTTP 的 OTLP
-e DASHBOARD__OTLP__HTTP__ENDPOINT=http://0.0.0.0:18890

# 要求 OTLP 使用 API 密钥
-e DASHBOARD__OTLP__AUTHMODE=ApiKey
-e DASHBOARD__OTLP__PRIMARYAPIKEY=my-api-key
```

### 资源限制

```bash
# 限制保留的日志条目数量
-e DASHBOARD__TELEMETRYLIMITS__MAXLOGCOUNT=10000

# 限制保留的追踪条目数量
-e DASHBOARD__TELEMETRYLIMITS__MAXTRACECOUNT=10000

# 限制保留的指标数据点数量
-e DASHBOARD__TELEMETRYLIMITS__MAXMETRICCOUNT=50000
```

---

## Copilot 集成

仪表板与 VS Code 中的 GitHub Copilot 集成：

- 询问资源状态相关问题
- 使用自然语言查询日志和追踪
- MCP 服务器（参见 [MCP 服务器](mcp-server.md)）提供桥梁功能

---

## 非 .NET 服务的遥测数据

要使非 .NET 服务在仪表板中显示，它们必须发出 OpenTelemetry 信号。使用 `.WithReference()` 时，Aspire 会自动注入 OTLP 端点环境变量：

### Python（OpenTelemetry SDK）

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import os

# Aspire 会自动注入 OTEL_EXPORTER_OTLP_ENDPOINT 环境变量
endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
trace.set_tracer_provider(provider)
```

### JavaScript（OpenTelemetry SDK）

```javascript
const { NodeTracerProvider } = require("@opentelemetry/sdk-trace-node");
const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-grpc");

const provider = new NodeTracerProvider();
provider.addSpanProcessor(
  new BatchSpanProcessor(
    new OTLPTraceExporter({
      url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || "http://localhost:4317",
    })
  )
);
provider.register();
```

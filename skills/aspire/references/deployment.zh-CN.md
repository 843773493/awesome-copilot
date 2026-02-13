# 部署 — 完整指南

Aspire 将 **编排**（运行什么）与 **部署**（在哪里运行）分离。`aspire publish` 命令将您的 AppHost 资源模型转换为针对目标平台的部署清单。

---

## 发布 vs 部署

| 概念 | 所做的事情 |
|---|---|
| **`aspire publish`** | 生成部署工件（Dockerfile、Helm 图表、Bicep 等） |
| **部署** | 您通过 CI/CD 管道运行生成的工件 |

Aspire 不直接进行部署。它生成清单 — 您进行部署。

---

## 支持的目标

### Docker

**包:** `Aspire.Hosting.Docker`

```bash
aspire publish -p docker -o ./docker-output
```

生成：
- `docker-compose.yml` — 与您的 AppHost 匹配的服务定义
- 每个 .NET 项目的 `Dockerfile`
- 环境变量配置
- 卷挂载
- 网络配置

```csharp
// AppHost 配置用于 Docker 发布
var api = builder.AddProject<Projects.Api>("api")
    .PublishAsDockerFile();  // 覆盖默认发布行为
```

### Kubernetes

**包:** `Aspire.Hosting.Kubernetes`

```bash
aspire publish -p kubernetes -o ./k8s-output
```

生成：
- Kubernetes YAML 清单（Deployment、Service、ConfigMaps、Secrets）
- Helm 图表（可选）
- Ingress 配置
- 基于 AppHost 配置的资源限制

```csharp
// AppHost：自定义 K8s 发布
var api = builder.AddProject<Projects.Api>("api")
    .WithReplicas(3)                    // 映射到 K8s replicas
    .WithExternalHttpEndpoints();       // 映射到 Ingress/LoadBalancer
```

### Azure 容器应用

**包:** `Aspire.Hosting.Azure.AppContainers`

```bash
aspire publish -p azure -o ./azure-output
```

生成：
- Azure 容器应用环境的 Bicep 模板
- 每个服务的容器应用定义
- Azure 容器注册表配置
- 托管身份配置
- 如果使用 Dapr 集成，则生成 Dapr 组件
- VNET 配置

```csharp
// AppHost：Azure 特定配置
var api = builder.AddProject<Projects.Api>("api")
    .WithExternalHttpEndpoints()        // 映射到外部入口
    .WithReplicas(3);                   // 映射到最小副本数

// Azure 资源会自动创建
var storage = builder.AddAzureStorage("storage");   // 创建存储账户
var cosmos = builder.AddAzureCosmosDB("cosmos");    // 创建 Cosmos DB 账户
var sb = builder.AddAzureServiceBus("messaging");   // 创建服务总线命名空间
```

### Azure 应用服务

**包:** `Aspire.Hosting.Azure.AppService`

```bash
aspire publish -p appservice -o ./appservice-output
```

生成：
- 应用服务计划和 Web 应用的 Bicep 模板
- 连接字符串配置
- 应用设置

---

## 资源模型到部署的映射

| AppHost 概念 | Docker Compose | Kubernetes | Azure 容器应用 |
|---|---|---|---|
| `AddProject<T>()` | 与 Dockerfile 匹配的服务 | Deployment + Service | 容器应用 |
| `AddContainer()` | 具有 `image:` 的服务 | Deployment + Service | 容器应用 |
| `AddRedis()` | 服务: redis | StatefulSet | 管理的 Redis |
| `AddPostgres()` | 服务: postgres | StatefulSet | Azure PostgreSQL |
| `.WithReference()` | `environment:` 变量 | ConfigMap / Secret | 应用设置 |
| `.WithReplicas(n)` | `deploy: replicas: n` | `replicas: n` | `minReplicas: n` |
| `.WithVolume()` | `volumes:` | PersistentVolumeClaim | Azure 文件 |
| `.WithHttpEndpoint()` | `ports:` | Service 端口 | Ingress |
| `.WithExternalHttpEndpoints()` | `ports:`（主机） | Ingress / LoadBalancer | 外部入口 |
| `AddParameter(secret: true)` | `.env` 文件 | Secret | 密钥保管库引用 |

---

## CI/CD 集成

### GitHub Actions 示例

```yaml
name: 部署
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 设置 .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '10.0.x'

      - name: 安装 Aspire CLI
        run: curl -sSL https://aspire.dev/install.sh | bash

      - name: 生成清单
        run: aspire publish -p azure -o ./deploy

      - name: 部署到 Azure
        uses: azure/arm-deploy@v2
        with:
          template: ./deploy/main.bicep
          parameters: ./deploy/main.parameters.json
```

### Azure DevOps 示例

```yaml
trigger:
  branches:
    include: [main]

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UseDotNet@2
    inputs:
      version: '10.0.x'

  - script: curl -sSL https://aspire.dev/install.sh | bash
    displayName: '安装 Aspire CLI'

  - script: aspire publish -p azure -o $(Build.ArtifactStagingDirectory)/deploy
    displayName: '生成部署清单'

  - task: AzureResourceManagerTemplateDeployment@3
    inputs:
      deploymentScope: '资源组'
      templateLocation: '$(Build.ArtifactStagingDirectory)/deploy/main.bicep'
```

---

## 环境特定配置

### 使用参数处理密钥

```csharp
// AppHost
var dbPassword = builder.AddParameter("db-password", secret: true);
var postgres = builder.AddPostgres("db", password: dbPassword);
```

在部署时：
- **Docker:** 从 `.env` 文件加载
- **Kubernetes:** 从 `Secret` 资源加载
- **Azure:** 通过托管身份从密钥保管库加载

### 条件资源

```csharp
// 生产环境使用 Azure 服务，本地使用模拟器
if (builder.ExecutionContext.IsPublishMode)
{
    var cosmos = builder.AddAzureCosmosDB("cosmos");    // 真实的 Azure 资源
}
else
{
    var cosmos = builder.AddAzureCosmosDB("cosmos")
        .RunAsEmulator();                                // 本地模拟器
}
```

---

## 开发容器 & GitHub Codespaces

Aspire 模板包含 `.devcontainer/` 配置：

```json
{
  "name": "Aspire 应用",
  "image": "mcr.microsoft.com/devcontainers/dotnet:10.0",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/node:1": {}
  },
  "postCreateCommand": "curl -sSL https://aspire.dev/install.sh | bash",
  "forwardPorts": [18888],
  "portsAttributes": {
    "18888": { "label": "Aspire 仪表板" }
  }
}
```

端口转发在 Codespaces 中自动工作 — 仪表板和所有服务端点可通过转发的 URL 访问。

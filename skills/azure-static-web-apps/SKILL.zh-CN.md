---
name: azure-static-web-apps
description: 帮助使用 SWA CLI 创建、配置和部署 Azure 静态网站应用。适用于将静态网站部署到 Azure、设置 SWA 本地开发、配置 staticwebapp.config.json、添加 Azure Functions API 到 SWA，或为静态网站应用设置 GitHub Actions CI/CD。
---

## 概述

Azure 静态网站应用（SWA）可托管静态前端并支持可选的无服务器 API 后端。SWA CLI（`swa`）提供本地开发模拟和部署功能。

**关键特性：**
- 包含 API 代理和身份验证模拟的本地模拟器
- 自动检测和配置框架
- 直接部署到 Azure
- 支持数据库连接

**配置文件：**
- `swa-cli.config.json` - CLI 设置，**由 `swa init` 创建**（从不手动创建）
- `staticwebapp.config.json` - 运行时配置（路由、身份验证、头信息、API 运行时）- 可手动创建

## 一般说明

### 安装

```bash
npm install -D @azure/static-web-apps-cli
```

验证：`npx swa --version`

### 快速入门工作流

**重要：始终使用 `swa init` 创建配置文件。不要手动创建 `swa-cli.config.json`。**

1. `swa init` - **必需的第一步** - 自动检测框架并创建 `swa-cli.config.json`
2. `swa start` - 在 `http://localhost:4280` 上运行本地模拟器
3. `swa login` - 与 Azure 进行身份验证
4. `swa deploy` - 部署到 Azure

### 配置文件

**swa-cli.config.json** - 由 `swa init` 创建，不要手动创建：
- 运行 `swa init` 以进行交互式设置并检测框架
- 运行 `swa init --yes` 以接受自动检测的默认值
- 仅在初始化后编辑生成的文件以自定义设置

生成的配置示例（仅作参考）：
```json
{
  "$schema": "https://aka.ms/azure/static-web-apps-cli/schema",
  "configurations": {
    "app": {
      "appLocation": ".",
      "apiLocation": "api",
      "outputLocation": "dist",
      "appBuildCommand": "npm run build",
      "run": "npm run dev",
      "appDevserverUrl": "http://localhost:3000"
    }
  }
}
```

**staticwebapp.config.json**（在应用源代码或输出文件夹中）- 该文件**可以手动创建**用于运行时配置：
```json
{
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/images/*", "/css/*"]
  },
  "routes": [
    { "route": "/api/*", "allowedRoles": ["authenticated"] }
  ],
  "platform": {
    "apiRuntime": "node:20"
  }
}
```

## 命令行参考

### swa login

与 Azure 进行身份验证以进行部署。

```bash
swa login                              # 交互式登录
swa login --subscription-id <id>       # 指定订阅
swa login --clear-credentials          # 清除缓存的身份验证凭据
```

**标志：** `--subscription-id, -S` | `--resource-group, -R` | `--tenant-id, -T` | `--client-id, -C` | `--client-secret, -CS` | `--app-name, -n`

### swa init

根据现有前端和（可选）API 配置新的 SWA 项目。自动检测框架。

```bash
swa init                    # 交互式设置
swa init --yes              # 接受默认值
```

### swa build

构建前端和/或 API。

```bash
swa build                   # 使用配置构建
swa build --auto            # 自动检测并构建
swa build myApp             # 构建特定配置
```

**标志：** `--app-location, -a` | `--api-location, -i` | `--output-location, -O` | `--app-build-command, -A` | `--api-build-command, -I`

### swa start

启动本地开发模拟器。

```bash
swa start                                    # 从 outputLocation 提供服务
swa start ./dist                             # 部署特定文件夹
swa start http://localhost:3000              # 代理到开发服务器
swa start ./dist --api-location ./api        # 包含 API 文件夹
swa start http://localhost:3000 --run "npm start"  # 自动启动开发服务器
```

**常见框架端口：**
| 框架 | 端口 |
|-----------|------|
| React/Vue/Next.js | 3000 |
| Angular | 4200 |
| Vite | 5173 |

**关键标志：**
- `--port, -p` - 模拟器端口（默认：4280）
- `--api-location, -i` - API 文件夹路径
- `--api-port, -j` - API 端口（默认：7071）
- `--run, -r` - 启动开发服务器的命令
- `--open, -o` - 自动打开浏览器
- `--ssl, -s` - 启用 HTTPS

### swa deploy

将应用部署到 Azure 静态网站应用。

```bash
swa deploy                              # 使用配置部署
swa deploy ./dist                       # 部署特定文件夹
swa deploy --env production             # 部署到生产环境
swa deploy --deployment-token <TOKEN>   # 使用部署令牌
swa deploy --dry-run                    # 预览部署而不实际部署
```

**获取部署令牌：**
- Azure 门户：静态网站应用 → 概述 → 管理部署令牌
- CLI：`swa deploy --print-token`
- 环境变量：`SWA_CLI_DEPLOYMENT_TOKEN`

**关键标志：**
- `--env` - 目标环境（`preview` 或 `production`）
- `--deployment-token, -d` - 部署令牌
- `--app-name, -n` - Azure SWA 资源名称

### swa db

初始化数据库连接。

```bash
swa db init --database-type mssql
swa db init --database-type postgresql
swa db init --database-type cosmosdb_nosql
```

## 场景

### 从现有前端和后端创建 SWA

**始终在运行 `swa start` 或 `swa deploy` 之前运行 `swa init`。不要手动创建 `swa-cli.config.json`。**

```bash
# 1. 安装 CLI
npm install -D @azure/static-web-apps-cli

# 2. 初始化 - 必需步骤：创建 swa-cli.config.json 并使用自动检测设置
npx swa init              # 交互模式
# 或
npx swa init --yes        # 接受自动检测的默认值

# 3. 构建应用（如需要）
npm run build

# 4. 本地测试（使用 swa-cli.config.json 中的设置）
npx swa start

# 5. 部署
npx swa login
npx swa deploy --env production
```

### 添加 Azure Functions 后端

1. **创建 API 文件夹：**
```bash
mkdir api && cd api
func init --worker-runtime node --model V4
func new --name message --template "HTTP trigger"
```

2. **示例函数**（`api/src/functions/message.js`）：
```javascript
const { app } = require('@azure/functions');

app.http('message', {
    methods: ['GET', 'POST'],
    authLevel: 'anonymous',
    handler: async (request) => {
        const name = request.query.get('name') || 'World';
        return { jsonBody: { message: `Hello, ${name}!` } };
    }
});
```

3. **在 `staticwebapp.config.json` 中设置 API 运行时：**
```json
{
  "platform": { "apiRuntime": "node:20" }
}
```

4. **更新 CLI 配置**在 `swa-cli.config.json` 中：
```json
{
  "configurations": {
    "app": { "apiLocation": "api" }
  }
}
```

5. **本地测试：**
```bash
npx swa start ./dist --api-location ./api
# 访问 API：http://localhost:4280/api/message
```

**支持的 API 运行时：** `node:18`, `node:20`, `node:22`, `dotnet:8.0`, `dotnet-isolated:8.0`, `python:3.10`, `python:3.11`

### 设置 GitHub Actions 部署

1. **在 Azure 门户或通过 Azure CLI 创建 SWA 资源**
2. **链接 GitHub 仓库** - 工作流自动生成，或手动创建：

`.github/workflows/azure-static-web-apps.yml`:
```yaml
name: Azure 静态网站应用 CI/CD

on:
  push:
    branches: [main]
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main]

jobs:
  build_and_deploy:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: 构建与部署
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: upload
          app_location: /
          api_location: api
          output_location: dist

  close_pr:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          action: close
```

3. **添加密钥：** 将部署令牌复制到仓库密钥 `AZURE_STATIC_WEB_APPS_API_TOKEN`

**工作流设置：**
- `app_location` - 前端源路径
- `api_location` - API 源路径
- `output_location` - 构建输出文件夹
- `skip_app_build: true` - 如果已预先构建则跳过
- `app_build_command` - 自定义构建命令

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 客户端路由返回 404 错误 | 在 `staticwebapp.config.json` 中添加 `navigationFallback` 并设置 `rewrite: "/index.html"` |
| API 返回 404 | 验证 `api` 文件夹结构，确保 `platform.apiRuntime` 已设置，检查函数导出 |
| 构建输出未找到 | 验证 `output_location` 是否与实际构建输出目录匹配 |
| 本地身份验证不工作 | 使用 `/.auth/login/<provider>` 访问身份验证模拟器 UI |
| CORS 错误 | `/api/*` 下的 API 是同源的；外部 API 需要 CORS 头信息 |
| 部署令牌过期 | 在 Azure 门户 → 静态网站应用 → 管理部署令牌中重新生成 |
| 配置未应用 | 确保 `staticwebapp.config.json` 位于 `app_location` 或 `output_location` 中 |
| 本地 API 超时 | 默认为 45 秒；优化函数或检查是否有阻塞调用 |

**调试命令：**
```bash
swa start --verbose log        # 显示详细输出
swa deploy --dry-run           # 预览部署
swa --print-config             # 显示解析后的配置
```

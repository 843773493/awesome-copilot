

---
agent: 'agent'
tools: ['search/codebase', 'edit/editFiles', 'terminalCommand']
description: '通过创建针对项目的自定义 Dockerfile 和 .dockerfile 文件来容器化 ASP.NET Core 项目。'
---

# ASP.NET Core 容器化提示

## 容器化请求

根据以下设置容器化指定的 ASP.NET Core (.NET) 项目，**仅关注**应用程序在 Linux Docker 容器中运行所需的所有更改。容器化应考虑此处指定的所有设置。

遵守容器化 .NET Core 应用程序的最佳实践，确保容器在性能、安全性和可维护性方面得到优化。

## 容器化设置

本提示的此部分包含容器化 ASP.NET Core 应用程序所需的特定设置和配置。在运行此提示之前，请确保填写了必要的信息。请注意，在许多情况下，仅需要前几个设置。如果项目不适用，后续设置可以保留默认值。

未指定的任何设置将被设置为默认值。默认值以 `[ ]` 括号提供。

### 基础项目信息
1. 要容器化的项目: 
   - `[项目名称（提供 .csproj 文件路径）]`

2. 要使用的 .NET 版本:
   - `[8.0 或 9.0（默认 8.0）]`

3. 要使用的 Linux 发行版:
   - `[debian, alpine, ubuntu, chiseled 或 Azure Linux（mariner）（默认 debian）]`

4. Docker 镜像构建阶段的自定义基础镜像（"None" 表示使用标准的 Microsoft 基础镜像）:
   - `[指定构建阶段使用的基础镜像（默认 None）]`

5. Docker 镜像运行阶段的自定义基础镜像（"None" 表示使用标准的 Microsoft 基础镜像）:
   - `[指定运行阶段使用的基础镜像（默认 None）]`   

### 容器配置
1. 必须在容器镜像中暴露的端口:
   - 主 HTTP 端口: `[例如，8080]`
   - 额外端口: `[列出任何额外端口，或 "None"]`

2. 容器应以哪个用户账户运行:
   - `[用户账户，或默认为 "$APP_UID"]`

3. 应用程序 URL 配置:
   - `[指定 ASPNETCORE_URLS，或默认为 "http://+:8080"]`

### 构建配置
1. 构建容器镜像前必须执行的自定义构建步骤:
   - `[列出任何特定的构建步骤，或 "None"]`

2. 构建容器镜像后必须执行的自定义构建步骤:
   - `[列出任何特定的构建步骤，或 "None"]`

3. 必须配置的 NuGet 包源:
   - `[列出任何带有认证细节的私有 NuGet 馈源，或 "None"]`

### 依赖项
1. 必须安装在容器镜像中的系统包:
   - `[所选 Linux 发行版的包名，或 "None"]`

2. 必须复制到容器镜像中的本地库:
   - `[库名和路径，或 "None"]`

3. 必须安装的额外 .NET 工具:
   - `[工具名和版本，或 "None"]`

### 系统配置
1. 必须在容器镜像中设置的环境变量:
   - `[变量名和值，或 "使用默认值"]`

### 文件系统
1. 需要复制到容器镜像中的文件/目录:
   - `[相对于项目根目录的路径，或 "None"]`
   - 容器中的目标位置: `[容器路径，或 "不适用"]`

2. 需要从容器化中排除的文件/目录:
   - `[要排除的路径，或 "None"]`

3. 应该配置的卷挂载点:
   - `[持久化数据的卷路径，或 "None"]`

### .dockerignore 配置
1. 需要包含在 `.dockerignore` 文件中的模式（`.dockerignore` 文件已包含常见默认模式；这些是额外的模式）:
   - 额外模式: `[列出任何额外模式，或 "None"]`

### 健康检查配置
1. 健康检查端点:
   - `[健康检查 URL 路径，或 "None"]`

2. 健康检查间隔和超时:
   - `[间隔和超时值，或 "使用默认值"]`

### 其他说明
1. 容器化项目必须遵循的其他说明:
   - `[特定要求，或 "None"]`

2. 需要解决的已知问题:
   - `[描述任何已知问题，或 "None"]`

## 范围

- ✅ 应用配置修改以确保应用程序设置和连接字符串可以从环境变量读取
- ✅ 创建和配置 ASP.NET Core 应用程序的 Dockerfile
- ✅ 在 Dockerfile 中指定多个阶段以构建/发布应用程序并将输出复制到最终镜像
- ✅ 配置 Linux 容器平台兼容性（Alpine、Ubuntu、Chiseled 或 Azure Linux（Mariner））
- ✅ 正确处理依赖项（系统包、本地库、额外工具等）
- ❌ 不进行基础设施设置（假设由其他部分处理）
- ❌ 仅进行容器化所需的代码更改，不进行超出需求的任何代码更改

## 执行过程

1. 查看上述容器化设置以了解容器化需求
2. 创建 `progress.md` 文件以跟踪更改并打勾标记
3. 通过检查项目中的 `TargetFramework` 元素来确定 .NET 版本
4. 根据以下内容选择适当的 Linux 容器镜像：
   - 从项目中检测到的 .NET 版本
   - 容器化设置中指定的 Linux 发行版（Alpine、Ubuntu、Chiseled 或 Azure Linux（Mariner））
   - 如果用户未在容器化设置中请求特定的基础镜像，则基础镜像必须是有效的 mcr.microsoft.com/dotnet 镜像，其标签如下面的示例 Dockerfile 或文档所示
   - 官方 Microsoft .NET 构建和运行时镜像标签：
      - SDK 镜像标签（用于构建阶段）：https://github.com/dotnet/dotnet-docker/blob/main/README.sdk.md
      - ASP.NET Core 运行时镜像标签：https://github.com/dotnet/dotnet-docker/blob/main/README.aspnet.md
      - .NET 运行时镜像标签：https://github.com/dotnet/dotnet-docker/blob/main/README.runtime.md
5. 在项目目录根部创建 Dockerfile 以容器化应用程序
   - Dockerfile 应使用多个阶段：
     - 构建阶段：使用 .NET SDK 镜像构建应用程序
       - 首先复制 csproj 文件
       - 如果存在，复制 NuGet.config 并配置任何私有馈源
       - 恢复 NuGet 包
       - 然后复制其余源代码并构建和发布应用程序到 /app/publish
     - 最终阶段：使用选定的 .NET 运行时镜像运行应用程序
       - 将工作目录设置为 /app
       - 按照指示设置用户（默认为非 root 用户（例如，`$APP_UID`））
         - 除非在容器化设置中另有说明，否则不需要创建新用户。使用 `$APP_UID` 变量指定用户账户。
       - 从构建阶段复制已发布的输出到最终镜像
   - 确保考虑容器化设置中的所有要求：
     - .NET 版本和 Linux 发行版
     - 暴露的端口
     - 容器的用户账户
     - ASPNETCORE_URLS 配置
     - 系统包安装
     - 本地库依赖项
     - 额外的 .NET 工具
     - 环境变量
     - 文件/目录复制
     - 卷挂载点
     - 健康检查配置
6. 在项目目录根部创建 `.dockerignore` 文件以排除 Docker 镜像中不必要的文件。`.dockerignore` 文件 **必须** 包含以下元素以及容器化设置中指定的额外模式：
   - bin/
   - obj/
   - .dockerignore
   - Dockerfile
   - .git/
   - .github/
   - .vs/
   - .vscode/
   - **/node_modules/
   - *.user
   - *.suo
   - **/.DS_Store
   - **/Thumbs.db
   - 容器化设置中指定的任何额外模式
7. 如果容器化设置中指定了健康检查，请进行配置：
   - 如果提供了健康检查端点，请在 Dockerfile 中添加 HEALTHCHECK 指令
   - 使用 curl 或 wget 检查健康检查端点
8. 标记任务为完成：[ ] → [✓]
9. 继续直到所有任务完成且 Docker 构建成功

## 构建和运行时验证

一旦 Dockerfile 完成，确认 Docker 构建成功。使用以下命令构建 Docker 镜像：

```bash
docker build -t aspnetcore-app:latest .
```

如果构建失败，请审查错误信息并根据需要调整 Dockerfile 或项目配置。报告成功或失败。

## 进度跟踪

维护一个 `progress.md` 文件，结构如下：
```markdown
# 容器化进度

## 环境检测
- [ ] .NET 版本检测（版本：___）
- [ ] Linux 发行版选择（发行版：___）

## 配置更改
- [ ] 验证应用程序配置以支持环境变量
- [ ] 配置 NuGet 包源（如适用）

## 容器化
- [ ] 创建 Dockerfile
- [ ] 创建 .dockerignore 文件
- [ ] 构建阶段使用 SDK 镜像
- [ ] 复制 csproj 文件以进行包恢复
- [ ] 如有需要，复制 NuGet.config 文件
- [ ] 使用运行时镜像创建运行阶段
- [ ] 配置非 root 用户
- [ ] 依赖项处理（系统包、本地库、工具等）
- [ ] 健康检查配置（如适用）
- [ ] 实现特殊要求

## 验证
- [ ] 审查容器化设置并确保所有要求都已满足
- [ ] Docker 构建成功
```

在步骤之间不要暂停确认。继续有条不紊地进行，直到应用程序完成容器化且 Docker 构建成功。

**直到所有复选框都被标记，你才算完成！** 这包括成功构建 Docker 镜像以及解决构建过程中出现的任何问题。

## 示例 Dockerfile

一个使用 Linux 基础镜像的 ASP.NET Core (.NET) 应用程序的示例 Dockerfile。

```dockerfile
# ============================================================
# 阶段 1：构建和发布应用程序
# ============================================================

# 基础镜像 - 选择适当的 .NET SDK 版本和 Linux 发行版
# 可能的标签包括：
# - 8.0-bookworm-slim（Debian 12）
# - 8.0-noble（Ubuntu 24.04）
# - 8.0-alpine（Alpine Linux）
# - 9.0-bookworm-slim（Debian 12）
# - 9.0-noble（Ubuntu 24.04）
# - 9.0-alpine（Alpine Linux）
# 使用 .NET SDK 镜像构建应用程序
FROM mcr.microsoft.com/dotnet/sdk:8.0-bookworm-slim AS build
ARG BUILD_CONFIGURATION=Release

WORKDIR /src

# 首先复制项目文件以实现更好的缓存
COPY ["YourProject/YourProject.csproj", "YourProject/"]
COPY ["YourOtherProject/YourOtherProject.csproj", "YourOtherProject/"]

# 如果存在，复制 NuGet 配置文件
COPY ["NuGet.config", "."]

# 恢复 NuGet 包
RUN dotnet restore "YourProject/YourProject.csproj"

# 复制源代码
COPY . .

# 在此处执行自定义预构建步骤（如需）
# RUN echo "运行预构建步骤..."

# 构建和发布应用程序
WORKDIR "/src/YourProject"
RUN dotnet build "YourProject.csproj" -c $BUILD_CONFIGURATION -o /app/build

# 发布应用程序
RUN dotnet publish "YourProject.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

# 在此处执行自定义后构建步骤（如需）
# RUN echo "运行后构建步骤..."

# ============================================================
# 阶段 2：最终运行时镜像
# ============================================================

# 基础镜像 - 选择适当的 .NET 运行时版本和 Linux 发行版
# 可能的标签包括：
# - 8.0-bookworm-slim（Debian 12）
# - 8.0-noble（Ubuntu 24.04）
# - 8.0-alpine（Alpine Linux）
# - 8.0-noble-chiseled（Ubuntu 24.04 Chiseled）
# - 8.0-azurelinux3.0（Azure Linux）
# - 9.0-bookworm-slim（Debian 12）
# - 9.0-noble（Ubuntu 24.04）
# - 9.0-alpine（Alpine Linux）
# - 9.0-noble-chiseled（Ubuntu 24.04 Chiseled）
# - 9.0-azurelinux3.0（Azure Linux）
# 使用 .NET 运行时镜像运行应用程序
FROM mcr.microsoft.com/dotnet/aspnet:8.0-bookworm-slim AS final

# 安装系统包（如需）（取消注释并根据需要修改）
# RUN apt-get update && apt-get install -y \
#     curl \
#     wget \
#     ca-certificates \
#     libgdiplus \
#     && rm -rf /var/lib/apt/lists/*

# 安装额外的 .NET 工具（如需）（取消注释并根据需要修改）
# RUN dotnet tool install --global dotnet-ef --version 8.0.0
# ENV PATH="$PATH:/root/.dotnet/tools"

WORKDIR /app

# 从构建阶段复制已发布的应用程序
COPY --from=build /app/publish .

# 复制其他文件（如需）（取消注释并根据需要修改）
# COPY ./config/appsettings.Production.json .
# COPY ./certificates/ ./certificates/

# 设置环境变量
ENV ASPNETCORE_ENVIRONMENT=Production
ENV ASPNETCORE_URLS=http://+:8080

# 添加自定义环境变量（如需）（取消注释并根据需要修改）
# ENV CONNECTIONSTRINGS__DEFAULTCONNECTION="your-connection-string"
# ENV FEATURE_FLAG_ENABLED=true

# 配置 SSL/TLS 证书（如需）（取消注释并根据需要修改）
# ENV ASPNETCORE_Kestrel__Certificates__Default__Path=/app/certificates/app.pfx
# ENV ASPNETCORE_Kestrel__Certificates__Default__Password=your_password

# 暴露应用程序监听的端口
EXPOSE 8080
# EXPOSE 8081  # 如果使用 HTTPS，请取消注释

# 安装 curl 用于健康检查（如果尚未安装）
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 配置健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# 为持久化数据创建卷（如需）（取消注释并根据需要修改）
# VOLUME ["/app/data", "/app/logs"]

# 为安全起见切换到非 root 用户
USER $APP_UID

# 设置应用程序的入口点
ENTRYPOINT ["dotnet", "YourProject.dll"]
```

## 适应此示例

**注意：** 根据容器化设置中的具体要求自定义此模板。

在适应此示例 Dockerfile 时：

1. 将 `YourProject.csproj`、`YourProject.dll` 等替换为您的实际项目名称
2. 根据需要调整 .NET 版本和 Linux 发行版
3. 根据您的需求修改依赖项安装步骤并删除任何不必要的步骤
4. 配置特定于您应用程序的环境变量
5. 根据您的特定工作流添加或删除阶段
6. 将健康检查端点更新为与您的应用程序健康检查路由匹配

## Linux 发行版差异

### Alpine Linux
为了获得更小的镜像大小，您可以使用 Alpine Linux：

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
# ... 构建步骤 ...
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS final
# 使用 apk 安装包
RUN apk update && apk add --no-cache curl ca-certificates
```

### Ubuntu Chiseled
为了最小化攻击面，考虑使用 chiseled 镜像：

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0-jammy-chiseled AS final
# 注意：Chiseled 镜像包含最少的包，因此您可能需要使用不同的基础镜像来安装额外依赖项
```

### Azure Linux（Mariner）
对于 Azure 优化的容器：

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0-azurelinux3.0 AS final
# 使用 tdnf 安装包
RUN tdnf update -y && tdnf install -y curl ca-certificates && tdnf clean all
```

## 阶段命名说明

- `AS stage-name` 语法为每个阶段命名
- 使用 `--from=stage-name` 从先前阶段复制文件
- 您可以有多个中间阶段，这些阶段不会用于最终镜像
- `final` 阶段是最终容器镜像
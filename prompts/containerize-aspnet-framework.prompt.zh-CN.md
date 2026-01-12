

---
agent: 'agent'
tools: ['search/codebase', 'edit/editFiles', 'terminalCommand']
description: '通过创建针对项目的 Dockerfile 和 .dockerfile 文件来容器化 ASP.NET .NET Framework 项目。'
---

# ASP.NET .NET Framework 容器化提示

根据以下容器化设置，容器化指定的 ASP.NET (.NET Framework) 项目，专注于**仅限**应用程序在 Windows Docker 容器中运行所需的更改。容器化应考虑此处指定的所有设置。

**请注意：** 这是一个 .NET Framework 应用程序，而不是 .NET Core。容器化过程将与 .NET Core 应用程序不同。

## 容器化设置

本提示的此部分包含容器化 ASP.NET (.NET Framework) 应用程序所需的特定设置和配置。在运行此提示之前，请确保填写了必要的信息。请注意，在许多情况下，只需填写前几个设置。如果这些设置不适用于被容器化的项目，后续设置可以保留默认值。

任何未指定的设置将设置为默认值。默认值以 `[ ]` 括起。

### 基本项目信息
1. 要容器化的项目：  
   - `[项目名称（提供 .csproj 文件的路径）]`

2. 要使用的 Windows Server SKU：  
   - `[Windows Server Core（默认）或 Windows Server Full]`

3. 要使用的 Windows Server 版本：  
   - `[2022、2019 或 2016（默认 2022）]`

4. Docker 镜像构建阶段的自定义基础镜像（"None" 表示使用标准的 Microsoft 基础镜像）：  
   - `[指定构建阶段使用的自定义基础镜像（默认 None）]`

5. Docker 镜像运行阶段的自定义基础镜像（"None" 表示使用标准的 Microsoft 基础镜像）：  
   - `[指定运行阶段使用的自定义基础镜像（默认 None）]`  

### 容器配置
1. 必须在容器镜像中暴露的端口：  
   - 主 HTTP 端口：`[例如，80]`  
   - 其他端口：`[列出任何其他端口，或 "None"]`

2. 容器应以哪个用户账户运行：  
   - `[用户账户，或默认为 "ContainerUser"]`

3. 必须在容器镜像中配置的 IIS 设置：  
   - `[列出任何特定的 IIS 设置，或 "None"]`

### 构建配置
1. 构建容器镜像前必须执行的自定义构建步骤：  
   - `[列出任何特定的构建步骤，或 "None"]`

2. 构建容器镜像后必须执行的自定义构建步骤：  
   - `[列出任何特定的构建步骤，或 "None"]`

### 依赖项
1. 应在容器镜像中注册的 .NET 程序集：  
   - `[程序集名称和版本，或 "None"]`

2. 必须复制到容器镜像并安装的 MSI 文件：  
   - `[MSI 文件名称和版本，或 "None"]`

3. 必须在容器镜像中注册的 COM 组件：  
   - `[COM 组件名称，或 "None"]`

### 系统配置
1. 必须添加到容器镜像的注册表键和值：  
   - `[注册表路径和值，或 "None"]`

2. 必须在容器镜像中设置的环境变量：  
   - `[变量名称和值，或 "使用默认值"]`

3. 必须在容器镜像中安装的 Windows Server 角色和功能：  
   - `[角色/功能名称，或 "None"]`

### 文件系统
1. 需要复制到容器镜像的文件/目录：  
   - `[相对于项目根目录的路径，或 "None"]`  
   - 容器中的目标位置：`[容器路径，或 "不适用"]`

2. 需要从容器化中排除的文件/目录：  
   - `[要排除的路径，或 "None"]`

### .dockerignore 配置
1. 需要包含在 `.dockerignore` 文件中的模式（`.dockerignore` 文件已包含常见默认模式；这些是额外的模式）：  
   - 额外模式：`[列出任何额外模式，或 "None"]`

### 健康检查配置
1. 健康检查端点：  
   - `[健康检查 URL 路径，或 "None"]`

2. 健康检查间隔和超时：  
   - `[间隔和超时值，或 "使用默认值"]`

### 额外说明
1. 容器化项目必须遵循的其他说明：  
   - `[特定要求，或 "None"]`

2. 需要解决的已知问题：  
   - `[描述任何已知问题，或 "None"]`

## 范围

- ✅ 修改应用程序配置以确保使用配置构建器从环境变量读取应用程序设置和连接字符串  
- ✅ 创建和配置 ASP.NET 应用程序的 Dockerfile  
- ✅ 在 Dockerfile 中指定多个阶段以构建/发布应用程序并将输出复制到最终镜像  
- ✅ 配置 Windows 容器平台兼容性（Windows Server Core 或 Full）  
- ✅ 正确处理依赖项（GAC 程序集、MSI、COM 组件、注册表键、环境变量、Windows 角色和功能、文件/目录等）  
- ❌ 不进行基础设施设置（假设由其他方式单独处理）  
- ❌ 除容器化所需外，不进行其他代码更改

## 执行流程

1. 审阅上述容器化设置以了解容器化需求  
2. 创建 `progress.md` 文件以跟踪完成情况（使用复选标记）  
3. 通过检查项目中的 `.csproj` 文件的 `TargetFrameworkVersion` 元素来确定所需的 .NET Framework 版本  
4. 根据以下内容选择适当的 Windows Server 容器镜像：  
   - 从项目中检测到的 .NET Framework 版本  
   - 容器化设置中指定的 Windows Server SKU（Core 或 Full）  
   - 容器化设置中指定的 Windows Server 版本（2016、2019 或 2022）  
   - Windows Server Core 标签可在以下链接中找到：https://github.com/microsoft/dotnet-framework-docker/blob/main/README.aspnet.md#full-tag-listing  
5. 确保所需的 NuGet 包已安装。**如果缺失，请不要安装**。如果未安装，用户必须手动安装。如果未安装，请暂停执行此提示，并要求用户使用 Visual Studio NuGet 包管理器或 Visual Studio 包管理器控制台进行安装。以下包是必需的：  
   - `Microsoft.Configuration.ConfigurationBuilders.Environment`  
6. 修改 `web.config` 文件，添加配置构建器部分并配置从环境变量读取应用程序设置和连接字符串：  
   - 在 `configSections` 中添加 `ConfigBuilders` 部分  
   - 在根目录中添加 `configBuilders` 部分  
   - 为 `appSettings` 和 `connectionStrings` 配置 `EnvironmentConfigBuilder`  
   - 示例模式：  
     ```xml
     <configSections>
       <section name="configBuilders" type="System.Configuration.ConfigurationBuildersSection, System.Configuration, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a" restartOnExternalChanges="false" requirePermission="false" />
     </configSections>
     <configBuilders>
       <builders>
         <add name="Environment" type="Microsoft.Configuration.ConfigurationBuilders.EnvironmentConfigBuilder, Microsoft.Configuration.ConfigurationBuilders.Environment" />
       </builders>
     </configBuilders>
     <appSettings configBuilders="Environment">
       <!-- 现有应用程序设置 -->
     </appSettings>
     <connectionStrings configBuilders="Environment">
       <!-- 现有连接字符串 -->
     </connectionStrings>
     ```  
7. 在将要创建 Dockerfile 的文件夹中创建 `LogMonitorConfig.json` 文件，通过复制此提示末尾提供的参考 `LogMonitorConfig.json` 文件。文件内容 **必须不修改**，除非容器化设置中有特别说明，否则必须与参考内容完全一致。  
   - 特别注意：确保不更改要记录的问题级别，因为使用 `Information` 级别记录 EventLog 源会导致不必要的日志噪声。  
8. 在项目目录根部创建 Dockerfile 以容器化应用程序  
   - Dockerfile 应使用多阶段构建：  
     - 构建阶段：使用 Windows Server Core 镜像构建应用程序  
       - 构建阶段 **必须** 使用 `mcr.microsoft.com/dotnet/framework/sdk` 基础镜像，除非设置文件中指定了自定义基础镜像  
       - 首先复制 sln、csproj 和 packages.config 文件  
       - 如果存在，复制 NuGet.config 文件并配置任何私有源  
       - 恢复 NuGet 包  
       - 然后复制其余源代码并使用 MSBuild 构建和发布应用程序到 C:\publish  
     - 最终阶段：使用选定的 Windows Server 镜像运行应用程序  
       - 最终阶段 **必须** 使用 `mcr.microsoft.com/dotnet/framework/aspnet` 基础镜像，除非设置文件中指定了自定义基础镜像  
       - 将 `LogMonitorConfig.json` 文件复制到容器中的某个目录（例如 C:\LogMonitor）  
       - 从 Microsoft 存储库下载 LogMonitor.exe 到同一目录  
           - 正确的 LogMonitor.exe URL 是：https://github.com/microsoft/windows-container-tools/releases/download/v2.1.1/LogMonitor.exe  
       - 将工作目录设置为 C:\inetpub\wwwroot  
       - 将构建阶段发布的输出复制到最终镜像  
       - 将容器的入口点设置为运行 LogMonitor.exe 以监控 IIS 服务  
           - `ENTRYPOINT [ "C:\\LogMonitor\\LogMonitor.exe", "C:\\ServiceMonitor.exe", "w3svc" ]`  
   - 确保考虑容器化设置中的所有要求：  
     - Windows Server SKU 和版本  
     - 暴露的端口  
     - 容器的用户账户  
     - IIS 设置  
     - GAC 程序集注册  
     - MSI 安装  
     - COM 组件注册  
     - 注册表键  
     - 环境变量  
     - Windows 角色和功能  
     - 文件/目录复制  
   - 以本提示末尾提供的示例为模型创建 Dockerfile，但确保其根据特定项目需求和设置进行定制。  
   - **重要：** 除非用户在设置文件中明确请求使用完整版 Windows Server 镜像，否则使用 Windows Server Core 基础镜像。  
9. 在项目目录根部创建 `.dockerignore` 文件，以排除 Docker 镜像中不必要的文件。`.dockerignore` 文件 **必须** 包含以下元素以及容器化设置中指定的额外模式：  
   - packages/  
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
   - 容器化设置中指定的任何其他模式  
10. 如果设置中指定了健康检查，请在 Dockerfile 中配置健康检查：  
   - 如果提供了健康检查端点，请添加 `HEALTHCHECK` 指令  
11. 通过向项目文件中添加以下项将 Dockerfile 添加到项目中：`<None Include="Dockerfile" />`  
12. 标记任务为完成：[ ] → [✓]  
13. 持续进行，直到所有任务完成且 Docker 构建成功

## 构建和运行时验证

在完成 Dockerfile 后，确认 Docker 构建成功。使用以下命令构建 Docker 镜像：

```bash
docker build -t aspnet-app:latest .
```

如果构建失败，请审阅错误信息并根据需要调整 Dockerfile 或项目配置。报告构建成功或失败。

## 进度跟踪

维护一个 `progress.md` 文件，结构如下：
```markdown
# 容器化进度

## 环境检测
- [ ] .NET Framework 版本检测（版本：___）
- [ ] Windows Server SKU 选择（SKU：___）
- [ ] Windows Server 版本选择（版本：___）

## 配置更改
- [ ] 对 web.config 进行配置构建器修改
- [ ] 配置 NuGet 包源（如适用）
- [ ] 复制 LogMonitorConfig.json 并根据设置需求进行调整

## 容器化
- [ ] 创建 Dockerfile
- [ ] 创建 .dockerignore 文件
- [ ] 构建阶段使用 SDK 镜像
- [ ] 复制 sln、csproj、packages.config 文件（如适用，复制 NuGet.config 文件以配置包源）
- [ ] 运行时阶段使用运行时镜像
- [ ] 配置非管理员用户
- [ ] 依赖项处理（GAC 程序集、MSI、COM、注册表、其他文件等）
- [ ] 健康检查配置（如适用）
- [ ] 特殊需求实现

## 验证
- [ ] 审阅容器化设置并确保所有需求得到满足
- [ ] Docker 构建成功
```

在步骤之间不要暂停确认。持续按流程执行，直到应用程序完成容器化且 Docker 构建成功。

**直到所有复选框都被标记，你才算完成！** 这包括成功构建 Docker 镜像以及解决构建过程中出现的任何问题。

## 参考资料

### 示例 Dockerfile

使用 Windows Server Core 基础镜像的 ASP.NET (.NET Framework) 应用程序的示例 Dockerfile。

```dockerfile
# escape=`
# 转义指令将转义字符从 \ 改为 `
# 在 Windows Dockerfile 中尤其有用

# ============================================================
# 阶段 1：构建和发布应用程序
# ============================================================

# 基础镜像 - 选择适当的 .NET Framework 版本和 Windows Server Core 版本
# 可能的标签包括：
# - 4.8.1-windowsservercore-ltsc2025（Windows Server 2025）
# - 4.8-windowsservercore-ltsc2022（Windows Server 2022）
# - 4.8-windowsservercore-ltsc2019（Windows Server 2019）
# - 4.8-windowsservercore-ltsc2016（Windows Server 2016）
# - 4.7.2-windowsservercore-ltsc2019（Windows Server 2019）
# - 4.7.2-windowsservercore-ltsc2016（Windows Server 2016）
# - 4.7.1-windowsservercore-ltsc2016（Windows Server 2016）
# - 4.7-windowsservercore-ltsc2016（Windows Server 2016）
# - 4.6.2-windowsservercore-ltsc2016（Windows Server 2016）
# - 3.5-windowsservercore-ltsc2025（Windows Server 2025）
# - 3.5-windowsservercore-ltsc2022（Windows Server 2022）
# - 3.5-windowsservercore-ltsc2019（Windows Server 2019）
# - 3.5-windowsservercore-ltsc2019（Windows Server 2016）
# 使用 .NET Framework SDK 镜像构建应用程序
FROM mcr.microsoft.com/dotnet/framework/sdk:4.8-windowsservercore-ltsc2022 AS build
ARG BUILD_CONFIGURATION=Release

# 设置默认 shell 为 PowerShell
SHELL ["powershell", "-command"]

WORKDIR /app

# 复制解决方案和项目文件
COPY YourSolution.sln .
COPY YourProject/*.csproj ./YourProject/
COPY YourOtherProject/*.csproj ./YourOtherProject/

# 复制 packages.config 文件
COPY YourProject/packages.config ./YourProject/
COPY YourOtherProject/packages.config ./YourOtherProject/

# 恢复 NuGet 包
RUN nuget restore YourSolution.sln

# 复制源代码
COPY . .

# 在此处执行自定义预构建步骤（如需要）

# 使用 MSBuild 构建并发布应用程序到 C:\publish
RUN msbuild /p:Configuration=$BUILD_CONFIGURATION `
            /p:WebPublishMethod=FileSystem `
            /p:PublishUrl=C:\publish `
            /p:DeployDefaultTarget=WebPublish

# 在此处执行自定义后构建步骤（如需要）

# ============================================================
# 阶段 2：最终运行时镜像
# ============================================================

# 基础镜像 - 选择适当的 .NET Framework 版本和 Windows Server Core 版本
# 可能的标签包括：
# - 4.8.1-windowsservercore-ltsc2025（Windows Server 2025）
# - 4.8-windowsservercore-ltsc2022（Windows Server 2022）
# - 4.8-windowsservercore-ltsc2019（Windows Server 2019）
# - 4.8-windowsservercore-ltsc2016（Windows Server 2016）
# - 4.7.2-windowsservercore-ltsc2019（Windows Server 2019）
# - 4.7.2-windowsservercore-ltsc2016（Windows Server 2016）
# - 4.7.1-windowsservercore-ltsc2016（Windows Server 2016）
# - 4.7-windowsservercore-ltsc2016（Windows Server 2016）
# - 4.6.2-windowsservercore-ltsc2016（Windows Server 2016）
# - 3.5-windowsservercore-ltsc2025（Windows Server 2025）
# - 3.5-windowsservercore-ltsc2022（Windows Server 2022）
# - 3.5-windowsservercore-ltsc2019（Windows Server 2019）
# - 3.5-windowsservercore-ltsc2019（Windows Server 2016）
# 使用 .NET Framework ASP.NET 镜像运行应用程序
FROM mcr.microsoft.com/dotnet/framework/aspnet:4.8-windowsservercore-ltsc2022

# 设置默认 shell 为 PowerShell
SHELL ["powershell", "-command"]

WORKDIR /inetpub/wwwroot

# 从构建阶段复制文件
COPY --from=build /publish .

# 添加应用程序所需的任何额外环境变量（如需取消注释并修改）
# ENV KEY=VALUE

# 安装 MSI 包（如需取消注释并修改）
# COPY ./msi-installers C:/Installers
# RUN Start-Process -Wait -FilePath 'msiexec.exe' -ArgumentList '/i', 'C:\Installers\your-package.msi', '/quiet', '/norestart'

# 安装自定义 Windows Server 角色和功能（如需取消注释并修改）
# RUN dism /Online /Enable-Feature /FeatureName:YOUR-FEATURE-NAME

# 添加额外的 Windows 功能（如需取消注释并修改）
# RUN Add-WindowsFeature Some-Windows-Feature; `
#    Add-WindowsFeature Another-Windows-Feature

# 如果需要安装 MSI 包，请取消注释并修改
# COPY ./msi-installers C:/Installers
# RUN Start-Process -Wait -FilePath 'msiexec.exe' -ArgumentList '/i', 'C:\Installers\your-package.msi', '/quiet', '/norestart'

# 如果需要在 GAC 中注册程序集，请取消注释并修改
# COPY ./assemblies C:/Assemblies
# RUN C:\Windows\Microsoft.NET\Framework64\v4.0.30319\gacutil -i C:/Assemblies/YourAssembly.dll

# 如果需要注册 COM 组件，请取消注释并修改
# COPY ./com-components C:/Components
# RUN regsvr32 /s C:/Components/YourComponent.dll

# 如果需要添加注册表键，请取消注释并修改
# RUN New-Item -Path 'HKLM:\Software\YourApp' -Force; `
#     Set-ItemProperty -Path 'HKLM:\Software\YourApp' -Name 'Setting' -Value 'Value'

# 如果需要配置 IIS 设置，请取消注释并修改
# RUN Import-Module WebAdministration; `
#     Set-ItemProperty 'IIS:\AppPools\DefaultAppPool' -Name somePropertyName -Value 'SomePropertyValue'; `
#     Set-ItemProperty 'IIS:\Sites\Default Web Site' -Name anotherPropertyName -Value 'AnotherPropertyValue'

# 暴露必要端口 - 默认情况下，IIS 使用端口 80
EXPOSE 80
# EXPOSE 443  # 如果使用 HTTPS，请取消注释

# 从 microsoft/windows-container-tools 存储库复制 LogMonitor
WORKDIR /LogMonitor
RUN curl -fSLo LogMonitor.exe https://github.com/microsoft/windows-container-tools/releases/download/v2.1.1/LogMonitor.exe

# 从本地文件复制 LogMonitorConfig.json
COPY LogMonitorConfig.json .

# 设置非管理员用户
USER ContainerUser

# 覆盖容器的默认入口点以利用 LogMonitor
ENTRYPOINT [ "C:\\LogMonitor\\LogMonitor.exe", "C:\\ServiceMonitor.exe", "w3svc" ]
```

## 适配此示例

**注意：** 根据容器化设置中的具体要求自定义此模板。

在适配此示例 Dockerfile 时：

1. 将 `YourSolution.sln`、`YourProject.csproj` 等替换为实际的文件名  
2. 根据需要调整 Windows Server 和 .NET Framework 版本  
3. 根据需求修改依赖项安装步骤并删除任何不必要的步骤  
4. 根据特定工作流添加或删除阶段

## 阶段命名说明

- `AS stage-name` 语法为每个阶段命名  
- 使用 `--from=stage-name` 从先前阶段复制文件  
- 可以有多个中间阶段，这些阶段不会用于最终镜像
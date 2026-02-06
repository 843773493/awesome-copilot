---
name: winapp-cli
description: '用于构建、打包和部署 Windows 应用程序的 Windows 应用开发命令行工具 (winapp)。在需要初始化 Windows 应用项目、创建 MSIX 包、生成 AppxManifest.xml、管理开发证书、添加包身份以进行调试、签名包或访问 Windows SDK 构建工具时使用。支持 .NET、C++、Electron、Rust、Tauri 和面向 Windows 的跨平台框架。'
---

# Windows 应用开发命令行工具

Windows 应用开发命令行工具 (`winapp`) 是用于管理 Windows SDK、MSIX 打包、生成应用身份、清单文件、证书以及使用任何应用框架访问构建工具的命令行界面。它弥合了跨平台开发与 Windows 原生功能之间的差距。

## 使用场景

在需要以下操作时使用此工具：

- 使用 SDK 设置、清单文件和证书初始化 Windows 应用项目
- 从应用程序目录创建 MSIX 包
- 生成或管理 AppxManifest.xml 文件
- 创建并安装用于签名的开发证书
- 为调试 Windows API 添加包身份
- 签名 MSIX 包或可执行文件
- 从任何框架或构建系统访问 Windows SDK 构建工具
- 使用跨平台框架（Electron、Rust、Tauri、Qt）构建 Windows 应用
- 为 Windows 应用部署设置持续集成/持续交付 (CI/CD) 流水线
- 访问需要包身份的 Windows API（通知、Windows AI、壳集成等）

## 先决条件

- Windows 10 或更高版本
- 通过以下方式之一安装 winapp CLI：
  - **WinGet**: `winget install Microsoft.WinAppCli --source winget`
  - **NPM**（用于 Electron）: `npm install @microsoft/winappcli --save-dev`
  - **GitHub Actions/Azure DevOps**: 使用 [setup-WinAppCli](https://github.com/microsoft/setup-WinAppCli) 动作
  - **手动安装**: 从 [GitHub 发布](https://github.com/microsoft/WinAppCli/releases/latest) 下载

## 核心功能

### 1. 项目初始化 (`winapp init`)

使用默认设置初始化目录，包含构建现代 Windows 应用所需的资产（清单、证书、库）。支持 SDK 安装模式：`stable`（稳定版）、`preview`（预览版）、`experimental`（实验版）或 `none`（无）。

### 2. MSIX 打包 (`winapp pack`)

从准备好的目录创建 MSIX 包，支持可选的签名、证书生成和自包含部署捆绑。

### 3. 调试包身份 (`winapp create-debug-identity`)

无需完整打包，即可为可执行文件添加临时包身份，用于调试需要身份的 Windows API（通知、Windows AI、壳集成等）。

### 4. 清单文件管理 (`winapp manifest`)

生成 AppxManifest.xml 文件，并从源图像自动更新图像资产，创建所有必需的尺寸和纵横比。

### 5. 证书管理 (`winapp cert`)

生成开发证书并将其安装到本地机器存储中，用于签名包。

### 6. 包签名 (`winapp sign`)

使用 PFX 证书对 MSIX 包和可执行文件进行签名，支持可选的时间戳服务器。

### 7. 访问 SDK 构建工具 (`winapp tool`)

从任何框架或构建系统运行 Windows SDK 构建工具，确保路径正确配置。

## 使用示例

### 示例 1：初始化并打包 Windows 应用

```bash
# 使用默认设置初始化工作区
winapp init

# 构建您的应用程序（框架特定）
# ...

# 创建带签名的 MSIX 包
winapp pack ./build-output --generate-cert --output MyApp.msix
```

### 示例 2：使用包身份调试

```bash
# 为测试 Windows API 为可执行文件添加调试身份
winapp create-debug-identity ./bin/MyApp.exe

# 运行您的应用 - 现在具有包身份
./bin/MyApp.exe
```

### 示例 3：CI/CD 流水线设置

```yaml
# GitHub Actions 示例
- name: 设置 winapp CLI
  uses: microsoft/setup-WinAppCli@v1

- name: 初始化并打包
  run: |
    winapp init --no-prompt
    winapp pack ./build-output --output MyApp.msix
```

### 示例 4：Electron 应用集成

```bash
# 通过 npm 安装
npm install @microsoft/winappcli --save-dev

# 初始化并为 Electron 添加调试身份
npx winapp init
npx winapp node add-electron-debug-identity

# 为分发打包
npx winapp pack ./out --output MyElectronApp.msix
```

## 使用指南

1. **首先运行 `winapp init`** - 在使用其他命令之前，始终初始化项目以确保 SDK 设置、清单文件和证书已配置。
2. **在清单文件更改后重新运行 `create-debug-identity`** - 每次修改 AppxManifest.xml 文件后，必须重新生成包身份。
3. **在 CI/CD 中使用 `--no-prompt`** - 通过使用默认值避免交互式提示，适用于自动化流水线。
4. **使用 `winapp restore` 用于共享项目** - 通过 `winapp.yaml` 重新创建跨机器的精确环境状态。
5. **从单个图像生成资产** - 使用 `winapp manifest update-assets` 命令，通过一个 logo 生成所有必需的图标尺寸。

## 常见模式

### 模式：初始化新项目

```bash
cd my-project
winapp init
# 生成：AppxManifest.xml、开发证书、SDK 配置、winapp.yaml
```

### 模式：使用现有证书打包

```bash
winapp pack ./build-output --cert ./mycert.pfx --cert-password secret --output MyApp.msix
```

### 模式：自包含部署

```bash
# 将 Windows 应用 SDK 运行时捆绑到包中
winapp pack ./my-app --self-contained --generate-cert
```

### 模式：更新包版本

```bash
# 更新到最新的稳定版 SDK
winapp update

# 或更新到预览版 SDK
winapp update --setup-sdks preview
```

## 局限性

- 需要 Windows 10 或更高版本（Windows 专用 CLI）
- 包身份调试需要在任何清单文件更改后重新运行 `create-debug-identity`
- 自包含部署通过捆绑 Windows 应用 SDK 运行时增加包大小
- 开发证书仅用于测试；生产环境需要受信任的证书
- 某些 Windows API 需要在清单文件中声明特定的权限
- winapp CLI 处于公开预览版，可能会发生变更

## 通过包身份启用的 Windows API

包身份解锁了强大的 Windows API 访问权限：

| API 类别 | 示例 |
| -------- | ---- |
| **通知** | 交互式原生通知、通知管理 |
| **Windows AI** | 设备端大语言模型（LLM）、文本/图像 AI API（Phi Silica、Windows ML） |
| **壳集成** | 探索器、任务栏、分享面板集成 |
| **协议处理程序** | 自定义 URI 方案 (`yourapp://`) |
| **设备访问** | 相机、麦克风、位置（需用户授权） |
| **后台任务** | 应用程序关闭时运行 |
| **文件关联** | 用您的应用程序打开特定文件类型 |

## 常见问题排查

| 问题 | 解决方案 |
| ---- | -------- |
| 证书不受信任 | 运行 `winapp cert install <cert-path>` 将证书安装到本地机器存储中 |
| 包身份不工作 | 在任何清单文件更改后运行 `winapp create-debug-identity` |
| 未找到 SDK | 运行 `winapp restore` 或 `winapp update` 确保 SDK 已安装 |
| 签名失败 | 验证证书密码并确保证书未过期 |

## 参考资料

- [GitHub 仓库](https://github.com/microsoft/WinAppCli)
- [完整 CLI 文档](https://github.com/microsoft/WinAppCli/blob/main/docs/usage.md)
- [示例应用程序](https://github.com/microsoft/WinAppCli/tree/main/samples)
- [Windows 应用 SDK](https://learn.microsoft.com/windows/apps/windows-app-sdk/)
- [MSIX 打包概述](https://learn.microsoft.com/windows/msix/overview)
- [包身份概述](https://learn.microsoft.com/windows/apps/desktop/modernize/package-identity-overview)

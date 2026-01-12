

---
name: appinsights-instrumentation
description: '对Web应用进行仪器化，以将有用的遥测数据发送到Azure应用洞察（App Insights）'
---

# 应用洞察（App Insights）仪器化

该技能可启用将Web应用的遥测数据发送到Azure应用洞察（App Insights），以实现对应用程序健康状况的更好可观测性。

## 何时使用此技能

当用户希望为其Web应用启用遥测时使用此技能。

## 先决条件

工作区中的应用必须是以下类型之一：

- 在Azure上托管的ASP.NET Core应用
- 在Azure上托管的Node.js应用

## 指南

### 收集上下文信息

确定用户要为其添加遥测支持的应用程序的（编程语言、应用程序框架、托管）元组。这决定了如何对应用程序进行仪器化。通过阅读源代码进行合理猜测。对于不确定的内容，请向用户确认。您必须始终询问用户应用程序的托管位置（例如，本地计算机、Azure应用服务中的代码、Azure应用服务中的容器、Azure容器应用等）。

### 优先使用自动仪器化（如可能）

如果应用程序是托管在Azure应用服务中的C# ASP.NET Core应用，请使用[AUTO指南](references/AUTO.md)来帮助用户自动仪器化应用。

### 手动仪器化

通过创建应用洞察资源并更新应用程序代码来手动仪器化应用。

#### 创建应用洞察资源

根据环境选择以下任一选项：

- 将应用洞察添加到现有的Bicep模板中。参见[examples/appinsights.bicep](examples/appinsights.bicep)了解应添加的内容。如果工作区中已有Bicep模板文件，这是最佳选择。
- 使用Azure CLI。参见[scripts/appinsights.ps1](scripts/appinsights.ps1)了解应执行的Azure CLI命令以创建应用洞察资源。

无论选择哪种方法，建议用户在便于管理资源的有意义的资源组中创建应用洞察资源。一个好的候选资源组是包含Azure中托管应用资源的同一资源组。

#### 修改应用程序代码

- 如果应用程序是ASP.NET Core应用，请参见[ASPNETCORE指南](references/ASPNETCORE.md)了解如何修改C#代码。
- 如果应用程序是Node.js应用，请参见[NODEJS指南](references/NODEJS.md)了解如何修改JavaScript/TypeScript代码。
- 如果应用程序是Python应用，请参见[PYTHON指南](references/PYTHON.md)了解如何修改Python代码。
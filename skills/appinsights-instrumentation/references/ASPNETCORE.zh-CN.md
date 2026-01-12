

## 修改代码

对应用程序进行必要的更改。

- 安装客户端库
```
dotnet add package Azure.Monitor.OpenTelemetry.AspNetCore
```

- 配置应用程序以使用 Azure Monitor
ASP.NET Core 应用程序通常有一个名为 Program.cs 的文件，用于“构建”应用程序。找到该文件并应用以下更改：
  - 在文件顶部添加 `using Azure.Monitor.OpenTelemetry.AspNetCore;` 
  - 在调用 `builder.Build()` 之前，添加以下行 `builder.Services.AddOpenTelemetry().UseAzureMonitor();`。

> 注意：由于我们修改了应用程序的代码，因此需要重新部署以使更改生效。

## 配置 Application Insights 连接字符串

Application Insights 资源有一个连接字符串。将该连接字符串作为运行应用程序的环境变量添加。您可以使用 Azure CLI 查询 Application Insights 资源的连接字符串。有关查询连接字符串的 Azure CLI 命令，请参阅 [scripts/appinsights.ps1](scripts/appinsights.ps1)。

获取连接字符串后，使用其值设置此环境变量。

```
"APPLICATIONINSIGHTS_CONNECTION_STRING={your_application_insights_connection_string}"
```

如果应用程序具有基础设施即代码（IaC）模板（例如 Bicep 或 terraform 文件，用于表示其云实例），则应将此环境变量添加到 IaC 模板中，并在每次部署时应用。否则，请使用 Azure CLI 手动将此环境变量应用到应用程序的云实例。有关设置此环境变量的 Azure CLI 命令，请参阅 [scripts/appinsights.ps1](scripts/appinsights.ps1)。

> 重要：不要修改 appsettings.json。这是配置 Application Insights 的已弃用方式。环境变量是新的推荐方式。
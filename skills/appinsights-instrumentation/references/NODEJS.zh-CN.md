

## 修改代码

对应用程序进行必要的更改。

- 安装客户端库
```
npm install @azure/monitor-opentelemetry
```

- 配置应用程序以使用 Azure Monitor
通常，Node.js 应用程序有一个入口文件，该文件在 package.json 中被列为 "main" 属性。找到该文件并在其中应用以下更改。
  - 在文件顶部引入客户端库。`const { useAzureMonitor } = require("@azure/monitor-opentelemetry");`
  - 调用 setup 方法。`useAzureMonitor();`

> 注意：setup 方法应尽可能早地调用，但必须在环境变量配置之后，因为它需要从环境变量获取应用洞察连接字符串。例如，如果应用程序使用 dotenv 加载环境变量，则应在 dotenv 加载之后、应用程序其余部分启动之前调用 setup 方法。
> 注意：由于我们修改了应用程序代码，需要将其部署以使更改生效。

## 配置应用洞察连接字符串

应用洞察资源有一个连接字符串。将该连接字符串添加为运行中的应用程序的环境变量。您可以使用 Azure CLI 查询应用洞察资源的连接字符串。请参阅 [scripts/appinsights.ps1] 以了解用于查询连接字符串的 Azure CLI 命令。

获取连接字符串后，将其值设置为该环境变量。

```
"APPLICATIONINSIGHTS_CONNECTION_STRING={your_application_insights_connection_string}"
```

如果应用程序有基础设施即代码模板（如 Bicep 或 Terraform 文件，用于表示其云实例），则应将此环境变量添加到 IaC 模板中，以便在每次部署时应用。否则，使用 Azure CLI 手动将此环境变量应用到应用程序的云实例上。请参阅用于设置此环境变量的 Azure CLI 命令。
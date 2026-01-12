

## 修改代码

请对应用程序进行以下必要更改。

- 安装客户端库
```
pip install azure-monitor-opentelemetry
```

- 配置应用程序以使用 Azure Monitor
Python 应用程序通过 Python 标准库中的 logger 类发送遥测数据。创建一个模块，用于配置并生成可以发送遥测数据的 logger。

```python
import logging
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    logger_name="<your_logger_namespace>"
)
logger = logging.getLogger("<your_logger_namespace>")
```

> 注意：由于我们修改了应用程序的代码，因此需要将其部署以生效。

## 配置 Application Insights 连接字符串

Application Insights 资源有一个连接字符串。请将该连接字符串作为运行应用程序的环境变量添加。您可以使用 Azure CLI 查询 Application Insights 资源的连接字符串。有关查询连接字符串的 Azure CLI 命令，请参阅 [scripts/appinsights.ps1]。

获取连接字符串后，请使用其值设置此环境变量。

```
"APPLICATIONINSIGHTS_CONNECTION_STRING={your_application_insights_connection_string}"
```

如果应用程序有 IaC 模板（例如 Bicep 或 Terraform 文件，这些文件表示其云实例），则应将此环境变量添加到 IaC 模板中，以便在每次部署时应用。否则，请使用 Azure CLI 手动将此环境变量应用到应用程序的云实例上。有关设置此环境变量的 Azure CLI 命令，请参阅相关文档。

## 发送数据

创建一个配置为发送遥测数据的 logger。
```python
logger = logging.getLogger("<your_logger_namespace>")
logger.setLevel(logging.INFO)
```

然后通过调用其日志记录方法发送遥测事件。
```python
logger.info("info log")
```
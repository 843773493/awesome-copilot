

# 自动仪器化应用

使用 Azure 门户对托管在 Azure 应用服务中的 Web 应用进行自动仪器化，以用于应用洞察，而无需进行任何代码更改。仅支持以下类型的 app 进行自动仪器化。请参阅 [支持的环境、语言和资源提供者](https://learn.microsoft.com/azure/azure-monitor/app/codeless-overview#supported-environments-languages-and-resource-providers)。

- 托管在 Azure 应用服务中的 ASP.NET Core 应用
- 托管在 Azure 应用服务中的 Node.js 应用

构建一个 URL，将用户引导至 Azure 门户中对应 App Service 应用的应用洞察仪表板。
```
https://portal.azure.com/#resource/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Web/sites/{app_service_name}/monitoringSettings
```

使用上下文或请用户获取托管 Web 应用的 subscription_id、resource_group_name 和 app_service_name。
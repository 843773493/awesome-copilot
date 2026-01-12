

---
applyTo: '**'
---
# Dataverse Python SDK — 官方快速入门

本指南总结了 Microsoft Learn 中关于 Dataverse Python SDK（预览版）的指导，并提供可复制的代码片段。

## 先决条件
- 具有读写权限的 Dataverse 环境
- Python 3.10+
- 对 PyPI 的网络访问权限

## 安装
```bash
pip install PowerPlatform-Dataverse-Client
```

## 连接
```python
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.config import DataverseConfig

cfg = DataverseConfig()  # 默认语言代码为 1033
client = DataverseClient(
    base_url="https://<myorg>.crm.dynamics.com",
    credential=InteractiveBrowserCredential(),
    config=cfg,
)
```
- 可选的 HTTP 设置：`cfg.http_retries`，`cfg.http_backoff`，`cfg.http_timeout`。

## CRUD 示例
```python
# 创建操作返回 GUID 列表
account_id = client.create("account", {"name": "Acme, Inc.", "telephone1": "555-0100"})[0]

# 单条检索
account = client.get("account", account_id)

# 更新（返回 None）
client.update("account", account_id, {"telephone1": "555-0199"})

# 删除
client.delete("account", account_id)
```

## 批量操作
```python
# 向多个 ID 发送补丁
ids = client.create("account", [{"name": "Contoso"}, {"name": "Fabrikam"}])
client.update("account", ids, {"telephone1": "555-0200"})

# 1:1 补丁列表
client.update("account", ids, [{"telephone1": "555-1200"}, {"telephone1": "555-1300"}])

# 批量创建
payloads = [{"name": "Contoso"}, {"name": "Fabrikam"}, {"name": "Northwind"}]
ids = client.create("account", payloads)
```

## 文件上传
```python
client.upload_file('account', record_id, 'sample_filecolumn', 'test.pdf')
client.upload_file('account', record_id, 'sample_filecolumn', 'test.pdf', mode='chunk', if_none_match=True)
```

## 分页检索多条记录
```python
pages = client.get(
    "account",
    select=["accountid", "name", "createdon"],
    orderby=["name asc"],
    top=10,
    page_size=3,
)
for page in pages:
    print(len(page), page[:2])
```

## 表元数据快速入门
```python
info = client.create_table("SampleItem", {
    "code": "string",
    "count": "int",
    "amount": "decimal",
    "when": "datetime",
    "active": "bool",
})
logical = info["entity_logical_name"]
rec_id = client.create(logical, {f"{logical}name": "Sample A"})[0]
client.delete(logical, rec_id)
client.delete_table("SampleItem")
```

## 参考资料
- 入门指南: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/get-started
- 数据操作: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/work-data
- SDK 源代码/示例: https://github.com/microsoft/PowerPlatform-DataverseClient-Python
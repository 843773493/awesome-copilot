

---
applyTo: '**'
---
# Dataverse Python SDK — API 参考指南

## DataverseClient 类
用于与 Dataverse 交互的主要客户端。使用基础 URL 和 Azure 凭据进行初始化。

### 主要方法

#### create(table_schema_name, records)
创建单条或多条记录。返回 GUID 列表。

```python
# 单条记录
ids = client.create("account", {"name": "Acme"})
print(ids[0])  # 第一个 GUID

# 批量创建
ids = client.create("account", [{"name": "Contoso"}, {"name": "Fabrikam"}])
```

#### get(table_schema_name, record_id=None, select, filter, orderby, top, expand, page_size)
通过 OData 选项获取单个记录或查询多个记录。

```python
# 单条记录
record = client.get("account", record_id="guid-here")

# 带筛选和分页的查询
for batch in client.get(
    "account",
    filter="statecode eq 0",
    select=["name", "telephone1"],
    orderby=["createdon desc"],
    top=100,
    page_size=50
):
    for record in batch:
        print(record["name"])
```

#### update(table_schema_name, ids, changes)
更新单条或多条记录。

```python
# 单条更新
client.update("account", "guid-here", {"telephone1": "555-0100"})

# 广播：将相同的更改应用于多个 ID
client.update("account", [id1, id2, id3], {"statecode": 1})

# 一对一映射
client.update("account", [id1, id2], [{"name": "A"}, {"name": "B"}])
```

#### delete(table_schema_name, ids, use_bulk_delete=True)
删除单条或多条记录。

```python
# 单条删除
client.delete("account", "guid-here")

# 批量删除（异步）
job_id = client.delete("account", [id1, id2, id3])
```

#### create_table(table_schema_name, columns, solution_unique_name=None, primary_column_schema_name=None)
创建自定义表。

```python
from enum import IntEnum

class ItemStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 2
    __labels__ = {
        1033: {"ACTIVE": "Active", "INACTIVE": "Inactive"}
    }

info = client.create_table("new_MyTable", {
    "new_Title": "string",
    "new_Quantity": "int",
    "new_Price": "decimal",
    "new_Active": "bool",
    "new_Status": ItemStatus
})
print(info["entity_logical_name"])
```

#### create_columns(table_schema_name, columns)
向现有表添加列。

```python
created = client.create_columns("new_MyTable", {
    "new_Notes": "string",
    "new_Count": "int"
})
```

#### delete_columns(table_schema_name, columns)
从表中移除列。

```python
removed = client.delete_columns("new_MyTable", ["new_Notes", "new_Count"])
```

#### delete_table(table_schema_name)
删除自定义表（不可逆操作）。

```python
client.delete_table("new_MyTable")
```

#### get_table_info(table_schema_name)
获取表的元数据。

```python
info = client.get_table_info("new_MyTable")
if info:
    print(info["table_logical_name"])
    print(info["entity_set_name"])
```

#### list_tables()
列出所有自定义表。

```python
tables = client.list_tables()
for table in tables:
    print(table)
```

#### flush_cache(kind)
清除 SDK 缓存（例如：下拉列表标签）。

```python
removed = client.flush_cache("picklist")
```

## DataverseConfig 类
配置客户端行为（超时、重试、语言）。

```python
from PowerPlatform.Dataverse.core.config import DataverseConfig

cfg = DataverseConfig()
cfg.http_retries = 3
cfg.http_backoff = 1.0
cfg.http_timeout = 30
cfg.language_code = 1033  # 英语

client = DataverseClient(base_url=url, credential=cred, config=cfg)
```

## 错误处理
捕获 `DataverseError` 以处理 SDK 特定异常。检查 `is_transient` 以决定是否重试。

```python
from PowerPlatform.Dataverse.core.errors import DataverseError

try:
    client.create("account", {"name": "Test"})
except DataverseError as e:
    print(f"代码: {e.code}")
    print(f"信息: {e.message}")
    print(f"是否瞬时: {e.is_transient}")
    print(f"详细信息: {e.to_dict()}")
```

## OData 筛选提示
- 在筛选表达式中使用精确的逻辑名称（小写）
- `select` 中的列名会自动转换为小写
- `expand` 中的导航属性名区分大小写

## 参考资料
- API 文档: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.client.dataverseclient
- 配置文档: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.core.config.dataverseconfig
- 错误信息: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.core.errors
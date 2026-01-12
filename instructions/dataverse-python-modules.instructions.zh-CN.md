

---
applyTo: '**'
---
# Dataverse Python SDK — 完整模块参考

## 包层次结构

```
PowerPlatform.Dataverse
├── client
│   └── DataverseClient
├── core
│   ├── config (DataverseConfig)
│   └── errors (DataverseError, ValidationError, MetadataError, HttpError, SQLParseError)
├── data (OData操作, 元数据, SQL, 文件上传)
├── extensions (预留用于未来扩展)
├── models (预留用于数据模型和类型定义)
└── utils (预留用于实用工具和适配器)
```

## core.config 模块

管理客户端连接和行为设置。

### DataverseConfig 类

包含语言、超时、重试设置的容器。不可变。

```python
from PowerPlatform.Dataverse.core.config import DataverseConfig

cfg = DataverseConfig(
    language_code=1033,        # 默认英文（美国）
    http_retries=None,         # 保留用于未来
    http_backoff=None,         # 保留用于未来
    http_timeout=None          # 保留用于未来
)

# 或使用默认静态构建器
cfg_default = DataverseConfig.from_env()
```

**关键属性：**
- `language_code: int = 1033` — 用于本地化标签和消息的LCID。
- `http_retries: int | None` — (保留) 临时错误的最大重试次数。
- `http_backoff: float | None` — (保留) 重试之间的退避乘数。
- `http_timeout: float | None` — (保留) 请求超时时间（秒）。

## core.errors 模块

SDK操作的结构化异常层次结构。

### DataverseError（基类）

SDK错误的基类异常。

```python
from PowerPlatform.Dataverse.core.errors import DataverseError

try:
    # SDK调用
    pass
except DataverseError as e:
    print(f"代码: {e.code}")                # 错误类别
    print(f"子代码: {e.subcode}")          # 具体错误
    print(f"消息: {e.message}")            # 人类可读信息
    print(f"状态: {e.status_code}")        # HTTP状态（如适用）
    print(f"是否瞬时错误: {e.is_transient}")   # 是否可重试？
    details = e.to_dict()                  # 转换为字典
```

### ValidationError

数据操作期间的验证失败。

```python
from PowerPlatform.Dataverse.core.errors import ValidationError
```

### MetadataError

创建、删除或检查表/列时的元数据错误。

```python
from PowerPlatform.Dataverse.core.errors import MetadataError

try:
    client.create_table("MyTable", {...})
except MetadataError as e:
    print(f"元数据问题: {e.message}")
```

### HttpError

Web API HTTP请求失败（4xx、5xx等）。

```python
from PowerPlatform.Dataverse.core.errors import HttpError

try:
    client.get("account", record_id)
except HttpError as e:
    print(f"HTTP {e.status_code}: {e.message}")
    print(f"服务错误代码: {e.service_error_code}")
    print(f"关联ID: {e.correlation_id}")
    print(f"请求ID: {e.request_id}")
    print(f"重试时间: {e.retry_after} 秒")
    print(f"是否瞬时错误（是否重试?）: {e.is_transient}")  # 429、503、504
```

### SQLParseError

使用`query_sql()`时的SQL查询语法错误。

```python
from PowerPlatform.Dataverse.core.errors import SQLParseError

try:
    client.query_sql("INVALID SQL HERE")
except SQLParseError as e:
    print(f"SQL解析错误: {e.message}")
```

## data 包

低级OData协议、元数据、SQL和文件操作（内部委托）。

`data`包主要用于内部实现；`client`模块中的高级`DataverseClient`封装并暴露以下功能：
- 通过OData进行CRUD操作
- 元数据管理（创建/更新/删除表和列）
- SQL查询执行
- 文件上传处理

用户通过`DataverseClient`方法（例如`create()`、`get()`、`update()`、`delete()`、`create_table()`、`query_sql()`、`upload_file()`）与这些功能交互。

## extensions 包（占位符）

保留用于未来扩展点（例如自定义适配器、中间件）。

目前为空；当前功能请使用`core`和`client`模块。

## models 包（占位符）

保留用于未来数据模型定义和类型定义。

目前为空。数据结构以`dict`（OData）形式返回，并可JSON序列化。

## utils 包（占位符）

保留用于实用工具适配器和辅助功能。

目前为空。未来版本可能会添加辅助函数。

## client 模块

主要面向用户的API。

### DataverseClient 类

所有Dataverse操作的高级客户端。

```python
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.config import DataverseConfig

# 创建凭证
credential = InteractiveBrowserCredential()

# 可选配置
cfg = DataverseConfig(language_code=1033)

# 创建客户端
client = DataverseClient(
    base_url="https://org.crm.dynamics.com",
    credential=credential,
    config=cfg  # 可选
)
```

#### CRUD方法

- `create(table_schema_name, records)` → `list[str]` — 创建记录，返回GUID列表。
- `get(table_schema_name, record_id=None, select, filter, orderby, top, expand, page_size)` → 记录（单个或多个）。
- `update(table_schema_name, ids, changes)` → `None` — 更新记录。
- `delete(table_schema_name, ids, use_bulk_delete=True)` → `str | None` — 删除记录。

#### 元数据方法

- `create_table(table_schema_name, columns, solution_unique_name, primary_column_schema_name)` → 元数据字典。
- `create_columns(table_schema_name, columns)` → `list[str]`。
- `delete_columns(table_schema_name, columns)` → `list[str]`。
- `delete_table(table_schema_name)` → `None`。
- `get_table_info(table_schema_name)` → 元数据字典或`None`。
- `list_tables()` → `list[str]`。

#### SQL与实用工具

- `query_sql(sql)` → `list[dict]` — 执行只读SQL查询。
- `upload_file(table_schema_name, record_id, file_name_attribute, path, mode, mime_type, if_none_match)` → `None` — 上传到文件列。
- `flush_cache(kind)` → `int` — 清除SDK缓存（例如`"picklist"`）。

## 导入摘要

```python
# 主客户端
from PowerPlatform.Dataverse.client import DataverseClient

# 配置
from PowerPlatform.Dataverse.core.config import DataverseConfig

# 异常
from PowerPlatform.Dataverse.core.errors import (
    DataverseError,
    ValidationError,
    MetadataError,
    HttpError,
    SQLParseError,
)
```

## 参考资料

- 模块文档: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/
- 核心模块: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.core
- 数据模块: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.data
- 扩展模块: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.extensions
- 模型模块: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.models
- 工具模块: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.utils
- 客户端模块: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.client
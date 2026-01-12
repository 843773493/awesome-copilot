

---
applyTo: '**'
---

# Dataverse Python SDK 性能与优化指南

基于官方 Microsoft Dataverse 和 Azure SDK 性能指导。

## 1. 性能概览

Dataverse Python SDK 为 Python 开发者进行了优化，但在预览版中存在一些限制：
- **最小重试策略**：默认仅对网络错误进行重试
- **无 DeleteMultiple**：需使用单条删除或更新状态代替
- **有限的 OData 批处理**：不支持通用的 OData 批处理
- **SQL 限制**：不支持 JOIN，WHERE/TOP/ORDER BY 有限制

可通过变通方法和优化策略来解决这些限制。

---

## 2. 查询优化

### 使用 Select 限制列

```python
# ❌ 慢 - 获取所有列
accounts = client.get("account", top=100)

# ✅ 快 - 仅获取所需列
accounts = client.get(
    "account",
    select=["accountid", "name", "telephone1", "creditlimit"],
    top=100
)
```

**影响**：减少数据包大小和内存使用量达 30-50%。

---

### 有效使用过滤器

```python
# ❌ 慢 - 获取所有数据，再在 Python 中过滤
all_accounts = client.get("account")
active_accounts = [a for a in all_accounts if a.get("statecode") == 0]

# ✅ 快 - 服务端过滤
accounts = client.get(
    "account",
    filter="statecode eq 0",
    top=100
)
```

**OData 过滤器示例**：
```python
# 等于
filter="statecode eq 0"

# 字符串包含
filter="contains(name, 'Acme')"

# 多个条件
filter="statecode eq 0 and createdon gt 2025-01-01Z"

# 不等于
filter="statecode ne 2"
```

---

### 使用 Order by 实现可预测的分页

```python
# 确保分页的一致性顺序
accounts = client.get(
    "account",
    orderby=["createdon desc", "name asc"],
    page_size=100
)

for page in accounts:
    process_page(page)
```

---

## 3. 分页最佳实践

### 懒加载分页（推荐）

```python
# ✅ 最佳 - 生成器每次返回一页数据
pages = client.get(
    "account",
    top=5000,              # 总限制
    page_size=200          # 每页大小（提示）
)

for page in pages:  # 每次迭代获取一页数据
    for record in page:
        process_record(record)  # 立即处理
```

**优势**：
- 内存效率高（按需加载分页）
- 快速获取第一个结果
- 可根据需要提前停止

### 避免一次性加载所有数据到内存

```python
# ❌ 慢 - 一次性加载 100,000 条记录
all_records = list(client.get("account", top=100000))
process(all_records)

# ✅ 快 - 按页处理
for page in client.get("account", top=100000, page_size=5000):
    process(page)
```

---

## 4. 批处理操作

### 批量创建（推荐）

```python
# ✅ 最佳 - 单次调用创建多条记录
payloads = [
    {"name": f"Account {i}", "telephone1": f"555-{i:04d}"}
    for i in range(1000)
]
ids = client.create("account", payloads)  # 一次 API 调用处理多条记录
```

### 批量更新 - 广播模式

```python
# ✅ 快 - 对多条记录应用相同的更新
account_ids = ["id1", "id2", "id3", "..."]
client.update("account", account_ids, {"statecode": 1})  # 一次调用
```

### 批量更新 - 每条记录模式

```python
# ✅ 可接受 - 每条记录应用不同的更新
account_ids = ["id1", "id2", "id3"]
updates = [
    {"telephone1": "555-0100"},
    {"telephone1": "555-0200"},
    {"telephone1": "555-0300"},
]
client.update("account", account_ids, updates)
```

### 批处理大小调优

根据表的复杂度（基于 Microsoft 的指导）：

| 表类型 | 批处理大小 | 最大线程数 |
|--------|------------|------------|
| 原生表（Account, Contact, Lead） | 200-300 | 30 |
| 简单表（少量关联） | ≤10 | 50 |
| 中等复杂度 | ≤100 | 30 |
| 大型复杂表（>100 列，>20 关联） | 10-20 | 10-20 |

```python
def bulk_create_optimized(client, table_name, payloads, batch_size=200):
    """以最优批次大小创建记录."""
    for i in range(0, len(payloads), batch_size):
        batch = payloads[i:i + batch_size]
        ids = client.create(table_name, batch)
        print(f"已创建 {len(ids)} 条记录")
        yield ids
```

---

## 5. 连接管理

### 复用客户端实例

```python
# ❌ 不推荐 - 每次创建新连接
def process_batch():
    for batch in batches:
        client = DataverseClient(...)  # 费用高!
        client.create("account", batch)

# ✅ 推荐 - 复用连接
client = DataverseClient(...)  # 仅创建一次

def process_batch():
    for batch in batches:
        client.create("account", batch)  # 复用连接
```

### 全局客户端实例

```python
# singleton_client.py
from azure.identity import DefaultAzureCredential
from PowerPlatform.Dataverse.client import DataverseClient

_client = None

def get_client():
    global _client
    if _client is None:
        _client = DataverseClient(
            base_url="https://myorg.crm.dynamics.com",
            credential=DefaultAzureCredential()
        )
    return _client

# main.py
from singleton_client import get_client

client = get_client()
records = client.get("account")
```

### 连接超时配置

```python
from PowerPlatform.Dataverse.core.config import DataverseConfig

cfg = DataverseConfig()
cfg.http_timeout = 30         # 请求超时
cfg.connection_timeout = 5    # 连接超时

client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=credential,
    config=cfg
)
```

---

## 6. 异步操作（未来功能）

目前为同步操作，但可为异步功能做准备：

```python
# 推荐的异步支持模式
import asyncio

async def get_accounts_async(client):
    """未来异步 SDK 的模式."""
    # 当 SDK 支持异步时：
    # accounts = await client.get("account")
    # 现在使用同步方式配合 executor
    loop = asyncio.get_event_loop()
    accounts = await loop.run_in_executor(
        None, 
        lambda: list(client.get("account"))
    )
    return accounts

# 使用示例
accounts = asyncio.run(get_accounts_async(client))
```

---

## 7. 文件上传优化

### 小文件（<128 MB）

```python
# ✅ 快 - 单次请求
client.upload_file(
    table_name="account",
    record_id=record_id,
    column_name="document_column",
    file_path="small_file.pdf"
)
```

### 大文件（>128 MB）

```python
# ✅ 优化 - 分块上传
client.upload_file(
    table_name="account",
    record_id=record_id,
    column_name="document_column",
    file_path="large_file.pdf",
    mode='chunk',
    if_none_match=True
)

# SDK 会自动：
# 1. 将文件拆分为 4MB 块
# 2. 并行上传块
# 3. 在服务端重新组合
```

---

## 8. OData 查询优化

### SQL 替代方案（简单查询）

```python
# ✅ 有时更快 - 仅 SELECT 的直接 SQL
# 有限支持：单个 SELECT，可选 WHERE/TOP/ORDER BY
records = client.get(
    "account",
    sql="SELECT accountid, name FROM account WHERE statecode = 0 ORDER BY name"
)
```

### 复杂查询

```python
# ❌ 不支持 - JOIN、复杂 WHERE
sql="SELECT a.accountid, c.fullname FROM account a JOIN contact c ON a.accountid = c.parentcustomerid"

# ✅ 工作方式 - 获取账户，然后为每个账户获取联系人
accounts = client.get("account", select=["accountid", "name"])
for account in accounts:
    contacts = client.get(
        "contact",
        filter=f"parentcustomerid eq '{account['accountid']}'"
    )
    process(account, contacts)
```

---

## 9. 内存管理

### 增量处理大型数据集

```python
import gc

def process_large_table(client, table_name):
    """无需内存问题地处理数百万条记录."""
    
    for page in client.get(table_name, page_size=5000):
        for record in page:
            result = process_record(record)
            save_result(result)
        
        # 在分页之间强制垃圾回收
        gc.collect()
```

### 使用分块加载 DataFrame

```python
import pandas as pd

def load_to_dataframe_chunked(client, table_name, chunk_size=10000):
    """分块加载数据到 DataFrame."""
    
    dfs = []
    for page in client.get(table_name, page_size=1000):
        df_chunk = pd.DataFrame(page)
        dfs.append(df_chunk)
        
        # 达到分块阈值时合并
        if len(dfs) >= chunk_size // 1000:
            df = pd.concat(dfs, ignore_index=True)
            process_chunk(df)
            dfs = []
    
    # 处理剩余数据
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        process_chunk(df)
```

---

## 10. 处理速率限制

SDK 仅提供基本重试支持，需手动实现：

```python
import time
from PowerPlatform.Dataverse.core.errors import DataverseError

def call_with_backoff(func, max_retries=3):
    """使用指数退避处理速率限制."""
    
    for attempt in range(max_retries):
        try:
            return func()
        except DataverseError as e:
            if e.status_code == 429:  # 请求过多
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 1秒、2秒、4秒
                    print(f"速率限制，等待 {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise
            else:
                raise

# 使用示例
ids = call_with_backoff(
    lambda: client.create("account", payload)
)
```

---

## 11. 事务一致性（已知限制）

SDK 不提供事务一致性保证：

```python
# ⚠️ 如果批量操作部分失败，部分记录可能已被创建

def create_with_consistency_check(client, table_name, payloads):
    """创建记录并验证所有记录是否成功."""
    
    try:
        ids = client.create(table_name, payloads)
        
        # 验证所有记录是否成功创建
        created = client.get(
            table_name,
            filter=f"isof(Microsoft.Dynamics.CRM.{table_name})"
        )
        
        if len(ids) != count_created:
            print(f"⚠️ 仅创建了 {count_created}/{len(ids)} 条记录")
            # 处理部分失败
    except Exception as e:
        print(f"创建失败: {e}")
        # 检查已创建的记录
```

---

## 12. 性能监控

### 记录操作耗时

```python
import time
import logging

logger = logging.getLogger("dataverse")

def monitored_operation(operation_name):
    """用于监控操作性能的装饰器."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start
                logger.info(f"{operation_name}: {duration:.2f}s")
                return result
            except Exception as e:
                duration = time.time() - start
                logger.error(f"{operation_name} 操作耗时 {duration:.2f}s 后失败: {e}")
                raise
        return wrapper
    return decorator

@monitored_operation("批量创建账户")
def create_accounts(client, payloads):
    return client.create("account", payloads)
```

---

## 13. 性能检查清单

| 项目 | 状态 | 备注 |
|------|------|------|
| 复用客户端实例 | ☐ | 创建一次，重复使用 |
| 使用 select 限制列 | ☐ | 仅获取所需数据 |
| 使用 OData 过滤器进行服务端过滤 | ☐ | 不要获取所有数据再过滤 |
| 使用 page_size 进行分页 | ☐ | 按页处理数据 |
| 批处理操作 | ☐ | 使用 create/update 处理多条记录 |
| 根据表类型调整批次大小 | ☐ | 原生表=200-300，简单表=≤10 |
| 处理速率限制（429） | ☐ | 实现指数退避机制 |
| 对大文件使用分块上传 | ☐ | SDK 会处理 >128MB 的文件 |
| 监控操作耗时 | ☐ | 记录时间用于分析 |
| 使用生产环境数据进行测试 | ☐ | 性能会因数据量而变化 |

---

## 14. 参考资料

- [Dataverse Web API 性能](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/optimize-performance-create-update)
- [OData 查询选项](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/query-data-web-api)
- [SDK 与数据交互](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/work-data)
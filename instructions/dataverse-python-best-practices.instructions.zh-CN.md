

# Dataverse SDK for Python - 最佳实践指南

## 概述
从 Microsoft 官方 PowerPlatform-DataverseClient-Python 仓库、示例和推荐工作流中提取的生产就绪模式和最佳实践。

## 1. 安装与环境配置

### 生产环境安装
```bash
# 从 PyPI 安装已发布的 SDK
pip install PowerPlatform-Dataverse-Client

# 安装 Azure Identity 用于身份验证
pip install azure-identity

# 可选：安装 pandas 用于数据操作
pip install pandas
```

### 开发环境安装
```bash
# 克隆仓库
git clone https://github.com/microsoft/PowerPlatform-DataverseClient-Python.git
cd PowerPlatform-DataverseClient-Python

# 以可编辑模式安装用于实时开发
pip install -e .

# 安装开发依赖项
pip install pytest pytest-cov black isort mypy ruff
```

### Python 版本支持
- **最低要求**: Python 3.10
- **推荐版本**: Python 3.11+ 以获得最佳性能
- **支持版本**: Python 3.10, 3.11, 3.12, 3.13, 3.14

### 验证安装
```python
from PowerPlatform.Dataverse import __version__
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import InteractiveBrowserCredential

print(f"SDK 版本: {__version__}")
print("安装成功！")
```

---

## 2. 身份验证模式

### 交互式开发（基于浏览器）
```python
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient

credential = InteractiveBrowserCredential()
client = DataverseClient("https://yourorg.crm.dynamics.com", credential)
```

**适用场景**: 本地开发、交互式测试、单用户场景。

### 生产环境（客户端密钥）
```python
from azure.identity import ClientSecretCredential
from PowerPlatform.Dataverse.client import DataverseClient

credential = ClientSecretCredential(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-client-secret"
)
client = DataverseClient("https://yourorg.crm.dynamics.com", credential)
```

**适用场景**: 服务器端应用程序、Azure 自动化、计划任务。

### 基于证书的身份验证
```python
from azure.identity import ClientCertificateCredential
from PowerPlatform.Dataverse.client import DataverseClient

credential = ClientCertificateCredential(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    certificate_path="path/to/certificate.pem"
)
client = DataverseClient("https://yourorg.crm.dynamics.com", credential)
```

**适用场景**: 高安全性环境、证书固定要求。

### Azure CLI 身份验证
```python
from azure.identity import AzureCliCredential
from PowerPlatform.Dataverse.client import DataverseClient

credential = AzureCliCredential()
client = DataverseClient("https://yourorg.crm.dynamics.com", credential)
```

**适用场景**: 安装了 Azure CLI 的本地测试、Azure DevOps 管道。

---

## 3. 单例客户端模式

**最佳实践**: 创建一个 `DataverseClient` 实例并在整个应用程序中重复使用。

```python
# ❌ 反模式：重复创建客户端
def fetch_account(account_id):
    credential = InteractiveBrowserCredential()
    client = DataverseClient("https://yourorg.crm.dynamics.com", credential)
    return client.get("account", account_id)

# ✅ 模式：单例客户端
class DataverseService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            credential = InteractiveBrowserCredential()
            cls._instance = DataverseClient(
                "https://yourorg.crm.dynamics.com", 
                credential
            )
        return cls._instance

# 使用方式
service = DataverseService()
account = service.get("account", account_id)
```

---

## 4. 配置优化

### 连接设置
```python
from PowerPlatform.Dataverse.core.config import DataverseConfig
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import ClientSecretCredential

config = DataverseConfig(
    language_code=1033,  # 英语（美国）
    # 注意：http_retries、http_backoff、http_timeout 保留用于内部使用
)

credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = DataverseClient("https://yourorg.crm.dynamics.com", credential, config)
```

**关键配置选项**:
- `language_code`: API 响应的语言（默认：1033 表示英语）

---

## 5. CRUD 操作最佳实践

### 创建操作

#### 单条记录
```python
record_data = {
    "name": "Contoso Ltd",
    "telephone1": "555-0100",
    "creditlimit": 100000.00,
}
created_ids = client.create("account", record_data)
record_id = created_ids[0]
print(f"已创建: {record_id}")
```

#### 批量创建（自动优化）
```python
# SDK 会自动对数组中记录数大于 1 的情况使用 CreateMultiple
records = [
    {"name": f"Company {i}", "creditlimit": 50000 + (i * 1000)}
    for i in range(100)
]
created_ids = client.create("account", records)
print(f"已创建 {len(created_ids)} 条记录")
```

**性能**: 批量创建在内部优化；无需手动分批。

### 读取操作

#### 通过 ID 读取单条记录
```python
account = client.get("account", "account-guid-here")
print(account.get("name"))
```

#### 带过滤和选择的查询
```python
# 返回分页结果（生成器）
for page in client.get(
    "account",
    filter="creditlimit gt 50000",
    select=["name", "creditlimit", "telephone1"],
    orderby="name",
    top=100
):
    for account in page:
        print(f"{account['name']}: ${account['creditlimit']}")
```

**关键参数**:
- `filter`: OData 过滤器（必须使用小写的逻辑名称）
- `select`: 要检索的字段（提升性能）
- `orderby`: 排序结果
- `top`: 每页最大记录数（默认：5000）
- `page_size`: 用于分页的页面大小覆盖

#### SQL 查询（只读）
```python
# SQL 查询为只读；用于复杂分析
results = client.query_sql("""
    SELECT TOP 10 name, creditlimit 
    FROM account 
    WHERE creditlimit > 50000
    ORDER BY name
""")

for row in results:
    print(f"{row['name']}: ${row['creditlimit']}")
```

**限制**:
- 只读（仅支持 SELECT，不支持 DML）
- 适用于复杂连接和分析
- 可能被组织策略禁用

### 更新操作

#### 单条记录
```python
client.update("account", "account-guid", {
    "creditlimit": 150000.00,
    "name": "Updated Company Name"
})
```

#### 批量更新（广播相同更改）
```python
# 更新所有选定记录的相同数据
account_ids = ["id1", "id2", "id3"]
client.update("account", account_ids, {
    "industrycode": 1,  # 零售
    "accountmanagerid": "manager-guid"
})
```

#### 配对更新（1:1 记录更新）
```python
# 对每条记录应用不同的更新，发送多个请求
updates = {
    "id1": {"creditlimit": 100000},
    "id2": {"creditlimit": 200000},
    "id3": {"creditlimit": 300000},
}
for record_id, data in updates.items():
    client.update("account", record_id, data)
```

### 删除操作

#### 单条记录
```python
client.delete("account", "account-guid")
```

#### 批量删除（优化）
```python
# SDK 会自动对大量列表使用 BulkDelete
record_ids = ["id1", "id2", "id3", ...]
client.delete("account", record_ids, use_bulk_delete=True)
```

---

## 6. 异常处理与恢复

### 异常层次结构
```python
from PowerPlatform.Dataverse.core.errors import (
    DataverseError,           # 基类
    ValidationError,          # 验证失败
    MetadataError,           # 表/列操作
    HttpError,               # HTTP 层错误
    SQLParseError            # SQL 查询语法错误
)

try:
    client.create("account", {"name": None})  # 无效
except ValidationError as e:
    print(f"验证失败: {e}")
    # 处理特定验证逻辑
except DataverseError as e:
    print(f"通用 SDK 错误: {e}")
    # 处理其他 SDK 错误
```

### 重试逻辑模式
```python
import time
from PowerPlatform.Dataverse.core.errors import HttpError

def create_with_retry(table_name, record_data, max_retries=3):
    """使用指数退避重试逻辑创建记录。"""
    for attempt in range(max_retries):
        try:
            return client.create(table_name, record_data)
        except HttpError as e:
            if attempt == max_retries - 1:
                raise
            
            # 指数退避：1s, 2s, 4s
            backoff_seconds = 2 ** attempt
            print(f"第 {attempt + 1} 次尝试失败。{backoff_seconds}s 后重试...")
            time.sleep(backoff_seconds)

# 使用方式
created_ids = create_with_retry("account", {"name": "Contoso"})
```

### 处理 429（请求速率限制）错误
```python
import time
from PowerPlatform.Dataverse.core.errors import HttpError

try:
    accounts = client.get("account", top=5000)
except HttpError as e:
    # 速率限制；等待后重试
    if "429" in str(e):
        print("速率限制。等待 60 秒...")
        time.sleep(60)
        accounts = client.get("account", top=5000)
    else:
        raise
```

---

## 7. 表与列管理

### 创建自定义表
```python
from enum import IntEnum

class Priority(IntEnum):
    低 = 1
    中 = 2
    高 = 3

# 定义列及其类型
columns = {
    "new_Title": "string",
    "new_Quantity": "int",
    "new_Amount": "decimal",
    "new_Completed": "bool",
    "new_Priority": Priority,  # 创建选项集/下拉列表
    "new_CreatedDate": "datetime"
}

table_info = client.create_table(
    "new_CustomTable",
    primary_column_schema_name="new_Name",
    columns=columns
)

print(f"已创建表: {table_info['table_schema_name']}")
```

### 获取表元数据
```python
table_info = client.get_table_info("account")
print(f"模式名称: {table_info['table_schema_name']}")
print(f"逻辑名称: {table_info['table_logical_name']}")
print(f"实体集: {table_info['entity_set_name']}")
print(f"主键: {table_info['primary_id_attribute']}")
```

### 列出所有表
```python
tables = client.list_tables()
for table in tables:
    print(f"{table['table_schema_name']} ({table['table_logical_name']})")
```

### 列管理
```python
# 向现有表添加列
client.create_columns("new_CustomTable", {
    "new_Status": "string",
    "new_Priority": "int"
})

# 删除列
client.delete_columns("new_CustomTable", ["new_Status", "new_Priority"])

# 删除表
client.delete_table("new_CustomTable")
```

---

## 8. 分页与大型结果集

### 分页模式
```python
# 分页获取所有账户
all_accounts = []
for page in client.get(
    "account",
    top=500,      # 每页记录数
    page_size=500
):
    all_accounts.extend(page)
    print(f"已获取包含 {len(page)} 条记录的页面")

print(f"总计: {len(all_accounts)} 条记录")
```

### 使用延续令牌的手动分页
```python
# 处理复杂分页场景
skip_count = 0
page_size = 1000

while True:
    page = client.get("account", top=page_size, skip=skip_count)
    if not page:
        break
    
    print(f"第 {skip_count // page_size + 1} 页: {len(page)} 条记录")
    skip_count += page_size
```

---

## 9. 文件操作

### 上传小文件（< 128 MB）
```python
from pathlib import Path

file_path = Path("document.pdf")
record_id = "account-guid"

# 单次 PATCH 上传
response = client.upload_file(
    table_name="account",
    record_id=record_id,
    file_column_name="new_documentfile",
    file_path=file_path
)
print(f"上传成功: {response}")
```

### 使用分块上传大文件
```python
from pathlib import Path

file_path = Path("large_video.mp4")
record_id = "account-guid"

# SDK 会自动分块大文件
response = client.upload_file(
    table_name="account",
    record_id=record_id,
    file_column_name="new_videofile",
    file_path=file_path,
    chunk_size=4 * 1024 * 1024  # 4 MB 分块
)
print(f"分块上传完成")
```

---

## 10. OData 过滤器优化

### 大小写规则
```python
# ❌ 错误：使用大写逻辑名称
results = client.get("account", filter="Name eq 'Contoso'")

# ✅ 正确：使用小写逻辑名称
results = client.get("account", filter="name eq 'Contoso'")

# ✅ 值在需要时是大小写敏感的
results = client.get("account", filter="name eq 'Contoso Ltd'")
```

### 过滤表达式示例
```python
# 等于
client.get("account", filter="name eq 'Contoso'")

# 大于 / 小于
client.get("account", filter="creditlimit gt 50000")
client.get("account", filter="createdon lt 2024-01-01")

# 字符串包含
client.get("account", filter="contains(name, 'Ltd')")

# AND/OR 操作
client.get("account", filter="(name eq 'Contoso') and (creditlimit gt 50000)")
client.get("account", filter="(industrycode eq 1) or (industrycode eq 2)")

# NOT 操作
client.get("account", filter="not(statecode eq 1)")
```

### 选择与展开
```python
# 选择特定列（提升性能）
client.get("account", select=["name", "creditlimit", "telephone1"])

# 展开相关记录
client.get(
    "account",
    expand=["parentaccountid($select=name)"],
    select=["name", "parentaccountid"]
)
```

---

## 11. 缓存管理

### 清除缓存
```python
# 在批量操作后清除 SDK 内部缓存
client.flush_cache()

# 适用于以下情况：
# - 元数据更改（表/列创建）
# - 批量删除
# - 元数据同步
```

---

## 12. 性能最佳实践

### 应该怎么做 ✅
1. **使用 `select` 参数**: 仅获取所需列
   ```python
   client.get("account", select=["name", "creditlimit"])
   ```

2. **批量操作**: 一次性创建/更新多条记录
   ```python
   ids = client.create("account", [record1, record2, record3])
   ```

3. **使用分页**: 避免一次性加载所有记录
   ```python
   for page in client.get("account", top=1000):
       process_page(page)
   ```

4. **复用客户端实例**: 创建一次，多次使用
   ```python
   client = DataverseClient(url, credential)  # 仅创建一次
   # 在整个应用程序中复用
   ```

5. **在服务器端应用过滤器**: 让 Dataverse 在返回前进行过滤
   ```python
   client.get("account", filter="creditlimit gt 50000")
   ```

### 不应该怎么做 ❌
1. **不要获取所有列**: 指定所需字段
   ```python
   # 效率低
   client.get("account")
   ```

2. **不要在循环中创建记录**: 批量创建
   ```python
   # 效率低
   for record in records:
       client.create("account", record)
   ```

3. **不要一次性加载所有结果**: 使用分页
   ```python
   # 效率低
   all_accounts = list(client.get("account"))
   ```

4. **不要重复创建新客户端**: 复用单例
   ```python
   # 效率低下
   for i in range(100):
       client = DataverseClient(url, credential)
   ```

---

## 13. 常见模式总结

### 模式：Upsert（创建或更新）
```python
def upsert_account(name, data):
    """创建账户或更新已存在的账户。"""
    try:
        # 尝试查找现有账户
        results = list(client.get("account", filter=f"name eq '{name}'"))
        if results:
            account_id = results[0]['accountid']
            client.update("account", account_id, data)
            return account_id, "已更新"
        else:
            ids = client.create("account", {"name": name, **data})
            return ids[0], "已创建"
    except Exception as e:
        print(f"Upsert 失败: {e}")
        raise
```

### 模式：带错误恢复的批量操作
```python
def create_with_recovery(records):
    """创建记录并跟踪每条记录的错误。"""
    results = {"成功": [], "失败": []}
    
    try:
        ids = client.create("account", records)
        results["成功"] = ids
    except Exception as e:
        # 如果批量操作失败，尝试单条记录
        for i, record in enumerate(records):
            try:
                ids = client.create("account", record)
                results["成功"].append(ids[0])
            except Exception as e:
                results["失败"].append({"索引": i, "记录": record, "错误": str(e)})
    
    return results
```

---

## 14. 依赖项与版本

### 核心依赖项
- **azure-identity** >= 1.17.0（身份验证）
- **azure-core** >= 1.30.2（HTTP 客户端）
- **requests** >= 2.32.0（HTTP 请求）
- **Python** >= 3.10

### 可选依赖项
- **pandas**（数据操作）
- **reportlab**（用于文件示例的 PDF 生成）

### 开发工具
- **pytest** >= 7.0.0（测试）
- **black** >= 23.0.0（代码格式化）
- **mypy** >= 1.0.0（类型检查）
- **ruff** >= 0.1.0（静态代码分析）

---

## 15. 常见问题排查

### ImportError: 缺少模块 'PowerPlatform'
```bash
# 验证安装
pip show PowerPlatform-Dataverse-Client

# 重新安装
pip install --upgrade PowerPlatform-Dataverse-Client

# 检查虚拟环境是否激活
which python  # 应显示虚拟环境路径
```

### 身份验证失败
```python
# 验证凭据是否具有 Dataverse 访问权限
# 首先尝试交互式身份验证进行测试
from azure.identity import InteractiveBrowserCredential
credential = InteractiveBrowserCredential(
    tenant_id="your-tenant-id"  # 如果有多个租户请指定
)

# 检查组织 URL 格式
# ✓ https://yourorg.crm.dynamics.com
# ❌ https://yourorg.crm.dynamics.com/
# ❌ https://yourorg.crm4.dynamics.com（区域）
```

### HTTP 429 速率限制
```python
# 降低请求频率
# 实现指数退避（参见错误处理部分）
# 减少页面大小
client.get("account", top=500)  # 代替 5000
```

### MetadataError: 表未找到
```python
# 验证表是否存在（存在性检查不区分大小写，但 API 调用区分大小写）
tables = client.list_tables()
print([t['table_schema_name'] for t in tables])

# 使用精确的模式名称
table_info = client.get_table_info("new_customprefixed_table")
```

### SQL 查询未启用
```python
# query_sql() 需要组织配置
# 如果禁用，可回退到 OData 查询
try:
    results = client.query_sql("SELECT * FROM account")
except Exception:
    # 回退到 OData
    results = client.get("account")
```

---

## 参考链接
- [官方仓库](https://github.com/microsoft/PowerPlatform-DataverseClient-Python)
- [PyPI 包](https://pypi.org/project/PowerPlatform-Dataverse-Client/)
- [Azure Identity 文档](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme)
- [Dataverse Web API 文档](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview)
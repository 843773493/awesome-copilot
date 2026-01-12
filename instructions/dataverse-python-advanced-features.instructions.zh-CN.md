

# Dataverse SDK for Python - 高级功能指南

## 概述
涵盖 Dataverse SDK 的高级功能的全面指南，包括枚举、复杂筛选、SQL 查询、元数据操作以及生产模式。基于官方 Microsoft 演练示例。

## 1. 使用选项集与下拉列表

### 使用 IntEnum 实现类型安全
```python
from enum import IntEnum
from PowerPlatform.Dataverse.client import DataverseClient

# 定义下拉列表的枚举
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Priority(IntEnum):
    COLD = 1
    WARM = 2
    HOT = 3

# 创建包含枚举值的记录
record_data = {
    "new_title": "Important Task",
    "new_priority": Priority.HIGH,  # 自动转换为整数
}

ids = client.create("new_tasktable", record_data)
```

### 处理格式化值
```python
# 在检索记录时，下拉列表值以整数形式返回
record = client.get("new_tasktable", record_id)

priority_int = record.get("new_priority")  # 返回: 3
priority_formatted = record.get("new_priority@OData.Community.Display.V1.FormattedValue")  # 返回: "High"

print(f"优先级（原始值）: {priority_int}")
print(f"优先级（格式化值）: {priority_formatted}")
```

### 创建包含枚举列的表
```python
from enum import IntEnum
from datetime import datetime

class TaskStatus(IntEnum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2

class TaskPriority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# 将枚举类作为列类型传递
columns = {
    "new_Subject": "string",
    "new_Description": "string",
    "new_Category": "string",
    "new_Priority": "int",
    "new_Status": TaskStatus,
    "new_EstimatedHours": "decimal",
    "new_DueDate": "datetime",
    "new_IsOverdue": "bool",
    "new_Notes": "string"
}

table_info = client.create_table(
    "new_WorkItem",
    primary_column_schema_name="new_Subject",
    columns=columns
)

print(f"✓ 创建了表: {table_info['table_schema_name']}")
print(f"  主键: {table_info['primary_id_attribute']}")
print(f"  列: {', '.join(table_info.get('columns_created', []))}")
```

---

## 2. 高级筛选与查询

### 复杂的 OData 筛选条件
```python
# 简单的等值筛选
filter1 = "name eq 'Contoso'"

# 比较运算符
filter2 = "creditlimit gt 50000"
filter3 = "createdon lt 2024-01-01"

# 字符串操作
filter4 = "contains(name, 'Ltd')"
filter5 = "startswith(name, 'Con')"
filter6 = "endswith(name, 'Ltd')"

# 使用 AND 连接多个条件
filter7 = "(name eq 'Contoso') and (creditlimit gt 50000)"

# 使用 OR 连接多个条件
filter8 = "(industrycode eq 1) or (industrycode eq 2)"

# 否定条件
filter9 = "not(statecode eq 1)"

# 复杂嵌套条件
filter10 = "(creditlimit gt 50000) and ((industrycode eq 1) or (industrycode eq 2))"

# 在 get() 调用中使用筛选条件
results = client.get("account", filter=filter10, select=["name", "creditlimit"])
```

### 获取相关记录（Expand）
```python
# 获取父账户信息
accounts = client.get(
    "account",
    filter="creditlimit gt 100000",
    expand=["parentaccountid($select=name,creditlimit)"],
    select=["accountid", "name", "creditlimit", "parentaccountid"]
)

for page in accounts:
    for account in page:
        parent_name = account.get("_parentaccountid_value")
        print(f"账户: {account['name']}, 父账户: {parent_name}")
```

### 使用 SQL 查询进行复杂分析
```python
# SQL 查询是只读的，但适用于分析
sql = """
SELECT 
    a.name as AccountName,
    a.creditlimit,
    COUNT(c.contactid) as ContactCount
FROM account a
LEFT JOIN contact c ON a.accountid = c.parentcustomerid
WHERE a.creditlimit > 50000
GROUP BY a.accountid, a.name, a.creditlimit
ORDER BY ContactCount DESC
"""

results = client.query_sql(sql)
for row in results:
    print(f"{row['AccountName']}: {row['ContactCount']} 个联系人")
```

### SQL 查询的分页处理
```python
# SQL 查询默认返回分页结果
sql = "SELECT TOP 10000 name, creditlimit FROM account ORDER BY name"

all_results = []
for page in client.query_sql(sql):
    all_results.extend(page)
    print(f"已检索 {len(page)} 行")

print(f"总计: {len(all_results)} 行")
```

---

## 3. 元数据操作

### 创建复杂表
```python
from enum import IntEnum
from datetime import datetime

class TaskStatus(IntEnum):
    NEW = 1
    OPEN = 2
    CLOSED = 3

class TaskPriority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# 创建包含多种列类型的表
columns = {
    "new_Subject": "string",
    "new_Description": "string",
    "new_Category": "string",
    "new_Priority": "int",
    "new_Status": TaskStatus,
    "new_EstimatedHours": "decimal",
    "new_DueDate": "datetime",
    "new_IsOverdue": "bool",
    "new_Notes": "string"
}

table_info = client.create_table(
    "new_WorkItem",
    primary_column_schema_name="new_Subject",
    columns=columns
)

print(f"✓ 创建了表: {table_info['table_schema_name']}")
print(f"  主键: {table_info['primary_id_attribute']}")
print(f"  列: {', '.join(table_info.get('columns_created', []))}")
```

### 检查表元数据
```python
# 获取表的详细信息
table_info = client.get_table_info("account")

print(f"模式名称: {table_info.get('table_schema_name')}")
print(f"逻辑名称: {table_info.get('table_logical_name')}")
print(f"显示名称: {table_info.get('table_display_name')}")
print(f"实体集: {table_info.get('entity_set_name')}")
print(f"主键: {table_info.get('primary_id_attribute')}")
print(f"主名称: {table_info.get('primary_name_attribute')}")
```

### 列出组织中的所有表
```python
# 获取所有表（可能返回大量结果）
all_tables = []
for page in client.list_tables():
    all_tables.extend(page)
    print(f"此页已检索 {len(page)} 个表")

print(f"\n总计表数: {len(all_tables)}")

# 过滤自定义表
custom_tables = [t for t in all_tables if t['table_schema_name'].startswith('new_')]
print(f"自定义表数: {len(custom_tables)}")
for table in custom_tables[:5]:
    print(f"  - {table['table_schema_name']}")
```

### 动态管理列
```python
# 向现有表添加列
client.create_columns("new_TaskTable", {
    "new_Department": "string",
    "new_Budget": "decimal",
    "new_ApprovedDate": "datetime"
})

# 删除特定列
client.delete_columns("new_TaskTable", [
    "new_OldField1",
    "new_OldField2"
])

# 删除整个表
client.delete_table("new_TaskTable")
```

---

## 4. 单条记录与多条记录操作

### 单条记录操作
```python
# 创建单条记录
record_id = client.create("account", {"name": "Contoso"})[0]

# 通过 ID 获取单条记录
account = client.get("account", record_id)

# 更新单条记录
client.update("account", record_id, {"creditlimit": 100000})

# 删除单条记录
client.delete("account", record_id)
```

### 多条记录操作

#### 创建多条记录
```python
# 创建记录列表
records = [
    {"name": "Company A", "creditlimit": 50000},
    {"name": "Company B", "creditlimit": 75000},
    {"name": "Company C", "creditlimit": 100000},
]

created_ids = client.create("account", records)
print(f"已创建 {len(created_ids)} 条记录: {created_ids}")
```

#### 广播更新多条记录
```python
# 对多条记录应用相同的更新
account_ids = ["id1", "id2", "id3"]
client.update("account", account_ids, {
    "industrycode": 1,  # 零售行业
    "accountmanagerid": "senior-manager-guid"
})
print(f"已更新 {len(account_ids)} 条记录")
```

#### 删除多条记录
```python
# 使用批量删除优化删除多条记录
record_ids = ["id1", "id2", "id3", "id4", "id5"]
client.delete("account", record_ids, use_bulk_delete=True)
print(f"已删除 {len(record_ids)} 条记录")
```

---

## 5. 数据操作模式

### 检索、修改、更新模式
```python
# 检索单条记录
account = client.get("account", record_id)

# 局部修改
original_amount = account.get("creditlimit", 0)
new_amount = original_amount + 10000

# 更新回数据库
client.update("account", record_id, {"creditlimit": new_amount})
print(f"更新信用额度: {original_amount} → {new_amount}")
```

### 批量处理模式
```python
# 分页检索并处理
batch_size = 100
processed = 0

for page in client.get("account", top=batch_size, filter="statecode eq 0"):
    # 处理每一页
    batch_updates = []
    for account in page:
        if account.get("creditlimit", 0) > 100000:
            batch_updates.append({
                "id": account['accountid'],
                "accountmanagerid": "senior-manager-guid"
            })
    
    # 批量更新
    for update in batch_updates:
        client.update("account", update['id'], {"accountmanagerid": update['accountmanagerid']})
        processed += 1

print(f"已处理 {processed} 个账户")
```

### 条件操作模式
```python
from PowerPlatform.Dataverse.core.errors import DataverseError

def safe_update(table, record_id, data, check_field=None, check_value=None):
    """带预条件检查的更新操作"""
    try:
        if check_field and check_value:
            # 更新前验证条件
            record = client.get(table, record_id, select=[check_field])
            if record.get(check_field) != check_value:
                print(f"条件未满足: {check_field} != {check_value}")
                return False
        
        client.update(table, record_id, data)
        return True
    except DataverseError as e:
        print(f"更新失败: {e}")
        return False

# 使用示例
safe_update("account", account_id, {"creditlimit": 100000}, "statecode", 0)
```

---

## 6. 格式化值与显示

### 检索格式化值
```python
# 检索包含选项集或货币字段的记录时，可请求格式化值用于显示

record = client.get(
    "account",
    record_id,
    select=["name", "creditlimit", "industrycode"]
)

# 原始值
name = record.get("name")  # "Contoso Ltd"
limit = record.get("creditlimit")  # 100000.00
industry = record.get("industrycode")  # 1

# 格式化值（OData 响应中返回）
limit_formatted = record.get("creditlimit@OData.Community.Display.V1.FormattedValue")
industry_formatted = record.get("industrycode@OData.Community.Display.V1.FormattedValue")

print(f"名称: {name}")
print(f"信用额度: {limit_formatted or limit}")  # "100,000.00" 或 100000.00
print(f"行业: {industry_formatted or industry}")  # "Technology" 或 1
```

---

## 7. 性能优化

### 列选择策略
```python
# ❌ 检索所有列（慢，占用更多带宽）
account = client.get("account", record_id)

# ✅ 仅检索所需列（快、高效）
account = client.get(
    "account",
    record_id,
    select=["accountid", "name", "creditlimit", "telephone1"]
)
```

### 服务器端筛选
```python
# ❌ 全部检索后本地筛选（低效）
all_accounts = []
for page in client.get("account"):
    all_accounts.extend(page)
large_accounts = [a for a in all_accounts if a.get("creditlimit", 0) > 100000]

# ✅ 服务器端筛选，仅检索匹配项（高效）
large_accounts = []
for page in client.get("account", filter="creditlimit gt 100000"):
    large_accounts.extend(page)
```

### 处理大型结果集的分页
```python
# ❌ 一次性加载所有结果（占用大量内存）
all_accounts = list(client.get("account"))

# ✅ 按页处理（内存高效）
processed = 0
for page in client.get("account", top=1000):
    for account in page:
        process_account(account)
        processed += 1
    print(f"已处理: {processed}")
```

### 批量操作
```python
# ❌ 循环中逐条创建（慢）
for account_data in accounts:
    client.create("account", account_data)

# ✅ 批量创建（快、优化）
created_ids = client.create("account", accounts)
```

---

## 8. 高级场景中的错误处理

### 处理元数据错误
```python
from PowerPlatform.Dataverse.core.errors import MetadataError

try:
    table_info = client.create_table("new_CustomTable", {"name": "string"})
except MetadataError as e:
    print(f"元数据操作失败: {e}")
    # 处理表创建相关错误
```

### 处理验证错误
```python
from PowerPlatform.Dataverse.core.errors import ValidationError

try:
    client.create("account", {"name": None})  # 无效：名称为必填字段
except ValidationError as e:
    print(f"验证错误: {e}")
    # 处理验证相关错误
```

### 处理 HTTP 错误
```python
from PowerPlatform.Dataverse.core.errors import HttpError

try:
    client.get("account", "invalid-guid")
except HttpError as e:
    if "404" in str(e):
        print("记录未找到")
    elif "403" in str(e):
        print("访问被拒绝")
    else:
        print(f"HTTP 错误: {e}")
```

### 处理 SQL 错误
```python
from PowerPlatform.Dataverse.core.errors import SQLParseError

try:
    results = client.query_sql("SELECT INVALID SYNTAX")
except SQLParseError as e:
    print(f"SQL 解析错误: {e}")
```

---

## 9. 处理关系

### 创建相关记录
```python
# 创建父账户
parent_ids = client.create("account", {
    "name": "Parent Company",
    "creditlimit": 500000
})
parent_id = parent_ids[0]

# 创建包含父账户引用的子账户
children = [
    {"name": "Subsidiary A", "parentaccountid": parent_id},
    {"name": "Subsidiary B", "parentaccountid": parent_id},
    {"name": "Subsidiary C", "parentaccountid": parent_id},
]
child_ids = client.create("account", children)
print(f"已创建 {len(child_ids)} 个子账户")
```

### 查询相关记录
```python
# 获取包含子账户的账户
account = client.get("account", account_id)

# 查询子账户
children = client.get(
    "account",
    filter=f"parentaccountid eq {account_id}",
    select=["accountid", "name", "creditlimit"]
)

for page in children:
    for child in page:
        print(f"  - {child['name']}: ${child['creditlimit']}")
```

---

## 10. 清理与维护

### 清除 SDK 缓存
```python
# 在批量操作后清除元数据缓存
client.flush_cache()

# 适用于以下情况：
# - 大规模删除操作
# - 表或列的创建或删除
# - 跨环境的元数据同步
```

### 安全删除表
```python
from PowerPlatform.Dataverse.core.errors import MetadataError

def delete_table_safe(table_name):
    """带错误处理的表删除"""
    try:
        # 验证表是否存在
        table_info = client.get_table_info(table_name)
        if not table_info:
            print(f"表 {table_name} 不存在")
            return False
        
        # 删除表
        client.delete_table(table_name)
        print(f"✓ 表已删除: {table_name}")
        
        # 清除缓存
        client.flush_cache()
        return True
        
    except MetadataError as e:
        print(f"❌ 表删除失败: {e}")
        return False

delete_table_safe("new_TempTable")
```

---

## 11. 综合示例：完整工作流

```python
from enum import IntEnum
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.errors import DataverseError, MetadataError

class TaskStatus(IntEnum):
    NEW = 1
    IN_PROGRESS = 2
    COMPLETED = 3

class TaskPriority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# 初始化
credential = InteractiveBrowserCredential()
client = DataverseClient("https://yourorg.crm.dynamics.com", credential)

try:
    # 1. 创建表
    print("正在创建表...")
    table_info = client.create_table(
        "new_ProjectTask",
        primary_column_schema_name="new_Title",
        columns={
            "new_Description": "string",
            "new_Status": TaskStatus,
            "new_Priority": TaskPriority,
            "new_DueDate": "datetime",
            "new_EstimatedHours": "decimal"
        }
    )
    print(f"✓ 表已创建: {table_info['table_schema_name']}")
    
    # 2. 创建记录
    print("\n正在创建任务...")
    tasks = [
        {
            "new_Title": "设计系统",
            "new_Description": "创建设计系统架构",
            "new_Status": TaskStatus.NEW,
            "new_Priority": TaskPriority.HIGH,
            "new_EstimatedHours": 40.0
        },
        {
            "new_Title": "实现 UI",
            "new_Description": "构建 React 组件",
            "new_Status": TaskStatus.IN_PROGRESS,
            "new_Priority": TaskPriority.HIGH,
            "new_EstimatedHours": 80.0
        },
        {
            "new_Title": "编写测试",
            "new_Description": "单元测试和集成测试",
            "new_Status": TaskStatus.NEW,
            "new_Priority": TaskPriority.MEDIUM,
            "new_EstimatedHours": 30.0
        }
    ]
    task_ids = client.create("new_ProjectTask", tasks)
    print(f"✓ 已创建 {len(task_ids)} 个任务")
    
    # 3. 查询与筛选
    print("\n查询高优先级任务...")
    high_priority = client.get(
        "new_ProjectTask",
        filter="new_priority eq 3",
        select=["new_Title", "new_Priority", "new_EstimatedHours"]
    )
    for page in high_priority:
        for task in page:
            print(f"  - {task['new_title']}: {task['new_estimatedhours']} 小时")
    
    # 4. 更新记录
    print("\n更新任务状态...")
    client.update("new_ProjectTask", task_ids[1], {
        "new_Status": TaskStatus.COMPLETED,
        "new_EstimatedHours": 85.5
    })
    print("✓ 任务状态已更新")
    
    # 5. 清理
    print("\n清理...")
    client.delete_table("new_ProjectTask")
    print("✓ 表已删除")
    
    # 清除缓存
    client.flush_cache()
    
except (MetadataError, DataverseError) as e:
    print(f"❌ 错误: {e}")
```


---
applyTo: '**'
---

# Dataverse Python SDK — 错误处理与故障排除指南

基于官方 Microsoft Azure SDK 错误处理模式和 Dataverse SDK 的具体实现。

## 1. DataverseError 类概述

Python 的 Dataverse SDK 提供了结构化的异常层次结构，以实现强大的错误处理。

### DataverseError 构造函数

```python
from PowerPlatform.Dataverse.core.errors import DataverseError

DataverseError(
    message: str,                          # 可读的错误信息
    code: str,                             # 错误类别（例如："validation_error", "http_error"）
    subcode: str | None = None,            # 可选的特定错误标识符
    status_code: int | None = None,        # HTTP 状态码（如适用）
    details: Dict[str, Any] | None = None, # 额外的诊断信息
    source: str | None = None,             # 错误来源："client" 或 "server"
    is_transient: bool = False             # 错误是否可能通过重试成功
)
```

### 关键属性

```python
try:
    client.get("account", record_id="invalid-id")
except DataverseError as e:
    print(f"Message: {e.message}")           # 可读信息
    print(f"Code: {e.code}")                 # 错误类别
    print(f"Subcode: {e.subcode}")           # 具体错误类型
    print(f"Status Code: {e.status_code}")   # HTTP 状态码（401、403、429 等）
    print(f"Source: {e.source}")             # "client" 或 "server"
    print(f"Is Transient: {e.is_transient}") # 是否可重试？
    print(f"Details: {e.details}")           # 额外上下文
    
    # 转换为字典用于日志记录
    error_dict = e.to_dict()
```

---

## 2. 常见错误场景

### 认证错误 (401)

**原因**: 无效凭据、过期令牌或配置错误。

```python
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.errors import DataverseError
from azure.identity import InteractiveBrowserCredential

try:
    # 凭据无效或令牌过期
    credential = InteractiveBrowserCredential()
    client = DataverseClient(
        base_url="https://invalid-org.crm.dynamics.com",
        credential=credential
    )
    records = client.get("account")
except DataverseError as e:
    if e.status_code == 401:
        print("认证失败。请检查凭据和令牌过期情况。")
        print(f"Details: {e.message}")
        # 不要重试，先修复凭据
    else:
        raise
```

### 授权错误 (403)

**原因**: 用户对请求的操作没有权限。

```python
try:
    # 用户没有权限读取联系人
    records = client.get("contact")
except DataverseError as e:
    if e.status_code == 403:
        print("访问被拒绝。用户缺少所需权限。")
        print(f"支持请求 ID: {e.details.get('request_id')}")
        # 升级到管理员
    else:
        raise
```

### 资源未找到 (404)

**原因**: 记录、表或资源不存在。

```python
try:
    # 记录不存在
    record = client.get("account", record_id="00000000-0000-0000-0000-000000000000")
except DataverseError as e:
    if e.status_code == 404:
        print("资源未找到。使用默认数据。")
        record = {"name": "Unknown", "id": None}
    else:
        raise
```

### 率限制 (429)

**原因**: 请求过多，超过服务保护限制。

**注意**: SDK 中内置的重试功能有限。手动处理瞬时一致性问题。

```python
import time

def create_with_retry(client, table_name, payload, max_retries=3):
    """使用指数退避重试机制创建记录。"""
    for attempt in range(max_retries):
        try:
            result = client.create(table_name, payload)
            return result
        except DataverseError as e:
            if e.status_code == 429 and e.is_transient:
                wait_time = 2 ** attempt  # 指数退避
                print(f"已达到速率限制。{wait_time}s 后重试...")
                time.sleep(wait_time)
            else:
                raise
    
    raise Exception(f"在 {max_retries} 次重试后仍失败")
```

### 服务器错误 (500, 502, 503, 504)

**原因**: 临时服务问题或基础设施故障。

```python
try:
    result = client.create("account", {"name": "Acme"})
except DataverseError as e:
    if 500 <= e.status_code < 600:
        print(f"服务器错误 ({e.status_code})。服务可能暂时不可用。")
        # 实现指数退避重试逻辑
    else:
        raise
```

### 验证错误 (400)

**原因**: 请求格式无效、缺少必填字段或违反业务规则。

```python
try:
    # 缺少必填字段或无效数据
    client.create("account", {"telephone1": "not-a-phone-number"})
except DataverseError as e:
    if e.status_code == 400:
        print(f"验证错误: {e.message}")
        if e.details:
            print(f"Details: {e.details}")
        # 记录验证问题用于调试
    else:
        raise
```

---

## 3. 错误处理最佳实践

### 使用特定异常处理

始终在通用异常之前捕获特定异常：

```python
from PowerPlatform.Dataverse.core.errors import DataverseError
from azure.core.exceptions import AzureError

try:
    records = client.get("account", filter="statecode eq 0", top=100)
except DataverseError as e:
    # 处理 Dataverse 特定错误
    if e.status_code == 401:
        print("需要重新认证")
    elif e.status_code == 404:
        print("资源未找到")
    elif e.is_transient:
        print("瞬时错误 - 可重试")
    else:
        print(f"操作失败: {e.message}")
except AzureError as e:
    # 处理 Azure SDK 错误（网络、认证等）
    print(f"Azure 错误: {e}")
except Exception as e:
    # 捕获意外错误
    print(f"意外错误: {e}")
```

### 实现智能重试逻辑

**不要重试**:
- 401 未授权（认证失败）
- 403 禁止（授权失败）
- 400 错误请求（客户端错误）
- 404 未找到（除非资源会最终出现）

**考虑重试**:
- 408 请求超时
- 429 请求过多（使用指数退避）
- 500 内部服务器错误
- 502 坏网关
- 503 服务不可用
- 504 网关超时

```python
def should_retry(error: DataverseError) -> bool:
    """判断操作是否应重试。"""
    if not error.is_transient:
        return False
    
    retryable_codes = {408, 429, 500, 502, 503, 504}
    return error.status_code in retryable_codes

def call_with_exponential_backoff(func, *args, max_attempts=3, **kwargs):
    """使用指数退避重试机制调用函数。"""
    for attempt in range(max_attempts):
        try:
            return func(*args, **kwargs)
        except DataverseError as e:
            if should_retry(e) and attempt < max_attempts - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s...
                print(f"第 {attempt + 1} 次尝试失败。{wait_time}s 后重试...")
                time.sleep(wait_time)
            else:
                raise
```

### 提取有意义的错误信息

```python
import json
from datetime import datetime

def log_error_for_support(error: DataverseError):
    """记录错误信息用于支持。"""
    error_info = {
        "timestamp": datetime.utcnow().isoformat(),
        "error_type": type(error).__name__,
        "message": error.message,
        "code": error.code,
        "subcode": error.subcode,
        "status_code": error.status_code,
        "source": error.source,
        "is_transient": error.is_transient,
        "details": error.details
    }
    
    print(json.dumps(error_info, indent=2))
    
    # 保存到日志文件或发送到监控服务
    return error_info
```

### 优雅处理批量操作

```python
def bulk_create_with_error_tracking(client, table_name, payloads):
    """创建多个记录，跟踪哪些成功哪些失败。"""
    results = {
        "succeeded": [],
        "failed": []
    }
    
    for idx, payload in enumerate(payloads):
        try:
            record_ids = client.create(table_name, payload)
            results["succeeded"].append({
                "payload": payload,
                "ids": record_ids
            })
        except DataverseError as e:
            results["failed"].append({
                "index": idx,
                "payload": payload,
                "error": {
                    "message": e.message,
                    "code": e.code,
                    "status": e.status_code
                }
            })
    
    return results
```

---

## 4. 启用诊断日志记录

### 配置日志记录

```python
import logging
import sys

# 设置根日志记录器
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dataverse_sdk.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# 配置特定日志记录器
logging.getLogger('azure').setLevel(logging.DEBUG)
logging.getLogger('PowerPlatform').setLevel(logging.DEBUG)

# HTTP 日志记录（注意敏感数据）
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.DEBUG)
```

### 启用 SDK 级别日志记录

```python
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.config import DataverseConfig
from azure.identity import InteractiveBrowserCredential

cfg = DataverseConfig()
cfg.logging_enable = True  # 启用详细日志记录

client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=InteractiveBrowserCredential(),
    config=cfg
)

# 现在 SDK 将记录详细的 HTTP 请求/响应
records = client.get("account", top=10)
```

### 解析错误响应

```python
import json

try:
    client.create("account", invalid_payload)
except DataverseError as e:
    # 提取结构化错误详情
    if e.details and isinstance(e.details, dict):
        error_code = e.details.get('error', {}).get('code')
        error_message = e.details.get('error', {}).get('message')
        
        print(f"错误代码: {error_code}")
        print(f"错误信息: {error_message}")
        
        # 有些错误包含嵌套详情
        if 'error' in e.details and 'details' in e.details['error']:
            for detail in e.details['error']['details']:
                print(f"  - {detail.get('code')}: {detail.get('message')}")
```

---

## 5. Dataverse 特定错误处理

### 处理 OData 查询错误

```python
try:
    # 无效的 OData 过滤器
    records = client.get(
        "account",
        filter="invalid_column eq 0"
    )
except DataverseError as e:
    if "invalid column" in e.message.lower():
        print("请检查 OData 列名和语法")
    else:
        print(f"查询错误: {e.message}")
```

### 处理文件上传错误

```python
try:
    client.upload_file(
        table_name="account",
        record_id=record_id,
        column_name="document_column",
        file_path="large_file.pdf"
    )
except DataverseError as e:
    if e.status_code == 413:
        print("文件过大。请使用分块上传模式。")
    elif e.status_code == 400:
        print("列无效或文件格式不正确。")
    else:
        raise
```

### 处理表元数据操作

```python
try:
    # 创建自定义表
    table_def = {
        "SchemaName": "new_CustomTable",
        "DisplayName": "自定义表"
    }
    client.create("EntityMetadata", table_def)
except DataverseError as e:
    if "already exists" in e.message:
        print("表已存在")
    elif "permission" in e.message.lower():
        print("缺少创建表的权限")
    else:
        raise
```

---

## 6. 监控与告警

### 用监控包装客户端调用

```python
from functools import wraps
import time

def monitor_operation(operation_name):
    """装饰器用于监控 SDK 操作。"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                print(f"✓ {operation_name} 操作完成，耗时 {duration:.2f}s")
                return result
            except DataverseError as e:
                duration = time.time() - start_time
                print(f"✗ {operation_name} 操作失败，耗时 {duration:.2f}s")
                print(f"  错误: {e.code} ({e.status_code}): {e.message}")
                raise
        return wrapper
    return decorator

@monitor_operation("获取账户")
def get_accounts(client):
    return client.get("account", top=100)

# 使用示例
try:
    accounts = get_accounts(client)
except DataverseError:
    print("操作失败 - 请查看日志以获取详细信息")
```

---

## 7. 常见故障排除清单

| 问题 | 诊断 | 解决方案 |
|-------|-----------|----------|
| 401 未授权 | 令牌过期或凭据错误 | 使用有效凭据重新认证 |
| 403 禁止 | 用户缺少权限 | 向管理员请求访问权限 |
| 404 未找到 | 记录/表不存在 | 验证架构名称和记录 ID |
| 429 率限制 | 请求过多 | 实现指数退避重试机制 |
| 500+ 服务器错误 | 服务问题 | 使用指数退避重试；检查服务状态页面 |
| 400 错误请求 | 请求格式无效 | 检查 OData 语法、列名和必填字段 |
| 网络超时 | 连接问题 | 检查网络，增加 DataverseConfig 中的超时时间 |
| InvalidOperationException | 插件/工作流错误 | 在 Dataverse 中检查插件日志 |

---

## 8. 日志记录最佳实践

```python
import logging
import json
from datetime import datetime

class DataverseErrorHandler:
    """集中式错误处理与日志记录。"""
    
    def __init__(self, log_file="dataverse_errors.log"):
        self.logger = logging.getLogger("DataverseSDK")
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.ERROR)
    
    def log_error(self, error: DataverseError, context: str = ""):
        """带上下文的日志记录用于调试。"""
        error_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "context": context,
            "error": error.to_dict()
        }
        
        self.logger.error(json.dumps(error_record, indent=2))
    
    def is_retryable(self, error: DataverseError) -> bool:
        """判断错误是否应重试。"""
        return error.is_transient and error.status_code in {408, 429, 500, 502, 503, 504}

# 使用示例
error_handler = DataverseErrorHandler()

try:
    client.create("account", payload)
except DataverseError as e:
    error_handler.log_error(e, "create_account_batch_1")
    if error_handler.is_retryable(e):
        print("将重试此操作")
    else:
        print("操作永久失败")
```

---

## 9. 参考资料

- [DataverseError API 参考文档](https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.core.errors.dataverseerror)
- [Azure SDK 错误处理](https://learn.microsoft.com/en-us/azure/developer/python/sdk/fundamentals/errors)
- [Dataverse SDK 入门指南](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/get-started)
- [服务保护 API 限制](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/optimize-performance-create-update)


---
applyTo: '**'
---

# Dataverse SDK for Python — 测试与调试策略

基于官方 Azure Functions 和 pytest 测试模式。

## 1. 测试概览

### Dataverse SDK 测试金字塔

```
         集成测试  <- 使用真实 Dataverse 进行测试
              /\
             /  \
            /单元测试（模拟）\
           /____________________\
          < 框架测试
```

---

## 2. 使用模拟进行单元测试

### 设置测试环境

```bash
# 安装测试依赖
pip install pytest pytest-cov unittest-mock
```

### 模拟 DataverseClient

```python
# tests/test_operations.py
import pytest
from unittest.mock import Mock, patch, MagicMock
from PowerPlatform.Dataverse.client import DataverseClient

@pytest.fixture
def mock_client():
    """提供模拟的 DataverseClient."""
    client = Mock(spec=DataverseClient)
    return client

def test_create_account(mock_client):
    """使用模拟客户端测试账户创建."""
    
    # 设置模拟响应
    mock_client.create.return_value = ["id-123"]
    
    # 调用函数
    from my_app import create_account
    result = create_account(mock_client, {"name": "Acme"})
    
    # 验证
    assert result == "id-123"
    mock_client.create.assert_called_once_with("account", {"name": "Acme"})

def test_create_account_error(mock_client):
    """测试账户创建中的错误处理."""
    from PowerPlatform.Dataverse.core.errors import DataverseError
    
    # 设置模拟引发错误
    mock_client.create.side_effect = DataverseError(
        message="账户已存在",
        code="验证错误",
        status_code=400
    )
    
    # 验证错误是否被引发
    from my_app import create_account
    with pytest.raises(DataverseError):
        create_account(mock_client, {"name": "Acme"})
```

### 测试数据结构

```python
# tests/fixtures.py
import pytest

@pytest.fixture
def sample_account():
    """用于测试的示例账户记录."""
    return {
        "accountid": "id-123",
        "name": "Acme 公司",
        "telephone1": "555-0100",
        "statecode": 0,
        "createdon": "2025-01-01T00:00:00Z"
    }

@pytest.fixture
def sample_accounts(sample_account):
    """多个示例账户."""
    return [
        sample_account,
        {**sample_account, "accountid": "id-124", "name": "Fabrikam"},
        {**sample_account, "accountid": "id-125", "name": "Contoso"},
    ]

# 测试中使用
def test_process_accounts(mock_client, sample_accounts):
    mock_client.get.return_value = iter([sample_accounts])
    # 测试处理
```

---

## 3. 常见模拟模式

### 模拟带分页的 Get 操作

```python
def test_pagination(mock_client, sample_accounts):
    """测试分页结果的处理."""
    
    # 模拟返回带有分页的生成器
    mock_client.get.return_value = iter([
        sample_accounts[:2],  # 第一页
        sample_accounts[2:]   # 第二页
    ])
    
    from my_app import process_all_accounts
    result = process_all_accounts(mock_client)
    
    assert len(result) == 3  # 所有分页处理完毕
```

### 模拟批量操作

```python
def test_bulk_create(mock_client):
    """测试批量账户创建."""
    
    payloads = [
        {"name": "账户 1"},
        {"name": "账户 2"},
    ]
    
    # 模拟返回 ID 列表
    mock_client.create.return_value = ["id-1", "id-2"]
    
    from my_app import create_accounts
    ids = create_accounts(mock_client, payloads)
    
    assert len(ids) == 2
    mock_client.create.assert_called_once_with("account", payloads)
```

### 模拟错误

```python
def test_rate_limiting_retry(mock_client):
    """测试在速率限制下的重试逻辑."""
    from PowerPlatform.Dataverse.core.errors import DataverseError
    
    # 模拟失败后成功
    error = DataverseError(
        message="请求过多",
        code="HTTP 错误",
        status_code=429,
        is_transient=True
    )
    mock_client.create.side_effect = [error, ["id-123"]]
    
    from my_app import create_with_retry
    result = create_with_retry(mock_client, "account", {})
    
    assert result == "id-123"
    assert mock_client.create.call_count == 2  # 已重试
```

---

## 4. 集成测试

### 本地开发测试

```python
# tests/test_integration.py
import pytest
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient

@pytest.fixture
def dataverse_client():
    """用于集成测试的真实客户端."""
    client = DataverseClient(
        base_url="https://myorg-dev.crm.dynamics.com",
        credential=InteractiveBrowserCredential()
    )
    return client

@pytest.mark.integration
def test_create_and_retrieve_account(dataverse_client):
    """测试创建和检索账户（针对真实 Dataverse）。"""
    
    # 创建
    account_id = dataverse_client.create("account", {
        "name": "测试账户"
    })[0]
    
    # 检索
    account = dataverse_client.get("account", account_id)
    
    # 验证
    assert account["name"] == "测试账户"
    
    # 清理
    dataverse_client.delete("account", account_id)
```

### 测试隔离

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="function")
def test_account(dataverse_client):
    """创建测试账户，测试结束后清理."""
    
    account_id = dataverse_client.create("account", {
        "name": "测试账户"
    })[0]
    
    yield account_id
    
    # 清理
    try:
        dataverse_client.delete("account", account_id)
    except:
        pass  # 已经被删除

# 使用示例
def test_update_account(dataverse_client, test_account):
    """测试更新账户."""
    dataverse_client.update("account", test_account, {"telephone1": "555-0100"})
    
    account = dataverse_client.get("account", test_account)
    assert account["telephone1"] == "555-0100"
```

---

## 5. pytest 配置

### pytest.ini

```ini
[pytest]
# 默认跳过集成测试
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    integration: 标记测试为集成测试（使用 -m integration 运行）
    slow: 标记测试为慢速测试
    unit: 标记测试为单元测试
```

### 运行测试

```bash
# 仅运行单元测试
pytest

# 单元测试 + 集成测试
pytest -m "unit or integration"

# 仅运行集成测试
pytest -m integration

# 带覆盖率分析
pytest --cov=my_app tests/

# 特定测试
pytest tests/test_operations.py::test_create_account
```

---

## 6. 覆盖率分析

### 生成覆盖率报告

```bash
# 运行带覆盖率的测试
pytest --cov=my_app --cov-report=html tests/

# 查看覆盖率
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

### 覆盖率配置 (.coveragerc)

```ini
[run]
branch = True
source = my_app

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov
```

---

## 7. 使用打印和日志调试

### 启用调试日志

```python
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('debug.log')
    ]
)

# 启用 SDK 日志
logging.getLogger('PowerPlatform').setLevel(logging.DEBUG)
logging.getLogger('azure').setLevel(logging.DEBUG)

# 在测试中
def test_with_logging(mock_client):
    logger = logging.getLogger(__name__)
    logger.debug("开始测试")
    
    result = my_function(mock_client)
    
    logger.debug(f"结果: {result}")
```

### pytest 捕获输出

```bash
# 在测试中显示打印和日志输出
pytest -s tests/

# 仅在失败时捕获并显示输出
pytest --tb=short tests/
```

---

## 8. 性能测试

### 测量操作持续时间

```python
import pytest
import time

def test_bulk_create_performance(dataverse_client):
    """测试批量创建性能."""
    
    payloads = [{"name": f"账户 {i}"} for i in range(1000)]
    
    start = time.time()
    ids = dataverse_client.create("account", payloads)
    duration = time.time() - start
    
    assert len(ids) == 1000
    assert duration < 10  # 应在 10 秒内完成
    
    print(f"在 {duration:.2f}s 内创建了 1000 条记录 ({1000/duration:.0f} 条/秒)")
```

### pytest 基准插件

```bash
pip install pytest-benchmark
```

```python
def test_query_performance(benchmark, dataverse_client):
    """基准查询性能."""
    
    def get_accounts():
        return list(dataverse_client.get("account", top=100))
    
    result = benchmark(get_accounts)
    assert len(result) <= 100
```

---

## 9. 常见测试模式

### 测试重试逻辑

```python
def test_retry_on_transient_error(mock_client):
    """测试在瞬时错误下的重试."""
    from PowerPlatform.Dataverse.core.errors import DataverseError
    
    error = DataverseError(
        message="超时",
        code="HTTP 错误",
        status_code=408,
        is_transient=True
    )
    
    # 失败后成功
    mock_client.create.side_effect = [error, ["id-123"]]
    
    from my_app import create_with_retry
    result = create_with_retry(mock_client, "account", {})
    
    assert result == "id-123"
```

### 测试过滤器构建

```python
def test_filter_builder():
    """测试 OData 过滤器生成."""
    from my_app import build_account_filter
    
    # 测试用例
    assert build_account_filter(status="active") == "statecode eq 0"
    assert build_account_filter(name="Acme") == "contains(name, 'Acme')"
    assert build_account_filter(status="active", name="Acme") \
        == "statecode eq 0 and contains(name, 'Acme')"
```

### 测试错误处理

```python
def test_handles_missing_record(mock_client):
    """测试处理 404 错误."""
    from PowerPlatform.Dataverse.core.errors import DataverseError
    
    mock_client.get.side_effect = DataverseError(
        message="未找到",
        code="HTTP 错误",
        status_code=404
    )
    
    from my_app import get_account_safe
    result = get_account_safe(mock_client, "invalid-id")
    
    assert result is None  # 返回 None 而不是引发异常
```

---

## 10. 调试检查清单

| 问题 | 调试步骤 |
|-------|-------------|
| 测试意外失败 | 添加 `-s` 标志以查看打印输出 |
| 模拟未被调用 | 检查方法名和参数是否完全匹配 |
| 真实 API 失败 | 检查凭据、URL 和权限 |
| 测试中的速率限制 | 添加延迟或使用较小批次 |
| 数据未找到 | 验证记录是否已创建且未被清理 |
| 断言错误 | 打印实际值与预期值的对比 |

---

## 11. 参见

- [Pytest 文档](https://docs.pytest.org/)
- [unittest.mock 参考](https://docs.python.org/3/library/unittest.mock.html)
- [Azure Functions 测试](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python#unit-testing)
- [Dataverse SDK 示例](https://github.com/microsoft/PowerPlatform-DataverseClient-Python/tree/main/examples)


---
applyTo: '**'
---

# Dataverse Python SDK — 认证与安全模式

基于官方 Microsoft Azure SDK 认证文档和 Dataverse SDK 最佳实践。

## 1. 认证概述

Dataverse Python SDK 使用 Azure Identity 凭据进行基于令牌的认证。这种方法遵循最小特权原则，并且适用于本地开发、云部署和本地环境。

### 为什么使用基于令牌的认证？

**与连接字符串相比的优势**：
- 为您的应用程序建立所需的特定权限（最小特权原则）
- 凭据仅作用于预期的应用程序
- 使用托管身份时，无需存储或保护任何密钥
- 不需要代码更改即可在不同环境中无缝运行

---

## 2. 凭据类型与选择

### 交互式浏览器凭证（本地开发）

**适用场景**：开发人员在本地开发工作站进行开发和测试。

```python
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient

# 打开浏览器进行认证
credential = InteractiveBrowserCredential()
client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=credential
)

# 首次使用会提示登录；后续调用使用缓存的令牌
records = client.get("account")
```

**适用情况**：
- ✅ 交互式开发和测试
- ✅ 带有用户界面的桌面应用程序
- ❌ 背景服务或计划任务

---

### 默认 Azure 凭据（推荐用于所有环境）

**适用场景**：在多个环境中运行的应用程序（开发 → 测试 → 生产）。

```python
from azure.identity import DefaultAzureCredential
from PowerPlatform.Dataverse.client import DataverseClient

# 按以下顺序尝试凭据：
# 1. 环境变量（应用服务主体）
# 2. Azure CLI 凭据（本地开发）
# 3. Azure PowerShell 凭据（本地开发）
# 4. 托管身份（在 Azure 上运行时）
credential = DefaultAzureCredential()

client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=credential
)

records = client.get("account")
```

**优势**：
- 单一代码路径适用于所有环境
- 不需要环境特定的逻辑
- 自动检测可用凭据
- 生产应用程序的首选方案

**凭据链**：
1. 环境变量 (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`)
2. Visual Studio Code 登录
3. Azure CLI (`az login`)
4. Azure PowerShell (`Connect-AzAccount`)
5. 托管身份（适用于 Azure 虚拟机、应用服务、AKS 等）

---

### 客户端密钥凭证（服务主体）

**适用场景**：无人值守的认证（计划任务、脚本、本地服务）。

```python
from azure.identity import ClientSecretCredential
from PowerPlatform.Dataverse.client import DataverseClient
import os

credential = ClientSecretCredential(
    tenant_id=os.environ["AZURE_TENANT_ID"],
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"]
)

client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=credential
)

records = client.get("account")
```

**设置步骤**：
1. 在 Azure AD 中创建应用程序注册
2. 创建客户端密钥（务必安全保管！）
3. 向应用程序授予 Dataverse 权限
4. 将凭据存储在环境变量或安全保险库中

**安全注意事项**：
- ⚠️ 绝不要在源代码中硬编码凭据
- ⚠️ 将密钥存储在 Azure Key Vault 或环境变量中
- ⚠️ 定期轮换凭据
- ⚠️ 使用最小必要权限

---

### 托管身份凭证（Azure 资源）

**适用场景**：托管在 Azure 上的应用程序（应用服务、Azure 函数、AKS、虚拟机等）。

```python
from azure.identity import ManagedIdentityCredential
from PowerPlatform.Dataverse.client import DataverseClient

# 无需管理密钥 - Azure 会管理身份
credential = ManagedIdentityCredential()

client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=credential
)

records = client.get("account")
```

**优势**：
- ✅ 无需管理密钥
- ✅ 自动令牌刷新
- ✅ 高安全性
- ✅ 内置于 Azure 服务中

**设置**：
1. 在 Azure 资源（应用服务、虚拟机等）上启用托管身份
2. 在 Dataverse 中授予托管身份权限
3. 代码会自动使用该身份

---

## 3. 环境特定配置

### 本地开发

```python
# .env 文件（Git 忽略）
DATAVERSE_URL=https://myorg-dev.crm.dynamics.com

# Python 代码
import os
from azure.identity import DefaultAzureCredential
from PowerPlatform.Dataverse.client import DataverseClient

# 使用您的 Azure CLI 凭据
credential = DefaultAzureCredential()
client = DataverseClient(
    base_url=os.environ["DATAVERSE_URL"],
    credential=credential
)
```

**设置**：使用您的开发者账户执行 `az login`

---

### Azure 应用服务 / Azure 函数

```python
from azure.identity import ManagedIdentityCredential
from PowerPlatform.Dataverse.client import DataverseClient

# 自动使用托管身份
credential = ManagedIdentityCredential()
client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=credential
)
```

**设置**：在应用服务中启用托管身份，并在 Dataverse 中授予权限

---

### 本地 / 第三方托管

```python
import os
from azure.identity import ClientSecretCredential
from PowerPlatform.Dataverse.client import DataverseClient

credential = ClientSecretCredential(
    tenant_id=os.environ["AZURE_TENANT_ID"],
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"]
)

client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=credential
)
```

**设置**：创建服务主体，安全存储凭据，并在 Dataverse 中授予权限

---

## 4. 客户端配置与连接设置

### 基本配置

```python
from PowerPlatform.Dataverse.core.config import DataverseConfig
from azure.identity import DefaultAzureCredential
from PowerPlatform.Dataverse.client import DataverseClient

cfg = DataverseConfig()
cfg.logging_enable = True  # 启用详细日志记录

client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=DefaultAzureCredential(),
    config=cfg
)
```

### HTTP 调优

```python
from PowerPlatform.Dataverse.core.config import DataverseConfig

cfg = DataverseConfig()

# 超时设置
cfg.http_timeout = 30          # 请求超时时间（秒）

# 重试配置
cfg.http_retries = 3           # 重试次数
cfg.http_backoff = 1           # 初始回退时间（秒）

# 连接复用
cfg.connection_timeout = 5     # 连接超时时间

client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=credential,
    config=cfg
)
```

---

## 5. 安全最佳实践

### 1. 不要硬编码凭据

```python
# ❌ 不推荐 - 切勿这样做！
credential = ClientSecretCredential(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-secret-key"  # 暴露！
)

# ✅ 推荐 - 使用环境变量
import os
credential = ClientSecretCredential(
    tenant_id=os.environ["AZURE_TENANT_ID"],
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"]
)
```

### 2. 安全存储密钥

**开发**：
```bash
# .env 文件（Git 忽略）
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-secret-key
```

**生产**：
```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# 从 Azure Key Vault 中检索密钥
credential = DefaultAzureCredential()
client = SecretClient(
    vault_url="https://mykeyvault.vault.azure.net",
    credential=credential
)

secret = client.get_secret("dataverse-client-secret")
```

### 3. 实施最小特权原则

```python
# 授予最小必要权限：
# - 如果应用程序只读，仅授予读取权限
# - 如果可能，仅授予特定表的权限
# - 限制凭证有效期（自动轮换）
# - 使用托管身份而不是共享密钥
```

### 4. 监控认证事件

```python
import logging

logger = logging.getLogger("dataverse_auth")

try:
    client = DataverseClient(
        base_url="https://myorg.crm.dynamics.com",
        credential=credential
    )
    logger.info("成功认证到 Dataverse")
except Exception as e:
    logger.error(f"认证失败: {e}")
    raise
```

### 5. 处理令牌过期

```python
from azure.core.exceptions import ClientAuthenticationError
import time

def create_with_auth_retry(client, table_name, payload, max_retries=2):
    """创建记录，如果令牌过期则重试。"""
    for attempt in range(max_retries):
        try:
            return client.create(table_name, payload)
        except ClientAuthenticationError:
            if attempt < max_retries - 1:
                logger.warning("令牌过期，正在重试...")
                time.sleep(1)
            else:
                raise
```

---

## 6. 多租户应用程序

### 租户感知客户端

```python
from azure.identity import DefaultAzureCredential
from PowerPlatform.Dataverse.client import DataverseClient

def get_client_for_tenant(tenant_id: str) -> DataverseClient:
    """获取特定租户的 Dataverse 客户端。"""
    credential = DefaultAzureCredential()
    
    # Dataverse URL 包含租户特定的组织
    base_url = f"https://{get_org_for_tenant(tenant_id)}.crm.dynamics.com"
    
    return DataverseClient(
        base_url=base_url,
        credential=credential
    )

def get_org_for_tenant(tenant_id: str) -> str:
    """将租户映射到 Dataverse 组织。"""
    # 实现取决于您的多租户策略
    # 可以是数据库查找、配置等
    pass
```

---

## 7. 认证问题排查

### 错误： "访问被拒绝" (403)

```python
try:
    client.get("account")
except DataverseError as e:
    if e.status_code == 403:
        print("用户/应用程序缺少 Dataverse 权限")
        print("请确保已分配 Dataverse 安全角色")
```

### 错误： "无效凭据" (401)

```python
# 检查凭据来源
from azure.identity import DefaultAzureCredential

try:
    cred = DefaultAzureCredential(exclude_cli_credential=False, 
                                  exclude_powershell_credential=False)
    # 强制重新认证
    import subprocess
    subprocess.run(["az", "login"])
except Exception as e:
    print(f"认证失败: {e}")
```

### 错误： "无效租户"

```python
# 验证租户 ID
import json
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
token = credential.get_token("https://dataverse.dynamics.com/.default")

# 解码令牌以验证租户
import base64
payload = base64.b64decode(token.token.split('.')[1] + '==')
claims = json.loads(payload)
print(f"令牌租户: {claims.get('tid')}")
```

---

## 8. 凭据生命周期

### 令牌刷新

Azure Identity 会自动处理令牌刷新：

```python
# 令牌会被缓存并自动刷新
credential = DefaultAzureCredential()

# 第一次调用获取令牌
client.get("account")

# 后续调用复用缓存的令牌
client.get("contact")

# 如果令牌过期，SDK 会自动刷新
```

### 会话管理

```python
class DataverseSession:
    """管理 DataverseClient 生命周期。"""
    
    def __init__(self, base_url: str):
        from azure.identity import DefaultAzureCredential
        
        self.client = DataverseClient(
            base_url=base_url,
            credential=DefaultAzureCredential()
        )
    
    def __enter__(self):
        return self.client
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 如需清理，请在此处添加逻辑
        pass

# 使用示例
with DataverseSession("https://myorg.crm.dynamics.com") as client:
    records = client.get("account")
```

---

## 9. Dataverse 特定安全

### 行级安全（RLS）

用户在 Dataverse 中的安全角色决定了其可访问的记录：

```python
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient

# 每个用户都会获得带有其凭据的客户端
def get_user_client(user_username: str) -> DataverseClient:
    # 用户必须已经认证
    credential = InteractiveBrowserCredential()
    
    client = DataverseClient(
        base_url="https://myorg.crm.dynamics.com",
        credential=credential
    )
    
    # 用户只能看到其有权访问的记录
    return client
```

### 安全角色

分配最小必要角色：
- **系统管理员**：完全访问权限（避免用于应用程序）
- **销售经理**：销售表 + 报表
- **服务代表**：服务案例 + 知识库
- **自定义**：创建具有特定表权限的角色

---

## 10. 参见

- [Azure 身份验证客户端库](https://learn.microsoft.com/en-us/python/api/azure-identity)
- [认证到 Azure 服务](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/overview)
- [Azure Key Vault 密钥管理](https://learn.microsoft.com/en-us/azure/key-vault/general/overview)
- [Dataverse 安全模型](https://learn.microsoft.com/en-us/power-platform/admin/security/security-overview)
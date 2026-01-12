

# Dataverse Python SDK - 代理工作流指南

## ⚠️ 预览功能通知

**状态**：该功能自2025年12月起进入**公共预览**  
**可用性**：通用可用性（GA）日期待定  
**文档**：完整的实现细节即将发布  

本指南涵盖了使用 Dataverse Python SDK 构建代理工作流的概念框架和计划功能。在通用可用性发布前，具体的 API 和实现可能会发生变化。

---

## 1. 概述：使用 Dataverse 构建代理工作流

### 什么是代理工作流？

代理工作流是自主、智能的流程，其中：
- **代理**根据数据和规则进行决策并采取行动
- **工作流**协调复杂的多步骤操作
- **Dataverse**作为企业数据的核心真实来源

Dataverse Python SDK 的设计目的是让数据科学家和开发者无需 .NET 专业知识即可构建这些智能系统。

### 计划中的关键功能

SDK 的战略定位是支持以下功能：

1. **自主数据代理** - 独立查询、更新和评估数据质量  
2. **表单预测与自动填充** - 基于数据模式和上下文预填充表单  
3. **模型上下文协议 (MCP)** 支持 - 实现标准化的代理与工具通信  
4. **代理对代理 (A2A)** 协作 - 多个代理协同完成复杂任务  
5. **语义建模** - 理解数据关系的自然语言处理  
6. **安全代理** - 以特定用户身份运行操作并保留审计追踪  
7. **内置合规性** - 强制执行数据治理和保留策略  

---

## 2. 代理系统的架构模式

### 多代理模式
```python
# 概念性模式 - 具体 API 待 GA
class DataQualityAgent:
    """监控并改进数据质量的自主代理。"""
    
    def __init__(self, client):
        self.client = client
    
    async def evaluate_data_quality(self, table_name):
        """评估表的数据质量指标。"""
        records = await self.client.get(table_name)
        
        metrics = {
            'total_records': len(records),
            'null_values': sum(1 for r in records if None in r.values()),
            'duplicate_records': await self._find_duplicates(table_name)
        }
        return metrics
    
    async def auto_remediate(self, issues):
        """自动修复发现的数据质量问题。"""
        # 代理自主决定修复操作
        pass

class DataEnrichmentAgent:
    """从外部来源丰富数据的自主代理。"""
    
    async def enrich_accounts(self):
        """使用市场信息丰富账户数据。"""
        accounts = await self.client.get("account")
        
        for account in accounts:
            enrichment = await self._lookup_market_data(account['name'])
            await self.client.update("account", account['id'], enrichment)
```

### 代理编排模式
```python
# 概念性模式 - 具体 API 待 GA
class DataPipeline:
    """编排多个代理协同工作的流程。"""
    
    def __init__(self, client):
        self.quality_agent = DataQualityAgent(client)
        self.enrichment_agent = DataEnrichmentAgent(client)
        self.sync_agent = SyncAgent(client)
    
    async def run(self, table_name):
        """执行多代理工作流。"""
        # 步骤1：质量检查
        print("运行质量检查...")
        issues = await self.quality_agent.evaluate_data_quality(table_name)
        
        # 步骤2：丰富数据
        print("丰富数据...")
        await self.enrichment_agent.enrich_accounts()
        
        # 步骤3：同步到外部系统
        print("同步到外部系统...")
        await self.sync_agent.sync_to_external_db(table_name)
```

---

## 3. 模型上下文协议 (MCP) 支持（计划中）

### 什么是 MCP？

模型上下文协议（MCP）是一个开放标准，用于：
- **工具定义** - 描述可用的工具/能力  
- **工具调用** - 允许大语言模型（LLM）使用参数调用工具  
- **上下文管理** - 管理代理与工具之间的上下文  
- **错误处理** - 标准化的错误响应  

### MCP 集成模式（概念性）
```python
# 概念性模式 - 具体 API 待 GA
from dataverse_mcp import DataverseMCPServer

# 定义可用工具
tools = [
    {
        "name": "query_accounts",
        "description": "带过滤条件查询账户",
        "parameters": {
            "filter": "OData 过滤表达式",
            "select": "要检索的列",
            "top": "最大记录数"
        }
    },
    {
        "name": "create_account",
        "description": "创建新账户",
        "parameters": {
            "name": "账户名称",
            "credit_limit": "信用额度金额"
        }
    },
    {
        "name": "update_account",
        "description": "更新账户字段",
        "parameters": {
            "account_id": "账户 GUID",
            "updates": "字段更新的字典"
        }
    }
]

# 创建 MCP 服务器
server = DataverseMCPServer(client, tools=tools)

# 大语言模型现在可以使用 Dataverse 工具
await server.handle_tool_call("query_accounts", {
    "filter": "creditlimit gt 100000",
    "select": ["name", "creditlimit"]
})
```

---

## 4. 代理对代理 (A2A) 协作（计划中）

### A2A 通信模式
```python
# 概念性模式 - 具体 API 待 GA
class DataValidationAgent:
    """在下游代理处理数据前验证数据。"""
    
    async def validate_and_notify(self, data):
        """验证数据并通知其他代理。"""
        if await self._is_valid(data):
            # 发布事件，其他代理可以订阅
            await self.publish_event("data_validated", data)
        else:
            await self.publish_event("validation_failed", data)

class DataProcessingAgent:
    """等待验证代理提供的有效数据。"""
    
    async def __init__(self):
        self.subscribe("data_validated", self.process_data)
    
    async def process_data(self, data):
        """处理已验证的数据。"""
        # 代理可以安全地假设数据有效
        result = await self._transform(data)
        await self.publish_event("processing_complete", result)
```

---

## 5. 构建自主数据代理

### 数据质量代理示例
```python
# 使用当前 SDK 功能的示例
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import InteractiveBrowserCredential
import json

class DataQualityAgent:
    """监控并报告数据质量。"""
    
    def __init__(self, org_url, credential):
        self.client = DataverseClient(org_url, credential)
    
    def analyze_completeness(self, table_name, required_fields):
        """分析字段完整性。"""
        records = self.client.get(
            table_name,
            select=required_fields
        )
        
        missing_by_field = {field: 0 for field in required_fields}
        total = 0
        
        for page in records:
            for record in page:
                total += 1
                for field in required_fields:
                    if field not in record or record[field] is None:
                        missing_by_field[field] += 1
        
        # 计算完整性百分比
        completeness = {
            field: ((total - count) / total * 100) 
            for field, count in missing_by_field.items()
        }
        
        return {
            'table': table_name,
            'total_records': total,
            'completeness': completeness,
            'missing_counts': missing_by_field
        }
    
    def detect_duplicates(self, table_name, key_fields):
        """检测潜在重复记录。"""
        records = self.client.get(table_name, select=key_fields)
        
        all_records = []
        for page in records:
            all_records.extend(page)
        
        seen = {}
        duplicates = []
        
        for record in all_records:
            key = tuple(record.get(f) for f in key_fields)
            if key in seen:
                duplicates.append({
                    'original_id': seen[key],
                    'duplicate_id': record.get('id'),
                    'key': key
                })
            else:
                seen[key] = record.get('id')
        
        return {
            'table': table_name,
            'duplicate_count': len(duplicates),
            'duplicates': duplicates
        }
    
    def generate_quality_report(self, table_name):
        """生成全面的质量报告。"""
        completeness = self.analyze_completeness(
            table_name,
            ['name', 'telephone1', 'emailaddress1']
        )
        
        duplicates = self.detect_duplicates(
            table_name,
            ['name', 'emailaddress1']
        )
        
        return {
            'timestamp': pd.Timestamp.now().isoformat(),
            'table': table_name,
            'completeness': completeness,
            'duplicates': duplicates
        }

# 使用示例
client = DataverseClient("https://<org>.crm.dynamics.com", InteractiveBrowserCredential())
agent = DataQualityAgent("https://<org>.crm.dynamics.com", InteractiveBrowserCredential())

report = agent.generate_quality_report("account")
print(json.dumps(report, indent=2))
```

### 表单预测代理示例
```python
# 使用当前 SDK 功能的概念性模式
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

class FormPredictionAgent:
    """预测并自动填充表单值。"""
    
    def __init__(self, org_url, credential):
        self.client = DataverseClient(org_url, credential)
        self.model = None
    
    def train_on_historical_data(self, table_name, features, target):
        """在历史数据上训练预测模型。"""
        # 收集训练数据
        records = []
        for page in self.client.get(table_name, select=features + [target]):
            records.extend(page)
        
        df = pd.DataFrame(records)
        
        # 训练模型
        X = df[features].fillna(0)
        y = df[target]
        
        self.model = RandomForestRegressor()
        self.model.fit(X, y)
        
        return self.model.score(X, y)
    
    def predict_field_values(self, table_name, record_id, features_data):
        """预测缺失字段值。"""
        if self.model is None:
            raise ValueError("模型尚未训练，请先调用 train_on_historical_data。")
        
        # 进行预测
        prediction = self.model.predict([features_data])[0]
        
        # 返回预测值及置信度
        return {
            'record_id': record_id,
            'predicted_value': prediction,
            'confidence': self.model.score([features_data], [prediction])
        }
```

---

## 6. 与 AI/ML 服务集成

### 大语言模型 (LLM) 集成模式
```python
# 使用 LLM 解释 Dataverse 数据
from openai import OpenAI

class DataInsightAgent:
    """使用 LLM 从 Dataverse 数据中生成见解。"""
    
    def __init__(self, org_url, credential, openai_key):
        self.client = DataverseClient(org_url, credential)
        self.llm = OpenAI(api_key=openai_key)
    
    def analyze_with_llm(self, table_name, sample_size=100):
        """使用 LLM 分析数据。"""
        # 获取样本数据
        records = []
        count = 0
        for page in self.client.get(table_name):
            records.extend(page)
            count += len(page)
            if count >= sample_size:
                break
        
        # 为 LLM 创建摘要
        summary = f"""
        表: {table_name}
        采样记录总数: {len(records)}
        
        样本数据:
        {json.dumps(records[:5], indent=2, default=str)}
        
        请提供关于这些数据的见解。
        """
        
        # 向 LLM 发起请求
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": summary}]
        )
        
        return response.choices[0].message.content
```

---

## 7. 安全代理与审计追踪

### 计划中的功能

SDK 将支持以特定用户身份运行操作：

```python
# 概念性模式 - 具体 API 待 GA
from dataverse_security import ImpersonationContext

# 以不同用户身份运行
with ImpersonationContext(client, user_id="user-guid"):
    # 所有操作均以该用户身份执行
    client.create("account", {"name": "新账户"})
    # 审计追踪：由 [user-guid] 于 [时间戳] 创建

# 获取审计追踪
audit_log = client.get_audit_trail(
    table="account",
    record_id="record-guid",
    action="create"
)
```

---

## 8. 合规性与数据治理

### 计划中的治理功能

```python
# 概念性模式 - 具体 API 待 GA
from dataverse_governance import DataGovernance

# 定义保留策略
governance = DataGovernance(client)
governance.set_retention_policy(
    table="account",
    retention_days=365
)

# 定义数据分类
governance.classify_columns(
    table="account",
    classifications={
        "name": "公开",
        "telephone1": "内部",
        "creditlimit": "机密"
    }
)

# 强制执行策略
governance.enforce_all_policies()
```

---

## 9. 当前支持代理工作流的 SDK 功能

尽管完整的代理功能处于预览状态，当前 SDK 已支持代理构建：

### ✅ 现在可用
- **CRUD 操作** - 创建、检索、更新、删除数据  
- **批量操作** - 高效处理大型数据集  
- **查询功能** - 支持 OData 和 SQL 灵活检索数据  
- **元数据操作** - 与表和列定义交互  
- **错误处理** - 结构化异常体系  
- **分页** - 处理大型结果集  
- **文件上传** - 管理文档附件  

### 🔜 GA 期间发布
- 完整的 MCP 集成  
- A2A 协作基础功能  
- 增强的认证/代理功能  
- 治理策略强制执行  
- 原生异步/等待支持  
- 高级缓存策略  

---

## 10. 快速入门：今天构建你的第一个代理

```python
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import InteractiveBrowserCredential
import json

class SimpleDataAgent:
    """你的第一个 Dataverse 代理。"""
    
    def __init__(self, org_url):
        credential = InteractiveBrowserCredential()
        self.client = DataverseClient(org_url, credential)
    
    def check_health(self, table_name):
        """代理功能：检查表的健康状态。"""
        try:
            tables = self.client.list_tables()
            matching = [t for t in tables if t['LogicalName'] == table_name]
            
            if not matching:
                return {"status": "error", "message": f"未找到表 {table_name}"}
            
            # 获取记录数量
            records = []
            for page in self.client.get(table_name):
                records.extend(page)
                if len(records) > 1000:
                    break
            
            return {
                "status": "healthy",
                "table": table_name,
                "record_count": len(records),
                "timestamp": pd.Timestamp.now().isoformat()
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

# 使用示例
agent = SimpleDataAgent("https://<org>.crm.dynamics.com")
health = agent.check_health("account")
print(json.dumps(health, indent=2))
```

---

## 11. 资源与文档

### 官方文档
- [Dataverse Python SDK 概述](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/overview)
- [数据操作](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/work-data)
- [发布计划：代理工作流](https://learn.microsoft.com/en-us/power-platform/release-plan/2025wave2/data-platform/build-agentic-flows-dataverse-sdk-python)

### 外部资源
- [模型上下文协议](https://modelcontextprotocol.io/)
- [Azure AI 服务](https://learn.microsoft.com/en-us/azure/ai-services/)
- [Python 异步/等待](https://docs.python.org/3/library/asyncio.html)

### 仓库
- [SDK 源代码](https://github.com/microsoft/PowerPlatform-DataverseClient-Python)
- [问题与功能请求](https://github.com/microsoft/PowerPlatform-DataverseClient-Python/issues)

---

## 12. 常见问题解答：代理工作流

**问：我能否使用当前 SDK 构建代理系统？**  
答：是的！可以使用当前功能构建类似代理的系统。完整的 MCP/A2A 支持将在 GA 发布。

**问：当前 SDK 与代理功能有何不同？**  
答：当前：同步的 CRUD 操作；代理功能：异步、自主决策、代理协作。

**问：从预览到 GA 是否会有破坏性变更？**  
答：有可能。这是一个预览功能，通用可用性发布前可能会进行 API 优化。

**问：我该如何为代理工作流做准备？**  
答：使用当前的 CRUD 操作构建代理，设计时考虑异步模式，使用 MCP 规范确保未来兼容性。

**问：代理功能是否有成本差异？**  
答：目前尚不清楚。请在 GA 接近时查看发布说明。

---

## 13. 下一步

1. **使用当前 SDK 功能构建原型**  
2. **在 MCP 集成发布时加入预览**  
3. **通过 GitHub 问题反馈**  
4. **关注 GA 宣布与完整 API 文档**  
5. **准备好后迁移到完整代理功能**  

Dataverse Python SDK 正在定位为构建 Microsoft Power Platform 上智能自主数据系统的首选平台。
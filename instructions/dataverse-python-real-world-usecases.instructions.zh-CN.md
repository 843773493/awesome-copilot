

---
applyTo: '**'
---

# Dataverse Python SDK — 实际应用场景与模板

基于官方 Dataverse 数据迁移和集成模式。

## 1. 从遗留系统迁移数据

### 迁移架构

```
Legacy System → Staging Database → Dataverse
    (提取)    (转换)        (加载)
```

### 完整迁移示例

```python
import pandas as pd
import time
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.errors import DataverseError
from azure.identity import DefaultAzureCredential

class DataMigrationPipeline:
    """从遗留系统迁移数据到 Dataverse."""
    
    def __init__(self, org_url: str):
        self.client = DataverseClient(
            base_url=org_url,
            credential=DefaultAzureCredential()
        )
        self.success_records = []
        self.failed_records = []
    
    def extract_from_legacy(self, legacy_db_connection, query: str):
        """从源系统提取数据."""
        return pd.read_sql(query, legacy_db_connection)
    
    def transform_accounts(self, df: pd.DataFrame) -> list:
        """将源数据转换为 Dataverse 模式."""
        payloads = []
        
        for _, row in df.iterrows():
            # 将源字段映射到 Dataverse
            payload = {
                "name": row["company_name"][:100],  # 限制为 100 个字符
                "telephone1": row["phone"],
                "websiteurl": row["website"],
                "revenue": float(row["annual_revenue"]) if row["annual_revenue"] else None,
                "numberofemployees": int(row["employees"]) if row["employees"] else None,
                # 跟踪源 ID 以进行对账
                "new_sourcecompanyid": str(row["legacy_id"]),
                "new_importsequencenumber": row["legacy_id"]
            }
            payloads.append(payload)
        
        return payloads
    
    def load_to_dataverse(self, payloads: list, batch_size: int = 200):
        """将数据加载到 Dataverse 并跟踪错误."""
        total = len(payloads)
        
        for i in range(0, total, batch_size):
            batch = payloads[i:i + batch_size]
            
            try:
                ids = self.client.create("account", batch)
                self.success_records.extend(ids)
                print(f"✓ 创建了 {len(ids)} 条记录 ({len(self.success_records)}/{total})")
                
                # 防止速率限制
                time.sleep(0.5)
                
            except DataverseError as e:
                self.failed_records.extend(batch)
                print(f"✗ 批次失败: {e.message}")
    
    def reconcile_migration(self, df: pd.DataFrame):
        """验证迁移并跟踪结果."""
        
        # 查询已创建的记录
        created_accounts = self.client.get(
            "account",
            filter="new_importsequencenumber ne null",
            select=["accountid", "new_sourcecompanyid", "new_importsequencenumber"],
            top=10000
        )
        
        created_df = pd.DataFrame(list(created_accounts))
        
        # 更新源表以包含 Dataverse ID
        merged = df.merge(
            created_df,
            left_on="legacy_id",
            right_on="new_importsequencenumber"
        )
        
        print(f"成功迁移了 {len(merged)} 条账户信息")
        print(f"失败: {len(self.failed_records)} 条记录")
        
        return {
            "total_source": len(df),
            "migrated": len(merged),
            "failed": len(self.failed_records),
            "success_rate": len(merged) / len(df) * 100
        }

# 使用示例
pipeline = DataMigrationPipeline("https://myorg.crm.dynamics.com")

# 提取数据
source_data = pipeline.extract_from_legacy(
    legacy_connection,
    "SELECT id, company_name, phone, website, annual_revenue, employees FROM companies"
)

# 数据转换
payloads = pipeline.transform_accounts(source_data)

# 数据加载
pipeline.load_to_dataverse(payloads, batch_size=300)

# 数据对账
results = pipeline.reconcile_migration(source_data)
print(results)
```

---

## 2. 数据质量与去重代理

### 检测并合并重复数据

```python
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import DefaultAzureCredential
import difflib

class DataQualityAgent:
    """监控并提升数据质量."""
    
    def __init__(self, org_url: str):
        self.client = DataverseClient(
            base_url=org_url,
            credential=DefaultAzureCredential()
        )
    
    def find_potential_duplicates(self, table_name: str, match_fields: list):
        """查找潜在重复记录."""
        
        records = []
        for page in self.client.get(table_name, select=match_fields, top=10000):
            records.extend(page)
        
        duplicates = []
        seen = {}
        
        for record in records:
            # 从匹配字段创建键
            key = tuple(
                record.get(field, "").lower().strip() 
                for field in match_fields
            )
            
            if key in seen and key != ("",) * len(match_fields):
                duplicates.append({
                    "original": seen[key],
                    "duplicate": record,
                    "fields_matched": match_fields
                })
            else:
                seen[key] = record
        
        return duplicates, len(records)
    
    def merge_records(self, table_name: str, primary_id: str, duplicate_id: str, 
                     mapping: dict):
        """将重复记录合并到主记录中."""
        
        # 将重复数据复制到主记录
        updates = {}
        duplicate = self.client.get(table_name, duplicate_id)
        
        for source_field, target_field in mapping.items():
            if duplicate.get(source_field) and not primary.get(target_field):
                updates[target_field] = duplicate[source_field]
        
        # 更新主记录
        if updates:
            self.client.update(table_name, primary_id, updates)
        
        # 删除重复记录
        self.client.delete(table_name, duplicate_id)
        
        return f"将 {duplicate_id} 合并到 {primary_id}"
    
    def generate_quality_report(self, table_name: str) -> dict:
        """生成数据质量指标报告."""
        
        records = list(self.client.get(table_name, top=10000))
        
        report = {
            "表": table_name,
            "总记录数": len(records),
            "空值": {},
            "重复记录数": 0,
            "完整性评分": 0
        }
        
        # 检查空值
        all_fields = set()
        for record in records:
            all_fields.update(record.keys())
        
        for field in all_fields:
            null_count = sum(1 for r in records if not r.get(field))
            completeness = (len(records) - null_count) / len(records) * 100
            
            if completeness < 100:
                report["空值"][field] = {
                    "空值数量": null_count,
                    "完整性": completeness
                }
        
        # 检查重复记录
        duplicates, _ = self.find_potential_duplicates(
            table_name, 
            ["name", "emailaddress1"]
        )
        report["重复记录数"] = len(duplicates)
        
        # 总体完整性评分
        avg_completeness = sum(
            100 - ((d["空值数量"] / len(records)) * 100)
            for d in report["空值"].values()
        ) / len(report["空值"]) if report["空值"] else 100
        report["完整性评分"] = avg_completeness
        
        return report

# 使用示例
agent = DataQualityAgent("https://myorg.crm.dynamics.com")

# 查找重复记录
duplicates, total = agent.find_potential_duplicates(
    "account",
    match_fields=["name", "emailaddress1"]
)

print(f"在 {total} 条账户信息中发现 {len(duplicates)} 条潜在重复记录")

# 确认后合并
for dup in duplicates[:5]:  # 处理前 5 条
    result = agent.merge_records(
        "account",
        primary_id=dup["original"]["accountid"],
        duplicate_id=dup["duplicate"]["accountid"],
        mapping={"telephone1": "telephone1", "websiteurl": "websiteurl"}
    )
    print(result)

# 生成质量报告
report = agent.generate_quality_report("account")
print(f"数据质量: {report['完整性评分']:.1f}%")
```

---

## 3. 联系人与账户信息增强

### 从外部源增强 CRM 数据

```python
import requests
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import DefaultAzureCredential

class DataEnrichmentAgent:
    """使用外部数据增强 CRM 记录."""
    
    def __init__(self, org_url: str, external_api_key: str):
        self.client = DataverseClient(
            base_url=org_url,
            credential=DefaultAzureCredential()
        )
        self.api_key = external_api_key
    
    def enrich_accounts_with_industry_data(self):
        """使用行业分类信息增强账户."""
        
        accounts = self.client.get(
            "account",
            select=["accountid", "name", "websiteurl"],
            filter="new_industrydata eq null",
            top=500
        )
        
        enriched_count = 0
        for page in accounts:
            for account in page:
                try:
                    # 调用外部 API
                    industry = self._lookup_industry(account["name"])
                    
                    if industry:
                        self.client.update(
                            "account",
                            account["accountid"],
                            {"new_industrydata": industry}
                        )
                        enriched_count += 1
                
                except Exception as e:
                    print(f"增强 {account['name']} 失败: {e}")
        
        return enriched_count
    
    def enrich_contacts_with_social_profiles(self):
        """查找并关联社交媒体资料."""
        
        contacts = self.client.get(
            "contact",
            select=["contactid", "fullname", "emailaddress1"],
            filter="new_linkedinurl eq null",
            top=500
        )
        
        for page in contacts:
            for contact in page:
                try:
                    # 查找社交媒体资料
                    profiles = self._find_social_profiles(
                        contact["fullname"],
                        contact["emailaddress1"]
                    )
                    
                    if profiles:
                        self.client.update(
                            "contact",
                            contact["contactid"],
                            {
                                "new_linkedinurl": profiles.get("linkedin"),
                                "new_twitterhandle": profiles.get("twitter")
                            }
                        )
                
                except Exception as e:
                    print(f"增强 {contact['fullname']} 失败: {e}")
    
    def _lookup_industry(self, company_name: str) -> str:
        """调用外部行业 API."""
        response = requests.get(
            "https://api.example.com/industry",
            params={"company": company_name},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        if response.status_code == 200:
            return response.json().get("industry")
        return None
    
    def _find_social_profiles(self, name: str, email: str) -> dict:
        """查找个人的社交媒体资料."""
        response = requests.get(
            "https://api.example.com/social",
            params={"name": name, "email": email},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        if response.status_code == 200:
            return response.json()
        return {}

# 使用示例
enricher = DataEnrichmentAgent(
    "https://myorg.crm.dynamics.com",
    api_key="your-api-key"
)

enriched = enricher.enrich_accounts_with_industry_data()
print(f"增强了 {enriched} 条账户信息")
```

---

## 4. 自动化报告数据导出

### 将 CRM 数据导出到 Excel

```python
import pandas as pd
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import DefaultAzureCredential
from datetime import datetime

class ReportExporter:
    """将 Dataverse 数据导出为报告."""
    
    def __init__(self, org_url: str):
        self.client = DataverseClient(
            base_url=org_url,
            credential=DefaultAzureCredential()
        )
    
    def export_sales_summary(self, output_file: str):
        """导出销售数据用于报告."""
        
        accounts = []
        for page in self.client.get(
            "account",
            select=["accountid", "name", "revenue", "numberofemployees", 
                   "createdon", "modifiedon"],
            filter="statecode eq 0",  # 仅活跃账户
            orderby=["revenue desc"],
            top=10000
        ):
            accounts.extend(page)
        
        # 商机
        opportunities = []
        for page in self.client.get(
            "opportunity",
            select=["opportunityid", "name", "estimatedvalue", 
                   "statuscode", "parentaccountid", "createdon"],
            top=10000
        ):
            opportunities.extend(page)
        
        # 创建数据框
        df_accounts = pd.DataFrame(accounts)
        df_opportunities = pd.DataFrame(opportunities)
        
        # 生成报告
        with pd.ExcelWriter(output_file) as writer:
            df_accounts.to_excel(writer, sheet_name="账户", index=False)
            df_opportunities.to_excel(writer, sheet_name="商机", index=False)
            
            # 总结工作表
            summary = pd.DataFrame({
                "指标": [
                    "总账户数",
                    "总商机数",
                    "总收入",
                    "导出日期"
                ],
                "数值": [
                    len(df_accounts),
                    len(df_opportunities),
                    df_accounts["revenue"].sum() if "revenue" in df_accounts else 0,
                    datetime.now().isoformat()
                ]
            })
            summary.to_excel(writer, sheet_name="总结", index=False)
        
        return output_file
    
    def export_activity_log(self, days_back: int = 30) -> str:
        """导出最近的活动日志用于审计."""
        
        from_date = pd.Timestamp.now(tz='UTC') - pd.Timedelta(days=days_back)
        
        activities = []
        for page in self.client.get(
            "activitypointer",
            select=["activityid", "subject", "activitytypecode", 
                   "createdon", "ownerid"],
            filter=f"createdon gt {from_date.isoformat()}",
            orderby=["createdon desc"],
            top=10000
        ):
            activities.extend(page)
        
        df = pd.DataFrame(activities)
        output = f"activity_log_{datetime.now():%Y%m%d}.csv"
        df.to_csv(output, index=False)
        
        return output

# 使用示例
exporter = ReportExporter("https://myorg.crm.dynamics.com")
report_file = exporter.export_sales_summary("sales_report.xlsx")
print(f"报告已保存至 {report_file}")
```

---

## 5. 工作流集成 — 批量操作

### 根据条件处理记录

```python
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import DefaultAzureCredential
from enum import IntEnum

class AccountStatus(IntEnum):
    潜在客户 = 1
    活跃 = 2
    已关闭 = 3

class BulkWorkflow:
    """自动化批量操作."""
    
    def __init__(self, org_url: str):
        self.client = DataverseClient(
            base_url=org_url,
            credential=DefaultAzureCredential()
        )
    
    def mark_accounts_as_inactive_if_no_activity(self, days_no_activity: int = 90):
        """标记无近期活动的账户为不活跃."""
        
        from_date = f"2025-{datetime.now().month:02d}-01T00:00:00Z"
        
        inactive_accounts = self.client.get(
            "account",
            select=["accountid", "name"],
            filter=f"modifiedon lt {from_date} and statecode eq 0",
            top=5000
        )
        
        accounts_to_deactivate = []
        for page in inactive_accounts:
            accounts_to_deactivate.extend([a["accountid"] for a in page])
        
        # 批量更新
        if accounts_to_deactivate:
            self.client.update("account", accounts_to_deactivate, {"statecode": AccountStatus.已关闭})
            print(f"已停用 {len(accounts_to_deactivate)} 条不活跃账户")
    
    def update_opportunity_status_based_on_amount(self):
        """根据预计价值更新商机阶段."""
        
        opportunities = self.client.get(
            "opportunity",
            select=["opportunityid", "estimatedvalue"],
            filter="statuscode ne 7",  # 排除已关闭状态
            top=5000
        )
        
        updates = []
        ids = []
        
        for page in opportunities:
            for opp in page:
                value = opp.get("estimatedvalue", 0)
                
                # 确定阶段
                if value < 10000:
                    stage = 1  # 初步接触
                elif value < 50000:
                    stage = 2  # 报价阶段
                else:
                    stage = 3  # 报价审核阶段
                
                updates.append({"stageid": stage})
                ids.append(opp["opportunityid"])
        
        # 批量更新
        if ids:
            self.client.update("opportunity", ids, updates)
            print(f"已更新 {len(ids)} 条商机")
```

---

## 6. 定时任务模板

### Azure 函数用于定时操作

```python
# scheduled_migration_job.py
import azure.functions as func
from datetime import datetime
from DataMigrationPipeline import DataMigrationPipeline
import logging

def main(timer: func.TimerRequest) -> None:
    """按计划运行迁移任务（例如每日）."""
    
    if timer.past_due:
        logging.info('定时任务已过期!')
    
    try:
        logging.info(f'迁移任务于 {datetime.utcnow()} 开始')
        
        # 运行迁移
        pipeline = DataMigrationPipeline("https://myorg.crm.dynamics.com")
        
        # 提取、转换、加载
        source_data = pipeline.extract_from_legacy(...)
        payloads = pipeline.transform_accounts(source_data)
        pipeline.load_to_dataverse(payloads)
        
        # 获取结果
        results = pipeline.reconcile_migration(source_data)
        
        logging.info(f'迁移完成: {results}')
        
    except Exception as e:
        logging.error(f'迁移失败: {e}')
        raise

# function_app.py - Azure 函数配置
app = func.FunctionApp()

@app.schedule_trigger(schedule="0 0 * * *")  # 每日午夜执行
def migration_job(timer: func.TimerRequest) -> None:
    main(timer)
```

---

## 7. 完整启动模板

```python
#!/usr/bin/env python3
"""
Python Dataverse SDK — 完整启动模板
"""

from azure.identity import DefaultAzureCredential
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.config import DataverseConfig
from PowerPlatform.Dataverse.core.errors import DataverseError
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataverseApp:
    """Dataverse 应用程序的基础类."""
    
    def __init__(self, org_url: str):
        self.org_url = org_url
        self.client = self._create_client()
    
    def _create_client(self) -> DataverseClient:
        """创建经过身份验证的客户端."""
        cfg = DataverseConfig()
        cfg.logging_enable = False
        
        return DataverseClient(
            base_url=self.org_url,
            credential=DefaultAzureCredential(),
            config=cfg
        )
    
    def create_account(self, name: str, phone: str = None) -> str:
        """创建账户记录."""
        try:
            payload = {"name": name}
            if phone:
                payload["telephone1"] = phone
            
            id = self.client.create("account", payload)[0]
            logger.info(f"创建账户: {id}")
            return id
        
        except DataverseError as e:
            logger.error(f"创建账户失败: {e.message}")
            raise
    
    def get_accounts(self, filter_expr: str = None, top: int = 100) -> list:
        """获取账户记录."""
        try:
            accounts = self.client.get(
                "account",
                filter=filter_expr,
                select=["accountid", "name", "telephone1", "createdon"],
                orderby=["createdon desc"],
                top=top
            )
            
            all_accounts = []
            for page in accounts:
                all_accounts.extend(page)
            
            logger.info(f"获取了 {len(all_accounts)} 条账户信息")
            return all_accounts
        
        except DataverseError as e:
            logger.error(f"获取账户信息失败: {e.message}")
            raise

if __name__ == "__main__":
    # 使用示例
    app = DataverseApp("https://myorg.crm.dynamics.com")
    
    # 创建账户
    account_id = app.create_account("Acme Inc", "555-0100")
    
    # 获取账户
    accounts = app.get_accounts(filter_expr="statecode eq 0", top=50)
    print(f"找到 {len(accounts)} 条活跃账户信息")
    
    # 更新账户
    app.update_account(account_id, telephone1="555-0199")
```

---

## 8. 参见

- [Dataverse 数据迁移](https://learn.microsoft.com/en-us/power-platform/architecture/key-concepts/data-migration/workflow-complex-data-migration)
- [使用数据（SDK）](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/work-data)
- [GitHub 上的 SDK 示例](https://github.com/microsoft/PowerPlatform-DataverseClient-Python/tree/main/examples)
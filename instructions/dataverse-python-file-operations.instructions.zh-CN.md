

# Dataverse Python SDK - 文件操作与实际示例

## 概述
关于使用 PowerPlatform-DataverseClient-Python SDK 进行文件上传操作、分块策略以及实际应用示例的完整指南。

---

## 1. 文件上传基础

### 小文件上传 (< 128 MB)
```python
from pathlib import Path
from PowerPlatform.Dataverse.client import DataverseClient

file_path = Path("document.pdf")
record_id = "account-guid"

# 单次 PATCH 上传用于小文件
response = client.upload_file(
    table_name="account",
    record_id=record_id,
    file_column_name="new_documentfile",
    file_path=file_path
)

print(f"上传成功: {response}")
```

**适用场景:** 小于 128 MB 的文档、图片、PDF 文件

### 大文件分块上传
```python
from pathlib import Path

file_path = Path("large_video.mp4")
record_id = "account-guid"

# SDK 会自动处理大文件的分块上传
response = client.upload_file(
    table_name="account",
    record_id=record_id,
    file_column_name="new_videofile",
    file_path=file_path,
    chunk_size=4 * 1024 * 1024  # 4 MB 分块
)

print("分块上传完成")
```

**适用场景:** 大于 128 MB 的视频、数据库、存档文件

### 带进度跟踪的上传
```python
import hashlib
from pathlib import Path

def calculate_file_hash(file_path):
    """计算文件的 SHA-256 哈希值。"""
    hash_obj = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def upload_with_tracking(client, table_name, record_id, column_name, file_path):
    """带验证跟踪的上传。"""
    file_path = Path(file_path)
    file_size = file_path.stat().st_size
    
    print(f"开始上传: {file_path.name} ({file_size / 1024 / 1024:.2f} MB)")
    
    # 上传前计算哈希值
    original_hash = calculate_file_hash(file_path)
    print(f"文件哈希值: {original_hash}")
    
    # 执行上传
    response = client.upload_file(
        table_name=table_name,
        record_id=record_id,
        file_column_name=column_name,
        file_path=file_path
    )
    
    print(f"✓ 上传完成")
    return response

# 使用示例
upload_with_tracking(client, "account", account_id, "new_documentfile", "report.pdf")
```

---

## 2. 上传策略与配置

### 自动分块策略选择
```python
def upload_file_smart(client, table_name, record_id, column_name, file_path):
    """带自动策略选择的上传。"""
    file_path = Path(file_path)
    file_size = file_path.stat().st_size
    max_single_patch = 128 * 1024 * 1024  # 128 MB
    
    if file_size <= max_single_patch:
        print(f"使用单次 PATCH（文件 < 128 MB）")
        chunk_size = None  # SDK 将使用单次请求
    else:
        print(f"使用分块上传（文件 > 128 MB）")
        chunk_size = 4 * 1024 * 1024  # 4 MB 分块
    
    response = client.upload_file(
        table_name=table_name,
        record_id=record_id,
        file_column_name=column_name,
        file_path=file_path,
        chunk_size=chunk_size
    )
    
    return response

# 使用示例
upload_file_smart(client, "account", account_id, "new_largemedifile", "video.mp4")
```

### 批量文件上传
```python
from pathlib import Path
from PowerPlatform.Dataverse.core.errors import HttpError

def batch_upload_files(client, table_name, record_id, files_dict):
    """
    将多个文件上传到同一记录的不同列。
    
    参数:
        table_name: 表名
        record_id: 记录 ID
        files_dict: {"column_name": "file_path", ...}
    
    返回:
        {"success": [...], "failed": [...]}
    """
    results = {"success": [], "failed": []}
    
    for column_name, file_path in files_dict.items():
        try:
            print(f"正在上传 {Path(file_path).name} 到 {column_name}...")
            response = client.upload_file(
                table_name=table_name,
                record_id=record_id,
                file_column_name=column_name,
                file_path=file_path
            )
            results["success"].append({
                "column": column_name,
                "file": Path(file_path).name,
                "response": response
            })
            print(f"  ✓ 上传成功")
        except HttpError as e:
            results["failed"].append({
                "column": column_name,
                "file": Path(file_path).name,
                "error": str(e)
            })
            print(f"  ❌ 上传失败: {e}")
    
    return results

# 使用示例
files = {
    "new_contractfile": "contract.pdf",
    "new_specfile": "specification.docx",
    "new_designfile": "design.png"
}
results = batch_upload_files(client, "account", account_id, files)
print(f"成功: {len(results['success'])}, 失败: {len(results['failed'])}")
```

### 恢复失败的上传
```python
from pathlib import Path
import time
from PowerPlatform.Dataverse.core.errors import HttpError

def upload_with_retry(client, table_name, record_id, column_name, file_path, max_retries=3):
    """带指数退避重试逻辑的上传。"""
    file_path = Path(file_path)
    
    for attempt in range(max_retries):
        try:
            print(f"第 {attempt + 1}/{max_retries} 次上传: {file_path.name}")
            response = client.upload_file(
                table_name=table_name,
                record_id=record_id,
                file_column_name=column_name,
                file_path=file_path,
                chunk_size=4 * 1024 * 1024
            )
            print(f"✓ 上传成功")
            return response
        except HttpError as e:
            if attempt == max_retries - 1:
                print(f"❌ 在 {max_retries} 次尝试后上传失败")
                raise
            
            # 指数退避: 1s, 2s, 4s
            backoff_seconds = 2 ** attempt
            print(f"⚠ 上传失败。将在 {backoff_seconds}s 后重试...")
            time.sleep(backoff_seconds)

# 使用示例
upload_with_retry(client, "account", account_id, "new_documentfile", "contract.pdf")
```

---

## 3. 实际应用示例

### 示例 1: 客户文档管理系统

```python
from pathlib import Path
from datetime import datetime
from enum import IntEnum
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import ClientSecretCredential

class DocumentType(IntEnum):
    CONTRACT = 1
    INVOICE = 2
    SPECIFICATION = 3
    OTHER = 4

# 初始化
credential = ClientSecretCredential(
    tenant_id="tenant-id",
    client_id="client-id",
    client_secret="client-secret"
)
client = DataverseClient("https://yourorg.crm.dynamics.com", credential)

def upload_customer_document(customer_id, doc_path, doc_type):
    """为客户上传文档。"""
    doc_path = Path(doc_path)
    
    # 创建文档记录
    doc_record = {
        "new_documentname": doc_path.stem,
        "new_documenttype": doc_type,
        "new_customerid": customer_id,
        "new_uploadeddate": datetime.now().isoformat(),
        "new_filesize": doc_path.stat().st_size
    }
    
    doc_ids = client.create("new_customerdocument", doc_record)
    doc_id = doc_ids[0]
    
    # 上传文件
    print(f"正在上传 {doc_path.name}...")
    client.upload_file(
        table_name="new_customerdocument",
        record_id=doc_id,
        file_column_name="new_documentfile",
        file_path=doc_path
    )
    
    print(f"✓ 文档上传并关联到客户")
    return doc_id

# 使用示例
customer_id = "customer-guid-here"
doc_id = upload_customer_document(
    customer_id,
    "contract.pdf",
    DocumentType.CONTRACT
)

# 查询已上传的文档
docs = client.get(
    "new_customerdocument",
    filter=f"new_customerid eq '{customer_id}'",
    select=["new_documentname", "new_documenttype", "new_uploadeddate"]
)

for page in docs:
    for doc in page:
        print(f"- {doc['new_documentname']} ({doc['new_uploadeddate']})")
```

### 示例 2: 带缩略图的媒体画廊

```python
from pathlib import Path
from enum import IntEnum
from PowerPlatform.Dataverse.client import DataverseClient

class MediaType(IntEnum):
    PHOTO = 1
    VIDEO = 2
    DOCUMENT = 3

def create_media_gallery(client, gallery_name, media_files):
    """
    创建带多个文件的媒体画廊。
    
    参数:
        gallery_name: 画廊名称
        media_files: [{"file": 路径, "type": MediaType, "description": 文本}, ...]
    """
    # 创建画廊记录
    gallery_ids = client.create("new_mediagallery", {
        "new_galleryname": gallery_name,
        "new_createddate": datetime.now().isoformat()
    })
    gallery_id = gallery_ids[0]
    
    # 创建并上传媒体项
    for media_info in media_files:
        file_path = Path(media_info["file"])
        
        # 创建媒体项记录
        item_ids = client.create("new_mediaitem", {
            "new_itemname": file_path.stem,
            "new_mediatype": media_info["type"],
            "new_description": media_info.get("description", ""),
            "new_galleryid": gallery_id,
            "new_filesize": file_path.stat().st_size
        })
        item_id = item_ids[0]
        
        # 上传媒体文件
        print(f"正在上传 {file_path.name}...")
        client.upload_file(
            table_name="new_mediaitem",
            record_id=item_id,
            file_column_name="new_mediafile",
            file_path=file_path
        )
        print(f"  ✓ {file_path.name}")
    
    return gallery_id

# 使用示例
media_files = [
    {"file": "photo1.jpg", "type": MediaType.PHOTO, "description": "产品照片 1"},
    {"file": "photo2.jpg", "type": MediaType.PHOTO, "description": "产品照片 2"},
    {"file": "demo.mp4", "type": MediaType.VIDEO, "description": "产品演示视频"},
    {"file": "manual.pdf", "type": MediaType.DOCUMENT, "description": "用户手册"}
]

gallery_id = create_media_gallery(client, "Q4 产品发布", media_files)
print(f"创建画廊: {gallery_id}")
```

### 示例 3: 备份与归档系统

```python
from pathlib import Path
from datetime import datetime, timedelta
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.errors import DataverseError
import json

def backup_table_data(client, table_name, output_dir):
    """
    将表数据备份到 JSON 文件并创建归档记录。
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    backup_time = datetime.now()
    backup_file = output_dir / f"{table_name}_{backup_time.strftime('%Y%m%d_%H%M%S')}.json"
    
    print(f"正在备份 {table_name}...")
    
    # 获取所有记录
    all_records = []
    for page in client.get(table_name, top=5000):
        all_records.extend(page)
    
    # 写入 JSON 文件
    with open(backup_file, 'w') as f:
        json.dump(all_records, f, indent=2, default=str)
    
    print(f"  ✓ 导出 {len(all_records)} 条记录")
    
    # 创建备份记录
    backup_ids = client.create("new_backuprecord", {
        "new_tablename": table_name,
        "new_recordcount": len(all_records),
        "new_backupdate": backup_time.isoformat(),
        "new_status": 1  # 已完成
    })
    backup_id = backup_ids[0]
    
    # 上传备份文件
    print(f"正在上传备份文件...")
    client.upload_file(
        table_name="new_backuprecord",
        record_id=backup_id,
        file_column_name="new_backupfile",
        file_path=backup_file
    )
    
    return backup_id

# 使用示例
backup_id = backup_table_data(client, "account", "backups")
print(f"备份已创建: {backup_id}")
```

### 示例 4: 自动报告生成与存储

```python
from pathlib import Path
from datetime import datetime
from enum import IntEnum
from PowerPlatform.Dataverse.client import DataverseClient
import json

class ReportStatus(IntEnum):
    PENDING = 1
    PROCESSING = 2
    COMPLETED = 3
    FAILED = 4

def generate_and_store_report(client, report_type, data):
    """
    从数据生成报告并存储到 Dataverse。
    """
    report_time = datetime.now()
    
    # 生成报告文件（模拟）
    report_file = Path(f"report_{report_type}_{report_time.strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # 创建报告记录
    report_ids = client.create("new_report", {
        "new_reportname": f"{report_type} 报告",
        "new_reporttype": report_type,
        "new_generateddate": report_time.isoformat(),
        "new_status": ReportStatus.PROCESSING,
        "new_recordcount": len(data.get("records", []))
    })
    report_id = report_ids[0]
    
    try:
        # 上传报告文件
        print(f"正在上传报告: {report_file.name}")
        client.upload_file(
            table_name="new_report",
            record_id=report_id,
            file_column_name="new_reportfile",
            file_path=report_file
        )
        
        # 更新状态为已完成
        client.update("new_report", report_id, {
            "new_status": ReportStatus.COMPLETED
        })
        
        print(f"✓ 报告存储成功")
        return report_id
        
    except Exception as e:
        print(f"❌ 报告生成失败: {e}")
        client.update("new_report", report_id, {
            "new_status": ReportStatus.FAILED,
            "new_errormessage": str(e)
        })
        raise
    finally:
        # 清理临时文件
        report_file.unlink(missing_ok=True)

# 使用示例
sales_data = {
    "month": "January",
    "records": [
        {"product": "A", "sales": 10000},
        {"product": "B", "sales": 15000},
        {"product": "C", "sales": 8000}
    ]
}

report_id = generate_and_store_report(client, "SALES_SUMMARY", sales_data)
```

---

## 4. 文件管理最佳实践

### 文件大小验证
```python
from pathlib import Path

def validate_file_for_upload(file_path, max_size_mb=500):
    """上传前验证文件。"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件未找到: {file_path}")
    
    file_size = file_path.stat().st_size
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if file_size > max_size_bytes:
        raise ValueError(f"文件过大: {file_size / 1024 / 1024:.2f} MB > {max_size_mb} MB")
    
    return file_size

# 使用示例
try:
    size = validate_file_for_upload("document.pdf", max_size_mb=128)
    print(f"文件有效: {size / 1024 / 1024:.2f} MB")
except (FileNotFoundError, ValueError) as e:
    print(f"验证失败: {e}")
```

### 支持的文件类型验证
```python
from pathlib import Path

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.xlsx', '.jpg', '.png', '.mp4', '.zip'}

def validate_file_type(file_path):
    """验证文件扩展名。"""
    file_path = Path(file_path)
    
    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(f"不支持的文件类型: {file_path.suffix}")
    
    return True

# 使用示例
try:
    validate_file_type("document.pdf")
    print("文件类型有效")
except ValueError as e:
    print(f"无效: {e}")
```

### 上传日志与审计追踪
```python
from pathlib import Path
from datetime import datetime
import json

def log_file_upload(table_name, record_id, file_path, status, error=None):
    """记录文件上传用于审计追踪。"""
    file_path = Path(file_path)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "表名": table_name,
        "记录ID": record_id,
        "文件名": file_path.name,
        "文件大小": file_path.stat().st_size if file_path.exists() else 0,
        "状态": status,
        "错误": error
    }
    
    # 追加到日志文件
    log_file = Path("upload_audit.log")
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return log_entry

# 在上传包装器中使用
def upload_with_logging(client, table_name, record_id, column_name, file_path):
    """带审计日志的上传。"""
    try:
        client.upload_file(
            table_name=table_name,
            record_id=record_id,
            file_column_name=column_name,
            file_path=file_path
        )
        log_file_upload(table_name, record_id, file_path, "SUCCESS")
    except Exception as e:
        log_file_upload(table_name, record_id, file_path, "FAILED", str(e))
        raise
```

---

## 5. 文件操作故障排除

### 常见问题与解决方案

#### 问题: 文件上传超时
```python
# 对于非常大的文件，战略性地增加分块大小
response = client.upload_file(
    table_name="account",
    record_id=record_id,
    file_column_name="new_file",
    file_path="large_file.zip",
    chunk_size=8 * 1024 * 1024  # 8 MB 分块
)
```

#### 问题: 磁盘空间不足
```python
import shutil
from pathlib import Path

def check_upload_space(file_path):
    """检查系统是否有空间存储文件及临时缓冲区。"""
    file_path = Path(file_path)
    file_size = file_path.stat().st_size
    
    # 获取磁盘空间
    total, used, free = shutil.disk_usage(file_path.parent)
    
    # 需要文件大小 + 10% 缓冲区
    required_space = file_size * 1.1
    
    if free < required_space:
        raise OSError(f"磁盘空间不足: {free / 1024 / 1024:.0f} MB 可用，{required_space / 1024 / 1024:.0f} MB 所需")
    
    return True
```

#### 问题: 上传过程中文件损坏
```python
import hashlib

def verify_uploaded_file(local_path, remote_data):
    """验证上传文件的完整性。"""
    # 计算本地哈希值
    with open(local_path, 'rb') as f:
        local_hash = hashlib.sha256(f.read()).hexdigest()
    
    # 与元数据比较
    remote_hash = remote_data.get("new_filehash")
    
    if local_hash != remote_hash:
        raise ValueError("检测到文件损坏: 哈希值不匹配")
    
    return True
```

---

## 参考
- [官方文件上传示例](https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/main/examples/advanced/file_upload.py)
- [文件上传最佳实践](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/file-column-data)
---
name: microsoft-code-reference
description: 查询微软API参考文档，查找可用的代码示例，并验证SDK代码是否正确。在使用Azure SDKs、.NET库或微软API时使用，以查找正确的方法、检查参数、获取可用示例或排查错误。通过查询官方文档来捕获虚构的方法、错误的签名和已弃用的模式。
compatibility: 需要微软学习MCP服务器（https://learn.microsoft.com/api/mcp）
---

# 微软代码参考

## 工具

| 需求 | 工具 | 示例 |
|------|------|---------|
| API方法/类查找 | `microsoft_docs_search` | `"BlobClient UploadAsync Azure.Storage.Blobs"` |
| 可用代码示例 | `microsoft_code_sample_search` | `query: "upload blob managed identity", language: "python"` |
| 完整API参考 | `microsoft_docs_fetch` | 从`microsoft_docs_search`获取URL（用于重载、完整签名） |

## 查找代码示例

使用`microsoft_code_sample_search`获取官方可用的示例代码：

```
microsoft_code_sample_search(query: "upload file to blob storage", language: "csharp")
microsoft_code_sample_search(query: "authenticate with managed identity", language: "python")
microsoft_code_sample_search(query: "send message service bus", language: "javascript")
```

**何时使用：**
- 编写代码前——查找可遵循的可用模式
- 出现错误后——将代码与已知正确的示例进行对比
- 不确定初始化/设置——示例展示了完整的上下文

## API查找

```
# 验证方法是否存在（包含命名空间以提高精确度）
"BlobClient UploadAsync Azure.Storage.Blobs"
"GraphServiceClient Users Microsoft.Graph"

# 查找类/接口
"DefaultAzureCredential class Azure.Identity"

# 查找正确的包
"Azure Blob Storage NuGet包"
"azure-storage-blob pip包"
```

当方法有多个重载或需要完整的参数细节时，获取完整页面。

## 错误排查

使用`microsoft_code_sample_search`查找可用代码示例并与您的实现进行对比。对于特定错误，使用`microsoft_docs_search`和`microsoft_docs_fetch`：

| 错误类型 | 查询 |
|------------|-------|
| 方法未找到 | `"[ClassName] methods [Namespace]"` |
| 类型未找到 | `"[TypeName] NuGet包命名空间"` |
| 签名错误 | `"[ClassName] [MethodName] 重载"` → 获取完整页面 |
| 已弃用警告 | `"[OldType] 迁移 v12"` |
| 认证失败 | `"DefaultAzureCredential 排错"` |
| 403禁止访问 | `"[ServiceName] RBAC权限"` |

## 验证时机

始终在以下情况下验证：
- 方法名称看起来“过于方便”（如`UploadFile`与实际`Upload`）
- 混合使用不同SDK版本（v11的`CloudBlobClient`与v12的`BlobServiceClient`）
- 包名称不符合规范（.NET的`Azure.*`，Python的`azure-*`）
- 首次使用某个API

## 验证流程

在使用微软SDK生成代码前，请确认其正确性：

1. **确认方法或包存在** — `microsoft_docs_search(query: "[ClassName] [MethodName] [Namespace]")`
2. **获取完整详情**（用于重载/复杂参数）— `microsoft_docs_fetch(url: "...")`
3. **查找可用示例** — `microsoft_code_sample_search(query: "[任务]", language: "[语言]")`

对于简单的查找，仅执行步骤1可能就足够。对于复杂的API使用，需完成所有三个步骤。

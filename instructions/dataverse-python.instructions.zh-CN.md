

---
applyTo: '**'
---
# Dataverse Python SDK 入门指南

- 安装 Dataverse Python SDK 及其前提条件。
- 为 Dataverse 租户、客户端 ID、密钥和资源 URL 配置环境变量。
- 使用 SDK 通过 OAuth 进行身份验证并执行 CRUD 操作。

## 安装准备
- Python 3.10+
- 建议：使用虚拟环境

## 安装
```bash
pip install dataverse-sdk
```

## 身份验证基础
- 使用 Azure AD 应用注册进行 OAuth 身份验证。
- 将密钥存储在 `.env` 文件中，并通过 `python-dotenv` 加载。

## 常见任务
- 查询表
- 创建/更新行
- 批量操作
- 处理分页和限流

## 小贴士
- 复用客户端；避免频繁重新认证。
- 对瞬时故障添加重试机制。
- 记录请求以进行故障排除。
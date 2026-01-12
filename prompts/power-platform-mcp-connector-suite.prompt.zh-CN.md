

---
description: 生成完整的 Power Platform 自定义连接器并集成 MCP 以用于 Copilot Studio - 包括模式生成、故障排除和验证
agent: agent
---

# Power Platform MCP 连接器套件

生成完整的 Power Platform 自定义连接器实现，并集成 Model Context Protocol 以用于 Microsoft Copilot Studio。

## Copilot Studio 中的 MCP 功能

**当前支持：**
- ✅ **工具**: LLM 可调用的函数（需用户批准）
- ✅ **资源**: 代理可读取的文件类数据（必须为工具输出）

**尚未支持：**
- ❌ **提示**: 预写模板（未来可能支持）

## 连接器生成

创建完整的 Power Platform 连接器，包含以下内容：

**核心文件：**
- `apiDefinition.swagger.json` 文件，包含 `x-ms-agentic-protocol: mcp-streamable-1.0`
- `apiProperties.json` 文件，包含连接器元数据和身份验证配置
- `script.csx` 文件，包含用于 MCP JSON-RPC 处理的自定义 C# 转换逻辑
- `readme.md` 文件，包含连接器文档

**MCP 集成：**
- 用于 JSON-RPC 2.0 通信的 POST `/mcp` 端点
- McpResponse 和 McpErrorResponse 模式定义
- Copilot Studio 约束条件合规性（无引用类型，单一类型）
- 资源作为工具输出集成（支持资源和工具；提示尚未支持）

## 模式验证与故障排除

**验证 Copilot Studio 合规性模式：**
- ✅ 工具输入/输出中无引用类型（`$ref`）
- ✅ 仅支持单一类型值（不支持 `["string", "number"]`）
- ✅ 原始类型：字符串、数字、整数、布尔值、数组、对象
- ✅ 资源作为工具输出，而非独立实体
- ✅ 所有端点使用完整 URI

**常见问题及解决方案：**
- 工具被过滤 → 移除引用类型，使用原始类型
- 类型错误 → 使用单一类型并添加验证逻辑
- 资源不可用 → 将其包含在工具输出中
- 连接失败 → 验证 `x-ms-agentic-protocol` 请求头

## 上下文变量

- **连接器名称**: [连接器的显示名称]
- **服务器用途**: [MCP 服务器应实现的功能]
- **所需工具**: [需要实现的 MCP 工具列表]
- **资源**: [需要提供的资源类型]
- **身份验证**: [无、API 密钥、OAuth 2.0、基本]
- **主机环境**: [Azure 函数、Express.js 等]
- **目标 API**: [需要集成的外部 API]

## 生成模式

### 模式 1：全新连接器生成
从零开始生成 Power Platform MCP 连接器的所有文件，包括 CLI 验证设置。

### 模式 2：模式验证
使用 paconn 和验证工具分析并修复现有模式以符合 Copilot Studio 的要求。

### 模式 3：集成故障排除
使用 CLI 调试工具诊断并解决 Copilot Studio 的 MCP 集成问题。

### 模式 4：混合连接器
在现有 Power Platform 连接器中添加 MCP 功能，并配置适当的验证流程。

### 模式 5：认证准备
准备连接器以满足 Microsoft 认证提交要求，包含完整的元数据和验证合规性。

### 模式 6：OAuth 安全加固
实现增强的 OAuth 2.0 身份验证，结合 MCP 安全最佳实践和高级令牌验证。

## 预期输出

**1. apiDefinition.swagger.json**
- Swagger 2.0 格式，包含 Microsoft 扩展
- MCP 端点：`POST /mcp`，包含正确的协议请求头
- 合规模式定义（仅原始类型）
- McpResponse/McpErrorResponse 模式定义

**2. apiProperties.json**
- 连接器元数据和品牌信息（`iconBrandColor` 为必填项）
- 身份验证配置
- 用于 MCP 转换的策略模板

**3. script.csx**
- JSON-RPC 2.0 消息处理
- 请求/响应转换
- MCP 协议合规性逻辑
- 错误处理和验证

**4. 实现指南**
- 工具注册和执行模式
- 资源管理策略
- Copilot Studio 集成步骤
- 测试和验证流程

## 验证清单

### 技术合规性
- [ ] MCP 端点包含 `x-ms-agentic-protocol: mcp-streamable-1.0`
- [ ] 任何模式定义中均无引用类型
- [ ] 所有类型字段均为单一类型（非数组）
- [ ] 资源作为工具输出包含
- [ ] script.csx 中 JSON-RPC 2.0 合规性
- [ ] 所有端点使用完整 URI
- [ ] Copilot Studio 代理的清晰描述
- [ ] 身份验证配置正确
- [ ] 用于 MCP 转换的策略模板
- [ ] 生成式编排兼容性

### CLI 验证
- [ ] **paconn validate**: `paconn validate --api-def apiDefinition.swagger.json` 无错误通过
- [ ] **pac CLI 就绪**: 使用 `pac connector create/update` 可创建/更新连接器
- [ ] **脚本验证**: script.csx 在 pac CLI 上传时通过自动验证
- [ ] **包验证**: `ConnectorPackageValidator.ps1` 脚本成功运行

### OAuth 和安全要求
- [ ] **增强的 OAuth 2.0**: 实现标准 OAuth 2.0 与 MCP 安全最佳实践
- [ ] **令牌验证**: 实现令牌受众验证以防止中间人攻击
- [ ] **自定义安全逻辑**: 在 script.csx 中增强验证以符合 MCP 要求
- [ ] **状态参数保护**: 为防止 CSRF 攻击的安全状态参数
- [ ] **HTTPS 强制**: 所有生产端点仅使用 HTTPS
- [ ] **MCP 安全实践**: 在 OAuth 2.0 中实现混淆代理攻击防护

### 认证要求
- [ ] **完整元数据**: 包含产品和服务信息的 `settings.json`
- [ ] **图标合规性**: PNG 格式，230x230 或 500x500 尺寸
- [ ] **文档**: 准备就绪的 `readme.md`，包含全面的示例
- [ ] **安全合规性**: 增强的 OAuth 2.0，结合 MCP 安全实践和隐私政策
- [ ] **身份验证流程**: 正确配置带有自定义安全验证的 OAuth 2.0

## 示例用法

```yaml
模式: 全新连接器生成
连接器名称: 客户分析 MCP
服务器用途: 客户数据分析和洞察
所需工具:
  - searchCustomers: 根据条件查找客户
  - getCustomerProfile: 获取详细客户数据
  - analyzeCustomerTrends: 生成趋势分析
资源:
  - 客户档案（JSON 数据）
  - 分析报告（结构化数据）
身份验证: OAuth 2.0
主机环境: Azure 函数
目标 API: CRM REST API
```
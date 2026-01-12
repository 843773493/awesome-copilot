

---
描述：生成一个适用于 Copilot Studio 集成的完整 MCP 服务器实现，包含正确的模式约束和流式 HTTP 支持
代理：代理
---

# Power Platform MCP 连接器生成器

生成一个与 Microsoft Copilot Studio 集成的完整 Power Platform 自定义连接器，遵循 Power Platform 连接器标准，并支持 MCP 流式 HTTP。

## 指示

创建一个完整的 MCP 服务器实现，需满足以下要求：

1. **使用 Copilot Studio MCP 模式：**
   - 实现 `x-ms-agentic-protocol: mcp-streamable-1.0`
   - 支持 JSON-RPC 2.0 通信协议
   - 在 `/mcp` 提供流式 HTTP 端点
   - 遵循 Power Platform 连接器结构

2. **模式合规性要求：**
   - **工具输入/输出中不使用引用类型**（由 Copilot Studio 过滤）
   - **仅允许单一类型值**（不支持多种类型的数组）
   - **避免使用枚举输入**（解释为字符串，而非枚举）
   - 使用原始类型：string、number、integer、boolean、array、object
   - 确保所有端点返回完整 URI

3. **需包含的 MCP 组件：**
   - **工具**：语言模型可调用的功能（✅ 支持 Copilot Studio）
   - **资源**：工具生成的文件类数据输出（✅ 支持 Copilot Studio - 必须为工具输出才能被访问）
   - **提示**：特定任务的预定义模板（❌ Copilot Studio 目前不支持）

4. **实现结构：**
   ```
   /apiDefinition.swagger.json  (Power Platform 连接器模式)
   /apiProperties.json         (连接器元数据和配置)
   /script.csx                 (自定义代码转换和逻辑)
   /server/                    (MCP 服务器实现)
   /tools/                     (单个 MCP 工具)
   /resources/                 (MCP 资源处理程序)
   ```

## 上下文变量

- **服务器用途**：[描述 MCP 服务器应实现的功能]
- **所需工具**：[需要实现的具体工具列表]  
- **资源**：[需提供的资源类型]
- **认证方式**：[认证方法：无、API 密钥、OAuth2]
- **主机环境**：[Azure 函数、Express.js、FastAPI 等]
- **目标 API**：[需集成的外部 API]

## 预期输出

生成以下内容：

1. **apiDefinition.swagger.json**，包含：
   - 正确的 `x-ms-agentic-protocol: mcp-streamable-1.0`
   - MCP 端点（POST 请求 `/mcp`）
   - 合规的模式定义（无引用类型）
   - McpResponse 和 McpErrorResponse 定义

2. **apiProperties.json**，包含：
   - 连接器元数据和品牌信息
   - 认证配置
   - 如有需要，包含策略模板

3. **script.csx**，包含：
   - 自定义 C# 代码用于请求/响应转换
   - MCP JSON-RPC 消息处理逻辑
   - 数据验证和处理函数
   - 错误处理和日志记录功能

4. **MCP 服务器代码**，包含：
   - JSON-RPC 2.0 请求处理程序
   - 工具注册和执行
   - 资源管理（作为工具输出）
   - 正确的错误处理
   - Copilot Studio 兼容性检查

5. **单个工具**，需满足：
   - 仅接受原始类型输入
   - 返回结构化输出
   - 在需要时将资源作为输出包含
   - 为 Copilot Studio 提供清晰的描述

6. **部署配置**，用于：
   - Power Platform 环境
   - Copilot Studio 代理集成
   - 测试和验证

## 验证检查清单

确保生成的代码：
- [ ] 模式中无引用类型
- [ ] 所有类型字段均为单一类型
- [ ] 枚举处理通过字符串实现并进行验证
- [ ] 资源可通过工具输出访问
- [ ] 端点返回完整 URI
- [ ] 符合 JSON-RPC 2.0 标准
- [ ] 正确的 `x-ms-agentic-protocol` 头部
- [ ] McpResponse/McpErrorResponse 模式定义
- [ ] 为 Copilot Studio 提供清晰的工具描述
- [ ] 与生成性编排兼容

## 示例用法

```yaml
服务器用途: 客户数据管理和分析
所需工具: 
  - searchCustomers
  - getCustomerDetails
  - analyzeCustomerTrends
资源:
  - 客户档案
  - 分析报告
认证方式: OAuth2
主机环境: Azure 函数
目标 API: CRM 系统 REST API
```


````prompt
---
模式: '代理'
工具: ['changes', 'search/codebase', 'edit/editFiles', 'problems']
描述: '通过集成具有身份验证、工具选择和配置的MCP服务器，创建适用于Microsoft 365 Copilot的声明式代理'
模型: 'gpt-4.1'
标签: [mcp, m365-copilot, 声明式代理, 模型上下文协议, api-plugin]
---

# 创建基于MCP的Microsoft 365 Copilot声明式代理

创建一个完整的Microsoft 365 Copilot声明式代理，通过集成模型上下文协议（MCP）服务器来访问外部系统和数据。

## 要求

使用Microsoft 365代理工具包生成以下项目结构：

### 项目设置
1. **通过Agents Toolkit生成声明式代理框架**
2. **添加指向MCP服务器的MCP操作**
3. **选择要从MCP服务器导入的工具**
4. **配置身份验证**（OAuth 2.0或SSO）
5. **审查生成的文件**（manifest.json、ai-plugin.json、declarativeAgent.json）

### 生成的关键文件

**appPackage/manifest.json** - Teams应用清单，包含插件引用：
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/teams/vDevPreview/MicrosoftTeams.schema.json",
  "manifestVersion": "devPreview",
  "version": "1.0.0",
  "id": "...",
  "developer": {
    "name": "...",
    "websiteUrl": "...",
    "privacyUrl": "...",
    "termsOfUseUrl": "..."
  },
  "name": {
    "short": "代理名称",
    "full": "完整代理名称"
  },
  "description": {
    "short": "简要描述",
    "full": "完整描述"
  },
  "copilotAgents": {
    "declarativeAgents": [
      {
        "id": "declarativeAgent",
        "file": "declarativeAgent.json"
      }
    ]
  }
}
```

**appPackage/declarativeAgent.json** - 代理定义：
```json
{
  "$schema": "https://aka.ms/json-schemas/copilot/declarative-agent/v1.0/schema.json",
  "version": "v1.0",
  "name": "代理名称",
  "description": "代理描述",
  "instructions": "你是一个帮助[特定领域]的助手。使用可用工具[功能]。",
  "capabilities": [
    {
      "name": "WebSearch",
      "websites": [
        {
          "url": "https://learn.microsoft.com"
        }
      ]
    },
    {
      "name": "MCP",
      "file": "ai-plugin.json"
    }
  ]
}
```

**appPackage/ai-plugin.json** - MCP插件清单：
```json
{
  "schema_version": "v2.1",
  "name_for_human": "服务名称",
  "description_for_human": "用户描述",
  "description_for_model": "AI模型描述",
  "contact_email": "support@company.com",
  "namespace": "serviceName",
  "capabilities": {
    "conversation_starters": [
      {
        "text": "示例查询1"
      }
    ]
  },
  "functions": [
    {
      "name": "functionName",
      "description": "功能描述",
      "capabilities": {
        "response_semantics": {
          "data_path": "$",
          "properties": {
            "title": "$.title",
            "subtitle": "$.description"
          }
        }
      }
    }
  ],
  "runtimes": [
    {
      "type": "MCP",
      "spec": {
        "url": "https://api.service.com/mcp/"
      },
      "run_for_functions": ["functionName"],
      "auth": {
        "type": "OAuthPluginVault",
        "reference_id": "${{OAUTH_REFERENCE_ID}}"
      }
    }
  ]
}
```

**/.vscode/mcp.json** - MCP服务器配置：
```json
{
  "serverUrl": "https://api.service.com/mcp/",
  "pluginFilePath": "appPackage/ai-plugin.json"
}
```

## MCP服务器集成

### 支持的MCP端点
MCP服务器必须提供以下端点：
- **服务器元数据端点**
- **工具列表端点**（暴露可用功能）
- **工具执行端点**（处理功能调用）

### 工具选择
从MCP导入时：
1. 从服务器获取可用工具
2. 选择需要包含的特定工具（用于安全性和简化）
3. 工具定义会自动在ai-plugin.json中生成

### 身份验证类型

**OAuth 2.0（静态注册）**
```json
"auth": {
  "type": "OAuthPluginVault",
  "reference_id": "${{OAUTH_REFERENCE_ID}}",
  "authorization_url": "https://auth.service.com/authorize",
  "client_id": "${{CLIENT_ID}}",
  "client_secret": "${{CLIENT_SECRET}}",
  "scope": "read write"
}
```

**单点登录（SSO）**
```json
"auth": {
  "type": "SSO"
}
```

## 响应语义

### 定义数据映射
使用`response_semantics`从API响应中提取相关字段：

```json
"capabilities": {
  "response_semantics": {
    "data_path": "$.results",
    "properties": {
      "title": "$.name",
      "subtitle": "$.description",
      "url": "$.link"
    }
  }
}
```

### 添加自适应卡片（可选）
参见`mcp-create-adaptive-cards`提示以添加视觉卡片模板。

## 环境配置

创建`.env.local`或`.env.dev`文件用于凭证：

```env
OAUTH_REFERENCE_ID=your-oauth-reference-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
```

## 测试与部署

### 本地测试
1. **在Agents Toolkit中配置代理**
2. **启动调试**以在Teams中加载
3. 在Microsoft 365 Copilot中测试：https://m365.cloud.microsoft/chat
4. 在提示时进行身份验证
5. 使用自然语言查询代理

### 验证
- 验证ai-plugin.json中的工具导入
- 检查身份验证配置
- 测试每个暴露的功能
- 验证响应数据映射

## 最佳实践

### 工具设计
- **专注功能**：每个工具应专注于单一功能
- **清晰描述**：帮助模型理解何时使用每个工具
- **最小范围**：仅导入代理所需的工具
- **描述性名称**：使用以动作为导向的功能名称

### 安全性
- **生产环境使用OAuth 2.0**
- **在环境变量中存储密钥**
- **在MCP服务器端验证输入**
- **限制到最小必要权限**
- **使用参考ID进行OAuth注册**

### 指令
- **明确代理的目的和功能**
- **定义成功和错误场景的行为**
- **在适用时在指令中显式引用工具**
- **设定用户对代理能力的期望**

### 性能
- **在MCP服务器上适当缓存响应**
- **尽可能批量操作**
- **为长时间操作设置超时**
- **对大型数据集进行分页**

## 常见MCP服务器示例

### GitHub MCP服务器
```
URL: https://api.githubcopilot.com/mcp/
工具: 搜索仓库、搜索用户、获取仓库
身份验证: OAuth 2.0
```

### Jira MCP服务器
```
URL: https://your-domain.atlassian.net/mcp/
工具: 搜索问题、创建问题、更新问题
身份验证: OAuth 2.0
```

### 自定义服务
```
URL: https://api.your-service.com/mcp/
工具: 由您的服务暴露的自定义工具
身份验证: OAuth 2.0或SSO
```

## 工作流程

询问用户：
1. 你正在集成哪个MCP服务器（URL）？
2. 应该向Copilot暴露哪些工具？
3. 服务器支持哪种身份验证方法？
4. 代理的主要用途是什么？
5. 是否需要响应语义或自适应卡片？

然后生成：
- 完整的appPackage/结构（manifest.json、declarativeAgent.json、ai-plugin.json）
- mcp.json配置
- .env.local模板
- 配置和测试说明

## 常见问题排查

### MCP服务器无响应
- 确认服务器URL是否正确
- 检查网络连接
- 验证MCP服务器是否实现了所需端点

### 身份验证失败
- 确认OAuth凭证是否正确
- 检查参考ID是否匹配注册
- 确认是否正确请求了作用域
- 独立测试OAuth流程

### 工具未显示
- 确保mcp.json指向正确的服务器
- 验证导入时是否选择了工具
- 检查ai-plugin.json中的功能定义是否正确
- 如果服务器更改，重新获取操作

### 代理无法理解查询
- 审查declarativeAgent.json中的指令
- 检查功能描述是否清晰
- 验证response_semantics是否提取了正确数据
- 使用更具体的查询进行测试
````


---
description: '构建基于 TypeSpec 的声明式代理和 Microsoft 365 Copilot API 插件的指南和最佳实践'
applyTo: '**/*.tsp'
---

# TypeSpec 用于 Microsoft 365 Copilot 开发指南

## 核心原则

在使用 TypeSpec 进行 Microsoft 365 Copilot 开发时：

1. **类型安全优先**：为所有模型和操作利用 TypeSpec 的强类型特性
2. **声明式方法**：使用装饰器描述意图，而非实现细节
3. **作用域能力**：在可能的情况下，始终将能力作用域限定到特定资源
4. **清晰指令**：编写明确、详细的代理指令
5. **以用户为中心**：为 Microsoft 365 Copilot 的最终用户体验进行设计

## 文件组织

### 标准结构
```
project/
├── appPackage/
│   ├── cards/              # Adaptive Card 模板
│   │   └── *.json
│   ├── .generated/         # 生成的清单文件（自动生成）
│   └── manifest.json       # Teams 应用清单
├── src/
│   ├── main.tsp           # 代理定义
│   └── actions.tsp        # API 操作（用于插件）
├── m365agents.yml         # Agents 工具包配置
└── package.json
```

### 导入语句
始终在 TypeSpec 文件顶部包含所需的导入：

```typescript
import "@typespec/http";
import "@typespec/openapi3";
import "@microsoft/typespec-m365-copilot";

using TypeSpec.Http;
using TypeSpec.M365.Copilot.Agents;  // 用于代理
using TypeSpec.M365.Copilot.Actions; // 用于 API 插件
```

## 代理开发最佳实践

### 代理声明
```typescript
@agent({
  name: "基于角色的名称",  // 例如："客户支持助手"
  description: "简洁明了的描述，不超过 1,000 个字符"
})
```

- 使用基于角色的名称来描述代理的功能
- 描述应信息丰富但简洁
- 避免使用通用名称如 "Helper" 或 "Bot"

### 指令
```typescript
@instructions("""
  你是一个 [特定角色]，专门负责 [领域]。
  
  你的职责包括：
  - [关键职责 1]
  - [关键职责 2]
  
  在帮助用户时：
  - [行为指南 1]
  - [行为指南 2]
  
  你不应：
  - [约束 1]
  - [约束 2]
""")
```

- 使用第二人称（"You are..."）编写
- 明确说明代理的角色和专长
- 定义代理应做什么以及不应做什么
- 保持在 8,000 个字符以内
- 使用清晰、结构化的格式

### 对话启动器
```typescript
@conversationStarter(#{
  title: "以行动为导向的标题",  // 例如："检查状态"
  text: "具体的查询示例"   // 例如："我的工单状态如何？"
})
```

- 提供 2-4 个多样化的启动器
- 每个展示不同的能力
- 使用以行动为导向的标题
- 编写现实的查询示例

### 能力 - 知识源

**网络搜索** - 在可能的情况下限定到特定网站：
```typescript
op webSearch is AgentCapabilities.WebSearch<Sites = [
  { url: "https://learn.microsoft.com" },
  { url: "https://docs.microsoft.com" }
]>;
```

**OneDrive 和 SharePoint** - 使用 URL 或 ID：
```typescript
op oneDriveAndSharePoint is AgentCapabilities.OneDriveAndSharePoint<
  ItemsByUrl = [
    { url: "https://contoso.sharepoint.com/sites/Engineering" }
  ]
>;
```

**Teams 消息** - 指定频道/聊天：
```typescript
op teamsMessages is AgentCapabilities.TeamsMessages<Urls = [
  { url: "https://teams.microsoft.com/l/channel/..." }
]>;
```

**电子邮件** - 限定到特定文件夹：
```typescript
op email is AgentCapabilities.Email<
  Folders = [
    { folderId: "Inbox" },
    { folderId: "SentItems" }
  ],
  SharedMailbox = "support@contoso.com"  // 可选
>;
```

**人员** - 不需要限定：
```typescript
op people is AgentCapabilities.People;
```

**Copilot 连接器** - 指定连接 ID：
```typescript
op copilotConnectors is AgentCapabilities.GraphConnectors<
  Connections = [
    { connectionId: "your-connector-id" }
  ]
>;
```

**Dataverse** - 限定到特定表：
```typescript
op dataverse is AgentCapabilities.Dataverse<
  KnowledgeSources = [
    {
      hostName: "contoso.crm.dynamics.com";
      tables: [
        { tableName: "account" },
        { tableName: "contact" }
      ];
    }
  ]
>;
```

### 能力 - 生产力工具

```typescript
// Python 代码执行
op codeInterpreter is AgentCapabilities.CodeInterpreter;

// 图像生成
op graphicArt is AgentCapabilities.GraphicArt;

// 会议内容访问
op meetings is AgentCapabilities.Meetings;

// 专用 AI 模型
op scenarioModels is AgentCapabilities.ScenarioModels<
  ModelsById = [
    { id: "model-id" }
  ]
>;
```

## API 插件开发最佳实践

### 服务定义
```typescript
@service
@actions(#{
  nameForHuman: "用户友好的 API 名称",
  descriptionForHuman: "用户能理解的描述",
  descriptionForModel: "模型需要知道的描述",
  contactEmail: "support@company.com",
  privacyPolicyUrl: "https://company.com/privacy",
  legalInfoUrl: "https://company.com/terms"
})
@server("https://api.example.com", "API 名称")
@useAuth([AuthType])  // 如果需要认证
namespace APINamespace {
  // 操作在此处
}
```

### 操作定义
```typescript
@route("/resource/{id}")
@get
@action
@card(#{
  dataPath: "$.items",
  title: "$.title",
  file: "cards/card.json"
})
@capabilities(#{
  confirmation: #{
    type: "AdaptiveCard",
    title: "确认操作",
    body: "请确认 {{ function.parameters.param }}"
  }
})
@reasoning("考虑 X 当 Y")
@responding("将结果呈现为 Z")
op getResource(
  @path id: string,
  @query filter?: string
): ResourceResponse;
```

### 模型
```typescript
model Resource {
  id: string;
  name: string;
  description?: string;  // 可选字段
  status: "active" | "inactive";  // 枚举的联合类型
  @format("date-time")
  createdAt: utcDateTime;
  @format("uri")
  url?: string;
}

model ResourceList {
  items: Resource[];
  totalCount: int32;
  nextPage?: string;
}
```

### 认证

**API 密钥**
```typescript
@useAuth(ApiKeyAuth<ApiKeyLocation.header, "X-API-Key">)

// 或使用引用 ID
@useAuth(Auth)
@authReferenceId("${{ENV_VAR_REFERENCE_ID}}")
model Auth is ApiKeyAuth<ApiKeyLocation.header, "X-API-Key">;
```

**OAuth2**
```typescript
@useAuth(OAuth2Auth<[{
  type: OAuth2FlowType.authorizationCode;
  authorizationUrl: "https://auth.example.com/authorize";
  tokenUrl: "https://auth.example.com/token";
  refreshUrl: "https://auth.example.com/refresh";
  scopes: ["read", "write"];
}]>)

// 或使用引用 ID
@useAuth(Auth)
@authReferenceId("${{OAUTH_REFERENCE_ID}}")
model Auth is OAuth2Auth<[...]>;
```

## 命名规范

### 文件
- `main.tsp` - 代理定义
- `actions.tsp` - API 操作
- `[功能].tsp` - 额外功能文件
- `cards/*.json` - Adaptive Card 模板

### TypeSpec 元素
- **命名空间**：PascalCase（例如：`CustomerSupportAgent`）
- **操作**：camelCase（例如：`listProjects`, `createTicket`）
- **模型**：PascalCase（例如：`Project`, `TicketResponse`）
- **模型属性**：camelCase（例如：`projectId`, `createdDate`）

## 常见模式

### 多能力代理
```typescript
@agent("知识工作者", "描述")
@instructions("...")
namespace KnowledgeWorker {
  op webSearch is AgentCapabilities.WebSearch;
  op files is AgentCapabilities.OneDriveAndSharePoint;
  op people is AgentCapabilities.People;
}
```

### CRUD API 插件
```typescript
namespace ProjectAPI {
  @route("/projects") @get @action
  op list(): Project[];
  
  @route("/projects/{id}") @get @action
  op get(@path id: string): Project;
  
  @route("/projects") @post @action
  @capabilities(#{confirmation: ...})
  op create(@body project: CreateProject): Project;
  
  @route("/projects/{id}") @patch @action
  @capabilities(#{confirmation: ...})
  op update(@path id: string, @body project: UpdateProject): Project;
  
  @route("/projects/{id}") @delete @action
  @capabilities(#{confirmation: ...})
  op delete(@path id: string): void;
}
```

### Adaptive Card 数据绑定
```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5",
  "body": [
    {
      "type": "Container",
      "$data": "${$root}",
      "items": [
        {
          "type": "TextBlock",
          "text": "标题: ${if(title, title, 'N/A')}",
          "wrap": true
        }
      ]
    }
  ]
}
```

## 验证与测试

### 部署前
1. 运行 TypeSpec 验证：`npm run build` 或使用 Agents 工具包
2. 检查所有 `@card` 装饰器中的文件路径是否存在
3. 验证认证引用是否与配置匹配
4. 确保能力作用域适当
5. 审核指令的清晰度和长度

### 测试策略
1. **部署**：部署到开发环境
2. **测试**：使用 Microsoft 365 Copilot 在 https://m365.cloud.microsoft/chat 进行测试
3. **调试**：启用 Copilot 开发者模式以获取 orchestrator 洞察
4. **迭代**：根据实际行为进行优化
5. **验证**：测试所有对话启动器和能力

## 性能优化

1. **作用域能力**：如果只需要子集数据，不要授予全部访问权限
2. **限制操作**：仅暴露代理实际使用的 API 操作
3. **高效模型**：保持响应模型专注于必要数据
4. **卡片优化**：在 Adaptive Cards 中使用条件渲染（`$when`）
5. **缓存**：为 API 设计适当的缓存头

## 安全最佳实践

1. **认证**：始终为非公开 API 使用认证
2. **作用域**：将能力访问限制到最小必要资源
3. **验证**：验证所有 API 操作的输入
4. **敏感数据**：使用环境变量存储敏感数据
5. **引用**：在生产环境中使用 `@authReferenceId` 引用凭证
6. **权限**：请求最小必要的 OAuth 权限范围

## 错误处理

```typescript
model ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: ErrorDetail[];
  };
}

model ErrorDetail {
  field?: string;
  message: string;
}
```

## 文档

在 TypeSpec 中为复杂操作添加注释：

```typescript
/**
 * 获取包含相关任务和团队成员的项目详细信息。
 * 
 * @param id - 项目的唯一标识符
 * @param includeArchived - 是否包含归档任务
 * @returns 完整的项目信息
 */
@route("/projects/{id}")
@get
@action
op getProjectDetails(
  @path id: string,
  @query includeArchived?: boolean
): ProjectDetails;
```

## 常见误区避免

1. ❌ 通用代理名称（"Helper Bot"）
2. ❌ 模糊的指令（"帮助用户做各种事情"）
3. ❌ 无能力作用域（访问所有数据）
4. ❌ 对破坏性操作缺少确认
5. ❌ 过于复杂的 Adaptive Cards
6. ❌ 在 TypeSpec 文件中硬编码凭证
7. ❌ 缺少错误响应模型
8. ❌ 命名规范不一致
9. ❌ 能力过多（仅使用所需能力）
10. ❌ 指令超过 8,000 个字符

## 资源

- [TypeSpec 官方文档](https://typespec.io/)
- [Microsoft 365 Copilot 可扩展性](https://learn.microsoft.com/microsoft-365-copilot/extensibility/)
- [Agents 工具包](https://aka.ms/M365AgentsToolkit)
- [Adaptive Cards 设计器](https://adaptivecards.io/designer/)


# Microsoft 365 Copilot 的 TypeSpec

## 概述

Microsoft 365 Copilot 的 TypeSpec 是一种强大的领域特定语言（DSL），它允许开发者使用干净且表达力强的语法创建声明式代理和 API 插件。基于 [TypeSpec](https://typespec.io/) 构建，这种专用语言提供了 Microsoft 365 特定的装饰器和功能，从而简化了扩展 Microsoft 365 Copilot 的开发流程。

## 为什么使用 TypeSpec？

- **类型安全**：对所有 Microsoft 365 Copilot 特定构造进行全面的类型检查
- **开发者体验**：在 Visual Studio Code 中提供丰富的 IntelliSense 支持和实时反馈
- **简化编写**：用直观的装饰器语法替代冗长的 JSON 配置
- **自动清单生成**：自动生成功能清单文件和 OpenAPI 规范
- **可维护性**：与手动编写 JSON 相比，代码库更易读且更易于维护

## 核心概念

### 声明式代理

声明式代理是 Microsoft 365 Copilot 的定制版本，允许用户通过声明特定的指令、操作和知识来创建个性化的体验。

**基本代理示例：**
```typescript
@agent(
  "客户支持助手",
  "一个帮助处理客户支持查询和工单管理的 AI 代理"
)
@instructions("""
  你是客户支持专家。帮助用户解决他们的咨询，
  提供故障排除步骤，并在必要时升级复杂问题。
  始终保持有帮助且专业的语气。
""")
@conversationStarter(#{
  title: "检查工单状态",
  text: "我的支持工单状态如何？"
})
namespace CustomerSupportAgent {
  // 在此处定义代理功能
}
```

### API 插件

API 插件通过自定义 API 操作扩展 Microsoft 365 Copilot，从而实现与外部服务和数据源的集成。

**基本 API 插件示例：**
```typescript
import "@typespec/http";
import "@microsoft/typespec-m365-copilot";

using TypeSpec.Http;
using Microsoft.M365Copilot;

@service
@server("https://api.contoso.com")
@actions(#{
  nameForHuman: "项目管理 API",
  descriptionForHuman: "管理项目和任务",
  descriptionForModel: "用于创建、更新和跟踪项目任务的 API"
})
namespace ProjectAPI {
  model Project {
    id: string;
    name: string;
    description?: string;
    status: "active" | "completed" | "on-hold";
    createdDate: utcDateTime;
  }

  @route("/projects")
  @get op listProjects(): Project[];

  @route("/projects/{id}")
  @get op getProject(@path id: string): Project;

  @route("/projects")
  @post op createProject(@body project: CreateProjectRequest): Project;
}
```

## 关键装饰器

### 代理装饰器

- **@agent**：使用名称、描述和可选 ID 定义代理
- **@instructions**：定义代理的行为指令和指南
- **@conversationStarter**：定义用户对话的起始提示
- **@behaviorOverrides**：修改代理编排行为设置
- **@disclaimer**：向用户显示法律或合规免责声明
- **@customExtension**：添加自定义键值对以实现扩展性

### API 插件装饰器

- **@actions**：定义操作元数据，包括名称、描述和 URL
- **@authReferenceId**：指定 API 访问的认证参考 ID
- **@capabilities**：配置功能能力，如确认和响应格式
- **@card**：定义用于功能响应的自适应卡片模板
- **@reasoning**：为功能调用提供推理指令
- **@responding**：定义功能的响应格式指令

## 代理功能

TypeSpec 提供了访问 Microsoft 365 服务和外部资源的内置功能：

### 知识源

**网络搜索**
```typescript
op webSearch is AgentCapabilities.WebSearch<Sites = [
  {
    url: "https://learn.microsoft.com"
  }
]>;
```

**OneDrive 和 SharePoint**
```typescript
op oneDriveAndSharePoint is AgentCapabilities.OneDriveAndSharePoint<
  ItemsByUrl = [
    { url: "https://contoso.sharepoint.com/sites/ProductSupport" }
  ]
>;
```

**Teams 消息**
```typescript
op teamsMessages is AgentCapabilities.TeamsMessages<Urls = [
  {
    url: "https://teams.microsoft.com/l/team/...",
  }
]>;
```

**电子邮件**
```typescript
op email is AgentCapabilities.Email<Folders = [
  {
    folderId: "Inbox",
  }
]>;
```

**人员**
```typescript
op people is AgentCapabilities.People;
```

**Copilot 连接器**
```typescript
op copilotConnectors is AgentCapabilities.GraphConnectors<Connections = [
  {
    connectionId: "policieslocal",
  }
]>;
```

**Dataverse**
```typescript
op dataverse is AgentCapabilities.Dataverse<KnowledgeSources = [
  {
    hostName: "contoso.crm.dynamics.com";
    tables: [
      { tableName: "account" },
      { tableName: "contact" }
    ];
  }
]>;
```

### 生产力工具

**代码解释器**
```typescript
op codeInterpreter is AgentCapabilities.CodeInterpreter;
```

**图像生成器**
```typescript
op graphicArt is AgentCapabilities.GraphicArt;
```

**会议**
```typescript
op meetings is AgentCapabilities.Meetings;
```

**场景模型**
```typescript
op scenarioModels is AgentCapabilities.ScenarioModels<ModelsById = [
  { id: "financial-forecasting-model-v3" }
]>;
```

## 认证

TypeSpec 支持多种认证方法以确保 API 插件的安全性：

### 无认证（匿名）
```typescript
@service
@actions(ACTIONS_METADATA)
@server(SERVER_URL, API_NAME)
namespace API {
  // 端点
}
```

### API 密钥认证
```typescript
@service
@actions(ACTIONS_METADATA)
@server(SERVER_URL, API_NAME)
@useAuth(ApiKeyAuth<ApiKeyLocation.header, "X-Your-Key">)
namespace API {
  // 端点
}
```

### OAuth2 授权码流程
```typescript
@service
@actions(ACTIONS_METADATA)
@server(SERVER_URL, API_NAME)
@useAuth(OAuth2Auth<[{ 
  type: OAuth2FlowType.authorizationCode;
  authorizationUrl: "https://contoso.com/oauth2/v2.0/authorize";
  tokenUrl: "https://contoso.com/oauth2/v2.0/token";
  refreshUrl: "https://contoso.com/oauth2/v2.0/token";
  scopes: ["scope-1", "scope-2"];
}]>)
namespace API {
  // 端点
}
```

### 使用注册认证
```typescript
@authReferenceId("NzFmOTg4YmYtODZmMS00MWFmLTkxYWItMmQ3Y2QwMTFkYjQ3IyM5NzQ5Njc3Yi04NDk2LTRlODYtOTdmZS1kNDUzODllZjUxYjM=")
model Auth is OAuth2Auth<[{ 
  type: OAuth2FlowType.authorizationCode;
  authorizationUrl: "https://contoso.com/oauth2/v2.0/authorize";
  tokenUrl: "https://contoso.com/oauth2/v2.0/token";
  refreshUrl: "https://contoso.com/oauth2/v2.0/token";
  scopes: ["scope-1", "scope-2"];
}]>
```

## 常见场景

### 多功能知识工作者代理
```typescript
import "@typespec/http";
import "@typespec/openapi3";
import "@microsoft/typespec-m365-copilot";

using TypeSpec.Http;
using TypeSpec.M365.Copilot.Agents;

@agent({
  name: "知识工作者助手",
  description: "一个帮助研究人员进行研究、文件管理和寻找同事的智能助手"
})
@instructions("""
  你是专门帮助知识工作者高效获取信息的知识型研究助手。
  你可以通过网络搜索外部研究资料，访问 SharePoint 文档获取组织内容，
  并帮助在组织内定位同事。
""")
namespace KnowledgeWorkerAgent {
  op webSearch is AgentCapabilities.WebSearch<Sites = [
    {
      url: "https://learn.microsoft.com";
    }
  ]>;

  op oneDriveAndSharePoint is AgentCapabilities.OneDriveAndSharePoint<
    ItemsByUrl = [
      { url: "https://contoso.sharepoint.com/sites/IT" }
    ]
  >;

  op people is AgentCapabilities.People;
}
```

### 带认证的 API 插件
```typescript
import "@typespec/http";
import "@microsoft/typespec-m365-copilot";

using TypeSpec.Http;
using TypeSpec.M365.Copilot.Actions;

@service
@actions(#{
    nameForHuman: "维修中心 API",
    descriptionForModel: "全面的维修管理系统",
    descriptionForHuman: "管理设施维修并跟踪分配"
})
@server("https://repairshub-apikey.contoso.com", "维修中心 API")
@useAuth(RepairsHubApiKeyAuth)
namespace RepairsHub {
  @route("/repairs")
  @get
  @action
  @card(#{
    dataPath: "$",
    title: "$.title",
    url: "$.image",
    file: "cards/card.json"
  })
  op listRepairs(
    @query assignedTo?: string
  ): string;

  @route("/repairs")
  @post
  @action
  @capabilities(#{
    confirmation: #{
      type: "AdaptiveCard",
      title: "创建新的维修",
      body: """
      正在使用以下详细信息创建新的维修：
        * **标题**: {{ function.parameters.title }}
        * **描述**: {{ function.parameters.description }}
      """
    }
  })
  op createRepair(
    @body repair: Repair
  ): Repair;

  model Repair {
    id?: string;
    title: string;
    description?: string;
    assignedTo?: string;
  }

  @authReferenceId("${{REPAIRSHUBAPIKEYAUTH_REFERENCE_ID}}")
  model RepairsHubApiKeyAuth is ApiKeyAuth<ApiKeyLocation.query, "code">;
}
```

## 快速入门

### 先决条件
- [Visual Studio Code](https://code.visualstudio.com/)
- [Microsoft 365 代理工具包 Visual Studio Code 扩展](https://aka.ms/M365AgentsToolkit)
- Microsoft 365 Copilot 许可证

### 创建第一个代理

1. 打开 Visual Studio Code
2. 选择 **Microsoft 365 代理工具包 > 创建新代理/应用**
3. 选择 **声明式代理**
4. 选择 **从 Microsoft 365 Copilot 的 TypeSpec 开始**
5. 选择您的项目位置和名称
6. 编辑 `main.tsp` 文件以自定义您的代理
7. 在生命周期面板中选择 **部署** 以发布

## 最佳实践

### 指令
- 明确说明代理的角色和专长
- 定义应避免的行为以及期望的行为
- 保持指令在 8000 字符以内
- 使用三引号字符串来编写多行指令

### 对话启动器
- 提供 2-4 个多样化的与代理交互示例
- 使其与您的代理功能相关
- 保持标题简洁（不超过 100 字符）

### 功能
- 仅包含代理实际需要的功能
- 尽可能将功能限定在特定资源上
- 使用 URL 和 ID 以限制对相关内容的访问

### API 操作
- 使用描述性的操作名称和清晰的参数名称
- 为模型和人类用户提供详细的描述
- 对破坏性操作使用确认对话框
- 实现带有有意义错误信息的适当错误处理

### 认证
- 在生产环境中使用注册的认证配置
- 遵循最小特权原则来配置作用域
- 将敏感凭据存储在环境变量中
- 使用 `@authReferenceId` 引用注册的配置

## 开发工作流程

1. **创建**：使用 Microsoft 365 代理工具包来搭建项目框架
2. **定义**：在 `main.tsp` 和 `actions.tsp` 中编写 TypeSpec 定义
3. **配置**：设置认证和功能
4. **部署**：发布到开发环境
5. **测试**：在 Microsoft 365 Copilot (https://m365.cloud.microsoft/chat) 中验证
6. **调试**：使用 Copilot 开发者模式进行故障排查
7. **迭代**：根据测试反馈进行优化
8. **发布**：准备好后发布到生产环境

## 常见模式

### 文件结构
```
project/
├── appPackage/
│   ├── cards/
│   │   └── card.json
│   ├── .generated/
│   ├── manifest.json
│   └── ...
├── src/
│   ├── main.tsp
│   └── actions.tsp
├── m365agents.yml
└── package.json
```

### 多文件 TypeSpec
```typescript
// main.tsp
import "@typespec/http";
import "@microsoft/typespec-m365-copilot";
import "./actions.tsp";

using TypeSpec.Http;
using TypeSpec.M365.Copilot.Agents;
using TypeSpec.M365.Copilot.Actions;

@agent("我的代理", "描述")
@instructions("指令内容")
namespace MyAgent {
  op apiAction is MyAPI.someOperation;
}

// actions.tsp
import "@typespec/http";
import "@microsoft/typespec-m365-copilot";

@service
@actions(#{
  nameForHuman: "项目管理 API",
  descriptionForHuman: "管理项目和任务",
  descriptionForModel: "用于创建、更新和跟踪项目任务的 API"
})
@server("https://api.example.com")
namespace MyAPI {
  @route("/operation")
  @get
  @action
  op someOperation(): Response;
}
```

### 自适应卡片
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
        },
        {
          "type": "Image",
          "url": "${image}",
          "$when": "${image != null}"
        }
      ]
    }
  ]
}
```

## 资源

- [TypeSpec 官方文档](https://typespec.io/)
- [Microsoft 365 代理工具包](https://aka.ms/M365AgentsToolkit)
- [声明式代理文档](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/overview-declarative-agent)
- [API 插件文档](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/overview-api-plugins)
- [PnP Copilot 示例](https://github.com/pnp/copilot-pro-dev-samples)

## 深入了解

- [TypeSpec 概述](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/overview-typespec)
- [使用 TypeSpec 构建声明式代理](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/build-declarative-agents-typespec)
- [TypeSpec 场景](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/typespec-scenarios)
- [TypeSpec 认证](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/typespec-authentication)
- [TypeSpec 装饰器参考](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/typespec-decorators)
- [TypeSpec 功能参考](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/typespec-capabilities)
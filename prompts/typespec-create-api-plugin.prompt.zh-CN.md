

---
mode: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems']
description: '生成一个包含 REST 操作、认证和 Microsoft 365 Copilot 自适应卡片的 TypeSpec API 插件'
model: 'gpt-4.1'
tags: [typespec, m365-copilot, api-plugin, rest-api]
---

# 创建 TypeSpec API 插件

创建一个完整的 TypeSpec API 插件，用于 Microsoft 365 Copilot 并与外部 REST API 集成。

## 要求

生成包含以下内容的 TypeSpec 文件：

### main.tsp - 代理定义
```typescript
import "@typespec/http";
import "@typespec/openapi3";
import "@microsoft/typespec-m365-copilot";
import "./actions.tsp";

using TypeSpec.Http;
using TypeSpec.M365.Copilot.Agents;
using TypeSpec.M365.Copilot.Actions;

@agent({
  name: "[代理名称]",
  description: "[描述]"
})
@instructions("""
  [使用 API 操作的说明]
""")
namespace [AgentName] {
  // 从 actions.tsp 引用操作
  op operation1 is [APINamespace].operationName;
}
```

### actions.tsp - API 操作
```typescript
import "@typespec/http";
import "@microsoft/typespec-m365-copilot";

using TypeSpec.Http;
using TypeSpec.M365.Copilot.Actions;

@service
@actions(#{
    nameForHuman: "[API 显示名称]",
    descriptionForModel: "[模型描述]",
    descriptionForHuman: "[用户描述]"
})
@server("[API_BASE_URL]", "[API 名称]")
@useAuth([AuthType]) // 可选
namespace [APINamespace] {
  
  @route("[/路径]")
  @get
  @action
  op operationName(
    @path param1: string,
    @query param2?: string
  ): ResponseModel;

  model ResponseModel {
    // 响应结构
  }
}
```

## 认证选项

根据 API 要求选择以下认证方式：

1. **无需认证**（公共 API）
   ```typescript
   // 不需要 @useAuth 装饰器
   ```

2. **API 密钥**
   ```typescript
   @useAuth(ApiKeyAuth<ApiKeyLocation.header, "X-API-Key">)
   ```

3. **OAuth2**
   ```typescript
   @useAuth(OAuth2Auth<[{
     type: OAuth2FlowType.authorizationCode;
     authorizationUrl: "https://oauth.example.com/authorize";
     tokenUrl: "https://oauth.example.com/token";
     refreshUrl: "https://oauth.example.com/token";
     scopes: ["read", "write"];
   }]>)
   ```

4. **注册的认证引用**
   ```typescript
   @useAuth(Auth)
   
   @authReferenceId("注册 ID")
   model Auth is ApiKeyAuth<ApiKeyLocation.header, "X-API-Key">
   ```

## 功能能力

### 确认对话框
```typescript
@capabilities(#{
  confirmation: #{
    type: "AdaptiveCard",
    title: "确认操作",
    body: """
    您确定要执行此操作吗？
      * **参数**: {{ function.parameters.paramName }}
    """
  }
})
```

### 自适应卡片响应
```typescript
@card(#{
  dataPath: "$.items",
  title: "$.title",
  url: "$.link",
  file: "cards/card.json"
})
```

### 推理与响应说明
```typescript
@reasoning("""
  调用此操作时需考虑用户的上下文。
  优先显示最近的条目而非较旧的条目。
""")
@responding("""
  以清晰的表格格式呈现结果，包含列：ID、标题、状态。
  最后包含一个总结计数。
""")
```

## 最佳实践

1. **操作名称**：使用清晰、以动词为导向的名称（如 listProjects、createTicket）
2. **模型**：为请求和响应定义类似 TypeScript 的模型
3. **HTTP 方法**：使用适当的动词（@get、@post、@patch、@delete）
4. **路径**：使用 @route 实现 RESTful 路径约定
5. **参数**：根据场景合理使用 @path、@query、@header、@body
6. **描述**：为模型提供清晰的描述以增强理解
7. **确认机制**：对具有破坏性的操作（如删除、更新关键数据）添加确认步骤
8. **卡片**：用于需要多数据项的丰富可视化响应

## 工作流程

请向用户询问以下信息：
1. API 的基础 URL 和用途是什么？
2. 需要哪些操作（CRUD 操作）？
3. API 使用哪种认证方式？
4. 是否需要对某些操作设置确认要求？
5. 响应是否需要使用自适应卡片？

然后生成：
- 包含代理定义的完整 `main.tsp` 文件
- 包含 API 操作和模型的完整 `actions.tsp` 文件
- 如需自适应卡片，可选生成 `cards/card.json` 文件
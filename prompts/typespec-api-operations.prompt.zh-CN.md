

---
mode: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems']
description: '为TypeSpec API插件添加GET、POST、PATCH和DELETE操作，包含正确的路由、参数和自适应卡片'
model: 'gpt-4.1'
tags: [typespec, m365-copilot, api-plugin, rest-operations, crud]
---

# 为TypeSpec API插件添加操作

为Microsoft 365 Copilot的现有TypeSpec API插件添加RESTful操作。

## 添加GET操作

### 简单GET - 列出所有项目
```typescript
/**
 * 列出所有项目。
 */
@route("/items")
@get op listItems(): Item[];
```

### 带查询参数的GET - 过滤结果
```typescript
/**
 * 根据条件过滤列出的项目。
 * @param userId 可选的用户ID以过滤项目
 */
@route("/items")
@get op listItems(@query userId?: integer): Item[];
```

### 带路径参数的GET - 获取单个项目
```typescript
/**
 * 通过ID获取特定项目。
 * @param id 要检索的项目的ID
 */
@route("/items/{id}")
@get op getItem(@path id: integer): Item;
```

### 带自适应卡片的GET
```typescript
/**
 * 列出带有自适应卡片可视化的项目。
 */
@route("/items")
@card(#{
  dataPath: "$",
  title: "$.title",
  file: "item-card.json"
})
@get op listItems(): Item[];
```

**创建自适应卡片** (`appPackage/item-card.json`):
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
          "text": "**${if(title, title, 'N/A')}**",
          "wrap": true
        },
        {
          "type": "TextBlock",
          "text": "${if(description, description, 'N/A')}",
          "wrap": true
        }
      ]
    }
  ],
  "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "查看详情",
      "url": "https://example.com/items/${id}"
    }
  ]
}
```

## 添加POST操作

### 简单POST - 创建项目
```typescript
/**
 * 创建新项目。
 * @param item 要创建的项目
 */
@route("/items")
@post op createItem(@body item: CreateItemRequest): Item;

model CreateItemRequest {
  title: string;
  description?: string;
  userId: integer;
}
```

### 带确认的POST
```typescript
/**
 * 创建新项目并进行确认。
 */
@route("/items")
@post
@capabilities(#{
  confirmation: #{
    type: "AdaptiveCard",
    title: "创建项目",
    body: """
    确认是否要创建此项目？
      * **标题**: {{ function.parameters.item.title }}
      * **用户ID**: {{ function.parameters.item.userId }}
    """
  }
})
op createItem(@body item: CreateItemRequest): Item;
```

## 添加PATCH操作

### 简单PATCH - 更新项目
```typescript
/**
 * 更新现有项目。
 * @param id 要更新的项目的ID
 * @param item 更新后的项目数据
 */
@route("/items/{id}")
@patch op updateItem(
  @path id: integer,
  @body item: UpdateItemRequest
): Item;

model UpdateItemRequest {
  title?: string;
  description?: string;
  status?: "active" | "completed" | "archived";
}
```

### 带确认的PATCH
```typescript
/**
 * 带确认的更新项目。
 */
@route("/items/{id}")
@patch
@capabilities(#{
  confirmation: #{
    type: "AdaptiveCard",
    title: "更新项目",
    body: """
    正在更新项目 #{{ function.parameters.id }}:
      * **标题**: {{ function.parameters.item.title }}
      * **状态**: {{ function.parameters.item.status }}
    """
  }
})
op updateItem(
  @path id: integer,
  @body item: UpdateItemRequest
): Item;
```

## 添加DELETE操作

### 简单DELETE
```typescript
/**
 * 删除项目。
 * @param id 要删除的项目的ID
 */
@route("/items/{id}")
@delete op deleteItem(@path id: integer): void;
```

### 带确认的DELETE
```typescript
/**
 * 带确认的删除项目。
 */
@route("/items/{id}")
@delete
@capabilities(#{
  confirmation: #{
    type: "AdaptiveCard",
    title: "删除项目",
    body: """
    ⚠️ 确认是否要删除项目 #{{ function.parameters.id }}？
    此操作无法撤销。
    """
  }
})
op deleteItem(@path id: integer): void;
```

## 完整的CRUD示例

### 定义服务和模型
```typescript
@service
@server("https://api.example.com")
@actions(#{
  nameForHuman: "Items API",
  descriptionForHuman: "管理项目",
  descriptionForModel: "读取、创建、更新和删除项目"
})
namespace ItemsAPI {
  
  // 模型
  model Item {
    @visibility(Lifecycle.Read)
    id: integer;
    
    userId: integer;
    title: string;
    description?: string;
    status: "active" | "completed" | "archived";
    
    @format("date-time")
    createdAt: utcDateTime;
    
    @format("date-time")
    updatedAt?: utcDateTime;
  }

  model CreateItemRequest {
    userId: integer;
    title: string;
    description?: string;
  }

  model UpdateItemRequest {
    title?: string;
    description?: string;
    status?: "active" | "completed" | "archived";
  }

  // 操作
  @route("/items")
  @card(#{ dataPath: "$", title: "$.title", file: "item-card.json" })
  @get op listItems(@query userId?: integer): Item[];

  @route("/items/{id}")
  @card(#{ dataPath: "$", title: "$.title", file: "item-card.json" })
  @get op getItem(@path id: integer): Item;

  @route("/items")
  @post
  @capabilities(#{
    confirmation: #{
      type: "AdaptiveCard",
      title: "创建项目",
      body: "正在创建: **{{ function.parameters.item.title }}**"
    }
  })
  op createItem(@body item: CreateItemRequest): Item;

  @route("/items/{id}")
  @patch
  @capabilities(#{
    confirmation: #{
      type: "AdaptiveCard",
      title: "更新项目",
      body: "正在更新项目 #{{ function.parameters.id }}"
    }
  })
  op updateItem(@path id: integer, @body item: UpdateItemRequest): Item;

  @route("/items/{id}")
  @delete
  @capabilities(#{
    confirmation: #{
      type: "AdaptiveCard",
      title: "删除项目",
      body: "⚠️ 确认是否要删除项目 #{{ function.parameters.id }}？"
    }
  })
  op deleteItem(@path id: integer): void;
}
```

## 高级功能

### 多个查询参数
```typescript
@route("/items")
@get op listItems(
  @query userId?: integer,
  @query status?: "active" | "completed" | "archived",
  @query limit?: integer,
  @query offset?: integer
): ItemList;

model ItemList {
  items: Item[];
  total: integer;
  hasMore: boolean;
}
```

### 头部参数
```typescript
@route("/items")
@get op listItems(
  @header("X-API-Version") apiVersion?: string,
  @query userId?: integer
): Item[];
```

### 自定义响应模型
```typescript
@route("/items/{id}")
@delete op deleteItem(@path id: integer): DeleteResponse;

model DeleteResponse {
  success: boolean;
  message: string;
  deletedId: integer;
}
```

### 错误响应
```typescript
model ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: string[];
  };
}

@route("/items/{id}")
@get op getItem(@path id: integer): Item | ErrorResponse;
```

## 测试提示

添加操作后，使用以下提示进行测试：

**GET操作:**
- "列出所有项目并以表格形式显示"
- "显示用户ID为1的项目"
- "获取项目42的详细信息"

**POST操作:**
- "为用户1创建一个标题为'My Task'的新项目"
- "添加一个项目：标题'New Feature'，描述'Add login'"

**PATCH操作:**
- "将项目10的标题更新为'Updated Title'"
- "将项目5的状态改为completed"

**DELETE操作:**
- "删除项目99"
- "删除ID为15的项目"

## 最佳实践

### 参数命名
- 使用描述性的参数名称：`userId` 而不是 `uid`
- 在所有操作中保持一致性
- 对于过滤条件使用可选参数 (`?`)

### 文档
- 为所有操作添加JSDoc注释
- 描述每个参数的作用
- 记录预期的响应

### 模型
- 对只读字段如 `id` 使用 `@visibility(Lifecycle.Read)`
- 对日期字段使用 `@format("date-time")`
- 对枚举使用联合类型：`"active" | "completed"`
- 使用 `?` 明确表示可选字段

### 确认
- 对破坏性操作（DELETE、PATCH）始终添加确认
- 在确认内容中显示关键信息
- 对不可逆操作使用警告表情符号（⚠️）

### 自适应卡片
- 保持卡片简洁且聚焦
- 使用 `${if(..., ..., 'N/A')}` 进行条件渲染
- 包含常见下一步操作的按钮
- 使用实际API响应测试数据绑定

### 路由
- 使用RESTful约定：
  - `GET /items` - 列出
  - `GET /items/{id}` - 获取单个
  - `POST /items` - 创建
  - `PATCH /items/{id}` - 更新
  - `DELETE /items/{id}` - 删除
- 将相关操作分组到同一命名空间
- 对分层资源使用嵌套路由
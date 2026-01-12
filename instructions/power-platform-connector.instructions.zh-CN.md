

---
title: Power Platform 连接器模式开发指南
description: '涵盖 API 定义（Swagger 2.0）、API 属性以及使用 Microsoft 扩展进行设置配置的全面开发指南。'
applyTo: '**/*.{json,md}'
---

# Power Platform 连接器模式开发指南

## 项目概述
此工作区包含 Power Platform 自定义连接器的 JSON 模式定义，特别是为 `paconn`（Power Apps 连接器）工具设计的。这些模式用于验证并为以下内容提供智能感知支持：

- **API 定义**（Swagger 2.0 格式）
- **API 属性**（连接器元数据和配置）
- **设置**（环境和部署配置）

## 文件结构理解

### 1. apiDefinition.swagger.json
- **用途**：此文件包含带有 Power Platform 扩展的 Swagger 2.0 API 定义。
- **关键特性**：
  - 标准的 Swagger 2.0 属性，包括 `info`、`paths`、`definitions` 等。
  - 以 `x-ms-*` 前缀开头的 Microsoft 特定扩展。
  - 专为 Power Platform 设计的自定义格式类型，如 `date-no-tz` 和 `html`。
  - 动态模式支持，提供运行时灵活性。
  - 安全定义，支持 OAuth2、API Key 和基本身份验证方法。

### 2. apiProperties.json
- **用途**：此文件定义连接器元数据、身份验证配置和策略配置。
- **关键组件**：
  - **连接参数**：支持 OAuth、API Key 和网关配置等多种身份验证类型。
  - **策略模板实例**：处理连接器的数据转换和路由策略。
  - **连接器元数据**：包括发布者信息、功能和品牌元素。

### 3. settings.json
- **用途**：此文件为 paconn 工具提供环境和部署配置设置。
- **配置选项**：
  - 针对特定 Power Platform 环境的环境 GUID 目标。
  - 连接器资产和配置文件的文件路径映射。
  - 生产环境和测试环境（PROD/TIP1）的 API 端点 URL。
  - API 版本规范以确保与 Power Platform 服务的兼容性。

## 开发指南

### 在处理 API 定义（Swagger）时
1. **始终验证 Swagger 2.0 规范** - 模式强制执行严格的 Swagger 2.0 合规性。
2. **Microsoft 对操作的扩展**：
   - `x-ms-summary`：用于提供用户友好的显示名称，必须使用标题格式。
   - `x-ms-visibility`：用于控制参数的可见性，值为 `important`、`advanced` 或 `internal`。
   - `x-ms-trigger`：用于标记操作为触发器，值为 `batch` 或 `single`。
   - `x-ms-trigger-hint`：用于提供有助于用户操作触发器的提示文本。
   - `x-ms-trigger-metadata`：用于定义触发器配置设置，包括 `kind` 和 `mode` 属性。
   - `x-ms-notification`：用于配置 Webhook 操作以支持实时通知。
   - `x-ms-pageable`：通过指定 `nextLinkName` 属性启用分页功能。
   - `x-ms-safe-operation`：用于标记无副作用的 POST 操作为安全操作。
   - `x-ms-no-generic-test`：用于禁用特定操作的自动测试。
   - `x-ms-operation-context`：用于配置操作模拟设置以进行测试。

3. **Microsoft 对参数的扩展**：
   - `x-ms-dynamic-list`：用于启用从 API 调用中填充的动态下拉列表。
   - `x-ms-dynamic-values`：用于配置动态值源以填充参数选项。
   - `x-ms-dynamic-tree`：用于创建嵌套数据结构的分层选择器。
   - `x-ms-dynamic-schema`：用于根据用户选择允许运行时模式更改。
   - `x-ms-dynamic-properties`：用于动态属性配置，适应上下文。
   - `x-ms-enum-values`：用于提供增强的枚举定义，包含显示名称以提升用户体验。
   - `x-ms-test-value`：用于提供测试用的示例值，但绝不包含机密或敏感数据。
   - `x-ms-trigger-value`：用于指定触发器参数的值，包含 `value-collection` 和 `value-path` 属性。
   - `x-ms-url-encoding`：用于指定 URL 编码风格为 `single` 或 `double`（默认为 `single`）。
   - `x-ms-parameter-location`：用于为 API 提供参数位置提示（AutoRest 扩展 - Power Platform 忽略）。
   - `x-ms-localizeDefaultValue`：用于启用默认参数值的本地化。
   - `x-ms-skip-url-encoding`：用于跳过路径参数的 URL 编码（AutoRest 扩展 - Power Platform 忽略）。

4. **Microsoft 对模式的扩展**：
   - `x-ms-notification-url`：用于标记模式属性为 Webhook 配置的通知 URL。
   - `x-ms-media-kind`：用于指定内容的媒体类型，支持的值为 `image` 或 `audio`。
   - `x-ms-enum`：用于提供增强的枚举元数据（AutoRest 扩展 - Power Platform 忽略）。
   - 注意：上述所有参数扩展也适用于模式属性，并可在模式定义中使用。

5. **根级扩展**：
   - `x-ms-capabilities`：用于定义连接器功能，如文件选择器和测试连接功能。
   - `x-ms-connector-metadata`：用于提供超出标准属性的额外连接器元数据。
   - `x-ms-docs`：用于配置连接器的文档设置和引用。
   - `x-ms-deployment-version`：用于跟踪部署管理的版本信息。
   - `x-ms-api-annotation`：用于添加 API 级别的注释以增强功能。

6. **路径级扩展**：
   - `x-ms-notification-content`：用于定义 Webhook 路径项的通知内容模式。

7. **操作级功能**：
   - `x-ms-capabilities`（操作级）：用于启用特定操作的功能，如 `chunkTransfer` 用于大文件传输。

8. **安全注意事项**：
   - 应为 API 定义适当的 `securityDefinitions` 以确保正确的身份验证。
   - **允许多个安全定义** - 可定义最多两种认证方法（例如，oauth2 + apiKey，basic + apiKey）。
   - **例外情况**：如果使用 "None" 认证，同一连接器中不能存在其他安全定义。
   - 应使用 `oauth2` 对于现代 API，使用 `apiKey` 对于简单令牌认证，并仅在内部/遗留系统中考虑 `basic` 认证。
   - 每个安全定义必须是恰好一种类型（通过 oneOf 验证：`basic`、`apiKey`、`oauth2`）。

9. **参数最佳实践**：
   - 应使用描述性的 `description` 字段帮助用户理解每个参数的用途。
   - 应实现 `x-ms-summary` 以提升用户体验（必须使用标题格式）。
   - 必须正确标记必填参数以确保验证正确。
   - 应使用适当的 `format` 值（包括 Power Platform 扩展）以启用正确的数据处理。
   - 应利用动态扩展以提升用户体验和数据验证。

10. **Power Platform 格式扩展**：
    - `date-no-tz`：表示不包含时间偏移信息的日期时间。
    - `html`：此格式告诉客户端在编辑时使用 HTML 编辑器，查看时使用 HTML 查看器。
    - 标准格式包括：`int32`、`int64`、`float`、`double`、`byte`、`binary`、`date`、`date-time`、`password`、`email`、`uri`、`uuid`。

### 在处理 API 属性时
1. **连接参数**：
   - 应选择适当的参数类型，如 `string`、`securestring` 或 `oauthSetting`。
   - 应使用正确的身份验证提供者配置 OAuth 设置。
   - 应在适当情况下使用 `allowedValues` 为下拉选项配置。
   - 应在需要条件参数时实现参数依赖关系。

2. **策略模板**：
   - 应使用 `routerequesttoendpoint` 为后端路由到不同的 API 端点。
   - 应实现 `setqueryparameter` 为查询参数设置默认值。
   - 应使用 `updatenextlink` 为分页场景处理分页。
   - 应应用 `pollingtrigger` 用于需要轮询行为的触发器操作。

3. **品牌和元数据**：
   - 必须始终指定 `iconBrandColor`，因为此属性对所有连接器都是必需的。
   - 应定义适当的 `capabilities` 以指定连接器是否支持操作或触发器。
   - 应设置有意义的 `publisher` 和 `stackOwner` 值以标识连接器的所有权。

### 在处理设置时
1. **环境配置**：
   - 应使用符合验证模式的正确 GUID 格式用于 `environment`。
   - 应为您的目标环境设置正确的 `powerAppsUrl` 和 `flowUrl`。
   - 应匹配 API 版本以满足特定需求。

2. **文件引用**：
   - 应保持与 `apiProperties.json` 和 `apiDefinition.swagger.json` 默认值一致的文件命名。
   - 应在本地开发环境中使用相对路径。
   - 应确保图标文件存在并正确引用在配置中。

## 模式验证规则

### 必需属性
- **API 定义**：`swagger: "2.0"`、`info`（包含 `title` 和 `version`）、`paths`
- **API 属性**：`properties` 中的 `iconBrandColor`
- **设置**：无必需属性（所有属性均为可选，且有默认值）

### 模式验证
- **供应商扩展**：必须匹配 `^x-(?!ms-)` 模式以用于非 Microsoft 扩展
- **路径项**：必须以 `/` 开头
- **环境 GUID**：必须匹配 UUID 格式模式 `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`
- **URL**：必须为有效的 URI 以用于端点配置
- **主机模式**：必须匹配 `^[^{}/ :\\\\]+(?::\\d+)?$`（不包含空格、协议或路径）

### 类型约束
- **安全定义**：
  - `securityDefinitions` 对象中最多允许两个安全定义
  - 每个单独的安全定义必须是恰好一种类型（通过 oneOf 验证：`basic`、`apiKey`、`oauth2`）
  - **例外情况**：使用 "None" 认证时，不能与其他安全定义共存
- **参数类型**：仅限特定枚举值（`string`、`number`、`integer`、`boolean`、`array`、`file`）
- **策略模板**：类型特定的参数要求
- **格式值**：扩展的格式集合，包括 Power Platform 格式
- **可见性值**：必须为 `important`、`advanced` 或 `internal` 中的一种
- **触发器类型**：必须为 `batch` 或 `single`

### 其他验证规则
- **$ref 引用**：应仅指向 `#/definitions/`、`#/parameters/` 或 `#/responses/`
- **路径参数**：所有路径参数必须标记为 `required: true`
- **信息对象**：描述应与标题不同
- **联系对象**：电子邮件必须为有效格式，URL 必须为有效 URI
- **许可证对象**：名称是必需的，若提供 URL 必须为有效 URI
- **外部文档**：URL 是必需的且必须为有效 URI
- **标签**：数组中的名称必须唯一
- **方案**：必须为有效的 HTTP 方案（`http`、`https`、`ws`、`wss`）
- **MIME 类型**：`consumes` 和 `produces` 中必须遵循有效的 MIME 类型格式

## 常见模式和示例

### API 定义示例

#### 使用 Microsoft 扩展的基本操作
```json
{
  "get": {
    "operationId": "GetItems",
    "summary": "Get items",
    "x-ms-summary": "获取项目",
    "x-ms-visibility": "important",
    "description": "从 API 获取项目列表",
    "parameters": [
      {
        "name": "category",
        "in": "query",
        "type": "string",
        "x-ms-summary": "类别",
        "x-ms-visibility": "important",
        "x-ms-dynamic-values": {
          "operationId": "GetCategories",
          "value-path": "id",
          "value-title": "name"
        }
      }
    ],
    "responses": {
      "200": {
        "description": "成功",
        "x-ms-summary": "成功",
        "schema": {
          "type": "object",
          "properties": {
            "items": {
              "type": "array",
              "x-ms-summary": "项目",
              "items": {
                "$ref": "#/definitions/Item"
              }
            }
          }
        }
      }
    }
  }
}
```

#### 触发器操作配置
```json
{
  "get": {
    "operationId": "WhenItemCreated",
    "x-ms-summary": "当项目被创建时",
    "x-ms-trigger": "batch",
    "x-ms-trigger-hint": "现在要查看其工作效果，请创建一个项目",
    "x-ms-trigger-metadata": {
      "kind": "query",
      "mode": "polling"
    },
    "x-ms-pageable": {
      "nextLinkName": "@odata.nextLink"
    }
  }
}
```

#### 动态模式示例
```json
{
  "name": "dynamicSchema",
  "in": "body",
  "schema": {
    "x-ms-dynamic-schema": {
      "operationId": "GetSchema",
      "parameters": {
        "table": {
          "parameter": "table"
        }
      },
      "value-path": "schema"
    }
  }
}
```

#### 文件选择器功能
```json
{
  "x-ms-capabilities": {
    "file-picker": {
      "open": {
        "operationId": "OneDriveFilePickerOpen",
        "parameters": {
          "dataset": {
            "value-property": "dataset"
          }
        }
      },
      "browse": {
        "operationId": "OneDriveFilePickerBrowse",
        "parameters": {
          "dataset": {
            "value-property": "dataset"
          }
        }
      },
      "value-title": "DisplayName",
      "value-collection": "value",
      "value-folder-property": "IsFolder",
      "value-media-property": "MediaType"
    }
  }
}
```

#### 测试连接功能（注意：不适用于自定义连接器）
```json
{
  "x-ms-capabilities": {
    "testConnection": {
      "operationId": "TestConnection",
      "parameters": {
        "param1": "literal-value"
      }
    }
  }
}
```

#### 操作上下文用于模拟
```json
{
  "x-ms-operation-context": {
    "simulate": {
      "operationId": "SimulateOperation",
      "parameters": {
        "param1": {
          "parameter": "inputParam"
        }
      }
    }
  }
}
```

### 基本 OAuth 配置
```json
{
  "type": "oauthSetting",
  "oAuthSettings": {
    "identityProvider": "oauth2",
    "clientId": "your-client-id",
    "scopes": ["scope1", "scope2"],
    "redirectMode": "Global"
  }
}
```

#### 多个安全定义示例
```json
{
  "securityDefinitions": {
    "oauth2": {
      "type": "oauth2",
      "flow": "accessCode",
      "authorizationUrl": "https://api.example.com/oauth/authorize",
      "tokenUrl": "https://api.example.com/oauth/token",
      "scopes": {
        "read": "读取权限",
        "write": "写入权限"
      }
    },
    "apiKey": {
      "type": "apiKey",
      "name": "X-API-Key",
      "in": "header"
    }
  }
}
```

**注意**：最多允许两个安全定义共存，但 "None" 认证不能与其他方法结合使用。

### 动态参数设置
```json
{
  "x-ms-dynamic-values": {
    "operationId": "GetItems",
    "value-path": "id",
    "value-title": "name"
  }
}
```

### 路由策略模板
```json
{
  "templateId": "routerequesttoendpoint",
  "title": "路由到后端",
  "parameters": {
    "x-ms-apimTemplate-operationName": ["GetData"],
    "x-ms-apimTemplateParameter.newPath": "/api/v2/data"
  }
}
```

## 最佳实践

1. **使用智能感知**：这些模式提供丰富的自动补全和验证功能，有助于开发过程。
2. **遵循命名规范**：为操作和参数使用描述性的名称以提高代码可读性。
3. **实现错误处理**：定义适当的响应模式和错误代码以正确处理失败场景。
4. **彻底测试**：在部署前验证模式以尽早发现潜在问题。
5. **注释扩展**：对 Microsoft 特定扩展进行注释，便于团队理解和未来维护。
6. **版本管理**：在 API 信息中使用语义化版本控制以跟踪更改和兼容性。
7. **安全优先**：始终实施适当的身份验证机制以保护您的 API 端点。

## 故障排除

### 常见模式违规
- **缺少必需属性**：`swagger: "2.0"`、`info.title`、`info.version`、`paths`
- **无效模式格式**：
  - GUID 必须匹配确切格式 `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`
  - URL 必须为有效的 URI 并包含正确的方案
  - 路径必须以 `/` 开头
  - 主机不能包含协议、路径或空格
- **错误的供应商扩展命名**：Microsoft 扩展使用 `x-ms-*` 前缀，其他扩展使用 `^x-(?!ms-)` 模式
- **类型不匹配的安全定义**：每个安全定义必须是恰好一种类型
- **无效的枚举值**：检查 `x-ms-visibility`、`x-ms-trigger` 和参数类型的允许值
- **$ref 指向无效位置**：必须指向 `#/definitions/`、`#/parameters/` 或 `#/responses/`
- **路径参数未标记为必填**：所有路径参数必须有 `required: true`
- **在错误上下文中使用 'file' 类型**：仅允许在 `formData` 参数中使用，不允许在模式中使用

### API 定义特定问题
- **动态模式冲突**：不能与固定模式属性同时使用 `x-ms-dynamic-schema`
- **触发器配置错误**：`x-ms-trigger-metadata` 必须同时包含 `kind` 和 `mode`
- **分页设置**：`x-ms-pageable` 必须包含 `nextLinkName` 属性
- **文件选择器配置错误**：必须包含 `open` 操作和必需属性
- **功能冲突**：某些功能可能与特定参数类型冲突
- **测试值安全**：绝不应在 `x-ms-test-value` 中包含机密或 PII 数据
- **操作上下文设置**：`x-ms-operation-context` 必须包含 `simulate` 对象和 `operationId`
- **通知内容模式**：路径级 `x-ms-notification-content` 必须定义正确的模式结构
- **媒体类型限制**：`x-ms-media-kind` 仅支持 `image` 或 `audio` 值
- **触发器值配置**：`x-ms-trigger-value` 必须至少包含一个属性（`value-collection` 或 `value-path`）

### 验证工具
- 使用 JSON 模式验证器检查您的模式定义是否符合规范。
- 利用 VS Code 内置的模式验证功能在开发过程中捕获错误。
- 部署前使用 paconn CLI 进行测试：`paconn validate --api-def apiDefinition.swagger.json`
- 验证与 Power Platform 连接器要求的兼容性。
- 使用 Power Platform 连接器门户在目标环境中进行验证和测试。
- 确保操作响应与预期模式匹配以防止运行时错误。

请记住：这些模式确保您的 Power Platform 连接器格式正确，并且能在 Power Platform 生态系统中正常运行。
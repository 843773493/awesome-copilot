

---
description: '开发 Azure 逻辑应用和 Power 自动化工作流的指南，包含工作流定义语言 (WDL)、集成模式和企业自动化最佳实践'
applyTo: "**/*.json,**/*.logicapp.json,**/workflow.json,**/*-definition.json,**/*.flow.json"
---

# Azure 逻辑应用和 Power 自动化说明

## 概述

这些说明将指导您使用基于 JSON 的工作流定义语言 (WDL) 编写高质量的 Azure 逻辑应用和 Microsoft Power 自动化工作流定义。Azure 逻辑应用是一个基于云的集成平台即服务 (iPaaS)，提供 1,400 多个连接器以简化跨服务和协议的集成。遵循这些指南，可以创建健壮、高效且易于维护的云工作流自动化解决方案。

## 工作流定义语言结构

在使用逻辑应用或 Power 自动化流程的 JSON 文件时，请确保您的工作流遵循以下标准结构：

```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "actions": { },
    "contentVersion": "1.0.0.0",
    "outputs": { },
    "parameters": { },
    "staticResults": { },
    "triggers": { }
  },
  "parameters": { }
}
```

## Azure 逻辑应用和 Power 自动化开发最佳实践

### 1. 触发器

- **根据场景选择适当的触发器类型**：
  - **请求触发器**：用于同步的 API 类似工作流
  - **周期触发器**：用于计划任务
  - **基于事件的触发器**：用于反应式模式（服务总线、事件网格等）
- **配置适当的触发器设置**：
  - 设置合理的超时时间
  - 对高流量数据源使用分页设置
  - 实现正确的身份验证

```json
"triggers": {
  "manual": {
    "type": "Request",
    "kind": "Http",
    "inputs": {
      "schema": {
        "type": "object",
        "properties": {
          "requestParameter": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

### 2. 动作

- **使用描述性的动作名称**来表明其用途
- **使用作用域对复杂工作流进行逻辑分组**
- **为不同操作使用适当的动作类型**：
  - HTTP 动作用于 API 调用
  - 连接器动作用于内置集成
  - 数据操作动作用于数据转换

```json
"actions": {
  "Get_Customer_Data": {
    "type": "Http",
    "inputs": {
      "method": "GET",
      "uri": "https://api.example.com/customers/@{triggerBody()?['customerId']}",
      "headers": {
        "Content-Type": "application/json"
      }
    },
    "runAfter": {}
  }
}
```

### 3. 错误处理与可靠性

- **实现强大的错误处理**：
  - 使用 "runAfter" 配置处理失败情况
  - 为瞬时错误配置重试策略
  - 使用带有 "runAfter" 条件的作用域处理错误分支
- **为关键操作实现回退机制**
- **为外部服务调用添加超时**
- **使用 runAfter 条件处理复杂的错误场景**

```json
"actions": {
  "HTTP_Action": {
    "type": "Http",
    "inputs": { },
    "retryPolicy": {
      "type": "fixed",
      "count": 3,
      "interval": "PT20S",
      "minimumInterval": "PT5S",
      "maximumInterval": "PT1H"
    }
  },
  "Handle_Success": {
    "type": "Scope",
    "actions": { },
    "runAfter": {
      "HTTP_Action": ["Succeeded"]
    }
  },
  "Handle_Failure": {
    "type": "Scope",
    "actions": {
      "Log_Error": {
        "type": "ApiConnection",
        "inputs": {
          "host": {
            "connection": {
              "name": "@parameters('$connections')['loganalytics']['connectionId']"
            }
          },
          "method": "post",
          "body": {
            "LogType": "WorkflowError",
            "ErrorDetails": "@{actions('HTTP_Action').outputs.body}",
            "StatusCode": "@{actions('HTTP_Action').outputs.statusCode}"
          }
        }
      },
      "Send_Notification": {
        "type": "ApiConnection",
        "inputs": {
          "host": {
            "connection": {
              "name": "@parameters('$connections')['office365']['connectionId']"
            }
          },
          "method": "post",
          "path": "/v2/Mail",
          "body": {
            "To": "support@contoso.com",
            "Subject": "工作流错误 - HTTP 调用失败",
            "Body": "<p>HTTP 调用失败，状态码：@{actions('HTTP_Action').outputs.statusCode}</p>"
          }
        },
        "runAfter": {
          "Log_Error": ["Succeeded"]
        }
      }
    },
    "runAfter": {
      "HTTP_Action": ["Failed", "TimedOut"]
    }
  }
}
```

### 4. 表达式和函数

- **使用内置表达式函数**来转换数据
- **保持表达式简洁且可读**
- **使用注释文档化复杂的表达式**

常见表达式模式：
- 字符串操作：`concat()`、`replace()`、`substring()`
- 集合操作：`filter()`、`map()`、`select()`
- 条件逻辑：`if()`、`and()`、`or()`、`equals()`
- 日期/时间操作：`formatDateTime()`、`addDays()`
- JSON 处理：`json()`、`array()`、`createArray()`

```json
"Set_Variable": {
  "type": "SetVariable",
  "inputs": {
    "name": "formattedData",
    "value": "@{map(body('Parse_JSON'), item => {
      return {
        id: item.id,
        name: toUpper(item.name),
        date: formatDateTime(item.timestamp, 'yyyy-MM-dd')
      }
    })}"
  }
}
```

#### 在 Power 自动化条件中使用表达式

Power 自动化支持在条件中使用高级表达式来检查多个值。在处理复杂逻辑条件时，请使用以下模式：

- 对单个值进行比较：使用基本条件设计器界面
- 多个条件：在高级模式中使用高级表达式

Power 自动化条件中的常见逻辑表达式函数：

| 表达式 | 描述 | 示例 |
|------------|-------------|---------|
| `and` | 如果两个参数都为真则返回 true | `@and(equals(item()?['Status'], 'completed'), equals(item()?['Assigned'], 'John'))` |
| `or` | 如果任一参数为真则返回 true | `@or(equals(item()?['Status'], 'completed'), equals(item()?['Status'], 'unnecessary'))` |
| `equals` | 检查值是否相等 | `@equals(item()?['Status'], 'blocked')` |
| `greater` | 检查第一个值是否大于第二个 | `@greater(item()?['Due'], item()?['Paid'])` |
| `less` | 检查第一个值是否小于第二个 | `@less(item()?['dueDate'], addDays(utcNow(),1))` |
| `empty` | 检查对象、数组或字符串是否为空 | `@empty(item()?['Status'])` |
| `not` | 返回布尔值的相反值 | `@not(contains(item()?['Status'], 'Failed'))` |

示例：检查状态是否为 "completed" 或 "unnecessary"：
```
@or(equals(item()?['Status'], 'completed'), equals(item()?['Status'], 'unnecessary'))
```

示例：检查状态是否为 "blocked" 并分配给特定人员：
```
@and(equals(item()?['Status'], 'blocked'), equals(item()?['Assigned'], 'John Wonder'))
```

示例：检查付款是否逾期且未完成：
```
@and(greater(item()?['Due'], item()?['Paid']), less(item()?['dueDate'], utcNow()))
```

**注意**：在 Power 自动化中，当在表达式中访问前一步骤的动态值时，使用 `item()?['PropertyName']` 语法安全地访问集合中的属性。

### 5. 参数和变量

- **对工作流进行参数化**以便在不同环境中复用
- **在工作流中使用变量存储临时值**
- **定义清晰的参数模式**，包含默认值和描述

```json
"parameters": {
  "apiEndpoint": {
    "type": "string",
    "defaultValue": "https://api.dev.example.com",
    "metadata": {
      "description": "API 端点的基础 URL"
    }
  }
},
"variables": {
  "requestId": "@{guid()}",
  "processedItems": []
}
```

### 6. 控制流

- **使用条件实现分支逻辑**
- **为独立操作实现并行分支**
- **使用 foreach 循环**并为集合设置合理的批次大小
- **为可并行操作应用 until 循环**并设置适当的退出条件

```json
"Process_Items": {
  "type": "Foreach",
  "foreach": "@body('Get_Items')",
  "actions": {
    "Process_Single_Item": {
      "type": "Scope",
      "actions": { }
    }
  },
  "runAfter": {
    "Get_Items": ["Succeeded"]
  },
  "runtimeConfiguration": {
    "concurrency": {
      "repetitions": 10
    }
  }
}
```

### 7. 内容和消息处理

- **验证消息模式**以确保数据完整性
- **实现适当的内容类型处理**
- **使用 Parse JSON 动作**处理结构化数据

```json
"Parse_Response": {
  "type": "ParseJson",
  "inputs": {
    "content": "@body('HTTP_Request')",
    "schema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string"
        },
        "data": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": { }
          }
        }
      }
    }
  }
}
```

### 8. 安全最佳实践

- **尽可能使用托管标识**
- **在 Key Vault 中存储密钥**
- **为连接实现最小权限访问**
- **对 API 端点实施身份验证**
- **为 HTTP 触发器实施 IP 限制**
- **对参数和消息中的敏感数据实施数据加密**
- **使用 Azure RBAC 控制对逻辑应用资源的访问**
- **定期审查工作流和连接的安全性**

```json
"Get_Secret": {
  "type": "ApiConnection",
  "inputs": {
    "host": {
      "connection": {
        "name": "@parameters('$connections')['keyvault']['connectionId']"
      }
    },
    "method": "get",
    "path": "/secrets/@{encodeURIComponent('apiKey')}/value"
  }
},
"Call_Protected_API": {
  "type": "Http",
  "inputs": {
    "method": "POST",
    "uri": "https://api.example.com/protected",
    "headers": {
      "Content-Type": "application/json",
      "Authorization": "Bearer @{body('Get_Secret')?['value']}"
    },
    "body": {
      "data": "@variables('processedData')"
    }
  },
  "authentication": {
    "type": "ManagedServiceIdentity"
  },
  "runAfter": {
    "Get_Secret": ["Succeeded"]
  }
}
```

## 性能优化

- **减少不必要的动作**
- **在可用时使用批量操作**
- **优化表达式以减少复杂性**
- **配置适当的超时值**
- **对大数据集实施分页**
- **对可并行操作实施并发控制**

```json
"Process_Items": {
  "type": "Foreach",
  "foreach": "@body('Get_Items')",
  "actions": {
    "Process_Single_Item": {
      "type": "Scope",
      "actions": { }
    }
  },
  "runAfter": {
    "Get_Items": ["Succeeded"]
  },
  "runtimeConfiguration": {
    "concurrency": {
      "repetitions": 10
    }
  }
}
```

### 工作流设计最佳实践

- **将工作流限制在 50 个动作以内**以优化设计器性能
- **在必要时将复杂的业务逻辑拆分为多个较小的工作流**
- **使用部署槽**进行需要零停机时间的逻辑应用部署
- **避免在触发器和动作定义中硬编码属性**
- **添加描述性注释**以提供触发器和动作定义的上下文信息
- **在可用时使用内置操作**而不是共享连接器以提高性能
- **使用集成账户**用于 B2B 场景和 EDI 消息处理
- **重用工作流模板**以在组织内实现标准模式
- **避免对作用域和动作进行深度嵌套**以保持可读性

### 监控和可观测性

- **配置诊断设置**以捕获工作流运行和指标
- **添加跟踪 ID**以关联相关的工作流运行
- **实现全面的日志记录**并使用适当的详细级别
- **设置警报**以监控工作流失败和性能下降
- **使用 Application Insights**进行端到端跟踪和监控

## 平台类型和注意事项

### Azure 逻辑应用 vs Power 自动化

虽然 Azure 逻辑应用和 Power 自动化共享相同的底层工作流引擎和语言，但它们的目标受众和功能有所不同：

- **Power 自动化**：
  - 提供面向业务用户的友好界面
  - 属于 Power 平台生态系统的一部分
  - 与 Microsoft 365 和 Dynamics 365 集成
  - 支持桌面流程用于 UI 自动化

- **Azure 逻辑应用**：
  - 企业级集成平台
  - 以开发者为中心，具备高级功能
  - 更深入的 Azure 服务集成
  - 更全面的监控和操作功能

### 逻辑应用类型

#### 消费型逻辑应用
- 按执行次数计费的定价模型
- 无服务器架构
- 适用于变量或不可预测的工作负载

#### 标准型逻辑应用
- 基于应用服务计划的固定定价
- 可预测的性能
- 支持本地开发
- 与虚拟网络 (VNet) 集成

#### 集成服务环境 (ISE)
- 专用的部署环境
- 更高的吞吐量和更长的执行时间
- 直接访问 VNet 资源
- 隔离的运行时环境

### Power 自动化许可证类型
- **Power 自动化每用户计划**：适用于单个用户
- **Power 自动化每流程计划**：适用于特定流程
- **Power 自动化流程计划**：适用于 RPA 功能
- **Power 自动化包含在 Office 365 中**：为 Office 365 用户提供有限功能

## 常见集成模式

### 架构模式
- **调解器模式**：使用逻辑应用/Power 自动化作为系统之间的编排层
- **基于内容的路由**：根据内容将消息路由到不同目的地
- **消息转换**：在不同格式（JSON、XML、EDI 等）之间转换消息
- **散射-收集模式**：并行分发工作并聚合结果
- **协议桥接**：连接使用不同协议（REST、SOAP、FTP 等）的系统
- **索赔检查模式**：将大型负载存储在 blob 存储或数据库中
- **Saga 模式**：使用补偿动作管理分布式事务
- **编舞模式**：在没有中央编排器的情况下协调多个服务

### 动作模式
- **异步处理模式**：用于长时间运行的操作
  ```json
  "LongRunningAction": {
    "type": "Http",
    "inputs": {
      "method": "POST",
      "uri": "https://api.example.com/longrunning",
      "body": { "data": "@triggerBody()" }
    },
    "retryPolicy": {
      "type": "fixed",
      "count": 3,
      "interval": "PT30S"
    }
  }
  ```

- **Webhook 模式**：用于基于回调的处理
  ```json
  "WebhookAction": {
    "type": "ApiConnectionWebhook",
    "inputs": {
      "host": {
        "connection": {
          "name": "@parameters('$connections')['servicebus']['connectionId']"
        }
      },
      "body": {
        "content": "@triggerBody()"
      },
      "path": "/subscribe/topics/@{encodeURIComponent('mytopic')}/subscriptions/@{encodeURIComponent('mysubscription')}"
    }
  }
  ```

### 企业集成模式
- **B2B 消息交换**：在贸易伙伴之间交换 EDI 文档（AS2、X12、EDIFACT）
- **集成账户**：用于存储和管理 B2B 艺术品（协议、模式、映射）
- **规则引擎**：使用 Azure 逻辑应用规则引擎实现复杂业务规则
- **消息验证**：根据模式验证消息以确保合规性和数据完整性
- **事务处理**：使用补偿事务处理业务事务以实现回滚

## 逻辑应用的 DevOps 和 CI/CD

### 源代码控制和版本管理

- **将逻辑应用定义存储在源代码控制中**（Git、Azure DevOps、GitHub）
- **使用 ARM 模板**部署到多个环境
- **实施适合您发布节奏的分支策略**
- **使用标签或版本属性**对逻辑应用进行版本管理

### 自动化部署

- **使用 Azure DevOps 管道或 GitHub Actions**进行自动化部署
- **实施参数化**以处理环境特定值
- **使用部署槽**进行零停机部署
- **在 CI/CD 管道中包含部署后验证测试**

```yaml
# 逻辑应用部署的 Azure DevOps YAML 管道示例
trigger:
  branches:
    include:
    - main
    - release/*

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: AzureResourceManagerTemplateDeployment@3
  inputs:
    deploymentScope: 'Resource Group'
    azureResourceManagerConnection: 'Your-Azure-Connection'
    subscriptionId: '$(subscriptionId)'
    action: 'Create Or Update Resource Group'
    resourceGroupName: '$(resourceGroupName)'
    location: '$(location)'
    templateLocation: 'Linked artifact'
    csmFile: '$(System.DefaultWorkingDirectory)/arm-templates/logicapp-template.json'
    csmParametersFile: '$(System.DefaultWorkingDirectory)/arm-templates/logicapp-parameters-$(Environment).json'
    deploymentMode: 'Incremental'
```

## 跨平台考虑事项

在同时使用 Azure 逻辑应用和 Power 自动化时：

- **导出/导入兼容性**：流程可以从 Power 自动化导出并导入到逻辑应用，但可能需要一些修改
- **连接器差异**：某些连接器在一个平台可用而在另一个平台不可用
- **环境隔离**：Power 自动化环境提供隔离，可能有不同的策略
- **ALM 实践**：考虑使用 Azure DevOps 管理逻辑应用，使用 Power 自动化解决方案管理流程

### 迁移策略

- **评估**：评估复杂性和迁移适配性
- **连接器映射**：在平台间映射连接器并识别差距
- **测试策略**：在切换前实施并行测试
- **文档**：记录所有配置更改以供参考

```json
// Power 平台解决方案结构示例（Power 自动化流程）
{
  "SolutionName": "MyEnterpriseFlows",
  "Version": "1.0.0",
  "Flows": [
    {
      "Name": "OrderProcessingFlow",
      "Type": "Microsoft.Flow/flows",
      "Properties": {
        "DisplayName": "订单处理流程",
        "DefinitionData": {
          "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
          "triggers": {
            "When_a_new_order_is_created": {
              "type": "ApiConnectionWebhook",
              "inputs": {
                "host": {
                  "connectionName": "shared_commondataserviceforapps",
                  "operationId": "SubscribeWebhookTrigger",
                  "apiId": "/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps"
                }
              }
            }
          },
          "actions": {
            // 动作将在此处定义
          }
        }
      }
    }
  ]
}
```

## 高级异常处理和监控

### 全面的异常处理策略

为实现健壮的工作流，采用多层次的异常处理方法：

1. **预防性措施**：
   - 为所有传入消息使用模式验证
   - 使用 `coalesce()` 和 `?` 运算符实施防御性表达式评估
   - 在关键操作前添加预条件检查

2. **运行时异常处理**：
   - 使用带有嵌套 try/catch 模式的结构化异常处理作用域
   - 对外部依赖项实施断路器模式
   - 根据异常类型不同处理捕获的异常

```json
"Process_With_Comprehensive_Error_Handling": {
  "type": "Scope",
  "actions": {
    "Try_Primary_Action": {
      "type": "Scope",
      "actions": {
        "Main_Operation": {
          "type": "Http",
          "inputs": { "method": "GET", "uri": "https://api.example.com/resource" }
        }
      }
    },
    "Handle_Connection_Errors": {
      "type": "Scope",
      "actions": {
        "Log_Connection_Error": {
          "type": "ApiConnection",
          "inputs": {
            "host": {
              "connection": {
                "name": "@parameters('$connections')['loganalytics']['connectionId']"
              }
            },
            "method": "post",
            "body": {
              "LogType": "ConnectionError",
              "ErrorCategory": "Network",
              "StatusCode": "@{result('Try_Primary_Action')?['outputs']?['Main_Operation']?['statusCode']}"
            }
          }
        },
        "Invoke_Fallback_Endpoint": {
          "type": "Http",
          "inputs": { "method": "GET", "uri": "https://fallback-api.example.com/resource" }
        }
      },
      "runAfter": {
        "Try_Primary_Action": ["Failed"]
      }
    },
    "Handle_Business_Logic_Errors": {
      "type": "Scope",
      "actions": {
        "Parse_Error_Response": {
          "type": "ParseJson",
          "inputs": {
            "content": "@outputs('Try_Primary_Action')?['Main_Operation']?['body']",
            "schema": {
              "type": "object",
              "properties": {
                "errorCode": { "type": "string" },
                "errorMessage": { "type": "string" }
              }
            }
          }
        },
        "Switch_On_Error_Type": {
          "type": "Switch",
          "expression": "@triggerBody()?['errorCode']",
          "cases": {
            "ResourceNotFound": {
              "actions": { "Create_Resource": { "type": "Http", "inputs": {} } }
            },
            "ValidationError": {
              "actions": { "Resubmit_With_Defaults": { "type": "Http", "inputs": {} } }
            },
            "PermissionDenied": {
              "actions": { "Elevate_Permissions": { "type": "Http", "inputs": {} } }
            }
          },
          "default": {
            "actions": { "Send_To_Support_Queue": { "type": "ApiConnection", "inputs": {} } }
          }
        }
      },
      "runAfter": {
        "Try_Primary_Action": ["Succeeded"]
      }
    }
  }
}
```

3. **集中式错误日志记录**：
   - 创建一个专门用于错误处理的逻辑应用，其他工作流可调用
   - 使用相关 ID 记录错误以实现跨系统的可追溯性
   - 按类型和严重程度分类错误以更好地分析

### 高级监控架构

实施涵盖以下内容的全面监控策略：

1. **操作监控**：
   - **健康检查**：创建专用的健康检查工作流
   - **心跳模式**：实施定期检查以验证系统健康状况
   - **死信处理**：处理和分析失败消息

2. **业务流程监控**：
   - **业务指标**：跟踪关键业务 KPI（订单处理时间、审批率等）
   - **SLA 监控**：测量与服务级别协议的性能
   - **相关追踪**：实施端到端事务追踪

3. **警报策略**：
   - **多渠道警报**：为适当的渠道配置警报（电子邮件、短信、Teams）
   - **基于严重程度的路由**：根据业务影响路由警报
   - **警报相关性**：将相关警报分组以防止警报疲劳

```json
"Monitor_Transaction_SLA": {
  "type": "Scope",
  "actions": {
    "Calculate_Processing_Time": {
      "type": "Compose",
      "inputs": "@{div(sub(ticks(utcNow()), ticks(triggerBody()?['startTime'])), 10000000)}"
    },
    "Check_SLA_Breach": {
      "type": "If",
      "expression": "@greater(outputs('Calculate_Processing_Time'), parameters('slaThresholdSeconds'))",
      "actions": {
        "Log_SLA_Breach": {
          "type": "ApiConnection",
          "inputs": {
            "host": {
              "connection": {
                "name": "@parameters('$connections')['loganalytics']['connectionId']"
              }
            },
            "method": "post",
            "body": {
              "LogType": "SLABreach",
              "TransactionId": "@{triggerBody()?['transactionId']}",
              "ProcessingTimeSeconds": "@{outputs('Calculate_Processing_Time')}",
              "SLAThresholdSeconds": "@{parameters('slaThresholdSeconds')}",
              "BreachSeverity": "@if(greater(length(body('Parse_Customer_Response')?['orders']), 0), div(sum(body('Parse_Customer_Response')?['orders'], item => item.amount), length(body('Parse_Customer_Response')?['orders'])), 0)"
            }
          }
        },
        "Send_SLA_Alert": {
          "type": "ApiConnection",
          "inputs": {
            "host": {
              "connection": {
                "name": "@parameters('$connections')['teams']['connectionId']"
              }
            },
            "method": "post",
            "body": {
              "notificationTitle": "SLA 超限警报",
              "message": "交易 @{triggerBody()?['transactionId']} 超过 SLA 限制",
              "channelId": "@{if(greater(outputs('Calculate_Processing_Time'), mul(parameters('slaThresholdSeconds'), 2)), parameters('criticalAlertChannelId'), parameters('warningAlertChannelId'))}"
            }
          }
        }
      }
    }
  }
}
```

## API 管理集成

将逻辑应用与 Azure API 管理集成以增强安全性、治理和管理：

### API 管理前端

- **通过 API 管理暴露逻辑应用**：
  - 为逻辑应用的 HTTP 触发器创建 API 定义
  - 应用一致的 URL 结构和版本控制
  - 实施 API 策略以实现安全性和转换

### 逻辑应用的 API 策略模板

```xml
<!-- 逻辑应用 API 策略示例 -->
<policies>
  <inbound>
    <!-- 身份验证 -->
    <validate-jwt header-name="Authorization" failed-validation-httpcode="401" failed-validation-error-message="未授权">
      <openid-config url="https://login.microsoftonline.com/{tenant-id}/.well-known/openid-configuration" />
      <required-claims>
        <claim name="aud" match="any">
          <value>api://mylogicapp</value>
        </claim>
      </required-claims>
    </validate-jwt>
    
    <!-- 速率限制 -->
    <rate-limit calls="5" renewal-period="60" />
    
    <!-- 请求转换 -->
    <set-header name="Correlation-Id" exists-action="override">
      <value>@(context.RequestId)</value>
    </set-header>
    
    <!-- 日志记录 -->
    <log-to-eventhub logger-id="api-logger">
      @{
        return new JObject(
          new JProperty("correlationId", context.RequestId),
          new JProperty("api", context.Api.Name),
          new JProperty("operation", context.Operation.Name),
          new JProperty("user", context.User.Email),
          new JProperty("ip", context.Request.IpAddress)
        ).ToString();
      }
    </log-to-eventhub>
  </inbound>
  <backend>
    <forward-request />
  </backend>
  <outbound>
    <!-- 响应转换 -->
    <set-header name="X-Powered-By" exists-action="delete" />
  </outbound>
  <on-error>
    <base />
  </on-error>
</policies>
```

### 工作流作为 API 模式

- **实现工作流作为 API 模式**：
  - 将逻辑应用专门设计为 API 后端
  - 使用带有 OpenAPI 模式的请求触发器
  - 应用一致的响应模式
  - 实现正确的状态码和错误处理

```json
"triggers": {
  "manual": {
    "type": "Request",
    "kind": "Http",
    "inputs": {
      "schema": {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
          "customerId": {
            "type": "string",
            "description": "客户的唯一标识符"
          },
          "requestType": {
            "type": "string",
            "enum": ["Profile", "OrderSummary"],
            "description": "要处理的请求类型"
          }
        },
        "required": ["customerId", "requestType"]
      },
      "method": "POST"
    }
  }
}
```

## 版本控制策略

为逻辑应用和 Power 自动化流程实施稳健的版本控制方法：

### 版本控制模式

1. **URI 路径版本控制**：
   - 在 HTTP 触发器路径中包含版本（/api/v1/resource）
   - 为每个主要版本维护独立的逻辑应用

2. **参数版本控制**：
   - 在流程定义中添加版本参数
   - 基于版本参数使用条件逻辑

3. **并行版本控制**：
   - 将新版本与现有版本并行部署
   - 在版本之间实施流量路由

### 版本迁移策略

```json
"actions": {
  "Check_Request_Version": {
    "type": "Switch",
    "expression": "@triggerBody()?['apiVersion']",
    "cases": {
      "1.0": {
        "actions": {
          "Process_V1_Format": {
            "type": "Scope",
            "actions": { }
          }
        }
      },
      "2.0": {
        "actions": {
          "Process_V2_Format": {
            "type": "Scope",
            "actions": { }
          }
        }
      }
    },
    "default": {
      "actions": {
        "Return_Version_Error": {
          "type": "Response",
          "kind": "Http",
          "inputs": {
            "statusCode": 400,
            "body": {
              "error": "不支持的 API 版本",
              "supportedVersions": ["1.0", "2.0"]
            }
          }
        }
      }
    }
  }
}
```

### 不同版本的 ARM 模板部署

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "logicAppName": {
      "type": "string",
      "metadata": {
        "description": "逻辑应用的基础名称"
      }
    },
    "version": {
      "type": "string",
      "metadata": {
        "description": "要部署的逻辑应用版本"
      },
      "allowedValues": ["v1", "v2", "v3"]
    }
  },
  "variables": {
    "fullLogicAppName": "[concat(parameters('logicAppName'), '-', parameters('version'))]",
    "workflowDefinitionMap": {
      "v1": "[variables('v1Definition')]",
      "v2": "[variables('v2Definition')]",
      "v3": "[variables('v3Definition')]"
    },
    "v1Definition": {},
    "v2Definition": {},
    "v3Definition": {}
  },
  "resources": [
    {
      "type": "Microsoft.Logic/workflows",
      "apiVersion": "2019-05-01",
      "name": "[variables('fullLogicAppName')]",
      "location": "[parameters('location')]",
      "identity": {
        "type": "SystemAssigned"
      },
      "properties": {
        "accessControl": {
          "triggers": {
            "allowedCallerIpAddresses": [
              {
                "addressRange": "13.91.0.0/16"
              },
              {
                "addressRange": "40.112.0.0/13"
              }
            ]
          },
          "contents": {
            "allowedCallerIpAddresses": [
              {
                "addressRange": "13.91.0.0/16"
              },
              {
                "addressRange": "40.112.0.0/13"
              }
            ]
          },
          "actions": {
            "allowedCallerIpAddresses": [
              {
                "addressRange": "13.91.0.0/16"
              },
              {
                "addressRange": "40.112.0.0/13"
              }
            ]
          }
        },
        "definition": {}
      }
    }
  ]
}
```

## 成本优化技术

实施策略以优化逻辑应用和 Power 自动化解决方案的成本：

### 逻辑应用按使用量计费优化

1. **触发器优化**：
   - 在触发器中使用批处理以在单次运行中处理多个项目
   - 实现适当的周期间隔（避免过度轮询）
   - 使用基于 Webhook 的触发器代替轮询触发器

2. **动作优化**：
   - 通过合并相关操作减少动作数量
   - 使用内置函数代替自定义动作
   - 为 foreach 循环实施适当的并发设置

3. **数据传输优化**：
   - 在 HTTP 请求/响应中最小化负载大小
   - 使用本地文件操作代替重复的 API 调用
   - 对大型负载实施数据压缩

### 逻辑应用标准（工作流）成本优化

1. **应用服务计划选择**：
   - 根据工作负载需求调整应用服务计划
   - 根据负载模式实施自动扩展
   - 对可预测的工作负载考虑保留实例

2. **资源共享**：
   - 在共享应用服务计划中合并工作流
   - 实施共享连接和集成资源
   - 高效使用集成账户

### Power 自动化许可证优化

1. **许可证类型选择**：
   - 根据工作流复杂度选择适当的许可证类型
   - 为每用户计划实施正确的用户分配
   - 考虑高级连接器的使用需求

2. **减少 API 调用**：
   - 缓存频繁访问的数据
   - 对多个记录实施批处理
   - 减少计划流程的触发频率

### 成本监控与治理

```json
"Monitor_Execution_Costs": {
  "type": "ApiConnection",
  "inputs": {
    "host": {
      "connection": {
        "name": "@parameters('$connections')['loganalytics']['connectionId']"
      }
    },
    "method": "post",
    "body": {
      "LogType": "WorkflowCostMetrics
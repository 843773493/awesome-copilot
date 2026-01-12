

description: '为记录端到端应用程序工作流的全面技术中立提示生成器。自动检测项目架构模式、技术栈和数据流模式，生成涵盖多个技术（包括 .NET、Java/Spring、React 和微服务架构）的详细实现蓝图，包括入口点、服务层、数据访问、错误处理和测试方法。'

agent: '代理'
---
# 项目工作流文档生成器

## 配置变量

```
${PROJECT_TYPE="Auto-detect|.NET|Java|Spring|Node.js|Python|React|Angular|Microservices|Other"}
<!-- 主要技术栈 -->

${ENTRY_POINT="API|GraphQL|Frontend|CLI|Message Consumer|Scheduled Job|Custom"}
<!-- 流程的起始点 -->

${PERSISTENCE_TYPE="Auto-detect|SQL Database|NoSQL Database|File System|External API|Message Queue|Cache|None"}
<!-- 数据存储类型 -->

${ARCHITECTURE_PATTERN="Auto-detect|Layered|Clean|CQRS|Microservices|MVC|MVVM|Serverless|Event-Driven|Other"}
<!-- 主要架构模式 -->

${WORKFLOW_COUNT=1-5}
<!-- 要记录的工作流数量 -->

${DETAIL_LEVEL="Standard|Implementation-Ready"}
<!-- 包含的实现细节级别 -->

${INCLUDE_SEQUENCE_DIAGRAM=true|false}
<!-- 生成序列图 -->

${INCLUDE_TEST_PATTERNS=true|false}
<!-- 包含测试方法 -->
```

## 生成的提示

```
"分析代码库并记录 ${WORKFLOW_COUNT} 个代表性端到端工作流
这些工作流可作为类似功能的实现模板。使用以下方法：
```

### 初始检测阶段

```
${PROJECT_TYPE == "Auto-detect" ? 
  "首先检查代码库结构以识别技术：
   - 检查 .NET 解决方案/项目、Spring 配置、Node.js/Express 文件等
   - 识别当前使用的主编程语言和框架
   - 根据文件夹结构和关键组件确定架构模式" 
  : "聚焦于 ${PROJECT_TYPE} 模式和规范"}
```

```
${ENTRY_POINT == "Auto-detect" ? 
  "通过查找以下内容识别典型入口点：
   - API 控制器或路由定义
   - GraphQL 解析器
   - 发起网络请求的 UI 组件
   - 消息处理程序或事件订阅者
   - 定时任务定义" 
  : "聚焦于 ${ENTRY_POINT} 入口点"}
```

```
${PERSISTENCE_TYPE == "Auto-detect" ? 
  "通过检查以下内容确定持久化机制：
   - 数据库上下文/连接配置
   - 仓库实现
   - ORM 映射
   - 外部 API 客户端
   - 文件系统交互" 
  : "聚焦于 ${PERSISTENCE_TYPE} 交互"}
```

### 工作流文档化说明

对于系统中 ${WORKFLOW_COUNT} 个最具代表性的流程：

#### 1. 流程概述
   - 提供流程名称和简要描述
   - 解释该流程所服务的业务目的
   - 识别触发动作或事件
   - 列出完整流程涉及的所有文件/类

#### 2. 入口点实现

**API 入口点：**
```
${ENTRY_POINT == "API" || ENTRY_POINT == "Auto-detect" ? 
  "- 文档化接收请求的 API 控制器类和方法
   - 展示完整的包含属性/注解的方法签名
   - 包含完整的请求 DTO/模型类定义
   - 文档化验证属性和自定义验证器
   - 展示认证/授权属性和检查逻辑" : ""}
```

**GraphQL 入口点：**
```
${ENTRY_POINT == "GraphQL" || ENTRY_POINT == "Auto-detect" ? 
  "- 文档化 GraphQL 解析器类和方法
   - 展示查询/变异的完整模式定义
   - 包含输入类型定义
   - 展示解析器方法实现及参数处理" : ""}
```

**前端入口点：**
```
${ENTRY_POINT == "Frontend" || ENTRY_POINT == "Auto-detect" ? 
  "- 文档化发起 API 调用的组件
   - 展示触发请求的事件处理函数
   - 包含 API 客户端服务方法
   - 展示与请求相关的状态管理代码" : ""}
```

**消息消费者入口点：**
```
${ENTRY_POINT == "Message Consumer" || ENTRY_POINT == "Auto-detect" ? 
  "- 文档化消息处理程序类和方法
   - 展示消息订阅配置
   - 包含完整的消息模型定义
   - 展示反序列化和验证逻辑" : ""}
```

#### 3. 服务层实现
   - 文档化每个涉及的服务类及其依赖关系
   - 展示完整的包含参数和返回类型的方法签名
   - 包含实际方法实现及关键业务逻辑
   - 在适用时文档化接口定义
   - 展示依赖注入注册模式

**CQRS 模式：**
```
${ARCHITECTURE_PATTERN == "CQRS" || ARCHITECTURE_PATTERN == "Auto-detect" ? 
  "- 包含完整的命令/查询处理程序实现" : ""}
```

**Clean 架构模式：**
```
${ARCHITECTURE_PATTERN == "Clean" || ARCHITECTURE_PATTERN == "Auto-detect" ? 
  "- 展示用例/交互器实现" : ""}
```

#### 4. 数据映射模式
   - 文档化 DTO 到领域模型的映射代码
   - 展示对象映射器配置或手动映射方法
   - 包含映射过程中的验证逻辑
   - 文档化映射过程中创建的任何领域事件

#### 5. 数据访问实现
   - 文档化仓库接口及其实现
   - 展示完整的包含参数和返回类型的完整方法签名
   - 包含实际查询实现
   - 文档化实体/模型类定义及其所有属性
   - 展示事务处理模式

**SQL 数据库模式：**
```
${PERSISTENCE_TYPE == "SQL Database" || PERSISTENCE_TYPE == "Auto-detect" ? 
  "- 包含 ORM 配置、注解或 Fluent API 使用
   - 展示实际 SQL 查询或 ORM 语句" : ""}
```

**NoSQL 数据库模式：**
```
${PERSISTENCE_TYPE == "NoSQL Database" || PERSISTENCE_TYPE == "Auto-detect" ? 
  "- 展示文档结构定义
   - 包含文档查询/更新操作" : ""}
```

#### 6. 响应构建
   - 文档化响应 DTO/模型类定义
   - 展示从领域/实体模型到响应模型的映射
   - 包含状态码选择逻辑
   - 文档化错误响应结构及生成方式

#### 7. 错误处理模式
   - 文档化流程中使用的异常类型
   - 展示每一层的 try/catch 模式
   - 包含全局异常处理程序配置
   - 文档化错误日志实现
   - 展示重试策略或断路器模式
   - 包含失败场景的补偿操作

#### 8. 异步处理模式
   - 文档化后台任务调度代码
   - 展示事件发布实现
   - 包含消息队列发送模式
   - 文档化回调或 Webhook 实现
   - 展示异步操作的跟踪和监控方式

**测试方法（可选）：**
```
${INCLUDE_TEST_PATTERNS ? 
  "9. **测试方法**
     - 文档化每一层的单元测试实现
     - 展示模拟模式和测试固定装置设置
     - 包含集成测试实现
     - 文档化测试数据生成方法
     - 展示 API/控制器测试实现" : ""}
```

**序列图（可选）：**
```
${INCLUDE_SEQUENCE_DIAGRAM ? 
  "10. **序列图**
      - 生成展示所有组件的详细序列图
      - 包含方法调用及其参数类型
      - 展示组件间的返回值
      - 文档化条件流程和错误路径" : ""}
```

#### 11. 命名规范
文档化以下一致的命名模式：
- 控制器命名（例如：`EntityNameController`）
- 服务命名（例如：`EntityNameService`）
- 仓库命名（例如：`IEntityNameRepository`）
- DTO 命名（例如：`EntityNameRequest`, `EntityNameResponse`）
- CRUD 操作的方法命名模式
- 变量命名规范
- 文件组织模式

#### 12. 实现模板
提供可复用的代码模板用于：
- 按照模式创建新的 API 端点
- 实现新的服务方法
- 添加新的仓库方法
- 创建新的领域模型类
- 实现适当的错误处理

### 技术特定实现模式

**.NET 实现模式（如检测到）：**
```
${PROJECT_TYPE == ".NET" || PROJECT_TYPE == "Auto-detect" ? 
  "- 完整的控制器类，包含属性、过滤器和依赖注入
   - Startup.cs 或 Program.cs 中的服务注册
   - Entity Framework DbContext 配置
   - 使用 EF Core 或 Dapper 的仓库实现
   - AutoMapper 配置文件
   - 用于横切关注点的中间件实现
   - 扩展方法模式
   - 配置驱动的选项模式实现
   - 使用 ILogger 的日志实现
   - 认证/授权过滤器或策略实现" : ""}
```

**Spring 实现模式（如检测到）：**
```
${PROJECT_TYPE == "Java" || PROJECT_TYPE == "Spring" || PROJECT_TYPE == "Auto-detect" ? 
  "- 完整的控制器类，包含注解和依赖注入
   - 服务实现中的事务边界
   - 仓库接口和实现
   - JPA 实体定义及其关系
   - DTO 类实现
   - Bean 配置和组件扫描
   - 异常处理程序实现
   - 自定义验证器实现" : ""}
```

**React 实现模式（如检测到）：**
```
${PROJECT_TYPE == "React" || PROJECT_TYPE == "Auto-detect" ? 
  "- 带有 props 和 state 的组件结构
   - Hook 实现模式（useState, useEffect, 自定义 Hook）
   - API 服务实现
   - 状态管理模式（Context, Redux）
   - 表单处理实现
   - 路由配置" : ""}
```

### 实现指南

基于记录的工作流，提供实现新功能的具体指导：

#### 1. 分步实现流程
- 添加类似功能时的起始位置
- 实现顺序（例如：模型 → 仓库 → 服务 → 控制器）
- 如何与现有横切关注点集成

#### 2. 常见避免问题
- 识别当前实现中的易错区域
- 注明性能考量
- 列出常见错误或问题

#### 3. 扩展机制
- 文档化如何接入现有扩展点
- 展示如何在不修改现有代码的情况下添加新行为
- 解释配置驱动的功能模式

**结论：**
总结在实现新功能时应遵循的重要模式，以保持与代码库的一致性。
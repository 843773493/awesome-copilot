

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems']
description: '创建具有正确OpenAPI文档的ASP.NET最小API端点'
---

# ASP.NET 最小API与OpenAPI

您的目标是帮助我创建结构良好的ASP.NET最小API端点，使用正确的类型并具备全面的OpenAPI/Swagger文档。

## API组织

- 使用 `MapGroup()` 扩展方法按组组织相关端点
- 使用端点过滤器处理横切关注点
- 通过单独的端点类构建较大的API
- 对于复杂的API，考虑采用基于功能的文件夹结构

## 请求与响应类型

- 定义显式的请求和响应DTO/模型
- 创建具有适当验证属性的清晰模型类
- 使用记录类型表示不可变的请求/响应对象
- 使用符合API设计标准的有意义属性名称
- 应用 `[Required]` 和其他验证属性以强制约束
- 使用 ProblemDetailsService 和 StatusCodePages 获取标准错误响应

## 类型处理

- 使用强类型路由参数并显式绑定类型
- 使用 `Results<T1, T2>` 表示多种响应类型
- 对于强类型响应，返回 `TypedResults` 而不是 `Results`
- 利用C# 10+特性如可空注解和只初始化属性

## OpenAPI文档

- 使用.NET 9中新增的内置OpenAPI文档支持
- 定义操作摘要和描述
- 使用 `WithName` 扩展方法添加操作ID
- 使用 `[Description()]` 为属性和参数添加描述
- 为请求和响应设置正确的内容类型
- 使用文档转换器添加服务器、标签和安全方案等元素
- 使用模式转换器对OpenAPI模式进行自定义调整
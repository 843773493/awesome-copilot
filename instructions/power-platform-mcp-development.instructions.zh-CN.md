

---
description: '开发Power Platform自定义连接器与Model Context Protocol (MCP)集成的说明'
applyTo: '**/*.{json,csx,md}'
---

# Power Platform MCP自定义连接器开发

## 说明

### MCP协议集成
- 始终为MCP通信实现JSON-RPC 2.0标准
- 使用`x-ms-agentic-protocol: mcp-streamable-1.0`头以实现与Copilot Studio的兼容性
- 将端点结构化以支持标准REST操作和MCP工具调用
- 转换响应以符合Copilot Studio的限制（不支持引用类型，仅支持单一类型）

### 模式设计最佳实践
- 从JSON模式中移除$ref和其他引用类型，因为Copilot Studio无法处理它们
- 在模式定义中使用单一类型而非类型数组
- 将anyOf/oneOf构造扁平化为单一模式以实现Copilot Studio兼容性
- 确保所有工具输入模式均为自包含模式，不包含外部引用

### 认证与安全
- 在Power Platform限制内实现OAuth 2.0并遵循MCP安全最佳实践
- 使用连接参数集以实现灵活的认证配置
- 验证令牌受众以防止中间人攻击
- 添加MCP特定的安全头以增强验证
- 支持多种认证方法（标准OAuth、增强型OAuth、API密钥回退）

### 自定义脚本实现
- 在自定义脚本(script.csx)中处理JSON-RPC转换
- 使用JSON-RPC错误响应格式实现适当的错误处理
- 在认证流程中添加令牌验证和受众检查
- 转换MCP服务器响应以实现Copilot Studio兼容性
- 使用连接参数实现动态安全配置

### Swagger定义指南
- 为Power Platform兼容性使用Swagger 2.0规范
- 为每个端点实现适当的`operationId`值
- 定义清晰的参数模式，包含适当的类型和描述
- 为所有成功和错误情况定义全面的响应模式
- 包含适当的HTTP状态码和响应头

### 资源和工具管理
- 将MCP资源结构化以便在Copilot Studio中作为工具输出使用
- 为资源内容确保正确的MIME类型声明
- 添加受众和优先级注释以提升Copilot Studio集成效果
- 实现资源转换以满足Copilot Studio的要求

### 连接参数配置
- 使用枚举下拉菜单选择OAuth版本和安全级别
- 提供清晰的参数描述和约束条件
- 支持不同部署场景下的多种认证参数集
- 在适当位置包含验证规则和默认值
- 通过连接参数值启用动态配置

### 错误处理与日志记录
- 实现符合JSON-RPC 2.0错误格式的全面错误响应
- 为认证、验证和转换步骤添加详细日志记录
- 提供有助于故障排查的清晰错误信息
- 包含与错误条件对应的适当HTTP状态码

### 测试与验证
- 使用实际的MCP服务器实现测试连接器
- 验证模式转换是否在Copilot Studio中正常工作
- 验证所有支持参数集的认证流程
- 确保各种故障场景下的正确错误处理
- 测试连接参数配置和动态行为

## 其他指南

### Power Platform认证要求
- 包含全面的文档（readme.md, CUSTOMIZE.md）
- 提供清晰的设置和配置说明
- 文档所有认证选项和安全考虑因素
- 包含适当的发布者和堆栈所有者信息
- 确保符合Power Platform连接器认证标准

### MCP服务器兼容性
- 设计以兼容标准的MCP服务器实现
- 支持常见的MCP方法，如`tools/list`、`tools/call`、`resources/list`
- 为`mcp-streamable-1.0`协议适当处理流式响应
- 实现适当的协议协商和功能检测

### Copilot Studio集成
- 确保工具定义在Copilot Studio的约束条件下正常工作
- 从Copilot Studio界面测试资源访问和工具调用
- 验证转换后的模式在对话中产生预期行为
- 确认与Copilot Studio代理框架的正确集成
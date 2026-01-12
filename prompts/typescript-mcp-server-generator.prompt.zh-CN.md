

---
agent: 'agent'
description: '生成一个完整的TypeScript MCP服务器项目，包含工具、资源和正确的配置'
---

# 生成TypeScript MCP服务器

创建一个完整的模型上下文协议（MCP）服务器项目，使用TypeScript/Node.js，并满足以下规格：

## 要求

1. **项目结构**：创建一个具有正确目录结构的新TypeScript/Node.js项目
2. **NPM包**：包含@modelcontextprotocol/sdk、zod@3，以及express（用于HTTP）或stdio支持
3. **TypeScript配置**：正确的tsconfig.json配置，支持ES模块
4. **服务器类型**：选择HTTP（带流式HTTP传输）或基于stdio的服务器
5. **工具**：创建至少一个有用的工具，并进行正确的模式验证
6. **错误处理**：包含全面的错误处理和验证

## 实现细节

### 项目设置
- 使用`npm init`初始化并创建package.json文件
- 安装依赖项：@modelcontextprotocol/sdk、zod@3以及传输相关的包
- 配置TypeScript以支持ES模块：在package.json中设置`"type": "module"`
- 添加开发依赖项：tsx或ts-node用于开发
- 创建适当的.gitignore文件

### 服务器配置
- 使用`McpServer`类进行高级实现
- 设置服务器名称和版本
- 选择适当的传输方式（StreamableHTTPServerTransport或StdioServerTransport）
- 对于HTTP：使用Express设置正确的中间件和错误处理
- 对于stdio：直接使用StdioServerTransport

### 工具实现
- 使用`registerTool()`方法并使用描述性名称
- 使用zod定义输入和输出的模式以进行验证
- 提供清晰的`title`和`description`字段
- 在结果中返回`content`和`structuredContent`
- 使用try-catch块实现正确的错误处理
- 在适当的情况下支持异步操作

### 资源/提示设置（可选）
- 使用`registerResource()`添加资源，并使用ResourceTemplate设置动态URI
- 使用`registerPrompt()`添加提示，并使用参数模式
- 考虑添加完成支持以提升用户体验

## 代码质量
- 使用TypeScript实现类型安全
- 一致使用async/await模式
- 在传输关闭事件中实现适当的清理
- 使用环境变量进行配置
- 为复杂逻辑添加内联注释
- 以清晰的职责划分结构化代码

## 可考虑的工具类型示例
- 数据处理和转换
- 外部API集成
- 文件系统操作（读取、搜索、分析）
- 数据库查询
- 文本分析或摘要（带抽样）
- 系统信息检索

## 配置选项
- **对于HTTP服务器**：
  - 通过环境变量配置端口
  - 为浏览器客户端设置CORS
  - 会话管理（无状态 vs 有状态）
  - 为本地服务器设置DNS重绑定保护

- **对于stdio服务器**：
  - 正确处理标准输入/输出
  - 基于环境的配置
  - 进程生命周期管理

## 测试指南
- 说明如何运行服务器（`npm start`或`npx tsx server.ts`）
- 提供MCP Inspector命令：`npx @modelcontextprotocol/inspector`
- 对于HTTP服务器，包含连接URL：`http://localhost:PORT/mcp`
- 提供工具调用示例
- 添加常见问题的故障排除提示

## 可考虑的附加功能
- 对于LLM驱动工具的抽样支持
- 交互式工作流的用户输入引导
- 支持启用/禁用的动态工具注册
- 用于批量更新的通知防抖
- 资源链接以实现高效的数据引用

生成一个完整的、生产就绪的MCP服务器项目，包含全面的文档、类型安全和错误处理功能。
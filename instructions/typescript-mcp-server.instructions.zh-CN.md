

---
描述: '使用TypeScript SDK构建Model Context Protocol (MCP)服务器的说明'
适用范围: '**/*.ts, **/*.js, **/package.json'
---

# TypeScript MCP服务器开发

## 指南

- 使用 **@modelcontextprotocol/sdk** npm包: `npm install @modelcontextprotocol/sdk`
- 从特定路径导入: `@modelcontextprotocol/sdk/server/mcp.js`, `@modelcontextprotocol/sdk/server/stdio.js` 等
- 使用 `McpServer` 类实现高级服务器功能，自动处理协议
- 使用 `Server` 类实现底层控制，手动处理请求处理器
- 使用 **zod** 进行输入/输出模式验证: `npm install zod@3`
- 始终为工具、资源和提示提供 `title` 字段以获得更好的UI显示
- 使用 `registerTool()`, `registerResource()` 和 `registerPrompt()` 方法（推荐使用较新的API）
- 使用zod定义模式: `{ inputSchema: { param: z.string() }, outputSchema: { result: z.string() } }`
- 从工具中返回 `content`（用于显示）和 `structuredContent`（用于结构化数据）
- 对于HTTP服务器，使用 `StreamableHTTPServerTransport` 与Express或类似框架
- 对于本地集成，使用 `StdioServerTransport` 进行基于标准I/O的通信
- 为每个请求创建新的传输实例以防止请求ID冲突（无状态模式）
- 使用 `sessionIdGenerator` 进行会话管理以实现有状态服务器
- 启用DNS重绑定保护以防止本地服务器攻击: `enableDnsRebindingProtection: true`
- 配置CORS头并暴露 `Mcp-Session-Id` 以支持浏览器端客户端
- 使用 `ResourceTemplate` 实现带有URI参数的动态资源: `new ResourceTemplate('resource://{param}', { list: undefined })`
- 使用 `completable()` 包装器从 `@modelcontextprotocol/sdk/server/completable.js` 实现补全功能以提升用户体验
- 使用 `server.server.createMessage()` 实现采样，向客户端请求LLM补全
- 使用 `server.server.elicitInput()` 在工具执行过程中请求额外用户输入
- 启用通知节流以支持批量更新: `debouncedNotificationMethods: ['notifications/tools/list_changed']`
- 动态更新: 调用已注册项的 `.enable()`、`.disable()`、`.update()` 或 `.remove()` 方法以发出 `listChanged` 通知
- 使用 `getDisplayName()` 从 `@modelcontextprotocol/sdk/shared/metadataUtils.js` 获取UI显示名称
- 使用MCP检查器测试服务器: `npx @modelcontextprotocol/inspector`

## 最佳实践

- 保持工具实现的单一职责
- 为LLM提供清晰、描述性的标题和描述
- 为所有参数和返回值使用正确的TypeScript类型
- 使用try-catch块实现全面的错误处理
- 在工具结果中返回 `isError: true` 以表示错误条件
- 使用async/await处理所有异步操作
- 正确关闭数据库连接并清理资源
- 在处理前验证输入参数
- 使用结构化日志进行调试，避免污染stdout/stderr
- 暴露文件系统或网络访问时考虑安全影响
- 在传输关闭事件中实现适当的资源清理
- 使用环境变量进行配置（端口、API密钥等）
- 清晰地记录工具的功能和限制
- 使用多个客户端进行测试以确保兼容性

## 常见模式

### 基本服务器设置（HTTP）
```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express from 'express';

const server = new McpServer({
    name: 'my-server',
    version: '1.0.0'
});

const app = express();
app.use(express.json());

app.post('/mcp', async (req, res) => {
    const transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: undefined,
        enableJsonResponse: true
    });
    
    res.on('close', () => transport.close());
    
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
});

app.listen(3000);
```

### 基本服务器设置（stdio）
```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new McpServer({
    name: 'my-server',
    version: '1.0.0'
});

// ... 注册工具、资源和提示 ...

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 简单工具
```typescript
import { z } from 'zod';

server.registerTool(
    'calculate',
    {
        title: '计算器',
        description: '执行基本计算',
        inputSchema: { a: z.number(), b: z.number(), op: z.enum(['+', '-', '*', '/']) },
        outputSchema: { result: z.number() }
    },
    async ({ a, b, op }) => {
        const result = op === '+' ? a + b : op === '-' ? a - b : 
                      op === '*' ? a * b : a / b;
        const output = { result };
        return {
            content: [{ type: 'text', text: JSON.stringify(output) }],
            structuredContent: output
        };
    }
);
```

### 动态资源
```typescript
import { ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';

server.registerResource(
    'user',
    new ResourceTemplate('users://{userId}', { list: undefined }),
    {
        title: '用户资料',
        description: '获取用户资料数据'
    },
    async (uri, { userId }) => ({
        contents: [{
            uri: uri.href,
            text: `用户 ${userId} 的数据在此`
        }]
    })
);
```

### 带有采样的工具
```typescript
server.registerTool(
    'summarize',
    {
        title: '文本摘要器',
        description: '使用LLM摘要文本',
        inputSchema: { text: z.string() },
        outputSchema: { summary: z.string() }
    },
    async ({ text }) => {
        const response = await server.server.createMessage({
            messages: [{
                role: 'user',
                content: { type: 'text', text: `摘要: ${text}` }
            }],
            maxTokens: 500
        });
        
        const summary = response.content.type === 'text' ? 
            response.content.text : '无法摘要';
        const output = { summary };
        return {
            content: [{ type: 'text', text: JSON.stringify(output) }],
            structuredContent: output
        };
    }
);
```

### 带补全的提示
```typescript
import { completable } from '@modelcontextprotocol/sdk/server/completable.js';

server.registerPrompt(
    'review',
    {
        title: '代码审查',
        description: '以特定重点审查代码',
        argsSchema: {
            language: completable(z.string(), value => 
                ['typescript', 'python', 'javascript', 'java']
                    .filter(l => l.startsWith(value))
            ),
            code: z.string()
        }
    },
    ({ language, code }) => ({
        messages: [{
            role: 'user',
            content: {
                type: 'text',
                text: `审查这段 ${language} 代码:\n\n${code}`
            }
        }]
    })
);
```

### 错误处理
```typescript
server.registerTool(
    'risky-operation',
    {
        title: '高风险操作',
        description: '可能会失败的操作',
        inputSchema: { input: z.string() },
        outputSchema: { result: z.string() }
    },
    async ({ input }) => {
        try {
            const result = await performRiskyOperation(input);
            const output = { result };
            return {
                content: [{ type: 'text', text: JSON.stringify(output) }],
                structuredContent: output
            };
        } catch (err: unknown) {
            const error = err as Error;
            return {
                content: [{ type: 'text', text: `错误: ${error.message}` }],
                isError: true
            };
        }
    }
);
```
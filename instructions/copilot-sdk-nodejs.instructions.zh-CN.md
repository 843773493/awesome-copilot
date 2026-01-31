---
applyTo: "**.ts, **.js, package.json"
description: "此文件提供了使用 GitHub Copilot SDK 构建 Node.js/TypeScript 应用程序的指导。"
name: "GitHub Copilot SDK Node.js 指南"
---

## 核心原则

- SDK 处于技术预览版，可能会有重大变更
- 需要 Node.js 18.0 或更高版本
- 需要安装 GitHub Copilot CLI 并将其添加到 PATH
- 使用 TypeScript 构建，以确保类型安全
- 全程使用 async/await 模式
- 提供完整的 TypeScript 类型定义

## 安装

始终通过 npm/pnpm/yarn 进行安装：

```bash
npm install @github/copilot-sdk
# 或
pnpm add @github/copilot-sdk
# 或
yarn add @github/copilot-sdk
```

## 客户端初始化

### 基础客户端设置

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();
// 使用 client...
await client.stop();
```

### 客户端配置选项

在创建 CopilotClient 时使用 `CopilotClientOptions`：

- `cliPath` - CLI 可执行文件路径（默认：从 PATH 中获取的 "copilot"）
- `cliArgs` - 在 SDK 管理的标志之前添加的额外参数（字符串数组）
- `cliUrl` - 现有 CLI 服务器的 URL（例如："localhost:8080"）。提供此参数时，客户端不会启动进程
- `port` - 服务器端口（默认：0 表示随机）
- `useStdio` - 使用 stdio 传输而不是 TCP（默认：true）
- `logLevel` - 日志级别（默认："debug"）
- `autoStart` - 自动启动服务器（默认：true）
- `autoRestart` - 在崩溃时自动重启（默认：true）
- `cwd` - CLI 进程的工作目录（默认：process.cwd()）
- `env` - CLI 进程的环境变量（默认：process.env）

### 手动服务器控制

对于显式控制：

```typescript
const client = new CopilotClient({ autoStart: false });
await client.start();
// 使用 client...
await client.stop();
```

当 `stop()` 响应时间过长时，使用 `forceStop()`。

## 会话管理

### 创建会话

使用 `SessionConfig` 进行配置：

```typescript
const session = await client.createSession({
    model: "gpt-5",
    streaming: true,
    tools: [...],
    systemMessage: { ... },
    availableTools: ["tool1", "tool2"],
    excludedTools: ["tool3"],
    provider: { ... }
});
```

### 会话配置选项

- `sessionId` - 自定义会话 ID（字符串）
- `model` - 模型名称（"gpt-5", "claude-sonnet-4.5" 等）
- `tools` - 暴露给 CLI 的自定义工具（Tool[]）
- `systemMessage` - 系统消息自定义（SystemMessageConfig）
- `availableTools` - 允许使用的工具名称列表（字符串数组）
- `excludedTools` - 禁用的工具名称列表（字符串数组）
- `provider` - 自定义 API 提供商配置（BYOK）（ProviderConfig）
- `streaming` - 启用流式响应块（布尔值）
- `mcpServers` - MCP 服务器配置（MCPServerConfig[]）
- `customAgents` - 自定义代理配置（CustomAgentConfig[]）
- `configDir` - 配置目录覆盖（字符串）
- `skillDirectories` - 技能目录（字符串数组）
- `disabledSkills` - 禁用的技能（字符串数组）
- `onPermissionRequest` - 权限请求处理程序（PermissionHandler）

### 恢复会话

```typescript
const session = await client.resumeSession("session-id", {
  tools: [myNewTool],
});
```

### 会话操作

- `session.sessionId` - 获取会话标识符（字符串）
- `await session.send({ prompt: "...", attachments: [...] })` - 发送消息，返回 Promise<string>
- `await session.sendAndWait({ prompt: "..." }, timeout)` - 发送并等待空闲，返回 Promise<AssistantMessageEvent | null>
- `await session.abort()` - 中止当前处理
- `await session.getMessages()` - 获取所有事件/消息，返回 Promise<SessionEvent[]>
- `await session.destroy()` - 清理会话

## 事件处理

### 事件订阅模式

始终使用 async/await 或 Promises 等待会话事件：

```typescript
await new Promise<void>((resolve) => {
  session.on((event) => {
    if (event.type === "assistant.message") {
      console.log(event.data.content);
    } else if (event.type === "session.idle") {
      resolve();
    }
  });

  session.send({ prompt: "..." });
});
```

### 取消事件订阅

`on()` 方法返回一个用于取消订阅的函数：

```typescript
const unsubscribe = session.on((event) => {
  // 处理程序
});
// 后续...
unsubscribe();
```

### 事件类型

使用类型守卫进行事件处理：

```typescript
session.on((event) => {
  switch (event.type) {
    case "user.message":
      // 处理用户消息
      break;
    case "assistant.message":
      console.log(event.data.content);
      break;
    case "tool.executionStart":
      // 工具执行开始
      break;
    case "tool.executionComplete":
      // 工具执行完成
      break;
    case "session.start":
      // 会话开始
      break;
    case "session.idle":
      // 会话空闲（处理完成）
      break;
    case "session.error":
      console.error(`错误: ${event.data.message}`);
      break;
  }
});
```

## 流式响应

### 启用流式响应

在 SessionConfig 中设置 `streaming: true`：

```typescript
const session = await client.createSession({
  model: "gpt-5",
  streaming: true,
});
```

### 处理流式事件

处理增量事件和最终事件：

```typescript
await new Promise<void>((resolve) => {
  session.on((event) => {
    switch (event.type) {
      case "assistant.message.delta":
        // 增量文本块
        process.stdout.write(event.data.deltaContent);
        break;
      case "assistant.reasoning.delta":
        // 增量推理块（模型相关）
        process.stdout.write(event.data.deltaContent);
        break;
      case "assistant.message":
        // 最终完整消息
        console.log("\n--- 最终 ---");
        console.log(event.data.content);
        break;
      case "assistant.reasoning":
        // 最终推理内容
        console.log("--- 推理 ---");
        console.log(event.data.content);
        break;
      case "session.idle":
        resolve();
        break;
    }
  });

  session.send({ prompt: "给我讲个故事" });
});
```

注意：最终事件（`assistant.message`, `assistant.reasoning`）无论流式设置如何都会始终发送。

## 自定义工具

### 使用 defineTool 定义工具

使用 `defineTool` 进行类型安全的工具定义：

```typescript
import { defineTool } from "@github/copilot-sdk";

const session = await client.createSession({
  model: "gpt-5",
  tools: [
    defineTool({
      name: "lookup_issue",
      description: "从跟踪器获取问题详情",
      parameters: {
        type: "object",
        properties: {
          id: { type: "string", description: "问题 ID" },
        },
        required: ["id"],
      },
      handler: async (args) => {
        const issue = await fetchIssue(args.id);
        return issue;
      },
    }),
  ],
});
```

### 使用 Zod 处理参数

SDK 支持 Zod 模式进行参数验证：

```typescript
import { z } from "zod";

const session = await client.createSession({
  tools: [
    defineTool({
      name: "get_weather",
      description: "获取指定位置的天气",
      parameters: z.object({
        location: z.string().describe("城市名称"),
        units: z.enum(["celsius", "fahrenheit"]).optional(),
      }),
      handler: async (args) => {
        return { temperature: 72, units: args.units || "fahrenheit" };
      },
    }),
  ],
});
```

### 工具返回类型

- 返回任何可序列化的 JSON 值（自动包装）
- 或返回 `ToolResultObject` 以完全控制元数据：

```typescript
{
    textResultForLlm: string;  // 显示给 LLM 的结果
    resultType: "success" | "failure";
    error?: string;  // 内部错误（不显示给 LLM）
    toolTelemetry?: Record<string, unknown>;
}
```

### 工具执行流程

当 Copilot 调用工具时，客户端会自动：

1. 运行您的处理函数
2. 序列化返回值
3. 向 CLI 响应

## 系统消息自定义

### 追加模式（默认 - 保留安全规则）

```typescript
const session = await client.createSession({
  model: "gpt-5",
  systemMessage: {
    mode: "append",
    content: `
<workflow_rules>
- 始终检查安全漏洞
- 适用时建议性能优化
</workflow_rules>
`,
  },
});
```

### 替换模式（完全控制 - 移除安全规则）

```typescript
const session = await client.createSession({
  model: "gpt-5",
  systemMessage: {
    mode: "replace",
    content: "你是一个有帮助的助手。",
  },
});
```

## 文件附件

将文件附加到消息中：

```typescript
await session.send({
  prompt: "分析此文件",
  attachments: [
    {
      type: "file",
      path: "/path/to/file.ts",
      displayName: "我的文件",
    },
  ],
});
```

## 消息传递模式

在消息选项中使用 `mode` 属性：

- `"enqueue"` - 将消息排队处理
- `"immediate"` - 立即处理消息

```typescript
await session.send({
  prompt: "...",
  mode: "enqueue",
});
```

## 多个会话

会话是独立的，可以并发运行：

```typescript
const session1 = await client.createSession({ model: "gpt-5" });
const session2 = await client.createSession({ model: "claude-sonnet-4.5" });

await Promise.all([
  session1.send({ prompt: "来自会话 1 的问候" }),
  session2.send({ prompt: "来自会话 2 的问候" }),
]);
```

## 自带密钥（BYOK）

使用自定义 API 提供商：

```typescript
const session = await client.createSession({
  provider: {
    type: "openai",
    baseUrl: "https://api.openai.com/v1",
    apiKey: "您的 API 密钥",
  },
});
```

## 会话生命周期管理

### 列出会话

```typescript
const sessions = await client.listSessions();
for (const metadata of sessions) {
  console.log(`${metadata.sessionId}: ${metadata.summary}`);
}
```

### 删除会话

```typescript
await client.deleteSession(sessionId);
```

### 获取最后一个会话 ID

```typescript
const lastId = await client.getLastSessionId();
if (lastId) {
  const session = await client.resumeSession(lastId);
}
```

### 检查连接状态

```typescript
const state = client.getState();
// 返回: "disconnected" | "connecting" | "connected" | "error"
```

## 错误处理

### 标准异常处理

```typescript
try {
  const session = await client.createSession();
  await session.send({ prompt: "Hello" });
} catch (error) {
  console.error(`错误: ${error.message}`);
}
```

### 会话错误事件

监控 `session.error` 事件类型以检测运行时错误：

```typescript
session.on((event) => {
  if (event.type === "session.error") {
    console.error(`会话错误: ${event.data.message}`);
    // 可选地重试或处理错误
  }
});

try {
  await session.send({ prompt: "危险操作" });
} catch (error) {
  // 处理发送错误
  console.error("发送失败:", error);
}
```

## 连接性测试

使用 ping 验证服务器连接性：

```typescript
const response = await client.ping("健康检查");
console.log(`服务器响应于 ${new Date(response.timestamp)}`);
```

## 资源清理

### 使用 try-finally 进行自动清理

始终使用 try-finally 或在 finally 块中进行清理：

```typescript
const client = new CopilotClient();
try {
  await client.start();
  const session = await client.createSession();
  try {
    // 使用 session...
  } finally {
    await session.destroy();
  }
} finally {
  await client.stop();
}
```

### 清理函数模式

```typescript
async function withClient<T>(
  fn: (client: CopilotClient) => Promise<T>,
): Promise<T> {
  const client = new CopilotClient();
  try {
    await client.start();
    return await fn(client);
  } finally {
    await client.stop();
  }
}

async function withSession<T>(
  client: CopilotClient,
  fn: (session: CopilotSession) => Promise<T>,
): Promise<T> {
  const session = await client.createSession();
  try {
    return await fn(session);
  } finally {
    await session.destroy();
  }
}

// 使用示例
await withClient(async (client) => {
  await withSession(client, async (session) => {
    await session.send({ prompt: "Hello!" });
  });
});
```

## 最佳实践

1. **始终使用 try-finally** 进行资源清理
2. **使用 Promises** 等待 session.idle 事件
3. **处理 session.error** 事件以实现健壮的错误处理
4. **使用类型守卫或 switch 语句** 进行事件处理
5. **启用流式响应** 以提升交互场景的用户体验
6. **使用 defineTool** 进行类型安全的工具定义
7. **使用 Zod 模式** 进行运行时参数验证
8. **在不再需要时取消事件订阅**
9. **使用 systemMessage 且 mode: "append"** 以保留安全规则
10. **启用流式响应时处理增量和最终事件**
11. **利用 TypeScript 类型** 实现编译时安全

## 常见模式

### 简单查询-响应

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
try {
  await client.start();

  const session = await client.createSession({ model: "gpt-5" });
  try {
    await new Promise<void>((resolve) => {
      session.on((event) => {
        if (event.type === "assistant.message") {
          console.log(event.data.content);
        } else if (event.type === "session.idle") {
          resolve();
        }
      });

      session.send({ prompt: "2+2 是多少？" });
    });
  } finally {
    await session.destroy();
  }
} finally {
  await client.stop();
}
```

### 多轮对话

```typescript
const session = await client.createSession();

async function sendAndWait(prompt: string): Promise<void> {
  await new Promise<void>((resolve, reject) => {
    const unsubscribe = session.on((event) => {
      if (event.type === "assistant.message") {
        console.log(event.data.content);
      } else if (event.type === "session.idle") {
        unsubscribe();
        resolve();
      } else if (event.type === "session.error") {
        unsubscribe();
        reject(new Error(event.data.message));
      }
    });

    session.send({ prompt });
  });
}

await sendAndWait("法国的首都是哪里？");
await sendAndWait("它的总人口是多少？");
```

### sendAndWait 辅助函数

```typescript
// 使用内置的 sendAndWait 实现更简单的同步交互
const response = await session.sendAndWait({ prompt: "2+2 是多少？" }, 60000);

if (response) {
  console.log(response.data.content);
}
```

### 带类型安全参数的工具

```typescript
import { z } from "zod";
import { defineTool } from "@github/copilot-sdk";

interface UserInfo {
  id: string;
  name: string;
  email: string;
  role: string;
}

const session = await client.createSession({
  tools: [
    defineTool({
      name: "get_user",
      description: "获取用户信息",
      parameters: z.object({
        userId: z.string().describe("用户 ID"),
      }),
      handler: async (args): Promise<UserInfo> => {
        return {
          id: args.userId,
          name: "John Doe",
          email: "john@example.com",
          role: "开发者",
        };
      },
    }),
  ],
});
```

### 带进度的流式响应

```typescript
let currentMessage = "";

const unsubscribe = session.on((event) => {
  if (event.type === "assistant.message.delta") {
    currentMessage += event.data.deltaContent;
    process.stdout.write(event.data.deltaContent);
  } else if (event.type === "assistant.message") {
    console.log("\n\n=== 完成 ===");
    console.log(`总长度: ${event.data.content.length} 个字符`);
  } else if (event.type === "session.idle") {
    unsubscribe();
  }
});

await session.send({ prompt: "写一个长故事" });
```

### 错误恢复

```typescript
session.on((event) => {
  if (event.type === "session.error") {
    console.error("会话错误:", event.data.message);
    // 可选地重试或处理错误
  }
});

try {
  await session.send({ prompt: "危险操作" });
} catch (error) {
  // 处理发送错误
  console.error("发送失败:", error);
}
```

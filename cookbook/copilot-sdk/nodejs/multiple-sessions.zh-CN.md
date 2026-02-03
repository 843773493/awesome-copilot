# 处理多个会话

同时管理多个独立的对话会话。

> **可运行示例：** [recipe/multiple-sessions.ts](recipe/multiple-sessions.ts)
>
> ```bash
> cd recipe && npm install
> npx tsx multiple-sessions.ts
> # 或：npm run multiple-sessions
> ```

## 示例场景

您需要并行运行多个对话会话，每个会话都有自己的上下文和历史记录。

## Node.js

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();

// 创建多个独立的会话
const session1 = await client.createSession({ model: "gpt-5" });
const session2 = await client.createSession({ model: "gpt-5" });
const session3 = await client.createSession({ model: "claude-sonnet-4.5" });

// 每个会话维护自己的对话历史记录
await session1.sendAndWait({ prompt: "您正在帮助处理一个Python项目" });
await session2.sendAndWait({ prompt: "您正在帮助处理一个TypeScript项目" });
await session3.sendAndWait({ prompt: "您正在帮助处理一个Go项目" });

// 后续消息保持在各自的上下文中
await session1.sendAndWait({ prompt: "如何创建虚拟环境？" });
await session2.sendAndWait({ prompt: "如何设置tsconfig？" });
await session3.sendAndWait({ prompt: "如何初始化一个模块？" });

// 清理所有会话
await session1.destroy();
await session2.destroy();
await session3.destroy();
await client.stop();
```

## 自定义会话ID

使用自定义ID以便于追踪：

```typescript
const session = await client.createSession({
    sessionId: "user-123-chat",
    model: "gpt-5",
});

console.log(session.sessionId); // "user-123-chat"
```

## 列出会话

```typescript
const sessions = await client.listSessions();
console.log(sessions);
// [{ sessionId: "user-123-chat", ... }, ...]
```

## 删除会话

```typescript
// 删除特定会话
await client.deleteSession("user-123-chat");
```

## 使用场景

- **多用户应用**：每个用户一个会话
- **多任务工作流**：为不同的任务创建独立会话
- **A/B测试**：比较不同模型的响应结果

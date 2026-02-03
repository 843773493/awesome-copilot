# 会话持久化与恢复

在应用程序重启时保存和恢复会话。

## 示例场景

您希望用户在关闭并重新打开应用程序后仍能继续之前的对话。

> **可运行示例：** [recipe/persisting-sessions.ts](recipe/persisting-sessions.ts)
>
> ```bash
> cd recipe && npm install
> npx tsx persisting-sessions.ts
> # 或者: npm run persisting-sessions
> ```

### 使用自定义 ID 创建会话

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();

// 使用一个可记忆的 ID 创建会话
const session = await client.createSession({
    sessionId: "user-123-conversation",
    model: "gpt-5",
});

await session.sendAndWait({ prompt: "让我们讨论 TypeScript 泛型" });

// 会话 ID 被保留
console.log(session.sessionId); // "user-123-conversation"

// 销毁会话但保留磁盘上的数据
await session.destroy();
await client.stop();
```

### 恢复会话

```typescript
const client = new CopilotClient();
await client.start();

// 恢复之前的会话
const session = await client.resumeSession("user-123-conversation");

// 恢复之前的上下文
await session.sendAndWait({ prompt: "我们之前在讨论什么？" });
// AI 会记住 TypeScript 泛型的讨论

await session.destroy();
await client.stop();
```

### 列出可用会话

```typescript
const sessions = await client.listSessions();
console.log(sessions);
// [
//   { sessionId: "user-123-conversation", ... },
//   { sessionId: "user-456-conversation", ... },
// ]
```

### 永久删除会话

```typescript
// 从磁盘中移除会话及其所有数据
await client.deleteSession("user-123-conversation");
```

## 获取会话历史记录

检索会话中的所有消息：

```typescript
const messages = await session.getMessages();
for (const msg of messages) {
    console.log(`[${msg.type}]`, msg.data);
}
```

## 最佳实践

1. **使用有意义的会话ID**：在会话ID中包含用户ID或上下文信息
2. **处理缺失的会话**：在恢复会话前检查会话是否存在
3. **清理旧会话**：定期删除不再需要的会话

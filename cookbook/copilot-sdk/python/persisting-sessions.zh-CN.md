# 会话持久化与恢复

在应用程序重启时保存和恢复对话会话。

## 示例场景

您希望用户在关闭并重新打开您的应用程序后仍能继续对话。

> **可运行示例：** [recipe/persisting_sessions.py](recipe/persisting_sessions.py)
>
> ```bash
> cd recipe && pip install -r requirements.txt
> python persisting_sessions.py
> ```

### 使用自定义ID创建会话

```python
import asyncio
from copilot import CopilotClient, SessionConfig, MessageOptions

async def main():
    client = CopilotClient()
    await client.start()

    # 使用可记忆的ID创建会话
    session = await client.create_session(SessionConfig(
        session_id="user-123-conversation",
        model="gpt-5",
    ))

    await session.send_and_wait(MessageOptions(prompt="让我们讨论TypeScript泛型"))

    # 会话ID保持不变
    print(session.session_id)  # "user-123-conversation"

    # 销毁会话但保留磁盘上的数据
    await session.destroy()
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### 恢复会话

```python
client = CopilotClient()
await client.start()

# 恢复之前的会话
session = await client.resume_session("user-123-conversation")

# 恢复之前的上下文
await session.send_and_wait(MessageOptions(prompt="我们之前在讨论什么？"))

await session.destroy()
await client.stop()
```

### 列出可用会话

```python
sessions = await client.list_sessions()
for s in sessions:
    print("会话:", s.session_id)
```

### 永久删除会话

```python
# 从磁盘中移除会话及其所有数据
await client.delete_session("user-123-conversation")
```

### 获取会话历史记录

```python
messages = await session.get_messages()
for msg in messages:
    print(f"[{msg.type}] {msg.data.content}")
```

## 最佳实践

1. **使用有意义的会话ID**：在会话ID中包含用户ID或上下文信息
2. **处理缺失的会话**：在恢复会话前检查会话是否存在
3. **清理旧会话**：定期删除不再需要的会话

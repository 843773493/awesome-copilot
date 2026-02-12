# 处理多个会话

同时管理多个独立的对话会话。

> **可运行示例：** [recipe/multiple_sessions.py](recipe/multiple_sessions.py)
>
> ```bash
> cd recipe && pip install -r requirements.txt
> python multiple_sessions.py
> ```

## 示例场景

您需要并行运行多个对话，每个对话都有自己的上下文和历史记录。

## Python

```python
import asyncio
from copilot import CopilotClient, SessionConfig, MessageOptions

async def main():
    client = CopilotClient()
    await client.start()

    # 创建多个独立的会话
    session1 = await client.create_session(SessionConfig(model="gpt-5"))
    session2 = await client.create_session(SessionConfig(model="gpt-5"))
    session3 = await client.create_session(SessionConfig(model="claude-sonnet-4.5"))

    # 每个会话维护自己的对话历史记录
    await session1.send(MessageOptions(prompt="You are helping with a Python project"))
    await session2.send(MessageOptions(prompt="You are helping with a TypeScript project"))
    await session3.send(MessageOptions(prompt="You are helping with a Go project"))

    # 后续消息保持在各自的上下文中
    await session1.send(MessageOptions(prompt="How do I create a virtual environment?"))
    await session2.send(MessageOptions(prompt="How do I set up tsconfig?"))
    await session3.send(MessageOptions(prompt="How do I initialize a module?"))

    # 清理所有会话
    await session1.destroy()
    await session2.destroy()
    await session3.destroy()
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## 自定义会话ID

使用自定义ID以便更轻松地跟踪：

```python
session = await client.create_session(SessionConfig(
    session_id="user-123-chat",
    model="gpt-5"
))

print(session.session_id)  # "user-123-chat"
```

## 列出会话

```python
sessions = await client.list_sessions()
for session_info in sessions:
    print(f"会话: {session_info.session_id}")
```

## 删除会话

```python
# 删除特定会话
await client.delete_session("user-123-chat")
```

## 用例

- **多用户应用**：每个用户一个会话
- **多任务工作流**：为不同的任务分配独立会话
- **A/B测试**：比较不同模型的响应

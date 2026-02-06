# 处理多个会话

同时管理多个独立的对话。

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
from copilot import CopilotClient

client = CopilotClient()
client.start()

# 创建多个独立的会话
session1 = client.create_session(model="gpt-5")
session2 = client.create_session(model="gpt-5")
session3 = client.create_session(model="claude-sonnet-4.5")

# 每个会话维护自己的对话历史
session1.send(prompt="您正在帮助处理一个Python项目")
session2.send(prompt="您正在帮助处理一个TypeScript项目")
session3.send(prompt="您正在帮助处理一个Go项目")

# 后续消息保持在各自的上下文中
session1.send(prompt="如何创建虚拟环境？")
session2.send(prompt="如何设置tsconfig？")
session3.send(prompt="如何初始化一个模块？")

# 清理所有会话
session1.destroy()
session2.destroy()
session3.destroy()
client.stop()
```

## 自定义会话ID

使用自定义ID以便于追踪：

```python
session = client.create_session(
    session_id="user-123-chat",
    model="gpt-5"
)

print(session.session_id)  # "user-123-chat"
```

## 列出会话

```python
sessions = client.list_sessions()
for session_info in sessions:
    print(f"会话: {session_info['sessionId']}")
```

## 删除会话

```python
# 删除特定会话
client.delete_session("user-123-chat")
```

## 使用场景

- **多用户应用**：每个用户对应一个会话
- **多任务工作流**：为不同的任务分配独立会话
- **A/B测试**：比较不同模型的响应结果

# 会话持久化与恢复

在应用程序重启时保存和恢复会话对话。

## 示例场景

您希望用户在关闭并重新打开应用程序后仍能继续之前的对话。

> **可运行示例：** [recipe/persisting_sessions.py](recipe/persisting_sessions.py)
>
> ```bash
> cd recipe && pip install -r requirements.txt
> python persisting_sessions.py
> ```

### 使用自定义ID创建会话

```python
from copilot import CopilotClient

client = CopilotClient()
client.start()

# 使用有意义的ID创建会话
session = client.create_session(
    session_id="user-123-conversation",
    model="gpt-5",
)

session.send(prompt="让我们讨论TypeScript泛型")

# 会话ID保持不变
print(session.session_id)  # "user-123-conversation"

# 销毁会话但保留磁盘上的数据
session.destroy()
client.stop()
```

### 恢复会话

```python
client = CopilotClient()
client.start()

# 恢复之前的会话
session = client.resume_session("user-123-conversation")

# 恢复之前的上下文
session.send(prompt="我们之前在讨论什么？")

session.destroy()
client.stop()
```

### 查看可用的会话

```python
sessions = client.list_sessions()
for s in sessions:
    print("会话:", s["sessionId"])
```

### 永久删除会话

```python
# 删除会话及其所有数据
client.delete_session("user-123-conversation")
```

### 获取会话历史记录

```python
messages = session.get_messages()
for msg in messages:
    print(f"[{msg['type']}] {msg['data']}")
```

## 最佳实践

1. **使用有意义的会话ID**：在会话ID中包含用户ID或上下文信息  
2. **处理缺失的会话**：在恢复会话前检查会话是否存在  
3. **清理旧会话**：定期删除不再需要的会话

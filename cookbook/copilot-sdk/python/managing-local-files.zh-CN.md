# 按元数据分组文件

使用 Copilot 根据文件的元数据智能整理文件夹中的文件。

> **可运行示例：** [recipe/managing_local_files.py](recipe/managing_local_files.py)
>
> ```bash
> cd recipe && pip install -r requirements.txt
> python managing_local_files.py
> ```

## 示例场景

你有一个包含大量文件的文件夹，希望根据元数据（如文件类型、创建日期、大小或其他属性）将它们整理到子文件夹中。Copilot 可以分析文件并建议或执行分组策略。

## 示例代码

```python
import asyncio
import os
from copilot import (
    CopilotClient, SessionConfig, MessageOptions,
    SessionEvent, SessionEventType,
)

async def main():
    # 创建并启动客户端
    client = CopilotClient()
    await client.start()

    # 创建会话
    session = await client.create_session(SessionConfig(model="gpt-5"))

    done = asyncio.Event()

    # 事件处理程序
    def handle_event(event: SessionEvent):
        if event.type == SessionEventType.ASSISTANT_MESSAGE:
            print(f"\nCopilot: {event.data.content}")
        elif event.type == SessionEventType.TOOL_EXECUTION_START:
            print(f"  → 正在运行: {event.data.tool_name}")
        elif event.type == SessionEventType.TOOL_EXECUTION_COMPLETE:
            print(f"  ✓ 已完成: {event.data.tool_call_id}")
        elif event.type.value == "session.idle":
            done.set()

    session.on(handle_event)

    # 请求 Copilot 整理文件
    target_folder = os.path.expanduser("~/Downloads")

    await session.send(MessageOptions(prompt=f"""
分析 "{target_folder}" 中的文件并整理到子文件夹中。

1. 首先，列出所有文件及其元数据
2. 预览按文件扩展名分组的情况
3. 创建适当的子文件夹（例如："images"、"documents"、"videos"）
4. 将每个文件移动到对应的子文件夹中

在移动任何文件前请确认。
"""))

    await done.wait()

    await session.destroy()
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## 分组策略

### 按文件扩展名分组

```python
# 分组示例：
# images/   -> .jpg, .png, .gif
# documents/ -> .pdf, .docx, .txt
# videos/   -> .mp4, .avi, .mov
```

### 按创建日期分组

```python
# 分组示例：
# 2024-01/ -> 2024年1月创建的文件
# 2024-02/ -> 2024年2月创建的文件
```

### 按文件大小分组

```python
# 分组示例：
# tiny-under-1kb/
# small-under-1mb/
# medium-under-100mb/
# large-over-100mb/
```

## 干运行模式

为了安全起见，你可以要求 Copilot 仅预览更改而不实际移动文件：

```python
await session.send(MessageOptions(prompt=f"""
分析 "{target_folder}" 中的文件，并向我展示你如何根据文件类型进行整理
的计划。不要移动任何文件，只需显示整理方案。
"""))
```

## 基于 AI 分析的自定义分组

让 Copilot 根据文件内容确定最佳分组方式：

```python
await session.send(MessageOptions(prompt=f"""
查看 "{target_folder}" 中的文件，并建议一个合理的组织方式。
考虑以下因素：
- 文件名及其可能包含的内容
- 文件类型及其典型用途
- 可能表示项目或事件的日期模式

提出具有描述性和实用性的文件夹名称。
"""))
```

## 安全注意事项

1. **移动前确认**：在执行移动操作前，请要求 Copilot 确认
2. **处理重复文件**：考虑如果存在同名文件会发生什么
3. **保留原始文件**：对于重要文件，考虑复制而非移动操作

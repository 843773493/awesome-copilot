# 错误处理模式

在您的 Copilot SDK 应用程序中优雅地处理错误。

> **可运行示例：** [recipe/error_handling.py](recipe/error_handling.py)
>
> ```bash
> cd recipe && pip install -r requirements.txt
> python error_handling.py
> ```

## 示例场景

您需要处理各种错误条件，例如连接失败、超时和无效响应。

## 基础 try-except

```python
import asyncio
from copilot import CopilotClient, SessionConfig, MessageOptions

async def main():
    client = CopilotClient()

    try:
        await client.start()
        session = await client.create_session(SessionConfig(model="gpt-5"))

        response = await session.send_and_wait(MessageOptions(prompt="Hello!"))

        if response:
            print(response.data.content)

        await session.destroy()
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## 处理特定错误类型

```python
try:
    await client.start()
except FileNotFoundError:
    print("未找到 Copilot CLI。请先安装它。")
except ConnectionError:
    print("无法连接到 Copilot CLI 服务器。")
except Exception as e:
    print(f"意外错误: {e}")
```

## 超时处理

```python
session = await client.create_session(SessionConfig(model="gpt-5"))

try:
    # send_and_wait 接受一个可选的超时时间（秒）
    response = await session.send_and_wait(
        MessageOptions(prompt="复杂问题..."),
        timeout=30.0
    )
    print("已收到响应")
except TimeoutError:
    print("请求超时")
```

## 中止请求

```python
session = await client.create_session(SessionConfig(model="gpt-5"))

# 开始请求（非阻塞发送）
await session.send(MessageOptions(prompt="写一个很长的故事..."))

# 在某些条件后中止请求
await asyncio.sleep(5)
await session.abort()
print("请求已中止")
```

## 优雅关闭

```python
import signal
import sys

def signal_handler(sig, frame):
    print("\n正在关闭...")
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(client.stop())
    except RuntimeError:
        asyncio.run(client.stop())
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
```

## 最佳实践

1. **始终进行清理**：使用 try-finally 确保调用 `await client.stop()`
2. **处理连接错误**：CLI 可能未安装或未运行
3. **设置适当的超时时间**：在 `send_and_wait()` 中使用 `timeout` 参数
4. **记录错误**：捕获错误详情以供调试

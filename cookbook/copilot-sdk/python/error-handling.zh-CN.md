# 错误处理模式

在您的 Copilot SDK 应用程序中优雅地处理错误。

> **可运行示例：** [recipe/error_handling.py](recipe/error_handling.py)
>
> ```bash
> cd recipe && pip install -r requirements.txt
> python error_handling.py
> ```

## 示例场景

您需要处理各种错误情况，例如连接失败、超时和无效响应。

## 基础 try-except

```python
from copilot import CopilotClient

client = CopilotClient()

try:
    client.start()
    session = client.create_session(model="gpt-5")

    response = None
    def handle_message(event):
        nonlocal response
        if event["type"] == "assistant.message":
            response = event["data"]["content"]

    session.on(handle_message)
    session.send(prompt="Hello!")
    session.wait_for_idle()

    if response:
        print(response)

    session.destroy()
except Exception as e:
    print(f"错误: {e}")
finally:
    client.stop()
```

## 处理特定错误类型

```python
import subprocess

try:
    client.start()
except FileNotFoundError:
    print("未找到 Copilot CLI。请先安装它。")
except ConnectionError:
    print("无法连接到 Copilot CLI 服务器。")
except Exception as e:
    print(f"意外错误: {e}")
```

## 超时处理

```python
import signal
from contextlib import contextmanager

@contextmanager
def timeout(seconds):
    def timeout_handler(signum, frame):
        raise TimeoutError("请求超时")

    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

session = client.create_session(model="gpt-5")

try:
    session.send(prompt="复杂问题...")

    # 带超时等待 (30 秒)
    with timeout(30):
        session.wait_for_idle()

    print("已收到响应")
except TimeoutError:
    print("请求超时")
```

## 中止请求

```python
import threading

session = client.create_session(model="gpt-5")

# 启动一个请求
session.send(prompt="写一个很长的故事...")

# 在某些条件后中止它
def abort_later():
    import time
    time.sleep(5)
    session.abort()
    print("请求已中止")

threading.Thread(target=abort_later).start()
```

## 优雅关闭

```python
import signal
import sys

def signal_handler(sig, frame):
    print("\n正在关闭...")
    errors = client.stop()
    if errors:
        print(f"清理错误: {errors}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
```

## 使用上下文管理器进行自动清理

```python
from copilot import CopilotClient

with CopilotClient() as client:
    client.start()
    session = client.create_session(model="gpt-5")

    # ... 执行工作 ...

    # 退出上下文时会自动调用 client.stop()
``` 

## 最佳实践

1. **始终进行清理**：使用 try-finally 或上下文管理器确保调用 `stop()`  
2. **处理连接错误**：CLI 可能未安装或未运行  
3. **设置适当的超时**：长时间运行的请求应设置超时  
4. **记录错误**：捕获错误详情以供调试

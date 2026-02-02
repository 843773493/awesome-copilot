---
applyTo: "**.py, pyproject.toml, setup.py"
description: "此文件提供使用 GitHub Copilot SDK 构建 Python 应用的指导。"
name: "GitHub Copilot SDK Python 指南"
---

## 核心原则

- SDK 处于技术预览阶段，可能会有破坏性变更
- 需要 Python 3.9 或更高版本
- 需要安装并配置 GitHub Copilot CLI
- 全程使用 async/await 模式（asyncio）
- 支持异步上下文管理器和手动生命周期管理
- 提供类型提示以增强 IDE 支持

## 安装

始终通过 pip 安装：

```bash
pip install copilot-sdk
# 或使用 poetry
poetry add copilot-sdk
# 或使用 uv
uv add copilot-sdk
```

## 客户端初始化

### 基础客户端设置

```python
from copilot import CopilotClient
import asyncio

async def main():
    async with CopilotClient() as client:
        # 使用 client...
        pass

asyncio.run(main())
```

### 客户端配置选项

创建 CopilotClient 时使用包含以下键的字典：

- `cli_path` - CLI 可执行文件路径（默认："copilot" 从 PATH 或 COPILOT_CLI_PATH 环境变量获取）
- `cli_url` - 现有 CLI 服务器的 URL（例如："localhost:8080"）。提供此参数时，客户端不会启动进程
- `port` - 服务器端口（默认：0 表示随机）
- `use_stdio` - 使用 stdio 传输而非 TCP（默认：True）
- `log_level` - 日志级别（默认："info"）
- `auto_start` - 自动启动服务器（默认：True）
- `auto_restart` - 在崩溃时自动重启（默认：True）
- `cwd` - CLI 进程的工作目录（默认：os.getcwd()）
- `env` - CLI 进程的环境变量（字典）

### 手动服务器控制

对于显式控制：

```python
from copilot import CopilotClient
import asyncio

async def main():
    client = CopilotClient({"auto_start": False})
    await client.start()
    # 使用 client...
    await client.stop()

asyncio.run(main())
```

当 `stop()` 响应过慢时，使用 `force_stop()`。

## 会话管理

### 创建会话

使用字典作为 SessionConfig：

```python
session = await client.create_session({
    "model": "gpt-5",
    "streaming": True,
    "tools": [...],
    "system_message": { ... },
    "available_tools": ["tool1", "tool2"],
    "excluded_tools": ["tool3"],
    "provider": { ... }
})
```

### 会话配置选项

- `session_id` - 自定义会话 ID（字符串）
- `model` - 模型名称（"gpt-5", "claude-sonnet-4.5" 等）
- `tools` - 暴露给 CLI 的自定义工具（列表[Tool]）
- `system_message` - 系统消息自定义（字典）
- `available_tools` - 允许的工具名称白名单（列表[str]）
- `excluded_tools` - 工具名称黑名单（列表[str]）
- `provider` - 自定义 API 提供商配置（BYOK）（ProviderConfig）
- `streaming` - 启用流式响应块（布尔值）
- `mcp_servers` - MCP 服务器配置（列表）
- `custom_agents` - 自定义代理配置（列表）
- `config_dir` - 配置目录覆盖（字符串）
- `skill_directories` - 技能目录（列表[str]）
- `disabled_skills` - 禁用的技能（列表[str]）
- `on_permission_request` - 权限请求处理程序（可调用对象）

### 恢复会话

```python
session = await client.resume_session("session-id", {
    "tools": [my_new_tool]
})
```

### 会话操作

- `session.session_id` - 获取会话标识符（字符串）
- `await session.send({"prompt": "...", "attachments": [...]})` - 发送消息，返回字符串（消息 ID）
- `await session.send_and_wait({"prompt": "..."}, timeout=60.0)` - 发送并等待空闲，返回 SessionEvent | None
- `await session.abort()` - 中止当前处理
- `await session.get_messages()` - 获取所有事件/消息，返回列表[SessionEvent]
- `await session.destroy()` - 清理会话

## 事件处理

### 事件订阅模式

始终使用 asyncio 事件或未来对象等待会话事件：

```python
import asyncio

done = asyncio.Event()

def handler(event):
    if event.type == "assistant.message":
        print(event.data.content)
    elif event.type == "session.idle":
        done.set()

session.on(handler)
await session.send({"prompt": "..."})
await done.wait()
```

### 取消事件订阅

`on()` 方法返回一个用于取消订阅的函数：

```python
unsubscribe = session.on(lambda event: print(event.type))
# 后续...
unsubscribe()
```

### 事件类型

通过属性访问进行事件类型检查：

```python
def handler(event):
    if event.type == "user.message":
        # 处理用户消息
        pass
    elif event.type == "assistant.message":
        print(event.data.content)
    elif event.type == "tool.executionStart":
        # 工具执行开始
        pass
    elif event.type == "tool.executionComplete":
        # 工具执行完成
        pass
    elif event.type == "session.start":
        # 会话开始
        pass
    elif event.type == "session.idle":
        # 会话空闲（处理完成）
        pass
    elif event.type == "session.error":
        print(f"错误: {event.data.message}")

session.on(handler)
```

## 流式响应

### 启用流式响应

在 SessionConfig 中设置 `streaming: True`：

```python
session = await client.create_session({
    "model": "gpt-5",
    "streaming": True
})
```

### 处理流式事件

处理增量事件（分块）和最终事件：

```python
import asyncio

current_message = []
done = asyncio.Event()

def handler(event):
    if event.type == "assistant.message.delta":
        current_message.append(event.data.delta_content)
        print(event.data.delta_content, end="", flush=True)
    elif event.type == "assistant.message":
        print(f"\n\n=== 完成 ===")
        print(f"总长度: {len(event.data.content)} 个字符")
    elif event.type == "session.idle":
        done.set()

unsubscribe = session.on(handler)
await session.send({"prompt": "写一个长故事"})
await done.wait()
unsubscribe()
```

### 流式响应注意事项

注意：最终事件（`assistant.message`, `assistant.reasoning`）无论流式设置如何始终发送。

## 自定义工具

### 使用 define_tool 定义工具

使用 `define_tool` 进行工具定义：

```python
from copilot import define_tool

async def fetch_issue(issue_id: str):
    # 从跟踪器获取问题
    return {"id": issue_id, "status": "open"}

session = await client.create_session({
    "model": "gpt-5",
    "tools": [
        define_tool(
            name="lookup_issue",
            description="从跟踪器获取问题详情",
            parameters={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "问题 ID"}
                },
                "required": ["id"]
            },
            handler=lambda args, inv: fetch_issue(args["id"])
        )
    ]
})
```

### 使用 Pydantic 进行参数校验

SDK 与 Pydantic 模型配合良好：

```python
from pydantic import BaseModel, Field

class WeatherArgs(BaseModel):
    location: str = Field(description="城市名称")
    units: str = Field(default="华氏度", description="温度单位")

async def get_weather(args: WeatherArgs, inv):
    return {"temperature": 72, "units": args.units}

session = await client.create_session({
    "tools": [
        define_tool(
            name="get_weather",
            description="获取指定位置的天气",
            parameters=WeatherArgs.model_json_schema(),
            handler=lambda args, inv: get_weather(WeatherArgs(**args), inv)
        )
    ]
})
```

### 工具返回类型

- 返回任何 JSON 可序列化值（自动包装）
- 或返回 ToolResult 字典以完全控制：

```python
{
    "text_result_for_llm": str,  # 显示给 LLM 的结果
    "result_type": "success" | "failure",
    "error": str,  # 可选：内部错误（不显示给 LLM）
    "tool_telemetry": dict  # 可选：遥测数据
}
```

### 工具处理函数签名

工具处理函数接收两个参数：

- `args`（字典）- LLM 传递的工具参数
- `invocation`（ToolInvocation）- 调用元数据
  - `invocation.session_id` - 会话 ID
  - `invocation.tool_call_id` - 工具调用 ID
  - `invocation.tool_name` - 工具名称
  - `invocation.arguments` - 与 args 参数相同

### 工具执行流程

当 Copilot 调用工具时，客户端会自动：

1. 运行您的处理函数
2. 序列化返回值
3. 向 CLI 响应

## 系统消息自定义

### 追加模式（默认 - 保留安全护栏）

```python
session = await client.create_session({
    "model": "gpt-5",
    "system_message": {
        "mode": "append",
        "content": """
<工作流规则>
- 始终检查安全漏洞
- 适用时建议性能优化
</工作流规则>
"""
    }
})
```

### 替换模式（完全控制 - 移除安全护栏）

```python
session = await client.create_session({
    "model": "gpt-5",
    "system_message": {
        "mode": "replace",
        "content": "你是一个有帮助的助手。"
    }
})
```

## 文件附件

将文件附加到消息中：

```python
await session.send({
    "prompt": "分析此文件",
    "attachments": [
        {
            "type": "file",
            "path": "/path/to/file.py",
            "display_name": "我的文件"
        }
    ]
})
```

## 消息传递模式

在消息选项中使用 `mode` 键：

- `"enqueue"` - 将消息排队等待处理
- `"immediate"` - 立即处理消息

```python
await session.send({
    "prompt": "...",
    "mode": "enqueue"
})
```

## 多个会话

会话是独立的，可以并发运行：

```python
session1 = await client.create_session({"model": "gpt-5"})
session2 = await client.create_session({"model": "claude-sonnet-4.5"})

await asyncio.gather(
    session1.send({"prompt": "会话 1 中的问候"}),
    session2.send({"prompt": "会话 2 中的问候"})
)
```

## 自带密钥（BYOK）

使用 `provider` 配置自定义 API 提供商：

```python
session = await client.create_session({
    "provider": {
        "type": "openai",
        "base_url": "https://api.openai.com/v1",
        "api_key": "您的 API 密钥"
    }
})
```

## 会话生命周期管理

### 列出会话

```python
sessions = await client.list_sessions()
for metadata in sessions:
    print(f"{metadata.session_id}: {metadata.summary}")
```

### 删除会话

```python
await client.delete_session(session_id)
```

### 获取最后会话 ID

```python
last_id = await client.get_last_session_id()
if last_id:
    session = await client.resume_session(last_id)
```

### 检查连接状态

```python
state = client.get_state()
# 返回: "断开连接" | "连接中" | "已连接" | "错误"
```

## 错误处理

### 标准异常处理

```python
try:
    session = await client.create_session()
    await session.send({"prompt": "你好"})
except Exception as e:
    print(f"错误: {e}")
```

### 会话错误事件

监控 `session.error` 事件类型以处理运行时错误：

```python
def handler(event):
    if event.type == "session.error":
        print(f"会话错误: {event.data.message}")
        # 可选：重试或处理错误

session.on(handler)

try:
    await session.send({"prompt": "高风险操作"})
except Exception as e:
    # 处理发送错误
    print(f"发送失败: {e}")
```

### 使用 TypedDict 实现类型安全

```python
from typing import TypedDict, List

class MessageOptions(TypedDict, total=False):
    prompt: str
    attachments: List[dict]
    mode: str

class SessionConfig(TypedDict, total=False):
    model: str
    streaming: bool
    tools: List

# 使用类型提示
options: MessageOptions = {
    "prompt": "你好",
    "mode": "enqueue"
}
await session.send(options)

config: SessionConfig = {
    "model": "gpt-5",
    "streaming": True
}
session = await client.create_session(config)
```

### 流式响应的异步生成器

```python
from typing import AsyncGenerator

async def stream_response(session, prompt: str) -> AsyncGenerator[str, None]:
    """将响应分块作为异步生成器流式传输。"""
    queue = asyncio.Queue()
    done = asyncio.Event()

    def handler(event):
        if event.type == "assistant.message.delta":
            queue.put_nowait(event.data.delta_content)
        elif event.type == "session.idle":
            done.set()

    unsubscribe = session.on(handler)
    await session.send({"prompt": prompt})

    while not done.is_set():
        try:
            chunk = await asyncio.wait_for(queue.get(), timeout=0.1)
            yield chunk
        except asyncio.TimeoutError:
            continue

    # 清空剩余项
    while not queue.empty():
        yield queue.get_nowait()

    unsubscribe()

# 使用示例
async for chunk in stream_response(session, "给我讲个故事"):
    print(chunk, end="", flush=True)
```

### 工具装饰器模式

```python
from typing import Callable, Any
from copilot import define_tool

def copilot_tool(
    name: str,
    description: str,
    parameters: dict
) -> Callable:
    """将函数转换为 Copilot 工具的装饰器。"""
    def decorator(func: Callable) -> Any:
        return define_tool(
            name=name,
            description=description,
            parameters=parameters,
            handler=lambda args, inv: func(**args)
        )
    return decorator

@copilot_tool(
    name="计算",
    description="执行计算",
    parameters={
        "type": "object",
        "properties": {
            "表达式": {"type": "string", "description": "数学表达式"}
        },
        "required": ["表达式"]
    }
)
def 计算(表达式: str) -> float:
    return eval(表达式)

session = await client.create_session({"tools": [计算]})
```

## Python 特定功能

### 异步上下文管理器协议

SDK 实现了 `__aenter__` 和 `__aexit__`：

```python
class CopilotClient:
    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
        return False

class CopilotSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.destroy()
        return False
```

### 数据类支持

事件数据可通过属性直接访问：

```python
def handler(event):
    # 直接访问事件属性
    print(event.type)
    print(event.data.content)  # 对于 assistant.message
    print(event.data.delta_content)  # 对于 assistant.message.delta
```



---
description: '使用 Python SDK 构建 Model Context Protocol (MCP) 服务器的说明'
applyTo: '**/*.py, **/pyproject.toml, **/requirements.txt'
---

# Python MCP 服务器开发

## 指导说明

- 使用 **uv** 进行项目管理：`uv init mcp-server-demo` 和 `uv add "mcp[cli]"`
- 从 `mcp.server.fastmcp` 导入 FastMCP：`from mcp.server.fastmcp import FastMCP`
- 使用 `@mcp.tool()`、`@mcp.resource()` 和 `@mcp.prompt()` 装饰器进行注册
- 类型提示是必需的 - 它们用于模式生成和验证
- 使用 Pydantic 模型、TypedDicts 或 dataclasses 来处理结构化输出
- 工具在返回类型兼容时会自动返回结构化输出
- 对于 stdio 传输，使用 `mcp.run()` 或 `mcp.run(transport="stdio")`
- 对于 HTTP 服务器，使用 `mcp.run(transport="streamable-http")` 或挂载到 Starlette/FastAPI
- 在工具/资源中使用 `Context` 参数来访问 MCP 功能：`ctx: Context`
- 使用 `await ctx.debug()`、`await ctx.info()`、`await ctx.warning()`、`await ctx.error()` 发送日志
- 使用 `await ctx.report_progress(progress, total, message)` 报告进度
- 使用 `await ctx.elicit(message, schema)` 请求用户输入
- 使用 `await ctx.session.create_message(messages, max_tokens)` 进行 LLM 采样
- 使用 `Icon(src="path", mimeType="image/png")` 配置图标，用于服务器、工具、资源和提示
- 使用 `Image` 类进行自动图像处理：`return Image(data=bytes, format="png")`
- 使用 URI 模式定义资源模板：`@mcp.resource("greeting://{name}")`
- 通过接受部分值并返回建议来实现补全支持
- 使用生命周期上下文管理器进行启动/关闭操作，以管理共享资源
- 通过 `ctx.request_context.lifespan_context` 在工具中访问生命周期上下文
- 对于无状态 HTTP 服务器，在 FastMCP 初始化时设置 `stateless_http=True`
- 启用 JSON 响应以支持现代客户端：`json_response=True`
- 使用以下命令测试服务器：`uv run mcp dev server.py`（Inspector）或 `uv run mcp install server.py`（Claude Desktop）
- 在 Starlette 中挂载多个服务器，使用不同的路径：`Mount("/path", mcp.streamable_http_app())`
- 为浏览器客户端配置 CORS：暴露 `Mcp-Session-Id` 头部
- 当 FastMCP 不足以满足需求时，使用低级 Server 类以获得最大控制权

## 最佳实践

- 始终使用类型提示 - 它们驱动模式生成和验证
- 返回 Pydantic 模型或 TypedDicts 以实现结构化工具输出
- 保持工具函数专注于单一职责
- 提供清晰的文档字符串 - 它们会成为工具描述
- 使用带有类型提示的描述性参数名称
- 使用 Pydantic Field 描述验证输入
- 使用 try-except 块实现适当的错误处理
- 对 I/O 绑定操作使用异步函数
- 在生命周期上下文管理器中清理资源
- 向 stderr 输出日志，以避免干扰 stdio 传输（当使用 stdio 时）
- 使用环境变量进行配置
- 在 LLM 集成之前独立测试工具
- 暴露文件系统或网络访问时考虑安全性
- 使用结构化输出处理机器可读数据
- 为向后兼容性同时提供内容和结构化数据

## 常见模式

### 基础服务器设置（stdio）
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("我的服务器")

@mcp.tool()
def calculate(a: int, b: int, op: str) -> int:
    """执行计算"""
    if op == "add":
        return a + b
    return a - b

if __name__ == "__main__":
    mcp.run()  # 默认使用 stdio
```

### HTTP 服务器
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("我的 HTTP 服务器")

@mcp.tool()
def hello(name: str = "World") -> str:
    """向某人打招呼"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

### 具有结构化输出的工具
```python
from pydantic import BaseModel, Field

class WeatherData(BaseModel):
    temperature: float = Field(description="摄氏度温度")
    condition: str
    humidity: float

@mcp.tool()
def get_weather(city: str) -> WeatherData:
    """获取某城市的天气信息"""
    return WeatherData(
        temperature=22.5,
        condition="晴朗",
        humidity=65.0
    )
```

### 动态资源
```python
@mcp.resource("users://{user_id}")
def get_user(user_id: str) -> str:
    """获取用户档案数据"""
    return f"用户 {user_id} 的档案数据"
```

### 带有上下文的工具
```python
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

@mcp.tool()
async def process_data(
    data: str, 
    ctx: Context[ServerSession, None]
) -> str:
    """使用日志处理数据"""
    await ctx.info(f"正在处理: {data}")
    await ctx.report_progress(0.5, 1.0, "完成了一半")
    return f"已处理: {data}"
```

### 带有采样的工具
```python
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from mcp.types import SamplingMessage, TextContent

@mcp.tool()
async def summarize(
    text: str,
    ctx: Context[ServerSession, None]
) -> str:
    """使用 LLM 对文本进行摘要"""
    result = await ctx.session.create_message(
        messages=[SamplingMessage(
            role="user",
            content=TextContent(type="text", text=f"摘要: {text}")
        )],
        max_tokens=100
    )
    return result.content.text if result.content.type == "text" else ""
```

### 生命周期管理
```python
from contextlib import asynccontextmanager
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP, Context

@dataclass
class AppContext:
    db: Database

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    db = await Database.connect()
    try:
        yield AppContext(db=db)
    finally:
        await db.disconnect()

mcp = FastMCP("我的应用", lifespan=app_lifespan)

@mcp.tool()
def query(sql: str, ctx: Context) -> str:
    """查询数据库"""
    db = ctx.request_context.lifespan_context.db
    return db.execute(sql)
```

### 带有消息的提示
```python
from mcp.server.fastmcp.prompts import base

@mcp.prompt(title="代码审查")
def review_code(code: str) -> list[base.Message]:
    """创建代码审查提示"""
    return [
        base.UserMessage("请审查以下代码："),
        base.UserMessage(code),
        base.AssistantMessage("我将为您审查代码。")
    ]
```

### 错误处理
```python
@mcp.tool()
async def risky_operation(input: str) -> str:
    """可能失败的操作"""
    try:
        result = await perform_operation(input)
        return f"成功: {result}"
    except Exception as e:
        return f"错误: {str(e)}"
```
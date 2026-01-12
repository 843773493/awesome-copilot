

---
agent: 'agent'
description: '使用工具、资源和正确配置生成一个完整的 Python MCP 服务器项目'
---

# 生成 Python MCP 服务器

创建一个符合以下规格的完整 Model Context Protocol (MCP) 服务器项目：

## 要求

1. **项目结构**：使用 uv 创建一个具有正确结构的新 Python 项目
2. **依赖项**：使用 uv 包含 mcp[cli] 包
3. **传输类型**：选择 stdio（用于本地）或 streamable-http（用于远程）
4. **工具**：创建至少一个有用的工具并包含适当的类型提示
5. **错误处理**：包含全面的错误处理和验证

## 实现细节

### 项目设置
- 使用 `uv init project-name` 初始化项目
- 添加 MCP SDK：`uv add "mcp[cli]"`
- 创建主服务器文件（例如 `server.py`）
- 添加 `.gitignore` 文件用于 Python 项目
- 配置为可直接执行：`if __name__ == "__main__"`

### 服务器配置
- 使用 `mcp.server.fastmcp` 中的 `FastMCP` 类
- 设置服务器名称和可选说明
- 选择传输方式：stdio（默认）或 streamable-http
- 对于 HTTP：可选配置主机、端口和无状态模式

### 工具实现
- 在函数上使用 `@mcp.tool()` 装饰器
- 始终包含类型提示 - 它们会自动生成模式
- 编写清晰的文档字符串 - 它们会成为工具描述
- 使用 Pydantic 模型或 TypedDicts 进行结构化输出
- 支持异步操作以处理 I/O 绑定任务
- 包含适当的错误处理

### 资源/提示设置（可选）
- 使用 `@mcp.resource()` 装饰器添加资源
- 使用 URI 模板为动态资源：`"resource://{param}"`
- 使用 `@mcp.prompt()` 装饰器添加提示
- 从提示返回字符串或 Message 列表

## 需要考虑的示例工具类型
- 数据处理和转换
- 文件系统操作（读取、分析、搜索）
- 外部 API 集成
- 数据库查询
- 文本分析或生成（带抽样）
- 系统信息检索
- 数学或科学计算

## 配置选项
- **对于 stdio 服务器**：
  - 简单的直接执行
  - 使用 `uv run mcp dev server.py` 进行测试
  - 安装到 Claude：`uv run mcp install server.py`
  
- **对于 HTTP 服务器**：
  - 通过环境变量配置端口
  - 无状态模式以实现可扩展性：`stateless_http=True`
  - JSON 响应模式：`json_response=True`
  - 为浏览器客户端配置 CORS
  - 挂载到现有 ASGI 服务器（Starlette/FastAPI）

## 测试指南
- 解释如何运行服务器：
  - stdio：`python server.py` 或 `uv run server.py`
  - HTTP：`python server.py` 然后连接到 `http://localhost:PORT/mcp`
- 使用 MCP 检查器进行测试：`uv run mcp dev server.py`
- 安装到 Claude 桌面：`uv run mcp install server.py`
- 包含示例工具调用
- 添加故障排除提示

## 可考虑的附加功能
- 上下文使用用于日志、进度和通知
- LLM 抽样用于 AI 驱动的工具
- 用户输入引导用于交互式工作流
- 共享资源（数据库、连接）的生命周期管理
- 使用 Pydantic 模型进行结构化输出
- 用于 UI 显示的图标
- 使用 Image 类处理图像
- 支持补全以提高用户体验

## 最佳实践
- 在所有地方使用类型提示 - 它们是必填项
- 在可能的情况下返回结构化数据
- 将日志记录到 stderr（或使用上下文日志）以避免污染 stdout
- 正确清理资源
- 早期验证输入
- 提供清晰的错误信息
- 在 LLM 集成之前独立测试工具

生成一个完整的、生产就绪的 MCP 服务器，具备类型安全、正确的错误处理和全面的文档。
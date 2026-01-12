

---
agent: 'agent'
description: '生成一个完整的 MCP 服务器项目，包含工具、提示和适当的配置'
---

# 生成 C# MCP 服务器

创建一个符合以下规范的完整 Model Context Protocol (MCP) 服务器项目：

## 要求

1. **项目结构**：创建一个新的 C# 控制台应用程序并配置合理的目录结构
2. **NuGet 包**：包含 ModelContextProtocol（预发行版）和 Microsoft.Extensions.Hosting
3. **日志配置**：将所有日志配置为输出到 stderr，以避免干扰 stdio 传输
4. **服务器设置**：使用 Host 构建器模式并进行适当的依赖注入（DI）配置
5. **工具**：创建至少一个有用的工具，并包含适当的属性和描述
6. **错误处理**：包含适当的错误处理和验证

## 实现细节

### 基础项目设置
- 使用 .NET 8.0 或更高版本
- 创建一个控制台应用程序
- 使用 --prerelease 标志添加必要的 NuGet 包
- 配置日志输出到 stderr

### 服务器配置
- 使用 `Host.CreateApplicationBuilder` 进行依赖注入（DI）和生命周期管理
- 使用 `AddMcpServer()` 配置 stdio 传输
- 使用 `WithToolsFromAssembly()` 实现工具的自动发现
- 确保服务器通过 `RunAsync()` 运行

### 工具实现
- 在工具类上使用 `[McpServerToolType]` 属性
- 在工具方法上使用 `[McpServerTool]` 属性
- 为工具和参数添加 `[Description]` 属性
- 在适当情况下支持异步操作
- 包含适当的参数验证

### 代码质量
- 遵循 C# 命名规范
- 包含 XML 文档注释
- 使用可空引用类型
- 使用 McpProtocolException 实现适当的错误处理
- 使用结构化日志进行调试

## 可考虑的示例工具类型
- 文件操作（读取、写入、搜索）
- 数据处理（转换、验证、分析）
- 外部 API 集成（HTTP 请求）
- 系统操作（执行命令、检查状态）
- 数据库操作（查询、更新）

## 测试指导
- 解释如何运行服务器
- 提供用于测试的 MCP 客户端示例命令
- 包含故障排除提示

生成一个完整、可投入生产的 MCP 服务器，包含全面的文档和错误处理。
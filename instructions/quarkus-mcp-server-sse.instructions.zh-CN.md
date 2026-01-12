

---
应用对象: *
描述: Quarkus 和 MCP 服务器的 HTTP SSE 传输开发标准和指南
---
# Quarkus MCP 服务器

使用 Java 21、Quarkus 框架和 HTTP SSE 传输构建 MCP 服务器。

## 技术栈

- Java 21 与 Quarkus 框架
- MCP 服务器扩展: `mcp-server-sse`
- CDI 依赖注入
- MCP 端点: `http://localhost:8080/mcp/sse`

## 快速入门

```bash
quarkus create app --no-code -x rest-client-jackson,qute,mcp-server-sse your-domain-mcp-server
```

## 结构

- 使用标准的 Java 命名规范（PascalCase 类名，camelCase 方法名）
- 按照包结构组织: `model`, `repository`, `service`, `mcp`
- 对不可变数据模型使用 Record 类型
- 不可变数据的状态管理必须由仓库层处理
- 为公共方法添加 Javadoc 注释

## MCP 工具

- 必须在 `@ApplicationScoped` CDI Bean 中定义公共方法
- 使用 `@Tool(name="工具名称", description="清晰描述")`
- 不要返回 `null`，而是返回错误信息
- 始终验证参数并优雅处理错误

## 架构

- 分离关注点：MCP 工具 → 服务层 → 仓库层
- 使用 `@Inject` 进行依赖注入
- 确保数据操作线程安全
- 使用 `Optional<T>` 来避免空指针异常

## 常见问题

- 不要在 MCP 工具中放置业务逻辑（使用服务层）
- 不要从工具中抛出异常（返回错误字符串）
- 不要忘记验证输入参数
- 使用边缘情况（空值、空输入）进行测试
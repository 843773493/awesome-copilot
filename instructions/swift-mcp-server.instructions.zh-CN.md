

---
description: '构建使用官方 MCP Swift SDK 包的 Model Context Protocol (MCP) 服务器的最佳实践和模式。'
applyTo: "**/*.swift, **/Package.swift, **/Package.resolved"
---

# Swift MCP 服务器开发指南

在使用官方 Swift SDK 构建 MCP 服务器时，请遵循以下最佳实践和模式。

## 服务器设置

使用 `Server` 类创建 MCP 服务器并配置其功能：

```swift
import MCP

let server = Server(
    name: "MyServer",
    version: "1.0.0",
    capabilities: .init(
        prompts: .init(listChanged: true),
        resources: .init(subscribe: true, listChanged: true),
        tools: .init(listChanged: true)
    )
)
```

## 添加工具

使用 `withMethodHandler` 注册工具处理程序：

```swift
// 注册工具列表处理程序
await server.withMethodHandler(ListTools.self) { _ in
    let tools = [
        Tool(
            name: "search",
            description: "搜索信息",
            inputSchema: .object([
                "properties": .object([
                    "query": .string("搜索查询"),
                    "limit": .number("最大结果数")
                ]),
                "required": .array([.string("query")])
            ])
        )
    ]
    return .init(tools: tools)
}

// 注册工具调用处理程序
await server.withMethodHandler(CallTool.self) { params in
    switch params.name {
    case "search":
        let query = params.arguments?["query"]?.stringValue ?? ""
        let limit = params.arguments?["limit"]?.intValue ?? 10
        
        // 执行搜索
        let results = performSearch(query: query, limit: limit)
        
        return .init(
            content: [.text("找到 $results.count) 个结果")],
            isError: false
        )
        
    default:
        return .init(
            content: [.text("未知工具")],
            isError: true
        )
    }
}
```

## 添加资源

实现资源处理程序以支持数据访问：

```swift
// 注册资源列表处理程序
await server.withMethodHandler(ListResources.self) { params in
    let resources = [
        Resource(
            name: "数据文件",
            uri: "resource://data/example.txt",
            description: "示例数据文件",
            mimeType: "text/plain"
        )
    ]
    return .init(resources: resources, nextCursor: nil)
}

// 注册资源读取处理程序
await server.withMethodHandler(ReadResource.self) { params in
    switch params.uri {
    case "resource://data/example.txt":
        let content = loadResourceContent(uri: params.uri)
        return .init(contents: [
            Resource.Content.text(
                content,
                uri: params.uri,
                mimeType: "text/plain"
            )
        ])
        
    default:
        throw MCPError.invalidParams("未知资源 URI: $params.uri)")
    }
}

// 注册资源订阅处理程序
await server.withMethodHandler(ResourceSubscribe.self) { params in
    // 跟踪订阅以接收通知
    subscriptions.insert(params.uri)
    print("客户端订阅了 $params.uri)")
    return .init()
}
```

## 添加提示

实现提示处理程序以支持模板化对话：

```swift
// 注册提示列表处理程序
await server.withMethodHandler(ListPrompts.self) { params in
    let prompts = [
        Prompt(
            name: "analyze",
            description: "分析主题",
            arguments: [
                .init(name: "topic", description: "要分析的主题", required: true),
                .init(name: "depth", description: "分析深度", required: false)
            ]
        )
    ]
    return .init(prompts: prompts, nextCursor: nil)
}

// 注册提示获取处理程序
await server.withMethodHandler(GetPrompt.self) { params in
    switch params.name {
    case "analyze":
        let topic = params.arguments?["topic"]?.stringValue ?? "general"
        let depth = params.arguments?["depth"]?.stringValue ?? "basic"
        
        let description = "对 $topic) 进行 $depth) 级分析"
        let messages: [Prompt.Message] = [
            .user("请分析此主题: $topic)"),
            .assistant("我将提供对 $topic) 的 $depth) 级分析")
        ]
        
        return .init(description: description, messages: messages)
        
    default:
        throw MCPError.invalidParams("未知提示: $params.name)")
    }
}
```

## 传输配置

### 标准输入输出传输 (Stdio Transport)

用于本地子进程通信：

```swift
import MCP
import Logging

let logger = Logger(label: "com.example.mcp-server")
let transport = StdioTransport(logger: logger)

try await server.start(transport: transport)
```

### HTTP 传输 (客户端侧)

用于远程服务器连接：

```swift
let transport = HTTPClientTransport(
    endpoint: URL(string: "http://localhost:8080")!,
    streaming: true  // 启用 Server-Sent Events
)

try await client.connect(transport: transport)
```

## 并发与 Actor

服务器是一个 Actor，确保线程安全访问：

```swift
actor ServerState {
    private var subscriptions: Set<String> = []
    private var cache: [String: Any] = [:]
    
    func addSubscription(_ uri: String) {
        subscriptions.insert(uri)
    }
    
    func getSubscriptions() -> Set<String> {
        return subscriptions
    }
}

let state = ServerState()

await server.withMethodHandler(ResourceSubscribe.self) { params in
    await state.addSubscription(params.uri)
    return .init()
}
```

## 错误处理

使用 Swift 的错误处理机制与 `MCPError`：

```swift
await server.withMethodHandler(CallTool.self) { params in
    do {
        guard let query = params.arguments?["query"]?.stringValue else {
            throw MCPError.invalidParams("缺少查询参数")
        }
        
        let result = try performOperation(query: query)
        
        return .init(
            content: [.text(result)],
            isError: false
        )
    } catch let error as MCPError {
        return .init(
            content: [.text(error.localizedDescription)],
            isError: true
        )
    } catch {
        return .init(
            content: [.text("意外错误: $error.localizedDescription)")],
            isError: true
        )
    }
}
```

## 使用 Value 类型的 JSON 模式

使用 `Value` 类型来定义 JSON 模式：

```swift
let schema = Value.object([
    "type": .string("object"),
    "properties": .object([
        "name": .object([
            "type": .string("string"),
            "description": .string("用户名")
        ]),
        "age": .object([
            "type": .string("integer"),
            "minimum": .number(0),
            "maximum": .number(150)
        ]),
        "email": .object([
            "type": .string("string"),
            "format": .string("email")
        ])
    ]),
    "required": .array([.string("name")])
])
```

## Swift 包管理器配置

创建你的 `Package.swift` 文件：

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyMCPServer",
    platforms: [
        .macOS(.v13),
        .iOS(.v16)
    ],
    dependencies: [
        .package(
            url: "https://github.com/modelcontextprotocol/swift-sdk.git",
            from: "0.10.0"
        ),
        .package(
            url: "https://github.com/apple/swift-log.git",
            from: "1.5.0"
        )
    ],
    targets: [
        .executableTarget(
            name: "MyMCPServer",
            dependencies: [
                .product(name: "MCP", package: "swift-sdk"),
                .product(name: "Logging", package: "swift-log")
            ]
        )
    ]
)
```

## 使用 ServiceLifecycle 实现优雅关闭

使用 Swift Service Lifecycle 进行正确关闭：

```swift
import MCP
import ServiceLifecycle
import Logging

struct MCPService: Service {
    let server: Server
    let transport: Transport
    
    func run() async throws {
        try await server.start(transport: transport)
        try await Task.sleep(for: .days(365 * 100))
    }
    
    func shutdown() async throws {
        await server.stop()
    }
}

let logger = Logger(label: "com.example.mcp-server")
let transport = StdioTransport(logger: logger)
let mcpService = MCPService(server: server, transport: transport)

let serviceGroup = ServiceGroup(
    services: [mcpService],
    configuration: .init(
        gracefulShutdownSignals: [.sigterm, .sigint]
    ),
    logger: logger
)

try await serviceGroup.run()
```

## 异步/等待模式

所有服务器操作均使用 Swift 并发：

```swift
await server.withMethodHandler(CallTool.self) { params in
    async let result1 = fetchData1()
    async let result2 = fetchData2()
    
    let combined = await "$result1) 和 $result2)"
    
    return .init(
        content: [.text(combined)],
        isError: false
    )
}
```

## 日志记录

使用 swift-log 进行结构化日志记录：

```swift
import Logging

let logger = Logger(label: "com.example.mcp-server")

await server.withMethodHandler(CallTool.self) { params in
    logger.info("工具调用", metadata: [
        "name": .string(params.name),
        "args": .string("\(params.arguments ?? [:])")
    ])
    
    // 处理工具调用
    
    logger.debug("工具调用成功完成")
    
    return .init(content: [.text("结果")], isError: false)
}
```

## 测试

使用异步/等待测试你的服务器：

```swift
import XCTest
@testable import MyMCPServer

final class 服务器测试: XCTestCase {
    func 测试工具调用() async throws {
        let server = createTestServer()
        
        // 测试工具调用逻辑
        let params = CallTool.Params(
            name: "search",
            arguments: ["query": .string("test")]
        )
        
        // 验证行为
        XCTAssertNoThrow(try await processToolCall(params))
    }
}
```

## 初始化钩子

通过初始化钩子验证客户端连接：

```swift
try await server.start(transport: transport) { clientInfo, clientCapabilities in
    // 验证客户端
    guard clientInfo.name != "BlockedClient" else {
        throw MCPError.invalidRequest("客户端不允许连接")
    }
    
    // 检查功能
    if clientCapabilities.sampling == nil {
        logger.warning("客户端不支持采样")
    }
    
    logger.info("客户端连接成功", metadata: [
        "name": .string(clientInfo.name),
        "version": .string(clientInfo.version)
    ])
}
```

## 常见模式

### 内容类型

处理不同的内容类型：

```swift
return .init(
    content: [
        .text("纯文本响应"),
        .image(imageData, mimeType: "image/png", metadata: [
            "width": 1024,
            "height": 768
        ]),
        .resource(
            uri: "resource://data",
            mimeType: "application/json",
            text: jsonString
        ])
    ],
    isError: false
)
```

### 严格配置

使用严格模式在缺少功能时快速失败：

```swift
let client = Client(
    name: "StrictClient",
    version: "1.0.0",
    configuration: .strict
)

// 如果功能不可用将立即抛出错误
try await client.listTools()
```

### 请求批处理

高效发送多个请求：

```swift
var tasks: [Task<CallTool.Result, Error>] = []

try await client.withBatch { batch in
    for i in 0..<10 {
        tasks.append(
            try await batch.addRequest(
                CallTool.request(.init(
                    name: "process",
                    arguments: ["id": .number(Double(i))]
                ))
            )
        )
    }
}

for (index, task) in tasks.enumerated() {
    let result = try await task.value
    print("\(index): $result.content)")
}
```
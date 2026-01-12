

---
description: '使用官方 io.modelcontextprotocol:kotlin-sdk 库构建 Model Context Protocol (MCP) 服务器的最佳实践和模式。'
applyTo: "**/*.kt, **/*.kts, **/build.gradle.kts, **/settings.gradle.kts"
---

# Kotlin MCP 服务器开发指南

在使用官方 Kotlin SDK 构建 MCP 服务器时，请遵循以下最佳实践和模式。

## 服务器设置

使用 `Server` 类创建 MCP 服务器：

```kotlin
import io.modelcontextprotocol.kotlin.sdk.server.Server
import io.modelcontextprotocol.kotlin.sdk.server.ServerOptions
import io.modelcontextprotocol.kotlin.sdk.Implementation
import io.modelcontextprotocol.kotlin.sdk.ServerCapabilities

val server = Server(
    serverInfo = Implementation(
        name = "my-server",
        version = "1.0.0"
    ),
    options = ServerOptions(
        capabilities = ServerCapabilities(
            tools = ServerCapabilities.Tools(),
            resources = ServerCapabilities.Resources(
                subscribe = true,
                listChanged = true
            ),
            prompts = ServerCapabilities.Prompts(listChanged = true)
        )
    )
) {
    "服务器描述在此处"
}
```

## 添加工具

使用 `server.addTool()` 注册带有类型化请求/响应处理的工具：

```kotlin
import io.modelcontextprotocol.kotlin.sdk.CallToolRequest
import io.modelcontextprotocol.kotlin.sdk.CallToolResult
import io.modelcontextprotocol.kotlin.sdk.TextContent

server.addTool(
    name = "search",
    description = "搜索信息",
    inputSchema = buildJsonObject {
        put("type", "object")
        putJsonObject("properties") {
            putJsonObject("query") {
                put("type", "string")
                put("description", "搜索查询")
            }
            putJsonObject("limit") {
                put("type", "integer")
                put("description", "返回的最大结果数")
            }
        }
        putJsonArray("required") {
            add("query")
        }
    }
) { request: CallToolRequest ->
    val query = request.params.arguments["query"] as? String
        ?: throw IllegalArgumentException("query 是必需的")
    val limit = (request.params.arguments["limit"] as? Number)?.toInt() ?: 10
    
    // 执行搜索
    val results = performSearch(query, limit)
    
    CallToolResult(
        content = listOf(
            TextContent(
                text = results.joinToString("\n")
            )
        )
    )
}
```

## 添加资源

使用 `server.addResource()` 提供可访问的数据：

```kotlin
import io.modelcontextprotocol.kotlin.sdk.ReadResourceRequest
import io.modelcontextprotocol.kotlin.sdk.ReadResourceResult
import io.modelcontextprotocol.kotlin.sdk.TextResourceContents

server.addResource(
    uri = "file:///data/example.txt",
    name = "示例数据",
    description = "示例资源数据",
    mimeType = "text/plain"
) { request: ReadResourceRequest ->
    val content = loadResourceContent(request.uri)
    
    ReadResourceResult(
        contents = listOf(
            TextResourceContents(
                text = content,
                uri = request.uri,
                mimeType = "text/plain"
            )
        )
    )
}
```

## 添加提示

使用 `server.addPrompt()` 注册可重用的提示模板：

```kotlin
import io.modelcontextprotocol.kotlin.sdk.GetPromptRequest
import io.modelcontextprotocol.kotlin.sdk.GetPromptResult
import io.modelcontextprotocol.kotlin.sdk.PromptMessage
import io.modelcontextprotocol.kotlin.sdk.Role

server.addPrompt(
    name = "analyze",
    description = "分析主题",
    arguments = listOf(
        PromptArgument(
            name = "topic",
            description = "要分析的主题",
            required = true
        )
    )
) { request: GetPromptRequest ->
    val topic = request.params.arguments?.get("topic") as? String
        ?: throw IllegalArgumentException("topic 是必需的")
    
    GetPromptResult(
        description = "分析给定的主题",
        messages = listOf(
            PromptMessage(
                role = Role.User,
                content = TextContent(
                    text = "分析此主题: $topic"
                )
            )
        )
    )
}
```

## 传输配置

### 标准输入/输出传输

用于通过标准输入/输出进行通信：

```kotlin
import io.modelcontextprotocol.kotlin.sdk.server.StdioServerTransport

suspend fun main() {
    val transport = StdioServerTransport()
    server.connect(transport)
}
```

### 使用 Ktor 的 SSE 传输

用于基于 HTTP 的 Server-Sent Events 通信：

```kotlin
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.modelcontextprotocol.kotlin.sdk.server.mcp

fun main() {
    embeddedServer(Netty, port = 8080) {
        mcp {
            Server(
                serverInfo = Implementation(
                    name = "sse-server",
                    version = "1.0.0"
                ),
                options = ServerOptions(
                    capabilities = ServerCapabilities(
                        tools = ServerCapabilities.Tools()
                    )
                )
            ) {
                "基于 SSE 的 MCP 服务器"
            }
        }
    }.start(wait = true)
}
```

## 协程使用

所有 MCP 操作均为挂起函数。请正确使用 Kotlin 协程：

```kotlin
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.async

server.addTool(
    name = "parallel-search",
    description = "并行搜索多个来源"
) { request ->
    coroutineScope {
        val source1 = async { searchSource1(query) }
        val source2 = async { searchSource2(query) }
        
        val results = source1.await() + source2.await()
        
        CallToolResult(
            content = listOf(TextContent(text = results.joinToString("\n")))
        )
    }
}
```

## 错误处理

使用 Kotlin 的异常处理并提供有意义的错误信息：

```kotlin
server.addTool(
    name = "validate-input",
    description = "处理验证输入"
) { request ->
    try {
        val input = request.params.arguments["input"] as? String
            ?: throw IllegalArgumentException("input 是必需的")
        
        require(input.isNotBlank()) { "input 不能为空" }
        
        val result = processInput(input)
        
        CallToolResult(
            content = listOf(TextContent(text = result))
        )
    } catch (e: IllegalArgumentException) {
        CallToolResult(
            isError = true,
            content = listOf(TextContent(text = "验证错误: ${e.message}"))
        )
    }
}
```

## 使用 kotlinx.serialization 的 JSON 模式

使用 kotlinx.serialization 实现类型安全的 JSON 模式：

```kotlin
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*

@Serializable
data class SearchInput(
    val query: String,
    val limit: Int = 10,
    val filters: List<String> = emptyList()
)

fun createToolSchema(): JsonObject = buildJsonObject {
    put("type", "object")
    putJsonObject("properties") {
        putJsonObject("query") {
            put("type", "string")
            put("description", "搜索查询")
        }
        putJsonObject("limit") {
            put("type", "integer")
            put("default", 10)
        }
        putJsonObject("filters") {
            put("type", "array")
            putJsonObject("items") {
                put("type", "string")
            }
        }
    }
    putJsonArray("required") {
        add("query")
    }
}
```

## Gradle 配置

正确设置您的 `build.gradle.kts` 文件：

```kotlin
plugins {
    kotlin("jvm") version "2.1.0"
    kotlin("plugin.serialization") version "2.1.0"
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("io.modelcontextprotocol:kotlin-sdk:0.7.2")
    
    // 用于客户端传输
    implementation("io.ktor:ktor-client-cio:3.0.0")
    
    // 用于服务器传输
    implementation("io.ktor:ktor-server-netty:3.0.0")
    
    // 用于 JSON 序列化
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")
    
    // 用于协程
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.9.0")
}
```

## 多平台支持

Kotlin SDK 支持 Kotlin 多平台（JVM、Wasm、iOS）：

```kotlin
kotlin {
    jvm()
    js(IR) {
        browser()
        nodejs()
    }
    wasmJs()
    
    sourceSets {
        commonMain.dependencies {
            implementation("io.modelcontextprotocol:kotlin-sdk:0.7.2")
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.9.0")
        }
    }
}
```

## 资源生命周期

处理资源更新和订阅：

```kotlin
server.addResource(
    uri = "file:///dynamic/data",
    name = "动态数据",
    description = "频繁更新的数据",
    mimeType = "application/json"
) { request ->
    // 提供当前状态
    ReadResourceResult(
        contents = listOf(
            TextResourceContents(
                text = getCurrentData(),
                uri = request.uri,
                mimeType = "application/json"
            )
        )
    )
}

// 当资源发生变化时通知客户端
server.notifyResourceListChanged()
```

## 测试

使用 Kotlin 协程测试工具对 MCP 工具进行测试：

```kotlin
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals

class ServerTest {
    @Test
    fun testSearchTool() = runTest {
        val server = createTestServer()
        
        val request = CallToolRequest(
            params = CallToolParams(
                name = "search",
                arguments = mapOf("query" to "test", "limit" to 5)
            )
        )
        
        val result = server.callTool(request)
        
        assertEquals(false, result.isError)
        assert(result.content.isNotEmpty())
    }
}
```

## 常见模式

### 日志记录

使用 Kotlin 日志库进行结构化日志记录：

```kotlin
import io.github.oshai.kotlinlogging.KotlinLogging

private val logger = KotlinLogging.logger {}

server.addTool(
    name = "logged-operation",
    description = "带日志记录的操作"
) { request ->
    logger.info { "工具被调用，参数为: ${request.params.arguments}" }
    
    try {
        val result = performOperation(request)
        logger.info { "操作成功" }
        result
    } catch (e: Exception) {
        logger.error(e) { "操作失败" }
        throw e
    }
}
```

### 配置

使用数据类进行配置：

```kotlin
import kotlinx.serialization.Serializable

@Serializable
data class ServerConfig(
    val name: String = "my-server",
    val version: String = "1.0.0",
    val port: Int = 8080,
    val enableTools: Boolean = true
)

fun loadConfig(): ServerConfig {
    // 从环境变量或配置文件加载
    return ServerConfig(
        name = System.getenv("SERVER_NAME") ?: "my-server",
        version = System.getenv("VERSION") ?: "1.0.0"
    )
}
```

### 依赖注入

使用构造函数注入以提高可测试性：

```kotlin
class MyServer(
    private val dataService: DataService,
    private val config: ServerConfig
) {
    fun createServer() = Server(
        serverInfo = Implementation(
            name = config.name,
            version = config.version
        )
    ) {
        "带依赖注入的 MCP 服务器"
    }.apply {
        addTool(
            name = "fetch-data",
            description = "使用注入的服务获取数据"
        ) { request ->
            val data = dataService.fetchData()
            CallToolResult(
                content = listOf(TextContent(text = data))
            )
        }
    }
}
```


---
description: '使用官方MCP Java SDK结合反应式流和Spring集成构建模型上下文协议（MCP）服务器的最佳实践和模式。'
applyTo: "**/*.java, **/pom.xml, **/build.gradle, **/build.gradle.kts"
---

# Java MCP服务器开发指南

在使用官方Java SDK构建MCP服务器时，请遵循以下最佳实践和模式。

## 依赖项

将MCP Java SDK添加到您的Maven项目中：

```xml
<dependencies>
    <dependency>
        <groupId>io.modelcontextprotocol.sdk</groupId>
        <artifactId>mcp</artifactId>
        <version>0.14.1</version>
    </dependency>
</dependencies>
```

或使用Gradle：

```kotlin
dependencies {
    implementation("io.modelcontextprotocol.sdk:mcp:0.14.1")
}
```

## 服务器设置

使用构建器模式创建MCP服务器：

```java
import io.mcp.server.McpServer;
import io.mcp.server.McpServerBuilder;
import io.mcp.server.transport.StdioServerTransport;

McpServer server = McpServerBuilder.builder()
    .serverInfo("my-server", "1.0.0")
    .capabilities(capabilities -> capabilities
        .tools(true)
        .resources(true)
        .prompts(true))
    .build();

// 使用标准输入输出传输启动
StdioServerTransport transport = new StdioServerTransport();
server.start(transport).subscribe();
```

## 添加工具

向服务器注册工具处理程序：

```java
import io.mcp.server.tool.Tool;
import io.mcp.server.tool.ToolHandler;
import reactor.core.publisher.Mono;

// 定义一个工具
Tool searchTool = Tool.builder()
    .name("search")
    .description("搜索信息")
    .inputSchema(JsonSchema.object()
        .property("query", JsonSchema.string()
            .description("搜索查询")
            .required(true))
        .property("limit", JsonSchema.integer()
            .description("最大结果数")
            .defaultValue(10)))
    .build();

// 注册工具处理程序
server.addToolHandler("search", (arguments) -> {
    String query = arguments.get("query").asText();
    int limit = arguments.has("limit") 
        ? arguments.get("limit").asInt() 
        : 10;
    
    // 执行搜索
    List<String> results = performSearch(query, limit);
    
    return Mono.just(ToolResponse.success()
        .addTextContent("找到 " + results.size() + " 个结果")
        .build());
});
```

## 添加资源

为数据访问实现资源处理程序：

```java
import io.mcp.server.resource.Resource;
import io.mcp.server.resource.ResourceHandler;

// 注册资源列表处理程序
server.addResourceListHandler(() -> {
    List<Resource> resources = List.of(
        Resource.builder()
            .name("数据文件")
            .uri("resource://data/example.txt")
            .description("示例数据文件")
            .mimeType("text/plain")
            .build()
    );
    return Mono.just(resources);
});

// 注册资源读取处理程序
server.addResourceReadHandler((uri) -> {
    if (uri.equals("resource://data/example.txt")) {
        String content = loadResourceContent(uri);
        return Mono.just(ResourceContent.text(content, uri));
    }
    throw new ResourceNotFoundException(uri);
});

// 注册资源订阅处理程序
server.addResourceSubscribeHandler((uri) -> {
    subscriptions.add(uri);
    log.info("客户端订阅了 {}", uri);
    return Mono.empty();
});
```

## 添加提示

为模板化对话实现提示处理程序：

```java
import io.mcp.server.prompt.Prompt;
import io.mcp.server.prompt.PromptMessage;
import io.mcp.server.prompt.PromptArgument;

// 注册提示列表处理程序
server.addPromptListHandler(() -> {
    List<Prompt> prompts = List.of(
        Prompt.builder()
            .name("analyze")
            .description("分析主题")
            .argument(PromptArgument.builder()
                .name("topic")
                .description("要分析的主题")
                .required(true)
                .build())
            .argument(PromptArgument.builder()
                .name("depth")
                .description("分析深度")
                .required(false)
                .build())
            .build()
    );
    return Mono.just(prompts);
});

// 注册提示获取处理程序
server.addPromptGetHandler((name, arguments) -> {
    if (name.equals("analyze")) {
        String topic = arguments.getOrDefault("topic", "general");
        String depth = arguments.getOrDefault("depth", "basic");
        
        List<PromptMessage> messages = List.of(
            PromptMessage.user("请分析此主题: " + topic),
            PromptMessage.assistant("我将提供 " + depth + " 级的分析")
        );
        
        return Mono.just(PromptResult.builder()
            .description("主题 " + topic + " 的 " + depth + " 级分析")
            .messages(messages)
            .build());
    }
    throw new PromptNotFoundException(name);
});
```

## 反应式流模式

Java SDK使用反应式流（Project Reactor）进行异步处理：

```java
// 返回Mono用于单个结果
server.addToolHandler("process", (args) -> {
    return Mono.fromCallable(() -> {
        String result = expensiveOperation(args);
        return ToolResponse.success()
            .addTextContent(result)
            .build();
    }).subscribeOn(Schedulers.boundedElastic());
});

// 返回Flux用于流式结果
server.addResourceListHandler(() -> {
    return Flux.fromIterable(getResources())
        .map(r -> Resource.builder()
            .uri(r.getUri())
            .name(r.getName())
            .build())
        .collectList();
});
```

## 同步门面

对于阻塞使用场景，使用同步API：

```java
import io.mcp.server.McpSyncServer;

McpSyncServer syncServer = server.toSyncServer();

// 阻塞工具处理程序
syncServer.addToolHandler("greet", (args) -> {
    String name = args.get("name").asText();
    return ToolResponse.success()
        .addTextContent("你好, " + name + "!")
        .build();
});
```

## 传输配置

### 标准输入输出传输

用于本地子进程通信：

```java
import io.mcp.server.transport.StdioServerTransport;

StdioServerTransport transport = new StdioServerTransport();
server.start(transport).block();
```

### HTTP传输（Servlet）

用于基于HTTP的服务器：

```java
import io.mcp.server.transport.ServletServerTransport;
import jakarta.servlet.http.HttpServlet;

public class McpServlet extends HttpServlet {
    private final McpServer server;
    private final ServletServerTransport transport;
    
    public McpServlet() {
        this.server = createMcpServer();
        this.transport = new ServletServerTransport();
    }
    
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) {
        transport.handleRequest(server, req, resp).block();
    }
}
```

## Spring Boot集成

使用Spring Boot starter进行无缝集成：

```xml
<dependency>
    <groupId>io.modelcontextprotocol.sdk</groupId>
    <artifactId>mcp-spring-boot-starter</artifactId>
    <version>0.14.1</version>
</dependency>
```

使用Spring配置服务器：

```java
import org.springframework.context.annotation.Configuration;
import io.mcp.spring.McpServerConfigurer;

@Configuration
public class McpConfiguration {
    
    @Bean
    public McpServerConfigurer mcpServerConfigurer() {
        return server -> server
            .serverInfo("spring-server", "1.0.0")
            .capabilities(cap -> cap
                .tools(true)
                .resources(true)
                .prompts(true));
    }
}
```

将处理程序注册为Spring bean：

```java
import org.springframework.stereotype.Component;
import io.mcp.spring.ToolHandler;

@Component
public class SearchToolHandler implements ToolHandler {
    
    @Override
    public String getName() {
        return "search";
    }
    
    @Override
    public Tool getTool() {
        return Tool.builder()
            .name("search")
            .description("搜索信息")
            .inputSchema(JsonSchema.object()
                .property("query", JsonSchema.string().required(true)))
            .build();
    }
    
    @Override
    public Mono<ToolResponse> handle(JsonNode arguments) {
        String query = arguments.get("query").asText();
        return Mono.just(ToolResponse.success()
            .addTextContent("搜索结果: " + query)
            .build());
    }
}
```

## 错误处理

使用MCP异常进行正确错误处理：

```java
server.addToolHandler("risky", (args) -> {
    return Mono.fromCallable(() -> {
        try {
            String result = riskyOperation(args);
            return ToolResponse.success()
                .addTextContent(result)
                .build();
        } catch (ValidationException e) {
            return ToolResponse.error()
                .message("无效输入: " + e.getMessage())
                .build();
        } catch (Exception e) {
            log.error("发生意外错误", e);
            return ToolResponse.error()
                .message("发生内部错误")
                .build();
        }
    });
});
```

## JSON Schema构建

使用流畅的schema构建器：

```java
import io.mcp.json.JsonSchema;

JsonSchema schema = JsonSchema.object()
    .property("name", JsonSchema.string()
        .description("用户名")
        .minLength(1)
        .maxLength(100)
        .required(true))
    .property("age", JsonSchema.integer()
        .description("年龄")
        .minimum(0)
        .maximum(150))
    .property("email", JsonSchema.string()
        .description("电子邮件地址")
        .format("email")
        .required(true))
    .property("tags", JsonSchema.array()
        .items(JsonSchema.string())
        .uniqueItems(true))
    .additionalProperties(false)
    .build();
```

## 日志和可观测性

使用SLF4J进行日志记录：

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

private static final Logger log = LoggerFactory.getLogger(MyMcpServer.class);

server.addToolHandler("process", (args) -> {
    log.info("调用工具: process, 参数: {}", args);
    
    return Mono.fromCallable(() -> {
        String result = process(args);
        log.debug("处理成功完成");
        return ToolResponse.success()
            .addTextContent(result)
            .build();
    }).doOnError(error -> {
        log.error("处理失败", error);
    });
});
```

通过Reactor传播上下文：

```java
import reactor.util.context.Context;

server.addToolHandler("traced", (args) -> {
    return Mono.deferContextual(ctx -> {
        String traceId = ctx.get("traceId");
        log.info("使用traceId: {}进行处理", traceId);
        
        return Mono.just(ToolResponse.success()
            .addTextContent("已处理")
            .build());
    });
});
```

## 测试

使用同步API编写测试：

```java
import org.junit.jupiter.api.Test;
import static org.assertj.core.Assertions.assertThat;

class McpServerTest {
    
    @Test
    void testToolHandler() {
        McpServer server = createTestServer();
        McpSyncServer syncServer = server.toSyncServer();
        
        JsonNode args = objectMapper.createObjectNode()
            .put("query", "test");
        
        ToolResponse response = syncServer.callTool("search", args);
        
        assertThat(response.isError()).isFalse();
        assertThat(response.getContent()).hasSize(1);
    }
}
```

## Jackson集成

SDK使用Jackson进行JSON序列化。根据需要进行自定义：

```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

ObjectMapper mapper = new ObjectMapper();
mapper.registerModule(new JavaTimeModule());

// 使用自定义映射器启动服务器
McpServer server = McpServerBuilder.builder()
    .objectMapper(mapper)
    .build();
```

## 内容类型

支持响应中的多种内容类型：

```java
import io.mcp.server.content.Content;

server.addToolHandler("multi", (args) -> {
    return Mono.just(ToolResponse.success()
        .addTextContent("纯文本响应")
        .addImageContent(imageBytes, "image/png")
        .addResourceContent("resource://data", "application/json", jsonData)
        .build());
});
```

## 服务器生命周期管理

正确管理服务器生命周期：

```java
import reactor.core.Disposable;

Disposable serverDisposable = server.start(transport).subscribe();

// 优雅关闭
Runtime.getRuntime().addShutdownHook(new Thread(() -> {
    log.info("关闭MCP服务器");
    serverDisposable.dispose();
    server.stop().block();
}));
```

## 常见模式

### 请求验证

```java
server.addToolHandler("validate", (args) -> {
    if (!args.has("required_field")) {
        return Mono.just(ToolResponse.error()
            .message("缺少必填字段required_field")
            .build());
    }
    
    return processRequest(args);
});
```

### 异步操作

```java
server.addToolHandler("async", (args) -> {
    return Mono.fromCallable(() -> callExternalApi(args))
        .timeout(Duration.ofSeconds(30))
        .onErrorResume(TimeoutException.class, e -> 
            Mono.just(ToolResponse.error()
                .message("操作超时")
                .build()))
        .subscribeOn(Schedulers.boundedElastic());
});
```

### 资源缓存

```java
private final Map<String, String> cache = new ConcurrentHashMap<>();

server.addResourceReadHandler((uri) -> {
    return Mono.fromCallable(() -> 
        cache.computeIfAbsent(uri, this::loadResource))
        .map(content -> ResourceContent.text(content, uri));
});
```

## 最佳实践

1. **使用反应式流**处理异步操作和背压
2. **利用Spring Boot** starter进行企业级应用开发
3. **实现完善的错误处理**并提供具体错误信息
4. **使用SLF4J**进行日志记录，而非System.out
5. **在工具和提示处理程序中验证输入**
6. **通过正确资源清理实现优雅关闭**
7. **使用受限弹性调度器**处理阻塞操作
8. **在反应式链中传播上下文**以实现可观测性
9. **使用同步API**进行简化测试
10. **遵循Java命名规范**（方法使用驼峰命名，类使用帕斯卡命名）
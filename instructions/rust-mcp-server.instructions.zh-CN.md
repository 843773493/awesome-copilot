

---
description: '使用官方 rmcp SDK 通过 async/await 模式构建 Model Context Protocol 服务器的最佳实践'
applyTo: '**/*.rs'
---

# Rust MCP 服务器开发最佳实践

本指南提供了使用官方 Rust SDK (`rmcp`) 构建模型上下文协议 (MCP) 服务器的最佳实践。

## 安装和设置

### 添加依赖项

将 `rmcp` crate 添加到你的 `Cargo.toml` 文件中：

```toml
[dependencies]
rmcp = { version = "0.8.1", features = ["server"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
anyhow = "1.0"
tracing = "0.1"
tracing-subscriber = "0.3"
```

对于宏支持：

```toml
[dependencies]
rmcp-macros = "0.8"
schemars = { version = "0.8", features = ["derive"] }
```

### 项目结构

组织你的 Rust MCP 服务器项目：

```
my-mcp-server/
├── Cargo.toml
├── src/
│   ├── main.rs           # 服务器入口
│   ├── handler.rs        # ServerHandler 实现
│   ├── tools/
│   │   ├── mod.rs
│   │   ├── calculator.rs
│   │   └── greeter.rs
│   ├── prompts/
│   │   ├── mod.rs
│   │   └── code_review.rs
│   └── resources/
│       ├── mod.rs
│       └── data.rs
└── tests/
    └── integration_tests.rs
```

## 服务器实现

### 基本服务器设置

创建一个使用标准输入输出传输的服务器：

```rust
use rmcp::{
    protocol::ServerCapabilities,
    server::{Server, ServerHandler},
    transport::StdioTransport,
};
use tokio::signal;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();
    
    let handler = MyServerHandler::new();
    let transport = StdioTransport::new();
    
    let server = Server::builder()
        .with_handler(handler)
        .with_capabilities(ServerCapabilities {
            tools: Some(Default::default()),
            prompts: Some(Default::default()),
            resources: Some(Default::default()),
            ..Default::default()
        })
        .build(transport)?;
    
    server.run(signal::ctrl_c()).await?;
    
    Ok(())
}
```

### ServerHandler 实现

实现 `ServerHandler` trait：

```rust
use rmcp::{
    model::*,
    protocol::*,
    server::{RequestContext, ServerHandler, RoleServer},
    ErrorData,
};

pub struct MyServerHandler {
    tool_router: ToolRouter,
}

impl MyServerHandler {
    pub fn new() -> Self {
        Self {
            tool_router: Self::create_tool_router(),
        }
    }
    
    fn create_tool_router() -> ToolRouter {
        // 初始化并返回工具路由器
        ToolRouter::new()
    }
}

#[async_trait::async_trait]
impl ServerHandler for MyServerHandler {
    async fn list_tools(
        &self,
        _request: Option<PaginatedRequestParam>,
        _context: RequestContext<RoleServer>,
    ) -> Result<ListToolsResult, ErrorData> {
        let items = self.tool_router.list_all();
        Ok(ListToolsResult::with_all_items(items))
    }
    
    async fn call_tool(
        &self,
        request: CallToolRequestParam,
        context: RequestContext<RoleServer>,
    ) -> Result<CallToolResult, ErrorData> {
        let tcc = ToolCallContext::new(self, request, context);
        self.tool_router.call(tcc).await
    }
}
```

## 工具开发

### 使用宏定义工具

使用 `#[tool]` 宏进行声明式工具定义：

```rust
use rmcp::tool;
use rmcp::model::Parameters;
use serde::{Deserialize, Serialize};
use schemars::JsonSchema;

#[derive(Debug, Deserialize, JsonSchema)]
pub struct CalculateParams {
    pub a: f64,
    pub b: f64,
    pub operation: String,
}

/// 执行数学计算
#[tool(
    name = "calculate",
    description = "执行基本的算术运算",
    annotations(read_only_hint = true)
)]
pub async fn calculate(params: Parameters<CalculateParams>) -> Result<f64, String> {
    let p = params.inner();
    match p.operation.as_str() {
        "add" => Ok(p.a + p.b),
        "subtract" => Ok(p.a - p.b),
        "multiply" => Ok(p.a * p.b),
        "divide" => {
            if p.b == 0.0 {
                Err("除以零".to_string())
            } else {
                Ok(p.a / p.b)
            }
        }
        _ => Err(format!("未知操作: {}", p.operation)),
    }
}
```

### 使用宏的工具路由器

使用 `#[tool_router]` 和 `#[tool_handler]` 宏：

```rust
use rmcp::{tool_router, tool_handler};

pub struct ToolsHandler {
    tool_router: ToolRouter,
}

#[tool_router]
impl ToolsHandler {
    #[tool]
    async fn greet(params: Parameters<GreetParams>) -> String {
        format!("你好, {}!", params.inner().name)
    }
    
    #[tool(annotations(destructive_hint = true))]
    async fn reset_counter() -> String {
        "计数器重置".to_string()
    }
    
    pub fn new() -> Self {
        Self {
            tool_router: Self::tool_router(),
        }
    }
}

#[tool_handler]
impl ServerHandler for ToolsHandler {
    // 其他处理方法...
}
```

### 工具注解

使用注解来提供工具行为的提示：

```rust
#[tool(
    name = "delete_file",
    annotations(
        destructive_hint = true,
        read_only_hint = false,
        idempotent_hint = false
    )
)]
pub async fn delete_file(params: Parameters<DeleteParams>) -> Result<(), String> {
    // 删除文件逻辑
}

#[tool(
    name = "search_data",
    annotations(
        read_only_hint = true,
        idempotent_hint = true,
        open_world_hint = true
    )
)]
pub async fn search_data(params: Parameters<SearchParams>) -> Vec<String> {
    // 搜索逻辑
}
```

### 返回丰富内容

从工具中返回结构化的内容：

```rust
use rmcp::model::{ToolResponseContent, TextContent, ImageContent};

#[tool]
async fn analyze_code(params: Parameters<CodeParams>) -> ToolResponseContent {
    ToolResponseContent::from(vec![
        TextContent::text(format!("分析 {}:", params.inner().filename)),
        TextContent::text("未发现任何问题。"),
    ])
}
```

## 提示实现

### 提示处理程序

实现提示处理程序：

```rust
use rmcp::model::{Prompt, PromptArgument, PromptMessage, GetPromptResult};

async fn list_prompts(
    &self,
    _request: Option<PaginatedRequestParam>,
    _context: RequestContext<RoleServer>,
) -> Result<ListPromptsResult, ErrorData> {
    let prompts = vec![
        Prompt {
            name: "code-review".to_string(),
            description: Some("检查代码最佳实践".to_string()),
            arguments: Some(vec![
                PromptArgument {
                    name: "language".to_string(),
                    description: Some("编程语言".to_string()),
                    required: Some(true),
                },
            ]),
        },
    ];
    
    Ok(ListPromptsResult { prompts })
}

async fn get_prompt(
    &self,
    request: GetPromptRequestParam,
    _context: RequestContext<RoleServer>,
) -> Result<GetPromptResult, ErrorData> {
    match request.name.as_str() {
        "code-review" => {
            let language = request.arguments
                .as_ref()
                .and_then(|args| args.get("language"))
                .ok_or_else(|| ErrorData::invalid_params("language required"))?;
            
            Ok(GetPromptResult {
                description: Some("代码审查提示".to_string()),
                messages: vec![
                    PromptMessage::user(format!(
                        "请审查此 {} 代码的最佳实践并提出改进建议",
                        language
                    )),
                ],
            })
        }
        _ => Err(ErrorData::invalid_params("未知提示")),
    }
}
```

## 资源实现

### 资源处理程序

实现资源处理程序：

```rust
use rmcp::model::{Resource, ResourceContents, ReadResourceResult};

async fn list_resources(
    &self,
    _request: Option<PaginatedRequestParam>,
    _context: RequestContext<RoleServer>,
) -> Result<ListResourcesResult, ErrorData> {
    let resources = vec![
        Resource {
            uri: "file:///data/config.json".to_string(),
            name: "配置".to_string(),
            description: Some("服务器配置".to_string()),
            mime_type: Some("application/json".to_string()),
        },
    ];
    
    Ok(ListResourcesResult { resources })
}

async fn read_resource(
    &self,
    request: ReadResourceRequestParam,
    _context: RequestContext<RoleServer>,
) -> Result<ReadResourceResult, ErrorData> {
    match request.uri.as_str() {
        "file:///data/config.json" => {
            let content = r#"{"version": "1.0", "enabled": true}"#;
            Ok(ReadResourceResult {
                contents: vec![
                    ResourceContents::text(content.to_string())
                        .with_uri(request.uri)
                        .with_mime_type("application/json"),
                ],
            })
        }
        _ => Err(ErrorData::invalid_params("未知资源")),
    }
}
```

## 传输选项

### 标准输入输出传输

用于 CLI 集成的标准输入输出传输：

```rust
use rmcp::transport::StdioTransport;

let transport = StdioTransport::new();
let server = Server::builder()
    .with_handler(handler)
    .build(transport)?;
```

### 服务器发送事件 (SSE) 传输

基于 HTTP 的 SSE 传输：

```rust
use rmcp::transport::SseServerTransport;
use std::net::SocketAddr;

let addr: SocketAddr = "127.0.0.1:8000".parse()?;
let transport = SseServerTransport::new(addr);

let server = Server::builder()
    .with_handler(handler)
    .build(transport)?;

server.run(signal::ctrl_c()).await?;
```

### 可流式传输的 HTTP 传输

使用 Axum 的 HTTP 流式传输：

```rust
use rmcp::transport::StreamableHttpTransport;
use axum::{Router, routing::post};

let transport = StreamableHttpTransport::new();
let app = Router::new()
    .route("/mcp", post(transport.handler()));

let listener = tokio::net::TcpListener::bind("127.0.0.1:3000").await?;
axum::serve(listener, app).await?;
```

### 自定义传输

实现自定义传输（TCP、Unix 套接字、WebSocket）：

```rust
use rmcp::transport::Transport;
use tokio::net::TcpListener;

// 查看 examples/transport/ 目录下的 TCP、Unix 套接字、WebSocket 实现示例
```

## 错误处理

### ErrorData 的使用

返回正确的 MCP 错误：

```rust
use rmcp::ErrorData;

fn validate_params(value: &str) -> Result<(), ErrorData> {
    if value.is_empty() {
        return Err(ErrorData::invalid_params("值不能为空"));
    }
    Ok(())
}

async fn call_tool(
    &self,
    request: CallToolRequestParam,
    context: RequestContext<RoleServer>,
) -> Result<CallToolResult, ErrorData> {
    validate_params(&request.name)?;
    
    // 工具执行...
    
    Ok(CallToolResult {
        content: vec![TextContent::text("成功")],
        is_error: Some(false),
    })
}
```

### 与 anyhow 的集成

使用 `anyhow` 处理应用级别的错误：

```rust
use anyhow::{Context, Result};

async fn load_config() -> Result<Config> {
    let content = tokio::fs::read_to_string("config.json")
        .await
        .context("读取配置文件失败")?;
    
    let config: Config = serde_json::from_str(&content)
        .context("解析配置失败")?;
    
    Ok(config)
}
```

## 测试

### 单元测试

为工具和处理程序编写单元测试：

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_calculate_add() {
        let params = Parameters::new(CalculateParams {
            a: 5.0,
            b: 3.0,
            operation: "add".to_string(),
        });
        
        let result = calculate(params).await.unwrap();
        assert_eq!(result, 8.0);
    }
    
    #[tokio::test]
    async fn test_divide_by_zero() {
        let params = Parameters::new(CalculateParams {
            a: 5.0,
            b: 0.0,
            operation: "divide".to_string(),
        });
        
        let result = calculate(params).await;
        assert!(result.is_err());
    }
}
```

### 集成测试

测试完整的服务器交互：

```rust
#[tokio::test]
async fn test_server_list_tools() {
    let handler = MyServerHandler::new();
    let context = RequestContext::default();
    
    let result = handler.list_tools(None, context).await.unwrap();
    
    assert!(!result.tools.is_empty());
    assert!(result.tools.iter().any(|t| t.name == "calculate"));
}
```

## 进度通知

### 报告进度

在长时间运行的操作中发送进度通知：

```rust
use rmcp::model::ProgressNotification;

#[tool]
async fn process_large_file(
    params: Parameters<ProcessParams>,
    context: RequestContext<RoleServer>,
) -> Result<String, String> {
    let total = 100;
    
    for i in 0..=total {
        // 执行工作...
        
        if i % 10 == 0 {
            context.notify_progress(ProgressNotification {
                progress: i,
                total: Some(total),
            }).await.ok();
        }
    }
    
    Ok("处理完成".to_string())
}
```

## OAuth 认证

### OAuth 集成

实现 OAuth 以确保安全访问：

```rust
use rmcp::oauth::{OAuthConfig, OAuthProvider};

let oauth_config = OAuthConfig {
    authorization_endpoint: "https://auth.example.com/authorize".to_string(),
    token_endpoint: "https://auth.example.com/token".to_string(),
    client_id: env::var("CLIENT_ID")?,
    client_secret: env::var("CLIENT_SECRET")?,
    scopes: vec!["read".to_string(), "write".to_string()],
};

let oauth_provider = OAuthProvider::new(oauth_config);
// 查看 examples/servers/complex_auth_sse.rs 获取完整实现
```

## 性能最佳实践

### 异步操作

使用 async/await 进行非阻塞操作：

```rust
#[tool]
async fn fetch_data(params: Parameters<FetchParams>) -> Result<String, String> {
    let client = reqwest::Client::new();
    let response = client
        .get(&params.inner().url)
        .send()
        .await
        .map_err(|e| e.to_string())?;
    
    let text = response.text().await.map_err(|e| e.to_string())?;
    Ok(text)
}
```

### 状态管理

使用 `Arc` 和 `RwLock` 管理共享状态：

```rust
use std::sync::Arc;
use tokio::sync::RwLock;

pub struct ServerState {
    counter: Arc<RwLock<i32>>,
}

impl ServerState {
    pub fn new() -> Self {
        Self {
            counter: Arc::new(RwLock::new(0)),
        }
    }
    
    pub async fn increment(&self) -> i32 {
        let mut counter = self.counter.write().await;
        *counter += 1;
        *counter
    }
}
```

## 日志和追踪

### 配置追踪

为可观测性配置追踪：

```rust
use tracing::{info, warn, error, debug};
use tracing_subscriber;

fn init_logging() {
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::DEBUG)
        .with_target(false)
        .with_thread_ids(true)
        .init();
}

#[tool]
async fn my_tool(params: Parameters<MyParams>) -> String {
    debug!("工具调用参数: {:?}", params);
    info!("处理请求");
    
    // 工具逻辑...
    
    info!("请求处理完成");
    "完成".to_string()
}
```

## 部署

### 二进制文件分发

构建优化的发布版本二进制文件：

```bash
cargo build --release --target x86_64-unknown-linux-gnu
cargo build --release --target x86_64-pc-windows-msvc
cargo build --release --target x86_64-apple-darwin
```

### 跨平台构建

使用 cross 进行跨平台构建：

```bash
cargo install cross
cross build --release --target aarch64-unknown-linux-gnu
```

### Docker 部署

创建一个 Dockerfile：

```dockerfile
FROM rust:1.75 as builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates
COPY --from=builder /app/target/release/my-mcp-server /usr/local/bin/
CMD ["my-mcp-server"]
```

## 其他资源

- [rmcp 文档](https://docs.rs/rmcp)
- [rmcp-macros 文档](https://docs.rs/rmcp-macros)
- [示例仓库](https://github.com/modelcontextprotocol/rust-sdk/tree/main/examples)
- [MCP 规范](https://spec.modelcontextprotocol.io/)
- [Rust 异步书](https://rust-lang.github.io/async-book/)


---
description: '使用官方 github.com/modelcontextprotocol/go-sdk 包构建 Model Context Protocol (MCP) 服务器的最佳实践和模式。'
applyTo: "**/*.go, **/go.mod, **/go.sum"
---

# Go MCP 服务器开发指南

在使用官方 Go SDK 构建 MCP 服务器时，请遵循以下最佳实践和模式。

## 服务器设置

使用 `mcp.NewServer` 创建 MCP 服务器：

```go
import "github.com/modelcontextprotocol/go-sdk/mcp"

server := mcp.NewServer(
    &mcp.Implementation{
        Name:    "my-server",
        Version: "v1.0.0",
    },
    nil, // 或提供 mcp.Options
)
```

## 添加工具

使用 `mcp.AddTool` 并通过结构体定义输入和输出以实现类型安全：

```go
type ToolInput struct {
    Query string `json:"query" jsonschema:"搜索查询"`
    Limit int    `json:"limit,omitempty" jsonschema:"最多返回结果数"`
}

type ToolOutput struct {
    Results []string `json:"results" jsonschema:"搜索结果列表"`
    Count   int      `json:"count" jsonschema:"找到的结果数"`
}

func SearchTool(ctx context.Context, req *mcp.CallToolRequest, input ToolInput) (
    *mcp.CallToolResult,
    ToolOutput,
    error,
) {
    // 实现工具逻辑
    results := performSearch(ctx, input.Query, input.Limit)
    
    return nil, ToolOutput{
        Results: results,
        Count:   len(results),
    }, nil
}

// 注册工具
mcp.AddTool(server, 
    &mcp.Tool{
        Name:        "search",
        Description: "搜索信息",
    },
    SearchTool,
)
```

## 添加资源

使用 `mcp.AddResource` 提供可访问的数据：

```go
func GetResource(ctx context.Context, req *mcp.ReadResourceRequest) (*mcp.ReadResourceResult, error) {
    content, err := loadResourceContent(ctx, req.URI)
    if err != nil {
        return nil, err
    }
    
    return &mcp.ReadResourceResult{
        Contents: []any{
            &mcp.TextResourceContents{
                ResourceContents: mcp.ResourceContents{
                    URI:      req.URI,
                    MIMEType: "text/plain",
                },
                Text: content,
            },
        },
    }, nil
}

mcp.AddResource(server,
    &mcp.Resource{
        URI:         "file:///data/example.txt",
        Name:        "示例数据",
        Description: "示例资源数据",
        MIMEType:    "text/plain",
    },
    GetResource,
)
```

## 添加提示

使用 `mcp.AddPrompt` 注册可重用的提示模板：

```go
type PromptInput struct {
    Topic string `json:"topic" jsonschema:"分析的主题"`
}

func AnalyzePrompt(ctx context.Context, req *mcp.GetPromptRequest, input PromptInput) (
    *mcp.GetPromptResult,
    error,
) {
    return &mcp.GetPromptResult{
        Description: "分析给定主题",
        Messages: []mcp.PromptMessage{
            {
                Role: mcp.RoleUser,
                Content: mcp.TextContent{
                    Text: fmt.Sprintf("分析此主题: %s", input.Topic),
                },
            },
        },
    }, nil
}

mcp.AddPrompt(server,
    &mcp.Prompt{
        Name:        "analyze",
        Description: "分析主题",
        Arguments: []mcp.PromptArgument{
            {
                Name:        "topic",
                Description: "要分析的主题",
                Required:    true,
            },
        },
    },
    AnalyzePrompt,
)
```

## 传输配置

### 标准输入/输出传输

用于通过 stdin/stdout 进行通信（桌面集成最常见）：

```go
if err := server.Run(ctx, &mcp.StdioTransport{}); err != nil {
    log.Fatal(err)
}
```

### HTTP 传输

用于基于 HTTP 的通信：

```go
import "github.com/modelcontextprotocol/go-sdk/mcp"

transport := &mcp.HTTPTransport{
    Addr: ":8080",
    // 可选：配置 TLS、超时等
}

if err := server.Run(ctx, transport); err != nil {
    log.Fatal(err)
}
```

## 错误处理

始终返回适当的错误，并使用上下文进行取消操作：

```go
func MyTool(ctx context.Context, req *mcp.CallToolRequest, input MyInput) (
    *mcp.CallToolResult,
    MyOutput,
    error,
) {
    // 检查上下文取消
    if ctx.Err() != nil {
        return nil, MyOutput{}, ctx.Err()
    }
    
    // 返回无效输入的错误
    if input.Query == "" {
        return nil, MyOutput{}, fmt.Errorf("查询不能为空")
    }
    
    // 执行操作
    result, err := performOperation(ctx, input)
    if err != nil {
        return nil, MyOutput{}, fmt.Errorf("操作失败: %w", err)
    }
    
    return nil, result, nil
}
```

## JSON Schema 标签

使用 `jsonschema` 标签对结构体进行文档说明，以提高客户端集成效果：

```go
type Input struct {
    Name     string   `json:"name" jsonschema:"必需,描述=用户的姓名"`
    Age      int      `json:"age" jsonschema:"最小值=0,最大值=150"`
    Email    string   `json:"email,omitempty" jsonschema:"格式=电子邮件"`
    Tags     []string `json:"tags,omitempty" jsonschema:"唯一项=true"`
    Active   bool     `json:"active" jsonschema:"默认值=true"`
}
```

## 上下文使用

始终尊重上下文的取消和截止时间：

```go
func LongRunningTool(ctx context.Context, req *mcp.CallToolRequest, input Input) (
    *mcp.CallToolResult,
    Output,
    error,
) {
    select {
    case <-ctx.Done():
        return nil, Output{}, ctx.Err()
    case result := <-performWork(ctx, input):
        return nil, result, nil
    }
}
```

## 服务器选项

通过选项配置服务器行为：

```go
options := &mcp.Options{
    Capabilities: &mcp.ServerCapabilities{
        Tools:     &mcp.ToolsCapability{},
        Resources: &mcp.ResourcesCapability{
            Subscribe: true, // 启用资源订阅
        },
        Prompts: &mcp.PromptsCapability{},
    },
}

server := mcp.NewServer(
    &mcp.Implementation{Name: "my-server", Version: "v1.0.0"},
    options,
)
```

## 测试

使用标准的 Go 测试模式测试您的 MCP 工具：

```go
func TestSearchTool(t *testing.T) {
    ctx := context.Background()
    input := ToolInput{Query: "test", Limit: 10}
    
    result, output, err := SearchTool(ctx, nil, input)
    if err != nil {
        t.Fatalf("SearchTool 失败: %v", err)
    }
    
    if len(output.Results) == 0 {
        t.Error("预期有结果，但未获得任何结果")
    }
}
```

## 模块设置

正确初始化您的 Go 模块：

```bash
go mod init github.com/yourusername/yourserver
go get github.com/modelcontextprotocol/go-sdk@latest
```

您的 `go.mod` 文件应包含：

```go
module github.com/yourusername/yourserver

go 1.23

require github.com/modelcontextprotocol/go-sdk v1.0.0
```

## 常见模式

### 日志记录

使用结构化日志记录：

```go
import "log/slog"

logger := slog.Default()
logger.Info("工具调用", "名称", req.Params.Name, "参数", req.Params.Arguments)
```

### 配置

使用环境变量或配置文件：

```go
type Config struct {
    ServerName string
    Version    string
    Port       int
}

func LoadConfig() *Config {
    return &Config{
        ServerName: getEnv("SERVER_NAME", "my-server"),
        Version:    getEnv("VERSION", "v1.0.0"),
        Port:       getEnvInt("PORT", 8080),
    }
}
```

### 平滑关闭

正确处理关闭信号：

```go
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

sigCh := make(chan os.Signal, 1)
signal.Notify(sigCh, os.Interrupt, syscall.SIGTERM)

go func() {
    <-sigCh
    cancel()
}()

if err := server.Run(ctx, transport); err != nil {
    log.Fatal(err)
}
```
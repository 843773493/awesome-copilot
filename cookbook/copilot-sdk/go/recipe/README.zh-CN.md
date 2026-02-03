# 可运行的食谱示例

此文件夹包含每个食谱的独立、可执行的 Go 示例。每个文件都是一个完整的程序，可以直接使用 `go run` 运行。

## 前提条件

- Go 1.21 或更高版本
- GitHub Copilot SDK for Go

```bash
go get github.com/github/copilot-sdk/go
```

## 运行示例

每个 `.go` 文件都是一个完整的、可运行的程序。只需使用：

```bash
go run <filename>.go
```

### 可用的食谱

| 食谱               | 命令                          | 描述                                |
| -------------------- | -------------------------------- | ------------------------------------------ |
| 错误处理       | `go run error-handling.go`       | 展示错误处理模式       |
| 多个会话    | `go run multiple-sessions.go`    | 管理多个独立对话 |
| 管理本地文件 | `go run managing-local-files.go` | 使用 AI 分组组织文件          |
| PR 可视化     | `go run pr-visualization.go`     | 生成 PR 年龄图表                    |
| 持久化会话  | `go run persisting-sessions.go`  | 在重启之间保存和恢复会话   |

### 带参数的示例

**使用特定仓库的 PR 可视化：**

```bash
go run pr-visualization.go -repo github/copilot-sdk
```

**管理本地文件（请先编辑 managing-local-files.go 中的 targetFolder 变量以更改目标文件夹）：**

```bash
# 请先编辑 managing-local-files.go 中的 targetFolder 变量
go run managing-local-files.go
```

## Go 最佳实践

这些示例遵循 Go 的惯例：

- 使用显式检查进行正确的错误处理
- 使用 `defer` 进行清理
- 惯用命名（本地变量使用驼峰命名）
- 在适当的情况下使用标准库
- 清晰的职责分离

## 学习资源

- [Go 文档](https://go.dev/doc/)
- [GitHub Copilot SDK for Go](https://github.com/github/copilot-sdk/blob/main/go/README.md)
- [父食谱](../README.md)

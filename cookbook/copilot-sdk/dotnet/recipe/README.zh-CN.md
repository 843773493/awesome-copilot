# 可运行的食谱示例

此文件夹包含每个食谱的独立、可执行的 C# 示例。这些是 [基于文件的应用程序](https://learn.microsoft.com/dotnet/core/sdk/file-based-apps)，可以直接使用 `dotnet run` 运行。

## 先决条件

- .NET 10.0 或更高版本
- GitHub Copilot SDK 包（自动引用）

## 运行示例

每个 `.cs` 文件都是一个完整的、可运行的程序。只需使用以下命令：

```bash
dotnet run <filename>.cs
```

### 可用的食谱

| 食谱               | 命令                              | 描述                                |
| -------------------- | ------------------------------------ | ------------------------------------------ |
| 错误处理           | `dotnet run error-handling.cs`       | 演示错误处理模式                        |
| 多个会话           | `dotnet run multiple-sessions.cs`    | 管理多个独立的对话                      |
| 管理本地文件       | `dotnet run managing-local-files.cs` | 使用 AI 分组组织文件                    |
| PR 可视化         | `dotnet run pr-visualization.cs`     | 生成 PR 年龄图表                        |
| 会话持久化         | `dotnet run persisting-sessions.cs`  | 在重启之间保存和恢复会话                |

### 带参数的示例

**指定特定仓库的 PR 可视化：**

```bash
dotnet run pr-visualization.cs -- --repo github/copilot-sdk
```

**管理本地文件（编辑文件以更改目标文件夹）：**

```bash
# 首先编辑 managing-local-files.cs 中的 targetFolder 变量
dotnet run managing-local-files.cs
```

## 基于文件的应用程序

这些示例使用了 .NET 的基于文件的应用程序功能，允许单文件 C# 程序：

- 不需要项目文件即可运行
- 自动引用常用包
- 支持顶级语句

## 学习资源

- [.NET 基于文件的应用程序文档](https://learn.microsoft.com/en-us/dotnet/core/sdk/file-based-apps)
- [GitHub Copilot SDK 文档](https://github.com/github/copilot-sdk/blob/main/dotnet/README.md)
- [父食谱](../README.md)



---
description: 'C# 应用程序开发的代码编写规则 by @jgkim999'
applyTo: '**/*.cs'
---

# C# 代码编写规则

## 命名规范 (命名规范)

一致的命名规范是代码可读性的核心。建议遵循 Microsoft 的指导方针。

| 元素 | 命名规范 | 示例 |
|------|-----------|------|
| 接口 | 接头词 'I' + PascalCase | `IAsyncRepository`, `ILogger` |
| 公开(public) 成员 | PascalCase（帕斯卡命名法） | `public int MaxCount;`, `public void GetData()` |
| 参数、局部变量 | camelCase（驼峰命名法） | `int userCount`, `string customerName` |
| 非公开/内部字段 | 下划线(_) + camelCase | `private string _connectionString;` |
| 常量 (const) | PascalCase（帕斯卡命名法） | `public const int DefaultTimeout = 5000;` |
| 泛型类型参数 | 接头词 'T' + 描述性名称 | `TKey`, `TValue`, `TResult` |
| 异步方法 | 'Async' 后缀 | `GetUserAsync`, `DownloadFileAsync` |

## 代码格式与可读性 (格式与可读性)

一致的格式使代码更容易视觉解析。

| 项目 | 规则 | 说明 |
|------|------|------|
| 缩进 | 使用 4 个空格 | 使用空格而非制表符进行缩进。cs 文件必须使用 4 个空格。 |
| 括号 | 始终使用大括号 {} | 即使控制语句（if、for、while 等）仅占一行，也始终使用大括号。 |
| 空行 | 逻辑性分隔 | 在方法定义、属性定义及逻辑性分隔的代码块之间添加空行。 |
| 语句编写 | 每行一个语句 | 每行仅编写一个语句。 |
| var 关键字 | 仅在类型明确时使用 | 仅在变量类型可以从右侧明确推断时使用 var。 |
| 命名空间 | 使用文件范围命名空间 | 在 C# 10 及以上版本中，使用文件范围命名空间以减少不必要的缩进。 |
| 注释 | 编写 XML 格式注释 | 对编写的所有 class 或函数始终添加 XML 格式注释。 |

## 语言功能使用 (语言功能使用)

利用最新的 C# 功能使代码更简洁高效。

| 功能 | 说明 | 示例/参考 |
|------|------|------|
| 异步编程 | 在 I/O 约束操作中使用 async/await | `async Task<string> GetDataAsync()` |
| ConfigureAwait | 减少库代码中的上下文切换开销 | `await SomeMethodAsync().ConfigureAwait(false)` |
| LINQ | 查询和操作集合数据 | `users.Where(u => u.IsActive).ToList()` |
| 表达式体成员 | 简洁地表达简单的方法/属性 | `public string Name => _name;` |
| 可空引用类型 | 防止编译时 NullReferenceException | `#nullable enable` |
| using 声明 | 简洁处理 IDisposable 对象 | `using var stream = new FileStream(...);` |

## 性能与异常处理 (性能与异常处理)

这些指导方针旨在打造坚固且快速的应用程序。

### 异常处理

仅捕获可处理的具体异常。避免使用 `catch (Exception)` 捕获通用异常。

不要将异常用于程序流程控制。异常应仅用于处理意外错误情况。

### 性能
s

在重复连接字符串时，使用 `StringBuilder` 而不是 `+` 运算符。

在使用 Entity Framework Core 时，对于只读查询使用 `.AsNoTracking()` 以提升性能。

避免不必要的对象分配，特别是在循环中要特别注意。

## 安全性 (安全性)

这些是编写安全代码的基本原则。

| 安全领域 | 规则 | 说明 |
|------|------|------|
| 输入验证 | 验证所有外部数据 | 从外部（用户、API 等）传入的所有数据都不可信任，必须始终进行验证。 |
| 防止 SQL 注入 | 使用参数化查询 | 始终使用参数化查询或 Entity Framework 等 ORM 工具防止 SQL 注入攻击。 |
| 保护敏感数据 | 使用配置管理工具 | 密码、连接字符串、API 密钥等不应硬编码在源代码中，而应使用 Secret Manager、Azure Key Vault 等工具。 |

应将这些规则整合到项目的 `.editorconfig` 文件和团队的代码审查流程中，以持续保持高质量代码。
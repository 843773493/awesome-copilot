

---
description: '处理 .NET Framework 项目的指南。包括项目结构、C# 语言版本、NuGet 管理以及最佳实践。'
applyTo: '**/*.csproj, **/*.cs'
---

# .NET Framework 开发

## 构建和编译要求
- 始终使用 `msbuild /t:rebuild` 来构建解决方案或项目，而不是使用 `dotnet build`

## 项目文件管理

### 非 SDK 风格的项目结构
.NET Framework 项目使用传统的项目格式，与现代 SDK 风格的项目有显著差异：

- **显式文件包含**：所有新源文件 **必须** 通过 `<Compile>` 元素显式添加到项目文件（`.csproj`）中
  - .NET Framework 项目不会像 SDK 风格的项目那样自动包含目录中的文件
  - 示例：`<Compile Include="Path\To\NewFile.cs" />`

- **无隐式导入**：与 SDK 风格的项目不同，.NET Framework 项目不会自动导入常用命名空间或程序集

- **构建配置**：包含显式的 `<PropertyGroup>` 部分用于 Debug/Release 配置

- **输出路径**：显式的 `<OutputPath>` 和 `<IntermediateOutputPath>` 定义

- **目标框架**：使用 `<TargetFrameworkVersion>` 而不是 `<TargetFramework>`
  - 示例：`<TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>`

## NuGet 包管理
- 在 .NET Framework 项目中安装和更新 NuGet 包是一项复杂的任务，需要对多个文件进行协调修改。因此，**不要尝试在此项目中安装或更新 NuGet 包**。
- 如果需要修改 NuGet 引用，请建议用户通过 Visual Studio 的 NuGet 包管理器或包管理器控制台进行安装或更新操作。
- 推荐 NuGet 包时，确保它们兼容 .NET Framework 或 .NET Standard 2.0（而不仅仅是 .NET Core 或 .NET 5+）。

## C# 语言版本为 7.3
- 本项目仅支持 C# 7.3 特性，请避免使用以下特性：

### C# 8.0+ 特性（不支持）：
  - 使用声明 (`using var stream = ...`)
  - 异步使用声明 (`await using var resource = ...`)
  - Switch 表达式 (`variable switch { ... }`)
  - 空合并赋值 (`??=`)
  - 范围和索引运算符 (`array[1..^1]`, `array[^1]`)
  - 默认接口方法
  - 结构体中的只读成员
  - 静态本地函数
  - 可空引用类型 (`string?`, `#nullable enable`)

### C# 9.0+ 特性（不支持）：
  - 记录类型 (`public record Person(string Name)`)
  - 只初始化属性 (`{ get; init; }`)
  - 顶级程序（无 Main 方法的程序）
  - 模式匹配增强功能
  - 目标类型 new 表达式 (`List<string> list = new()`)

### C# 10+ 特性（不支持）：
  - 全局 using 声明
  - 文件作用域命名空间
  - 记录结构体
  - 必需成员

### 替代方案（C# 7.3 兼容）：
  - 使用带大括号的传统 using 声明
  - 使用 switch 语句而非 switch 表达式
  - 使用显式空检查而非空合并赋值
  - 使用手动索引进行数组切片
  - 使用抽象类或接口而非默认接口方法

## 环境注意事项（Windows 环境）
- 使用带反斜杠的 Windows 风格路径（例如：`C:\path\to\file.cs`）
- 在建议终端操作时使用适用于 Windows 的命令
- 在处理文件系统操作时考虑 Windows 特有的行为

## 常见 .NET Framework 洞察与最佳实践

### 异步/等待模式
- **ConfigureAwait(false)**：在库代码中始终使用 `ConfigureAwait(false)` 以避免死锁：
  ```csharp
  var result = await SomeAsyncMethod().ConfigureAwait(false);
  ```
- **避免同步调用异步方法**：不要使用 `.Result` 或 `.Wait()` 或 `.GetAwaiter().GetResult()`。这些同步调用异步方法的模式可能导致死锁和性能问题。始终使用 `await` 进行异步调用。

### 日期时间处理
- **使用 DateTimeOffset 用于时间戳**：对于绝对时间点，优先使用 `DateTimeOffset` 而不是 `DateTime`
- **指定 DateTimeKind**：在使用 `DateTime` 时，始终指定 `DateTimeKind.Utc` 或 `DateTimeKind.Local`
- **文化感知格式化**：在序列化/解析时使用 `CultureInfo.InvariantCulture`

### 字符串操作
- **使用 StringBuilder 进行字符串拼接**：对于多次字符串拼接操作，使用 `StringBuilder`
- **StringComparison**：在字符串操作中始终指定 `StringComparison`：
  ```csharp
  string.Equals(other, StringComparison.OrdinalIgnoreCase)
  ```

### 内存管理
- **实现 IDisposable 模式**：对非托管资源，正确实现 `IDisposable` 接口
- **使用 using 语句**：始终将 `IDisposable` 对象包裹在 using 语句中
- **避免大对象堆分配**：保持对象小于 85KB 以避免 LOH 分配

### 配置管理
- **使用 ConfigurationManager**：通过 `ConfigurationManager.AppSettings` 访问应用程序设置
- **连接字符串**：存储在 `<connectionStrings>` 部分，而不是 `<appSettings>`
- **转换配置**：使用 web.config/app.config 转换来处理环境特定的配置

### 异常处理
- **捕获特定异常类型**：不要捕获通用的 `Exception`
- **不要吞没异常**：始终适当地记录或重新抛出异常
- **使用 using 管理可释放资源**：确保即使发生异常也能正确清理资源

### 性能注意事项
- **避免装箱操作**：注意值类型和泛型中的装箱/拆箱操作
- **字符串内联**：对频繁使用的字符串谨慎使用 `string.Intern()`
- **延迟初始化**：使用 `Lazy<T>` 进行昂贵的对象创建
- **避免在热路径中使用反射**：尽可能缓存 `MethodInfo`、`PropertyInfo` 对象
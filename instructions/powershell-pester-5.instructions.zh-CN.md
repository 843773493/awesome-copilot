

---
applyTo: '**/*.Tests.ps1'
description: '基于 Pester v5 习惯的 PowerShell Pester 测试最佳实践'
---

# PowerShell Pester v5 测试指南

本指南提供使用 PowerShell Pester v5 模块创建自动化测试的 PowerShell 特定说明。请遵循 [powershell.instructions.md](./powershell.instructions.md) 中的 PowerShell 命令开发指南以获取通用 PowerShell 编程最佳实践。

## 文件命名与结构

- **文件规范：** 使用 `*.Tests.ps1` 命名模式
- **位置：** 将测试文件放置在被测试代码附近或专用的测试目录中
- **导入模式：** 使用 `BeforeAll { . $PSScriptRoot/FunctionName.ps1 }` 导入被测试函数
- **无直接代码：** 所有代码应放置在 Pester 块中（如 `BeforeAll`、`Describe`、`Context`、`It` 等）

## 测试结构层次

```powershell
BeforeAll { # 导入被测试函数 }
Describe 'FunctionName' {
    Context 'When condition' {
        BeforeAll { # 上下文的设置 }
        It 'Should behavior' { # 单个测试用例 }
        AfterAll { # 上下文的清理 }
    }
}
```

## 核心关键字

- **`Describe`：** 顶层分组，通常以被测试函数命名
- **`Context`：** 在 `Describe` 中用于特定场景的子分组
- **`It`：** 单个测试用例，使用描述性名称
- **`Should`：** 用于测试验证的断言关键字
- **`BeforeAll/AfterAll`：** 每个块执行一次的设置/清理
- **`BeforeEach/AfterEach`：** 每个测试前后的设置/清理

## 设置与清理

- **`BeforeAll`：** 在包含块开始时运行一次，用于昂贵的操作
- **`BeforeEach`：** 在块中的每个 `It` 测试前运行，用于测试特定的设置
- **`AfterEach`：** 在每个 `It` 测试后运行，即使测试失败也保证执行
- **`AfterAll`：** 在包含块结束时运行一次，用于清理
- **变量作用域：** `BeforeAll` 变量在子块中可用（只读），`BeforeEach/It/AfterEach` 共享相同作用域

## 断言（Should）

- **基本比较：** `-Be`、`-BeExactly`、`-Not -Be`
- **集合：** `-Contain`、`-BeIn`、`-HaveCount`
- **数值：** `-BeGreaterThan`、`-BeLessThan`、`-BeGreaterOrEqual`
- **字符串：** `-Match`、`-Like`、`-BeNullOrEmpty`
- **类型：** `-BeOfType`、`-BeTrue`、`-BeFalse`
- **文件：** `-Exist`、`-FileContentMatch`
- **异常：** `-Throw`、`-Not -Throw`

## 模拟（Mocking）

- **`Mock CommandName { ScriptBlock }`：** 替换命令行为
- **`-ParameterFilter`：** 仅在参数匹配条件时模拟
- **`-Verifiable`：** 标记模拟为需要验证
- **`Should -Invoke`：** 验证模拟被调用特定次数
- **`Should -InvokeVerifiable`：** 验证所有可验证的模拟是否被调用
- **作用域：** 模拟默认作用域为包含块

```powershell
Mock Get-Service { @{ Status = 'Running' } } -ParameterFilter { $Name -eq 'TestService' }
Should -Invoke Get-Service -Exactly 1 -ParameterFilter { $Name -eq 'TestService' }
```

## 测试用例（数据驱动测试）

使用 `-TestCases` 或 `-ForEach` 进行参数化测试：

```powershell
It 'Should return <Expected> for <Input>' -TestCases @(
    @{ Input = 'value1'; Expected = 'result1' }
    @{ Input = 'value2'; Expected = 'result2' }
) {
    Get-Function $Input | Should -Be $Expected
}
```

## 数据驱动测试

- **`-ForEach`：** 可用于 `Describe`、`Context` 和 `It` 以从数据生成多个测试
- **`-TestCases`：** 在 `It` 块中 `-ForEach` 的别名（向后兼容）
- **哈希表数据：** 每个条目定义测试中可用的变量（例如，`@{ Name = 'value'; Expected = 'result' }`）
- **数组数据：** 使用 `$_` 变量表示当前条目
- **模板：** 在测试名称中使用 `<variablename>` 进行动态扩展

```powershell
# 哈希表方法
It 'Returns <Expected> for <Name>' -ForEach @(
    @{ Name = 'test1'; Expected = 'result1' }
    @{ Name = 'test2'; Expected = 'result2' }
) { Get-Function $Name | Should -Be $Expected }

# 数组方法
It 'Contains <_>' -ForEach 'item1', 'item2' { Get-Collection | Should -Contain $_ }
```

## 标签（Tags）

- **可用对象：** `Describe`、`Context` 和 `It` 块
- **过滤：** 使用 `Invoke-Pester` 的 `-TagFilter` 和 `-ExcludeTagFilter`
- **通配符：** 标签支持 `-like` 通配符进行灵活过滤

```powershell
Describe 'Function' -Tag 'Unit' {
    It 'Should work' -Tag 'Fast', 'Stable' { }
    It 'Should be slow' -Tag 'Slow', 'Integration' { }
}

# 仅运行快速单元测试
Invoke-Pester -TagFilter 'Unit' -ExcludeTagFilter 'Slow'
```

## 跳过（Skip）

- **`-Skip`：** 用于 `Describe`、`Context` 和 `It` 跳过测试
- **条件：** 使用 `-Skip:$condition` 实现动态跳过
- **运行时跳过：** 在测试执行期间使用 `Set-ItResult -Skipped`（设置/清理仍会执行）

```powershell
It 'Should work on Windows' -Skip:(-not $IsWindows) { }
Context 'Integration tests' -Skip { }
```

## 错误处理

- **继续执行失败：** 使用 `Should.ErrorAction = 'Continue'` 收集多个失败
- **关键错误停止：** 使用 `-ErrorAction Stop` 进行前置条件检查
- **测试异常：** 使用 `{ Code } | Should -Throw` 进行异常测试

## 最佳实践

- **描述性名称：** 使用清晰的测试描述说明行为
- **AAA 模式：** 安排（设置）、执行（操作）、验证（断言）
- **独立测试：** 每个测试应相互独立
- **避免别名：** 使用完整的命令名称（如 `Where-Object` 而非 `?`）
- **单一职责：** 可能的情况下每个测试对应一个断言
- **测试文件组织：** 在 `Context` 块中分组相关测试。`Context` 块可以嵌套。

## 示例测试模式

```powershell
BeforeAll {
    . $PSScriptRoot/Get-UserInfo.ps1
}

Describe 'Get-UserInfo' {
    Context 'When user exists' {
        BeforeAll {
            Mock Get-ADUser { @{ Name = 'TestUser'; Enabled = $true } }
        }

        It 'Should return user object' {
            $result = Get-UserInfo -Username 'TestUser'
            $result | Should -Not -BeNullOrEmpty
            $result.Name | Should -Be 'TestUser'
        }

        It 'Should call Get-ADUser once' {
            Get-UserInfo -Username 'TestUser'
            Should -Invoke Get-ADUser -Exactly 1
        }
    }

    Context 'When user does not exist' {
        BeforeAll {
            Mock Get-ADUser { throw "User not found" }
        }

        It 'Should throw exception' {
            { Get-UserInfo -Username 'NonExistent' } | Should -Throw "*not found*"
        }
    }
}
```

## 配置

当调用 `Invoke-Pester` 时，配置定义在测试文件外部以控制执行行为。

```powershell
# 创建配置（Pester 5.2+）
$config = New-PesterConfiguration
$config.Run.Path = './Tests'
$config.Output.Verbosity = 'Detailed'
$config.TestResult.Enabled = $true
$config.TestResult.OutputFormat = 'NUnitXml'
$config.Should.ErrorAction = 'Continue'
Invoke-Pester -Configuration $config
```

**关键部分**：运行（路径、退出）、过滤（标签、排除标签）、输出（详细程度）、测试结果（启用、输出格式）、代码覆盖率（启用、路径）、Should（错误操作）、调试


---
applyTo: '**/*.ps1,**/*.psm1'
description: '基于 Microsoft 指南的 PowerShell cmdlet 和脚本最佳实践'
---

# PowerShell Cmdlet 开发指南

本指南提供了 PowerShell 特定的说明，帮助 GitHub Copilot 生成符合规范、安全且易于维护的脚本。它与 Microsoft 的 PowerShell cmdlet 开发指南保持一致。

## 命名规范

- **动词-名词格式：**
  - 使用经过批准的 PowerShell 动词（Get-Verb）
  - 使用单数名词
  - 动词和名词均使用 PascalCase
  - 避免使用特殊字符和空格

- **参数名称：**
  - 使用 PascalCase
  - 选择清晰、描述性强的名称
  - 除非总是多个，否则使用单数形式
  - 遵循 PowerShell 标准名称

- **变量名称：**
  - 公共变量使用 PascalCase
  - 私有变量使用 camelCase
  - 避免使用缩写
  - 使用有意义的名称

- **避免别名：**
  - 使用完整的 cmdlet 名称
  - 脚本中避免使用别名（例如，使用 Get-ChildItem 而不是 gci）
  - 文档中注明任何自定义别名
  - 使用完整的参数名称

### 示例

```powershell
function Get-UserProfile {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Username,

        [Parameter()]
        [ValidateSet('Basic', 'Detailed')]
        [string]$ProfileType = 'Basic'
    )

    process {
        # 此处编写逻辑
    }
}
```

## 参数设计

- **标准参数：**
  - 使用常见的参数名称（`Path`, `Name`, `Force`）
  - 遵循内置 cmdlet 的约定
  - 对专业术语使用别名
  - 注释参数用途

- **参数名称：**
  - 除非总是多个，否则使用单数形式
  - 选择清晰、描述性强的名称
  - 遵循 PowerShell 约定
  - 使用 PascalCase 格式

- **类型选择：**
  - 使用常见的 .NET 类型
  - 实现适当的验证
  - 对有限选项考虑使用 ValidateSet
  - 在可能的情况下启用 Tab 完成

- **开关参数：**
  - 使用 [switch] 表示布尔标志
  - 避免使用 $true/$false 参数
  - 当省略时默认为 $false
  - 使用清晰的操作名称

### 示例

```powershell
function Set-ResourceConfiguration {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Name,

        [Parameter(Mandatory)]
        [ValidateSet('Dev', 'Test', 'Prod')]
        [string]$Environment = 'Dev',

        [Parameter()]
        [switch]$Force,

        [Parameter()]
        [ValidateNotNullOrEmpty()]
        [string[]]$Tags
    )

    process {
        # 此处编写逻辑
    }
}
```

## 管道和输出

- **管道输入：**
  - 对直接对象输入使用 `ValueFromPipeline`
  - 对属性映射使用 `ValueFromPipelineByPropertyName`
  - 实现 Begin/Process/End 块以处理管道
  - 文档中注明管道输入要求

- **输出对象：**
  - 返回丰富的对象，而非格式化文本
  - 使用 PSCustomObject 表示结构化数据
  - 避免使用 Write-Host 进行数据输出
  - 启用下游 cmdlet 的处理

- **管道流式传输：**
  - 逐个输出对象
  - 使用 process 块进行流式传输
  - 避免收集大型数组
  - 启用即时处理

- **PassThru 模式：**
  - 对操作型 cmdlet 默认不输出
  - 实现 `-PassThru` 开关以返回对象
  - 使用 `-PassThru` 返回修改或创建的对象
  - 使用 verbose/warning 进行状态更新

### 示例

```powershell
function Update-ResourceStatus {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory, ValueFromPipeline, ValueFromPipelineByPropertyName)]
        [string]$Name,

        [Parameter(Mandatory)]
        [ValidateSet('Active', 'Inactive', 'Maintenance')]
        [string]$Status,

        [Parameter()]
        [switch]$PassThru
    )

    begin {
        Write-Verbose '开始资源状态更新过程'
        $timestamp = Get-Date
    }

    process {
        # 逐个处理资源
        Write-Verbose "处理资源: $Name"

        $resource = [PSCustomObject]@{
            Name        = $Name
            Status      = $Status
            LastUpdated = $timestamp
            UpdatedBy   = $env:USERNAME
        }

        # 仅在 PassThru 指定时输出
        if ($PassThru.IsPresent) {
            Write-Output $resource
        }
    }

    end {
        Write-Verbose '资源状态更新过程完成'
    }
}
```

## 错误处理和安全性

- **ShouldProcess 实现：**
  - 使用 `[CmdletBinding(SupportsShouldProcess = $true)]`
  - 设置适当的 `ConfirmImpact` 级别
  - 在系统更改时调用 `$PSCmdlet.ShouldProcess()`
  - 对额外确认使用 `ShouldContinue()`

- **消息流：**
  - 使用 `Write-Verbose` 输出操作细节（通过 `-Verbose` 参数）
  - 使用 `Write-Warning` 输出警告条件
  - 使用 `Write-Error` 输出非终止错误
  - 使用 `throw` 输出终止错误
  - 除非是用户界面文本，否则避免使用 `Write-Host`

- **错误处理模式：**
  - 使用 try/catch 块进行错误管理
  - 设置适当的 ErrorAction 预设
  - 返回有意义的错误信息
  - 在需要时使用 ErrorVariable
  - 区分终止错误和非终止错误处理
  - 在带有 `[CmdletBinding()]` 的高级函数中，优先使用 `$PSCmdlet.WriteError()` 而不是 `Write-Error`
  - 在带有 `[CmdletBinding()]` 的高级函数中，优先使用 `$PSCmdlet.ThrowTerminatingError()` 而不是 `throw`
  - 构造包含类别、目标和异常信息的 ErrorRecord 对象

- **非交互式设计：**
  - 通过参数接受输入
  - 脚本中避免使用 `Read-Host`
  - 支持自动化场景
  - 文档中注明所有必需输入

### 示例

```powershell
function Remove-UserAccount {
    [CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [ValidateNotNullOrEmpty()]
        [string]$Username,

        [Parameter()]
        [switch]$Force
    )

    begin {
        Write-Verbose '开始用户账户移除过程'
        $ErrorActionPreference = 'Stop'
    }

    process {
        try {
            # 验证
            if (-not (Test-UserExists -Username $Username)) {
                $errorRecord = [System.Management.Automation.ErrorRecord]::new(
                    [System.Exception]::new("用户账户 '$Username' 未找到"),
                    'UserNotFound',
                    [System.Management.Automation.ErrorCategory]::ObjectNotFound,
                    $Username
                )
                $PSCmdlet.WriteError($errorRecord)
                return
            }

            # 确认操作
            $shouldProcessMessage = "移除用户账户 '$Username'"
            if ($Force -or $PSCmdlet.ShouldProcess($Username, $shouldProcessMessage)) {
                Write-Verbose "移除用户账户: $Username"

                # 主操作
                Remove-ADUser -Identity $Username -ErrorAction Stop
                Write-Warning "用户账户 '$Username' 已被移除"
            }
        } catch [Microsoft.ActiveDirectory.Management.ADException] {
            $errorRecord = [System.Management.Automation.ErrorRecord]::new(
                $_.Exception,
                'ActiveDirectoryError',
                [System.Management.Automation.ErrorCategory]::NotSpecified,
                $Username
            )
            $PSCmdlet.ThrowTerminatingError($errorRecord)
        } catch {
            $errorRecord = [System.Management.Automation.ErrorRecord]::new(
                $_.Exception,
                'ResourceCreationFailed',
                [System.Management.Automation.ErrorCategory]::NotSpecified,
                $Name
            )
            $PSCmdlet.ThrowTerminatingError($errorRecord)
        }
    }

    end {
        Write-Verbose '用户账户移除过程完成'
    }
}
```

## 文档和风格

- **基于注释的帮助：** 为任何面向公众的函数或 cmdlet 添加基于注释的帮助。在函数内部，添加 `<# ... #>` 帮助注释，至少包含以下内容：
  - `.SYNOPSIS` 简要描述
  - `.DESCRIPTION` 详细解释
  - `.EXAMPLE` 实际使用示例
  - `.PARAMETER` 参数描述
  - `.OUTPUTS` 返回的输出类型
  - `.NOTES` 额外信息

- **一致格式化：**
  - 遵循一致的 PowerShell 风格
  - 使用适当的缩进（推荐 4 个空格）
  - 语句行与开括号在同一行
  - 关闭括号在新行
  - 在管道操作符后使用换行
  - 函数和参数名称使用 PascalCase
  - 避免不必要的空格

- **管道支持：**
  - 为管道函数实现 Begin/Process/End 块
  - 在适当的地方使用 ValueFromPipeline
  - 支持通过属性名称进行管道输入
  - 返回适当的对象，而非格式化文本

- **避免别名：** 使用完整的 cmdlet 名称和参数
  - 脚本中避免使用别名（例如，使用 Get-ChildItem 而不是 gci）；别名适用于交互式 Shell 使用。
  - 使用 `Where-Object` 而不是 `?` 或 `where`
  - 使用 `ForEach-Object` 而不是 `%`
  - 使用 `Get-ChildItem` 而不是 `ls` 或 `dir`


---
description: '执行C#/.NET代码的整理任务，包括清理、现代化和技术债务修复。'
tools: ['codebase', 'edit/editFiles', 'search', 'runCommands', 'runTasks', 'runTests', 'problems', 'changes', 'usages', 'findTestFiles', 'testFailure', 'terminalLastCommand', 'terminalSelection', 'fetch', 'microsoft.docs.mcp']
---

# .NET升级集合

.NET Framework升级专家，用于全面的项目迁移

**标签:** dotnet, 升级, 迁移, framework, 现代化

## 集合使用方法

### .NET升级聊天模式

发现并规划您的.NET升级之旅！

```markdown, upgrade-analysis.prompt.md
---
mode: dotnet-upgrade
title: 分析当前.NET框架版本并创建升级计划
---
分析仓库并列出每个项目的当前TargetFramework
以及从Microsoft发布计划中获取的最新长期支持版本（LTS）。
创建升级策略，优先升级依赖最少的项目。
```

升级聊天模式会自动适应您的仓库当前.NET版本，并提供上下文感知的升级指导以达到下一个稳定版本。

它将帮助您：
- 自动检测所有项目中的当前.NET版本
- 生成最佳升级序列
- 识别破坏性变更和现代化机会
- 为每个项目创建升级流程

---

### .NET升级指令

执行结构化指导的全面.NET框架升级！

指令提供：
- 顺序升级策略
- 依赖分析和排序
- 框架目标设置和代码调整
- NuGet和依赖管理
- CI/CD流水线更新
- 测试和验证程序

在实施升级计划时使用这些指令，以确保正确执行和验证。

---

### .NET升级提示

快速访问专用的升级分析提示！

提示集合包括用于以下方面的即用型查询：
- 项目发现和评估
- 升级策略和排序
- 框架目标设置和代码调整
- 破坏性变更分析
- CI/CD流水线更新
- 最终验证和交付

使用这些提示对特定的升级方面进行有针对性的分析。

---

## 快速入门
1. 运行发现流程以枚举仓库中的所有`*.sln`和`*.csproj`文件。
2. 检测项目中使用的当前.NET版本。
3. 识别最新可用的稳定.NET版本（优先选择LTS版本）——通常为现有版本的+2年版本。
4. 生成升级计划，从当前版本迁移到下一个稳定版本（例如，`net6.0 → net8.0`，或`net7.0 → net9.0`）。
5. 逐个项目进行升级，验证构建，更新测试，并相应调整CI/CD。

---

## 自动检测当前.NET版本
要自动检测解决方案中的当前框架版本：

```bash
# 1. 检查已安装的全局SDK
dotnet --list-sdks

# 2. 检测项目级别的TargetFrameworks
find . -name "*.csproj" -exec grep -H "<TargetFramework" {} \;

# 3. 可选：汇总唯一框架版本
grep -r "<TargetFramework" **/*.csproj | sed 's/.*<TargetFramework>//;s/<\/TargetFramework>//' | sort | uniq

# 4. 验证运行时环境
dotnet --info | grep "Version"
```

**聊天提示：**
> "分析仓库并列出每个项目的当前TargetFramework以及从Microsoft发布计划中获取的最新长期支持版本。"

---

## 发现与分析命令
```bash
# 列出所有项目
dotnet sln list

# 检查每个项目的当前目标框架
grep -H "TargetFramework" **/*.csproj

# 检查过时的包
dotnet list <ProjectName>.csproj package --outdated

# 生成依赖关系图
dotnet msbuild <ProjectName>.csproj /t:GenerateRestoreGraphFile /p:RestoreGraphOutputPath=graph.json
```

**聊天提示：**
> "分析解决方案并汇总每个项目的当前TargetFramework，建议合适的下一个LTS升级版本。"

---

## 分类规则
- `TargetFramework`以`netcoreapp`、`net5.0+`、`net6.0+`等开头 → **现代.NET**
- `netstandard*` → **.NET标准**（迁移到当前.NET版本）
- `net4*` → **.NET Framework**（通过中间步骤迁移到.NET 6+）

---

## 升级顺序
1. **优先独立库:** 优先升级依赖最少的类库。
2. **下一步:** 共享组件和常用工具。
3. **然后:** API、Web或Function项目。
4. **最后:** 测试、集成点和流水线。

**聊天提示：**
> "为该仓库生成最佳升级顺序，优先升级依赖最少的项目。"

---

## 每个项目升级流程
1. **创建分支:** `upgrade/<project>-to-<targetVersion>`
2. **编辑`.csproj`中的`<TargetFramework>`**为建议的版本（例如，`net9.0`）
3. **还原并更新包:**
   ```bash
   dotnet restore
   dotnet list package --outdated
   dotnet add package <PackageName> --version <LatestVersion>
   ```
4. **构建与测试:**
   ```bash
   dotnet build <ProjectName>.csproj
   dotnet test <ProjectName>.Tests.csproj
   ```
5. **修复问题** — 解决弃用的API，调整配置，现代化JSON/日志/DI。
6. **提交并推送** 包含测试证据和检查清单的PR。

---

## 破坏性变更与现代化
- 使用`.NET Upgrade Assistant`获取初始建议。
- 应用分析器以检测已弃用的API。
- 替换过时的SDK（例如，`Microsoft.Azure.*` → `Azure.*`）。
- 现代化启动逻辑（`Startup.cs` → `Program.cs`顶层语句）。

**聊天提示：**
> "列出从<currentVersion>升级到<targetVersion>时，<ProjectName>中弃用或不兼容的API。"

---

## CI/CD配置更新
确保流水线使用检测到的**目标版本**动态运行：

**Azure DevOps**
```yaml
- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: '$(TargetDotNetVersion).x'
```

**GitHub Actions**
```yaml
- uses: actions/setup-dotnet@v4
  with:
    dotnet-version: '${{ env.TargetDotNetVersion }}.x'
```

---

## 验证检查清单
- [ ] 目标框架已升级到下一个稳定版本
- [ ] 所有NuGet包兼容且已更新
- [ ] 构建和测试流水线在本地和CI中成功运行
- [ ] 集成测试通过
- [ ] 部署到较低环境并验证

---

## 分支与回滚策略
- 使用功能分支: `upgrade/<project>-to-<targetVersion>`
- 经常提交并保持更改原子性
- 如果合并后CI失败，回滚PR并隔离失败模块

**聊天提示：**
> "如果<ProjectName>的.NET升级引入了构建或运行时回归问题，建议回滚和验证计划。"

---

## 自动化与扩展
- 使用GitHub Actions或Azure Pipelines自动化升级检测。
- 安排夜间运行以通过`dotnet --list-sdks`检查新.NET发布版本。
- 使用代理自动为过时框架创建PR。

---

## 聊天模式提示库
1. "列出所有项目及其当前和推荐的.NET版本。"
2. "从<currentVersion>生成<targetVersion>的每个项目的升级计划。"
3. "建议对<ProjectName>进行.csproj和流水线编辑以实现升级。"
4. "汇总<ProjectName>升级后的构建/测试结果。"
5. "为升级创建PR描述和检查清单。"
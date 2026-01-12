

---
description: '使用 Community.VisualStudio.Toolkit 开发 Visual Studio 扩展 (VSIX) 的指南'
applyTo: '**/*.cs, **/*.vsct, **/*.xaml, **/source.extension.vsixmanifest'
---

# 使用 Community.VisualStudio.Toolkit 进行 Visual Studio 扩展开发

## 范围

**这些说明仅适用于使用 `Community.VisualStudio.Toolkit` 的 Visual Studio 扩展。**

请通过以下方式验证项目是否使用了该工具包：
- `Community.VisualStudio.Toolkit.*` NuGet 包引用
- `ToolkitPackage` 基类（而非原始 `AsyncPackage`）
- `BaseCommand<T>` 模式用于命令

**如果项目直接使用原始 VSSDK（`AsyncPackage`）或新 `VisualStudio.Extensibility` 模型，请不要应用这些说明。**

## 目标

- 生成以异步优先、线程安全的扩展代码
- 使用工具包抽象（`VS.*` 辅助类、`BaseCommand<T>`、`BaseOptionModel<T>`）
- 确保所有 UI 尊重 Visual Studio 主题
- 遵循 VSSDK 和 VSTHRD 分析器规则
- 生成可测试、可维护的扩展代码

## 示例提示行为

### ✅ 建议
- "使用 `BaseCommand<T>` 创建一个打开当前文件所在文件夹的命令"
- "使用 `BaseOptionModel<T>` 添加一个带有布尔设置的选项页面"
- "为 C# 文件编写一个标记提供者，突出显示 TODO 注释"
- "在处理文件时显示状态栏进度指示器"

### ❌ 避免
- 建议使用原始 `AsyncPackage` 而非 `ToolkitPackage`
- 直接使用 `OleMenuCommandService` 而非 `BaseCommand<T>`
- 在创建/修改 WPF 元素前不切换到 UI 线程
- 在 UI 工作中使用 `.Result`、`.Wait()` 或 `Task.Run`
- 硬编码颜色而非使用 VS 主题颜色

## 项目结构

```
src/
├── Commands/           # 命令处理程序（菜单项、工具栏按钮）
├── Options/            # 设置/选项页面
├── Services/           # 业务逻辑和服务
├── Tagging/            # ITagger 实现（语法高亮、大纲）
├── Adornments/         # 编辑器装饰（IntraTextAdornment、边距）
├── QuickInfo/          # 快速信息/工具提示提供者
├── SuggestedActions/   # 灯泡建议
├── Handlers/           # 事件处理程序（格式化文档、粘贴等）
├── Resources/          # 图像、图标、许可证文件
├── source.extension.vsixmanifest  # 扩展清单
├── VSCommandTable.vsct            # 命令定义（菜单、按钮）
├── VSCommandTable.cs              # 自动生成的命令 ID
└── *Package.cs                    # 主包类
```

## Community.VisualStudio.Toolkit 模式

### 全局 using 语句

使用工具包的扩展应在包文件中包含以下全局 using 语句：

```csharp
global using System;
global using Community.VisualStudio.Toolkit;
global using Microsoft.VisualStudio.Shell;
global using Task = System.Threading.Tasks.Task;
```

### 包类

```csharp
[PackageRegistration(UseManagedResourcesOnly = true, AllowsBackgroundLoading = true)]
[InstalledProductRegistration(Vsix.Name, Vsix.Description, Vsix.Version)]
[ProvideMenuResource("Menus.ctmenu", 1)]
[Guid(PackageGuids.YourExtensionString)]
[ProvideOptionPage(typeof(OptionsProvider.GeneralOptions), Vsix.Name, "General", 0, 0, true, SupportsProfiles = true)]
public sealed class YourPackage : ToolkitPackage
{
    protected override async Task InitializeAsync(CancellationToken cancellationToken, IProgress<ServiceProgressData> progress)
    {
        await this.RegisterCommandsAsync();
    }
}
```

### 命令

命令使用 `[Command]` 特性并继承自 `BaseCommand<T>`：

```csharp
[Command(PackageIds.YourCommandId)]
internal sealed class YourCommand : BaseCommand<YourCommand>
{
    protected override async Task ExecuteAsync(OleMenuCmdEventArgs e)
    {
        // 命令实现
    }

    // 可选：控制命令状态（启用、选中、可见）
    protected override void BeforeQueryStatus(EventArgs e)
    {
        Command.Checked = someCondition;
        Command.Enabled = anotherCondition;
    }
}
```

### 选项页面

```csharp
internal partial class OptionsProvider
{
    [ComVisible(true)]
    public class GeneralOptions : BaseOptionPage<General> { }
}

public class General : BaseOptionModel<General>
{
    [Category("分类名称")]
    [DisplayName("设置名称")]
    [Description("设置的描述。")]
    [DefaultValue(true)]
    public bool MySetting { get; set; } = true;
}
```

## MEF 组件

### 标记提供者

使用 `[Export]` 和适当的 `[ContentType]` 特性：

```csharp
[Export(typeof(IViewTaggerProvider))]
[ContentType("CSharp")]
[ContentType("Basic")]
[TagType(typeof(IntraTextAdornmentTag))]
[TextViewRole(PredefinedTextViewRoles.Document)]
internal sealed class YourTaggerProvider : IViewTaggerProvider
{
    [Import]
    internal IOutliningManagerService OutliningManagerService { get; set; }

    public ITagger<T> CreateTagger<T>(ITextView textView, ITextBuffer buffer) where T : ITag
    {
        if (textView == null || !(textView is IWpfTextView wpfTextView))
            return null;

        if (textView.TextBuffer != buffer)
            return null;

        return wpfTextView.Properties.GetOrCreateSingletonProperty(
            () => new YourTagger(wpfTextView)) as ITagger<T>;
    }
}
```

### 快速信息源

```csharp
[Export(typeof(IAsyncQuickInfoSourceProvider))]
[Name("YourQuickInfo")]
[ContentType("code")]
[Order(Before = "Default Quick Info Presenter")]
internal sealed class YourQuickInfoSourceProvider : IAsyncQuickInfoSourceProvider
{
    public IAsyncQuickInfoSource TryCreateQuickInfoSource(ITextBuffer textBuffer)
    {
        return textBuffer.Properties.GetOrCreateSingletonProperty(
            () => new YourQuickInfoSource(textBuffer));
    }
}
```

### 建议操作（灯泡）

```csharp
[Export(typeof(ISuggestedActionsSourceProvider))]
[Name("Your Suggested Actions")]
[ContentType("text")]
internal sealed class YourSuggestedActionsSourceProvider : ISuggestedActionsSourceProvider
{
    public ISuggestedActionsSource CreateSuggestedActionsSource(ITextView textView, ITextBuffer textBuffer)
    {
        return new YourSuggestedActionsSource(textView, textBuffer);
    }
}
```

## 线程指南

### 始终切换到 UI 线程进行 WPF 操作

```csharp
await ThreadHelper.JoinableTaskFactory.SwitchToMainThreadAsync(cancellationToken);
// 现在可以安全地创建/修改 WPF 元素
```

### 后台工作

```csharp
ThreadHelper.JoinableTaskFactory.RunAsync(async () =>
{
    await ThreadHelper.JoinableTaskFactory.SwitchToMainThreadAsync();
    await VS.Commands.ExecuteAsync("View.TaskList");
});
```

## VSSDK 与线程分析器规则

扩展应强制执行这些分析器规则。添加到 `.editorconfig`：

```ini
dotnet_diagnostic.VSSDK*.severity = error
dotnet_diagnostic.VSTHRD*.severity = error
```

### 性能规则
| ID | 规则 | 修复 |
|----|------|-----|
| **VSSDK001** | 从 `AsyncPackage` 派生 | 使用 `ToolkitPackage`（继承自 AsyncPackage） |
| **VSSDK002** | `AllowsBackgroundLoading = true` | 添加到 `[PackageRegistration]` |

### 线程规则 (VSTHRD)
| ID | 规则 | 修复 |
|----|------|-----|
| **VSTHRD001** | 避免 `.Wait()` | 使用 `await` |
| **VSTHRD002** | 避免 `JoinableTaskFactory.Run` | 使用 `RunAsync` 或 `await` |
| **VSTHRD100** | 不允许 `async void` | 使用 `async Task` |
| **VSTHRD110** | 观察异步结果 | `await task;` 或使用 pragma 抑制 |

## Visual Studio 主题

**所有 UI 必须尊重 VS 主题（浅色、深色、蓝色、高对比度）**

### 使用环境颜色进行 WPF 主题设置

```xml
<!-- MyControl.xaml -->
<UserControl x:Class="MyExt.MyControl"
             xmlns:vsui="clr-namespace:Microsoft.VisualStudio.PlatformUI;assembly=Microsoft.VisualStudio.Shell.15.0">
    <Grid Background="{DynamicResource {x:Static vsui:EnvironmentColors.ToolWindowBackgroundBrushKey}}">
        <TextBlock Foreground="{DynamicResource {x:Static vsui:EnvironmentColors.ToolWindowTextBrushKey}}"
                   Text="Hello, 主题化世界!" />
    </Grid>
</UserControl>
```

### 工具包自动主题（推荐）

工具包为 WPF UserControls 提供自动主题设置：

```xml
<UserControl x:Class="MyExt.MyUserControl"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:toolkit="clr-namespace:Community.VisualStudio.Toolkit;assembly=Community.VisualStudio.Toolkit"
             toolkit:Themes.UseVsTheme="True">
    <!-- 控件自动获取 VS 风格 -->
</UserControl>
```

对于对话框窗口，使用 `DialogWindow`：

```xml
<platform:DialogWindow
    x:Class="MyExt.MyDialog"
    xmlns:platform="clr-namespace:Microsoft.VisualStudio.PlatformUI;assembly=Microsoft.VisualStudio.Shell.15.0"
    xmlns:toolkit="clr-namespace:Community.VisualStudio.Toolkit;assembly=Community.VisualStudio.Toolkit"
    toolkit:Themes.UseVsTheme="True">
</platform:DialogWindow>
```

### 常用主题颜色标记

| 分类 | 标记 | 使用场景 |
|----------|-------|-------|
| **背景** | `EnvironmentColors.ToolWindowBackgroundBrushKey` | 窗口/面板背景 |
| **前景** | `EnvironmentColors.ToolWindowTextBrushKey` | 文本 |
| **命令栏** | `EnvironmentColors.CommandBarTextActiveBrushKey` | 菜单项 |
| **链接** | `EnvironmentColors.ControlLinkTextBrushKey` | 超链接 |

### 主题感知图标

使用 VS 图像目录中的 `KnownMonikers` 获取主题感知图标：

```csharp
public ImageMoniker IconMoniker => KnownMonikers.Settings;
```

在 VSCT 中：
```xml
<Icon guid="ImageCatalogGuid" id="Settings"/>
<CommandFlag>IconIsMoniker</CommandFlag>
```

## 常用 VS SDK API

### VS 辅助方法 (Community.VisualStudio.Toolkit)

```csharp
// 状态栏
await VS.StatusBar.ShowMessageAsync("消息");
await VS.StatusBar.ShowProgressAsync("正在工作...", currentStep, totalSteps);

// 解决方案/项目
Solution solution = await VS.Solutions.GetCurrentSolutionAsync();
IEnumerable<SolutionItem> items = await VS.Solutions.GetActiveItemsAsync();
bool isOpen = await VS.Solutions.IsOpenAsync();

// 文档
DocumentView docView = await VS.Documents.GetActiveDocumentViewAsync();
string text = docView?.TextBuffer?.CurrentSnapshot.GetText();
await VS.Documents.OpenAsync(fileName);
await VS.Documents.OpenInPreviewTabAsync(fileName);

// 命令
await VS.Commands.ExecuteAsync("View.TaskList");

// 设置
await VS.Settings.OpenAsync<OptionsProvider.GeneralOptions>();

// 消息框
await VS.MessageBox.ShowAsync("标题", "消息");
await VS.MessageBox.ShowErrorAsync("扩展名称", ex.ToString());

// 事件
VS.Events.SolutionEvents.OnAfterOpenProject += OnAfterOpenProject;
VS.Events.DocumentEvents.Saved += OnDocumentSaved;
```

### 与设置交互

```csharp
// 同步读取设置
var value = General.Instance.MyOption;

// 异步读取设置
var general = await General.GetLiveInstanceAsync();
var value = general.MyOption;

// 写入设置
General.Instance.MyOption = newValue;
General.Instance.Save();

// 或异步写入
general.MyOption = newValue;
await general.SaveAsync();

// 监听设置更改
General.Saved += OnSettingsSaved;
```

### 文本缓冲区操作

```csharp
// 获取快照
ITextSnapshot snapshot = textBuffer.CurrentSnapshot;

// 获取行
ITextSnapshotLine line = snapshot.GetLineFromLineNumber(lineNumber);
string lineText = line.GetText();

// 创建跟踪跨度
ITrackingSpan trackingSpan = snapshot.CreateTrackingSpan(span, SpanTrackingMode.EdgeInclusive);

// 编辑缓冲区
using (ITextEdit edit = textBuffer.CreateEdit())
{
    edit.Replace(span, newText);
    edit.Apply();
}

// 在光标位置插入文本
DocumentView docView = await VS.Documents.GetActiveDocumentViewAsync();
if (docView?.TextView != null)
{
    SnapshotPoint position = docView.TextView.Caret.Position.BufferPosition;
    docView.TextBuffer?.Insert(position, "要插入的文本");
}
```

## VSCT 命令表

### 菜单/命令结构

```xml
<Commands package="YourPackage">
  <Menus>
    <Menu guid="YourPackage" id="SubMenu" type="Menu">
      <Parent guid="YourPackage" id="MenuGroup"/>
      <Strings>
        <ButtonText>菜单名称</ButtonText>
        <CommandName>菜单名称</CommandName>
        <CanonicalName>.YourExtension.MenuName</CanonicalName>
      </Strings>
    </Menu>
  </Menus>

  <Groups>
    <Group guid="YourPackage" id="MenuGroup" priority="0x0600">
      <Parent guid="guidSHLMainMenu" id="IDM_VS_CTXT_CODEWIN"/>
    </Group>
  </Groups>

  <Buttons>
    <Button guid="YourPackage" id="CommandId" type="Button">
      <Parent guid="YourPackage" id="MenuGroup"/>
      <Icon guid="ImageCatalogGuid" id="Settings"/>
      <CommandFlag>IconIsMoniker</CommandFlag>
      <CommandFlag>DynamicVisibility</CommandFlag>
      <Strings>
        <ButtonText>命令名称</ButtonText>
        <CanonicalName>.YourExtension.CommandName</CanonicalName>
      </Strings>
    </Button>
  </Buttons>
</Commands>

<Symbols>
  <GuidSymbol name="YourPackage" value="{guid-here}">
    <IDSymbol name="MenuGroup" value="0x0001"/>
    <IDSymbol name="CommandId" value="0x0100"/>
  </GuidSymbol>
</Symbols>
```

## 最佳实践

### 1. 性能优化

- 在处理大型文档前检查文件/缓冲区大小
- 使用 `NormalizedSnapshotSpanCollection` 进行高效的跨度操作
- 在可能的情况下缓存解析结果
- 在库代码中使用 `ConfigureAwait(false)`

```csharp
// 跳过大型文件
if (buffer.CurrentSnapshot.Length > 150000)
    return null;
```

### 2. 异常处理

- 在外部操作周围使用 try-catch
- 适当记录错误
- 绝对不要让异常导致 VS 崩溃

```csharp
try
{
    // 操作
}
catch (Exception ex)
{
    await ex.LogAsync();
}
```

### 3. 可处置资源

- 在标记提供器和其他长生命周期对象上实现 `IDisposable`
- 在 Dispose 中取消订阅事件

```csharp
public void Dispose()
{
    if (!_isDisposed)
    {
        _buffer.Changed -= OnBufferChanged;
        _isDisposed = true;
    }
}
```

### 4. 内容类型

`[ContentType]` 特性常用的内内容类型：
- `"text"` - 所有文本文件
- `"code"` - 所有代码文件
- `"CSharp"` - C# 文件
- `"Basic"` - VB.NET 文件
- `"CSS"`, `"LESS"`, `"SCSS"` - 样式文件
- `"TypeScript"`, `"JavaScript"` - 脚本文件
- `"HTML"`, `"HTMLX"` - HTML 文件
- `"XML"` - XML 文件
- `"JSON"` - JSON 文件

### 5. 图像和图标

使用 VS 图像目录中的 `KnownMonikers`：

```csharp
public ImageMoniker IconMoniker => KnownMonikers.Settings;
```

在 VSCT 中：
```xml
<Icon guid="ImageCatalogGuid" id="Settings"/>
<CommandFlag>IconIsMoniker</CommandFlag>
```

## 测试

- 使用 `[VsTestMethod]` 进行需要 VS 上下文的测试
- 在可能的情况下模拟 VS 服务
- 将业务逻辑测试与 VS 集成分开

## 常见陷阱

| 陷阱 | 解决方案 |
|---------|----------|
| 阻塞 UI 线程 | 始终使用 `async`/`await` |
| 在后台线程创建 WPF | 首先调用 `SwitchToMainThreadAsync()` |
| 忽略取消令牌 | 在异步链中传递它们 |
| VSCommandTable.cs 不匹配 | 在 VSCT 更改后重新生成 |
| 硬编码 GUID | 使用 `PackageGuids` 和 `PackageIds` 常量 |
| 吞掉异常 | 使用 `await ex.LogAsync()` 记录 |
| 缺少 DynamicVisibility | `BeforeQueryStatus` 要求此功能 |
| 使用 `.Result`, `.Wait()` | 会导致死锁；始终使用 `await` |
| 硬编码颜色 | 使用 VS 主题颜色 (`EnvironmentColors`) |
| `async void` 方法 | 使用 `async Task` 代替 |

## 验证

构建并验证扩展：

```bash
msbuild /t:rebuild
```

确保在 `.editorconfig` 中启用了分析器：

```ini
dotnet_diagnostic.VSSDK*.severity = error
dotnet_diagnostic.VSTHRD*.severity = error
```

在发布前测试 Visual Studio 实验性实例。

## NuGet 包

| 包 | 用途 |
|---------|---------|
| `Community.VisualStudio.Toolkit.17` | 简化 VS 扩展开发 |
| `Microsoft.VisualStudio.SDK` | 核心 VS SDK |
| `Microsoft.VSSDK.BuildTools` | VSIX 构建工具 |
| `Microsoft.VisualStudio.Threading.Analyzers` | 线程分析器 |
| `Microsoft.VisualStudio.SDK.Analyzers` | VSSDK 分析器 |

## 资源

- [Community.VisualStudio.Toolkit](https://github.com/VsixCommunity/Community.VisualStudio.Toolkit)
- [VS 扩展性文档](https://learn.microsoft.com/en-us/visualstudio/extensibility/)
- [VSIX 社区示例](https://github.com/VsixCommunity/Samples)

## README 和市场展示

一个良好的 README 在 GitHub 和 VS 市场都能发挥作用。市场使用 README.md 作为扩展的描述页面。

### README 结构

```markdown
[marketplace]: https://marketplace.visualstudio.com/items?itemName=Publisher.ExtensionName
[repo]: https://github.com/user/repo

# 扩展名称

[![构建状态](https://github.com/user/repo/actions/workflows/build.yaml/badge.svg)](...)
[![Visual Studio 市场版本](https://img.shields.io/visual-studio-marketplace/v/Publisher.ExtensionName)][marketplace]
[![Visual Studio 市场下载量](https://img.shields.io/visual-studio-marketplace/d/Publisher.ExtensionName)][marketplace]

从 [Visual Studio 市场][marketplace] 下载此扩展，或获取 [CI 构建](http://vsixgallery.com/extension/ExtensionId/)。

--------------------------------------

**一句话推销扩展的钩子行。**

![截图](art/screenshot.png)

## 功能

### 功能 1
描述和截图...

## 使用方法
...

## 许可证
[Apache 2.0](LICENSE)
```

### README 最佳实践

| 元素 | 指南 |
|---------|-----------|
| **标题** | 使用 vsixmanifest 中的 `DisplayName` 作为相同名称 |
| **钩子行** | 在徽章之后立即使用加粗的一句话价值主张 |
| **截图** | 放置在 `/art` 文件夹中，使用相对路径 (`art/image.png`) |
| **图像大小** | 保持在 1MB 以下，宽度 800-1200 像素以确保清晰度 |
| **徽章** | 版本、下载量、评分、构建状态 |
| **功能部分** | 使用 H3 (`###`) 并为每个主要功能添加截图 |
| **键盘快捷键** | 格式化为 **Ctrl+M, Ctrl+C**（加粗） |
| **表格** | 适用于比较选项或列出功能 |
| **链接** | 在顶部使用参考样式链接以获得更整洁的 markdown |
| **VSIX 清单 (source.extension.vsixmanifest)**

```xml
<Metadata>
  <Identity Id="ExtensionName.guid-here" Version="1.0.0" Language="en-US" Publisher="您的名称" />
  <DisplayName>扩展名称</DisplayName>
  <Description xml:space="preserve">简短且有吸引力的描述，不超过 200 个字符。此描述会出现在搜索结果和扩展磁贴中。</Description>
  <MoreInfo>https://github.com/user/repo</MoreInfo>
  <License>Resources\LICENSE.txt</License>
  <Icon>Resources\Icon.png</Icon>
  <PreviewImage>Resources\Preview.png</PreviewImage>
  <Tags>关键字1, 关键字2, 关键字3</Tags>
</Metadata>
```

### 清单最佳实践

| 元素 | 指南 |
|---------|-----------|
| **DisplayName** | 3-5 个单词，不包含 "for Visual Studio"（隐含） |
| **Description** | 不超过 200 个字符，聚焦价值而非功能。出现在搜索磁贴中 |
| **Tags** | 5-10 个相关关键字，逗号分隔，有助于发现 |
| **Icon** | 128x128 或 256x256 PNG，简单设计在小尺寸下仍清晰可见 |
| **PreviewImage** | 200x200 PNG，可以与图标相同或展示功能截图 |
| **MoreInfo** | 链接到 GitHub 仓库以获取文档和问题 |

### 写作提示

1. **先讲价值，再讲功能** - "停止与 XML 注释争斗" 比 "XML 注释格式化器" 更具吸引力
2. **展示而非描述** - 截图比描述更有说服力
3. **术语一致** - README、清单和 UI 中的术语要匹配
4. **保持描述可扫描** - 短段落、项目符号、表格
5. **包含键盘快捷键** - 用户喜欢生产力提示
6. **添加 "为什么" 部分** - 在提出解决方案前解释问题
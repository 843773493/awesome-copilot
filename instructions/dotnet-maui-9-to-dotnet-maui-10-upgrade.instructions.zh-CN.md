

---
描述：从 .NET MAUI 9 升级到 .NET MAUI 10 的说明，包括破坏性变更、已弃用的 API 以及将 ListView 迁移到 CollectionView 的迁移策略。
适用于：**/*.csproj, **/*.cs, **/*.xaml
---

# 从 .NET MAUI 9 升级到 .NET MAUI 10

本指南帮助您通过关注需要代码更新的关键破坏性变更和已弃用 API，将 .NET MAUI 应用程序从 .NET 9 升级到 .NET 10。

---

## 目录

1. [快速入门](#quick-start)
2. [更新目标框架](#update-target-framework)
3. [破坏性变更 (P0 - 必须修复)](#breaking-changes-p0---must-fix)
   - [MessagingCenter 被设为内部](#messagingcenter-made-internal)
   - [ListView 和 TableView 已弃用](#listview-and-tableview-deprecated)
4. [已弃用的 API (P1 - 请尽快修复)](#deprecated-apis-p1---fix-soon)
   - [动画方法](#1-animation-methods)
   - [DisplayAlert 和 DisplayActionSheet](#2-displayalert-and-displayactionsheet)
   - [Page.IsBusy](#3-pageisbusy)
   - [MediaPicker API](#4-mediapicker-apis)
5. [推荐变更 (P2)](#recommended-changes-p2)
6. [批量迁移工具](#bulk-migration-tools)
7. [测试您的升级](#testing-your-upgrade)
8. [故障排除](#troubleshooting)

---

## 快速入门

**五步升级流程：**

1. **将 TargetFramework 更新为 `net10.0`**
2. **将 CommunityToolkit.Maui 更新为 12.3.0 或更高版本**（如果您使用它）- 必须执行
3. **修复破坏性变更** - MessagingCenter (P0)
4. **将 ListView/TableView 迁移到 CollectionView** (P0 - 关键)
5. **修复已弃用的 API** - 动画方法、DisplayAlert、IsBusy、MediaPicker (P1)

> ⚠️ **重大破坏性变更**：
> - CommunityToolkit.Maui **必须** 使用版本 12.3.0 或更高版本
> - ListView 和 TableView 现在已过时（迁移工作量最大）

---

## 更新目标框架

### 单平台

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>
</Project>
```

### 多平台

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFrameworks>net10.0-android;net10.0-ios;net10.0-maccatalyst;net10.0-windows10.0.19041.0</TargetFrameworks>
  </PropertyGroup>
</Project>
```

### 可选：Linux 兼容性（GitHub Copilot、WSL 等）

> 💡 **对于 Linux 开发**：如果您在 Linux 上构建（例如 GitHub Codespaces、WSL 或使用 GitHub Copilot），可以通过有条件排除 iOS/Mac Catalyst 目标使项目在 Linux 上编译：

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <!-- 从 Android 开始（始终支持） -->
    <TargetFrameworks>net10.0-android</TargetFrameworks>
    
    <!-- 仅在非 Linux 环境下添加 iOS/Mac Catalyst 目标 -->
    <TargetFrameworks Condition="!$([MSBuild]::IsOSPlatform('linux'))">$(TargetFrameworks);net10.0-ios;net10.0-maccatalyst</TargetFrameworks>
    
    <!-- 在 Windows 环境下添加 Windows 目标 -->
    <TargetFrameworks Condition="$([MSBuild]::IsOSPlatform('windows'))">$(TargetFrameworks);net10.0-windows10.0.19041.0</TargetFrameworks>
  </PropertyGroup>
</Project>
```

**优势：**
- ✅ 在 Linux 上成功编译（无需 iOS/Mac 工具）
- ✅ 与 GitHub Codespaces 和 Copilot 兼容
- ✅ 根据构建操作系统自动包含正确的目标
- ✅ 在切换操作系统环境时无需更改

**参考：** [dotnet/maui#32186](https://github.com/dotnet/maui/pull/32186)

### 更新必需的 NuGet 包

> ⚠️ **关键**：如果您使用 CommunityToolkit.Maui，您**必须**将其更新为 12.3.0 或更高版本。较早版本与 .NET 10 不兼容，会导致编译错误。

```bash
# 更新 CommunityToolkit.Maui（如果使用）
dotnet add package CommunityToolkit.Maui --version 12.3.0

# 更新其他常用包为 .NET 10 兼容版本
dotnet add package Microsoft.Maui.Controls --version 10.0.0
```

**检查所有 NuGet 包：**
```bash
# 列出所有包并检查更新
dotnet list package --outdated

# 更新所有包为最新兼容版本
dotnet list package --outdated | grep ">" | cut -d '>' -f 1 | xargs -I {} dotnet add package {}
```

---

## 破坏性变更 (P0 - 必须修复)

### MessagingCenter 被设为内部

**状态：** 🚨 **破坏性变更** - `MessagingCenter` 现在是 `internal`，无法访问。

**您将看到的错误：**
```
error CS0122: 'MessagingCenter' 由于其保护级别而不可访问
```

**迁移要求：**

#### 步骤 1：安装 CommunityToolkit.Mvvm

```bash
dotnet add package CommunityToolkit.Mvvm --version 8.3.0
```

#### 步骤 2：定义消息类

```csharp
// 旧：无需消息类
MessagingCenter.Send(this, "UserLoggedIn", userData);

// 新：创建消息类
public class UserLoggedInMessage
{
    public UserData Data { get; set; }
    
    public UserLoggedInMessage(UserData data)
    {
        Data = data;
    }
}
```

#### 步骤 3：更新 Send 调用

```csharp
// ❌ 旧（在 .NET 10 中已损坏）
using Microsoft.Maui.Controls;

MessagingCenter.Send(this, "UserLoggedIn", userData);
MessagingCenter.Send<App, string>(this, "StatusChanged", "Active");

// ✅ 新（必需）
using CommunityToolkit.Mvvm.Messaging;

WeakReferenceMessenger.Default.Send(new UserLoggedInMessage(userData));
WeakReferenceMessenger.Default.Send(new StatusChangedMessage("Active"));
```

#### 步骤 4：更新 Subscribe 调用

```csharp
// ❌ 旧（在 .NET 10 中已损坏）
MessagingCenter.Subscribe<App, UserData>(this, "UserLoggedIn", (sender, data) =>
{
    // 处理消息
    CurrentUser = data;
});

// ✅ 新（必需）
WeakReferenceMessenger.Default.Register<UserLoggedInMessage>(this, (recipient, message) =>
{
    // 处理消息
    CurrentUser = message.Data;
});
```

#### ⚠️ 重要行为差异：重复订阅

**WeakReferenceMessenger** 如果尝试在同一个接收者上注册相同的消息类型多次，会抛出 `InvalidOperationException`（MessagingCenter 允许这样做）：

```csharp
// ❌ 这会抛出 InvalidOperationException
WeakReferenceMessenger.Default.Register<UserLoggedInMessage>(this, (r, m) => Handler1(m));
WeakReferenceMessenger.Default.Register<UserLoggedInMessage>(this, (r, m) => Handler2(m)); // ❌ 报错！

// ✅ 解决方案 1：在重新注册前取消注册
WeakReferenceMessenger.Default.Unregister<UserLoggedInMessage>(this);
WeakReferenceMessenger.Default.Register<UserLoggedInMessage>(this, (r, m) => Handler1(m));

// ✅ 解决方案 2：在一个注册中处理多个操作
WeakReferenceMessenger.Default.Register<UserLoggedInMessage>(this, (r, m) => 
{
    Handler1(m);
    Handler2(m);
});
```

**为何重要**：如果您的代码在多个地方订阅了相同的消息（例如在页面构造函数和 `OnAppearing` 中），您将遇到运行时崩溃。

#### 步骤 5：完成时取消注册

```csharp
// ❌ 旧
MessagingCenter.Unsubscribe<App, UserData>(this, "UserLoggedIn");

// ✅ 新（关键 - 防止内存泄漏）
WeakReferenceMessenger.Default.Unregister<UserLoggedInMessage>(this);

// 或取消该接收者的全部消息注册
WeakReferenceMessenger.Default.UnregisterAll(this);
```

#### 完整的前后示例

**之前 (.NET 9)：**
```csharp
// 发送者
public class LoginViewModel
{
    public async Task LoginAsync()
    {
        var user = await AuthService.LoginAsync(username, password);
        MessagingCenter.Send(this, "UserLoggedIn", user);
    }
}

// 接收者
public partial class MainPage : ContentPage
{
    public MainPage()
    {
        InitializeComponent();
        
        MessagingCenter.Subscribe<LoginViewModel, User>(this, "UserLoggedIn", (sender, user) =>
        {
            WelcomeLabel.Text = $"Welcome, {user.Name}!";
        });
    }
    
    protected override void OnDisappearing()
    {
        base.OnDisappearing();
        MessagingCenter.Unsubscribe<LoginViewModel, User>(this, "UserLoggedIn");
    }
}
```

**之后 (.NET 10)：**
```csharp
// 1. 定义消息
public class UserLoggedInMessage
{
    public User User { get; }
    
    public UserLoggedInMessage(User user)
    {
        User = user;
    }
}

// 2. 发送者
public class LoginViewModel
{
    public async Task LoginAsync()
    {
        var user = await AuthService.LoginAsync(username, password);
        WeakReferenceMessenger.Default.Send(new UserLoggedInMessage(user));
    }
}

// 3. 接收者
public partial class MainPage : ContentPage
{
    public MainPage()
    {
        InitializeComponent();
        
        WeakReferenceMessenger.Default.Register<UserLoggedInMessage>(this, (recipient, message) =>
        {
            WelcomeLabel.Text = $"Welcome, {message.User.Name}!";
        });
    }
    
    protected override void OnDisappearing()
    {
        base.OnDisappearing();
        WeakReferenceMessenger.Default.UnregisterAll(this);
    }
}
```

**关键差异：**
- ✅ 类型安全的消息类
- ✅ 不使用魔法字符串
- ✅ 更好的 IntelliSense 支持
- ✅ 更容易重构
- ⚠️ **必须记得取消注册！**

---

### ListView 和 TableView 已弃用

**状态：** 🚨 **已弃用 (P0)** - `ListView`、`TableView` 和所有 Cell 类型现在已过时。迁移到 `CollectionView`。

**您将看到的警告：**
```
warning CS0618: 'ListView' 已过时: 'ListView 已弃用。请改用 CollectionView。'
warning CS0618: 'TableView' 已过时: '请改用 CollectionView。'
warning CS0618: 'TextCell' 已过时: '使用 TextCell 的控件（ListView 和 TableView）已过时。请改用 CollectionView。'
```

**已弃用类型：**
- `ListView` → `CollectionView`
- `TableView` → `CollectionView`（用于设置页面时，考虑使用垂直 StackLayout 与 BindableLayout）
- `TextCell` → 使用带有 Label 的自定义 DataTemplate
- `ImageCell` → 使用带有 Image 和 Label 的自定义 DataTemplate
- `EntryCell` → 使用带有 Entry 的自定义 DataTemplate
- `SwitchCell` → 使用带有 Switch 的自定义 DataTemplate
- `ViewCell` → DataTemplate

**影响：** 这是一个 **重大** 的破坏性变更。ListView 和 TableView 是 MAUI 应用中最常用的控件之一。

#### 为何需要时间

将 ListView/TableView 转换为 CollectionView 不是简单的查找替换：

1. **不同的事件模型** - `ItemSelected` → `SelectionChanged` 与不同的参数
2. **不同的分组** - GroupDisplayBinding 已不再存在
3. **上下文操作** - 必须转换为 SwipeView
4. **项目大小** - `HasUnevenRows` 的处理方式不同
5. **平台特定代码** - iOS/Android 的 ListView 平台配置需要移除
6. **需要测试** - CollectionView 的虚拟化方式不同，可能影响性能

#### 迁移策略

**步骤 1：列出所有 ListViews**

```bash
# 查找所有 ListView/TableView 的使用情况
grep -r "ListView\|TableView" --include="*.xaml" --include="*.cs" .
```

**步骤 2：基本的 ListView → CollectionView**

**之前 (ListView)：**
```xaml
<ListView ItemsSource="{Binding Items}"
          ItemSelected="OnItemSelected"
          HasUnevenRows="True">
    <ListView.ItemTemplate>
        <DataTemplate>
            <TextCell Text="{Binding Title}"
                     Detail="{Binding Description}" />
        </DataTemplate>
    </ListView.ItemTemplate>
</ListView>
```

**之后 (CollectionView)：**
```xaml
<CollectionView ItemsSource="{Binding Items}"
                SelectionMode="Single"
                SelectionChanged="OnSelectionChanged">
    <CollectionView.ItemTemplate>
        <DataTemplate>
            <VerticalStackLayout Padding="10">
                <Label Text="{Binding Title}" 
                       FontAttributes="Bold" />
                <Label Text="{Binding Description}"
                       FontSize="12"
                       TextColor="{StaticResource Gray600}" />
            </VerticalStackLayout>
        </DataTemplate>
    </CollectionView.ItemTemplate>
</CollectionView>
```

> ⚠️ **注意**：CollectionView 默认的 `SelectionMode` 是 `None`（选择禁用）。您必须显式设置 `SelectionMode="Single"` 或 `SelectionMode="Multiple"` 来启用选择。

**代码后台变更：**
```csharp
// ❌ 旧（ListView）
void OnItemSelected(object sender, SelectedItemChangedEventArgs e)
{
    if (e.SelectedItem == null)
        return;
        
    var item = (MyItem)e.SelectedItem;
    // 处理选择
    
    // 取消选择
    ((ListView)sender).SelectedItem = null;
}

// ✅ 新（CollectionView）
void OnSelectionChanged(object sender, SelectionChangedEventArgs e)
{
    if (e.CurrentSelection.Count == 0)
        return;
        
    var item = (MyItem)e.CurrentSelection.FirstOrDefault();
    // 处理选择
    
    // 取消选择（可选）
    ((CollectionView)sender).SelectedItem = null;
}
```

**步骤 3：分组的 ListView → 分组的 CollectionView**

**之前 (分组的 ListView)：**
```xaml
<ListView ItemsSource="{Binding GroupedItems}"
          IsGroupingEnabled="True"
          GroupDisplayBinding="{Binding Key}">
    <ListView.ItemTemplate>
        <DataTemplate>
            <TextCell Text="{Binding Name}" />
        </DataTemplate>
    </ListView.ItemTemplate>
</ListView>
```

**之后 (分组的 CollectionView)：**
```xaml
<CollectionView ItemsSource="{Binding GroupedItems}"
                IsGrouped="true">
    <CollectionView.GroupHeaderTemplate>
        <DataTemplate>
            <Label Text="{Binding Key}"
                   FontAttributes="Bold"
                   BackgroundColor="{StaticResource Gray100}"
                   Padding="10,5" />
        </DataTemplate>
    </CollectionView.GroupHeaderTemplate>
    
    <CollectionView.ItemTemplate>
        <DataTemplate>
            <VerticalStackLayout Padding="20,10">
                <Label Text="{Binding Name}" />
            </VerticalStackLayout>
        </DataTemplate>
    </CollectionView.ItemTemplate>
</CollectionView>
```

**步骤 4：上下文操作 → SwipeView**

> ⚠️ **平台注意**：SwipeView 需要触摸输入。在 Windows 桌面端，它仅在触摸屏上有效，不支持鼠标/触控板。考虑为桌面场景提供替代 UI（例如按钮、右键菜单）。

**之前 (ListView 带有 ContextActions)：**
```xaml
<ListView.ItemTemplate>
    <DataTemplate>
        <ViewCell>
            <ViewCell.ContextActions>
                <MenuItem Text="Delete" 
                          IsDestructive="True"
                          Command="{Binding Source={RelativeSource AncestorType={x:Type local:MyPage}}, Path=DeleteCommand}"
                          CommandParameter="{Binding .}" />
            </ViewCell.ContextActions>
            
            <Label Text="{Binding Title}" Padding="10" />
        </ViewCell>
    </DataTemplate>
</ListView.ItemTemplate>
```

**之后 (CollectionView 带有 SwipeView)：**
```xaml
<CollectionView.ItemTemplate>
    <DataTemplate>
        <SwipeView>
            <SwipeView.RightItems>
                <SwipeItems>
                    <SwipeItem Text="Delete"
                              BackgroundColor="Red"
                              Command="{Binding Source={RelativeSource AncestorType={x:Type local:MyPage}}, Path=DeleteCommand}"
                              CommandParameter="{Binding .}" />
                </SwipeItems>
            </SwipeView.RightItems>
            
            <VerticalStackLayout Padding="10">
                <Label Text="{Binding Title}" />
            </VerticalStackLayout>
        </SwipeView>
    </DataTemplate>
</CollectionView.ItemTemplate>
```

**步骤 5：TableView 用于设置页面 → 替代方案**

TableView 常用于设置页面。以下是现代替代方案：

**选项 1：使用分组的 CollectionView**
```xaml
<CollectionView ItemsSource="{Binding SettingGroups}"
                IsGrouped="true"
                SelectionMode="None">
    <CollectionView.GroupHeaderTemplate>
        <DataTemplate>
            <Label Text="{Binding Title}" 
                   FontAttributes="Bold"
                   Margin="10,15,10,5" />
        </DataTemplate>
    </CollectionView.GroupHeaderTemplate>
    
    <CollectionView.ItemTemplate>
        <DataTemplate>
            <Grid Padding="15,10" ColumnDefinitions="*,Auto">
                <Label Text="{Binding Title}" 
                       VerticalOptions="Center" />
                <Switch Grid.Column="1" 
                        IsToggled="{Binding IsEnabled}"
                        IsVisible="{Binding ShowSwitch}" />
            </Grid>
        </DataTemplate>
    </CollectionView.ItemTemplate>
</CollectionView>
```

**选项 2：垂直 StackLayout（用于小型设置列表）**
```xaml
<ScrollView>
    <VerticalStackLayout BindableLayout.ItemsSource="{Binding Settings}"
                        Spacing="10"
                        Padding="15">
        <BindableLayout.ItemTemplate>
            <DataTemplate>
                <Border StrokeThickness="0"
                       BackgroundColor="{StaticResource Gray100}"
                       Padding="15,10">
                    <Grid ColumnDefinitions="*,Auto">
                        <Label Text="{Binding Title}" 
                              VerticalOptions="Center" />
                        <Switch Grid.Column="1" 
                               IsToggled="{Binding IsEnabled}" />
                    </Grid>
                </Border>
            </DataTemplate>
        </BindableLayout.ItemTemplate>
    </VerticalStackLayout>
</ScrollView>
```

**步骤 6：移除平台特定的 ListView 代码**

如果您使用了平台特定的 ListView 功能，请移除它们：

```csharp
// ❌ 旧 - 移除这些 using 语句（现在在 .NET 10 中已过时）
using Microsoft.Maui.Controls.PlatformConfiguration;
using Microsoft.Maui.Controls.PlatformConfiguration.iOSSpecific;
using Microsoft.Maui.Controls.PlatformConfiguration.AndroidSpecific;

// ❌ 旧 - 移除 ListView 平台配置（现在在 .NET 10 中已过时）
myListView.On<iOS>().SetSeparatorStyle(SeparatorStyle.FullWidth);
myListView.On<Android>().IsFastScrollEnabled();

// ❌ 旧 - 移除 Cell 平台配置（现在在 .NET 10 中已过时）
viewCell.On<iOS>().SetDefaultBackgroundColor(Colors.White);
viewCell.On<Android>().SetIsContextActionsLegacyModeEnabled(false);
```

**迁移：** CollectionView 不具有与 ListView 相同的平台特定配置。如果您需要平台特定样式：

```csharp
// ✅ 新 - 使用条件编译
#if IOS
var backgroundColor = Colors.White;
#elif ANDROID
var backgroundColor = Colors.Transparent;
#endif

var grid = new Grid
{
    BackgroundColor = backgroundColor,
    // ... 其余的单元格内容
};
```

或在 XAML 中：
```xaml
<CollectionView.ItemTemplate>
    <DataTemplate>
        <Grid>
            <Grid.BackgroundColor>
                <OnPlatform x:TypeArguments="Color">
                    <On Platform="iOS" Value="White" />
                    <On Platform="Android" Value="Transparent" />
                </OnPlatform>
            </Grid.BackgroundColor>
            <!-- 单元格内容 -->
        </Grid>
    </DataTemplate>
</CollectionView.ItemTemplate>
```

#### 常见模式与陷阱

**1. 空视图**
```xaml
<!-- CollectionView 具有内置的 EmptyView 支持 -->
<CollectionView ItemsSource="{Binding Items}">
    <CollectionView.EmptyView>
        <ContentView>
            <VerticalStackLayout Padding="50" VerticalOptions="Center">
                <Label Text="未找到项目" 
                       HorizontalTextAlignment="Center" />
            </VerticalStackLayout>
        </ContentView>
    </CollectionView.EmptyView>
    <!-- ... -->
</CollectionView>
```

**2. 拉取刷新**
```xaml
<RefreshView IsRefreshing="{Binding IsRefreshing}"
             Command="{Binding RefreshCommand}">
    <CollectionView ItemsSource="{Binding Items}">
        <!-- ... -->
    </CollectionView>
</RefreshView>
```

**3. 项目间距**
```xaml
<!-- 使用 ItemsLayout 设置间距 -->
<CollectionView ItemsSource="{Binding Items}">
    <CollectionView.ItemsLayout>
        <LinearItemsLayout Orientation="Vertical" 
                          ItemSpacing="10" />
    </CollectionView.ItemsLayout>
    <!-- ... -->
</CollectionView>
```

**4. 头部和尾部**
```xaml
<CollectionView ItemsSource="{Binding Items}">
    <CollectionView.Header>
        <Label Text="我的列表" 
               FontSize="24" 
               Padding="10" />
    </CollectionView.Header>
    
    <CollectionView.Footer>
        <Label Text="列表结尾" 
               Padding="10" 
               HorizontalTextAlignment="Center" />
    </CollectionView.Footer>
    
    <!-- ItemTemplate -->
</CollectionView>
```

**5. 加载更多 / 无限滚动**
```xaml
<CollectionView ItemsSource="{Binding Items}"
                RemainingItemsThreshold="5"
                RemainingItemsThresholdReachedCommand="{Binding LoadMoreCommand}">
    <!-- ItemTemplate -->
</CollectionView>
```

**6. 项目大小优化**

CollectionView 使用 `ItemSizingStrategy` 来控制项目测量：

```xaml
<!-- 默认：每个项目单独测量（类似 HasUnevenRows="True") -->
<CollectionView ItemSizingStrategy="MeasureAllItems">
    <!-- ... -->
</CollectionView>

<!-- 性能：仅测量第一个项目，其余使用相同高度 -->
<CollectionView ItemSizingStrategy="MeasureFirstItem">
    <!-- 使用此方法时，所有项目高度相似 -->
</CollectionView>
```

> 💡 **性能提示**：如果您的列表项高度一致，请使用 `ItemSizingStrategy="MeasureFirstItem"` 来提高大型列表的性能。

#### .NET 10 处理器变更（iOS/Mac Catalyst）

> ℹ️ **.NET 10 默认使用新的优化 CollectionView 和 CarouselView 处理器**，提供更好的性能和稳定性。

**如果您之前在 .NET 9 中选择了新的处理器**，您应该现在 **移除** 这段代码：

```csharp
// ❌ 移除此代码（这些处理器现在是默认值）
#if IOS || MACCATALYST
builder.ConfigureMauiHandlers(handlers =>
{
    handlers.AddHandler<CollectionView, CollectionViewHandler2>();
    handlers.AddHandler<CarouselView, CarouselViewHandler2>();
});
#endif
```

在 .NET 10 中，优化的处理器会自动使用 - 不需要配置！

**只有在遇到问题时**，您可以回退到旧版处理器：

```csharp
// 在 MauiProgram.cs 中 - 仅在需要时
#if IOS || MACCATALYST
builder.ConfigureMauiHandlers(handlers =>
{
    handlers.AddHandler<Microsoft.Maui.Controls.CollectionView, 
                        Microsoft.Maui.Controls.Handlers.Items.CollectionViewHandler>();
});
#endif
```

然而，Microsoft 建议使用新的默认处理器以获得最佳效果。

#### 测试清单

迁移后，请测试以下场景：

- [ ] **项目选择** 正常工作
- [ ] **分组列表** 正确显示带有正确标题的头部
- [ ] **滑动手势操作**（如果使用）在 iOS 和 Android 上正常工作
- [ ] **空视图** 在列表为空时显示
- [ ] **下拉刷新** 正常工作（如果使用）
- [ ] **滚动性能** 可接受（尤其是大型列表）
- [ ] **项目大小** 正确（CollectionView 默认自动调整大小）
- [ ] **选择视觉状态** 正确显示/隐藏
- [ ] **数据绑定** 正确更新列表
- [ ] **从列表项导航** 正常工作

#### 迁移复杂性因素

从 ListView 迁移到 CollectionView 是复杂的，因为：
- 每个 ListView 可能具有独特的行为
- 需要更新平台特定代码
- 需要广泛的测试
- 需要将上下文操作转换为 SwipeView
- 分组列表需要更新模板
- 可能需要更改 ViewModel

#### 快速参考：ListView vs CollectionView

| 功能 | ListView | CollectionView |
|------|----------|----------------|
| **选择事件** | `ItemSelected` | `SelectionChanged` |
| **选择参数** | `SelectedItemChangedEventArgs` | `SelectionChangedEventArgs` |
| **获取选择项** | `e.SelectedItem` | `e.CurrentSelection.FirstOrDefault()` |
| **上下文菜单** | `ContextActions` | `SwipeView` |
| **分组** | `IsGroupingEnabled="True"` | `IsGrouped="true"` |
| **分组标题** | `GroupDisplayBinding` | `GroupHeaderTemplate` |
| **偶数行** | `HasUnevenRows="False"` | 自动调整大小（默认） |
| **空状态** | 手动 | `EmptyView` 属性 |
| **单元格** | TextCell、ImageCell 等 | 自定义 DataTemplate |

---

## 已弃用的 API (P1 - 请尽快修复)

这些 API 在 .NET 10 中仍然可以工作，但会显示编译器警告。它们将在未来版本中被移除。

### 1. 动画方法

**状态：** ⚠️ **已弃用** - 所有同步动画方法已被异步版本取代。

**您将看到的警告：**
```
warning CS0618: 'ViewExtensions.FadeTo(VisualElement, double, uint, Easing)' 已过时: '请改用 FadeToAsync。'
```

**迁移表：**

| 旧方法 | 新方法 | 示例 |
|--------|--------|------|
| `FadeTo()` | `FadeToAsync()` | `await view.FadeToAsync(0, 500);` |
| `ScaleTo()` | `ScaleToAsync()` | `await view.ScaleToAsync(1.5, 300);` |
| `TranslateTo()` | `TranslateToAsync()` | `await view.TranslateToAsync(100, 100, 250);` |
| `RotateTo()` | `RotateToAsync()` | `await view.RotateToAsync(360, 500);` |
| `RotateXTo()` | `RotateXToAsync()` | `await view.RotateXToAsync(45, 300);` |
| `RotateYTo()` | `RotateYToAsync()` | `await view.RotateYToAsync(45, 300);` |
| `ScaleXTo()` | `ScaleXToAsync()` | `await view.ScaleXToAsync(2.0, 300);` |
| `ScaleYTo()` | `ScaleYToAsync()` | `await view.ScaleYToAsync(2.0, 300);` |
| `RelRotateTo()` | `RelRotateToAsync()` | `await view.RelRotateToAsync(90, 300);` |
| `RelScaleTo()` | `RelScaleToAsync()` | `await view.RelScaleToAsync(0.5, 300);` |
| `LayoutTo()` | `LayoutToAsync()` | 请参阅下方特殊说明 |

#### 迁移示例

**简单动画：**
```csharp
// ❌ 旧（已弃用）
await myButton.FadeTo(0, 500);
await myButton.ScaleTo(1.5, 300);
await myButton.TranslateTo(100, 100, 250);

// ✅ 新（必需）
await myButton.FadeToAsync(0, 500);
await myButton.ScaleToAsync(1.5, 300);
await myButton.TranslateToAsync(100, 100, 250);
```

**顺序动画：**
```csharp
// ❌ 旧
await image.FadeTo(0, 300);
await image.ScaleTo(0.5, 300);
await image.FadeTo(1, 300);

// ✅ 新
await image.FadeToAsync(0, 300);
await image.ScaleToAsync(0.5, 300);
await image.FadeToAsync(1, 300);
```

**并行动画：**
```csharp
// ❌ 旧
await Task.WhenAll(
    image.FadeTo(0, 300),
    image.ScaleTo(0.5, 300),
    image.RotateTo(360, 300)
);

// ✅ 新
await Task.WhenAll(
    image.FadeToAsync(0, 300),
    image.ScaleToAsync(0.5, 300),
    image.RotateToAsync(360, 300)
);
```

**带取消：**
```csharp
// 新：异步方法支持取消
CancellationTokenSource cts = new();

try
{
    await view.FadeToAsync(0, 2000);
}
catch (TaskCanceledException)
{
    // 动画被取消
}

// 从其他地方取消
cts.Cancel();
```

#### 特殊情况：LayoutTo

`LayoutToAsync()` 被弃用，并带有特殊消息：“使用平移来动画化布局更改。”

```csharp
// ❌ 旧（已弃用）
await view.LayoutToAsync(new Rect(100, 100, 200, 200), 250);

// ✅ 新（使用 TranslateToAsync 替代）
await view.TranslateToAsync(100, 100, 250);

// 或直接动画化平移属性
var animation = new Animation(v => view.TranslationX = v, 0, 100);
animation.Commit(view, "MoveX", length: 250);
```

---

## 2. DisplayAlert 和 DisplayActionSheet

**状态：** ⚠️ **已弃用** - 同步方法被异步方法取代。

**您将看到的警告：**
```
warning CS0618: 'Page.DisplayAlert(string, string, string)' 已过时: '请改用 DisplayAlertAsync。'
```

#### 迁移示例

**DisplayAlert：**
```csharp
// ❌ 旧（已弃用）
await DisplayAlert("成功", "数据保存成功", "确定");
await DisplayAlert("错误", "保存失败", "取消");
bool result = await DisplayAlert("确认", "删除此项目？", "是", "否");

// ✅ 新（必需）
await DisplayAlertAsync("成功", "数据保存成功", "确定");
await DisplayAlertAsync("错误", "保存失败", "取消");
bool result = await DisplayAlertAsync("确认", "删除此项目？", "是", "否");
```

**DisplayActionSheet：**
```csharp
// ❌ 旧（已弃用）
string action = await DisplayActionSheet(
    "选择操作",
    "取消",
    "删除",
    "编辑", "分享", "复制"
);

// ✅ 新（必需）
string action = await DisplayActionSheetAsync(
    "选择操作",
    "取消",
    "删除",
    "编辑", "分享", "复制"
);
```

**在 ViewModel 中（使用 IDispatcher）：**
```csharp
public class MyViewModel
{
    private readonly IDispatcher _dispatcher;
    private readonly Page _page;
    
    public MyViewModel(IDispatcher dispatcher, Page page)
    {
        _dispatcher = dispatcher;
        _page = page;
    }
    
    public async Task ShowAlertAsync()
    {
        await _dispatcher.DispatchAsync(async () =>
        {
            await _page.DisplayAlertAsync("信息", "来自 ViewModel 的消息", "确定");
        });
    }
}
```

---

## 3. Page.IsBusy

**状态：** ⚠️ **已弃用** - 该属性将在 .NET 11 中移除。

**您将看到的警告：**
```
warning CS0618: 'Page.IsBusy' 已过时: 'Page.IsBusy 已弃用，将在 .NET 11 中移除'
```

**为何弃用：**
- 跨平台行为不一致
- 自定义选项有限
- 与现代 MVVM 模式兼容性差

#### 迁移示例

**简单页面：**
```xaml
<!-- ❌ 旧（已弃用） -->
<ContentPage IsBusy="{Binding IsLoading}">
    <StackLayout>
        <Label Text="内容在此处" />
    </StackLayout>
</ContentPage>

<!-- ✅ 新（推荐） -->
<ContentPage>
    <Grid>
        <!-- 主要内容 -->
        <StackLayout>
            <Label Text="内容在此处" />
        </StackLayout>
        
        <!-- 加载指示器覆盖层 -->
        <ActivityIndicator IsRunning="{Binding IsLoading}"
                          IsVisible="{Binding IsLoading}"
                          Color="{StaticResource Primary}"
                          VerticalOptions="Center"
                          HorizontalOptions="Center" />
    </Grid>
</ContentPage>
```

**带加载覆盖层：**
```xaml
<!-- ✅ 更好：自定义加载覆盖层 -->
<ContentPage>
    <Grid>
        <!-- 主要内容 -->
        <ScrollView>
            <VerticalStackLayout Padding="20">
                <Label Text="您的内容在此处" />
            </VerticalStackLayout>
        </ScrollView>
        
        <!-- 加载覆盖层 -->
        <Grid IsVisible="{Binding IsLoading}"
              BackgroundColor="#80000000">
            <VerticalStackLayout VerticalOptions="Center"
                               HorizontalOptions="Center"
                               Spacing="10">
                <ActivityIndicator IsRunning="True"
                                 Color="White" />
                <Label Text="加载中..."
                       TextColor="White" />
            </VerticalStackLayout>
        </Grid>
    </Grid>
</ContentPage>
```

**在代码后台：**
```csharp
// ❌ 旧（已弃用）
public partial class MyPage : ContentPage
{
    async Task LoadDataAsync()
    {
        IsBusy = true;
        try
        {
            await LoadDataFromServerAsync();
        }
        finally
        {
            IsBusy = false;
        }
    }
}

// ✅ 新（推荐）
public partial class MyPage : ContentPage
{
    async Task LoadDataAsync()
    {
        LoadingIndicator.IsVisible = true;
        LoadingIndicator.IsRunning = true;
        try
        {
            await LoadDataFromServerAsync();
        }
        finally
        {
            LoadingIndicator.IsVisible = false;
            LoadingIndicator.IsRunning = false;
        }
    }
}
```

**在 ViewModel 中：**
```csharp
public class MyViewModel : INotifyPropertyChanged
{
    private bool _isLoading;
    public bool IsLoading
    {
        get => _isLoading;
        set
        {
            _isLoading = value;
            OnPropertyChanged();
        }
    }
    
    public async Task LoadDataAsync()
    {
        IsLoading = true;
        try
        {
            await LoadDataFromServerAsync();
        }
        finally
        {
            IsLoading = false;
        }
    }
}
```

---

## 4. MediaPicker API

**状态：** ⚠️ **已弃用** - 单选方法被多选变体取代。

**您将看到的警告：**
```
warning CS0618: 'MediaPicker.PickPhotoAsync(MediaPickerOptions)' 已过时: '请切换到 PickPhotosAsync，该方法也支持多选。'
warning CS0618: 'MediaPicker.PickVideoAsync(MediaPickerOptions)' 已过时: '
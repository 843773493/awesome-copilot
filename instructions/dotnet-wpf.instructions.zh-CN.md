

---
描述: '.NET WPF 组件和应用程序模式'
适用范围: '**/*.xaml, **/*.cs'
---

## 摘要

这些说明指导 GitHub Copilot 在使用 MVVM 模式构建高质量、可维护且高性能的 WPF 应用程序时提供帮助。它包括 XAML、数据绑定、UI 响应性和 .NET 性能的最佳实践。

## 理想项目类型

- 使用 C# 和 WPF 的桌面应用程序
- 遵循 MVVM（模型-视图-视图模型）设计模式的应用程序
- 使用 .NET 8.0 或更高版本的项目
- 使用 XAML 构建的 UI 组件
- 强调性能和响应性的解决方案

## 目标

- 为 `INotifyPropertyChanged` 和 `RelayCommand` 生成样板代码
- 建议 ViewModel 和 View 逻辑的清晰分离
- 鼓励使用 `ObservableCollection<T>`、`ICommand` 和正确的绑定
- 推荐性能优化技巧（例如虚拟化、异步加载）
- 避免代码后台逻辑的紧密耦合
- 生成可测试的 ViewModel

## 示例提示行为

### ✅ 好的建议
- "为登录屏幕生成一个 ViewModel，包含用户名和密码属性以及一个 LoginCommand"
- "编写一个使用 UI 虚拟化的 ListView XAML 片段，并绑定到 ObservableCollection"
- "将此代码后台点击处理程序重构为 ViewModel 中的 RelayCommand"
- "在 WPF 中异步获取数据时添加加载旋转指示器"

### ❌ 避免
- 在代码后台中建议业务逻辑
- 使用没有上下文的静态事件处理程序
- 生成没有绑定的紧密耦合 XAML
- 建议使用 WinForms 或 UWP 的方法

## 更推荐的技术
- C# 与 .NET 8.0+
- XAML 与 MVVM 结构
- `CommunityToolkit.Mvvm` 或自定义 `RelayCommand` 实现
- 使用 Async/await 实现非阻塞 UI
- `ObservableCollection`、`ICommand`、`INotifyPropertyChanged`

## 常见模式
- 以 ViewModel 为中心的绑定
- 使用 .NET 或第三方容器进行依赖注入（例如 Autofac、SimpleInjector）
- XAML 命名约定（控件使用 PascalCase，绑定使用 camelCase）
- 避免绑定中的魔法字符串（使用 `nameof`）

## Copilot 可使用的示例指令片段

```csharp
public class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private string userName;

    [ObservableProperty]
    private string password;

    [RelayCommand]
    private void Login()
    {
        // 在此处添加登录逻辑
    }
}
```

```xml
<StackPanel>
    <TextBox Text="{Binding UserName, UpdateSourceTrigger=PropertyChanged}" />
    <PasswordBox x:Name="PasswordBox" />
    <Button 内容="登录" 命令="{Binding LoginCommand}" />
</StackPanel>
```
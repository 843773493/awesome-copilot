

---
描述: 'Playwright .NET 测试生成指南'
应用到: '**'
---

# Playwright .NET 测试生成指南

## 测试编写指南

### 代码质量标准

- **定位器**: 优先使用面向用户、基于角色的定位器（如 `GetByRole`, `GetByLabel`, `GetByText` 等），以提高测试的健壮性和可访问性。使用 `await Test.StepAsync()` 来分组交互并提高测试可读性和报告质量。
- **断言**: 使用自动重试的基于网络的断言。这些断言使用 Playwright 断言中的 `Expect()`（例如 `await Expect(locator).ToHaveTextAsync()`）。除非明确测试可见性变化，否则避免检查元素可见性。
- **超时**: 依赖 Playwright 内置的自动等待机制。避免使用硬编码等待或增加默认超时时间。
- **清晰度**: 使用描述性的测试和步骤标题，明确表达意图。仅在需要解释复杂逻辑或非直观交互时添加注释。

### 测试结构

- **引用**: 首先使用 `using Microsoft.Playwright;`，并根据测试框架选择 `using Microsoft.Playwright.Xunit;` 或 `using Microsoft.Playwright.NUnit;` 或 `using Microsoft.Playwright.MSTest;`（用于 MSTest）。
- **组织**: 创建继承自 `PageTest`（可在 NUnit、xUnit 和 MSTest 包中找到）的测试类，或在 xUnit 中使用 `IClassFixture<PlaywrightFixture>` 自定义测试套件。将同一功能相关的测试分组到同一个测试类中。
- **设置**: 使用 `[SetUp]`（NUnit）、`[TestInitialize]`（MSTest）或 xUnit 的构造函数初始化来执行所有测试共有的设置操作（例如导航到页面）。
- **标题**: 使用适当的测试属性（如 NUnit 的 `[Test]`、xUnit 的 `[Fact]`、MSTest 的 `[TestMethod]`），并遵循 C# 命名规范编写描述性的方法名称（例如 `SearchForMovieByTitle`）。

### 文件组织

- **位置**: 将所有测试文件存储在 `Tests/` 目录中，或按功能分类。
- **命名**: 使用 `<功能或页面>Tests.cs` 的命名约定（例如 `LoginTests.cs`，`SearchTests.cs`）。
- **范围**: 每个主要应用功能或页面应对应一个测试类。

### 断言最佳实践

- **UI 结构**: 使用 `ToMatchAriaSnapshotAsync` 来验证组件的可访问性树结构。这提供了全面且可访问的快照。
- **元素数量**: 使用 `ToHaveCountAsync` 来断言定位器找到的元素数量。
- **文本内容**: 使用 `ToHaveTextAsync` 进行精确文本匹配，使用 `ToContainTextAsync` 进行部分匹配。
- **导航**: 使用 `ToHaveURLAsync` 来验证操作后的页面 URL。

## 示例测试结构

```csharp
using Microsoft.Playwright;
using Microsoft.Playwright.Xunit;
using static Microsoft.Playwright.Assertions;

namespace PlaywrightTests;

public class 电影搜索测试 : PageTest
{
    public override async Task InitializeAsync()
    {
        await base.InitializeAsync();
        // 每个测试前导航到应用
        await Page.GotoAsync("https://debs-obrien.github.io/playwright-movies-app");
    }

    [Fact]
    public async Task 按标题搜索电影()
    {
        await Test.StepAsync("激活并执行搜索", async () =>
        {
            await Page.GetByRole(AriaRole.Search).ClickAsync();
            var searchInput = Page.GetByRole(AriaRole.Textbox, new() { Name = "Search Input" });
            await searchInput.FillAsync("Garfield");
            await searchInput.PressAsync("Enter");
        });

        await Test.StepAsync("验证搜索结果", async () =>
        {
            // 验证搜索结果的可访问性树
            await Expect(Page.GetByRole(AriaRole.Main)).ToMatchAriaSnapshotAsync(@"
                - main:
                  - heading ""Garfield"" [level=1]
                  - heading ""search results"" [level=2]
                  - list ""movies"":
                    - listitem ""movie"":
                      - link ""poster of The Garfield Movie The Garfield Movie rating"":
                        - /url: /playwright-movies-app/movie?id=tt5779228&page=1
                        - img ""poster of The Garfield Movie""
                        - heading ""The Garfield Movie"" [level=2]
            ");
        });
    }
}
```

## 测试执行策略

1. **初始运行**: 使用 `dotnet test` 或在 IDE 中运行测试工具执行测试
2. **调试失败**: 分析测试失败原因并识别根本问题
3. **迭代优化**: 根据需要优化定位器、断言或测试逻辑
4. **验证**: 确保测试稳定通过并覆盖预期功能
5. **报告**: 提供测试结果反馈及发现的任何问题

## 质量检查清单

在最终确定测试前，请确保：

- [ ] 所有定位器都可访问且具体，并避免严格模式违规
- [ ] 测试按逻辑分组并遵循清晰的结构
- [ ] 断言具有实际意义并反映用户期望
- [ ] 测试遵循一致的命名规范
- [ ] 代码格式正确且注释清晰
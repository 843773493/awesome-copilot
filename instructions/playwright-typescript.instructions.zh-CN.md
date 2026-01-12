

---
描述：'Playwright 测试生成指南'
适用范围：'**'
---

## 测试编写指南

### 代码质量标准
- **定位器**：优先使用面向用户、基于角色的定位器（如 `getByRole`, `getByLabel`, `getByText` 等），以提高测试的健壮性和可访问性。使用 `test.step()` 将交互操作分组，以提升测试的可读性和报告质量。
- **断言**：使用自动重试的基于网络的断言。这些断言以 `await` 关键字开头（例如 `await expect(locator).toHaveText()`）。除非特别测试可见性变化，否则避免使用 `expect(locator).toBeVisible()`。
- **超时**：依赖 Playwright 内置的自动等待机制。避免硬编码等待或增加默认超时时间。
- **清晰性**：使用描述性的测试和步骤标题，明确表达意图。仅在需要解释复杂逻辑或非直观交互时添加注释。

### 测试结构
- **导入**：以 `import { test, expect } from '@playwright/test';` 开始。
- **组织**：将同一功能相关的测试分组到 `test.describe()` 块中。
- **钩子函数**：使用 `beforeEach` 执行 `describe` 块中所有测试共有的设置操作（例如导航到页面）。
- **标题**：遵循清晰的命名规范，例如 `功能 - 具体操作或场景`。

### 文件组织
- **位置**：将所有测试文件存储在 `tests/` 目录中。
- **命名**：使用 `<功能或页面>.spec.ts` 命名约定（例如 `login.spec.ts`, `search.spec.ts`）。
- **范围**：每个主要应用功能或页面应有一个测试文件。

### 断言最佳实践
- **UI 结构**：使用 `toMatchAriaSnapshot` 验证组件的可访问性树结构。这提供了全面且可访问的快照。
- **元素数量**：使用 `toHaveCount` 断言定位器找到的元素数量。
- **文本内容**：使用 `toHaveText` 进行精确文本匹配，使用 `toContainText` 进行部分匹配。
- **导航**：使用 `toHaveURL` 验证操作后的页面 URL。

## 示例测试结构

```typescript
import { test, expect } from '@playwright/test';

test.describe('电影搜索功能', () => {
  test.beforeEach(async ({ page }) => {
    // 每次测试前导航到应用页面
    await page.goto('https://debs-obrien.github.io/playwright-movies-app');
  });

  test('通过标题搜索电影', async ({ page }) => {
    await test.step('激活并执行搜索', async () => {
      await page.getByRole('search').click();
      const searchInput = page.getByRole('textbox', { name: '搜索输入' });
      await searchInput.fill('Garfield');
      await searchInput.press('Enter');
    });

    await test.step('验证搜索结果', async () => {
      // 验证搜索结果的可访问性树结构
      await expect(page.getByRole('main')).toMatchAriaSnapshot(`
        - 主区域:
          - 标题 "Garfield" [级别=1]
          - 标题 "搜索结果" [级别=2]
          - 列表 "电影":
            - 列表项 "电影":
              - 链接 "The Garfield Movie 海报 The Garfield Movie 评分":
                - /url: /playwright-movies-app/movie?id=tt5779228&page=1
                - 图片 "The Garfield Movie 海报"
                - 标题 "The Garfield Movie" [级别=2]
      `);
    });
  });
});
```

## 测试执行策略

1. **初始运行**：使用 `npx playwright test --project=chromium` 执行测试
2. **调试失败**：分析测试失败并确定根本原因
3. **迭代优化**：根据需要优化定位器、断言或测试逻辑
4. **验证**：确保测试稳定通过并覆盖预期功能
5. **报告**：提供测试结果和发现的任何问题的反馈

## 质量检查清单

在最终确定测试前，请确保：
- [ ] 所有定位器都是可访问且具体的，避免严格模式违规
- [ ] 测试逻辑分组，结构清晰
- [ ] 断言有意义且反映用户期望
- [ ] 测试遵循一致的命名规范
- [ ] 代码格式正确且注释清晰
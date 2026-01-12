

---
description: '基于官方文档的 Playwright Python AI 测试生成指南。'
applyTo: '**'
---

# Playwright Python 测试生成指南

## 测试编写规范

### 代码质量标准
- **定位器**：优先使用面向用户的、基于角色的定位器（get_by_role, get_by_label, get_by_text）以提高稳定性和可访问性。
- **断言**：通过 expect API 使用自动重试的基于网页的断言（例如：expect(page).to_have_title(...)）。除非特别测试元素可见性变化，否则避免使用 expect(locator).to_be_visible()，因为更具体的断言通常更可靠。
- **超时**：依赖 Playwright 内置的自动等待机制。避免硬编码等待或增加默认超时时间。
- **清晰度**：使用描述性的测试标题（例如：def test_navigation_link_works():），明确表达测试意图。仅在解释复杂逻辑时添加注释，不要用于描述简单操作（如“点击按钮”）。

### 测试结构
- **导入**：每个测试文件应以 from playwright.sync_api import Page, expect 开始。
- **固定装置**：在测试函数中使用 page: Page 固定装置作为参数，以与浏览器页面交互。
- **设置**：将导航步骤（如 page.goto()）放在每个测试函数的开头。对于多个测试共享的设置操作，使用标准的 Pytest 固定装置。

### 文件组织
- **位置**：将测试文件存储在专门的 tests/ 目录中，或遵循现有项目结构。
- **命名**：测试文件必须遵循 test_<功能或页面>.py 命名规范，以便被 Pytest 发现。
- **作用域**：每个主要应用程序功能或页面应对应一个测试文件。

## 断言最佳实践
- **元素数量**：使用 expect(locator).to_have_count() 来断言定位器找到的元素数量。
- **文本内容**：使用 expect(locator).to_have_text() 进行精确文本匹配，使用 expect(locator).to_contain_text() 进行部分匹配。
- **导航**：使用 expect(page).to_have_url() 验证页面 URL。
- **断言风格**：优先使用 `expect` 而不是 `assert`，以获得更可靠的 UI 测试。

## 示例

```python
import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    # 在每个测试开始前访问起始 URL。
    page.goto("https://playwright.dev/")

def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")

def test_has_title(page: Page):
    # 期望标题包含一个子字符串。
    expect(page).to_have_title(re.compile("Playwright"))

def test_get_started_link(page: Page):
    page.get_by_role("link", name="Get started").click()
    
    # 验证页面是否包含名为 "Installation" 的标题。
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
```

## 测试执行策略

1. **执行**：通过终端使用 pytest 命令运行测试。
2. **调试失败**：分析测试失败原因并识别根本问题。
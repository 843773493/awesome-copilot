# 可访问性指南参考（WCAG）

## 快速合规检查表

### AA级要求（最低标准）

- [ ] 普通文本的颜色对比度 4.5:1
- [ ] 大文本（18px 及以上或 14px 加粗）的颜色对比度 3:1
- [ ] 触摸目标最小尺寸为 44×44 像素
- [ ] 所有功能均可通过键盘访问
- [ ] 始终可见焦点指示器
- [ ] 页面内容不得每秒闪烁超过 3 次
- [ ] 页面具有描述性的标题
- [ ] 链接的目的从文本中清晰可见
- [ ] 表单输入项需有标签
- [ ] 错误信息需具有描述性

---

## 颜色与对比度

### 对比度比率

| 元素 | 最小比率 | 增强（AAA） |
|------|----------|-------------|
| 正文文本 | 4.5:1 | 7:1 |
| 大文本（18px 及以上） | 3:1 | 4.5:1 |
| UI 组件 | 3:1 | - |
| 图形对象 | 3:1 | - |

### 颜色独立性

永远不要仅通过颜色传达信息：

```text
✗ 错误字段仅用红色显示
✓ 错误字段使用红色边框 + 错误图标 + 文本信息

✗ 必填字段仅用红色星号标记
✓ 必填字段标注为 "(required)" 或使用图标 + 提示信息

✗ 状态仅通过颜色点显示
✓ 状态使用颜色 + 图标 + 标签文本

```

### 可访问颜色组合

**安全文本颜色与背景组合：**

| 背景 | 文本颜色 | 对比度 |
|------|----------|--------|
| 白色（#FFFFFF） | 深灰色（#1F2937） | 15.5:1 ✓ |
| 浅灰色（#F3F4F6） | 深灰色（#374151） | 10.9:1 ✓ |
| 主色调蓝色（#2563EB） | 白色（#FFFFFF） | 4.6:1 ✓ |
| 深色（#111827） | 白色（#FFFFFF） | 18.1:1 ✓ |

**避免使用以下文本颜色组合：**

- 白色背景上的黄色文字（对比度不足）
- 白色背景上的浅灰色文字
- 白色背景上的橙色文字（最佳对比度有限）

---

## 键盘导航

### 要求

1. **所有交互元素** 必须可通过 Tab 键访问
2. **逻辑上的 Tab 顺序** 需遵循视觉布局
3. **无键盘陷阱**（用户始终可以 Tab 离开）
4. **键盘导航时始终可见焦点**
5. **跳转链接** 用于跳过重复导航

### 焦点指示器

```css
/* 示例聚焦样式 */
:focus {
  outline: 2px solid #2563EB;
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none; /* 隐藏鼠标用户聚焦 */
}

:focus-visible {
  outline: 2px solid #2563EB;
  outline-offset: 2px;
}

```

### 键盘快捷键

| 键 | 预期行为 |
|----|----------|
| Tab | 移动到下一个交互元素 |
| Shift+Tab | 移动到上一个元素 |
| Enter | 激活按钮/链接 |
| Space | 激活按钮，切换复选框 |
| Escape | 关闭模态框/下拉菜单 |
| 方向键 | 在组件内导航 |

---

## 屏幕阅读器支持

### 语义 HTML 元素

使用适合其用途的元素：

| 用途 | 元素 | 不要使用 |
|------|------|----------|
| 导航 | `<nav>` | `<div class="nav">` |
| 主要内容 | `<main>` | `<div id="main">` |
| 标题 | `<header>` | `<div class="header">` |
| 页脚 | `<footer>` | `<div class="footer">` |
| 按钮 | `<button>` | `<div onclick>` |
| 链接 | `<a href>` | `<span onclick>` |

### 标题层级

```text
h1 - 页面标题（每页一个）
  h2 - 主要部分
    h3 - 子部分
      h4 - 子子部分
    h3 - 另一个子部分
  h2 - 另一个主要部分

```

**不要跳过层级**（h1 → h3 而不使用 h2）

### 图像替代文本

```text
装饰性：alt=""（空，不要省略）
信息性：alt="图像所展示内容的描述"
功能性：alt="图像执行的操作"
复杂性：alt="简要描述" + 附近详细描述

```

**替代文本示例：**

```text
✓ alt="柱状图显示第四季度销售额从 1000 万美元增长至 1500 万美元"
✓ alt="公司标志"
✓ alt=""（用于装饰性背景图案）

✗ alt="image" 或 alt="photo"
✗ alt="img_12345.jpg"
✗ 完全缺少 alt 属性

```

---

## 触摸与指针

### 触摸目标尺寸

| 平台 | 最小 | 推荐 |
|------|------|-----|
| WCAG 2.1 | 44×44 像素 | 48×48 像素 |
| iOS（苹果） | 44×44 点 | - |
| Android | 48×48 dp | - |

### 触摸目标间距

- 相邻目标之间最小间距为 8 像素
- 建议使用 16 像素以上以提高舒适度
- 主要操作的目标应更大

### 指针手势

- 复杂手势需有单指替代方案
- 拖拽操作需有等效的点击操作
- 避免在触摸设备上使用仅悬停功能

---

## 表单可访问性

### 标签

每个输入项必须有对应的标签：

```text
<label for="email">电子邮件地址</label>
<input type="email" id="email" name="email">

```

### 必填字段

```text
<!-- 通知屏幕阅读器 -->
<label for="name">
  姓名 <span aria-label="必填">*</span>
</label>
<input type="text" id="name" required aria-required="true">

```

### 错误处理

```text
<label for="email">电子邮件</label>
<input type="email" id="email" aria-invalid="true" aria-describedby="email-error">
<span id="email-error" role="alert">
  请输入有效的电子邮件地址
</span>

```

### 表单说明

- 在输入前提供格式提示
- 在错误前显示密码要求
- 使用 fieldset/legend 将相关字段分组

---

## 动态内容

### 实时区域

对于动态更新的内容：

```text
aria-live="polite" - 适时宣布
aria-live="assertive" - 立即宣布（可能中断）
role="alert" - 紧急信息（如 assertive）
role="status" - 状态更新（如 polite）

```

### 加载状态

```text
<button aria-busy="true" aria-live="polite">
  <span class="spinner"></span>
  加载中...
</button>

```

### 模态对话框

- 打开时焦点移入模态框
- 焦点被限制在模态框内
- 按 Esc 键关闭模态框
- 关闭时焦点返回触发元素

---

## 可访问性测试

### 手动测试检查表

1. **仅使用键盘：** 通过 Tab/Enter 键导航整个页面
2. **屏幕阅读器：** 使用 VoiceOver（Mac）或 NVDA（Windows）进行测试
3. **200% 放大：** 内容保持可读和可用
4. **高对比度：** 使用系统高对比度模式进行测试
5. **无鼠标：** 无需指针设备即可完成所有任务

### 自动化工具

- axe DevTools（浏览器扩展）
- WAVE（WebAIM 浏览器扩展）
- Lighthouse（Chrome DevTools）
- 颜色对比度检查器（WebAIM、Contrast Ratio）

### 常见问题检查

- [ ] 缺失或空的替代文本
- [ ] 空链接或按钮
- [ ] 缺失表单标签
- [ ] 颜色对比度不足
- [ ] 缺失语言属性
- [ ] 标题层级结构错误
- [ ] 缺失跳转导航链接
- [ ] 自定义控件不可访问

---

## ARIA 快速参考

### 角色

| 角色 | 用途 |
|------|------|
| `button` | 可点击按钮 |
| `link` | 导航链接 |
| `dialog` | 模态对话框 |
| `alert` | 重要信息 |
| `navigation` | 导航区域 |
| `main` | 主要内容 |
| `search` | 搜索功能 |
| `tab/tablist/tabpanel` | Tab 接口 |

### 属性

| 属性 | 用途 |
|------|------|
| `aria-label` | 可访问名称 |
| `aria-labelledby` | 引用标签元素 |
| `aria-describedby` | 引用描述 |
| `aria-hidden` | 隐藏辅助技术 |
| `aria-expanded` | 可展开状态 |
| `aria-selected` | 选择状态 |
| `aria-disabled` | 禁用状态 |
| `aria-required` | 必填字段 |
| `aria-invalid` | 无效输入 |

### 黄金规则

**ARIA 的第一条规则：** 如果原生 HTML 可以实现，不要使用 ARIA。

```text
✗ <div role="button" tabindex="0">点击</div>
✓ <button>点击</button>

```

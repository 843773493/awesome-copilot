# 网页可访问性参考指南

从MDN Web文档中整理的综合参考指南，涵盖核心可访问性概念、作者指南、安全浏览实践、基于ARIA的小部件以及移动可访问性要求。

---

## 1. 可访问性概述

> **来源:** https://developer.mozilla.org/en-US/docs/Web/Accessibility

### 什么是可访问性？

**可访问性**（简称**A11y** -- "a" + 11个字符 + "y"）在网页开发中意味着尽可能让所有人使用网站，即使他们的能力在某些方面受到限制。

> "网络本质上是为所有人设计的，无论其硬件、软件、语言、地理位置或能力如何。当网络达到这一目标时，它对听力、运动、视力和认知能力各异的人群都是可访问的。" -- W3C

关键点：

- 技术使许多人**更容易**使用。
- 技术使**残障人士**能够实现某些事情。
- 可访问性涵盖身体、认知、听力、运动和视力能力。

### 核心原则

1. **语义化HTML** -- 使用正确的元素来实现其预期目的。
2. **键盘导航** -- 确保在没有鼠标的情况下也能完全使用。
3. **辅助技术支持** -- 与屏幕阅读器和其他工具保持兼容。
4. **可感知性** -- 内容必须能够通过多种感官感知。
5. **可操作性** -- 所有功能必须可以通过键盘访问。
6. **可理解性** -- 使用清晰的语言和可预测的行为。
7. **鲁棒性** -- 能在各种辅助技术中正常运行。

### 初学者教程模块（MDN Learn Web Development）

| 模块 | 描述 |
|------|------|
| 什么是可访问性？ | 需要考虑的群体、用户依赖的工具、工作流程整合 |
| 可访问性工具与辅助技术 | 解决可访问性问题的工具 |
| HTML：可访问性的良好基础 | 语义化标记和正确元素使用 |
| CSS和JavaScript最佳实践 | 可访问性实现的CSS和JS |
| ARIA基础 | 为复杂UI控件和动态内容添加语义 |
| 可访问性多媒体 | 视频、音频和图像的文本替代 |
| 移动可访问性 | iOS/Android工具和移动特定考虑因素 |

### 关键标准和框架

- **WCAG（网页内容可访问性指南）** -- 分为可感知性、可操作性、可理解性和鲁棒性四个类别。
- **ARIA（可访问的丰富网络应用）** -- 为自定义小部件添加语义意义，包含53+属性和87+角色。

---

## 2. 网页作者信息

> **来源:** https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Information_for_Web_authors

### 指南与法规

#### ARIA作者实践指南（APG）

- **提供者:** W3C
- **网址:** https://www.w3.org/WAI/ARIA/apg/
- 为可访问的网页体验提供设计模式和功能示例。
- 覆盖如何将可访问性语义应用于常见设计模式和小部件。

#### 网页内容可访问性指南（WCAG）

- **提供者:** W3C网络可访问性倡议（WAI）
- **网址:** https://www.w3.org/WAI/standards-guidelines/wcag/
- 被欧盟可访问性法规采用的重要基础指南。

#### ARIA在MDN上的内容

- 提供完整的ARIA角色、属性和属性指南。
- 每个角色的最佳实践和代码示例。

### 操作指南

| 指南 | 提供者 | 网址 |
|------|--------|------|
| 团队可访问性 | 美国通用服务管理局 | https://digital.gov/guides/accessibility-for-teams/ |
| 可访问性网页页面编写 | IBM | https://www.ibm.com/able/requirements/requirements/ |

### 自动检查和修复工具

#### 浏览器扩展

| 工具 | 网址 |
|------|-----|
| HTML代码嗅探器 | https://squizlabs.github.io/HTML_CodeSniffer/ |
| aXe DevTools | 内置于浏览器开发者工具 |
| Lighthouse可访问性审核 | Chrome开发者工具集成 |
| 可访问性洞察 | https://accessibilityinsights.io/ |
| WAVE | https://wave.webaim.org/extension/ |

#### 构建过程/程序化测试

| 工具 | 描述 |
|------|------|
| axe-core | 自动化测试的可访问性引擎（dequelabs/axe-core） |
| eslint-plugin-jsx-a11y | JSX可访问性规则的ESLint插件 |
| Lighthouse审核 | 可编程审核运行器（GoogleChrome/lighthouse） |
| AccessLint.js | 自动化a11y检查库 |

#### 持续集成

- **AccessLint** (https://accesslint.com/) -- 与GitHub拉取请求集成，用于自动化可访问性审查。

### 测试建议

模拟和测试方法：

- 色盲模拟
- 低视力模拟
- 低对比度测试
- 放大测试
- 仅键盘导航（禁用鼠标）
- 仅触控测试
- 语音命令测试
- 使用**网页残疾模拟器**浏览器扩展进行测试

最佳实践：**在可能的情况下，使用真实用户进行测试。**

---

## 3. 安全浏览

> **来源:** https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Browsing_safely

### 针对的条件

| 条件 | 常见触发因素 |
|------|-------------|
| 前庭障碍 | 运动、动画、视差效果 |
| 癫痫 | 闪烁（每秒3次以上）、闪烁、高对比度颜色变化 |
| 光敏感 | 颜色强度、闪烁、高对比度 |
| 脑外伤（TBI） | 从颜色处理中产生的高认知负担 |

### CSS媒体功能：`prefers-reduced-motion`

检测用户操作系统级别的减少运动偏好。

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

开发者可以监听的CSS过渡事件：

- `transitionrun`
- `transitionstart`
- `transitionend`
- `transitioncancel`

### 平台级浏览器控件

| 平台 | 设置 | 备注 |
|------|------|------|
| 桌面版Safari（10.1+） | 禁用自动播放 | 不影响动画GIF |
| iOS Safari（10.3+） | 减少运动（操作系统可访问性设置） | GIF不受影响 |
| Firefox | `image.animation_mode` 设置为 `"none"` | 禁用所有动画GIF |
| 阅读模式（多种） | 内容阻止器、文本转语音、字体/缩放 | 减少干扰 |

### 操作系统可访问性功能

**Windows 10:**

- 设置 > 易用性 > 显示 -- 关闭动画。
- 设置 > 易用性 > 显示 > 颜色过滤器 -- 切换灰度模式。
- 灰度模式可减少TBI、光敏感癫痫等条件下的认知负担。

**macOS:**

- 系统偏好设置 > 可访问性 > 显示 -- 选择“减少运动”选项。

### WCAG合规性：成功标准2.3.1

**三次闪烁或以下阈值** -- 内容不得每秒闪烁超过三次，除非闪烁低于一般闪烁和红色闪烁阈值。

### 开发者最佳实践

**应做：**

- 支持 `prefers-reduced-motion` 媒体查询。
- 保持闪烁频率低于每秒3次。
- 为所有动画提供播放/暂停控制。
- 在启用操作系统可访问性功能的情况下进行测试。

**不应做：**

- 在没有用户控制的情况下自动播放视频或动画。
- 使用高频闪烁或闪烁效果。
- 假设所有用户都能容忍运动。

### 实施检查清单

- [ ] 在CSS中添加 `@media (prefers-reduced-motion: reduce)` 规则。
- [ ] 当用户偏好设置时禁用自动播放动画。
- [ ] 确保GIF有暂停控制。
- [ ] 在Windows和macOS可访问性模式下测试。
- [ ] 验证是否符合WCAG 2.3.1（三次闪烁标准）。

---

## 4. 可访问的网页应用和小部件

> **来源:** https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Accessible_web_applications_and_widgets

### 问题

使用通用HTML元素（如 `<div>` 和 `<span>`）构建的自定义JavaScript小部件（滑块、菜单栏、标签、对话框）缺乏语义意义，辅助技术无法识别动态内容的变化。

### ARIA（可访问的丰富网络应用）

ARIA填补了标准HTML和桌面风格UI控件之间的空白，包含三种类型的属性：

1. **角色（Roles）** -- 描述HTML原生不支持的小部件（滑块、菜单栏、标签、对话框）。
2. **属性（Properties）** -- 描述特征（可拖动、必填、有弹出窗口）。
3. **状态（States）** -- 描述当前交互状态（忙碌、禁用、选中、隐藏）。

**重要提示：** 当有语义化HTML元素可用时，优先使用它们。ARIA是动态组件的渐进增强。

### 示例：标签小部件

**无ARIA（不可访问）：**

```html
<ol>
  <li id="ch1Tab">
    <a href="#ch1Panel">第一章</a>
  </li>
  <li id="ch2Tab">
    <a href="#ch2Panel">第二章</a>
  </li>
</ol>

<div>
  <div id="ch1Panel">第一章内容在此</div>
  <div id="ch2Panel">第二章内容在此</div>
</div>
```

**有ARIA（可访问）：**

```html
<ol role="tablist">
  <li id="ch1Tab" role="tab">
    <a href="#ch1Panel">第一章</a>
  </li>
  <li id="ch2Tab" role="tab">
    <a href="#ch2Panel">第二章</a>
  </li>
</ol>

<div>
  <div id="ch1Panel" role="tabpanel" aria-labelledby="ch1Tab">
    第一章内容在此
  </div>
  <div id="ch2Panel" role="tabpanel" aria-labelledby="ch2Tab">
    第二章内容在此
  </div>
</div>
```

### 用于交互小部件的常见ARIA状态属性

| 属性 | 用途 |
|------|------|
| `aria-checked` | 复选框或单选按钮的状态 |
| `aria-disabled` | 可见但不可编辑或操作 |
| `aria-grabbed` | 拖放中的“抓取”状态 |
| `aria-selected` | 元素的选中状态 |
| `aria-expanded` | 可展开内容是否展开 |
| `aria-pressed` | 切换按钮的按下状态 |

使用ARIA状态来指示UI状态，并使用CSS属性选择器进行样式设置。

### 使用 `aria-hidden` 管理可见性

```html
<div id="tp1" class="tooltip" role="tooltip" aria-hidden="true">
  您的姓名是可选的
</div>
```

```css
div.tooltip[aria-hidden="true"] {
  display: none;
}
```

```javascript
function showTip(el) {
  el.setAttribute("aria-hidden", "false");
}
```

### 角色更改

不要动态更改元素的ARIA角色。相反，应完全替换元素：

```javascript
// 正确做法：替换元素
// 查看模式
<div role="button">编辑此文本</div>

// 编辑模式：替换为输入框
<input type="text" />
```

### 键盘导航最佳实践

| 键 | 预期行为 |
|----|---------|
| Tab / Shift+Tab | 在小部件内移动焦点 |
| 方向键 | 在小部件内导航项目 |
| Enter / 空格键 | 激活焦点控件 |
| Esc | 关闭菜单或对话框 |
| Home / End | 跳转到第一个或最后一个项目 |

焦点管理注意事项：

- 保持焦点顺序与视觉布局一致。
- 使用 `tabindex="0"` 使自定义元素可通过键盘访问。
- 避免使用 `tabindex > 0`（破坏自然的焦点顺序）。
- 更新键盘用户的视觉焦点指示器。
- 在打开对话框或模态框时通过程序移动焦点。

### 用于交互小部件的关键ARIA属性

**标签和描述：**

| 属性 | 使用方式 |
|------|---------|
| `aria-label` | 直接文本标签 |
| `aria-labelledby` | 引用标记此元素的元素 |
| `aria-describedby` | 引用附加描述文本 |
| `aria-description` | 内联描述文本 |

**关系：**

| 属性 | 使用方式 |
|------|---------|
| `aria-controls` | 此元素控制另一个元素 |
| `aria-owns` | 建立父子关系 |
| `aria-flowto` | 定义逻辑阅读顺序 |

**小部件行为：**

| 属性 | 使用方式 |
|------|---------|
| `aria-haspopup` | 有弹出窗口（菜单、列表框、对话框、网格、树） |
| `aria-expanded` | 可展开内容的状态（true/false） |
| `aria-modal` | 模态对话框（true） |
| `aria-live` | 实时区域公告（polite、assertive、off） |
| `aria-busy` | 加载或处理状态（true/false） |

### 动态内容的实时区域

```html
<div aria-live="polite" aria-atomic="true">
  屏幕阅读器将宣布更新
</div>
```

- `aria-live="polite"` -- 适时宣布。
- `aria-live="assertive"` -- 立即宣布。
- `aria-atomic="true"` -- 宣布整个区域，而不仅仅是更改的部分。

---

## 5. 移动可访问性检查清单

> **来源:** https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Mobile_accessibility_checklist

为移动应用开发者提供的可访问性要求检查清单，目标是符合WCAG 2.2 AA标准。

### 颜色

- **普通文本：** 最小4.5:1对比度比率（小于18pt或14pt粗体）。
- **大文本：** 最小3:1对比度比率（至少18pt或14pt粗体）。
- 通过颜色传达的信息必须通过其他方式获得（例如，使用下划线表示链接）。

### 可见性

- 不要仅通过零透明度、z-index排序或屏幕外放置来隐藏内容。
- 使用HTML的 `hidden` 属性、CSS的 `visibility` 或 `display` 属性真正隐藏内容。
- 除非绝对必要，否则避免使用 `aria-hidden`。
- 对于单页应用中可能重叠的多个视图/卡片尤为重要。

### 焦点

- 标准控件（链接、按钮、表单字段）默认可聚焦。
- 自定义控件必须具有适当ARIA角色（例如，`button`、`link`、`checkbox`）。
- 焦点顺序必须逻辑且一致。

### 文本等效

- 使用 `alt`、`title`、`aria-label`、`aria-labelledby` 或 `aria-describedby` 为所有非文本元素提供文本替代。
- 避免使用文本图像。
- 可见UI组件的文本必须与程序化名称匹配（WCAG 2.1：标签在名称中）。
- 所有表单控件必须有相关 `<label>` 元素。

### 状态管理

- 标准控件：操作系统处理单选按钮和复选框。
- 自定义控件必须通过ARIA状态传递状态变化：
  - `aria-checked`
  - `aria-disabled`
  - `aria-selected`
  - `aria-expanded`
  - `aria-pressed`

### 方向

- 内容不得限制为竖屏或横屏，除非必要（例如，钢琴应用或银行支票扫描器）。
- 参考：WCAG 2.1方向（https://www.w3.org/WAI/WCAG21/Understanding/orientation.html）。

### 一般指南

**应用结构：**

- 始终提供应用标题。
- 使用适当的标题层级，不要跳过层级：

```html
<h1>顶级标题</h1>
  <h2>次级标题</h2>
  <h2>另一个次级标题</h2>
    <h3>低级标题</h3>
```

**ARIA地标角色：**

使用地标来描述应用或文档结构：

- `banner`
- `complementary`
- `contentinfo`
- `main`
- `navigation`
- `search`

**触控事件（WCAG 2.1：指针取消）：**

1. 避免在按下事件中执行函数。
2. 如果无法避免，应在抬起事件中完成函数并提供中止机制。
3. 如果无法避免，确保抬起事件可以撤销按下事件的操作。
4. 例外情况：游戏控制、虚拟键盘、实时反馈。

**触控目标大小：**

- 目标必须足够大以确保可靠的用户交互。
- 参考：BBC移动可访问性指南中的具体尺寸建议（https://www.bbc.co.uk/accessibility/forproducts/guides/mobile/target-touch-size）。

---

## 额外资源

| 资源 | 网址 |
|------|-----|
| W3C可访问性标准 | https://www.w3.org/standards/webdesign/accessibility |
| WAI兴趣小组 | https://www.w3.org/WAI/about/groups/waiig/ |
| ARIA规范 | https://w3c.github.io/aria/ |
| WAI-ARIA作者实践指南 | https://www.w3.org/WAI/ARIA/apg/ |
| WCAG 2.1理解文档 | https://www.w3.org/WAI/WCAG21/Understanding/ |
| IBM可访问性要求 | https://www.ibm.com/able/requirements/requirements/ |
| 可访问性洞察 | https://accessibilityinsights.io/ |
| WAVE评估工具 | https://wave.webaim.org/extension/ |

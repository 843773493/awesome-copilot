# ARIA 表单角色参考

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/form_role>

## 定义和描述

`form` 角色标识页面上一组提供等效功能的元素，其功能等同于 HTML 表单。它是一种 **地标角色**，有助于用户导航到表单区域。

`form` 地标角色用于标识一个包含多个项目和对象的页面区域，这些项目和对象整体上构成一个表单，当没有其他合适的地标角色（例如 `main` 或 `search`）时使用。

**重要:** 除非表单具有可访问名称，否则它不会被暴露为地标区域。

## 推荐方法：使用 HTML `<form>` 元素

除非有非常充分的理由，否则应使用 HTML `<form>` 元素来包含表单控件，而不是 ARIA 的 `form` 角色。HTML `<form>` 元素足以告知辅助技术存在一个表单。

```html
<!-- 推荐的语义化方法 -->
<form id="send-comment" aria-label="添加评论">
  <!-- 表单控件 -->
</form>
```

如果 `<form>` 元素提供了可访问名称，它将自动作为 `form` 地标角色进行通信。

## 何时使用 `role="form"`

`form` 角色应用于标识页面上的 **一个区域**，而不是单个表单字段。当您不使用原生 `<form>` 元素但仍希望向辅助技术传达表单语义时，使用 `role="form"` 是合适的。

### 基本示例

```html
<div role="form" id="contact-info" aria-label="联系信息">
  <!-- 表单内容 -->
</div>
```

### 包含表单控件的完整示例

```html
<div role="form" id="send-comment" aria-label="添加评论">
  <label for="username">用户名</label>
  <input
    id="username"
    name="username"
    autocomplete="nickname"
    autocorrect="off"
    type="text" />

  <label for="email">电子邮件</label>
  <input
    id="email"
    name="email"
    autocomplete="email"
    autocapitalize="off"
    autocorrect="off"
    spellcheck="false"
    type="text" />

  <label for="comment">评论</label>
  <textarea id="comment" name="comment"></textarea>

  <input value="评论" type="submit" />
</div>
```

## 可访问命名（地标暴露的必需条件）

每个需要作为地标暴露的 `<form>` 元素和 `form` 角色必须使用以下方式之一提供一个可访问名称：

- `aria-label`
- `aria-labelledby`
- `title` 属性

### 使用 `aria-label` 的示例

```html
<div role="form" id="gift-cards" aria-label="购买礼品卡">
  <!-- 表单内容 -->
</div>
```

### 避免冗余描述

屏幕阅读器会宣布角色类型，因此不要在标签中重复它：

- **错误：** `aria-label="联系表单"`（会宣布“联系表单表单”）
- **正确：** `aria-label="联系信息"`（简洁且无冗余）

## 属性和交互

### 关联的 WAI-ARIA 角色、状态和属性

`form` 角色没有定义特定的角色状态或属性。

### 键盘交互

`form` 角色没有定义特定的键盘交互。

### 必需的 JavaScript 功能

- **`onsubmit` 事件处理程序：** 处理表单提交时触发的事件。
- 任何非原生 `<form>` 元素都不能通过标准表单提交机制提交数据。您必须使用 JavaScript 来构建替代的数据提交机制（例如使用 `fetch()` 或 `XMLHttpRequest`）。

## 可访问性问题

### 1. 稀疏使用

地标角色旨在用于文档中的较大整体区域。过度使用地标角色会在屏幕阅读器中产生“噪音”，使用户难以理解整个页面布局。

### 2. 输入不是表单

不要在单个表单元素（如输入框、文本区域、下拉框等）上声明 `role="form"`。应仅将角色应用于 **包装元素**。

```html
<!-- 错误 -->
<input role="form" type="text" />

<!-- 正确 -->
<div role="form" aria-label="用户信息">
  <input type="text" />
</div>
```

### 3. 搜索表单使用 `search` 角色

如果表单用于搜索功能，请使用更专业的 `role="search"` 替代 `role="form"`。

### 4. 使用原生表单控件

即使使用 `role="form"`，也应优先使用原生的 HTML 表单控件：

- `<button>`
- `<input>`
- `<select>`
- `<textarea>`
- `<label>`

## 最佳实践

- **优先使用 HTML `<form>` 元素。** 使用语义化的 `<form>` 元素可自动传达表单地标，无需 ARIA。
- **提供唯一的标签。** 文档中的每个表单都应具有唯一的可访问名称，以帮助用户理解其用途。
- **确保标签可见。** 标签应对于所有用户可见，而不仅仅是辅助技术用户。
- **使用适当的地标角色。** 搜索表单使用 `role="search"`，通用表单组使用 `role="form"`，并在可能的情况下使用 `<form>` HTML 元素。

## 规范

- [WAI-ARIA: 表单角色规范](https://w3c.github.io/aria/#form)
- [WAI-ARIA APG: 表单地标示例](https://www.w3.org/WAI/ARIA/apg/patterns/landmarks/examples/form.html)

## 相关参考资料

- [`<form>` HTML 元素（MDN）](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/form)
- [`<legend>` HTML 元素（MDN）](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/legend)
- [`<label>` HTML 元素（MDN）](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/label)
- [`search` ARIA 角色（MDN）](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/search_role)

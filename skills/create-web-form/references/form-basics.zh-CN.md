# 表单基础参考

本参考内容整合了 MDN Web 文档中关于创建和构建 HTML 网页表单的核心教育内容。

---

## 你的第一个表单

> **来源:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Your_first_form

### 什么是网页表单？

网页表单是用户与网站或应用程序之间交互的主要方式之一。它们允许用户输入数据，供服务器处理和存储，或者在客户端立即更新界面。

一个网页表单由以下部分组成：

- **表单控件（小部件）**：文本框、下拉菜单、按钮、复选框、单选按钮
- **附加元素**：主要使用 `<input>` 元素构建，再加上其他语义元素
- **表单标签**：与控件配对以提高可访问性

表单控件可以通过 **表单验证** 强制特定格式，并且应与文本标签配对，以兼顾视力正常用户和视障用户的需求。

### 设计你的表单

在编写任何代码之前，最佳实践包括：

- 在编写代码之前先退后一步进行规划
- 创建草图以定义所需的数据
- 保持表单简洁且专注
- 仅请求绝对必要的数据
- 较大的表单可能让用户感到沮丧并降低参与度

### `<form>` 元素

`<form>` 元素正式定义了一个表单容器及其行为。

```html
<form action="/my-handling-form-page" method="post">...</form>
```

**属性：**

| 属性 | 描述 |
|------|------|
| `action` | 提交表单数据时数据发送的 URL |
| `method` | 发送数据的 HTTP 方法（`get` 或 `post`） |

这两个属性都是可选的，但按照标准实践，应始终设置它们。

### `<label>`、`<input>` 和 `<textarea>` 元素

```html
<form action="/my-handling-form-page" method="post">
  <p>
    <label for="name">Name:</label>
    <input type="text" id="name" name="user_name" />
  </p>
  <p>
    <label for="mail">Email:</label>
    <input type="email" id="mail" name="user_email" />
  </p>
  <p>
    <label for="msg">Message:</label>
    <textarea id="msg" name="user_message"></textarea>
  </p>
</form>
```

#### `<label>` 元素

- `for` 属性必须与关联的表单控件的 `id` 匹配。
- 点击或轻触标签会激活其关联的控件。
- 为屏幕阅读器提供可访问的名称。
- 提高鼠标、触控板和触摸设备的可用性。

#### `<input>` 元素

`type` 属性定义了输入的外观和行为。

| 类型 | 描述 |
|------|------|
| `text` | 基本的单行文本框（默认）；接受任何文本 |
| `email` | 单行字段，用于验证格式正确的电子邮件地址；在移动设备上显示合适的键盘 |

`<input>` 是一个 **空元素** —— 它没有闭合标签。

设置默认值：

```html
<input type="text" value="by default this element is filled with this text" />
```

#### `<textarea>` 元素

一个用于较长消息的多行文本框。与 `<input>` 不同，它 **不是** 空元素，需要闭合标签。

设置默认值：

```html
<textarea>
by default this element is filled with this text
</textarea>
```

### `<button>` 元素

```html
<p class="button">
  <button type="submit">Send your message</button>
</p>
```

**`type` 属性值：**

| 值 | 描述 |
|----|------|
| `submit` | 将表单数据发送到 `<form>` 元素的 `action` 属性中定义的 URL（默认） |
| `reset` | 将所有小部件重置为其默认值（被视为用户体验的反模式，除非必要，否则应避免） |
| `button` | 默认不执行任何操作；适用于自定义 JavaScript 功能 |

`<button>` 元素优于 `<input type="submit">`，因为 `<button>` 允许在其内部包含完整的 HTML 内容，从而实现更复杂的样式设计，而 `<input>` 仅允许纯文本。

### 基础表单样式

```css
body {
  text-align: center;
}

form {
  display: inline-block;
  padding: 1em;
  border: 1px solid #cccccc;
  border-radius: 1em;
}

p + p {
  margin-top: 1em;
}

label {
  display: inline-block;
  min-width: 90px;
  text-align: right;
}

input,
textarea {
  font: 1em sans-serif;
  width: 300px;
  box-sizing: border-box;
  border: 1px solid #999999;
}

input:focus,
textarea:focus {
  outline-style: solid;
  outline-color: black;
}

textarea {
  vertical-align: top;
  height: 5em;
}

.button {
  padding-left: 90px;
}

button {
  margin-left: 0.5em;
}
```

### 将表单数据发送到你的 Web 服务器

表单数据以 **名称/值对** 的形式发送。每个应提交数据的表单控件都必须具有 `name` 属性。

```html
<form action="/my-handling-form-page" method="post">
  <input type="text" id="name" name="user_name" />
  <input type="email" id="mail" name="user_email" />
  <textarea id="msg" name="user_message"></textarea>
  <button type="submit">Send your message</button>
</form>
```

这个表单通过 HTTP POST 向 `/my-handling-form-page` 发送三段数据：

- `user_name` -- 用户的姓名
- `user_email` -- 用户的电子邮件
- `user_message` -- 用户的消息

每种服务器端语言（如 PHP、Python、Ruby、Java、C# 等）都有其使用 `name` 属性处理表单数据的机制。

### 完整示例

```html
<form action="/my-handling-form-page" method="post">
  <div>
    <label for="name">Name:</label>
    <input type="text" id="name" name="user_name" />
  </div>

  <div>
    <label for="mail">Email:</label>
    <input type="email" id="mail" name="user_email" />
  </div>

  <div>
    <label for="msg">Message:</label>
    <textarea id="msg" name="user_message"></textarea>
  </div>

  <div class="button">
    <button type="submit">Send your message</button>
  </div>
</form>
```

### 关键要点

1. **以可访问性为先**：始终使用带有 `for` 属性的 `<label>` 元素。
2. **语义 HTML**：使用适当的 `<input>` 类型（如电子邮件、文本等）。
3. **保持简洁**：仅请求必要的数据。
4. **命名你的控件**：每个输入都需要 `name` 属性以供表单提交。
5. **样式很重要**：表单需要 CSS 才能看起来专业。

---

## 如何构建网页表单结构

> **来源:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/How_to_structure_a_web_form

### `<form>` 元素

`<form>` 元素正式定义了表单及其行为。

关键点：

- 所有表单内容必须嵌套在 `<form>` 标签内。
- 助力技术（如 JAWS 和 NVDA）和浏览器插件可以发现 `<form>` 元素并提供特殊功能。
- **严格禁止在另一个表单内嵌套表单** —— 这会导致不可预测的行为。
- 表单控件可以位于 `<form>` 元素之外，但应使用 `form` 属性将其与表单关联。

### `<fieldset>` 和 `<legend>` 元素

`<fieldset>` 用于按样式和语义分组控件。`<legend>` 为 fieldset 提供描述性标签，直接位于 `<fieldset>` 开始标签之后。

许多助力技术（如 JAWS 和 NVDA）将 legend 文本视为 fieldset 内每个控件标签的一部分。

```html
<form>
  <fieldset>
    <legend>Fruit juice size</legend>
    <p>
      <input type="radio" name="size" id="size_1" value="small" />
      <label for="size_1">Small</label>
    </p>
    <p>
      <input type="radio" name="size" id="size_2" value="medium" />
      <label for="size_2">Medium</label>
    </p>
    <p>
      <input type="radio" name="size" id="size_3" value="large" />
      <label for="size_3">Large</label>
    </p>
  </fieldset>
</form>
```

屏幕阅读器会宣布： "Fruit juice size small," "Fruit juice size medium," "Fruit juice size large."

**使用场景：**

- 对单选按钮进行分组是必需的
- 将复杂的、多页的表单进行分段
- 当单页上有大量控件时，提高可用性

### `<label>` 元素

`<label>` 元素是正式定义 HTML 表单控件标签的方式。

#### 两种关联标签的方法

**方法 1：使用 `for` 属性（推荐）**

```html
<label for="name">Name:</label>
<input type="text" id="name" name="user_name" />
```

屏幕阅读器会宣布： "Name, edit text."

**方法 2：隐式关联（嵌套）**

```html
<label for="name">
  Name: <input type="text" id="name" name="user_name" />
</label>
```

**最佳实践**：即使在嵌套时，也始终设置 `for` 属性，以确保所有助力技术都能理解控件之间的关系。

#### 标签是可点击的

点击或轻触标签会激活对应的控件。这对于具有小点击区域的单选按钮和复选框尤其有用。

```html
<form>
  <p>
    <input type="checkbox" id="taste_1" name="taste_cherry" value="cherry" />
    <label for="taste_1">I like cherry</label>
  </p>
  <p>
    <input type="checkbox" id="taste_2" name="taste_banana" value="banana" />
    <label for="taste_2">I like banana</label>
  </p>
</form>
```

#### 处理多个标签

避免在一个控件上放置多个独立的标签。相反，将所有标签信息包含在一个 `<label>` 元素中：

```html
<div>
  <label for="username">Name *:</label>
  <input id="username" type="text" name="username" required />
</div>
```

### 常见与表单一起使用的 HTML 结构

推荐用于组织表单内容的结构元素：

- 使用 `<ul>` 或 `<ol>` 列表与 `<li>` 项目 —— 特别适合多个复选框或单选按钮
- 使用 `<p>` 和 `<div>` 元素包裹标签和控件
- 使用 `<section>` 元素将复杂的表单组织成逻辑分组
- 使用 HTML 标题（如 `<h1>`、`<h2>` 等）进行分段
- 如果表单有必填字段，请在表单开始前加入一段说明（例如： "* 必填"）

### 构建表单结构 —— 支付表单示例

```html
<form>
  <h1>支付表单</h1>
  <p>请完成所有必填字段（* 标记）。</p>

  <!-- 联系信息部分 -->
  <section>
    <h2>联系信息</h2>
    <fieldset>
      <legend>头衔</legend>
      <ul>
        <li>
          <label for="title_1">
            <input type="radio" id="title_1" name="title" value="A" />
            Ace
          </label>
        </li>
        <li>
          <label for="title_2">
            <input type="radio" id="title_2" name="title" value="K" />
            King
          </label>
        </li>
        <li>
          <label for="title_3">
            <input type="radio" id="title_3" name="title" value="Q" />
            Queen
          </label>
        </li>
      </ul>
    </fieldset>
    <p>
      <label for="name">Name *:</label>
      <input type="text" id="name" name="username" required />
    </p>
    <p>
      <label for="mail">Email *:</label>
      <input type="email" id="mail" name="user-mail" required />
    </p>
    <p>
      <label for="pwd">Password *:</label>
      <input type="password" id="pwd" name="password" required />
    </p>
  </section>

  <!-- 支付信息部分 -->
  <section>
    <h2>支付信息</h2>
    <p>
      <label for="card">
        <span>卡类型:</span>
      </label>
      <select id="card" name="user-card">
        <option value="visa">Visa</option>
        <option value="mc">Mastercard</option>
        <option value="amex">American Express</option>
      </select>
    </p>
    <p>
      <label for="number">Card number *:</label>
      <input
        type="tel"
        id="number"
        name="card-number"
        required
        placeholder="MM/YY"
        pattern="^(0[1-9]|1[0-2])\/([0-9]{2})$" />
    </p>
  </section>

  <!-- 提交部分 -->
  <section>
    <p>
      <button type="submit">验证支付</button>
    </p>
  </section>
</form>
```

### 重要属性参考

| 属性 | 元素 | 用途 |
|------|------|------|
| `for` | `<label>` | 通过匹配控件的 `id` 将标签与表单控件关联 |
| `id` | 表单控件 | 用于与标签关联的唯一标识符 |
| `name` | 表单控件 | 识别与表单一起提交的数据 |
| `required` | 表单控件 | 标记为提交时必填字段 |
| `placeholder` | `<input>` | 在字段中显示示例格式（例如："MM/YY"） |
| `pattern` | `<input>` | 客户端验证的正则表达式 |
| `form` | 表单控件 | 即使控件位于表单之外，也将其与 `<form>` 关联 |
| `type` | `<input>`、`<button>` | 指定输入行为（文本、电子邮件、密码、电话等） |

### 可访问性表单结构的关键最佳实践

1. 始终使用 `<form>` 元素包裹所有表单内容。
2. 使用 `<fieldset>` 和 `<legend>` 对相关控件进行分组，尤其是单选按钮。
3. 始终使用指向控件 `id` 的 `for` 属性将标签与表单控件关联。
4. 使用语义 HTML（如 `<section>`、标题）来组织复杂的表单。
5. 在表单开始前加入一段说明，解释必填字段的标记（例如： "* 必填"）。
6. 对多个复选框或单选按钮使用列表（`<ul>`/`<ol>`）。
7. 使用屏幕阅读器进行测试以验证可访问性。
8. 从不将表单嵌套在另一个表单中。
9. 使标签可点击，以增加复选框和单选按钮控件的点击区域。

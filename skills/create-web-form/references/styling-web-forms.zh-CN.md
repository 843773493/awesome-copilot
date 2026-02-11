# Web表单样式化参考

---

## 1. Web表单样式化

> **来源:** <https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Styling_web_forms>

### 概述

本节介绍用于样式化HTML表单元素的CSS技术。理解哪些表单元素易于样式化，哪些需要特殊技术是至关重要的。

**前提条件：**

- 对HTML的基本理解
- CSS样式化基础

**目标：** 学习适用于表单控件的样式化技术，并了解其中的挑战。

### 表单控件样式化的挑战

#### 历史背景

- **1995年：** HTML 2规范引入了表单控件。
- **1996年末：** CSS发布，但尚未广泛支持。
- **早期时代：** 浏览器依赖操作系统渲染表单控件。
- **现代时代：** 大多数表单控件现在都可以样式化，但有一些例外。

#### 表单控件分类

**易于样式化的元素：**

1. `<form>`
2. `<fieldset>` 和 `<legend>`
3. 单行文本 `<input>`（类型：text, url, email）
4. 多行 `<textarea>`
5. 按钮（`<input>` 和 `<button>`）
6. `<label>`
7. `<output>`

**较难样式化的元素：**

- 复选框和单选按钮
- `<input type="search">`
- （详见“高级表单样式化”部分的技巧）

**无法仅通过CSS样式化的元素：**

- `<input type="color">`
- 日期相关控件（`<input type="datetime-local">`）
- `<input type="range">`
- `<input type="file">`
- `<select>`、`<option>`、`<optgroup>`、`<datalist>`
- `<progress>` 和 `<meter>`

### 简单表单控件样式化

#### 字体和文本

**问题：** 浏览器不一致地继承 `font-family` 和 `font-size` —— 许多浏览器使用系统默认值。

**解决方案：** 强制继承以实现一致的样式：

```css
button,
input,
select,
textarea {
  font-family: inherit;
  font-size: 100%;
}
```

`inherit` 值匹配父元素的计算属性值。

**注意：** `<input type="submit">` 在某些浏览器中无法继承；为了更好的一致性，请改用 `<button>`。

#### 盒模型

**问题：** 每个控件有不同的默认边框、内边距和外边距规则。

**解决方案：** 使用 `box-sizing` 保持一致的尺寸：

```css
input,
textarea,
select,
button {
  width: 150px;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}
```

这确保了所有元素在使用原生平台默认值时占据相同的空间。

#### 图例位置调整

默认情况下，`<legend>` 元素位于 `<fieldset>` 边框之上。要重新定位它：

```css
fieldset {
  position: relative;
}

legend {
  position: absolute;
  bottom: 0;
  right: 0;
  color: white;
  background-color: black;
  padding: 3px;
}
```

示例HTML：

```html
<form>
  <fieldset>
    <legend>选择你喜欢的蔬菜</legend>
    <ul>
      <li>
        <label for="carrots">胡萝卜</label>
        <input
          type="checkbox"
          checked
          id="carrots"
          name="carrots"
          value="carrots" />
      </li>
      <li>
        <label for="peas">豌豆</label>
        <input type="checkbox" id="peas" name="peas" value="peas" />
      </li>
    </ul>
  </fieldset>
</form>
```

**可访问性注意：** `<legend>` 内容会被辅助技术读出。视觉上重新定位它，但要确保其在DOM中保留。考虑使用 `transform` 而不是定位，以避免边框间隙。

### 实用样式化示例：明信片表单

#### HTML结构

```html
<form>
  <h1>寄给：Mozilla</h1>

  <div id="from">
    <label for="name">来自：</label>
    <input type="text" id="name" name="user_name" />
  </div>

  <div id="reply">
    <label for="mail">回复：</label>
    <input type="email" id="mail" name="user_email" />
  </div>

  <div id="message">
    <label for="msg">你的信息：</label>
    <textarea id="msg" name="user_message"></textarea>
  </div>

  <div class="button">
    <button type="submit">发送你的信息</button>
  </div>
</form>
```

#### 设置网络字体

```css
@font-face {
  font-family: "手写体";
  src:
    url("fonts/journal-webfont.woff2") format("woff2"),
    url("fonts/journal-webfont.woff") format("woff");
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: "打字机字体";
  src:
    url("fonts/momot___-webfont.woff2") format("woff2"),
    url("fonts/momot___-webfont.woff") format("woff");
  font-weight: normal;
  font-style: normal;
}
```

#### 整体布局

```css
body {
  font: 1.3rem sans-serif;
  padding: 0.5em;
  margin: 0;
  background: #222222;
}

form {
  position: relative;
  width: 740px;
  height: 498px;
  margin: 0 auto;
  padding: 1em;
  box-sizing: border-box;
  background: white url("background.jpg");

  /* 使用CSS Grid布局 */
  display: grid;
  grid-gap: 20px;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: 10em 1em 1em 1em;
}
```

#### 标题和布局

```css
h1 {
  font:
    1em "打字机字体",
    monospace;
  align-self: end;
}

#message {
  grid-row: 1 / 5;
}

#from,
#reply {
  display: flex;
}
```

#### 标签样式

```css
label {
  font:
    0.8em "打字机字体",
    sans-serif;
}
```

#### 文本字段样式

```css
input,
textarea {
  font:
    1.4em/1.5em "手写体",
    cursive,
    sans-serif;
  border: none;
  padding: 0 10px;
  margin: 0;
  width: 80%;
  background: none;
}

input:focus,
textarea:focus {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}
```

#### 文本区域调整

```css
textarea {
  display: block;
  padding: 10px;
  margin: 10px 0 0 -10px;
  width: 100%;
  height: 90%;
  border-right: 1px solid;
  /* resize: none; */
  overflow: auto;
}
```

提示：

- 仅在必要时使用 `resize: none`（避免限制用户控制）。
- 设置 `overflow: auto` 以实现跨浏览器一致的滚动效果。

#### 按钮样式化

```css
button {
  padding: 5px;
  font: bold 0.6em sans-serif;
  border: 2px solid #333333;
  border-radius: 5px;
  background: none;
  cursor: pointer;
  transform: rotate(-1.5deg);
}

button::after {
  content: " >>>";
}
```

### 表单中关键的CSS属性

| 属性 | 用途 |
|---|---|
| `font-family: inherit` | 继承父元素字体 |
| `font-size: 100%` | 继承父元素尺寸 |
| `box-sizing: border-box` | 将内边距/边框包含在宽度内 |
| `border: none` | 移除默认边框 |
| `padding` | 在元素内部添加空间 |
| `margin` | 在元素外部添加空间 |
| `background` | 控制背景外观 |
| `:focus` | 样式化聚焦的表单字段 |
| `resize` | 允许/阻止文本区域调整大小 |
| `overflow: auto` | 保持滚动一致 |

### 最佳实践

1. **一致性：** 使用 `box-sizing: border-box` 以实现可预测的尺寸。
2. **继承：** 明确设置表单元素的 `font-family` 和 `font-size`。
3. **可访问性：** 始终为键盘导航添加 `:focus` 样式。
4. **浏览器兼容性：** 在不同浏览器中测试以确保一致的渲染。
5. **用户控制：** 避免移除有用的默认样式（如文本区域调整大小）。
6. **自定义字体：** 使用 `@font-face` 并包含多种格式（woff2 + woff）以提高兼容性。

---

## 2. 高级表单样式化

> **来源:** <https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Advanced_form_styling>

### 概述

本节介绍样式化那些使用CSS难以样式的表单控件，分为“较难”（需要更复杂的CSS）和“难以彻底样式化”（无法完全样式化）两类。

**较难样式化的控件：**

- 复选框和单选按钮
- `<input type="search">`

**难以彻底样式化的控件：**

- 下拉控件：`<select>`、`<option>`、`<optgroup>`、`<datalist>`
- `<input type="color">`
- 日期相关控件（`<input type="datetime-local">`）
- `<input type="range">`
- `<input type="file">`
- `<progress>` 和 `<meter>`

### `appearance` 属性

`appearance` 属性用于控制表单控件的系统级样式。最有用的值是 `none`，它会移除系统级样式并允许自定义CSS样式。

```css
input {
  appearance: none;
}
```

这会阻止控件使用系统级样式，从而允许你通过CSS构建自定义样式。

### 复选框和单选按钮的样式化

#### 方法：使用 `appearance: none`

彻底移除默认的复选框/单选按钮样式，并创建自定义设计：

```html
<form>
  <fieldset>
    <legend>水果偏好</legend>
    <p>
      <label>
        <input type="checkbox" name="fruit" value="cherry" />
        我喜欢樱桃
      </label>
    </p>
    <p>
      <label>
        <input type="checkbox" name="fruit" value="banana" disabled />
        我不能喜欢香蕉
      </label>
    </p>
  </fieldset>
</form>
```

#### 自定义复选框样式

```css
input[type="checkbox"] {
  appearance: none;
  position: relative;
  width: 1em;
  height: 1em;
  border: 1px solid gray;
  /* 调整复选框在文本基线的位置 */
  vertical-align: -2px;
  /* 设置在此处以便Windows的高对比度模式可以覆盖 */
  color: green;
}

input[type="checkbox"]::before {
  content: "\2714";
  position: absolute;
  font-size: 1.2em;
  right: -1px;
  top: -0.3em;
  visibility: hidden;
}

input[type="checkbox"]:checked::before {
  /* 使用 `visibility` 而不是 `display` 以避免重新计算布局 */
  visibility: visible;
}

input[type="checkbox"]:disabled {
  border-color: black;
  background: #dddddd;
  color: gray;
}
```

**关键伪类：**

- `:checked` —— 复选框/单选按钮处于选中状态
- `:disabled` —— 复选框/单选按钮被禁用，无法交互
- `:default` —— 页面加载时默认选中的元素

### 使用 `appearance` 样式化搜索框

对于 `<input type="search">` 元素，`appearance: none` 在历史上是必需的，但在Safari 16+中不再需要。

移除“x”删除按钮：

```css
input[type="search"]:not(:focus, :active)::-webkit-search-cancel-button {
  display: none;
}
```

### 样式化“难以彻底样式化”的表单控件

#### 全局规范化

为所有表单控件应用一致的样式：

```css
button,
label,
input,
select,
progress,
meter {
  display: block;
  font-family: inherit;
  font-size: 100%;
  margin: 0;
  box-sizing: border-box;
  width: 100%;
  padding: 5px;
  height: 30px;
}
```

### 样式化 `<select>` 和 `<datalist>` 元素

#### 创建自定义下拉箭头

```html
<label for="select">下拉框：</label>
<div class="select-wrapper">
  <select id="select" name="select">
    <option>Banana</option>
    <option>Cherry</option>
    <option>Lemon</option>
  </select>
</div>
```

```css
select {
  appearance: none;
  width: 100%;
  height: 100%;
}

.select-wrapper {
  position: relative;
}

.select-wrapper::after {
  content: "\25BC";
  font-size: 1rem;
  top: 3px;
  right: 10px;
  position: absolute;
}
```

**限制：**

- 无法样式化点击后出现的下拉选项框。
- 无法样式化 `<datalist>` 的自动补全列表。
- 要完全控制这些元素，请使用库、构建自定义控件或使用现代HTML/CSS特性如可定制的下拉框。

### 样式化日期输入类型

日期/时间输入（`datetime-local`、`time`、`week`、`month`）的样式化选项有限：

```css
input[type="datetime-local"] {
  box-shadow: inset 1px 1px 3px #cccccc;
  border-radius: 5px;
}
```

可以样式化包含框，但内部部分（弹出日历、滑块）无法样式化。要完全控制，请使用自定义控件库。

### 样式化范围滑块

范围滑块需要大量的CSS工作量进行定制：

```css
input[type="range"] {
  appearance: none;
  background: red;
  height: 2px;
  padding: 0;
  outline: 1px solid transparent;
}
```

完整的范围样式化需要复杂的CSS以及浏览器特定的伪元素（`::-webkit-slider-thumb`、`::-moz-range-thumb` 等）。

### 样式化颜色输入类型

```css
input[type="color"] {
  border: 0;
  padding: 0;
}
```

如需更显著的自定义，需要自定义解决方案。

### 样式化文件输入类型

文件输入大部分可以样式化，但文件选择按钮完全无法样式化。推荐做法是隐藏输入并样式化标签。

```html
<label for="file">选择要上传的文件</label>
<input id="file" name="file" type="file" multiple />
```

```css
input[type="file"] {
  height: 0;
  padding: 0;
  opacity: 0;
}

label[for="file"] {
  box-shadow: 1px 1px 3px #cccccc;
  background: linear-gradient(to bottom, #eeeeee, #cccccc);
  border: 1px solid darkgrey;
  border-radius: 5px;
  text-align: center;
  line-height: 1.5;
}
```

#### JavaScript显示文件信息

```javascript
const fileInput = document.querySelector("#file");
const fileList = document.querySelector("#file-list");

fileInput.addEventListener("change", updateFileList);

function updateFileList() {
  while (fileList.firstChild) {
    fileList.removeChild(fileList.firstChild);
  }

  const curFiles = fileInput.files;

  if (curFiles.length > 0) {
    for (const file of curFiles) {
      const listItem = document.createElement("li");
      listItem.textContent = `文件名: ${file.name}; 文件大小: ${returnFileSize(file.size)}.`;
      fileList.appendChild(listItem);
    }
  }
}

function returnFileSize(number) {
  if (number < 1e3) {
    return `${number} 字节`;
  } else if (number >= 1e3 && number < 1e6) {
    return `${(number / 1e3).toFixed(1)} KB`;
  }
  return `${(number / 1e6).toFixed(1)} MB`;
}
```

### 样式化进度条和计量条

进度条和计量条是最难样式化的。

```css
progress,
meter {
  display: block;
  width: 100%;
  padding: 5px;
  height: 30px;
}
```

**限制：**

- 不同浏览器对高度处理不一致。
- 无法单独样式化前景条颜色。
- `appearance: none` 会使情况变得更糟，而不是更好。
- **建议：** 使用自定义解决方案或第三方库。

### 样式化方法总结

| 控件类型 | 方法 | 难度 |
|---|---|---|
| 复选框/单选按钮 | `appearance: none` + 自定义设计 | 中等 |
| 搜索输入 | `appearance: none` 用于旧版浏览器 | 低 |
| 下拉框/数据列表 | 包裹元素 + 自定义箭头，控制有限 | 中等 |
| 日期输入 | 仅基础样式化 | 高 |
| 范围滑块 | `appearance: none` + 复杂伪元素 | 高 |
| 颜色输入 | 移除边框/内边距 | 低 |
| 文件输入 | 隐藏 + 样式化标签 | 中等 |
| 进度条/计量条 | 推荐使用自定义解决方案 | 非常高 |

### 关键要点

1. 使用 `appearance: none` 移除操作系统级样式，再应用自定义CSS。
2. 伪类如 `:checked` 和 `:disabled` 对表单控件状态至关重要。
3. 某些控件（如下拉选项、文件选择按钮、进度条内部）存在固有限制。
4. 对于“难以彻底样式化”的元素，考虑使用自定义JavaScript控件、第三方库或现代HTML/CSS特性如可定制的下拉框。

---

## 3. 可定制的下拉框元素

> **来源:** <https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Customizable_select>

### 概述

可定制的下拉框元素允许你使用实验性的HTML和CSS特性来构建完全样式化的 `<select>` 元素，并完全控制：

- 下拉框按钮的样式
- 下拉选择器的外观
- 箭头图标的设计
- 当前选择的勾选标记
- 单个 `<option>` 元素的样式

**警告：** 这些功能在浏览器中支持有限。某些JavaScript框架中，这些功能可能导致水合失败（hydration failures）。

### 可定制下拉框包含哪些功能？

#### HTML元素

**`<select>`、`<option>`、`<optgroup>` 元素：**

- 与传统下拉框类似，但允许额外的内容类型。
- `<option>` 元素现在可以包含标记（如 `<span>`、`<img>`、语义元素）而不仅仅是文本。

**`<button>` 元素在 `<select>` 内部：**

- `<select>` 的第一个子元素（此前不允许）。
- 替代默认关闭下拉框的按钮渲染。
- 被称为 **下拉框按钮**（打开下拉选择器）。
- 默认情况下，下拉框按钮是 `inert`，使其子元素无法聚焦。

**`<selectedcontent>` 元素：**

- 可选地放置在第一个 `<button>` 子元素内部。
- 显示关闭下拉框时当前选择的值。
- 包含当前选择的 `<option>` 内容的克隆。

#### CSS属性和伪元素

| 功能 | 用途 |
|---|---|
| `appearance: base-select` | 启用浏览器定义的自定义下拉框样式（需同时应用于 `select` 和 `::picker(select)`） |
| `::picker(select)` | 目标为整个选择器内容（所有元素除第一个 `<button>`） |
| `::picker-icon` | 目标为下拉框按钮内的箭头图标 |
| `::checkmark` | 目标为当前选择的 `<option>` 中的勾选标记 |
| `:open` | 目标为打开选择器时的下拉框按钮 |
| `:checked` | 目标为当前选择的 `<option>` |
| `:popover-open` | 目标为显示状态的下拉框（通过弹出窗口API） |

#### 自动行为

- **调用者/弹出窗口关系** 通过弹出窗口API实现。
- **隐式锚点参考** 通过CSS锚点定位（无需显式锚点名称/锚点定位）。
- **自动定位** 并提供回退选项以防止视口溢出。

### HTML标记结构

#### 基本示例：宠物选择器

```html
<form>
  <p>
    <label for="select">选择宠物：</label>
    <select id="select" name="select">
      <button>
        <selectedcontent></selectedcontent>
      </button>

      <option value="">请选择宠物</option>
      <option value="cat">
        <span class="icon" aria-hidden="true">&#x1F431;</span>
        <span class="option-label">猫</span>
      </option>
      <option value="dog">
        <span class="icon" aria-hidden="true">&#x1F436;</span>
        <span class="option-label">狗</span>
      </option>
      <option value="hamster">
        <span class="icon" aria-hidden="true">&#x1F439;</span>
        <span class="option-label">仓鼠</span>
      </option>
      <option value="chicken">
        <span class="icon" aria-hidden="true">&#x1F414;</span>
        <span class="option-label">鸡</span>
      </option>
      <option value="fish">
        <span class="icon" aria-hidden="true">&#x1F41F;</span>
        <span class="option-label">鱼</span>
      </option>
      <option value="snake">
        <span class="icon" aria-hidden="true">&#x1F40D;</span>
        <span class="option-label">蛇</span>
      </option>
    </select>
  </p>
</form>
```

**关键标记点：**

- 在装饰性图标上使用 `aria-hidden="true"` 以防止辅助技术重复读取。
- `<button><selectedcontent></selectedcontent></button>` 表示下拉框按钮，允许样式化。
- 多元素 `<option>` 内容会被克隆到 `<selectedcontent>` 并在关闭下拉框时显示。
- **渐进增强：** 不支持的浏览器会忽略按钮结构并移除非文本选项内容。

#### 值提取规则

当 `<option>` 包含多层DOM子树时：

1. 浏览器获取 `textContent` 属性。
2. 应用 `trim()`。
3. 将结果设置为 `<select>` 的值。

### CSS样式化技巧

#### 1. 启用自定义下拉框渲染

**必要第一步：**

```css
select,
::picker(select) {
  appearance: base-select;
}
```

这会移除操作系统级样式，启用自定义浏览器基础样式。

#### 2. 样式化下拉框按钮

```css
* {
  box-sizing: border-box;
}

html {
  font-family: "Helvetica", "Arial", sans-serif;
}

select {
  border: 2px solid #dddddd;
  background: #eeeeee;
  padding: 10px;
  transition: 0.4s;
  flex: 1;
}

select:hover,
select:focus {
  background: #dddddd;
}
```

#### 3. 样式化下拉框箭头图标

```css
select::picker-icon {
  color: #999999;
  transition: 0.4s rotate;
}

/* 当下拉框打开时旋转箭头图标 */
select:open::picker-icon {
  rotate: 180deg;
}
```

#### 4. 样式化下拉框内容

```css
::picker(select) {
  border: none;
  border-radius: 8px;
}

option {
  display: flex;
  justify-content: flex-start;
  gap: 20px;

  border: 2px solid #dddddd;
  background: #eeeeee;
  padding: 10px;
  transition: 0.4s;
}

/* 圆角顶部和底部 */
option:first-of-type {
  border-radius: 8px 8px 0 0;
}

option:last-of-type {
  border-radius: 0 0 8px 8px;
}

/* 移除除最后一个外的所有内边框 */
option:not(option:last-of-type) {
  border-bottom: none;
}

/* 条纹样式 */
option:nth-of-type(odd) {
  background: white;
}

/* 高亮悬停/聚焦状态 */
option:hover,
option:focus {
  background: plum;
}
```

#### 5. 样式化当前选择内容

```css
option::checkmark {
  order: 1;
  margin-left: auto;
  content: "\2611\FE0F";
}
```

**注意：** `::checkmark` 不在可访问性树中；生成内容不会被辅助技术读出。

### 样式化“难以彻底样式化”的表单控件

#### 全局规范化

为所有表单控件应用一致的样式：

```css
button,
label,
input,
select,
progress,
meter {
  display: block;
  font-family: inherit;
  font-size: 100%;
  margin: 0;
  box-sizing: border-box;
  width: 100%;
  padding: 5px;
  height: 30px;
}

input[type="text"],
input[type="datetime-local"],
input[type="color"],
select {
  box-shadow: inset 1px 1px 3px #cccccc;
  border-radius: 5px;
}
```

### 样式化 `<select>` 和 `<datalist>` 元素

#### 创建自定义下拉框箭头

```html
<label for="select">下拉框：</label>
<div class="select-wrapper">
  <select id="select" name="select">
    <option value="">请选择宠物</option>
    <option value="cat">
      <span class="icon" aria-hidden="true">&#x1F431;</span>
      <span class="option-label">猫</span>
    </option>
    <option value="dog">
      <span class="icon" aria-hidden="true">&#x1F436;</span>
      <span class="option-label">狗</span>
    </option>
    <option value="hamster">
      <span class="icon" aria-hidden="true">&#x1F439;</span>
      <span class="option-label">仓鼠</span>
    </option>
  </select>
</div>
```

```css
select {
  appearance: none;
  width: 100%;
  height: 100%;
}

.select-wrapper {
  position: relative;
}

.select-wrapper::after {
  content: "\25BC";
  font-size: 1rem;
  top: 3px;
  right: 10px;
  position: absolute;
}
```

**限制：**

- 无法样式化点击后出现的下拉选项框。
- 无法样式化 `<datalist>` 的自动补全列表。
- 要完全控制，请使用库、构建自定义控件或使用 `multiple` 属性。

### 样式化日期输入类型

日期/时间输入（`datetime-local`、`time`、`week`、`month`）的样式化选项有限：

```css
input[type="datetime-local"] {
  box-shadow: inset 1px 1px 3px #cccccc;
  border-radius: 5px;
}
```

可以样式化包含框，但内部部分（弹出日历、滑块）无法样式化。要完全控制，请使用自定义控件库。

### 样式化范围滑块

范围滑块需要大量CSS工作量进行定制：

```css
input[type="range"] {
  appearance: none;
  background: red;
  height: 2px;
  padding: 0;
  outline: 1px solid transparent;
}
```

完整的范围样式化需要复杂的CSS以及浏览器特定的伪元素（`::-webkit-slider-thumb`、`::-moz-range-thumb` 等）。

### 样式化颜色输入类型

```css
input[type="color"] {
  border: 0;
  padding: 0;
}
```

如需更显著的自定义，需要自定义解决方案。

### 样式化文件输入类型

文件输入大部分可以样式化，但文件选择按钮完全无法样式化。推荐做法是隐藏输入并样式化标签。

```html
<label for="file">选择要上传的文件</label>
<input id="file" name="file" type="file" multiple />
```

```css
input[type="file"] {
  height: 0;
  padding: 0;
  opacity: 0;
}

label[for="file"] {
  box-shadow: 1px 1px 3px #cccccc;
  background: linear-gradient(to bottom, #eeeeee, #cccccc);
  border: 1px solid darkgrey;
  border-radius: 5px;
  text-align: center;
  line-height: 1.5;
}

label[for="file"]:hover {
  background: linear-gradient(to bottom, white, #dddddd);
}

label[for="file"]:active {
  box-shadow: inset 1px 1px 3px #cccccc;
}
```

#### JavaScript显示文件信息

```javascript
const fileInput = document.querySelector("#file");
const fileList = document.querySelector("#file-list");

fileInput.addEventListener("change", updateFileList);

function updateFileList() {
  while (fileList.firstChild) {
    fileList.removeChild(fileList.firstChild);
  }

  const curFiles = fileInput.files;

  if (curFiles.length > 0) {
    for (const file of curFiles) {
      const listItem = document.createElement("li");
      listItem.textContent = `文件名: ${file.name}; 文件大小: ${returnFileSize(file.size)}.`;
      fileList.appendChild(listItem);
    }
  }
}

function returnFileSize(number) {
  if (number < 1e3) {
    return `${number} 字节`;
  } else if (number >= 1e3 && number < 1e6) {
    return `${(number / 1e3).toFixed(1)} KB`;
  }
  return `${(number / 1e6).toFixed(1)} MB`;
}
```

### 样式化进度条和计量条元素

进度条和计量条是最难样式化的。

```css
progress,
meter {
  display: block;
  width: 100%;
  padding: 5px;
  height: 30px;
}
```

**限制：**

- 不同浏览器对高度处理不一致。
- 无法单独样式化前景条颜色。
- `appearance: none` 会使情况变得更糟，而不是更好。
- **建议：** 使用自定义解决方案或第三方库。

### 样式化方法总结

| 控件类型 | 方法 | 难度 |
|---|---|---|
| 复选框/单选按钮 | `appearance: none` + 自定义设计 | 中等 |
| 搜索输入 | `appearance: none` 用于旧版浏览器 | 低 |
| 下拉框/数据列表 | 包裹元素 + 自定义箭头，控制有限 | 中等 |
| 日期输入 | 仅基础样式化 | 高 |
| 范围滑块 | `appearance: none` + 复杂伪元素 | 高 |
| 颜色输入 | 移除边框/内边距 | 低 |
| 文件输入 | 隐藏 + 样式化标签 | 中等 |
| 进度条/计量条 | 推荐使用自定义解决方案 | 非常高 |

### 关键要点

1. 使用 `appearance: none` 移除操作系统级样式，再应用自定义CSS。
2. 伪类如 `:checked` 和 `:disabled` 对表单控件状态至关重要。
3. 某些控件（如下拉选项、文件按钮、进度条内部）存在固有限制。
4. 对于“难以彻底样式化”的元素，考虑使用自定义JavaScript控件、第三方库或现代HTML/CSS特性如可定制的下拉框。

---

## 4. UI伪类

> **来源:** <https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/UI_pseudo-classes>

### 概述

CSS中的UI伪类允许你根据表单控件的不同状态进行样式化。本节介绍如何使用CSS选择器来样式化不同状态的表单。

**前提条件：**

- 对HTML和CSS的基本理解
- 对伪类和伪元素的知识

**目标：** 理解表单中哪些部分难以样式化以及原因，并学习如何使用伪类自定义表单控件。

### 可用的伪类

#### 常见伪类

- **`:hover`** —— 仅当鼠标指针悬停在元素上时选择。
- **`:focus`** —— 仅当通过键盘聚焦时选择。
- **`:active`** —— 仅当激活元素（点击或按Return/Enter键）时选择。

#### 表单特定伪类

**必需和可选：**

- **`:required`** —— 目标为带有 `required` HTML属性的元素。
- **`:optional`** —— 目标为可选表单控件。

**验证状态：**

- **`:valid`** —— 目标为数据有效的表单控件。
- **`:invalid`** —— 目标为数据无效的表单控件。
- **`:in-range`** —— 目标为数值在min/max范围内的输入。
- **`:out-of-range`** —— 目标为数值超出min/max范围的输入。

**启用/禁用和只读状态：**

- **`:enabled`** —— 目标为可激活的元素。
- **`:disabled`** —— 目标为不可交互的元素。
- **`:read-only`** —— 目标为带有 `readonly` 属性的元素。
- **`:read-write`** —— 目标为可编辑的表单控件（默认状态）。

**复选框和单选按钮状态：**

- **`:checked`** —— 目标为选中的复选框和单选按钮。
- **`:indeterminate`** —— 目标为既未选中也未取消选中的元素。
- **`:default`** —— 目标为页面加载时默认选中的元素。

#### 其他有用的伪类

- **`:focus-within`** —— 当元素或其子元素被聚焦时匹配。
- **`:focus-visible`** —— 当通过键盘交互聚焦时匹配（非触摸/鼠标）。
- **`:placeholder-shown`** —— 当 `<input>` 或 `<textarea>` 为空时显示占位符文本。

### 根据必填或可选状态样式化输入

#### HTML结构

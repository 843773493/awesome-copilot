# HTML表单元素参考

来自Mozilla开发者网络（MDN）Web文档的HTML表单相关元素综合参考。

---

## 目录

1. [`<form>`](#form)
2. [`HTMLFormElement.elements`](#htmlformelementelements)
3. [`<button>`](#button)
4. [`<datalist>`](#datalist)
5. [`<fieldset>`](#fieldset)
6. [`<input>`](#input)
7. [`<label>`](#label)
8. [`<legend>`](#legend)
9. [`<meter>`](#meter)
10. [`<optgroup>`](#optgroup)
11. [`<option>`](#option)
12. [`<output>`](#output)
13. [`<progress>`](#progress)
14. [`<select>`](#select)
15. [`<textarea>`](#textarea)

---

## `<form>`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/form>

### 描述

`<form>`元素表示一个包含用于向服务器提交信息的交互控件的文档部分。必须同时包含开始和结束标签。表单不能嵌套在其他表单中。

### 关键属性

| 属性 | 描述 |
|------|------|
| `action` | 处理表单提交的URL。可以通过提交按钮的`formaction`属性覆盖。 |
| `method` | HTTP方法：`get`（默认）、`post`或`dialog`。定义数据如何发送。 |
| `enctype` | POST提交的MIME类型：`application/x-www-form-urlencoded`（默认）、`multipart/form-data`（用于文件）、`text/plain`。 |
| `novalidate` | 布尔属性，禁用表单提交时的验证。 |
| `autocomplete` | 控制自动补全：`on`（默认）或`off`。 |
| `accept-charset` | 接受的字符编码（通常为`UTF-8`）。 |
| `name` | 表单的标识符；必须唯一。成为`window`、`document`和`document.forms`的属性。 |
| `target` | 显示响应的位置：`_self`（默认）、`_blank`、`_parent`、`_top`。 |
| `rel` | 链接关系类型：`external`、`nofollow`、`noopener`、`noreferrer`等。 |

### 使用说明

- 表单**不能嵌套其他表单**。
- 支持CSS伪类：`valid`和`invalid`用于根据表单有效性进行样式控制。
- DOM接口：`HTMLFormElement`。
- 隐式ARIA角色：`form`。

### 示例

```html
<form action="/submit" method="post">
  <div>
    <label for="name">姓名：</label>
    <input type="text" id="name" name="name" required />
  </div>
  <div>
    <label for="email">电子邮件：</label>
    <input type="email" id="email" name="email" required />
  </div>
  <input type="submit" value="提交" />
</form>
```

---

## `HTMLFormElement.elements`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/elements>

### 描述

`elements`属性返回一个`HTMLFormControlsCollection`，其中包含与`<form>`元素相关的所有表单控件。可以通过索引或`name`/`id`属性访问控件。

### 返回值

- **类型:** `HTMLFormControlsCollection`（基于`HTMLCollection`的实时集合）
- **实时性:** 是 -- 当控件被添加或移除时会自动更新。
- **顺序:** 树状顺序（深度优先遍历文档）。

### 包含的表单控件

该集合包括：

- `<button>`
- `<fieldset>`
- `<input>`（除`type="image"`外）
- `<object>`
- `<output>`
- `<select>`
- `<textarea>`
- 与表单关联的自定义元素

**注意:** `<label>`和`<legend>`元素**不包含**在内。

### 示例

```javascript
// 访问表单控件
const inputs = document.getElementById("my-form").elements;
const firstControl = inputs[0];           // 通过索引
const byName = inputs["username"];        // 通过name属性

// 遍历控件
for (const control of inputs) {
  if (control.nodeName === "INPUT" && control.type === "text") {
    control.value = control.value.toUpperCase();
  }
}

// 获取控件数量
console.log(inputs.length);
```

---

## `<button>`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button>

### 描述

`<button>`元素是一个交互元素，用户通过鼠标、键盘、手指、语音或辅助技术激活它，执行操作，例如提交表单或打开对话框。默认情况下，其外观反映用户的平台，但可以通过CSS进行完全自定义。

### 关键属性

| 属性 | 描述 |
|------|------|
| `type` | 指定行为：`submit`（表单默认）、`reset`（重置表单）、`button`（无默认行为）。 |
| `disabled` | 布尔属性，阻止用户交互。 |
| `name` | 表单控件的名称，用于提交。 |
| `value` | 提交表单时控件的值。 |
| `form` | 通过ID将按钮与表单关联，即使按钮未嵌套在表单中。 |
| `formaction` | 覆盖表单的`action`URL。 |
| `formmethod` | 覆盖表单的HTTP方法（`post`/`get`）。 |
| `autofocus` | 页面加载时给按钮聚焦。 |
| `popovertarget` | 通过ID控制一个弹出面板元素。 |
| `popovertargetaction` | 弹出面板操作：`show`、`hide`或`toggle`。 |

### 使用说明

- **标签必须使用**：始终为输入元素配对`<label>`标签以提高可访问性。
- **占位符不是标签**：占位符在输入时会消失，且不被所有屏幕阅读器识别。
- **客户端验证**：使用约束属性（`required`、`pattern`、`min`、`max`）进行浏览器验证，但始终也要进行服务器端验证。
- **默认类型**：如果未指定`type`，则默认为`text`。
- **表单关联**：使用`name`属性进行表单提交；没有`name`属性的输入不会被提交。
- **CSS伪类**：使用`invalid`、`valid`、`checked`、`disabled`、`placeholder-shown`等进行样式控制。

### 示例

```html
<!-- 基本按钮 -->
<button type="button">点击我</button>

<!-- 表单提交按钮 -->
<form>
  <input type="text" name="username" />
  <button type="submit">提交</button>
</form>

<!-- 自定义样式按钮 -->
<button class="favorite" type="button">加入收藏</button>

<style>
  .favorite {
    padding: 10px 20px;
    background-color: 番茄红;
    color: 白色;
    border: none;
    border-radius: 5px;
    cursor: 指针;
  }

  .favorite:hover {
    background-color: 红色;
  }
</style>
```

---

## `<datalist>`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/datalist>

### 描述

`<datalist>`元素包含一组`<option>`元素，用于表示可在其他控件（如`<input>`）中选择的允许或推荐选项。它提供自动补全/建议功能，但不限制用户输入。

### 工作原理

`<datalist>`通过以下方式与`<input>`元素关联：

1. 给`<datalist>`分配一个唯一的`id`。
2. 在`<input>`上添加`list`属性，其值与`<datalist>`的`id`相同。

### 关键属性

| 属性 | 描述 |
|------|------|
| `value` | 建议值（必需） |
| `label` | 显示文本（可选） |

### 支持的输入类型

- 文本类：`text`、`search`、`url`、`tel`、`email`、`number`
- 日期/时间类：`month`、`week`、`date`、`time`、`datetime-local`
- 可视类：`range`、`color`

### 使用说明

- **不是`<select>`的替代**：用户仍可以输入列表中未包含的值。
- 提供建议，而非限制。
- 浏览器对下拉菜单的样式有限制。
- 某些屏幕阅读器可能不会宣布建议。

### 示例

```html
<!-- 简单的下拉列表 -->
<label for="ice-cream-choice">选择口味：</label>
<input list="ice-cream-flavors" id="ice-cream-choice" />

<datalist id="ice-cream-flavors">
  <option value="巧克力"></option>
  <option value="椰子"></option>
  <option value="薄荷"></option>
  <option value="草莓"></option>
  <option value="香草"></option>
</datalist>
```

---

## `<fieldset>`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/fieldset>

### 描述

`<fieldset>`元素用于在网页表单中将多个表单控件和标签分组。它提供语义化分组和相关表单字段的视觉组织。

### 关键细节

- **必须**是`<fieldset>`元素的第一个子元素。
- 为整个`<fieldset>`组提供可访问的标签。
- 仅支持全局属性（无特定元素属性）。
- 可包含短语内容和标题（`h1`--`h6`）。
- DOM接口：`HTMLFieldSetElement`。

### 示例

```html
<fieldset>
  <legend>选择你最喜欢的怪兽</legend>

  <input type="radio" id="kraken" name="monster" value="K" />
  <label for="kraken">巨蟹</label><br />

  <input type="radio" id="sasquatch" name="monster" value="S" />
  <label for="sasquatch">大脚怪</label>
</fieldset>
```

```css
legend {
  background-color: 黑色;
  color: 白色;
  padding: 3px 6px;
}
```

---

## `<meter>`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meter>

### 描述

`<meter>`元素表示一个已知范围内的标量值或分数值。常用于显示诸如燃油水平、温度、磁盘使用情况或评分等度量。

### 关键属性

| 属性 | 默认值 | 描述 |
|------|--------|------|
| `value` | `0` | 当前数值（必须介于`min`和`max`之间）。 |
| `min` | `0` | 测量范围的下限。 |
| `max` | `1` | 测量范围的上限。 |
| `low` | `min`值 | 范围的“低”端上限。 |
| `high` | `max`值 | 范围的“高”端下限。 |
| `optimum` | -- | 最优数值；表示首选范围部分。 |

### 使用说明

- 除非`value`在0到1之间，否则必须定义`min`和`max`以确保`value`在范围内。
- 浏览器会根据`value`是否低于`low`、介于`low`和`high`之间、高于`high`或与`optimum`相关而改变进度条颜色。
- 不能嵌套其他`<meter>`元素。
- 隐式ARIA角色：`meter`。

### 与`<progress>`的区别

- **`<meter>`**：显示一个范围内的标量测量（例如温度、磁盘使用情况）。
- **`<progress>`**：显示任务完成进度（从0到`max`）。

### 示例

```html
<!-- 简单的电池水平 -->
<p>电池水平： <meter min="0" max="100" value="75">75%</meter></p>

<!-- 带低/高范围 -->
<p>
  学生的考试成绩：
  <meter low="50" high="80" max="100" value="84">84%</meter>
</p>

<!-- 完整示例带最优值 -->
<label for="fuel">燃油水平：</label>
<meter id="fuel" min="0" max="100" low="33" high="66" optimum="80" value="50">
  在50/100
</meter>
```

---

## `<optgroup>`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/optgroup>

### 描述

`<optgroup>`元素在`<select>`元素中创建选项组，允许将相关选项组织成带标签的组。

### 关键属性

| 属性 | 描述 |
|------|------|
| `label` | 选项组的名称（必需）。浏览器在UI中显示为不可选的标签。 |
| `disabled` | 布尔属性。设置后，该组中的所有选项变为不可选并显示为灰色。 |

### 使用说明

- 必须是`<select>`元素的子元素。
- 包含一个或多个`<option>`元素。
- 不能嵌套在其他`<optgroup>`元素中。
- `label`属性是**必需的**。
- 隐式ARIA角色：`group`。

### 示例

```html
<label for="dino-select">选择恐龙：</label>
<select id="dino-select">
  <optgroup label="兽脚类">
    <option>Tyrannosaurus</option>
    <option>Velociraptor</option>
    <option>Deinonychus</option>
  </optgroup>
  <optgroup label="蜥脚类">
    <option>Diplodocus</option>
    <option>Saltasaurus</option>
    <option>Apatosaurus</option>
  </optgroup>
  <optgroup label="已灭绝群体" disabled>
    <option>Stegosaurus</option>
  </optgroup>
</select>
```

---

## `<option>`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/option>

### 描述

`<option>`元素定义包含在`<select>`、`<optgroup>`或`<datalist>`元素中的项目。它表示单个菜单项或可选选项。

### 关键属性

| 属性 | 描述 |
|------|------|
| `value` | 当选项被选中时提交给服务器的值。如果省略，则使用元素的文本内容。 |
| `selected` | 布尔属性，标记选项为初始选中状态。每个`<select>`（无`multiple`属性时）只能有一个`<option>`具有此属性。 |
| `disabled` | 布尔属性，禁用选项（灰色，不可交互）。如果其`<optgroup>`祖先被禁用，选项也会被禁用。 |
| `label` | 选项的文本标签。如果未定义，则使用元素的文本内容。 |

### 使用场景

- **在`<select>`中**：列出可选选项；用户选择一个（或多个，如果`<select>`设置了`multiple`属性）。
- **在`<optgroup>`中**：将相关选项分组。
- **在`<datalist>`中**：为`<input>`元素提供自动补全建议。

### 使用说明

- 如果紧接着另一个`<option>`或`<optgroup>`，可以省略结束标签。
- 隐式ARIA角色：`option`。

### 示例

```html
<label for="pet-select">选择宠物：</label>

<select name="pets" id="pet-select">
  <option value="">--请选择一个选项--</option>
  <option value="dog">狗</option>
  <option value="cat">猫</option>
  <option value="hamster" disabled>仓鼠</option>
  <option value="parrot" selected>鹦鹉</option>
</select>
```

---

## `<output>`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/output>

### 描述

`<output>`元素是一个容器元素，用于显示计算结果或用户操作结果。它与表单相关，并且大多数浏览器将其实现为ARIA实时区域，这意味着辅助技术会自动宣布更改。

### 关键属性

| 属性 | 描述 |
|------|------|
| `for` | 用于计算的元素`id`列表（以空格分隔）。 |
| `form` | 通过其`id`将输出与特定表单关联（覆盖祖先表单）。 |
| `name` | 元素的名称；用于`form.elements` API。 |

### 使用说明

- `<output>`的值、名称和内容**不会随表单提交**。
- 实现为`aria-live`区域；辅助技术会自动宣布更改。
- 必须同时包含开始和结束标签。

### 示例

```html
<form id="example-form">
  <input type="range" id="b" name="b" value="50" /> +
  <input type="number" id="a" name="a" value="10" /> =
  <output name="result" for="a b">60</output>
</form>

<script>
  const form = document.getElementById("example-form");
  form.addEventListener("input", () => {
    const result = form.elements["a"].valueAsNumber +
                   form.elements["b"].valueAsNumber;
    form.elements["result"].value = result;
  });
</script>
```

---

## `<progress>`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/progress>

### 描述

`<progress>`元素显示一个进度指示器，表示任务的完成情况，通常以进度条形式呈现。

### 关键属性

| 属性 | 描述 |
|------|------|
| `max` | 任务所需的总工作量。必须大于0且为有效浮点数。默认值：`1`。 |
| `value` | 已完成的工作量（0到`max`，或0到1如果`max`被省略）。如果省略，显示不确定的进度条。 |

### 与`<meter>`的区别

- 最小值始终为0（`<progress>`不允许`min`属性）。
- `<progress>`专门用于任务完成进度；`<meter>`用于标量测量。

### 使用说明

- 必须同时包含开始和结束标签。
- 隐式ARIA角色：`progressbar`。
- 标签之间的文本是旧版浏览器的备用内容（不是可访问标签）。
- 使用`:indeterminate`伪类来样式不确定的进度条。
- 移除`value`属性（`element.removeAttribute('value')`）以创建不确定的进度条。

### 可访问性考虑

- 始终使用`<label>`元素、`aria-labelledby`或`aria-label`提供可访问标签。
- 对于正在加载的页面部分：在更新的区域设置`aria-busy="true"`，使用`aria-describedby`链接到进度元素，并在加载完成后移除`aria-busy`。

### 示例

```html
<!-- 基本进度条 -->
<label for="file">文件进度：</label>
<progress id="file" max="100" value="70">70%</progress>

<!-- 可访问的隐式标签 -->
<label>
  正在上传文档： <progress value="70" max="100">70%</progress>
</label>

<!-- 不确定（无value属性） -->
<progress max="100"></progress>
```

---

## `<select>`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/select>

### 描述

`<select>`元素表示一个提供选项菜单的控件，允许用户从下拉列表中选择选项。

### 关键属性

| 属性 | 描述 |
|------|------|
| `name` | 指定控件的名称，用于表单提交。 |
| `multiple` | 布尔属性，允许选择多个选项。 |
| `size` | 可视滚动列表框中的可见行数（默认：`0`）。 |
| `required` | 布尔属性，要求选择非空选项。 |
| `disabled` | 布尔属性，阻止用户交互。 |
| `autofocus` | 布尔属性，页面加载时聚焦该控件。 |
| `form` | 通过ID将`<select>`与特定表单关联。 |
| `autocomplete` | 提供自动补全提示。 |

### 使用说明

- 每个选项通过嵌套的`<option>`元素定义。
- 使用`<optgroup>`对相关选项进行视觉分组。
- 使用`<hr>`元素创建选项之间的视觉分隔。
- `<option>`元素的`value`属性指定提交给服务器的数据。
- 如果选项没有`value`属性，则使用选项的文本内容。
- 若未设置`selected`属性，第一个选项默认被选中。
- 使用`multiple`属性时，多个选择会被提交为`name=value1&name=value2`。

### 可访问性考虑

- 使用`<label>`与`for`属性匹配`<select>`的`id`来关联标签。
- 隐式ARIA角色：`combobox`（单选）、`listbox`（多选或`size`大于1）。

### 示例

```html
<label for="pet-select">选择宠物：</label>

<select name="pets" id="pet-select">
  <option value="">--请选择一个选项--</option>
  <option value="dog">狗</option>
  <option value="cat">猫</option>
  <option value="hamster">仓鼠</option>
</select>
```

---

## `<textarea>`

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/textarea>

### 描述

`<textarea>`元素表示一个允许用户输入大量自由文本（如评论、反馈、评价）的多行纯文本编辑控件。

### 关键属性

| 属性 | 描述 |
|------|------|
| `rows` | 可见文本行数（默认：`2`）。 |
| `cols` | 可见宽度（以平均字符宽度为单位，默认：`20`）。 |
| `name` | 表单提交的控件名称。 |
| `id` | 用于与`<label>`元素关联。 |
| `placeholder` | 显示给用户的提示文本。 |
| `maxlength` | 最大字符串长度（以UTF-16代码单元为单位）。 |
| `minlength` | 最小字符串长度（以UTF-16代码单元为单位）。 |
| `wrap` | 换行行为：`soft`（默认）、`hard`或`off`。 |
| `disabled` | 布尔属性，禁用用户交互。 |
| `readonly` | 布尔属性，用户无法修改内容，但内容仍可聚焦和提交。 |
| `required` | 布尔属性，用户必须填写值。 |
| `autocomplete` | 浏览器自动补全提示：`on`或`off`。 |
| `spellcheck` | 拼写检查行为：`true`、`false`或`default`。 |
| `autofocus` | 布尔属性，页面加载时聚焦该控件。 |

### 使用说明

- 初始内容位于开始和结束标签之间（而非`value`属性）。
- 使用JavaScript的`.value`属性获取/设置内容；`.defaultValue`用于初始值。
- 默认可调整大小；使用CSS的`resize: none`禁用调整大小。
- 使用`:valid`和`:invalid`伪类根据`minlength`/`maxlength`/`required`约束进行样式控制。

### 示例

```html
<label for="story">告诉我们你的故事：</label>

<textarea
  id="story"
  name="story"
  rows="5"
  cols="33"
  placeholder="在此输入你的反馈..."
  maxlength="500"
  required>
它是一个黑暗而风雨交加的夜晚...
</textarea>
```

```css
textarea {
  padding: 10px;
  border: 1px solid #cccccc;
  border-radius: 5px;
  font-family: Arial, sans-serif;
  resize: vertical;
}

textarea:invalid {
  border-color: 红色;
}

textarea:valid {
  border-color: 绿色;
}
```

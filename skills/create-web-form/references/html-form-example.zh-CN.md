# HTML 表单示例参考

本参考文档整合了 W3Schools 关于 HTML 表单、表单元素、输入类型和相关属性的关键教学内容。

---

## HTML 表单

> **来源:** https://www.w3schools.com/html/html_forms.asp

### `<form>` 元素

`<form>` 元素用于创建 HTML 表单以供用户输入。它作为不同类型的输入元素（如文本框、复选框、单选按钮、提交按钮等）的容器。

```html
<form>
  <!-- 表单元素放在这里 -->
</form>
```

### `<input>` 元素

`<input>` 元素是使用最广泛的表单元素。它可以根据 `type` 属性以多种方式显示。

| 类型 | 描述 |
|------|-------------|
| `<input type="text">` | 显示一个单行文本输入框 |
| `<input type="radio">` | 显示一个单选按钮（用于从多个选项中选择一个） |
| `<input type="checkbox">` | 显示一个复选框（用于从多个选项中选择零个或多个） |
| `<input type="submit">` | 显示一个提交按钮（用于提交表单） |
| `<input type="button">` | 显示一个可点击的按钮 |

### 文本框

`<input type="text">` 定义了一个单行文本输入框。

```html
<form>
  <label for="fname">姓名：</label><br>
  <input type="text" id="fname" name="fname"><br>
  <label for="lname">姓氏：</label><br>
  <input type="text" id="lname" name="lname">
</form>
```

**注意：** 表单本身是不可见的。输入框的默认宽度为 20 个字符。

### `<label>` 元素

`<label>` 元素用于为多个表单元素定义标签。它对屏幕阅读器用户非常有用，因为当用户聚焦于输入元素时，屏幕阅读器会朗读标签内容。它也帮助那些难以点击小区域（如单选按钮或复选框）的用户，因为点击标签文本会切换关联的输入框焦点或选择状态。

`<label>` 标签的 `for` 属性应等于 `<input>` 元素的 `id` 属性，以将它们绑定在一起。

### 单选按钮

`<input type="radio">` 定义了一个单选按钮。单选按钮允许用户从有限的选项中选择一个。

```html
<form>
  <p>请选择您最喜欢的网页语言：</p>
  <input type="radio" id="html" name="fav_language" value="HTML">
  <label for="html">HTML</label><br>
  <input type="radio" id="css" name="fav_language" value="CSS">
  <label for="css">CSS</label><br>
  <input type="radio" id="javascript" name="fav_language" value="JavaScript">
  <label for="javascript">JavaScript</label>
</form>
```

### 复选框

`<input type="checkbox">` 定义了一个复选框。复选框允许用户选择零个或多个选项。

```html
<form>
  <input type="checkbox" id="vehicle1" name="vehicle1" value="Bike">
  <label for="vehicle1">我有一辆自行车</label><br>
  <input type="checkbox" id="vehicle2" name="vehicle2" value="Car">
  <label for="vehicle2">我有一辆汽车</label><br>
  <input type="checkbox" id="vehicle3" name="vehicle3" value="Boat">
  <label for="vehicle3">我有一艘船</label>
</form>
```

### 提交按钮

`<input type="submit">` 定义了一个提交按钮，用于将表单数据提交给表单处理程序。表单处理程序通常是服务器上的一个文件，通过表单的 `action` 属性指定。

```html
<form action="/action_page.php">
  <label for="fname">姓名：</label><br>
  <input type="text" id="fname" name="fname" value="John"><br>
  <label for="lname">姓氏：</label><br>
  <input type="text" id="lname" name="lname" value="Doe"><br><br>
  <input type="submit" value="提交">
</form>
```

如果您省略了提交按钮的 `value` 属性，按钮将使用默认文本。

### `<input>` 元素的 `name` 属性

每个输入字段都必须有 `name` 属性才能被提交。如果省略了 `name` 属性，输入字段的值将不会被发送。

---

## HTML 表单属性

> **来源:** https://www.w3schools.com/html/html_forms_attributes.asp

### `action` 属性

`action` 属性定义了表单提交时要执行的操作。通常，当用户点击提交按钮时，表单数据会发送到服务器上的一个文件。

```html
<form action="/action_page.php">
  <label for="fname">姓名：</label><br>
  <input type="text" id="fname" name="fname" value="John"><br>
  <label for="lname">姓氏：</label><br>
  <input type="text" id="lname" name="lname" value="Doe"><br><br>
  <input type="submit" value="提交">
</form>
```

**提示：** 如果省略了 `action` 属性，操作将设置为当前页面。

### `target` 属性

`target` 属性指定表单提交后的响应显示位置。

| 值 | 描述 |
|-------|-------------|
| `_blank` | 响应显示在新窗口或标签页中 |
| `_self` | 响应显示在当前窗口中（默认） |
| `_parent` | 响应显示在父框架中 |
| `_top` | 响应显示在窗口的整个内容区域中 |
| `framename` | 响应显示在指定名称的 iframe 中 |

```html
<form action="/action_page.php" target="_blank">
```

### `method` 属性

`method` 属性指定提交表单数据时使用的 HTTP 方法。表单数据可以以 URL 参数形式发送（使用 `method="get"`）或通过 HTTP POST 事务发送（使用 `method="post"`）。

```html
<!-- 使用 GET -->
<form action="/action_page.php" method="get">

<!-- 使用 POST -->
<form action="/action_page.php" method="post">
```

**何时使用 GET：**

- 如果未指定，默认方法
- 表单数据以名称/值对附加到 URL
- URL 的长度有限制（大约 2048 个字符）
- 不要使用 GET 提交敏感数据（它会显示在 URL 中）
- 适用于用户希望书签结果的表单提交

**何时使用 POST：**

- 表单数据附加在 HTTP 请求体中（数据不会显示在 URL 中）
- POST 没有大小限制
- 使用 POST 提交的表单无法被书签
- 提交敏感或个人信息时始终使用 POST

### `autocomplete` 属性

`autocomplete` 属性指定表单或输入字段是否启用自动补全功能。当启用时，浏览器会根据用户之前输入的值自动补全。

```html
<form action="/action_page.php" autocomplete="on">
```

### `novalidate` 属性

`novalidate` 属性是一个布尔属性。当存在时，它指定在提交表单时不应进行验证。

```html
<form action="/action_page.php" novalidate>
```

### `enctype` 属性

`enctype` 属性指定提交表单数据时如何编码。此属性只能与 `method="post"` 一起使用。

| 值 | 描述 |
|-------|-------------|
| `application/x-www-form-urlencoded` | 默认。提交前对所有字符进行编码 |
| `multipart/form-data` | 当表单包含文件上传控件（`<input type="file">`）时必需 |
| `text/plain` | 不对数据进行编码（不推荐） |

```html
<form action="/action_page.php" method="post" enctype="multipart/form-data">
```

### `name` 属性

`name` 属性指定表单的名称。它用于 JavaScript 引用元素，或在提交后引用表单数据。只有具有 `name` 属性的表单才会在提交时传递其值。

### `accept-charset` 属性

`accept-charset` 属性指定表单提交时使用的字符编码。默认值为 `"unknown"`，表示与文档相同的编码。

### 所有 `<form>` 属性汇总

| 属性 | 描述 |
|-----------|-------------|
| `accept-charset` | 指定表单提交的字符编码 |
| `action` | 指定提交表单时数据发送的位置 |
| `autocomplete` | 指定表单或输入字段是否启用自动补全 |
| `enctype` | 指定提交表单数据时的编码方式（适用于 `method="post"`） |
| `method` | 指定提交表单数据时使用的 HTTP 方法 |
| `name` | 指定表单的名称 |
| `novalidate` | 指定表单提交时不进行验证 |
| `rel` | 指定链接资源与当前文档的关系 |
| `target` | 指定表单提交后响应的显示位置 |

---

## HTML 表单元素

> **来源:** https://www.w3schools.com/html/html_form_elements.asp

### `<input>` 元素

最重要的表单元素。根据 `type` 属性的不同，可以以多种方式显示。如果省略 `type`，输入框将使用默认类型 `text`。

```html
<form>
  <label for="fname">姓名：</label><br>
  <input type="text" id="fname" name="fname" value="John"><br>
  <label for="lname">姓氏：</label><br>
  <input type="text" id="lname" name="lname" value="Doe">
</form>
```

### `<label>` 元素

为多个表单元素定义标签。它对屏幕阅读器用户非常有用，因为当用户聚焦于输入元素时，屏幕阅读器会朗读标签内容。它也帮助那些难以点击小区域（如单选按钮或复选框）的用户，因为点击标签文本会切换关联的输入框焦点或选择状态。

### 下拉列表

`<select>` 元素定义了一个下拉列表。

```html
<label for="cars">请选择一辆车：</label>
<select id="cars" name="cars">
  <option value="volvo">沃尔沃</option>
  <option value="saab">萨博</option>
  <option value="fiat" selected>菲亚特</option>
  <option value="audi">奥迪</option>
</select>
```

- `<option>` 元素定义了可选的选项。
- 默认情况下，下拉列表中的第一个选项被选中。
- `selected` 属性用于预选一个选项。
- 使用 `size` 属性指定可见选项的数量。
- 使用 `multiple` 属性允许用户选择多个选项。

```html
<!-- 显示多个可见选项 -->
<select id="cars" name="cars" size="3">

<!-- 允许选择多个选项 -->
<select id="cars" name="cars" size="4" multiple>
```

### `<textarea>` 元素

`<textarea>` 元素定义了一个多行文本输入框（文本区域）。

```html
<textarea name="message" rows="10" cols="30">
猫咪在花园里玩耍。
</textarea>
```

- `rows` 属性指定文本区域中可见的行数。
- `cols` 属性指定文本区域的可见宽度。
- 您也可以使用 CSS 的 `height` 和 `width` 属性定义大小。

```css
textarea {
  width: 100%;
  height: 200px;
}
```

### `<button>` 元素

`<button>` 元素定义了一个可点击的按钮。

```html
<button type="button" onclick="alert('Hello World!')">点击我！</button>
```

**注意：** 对于 `<button>` 元素，始终指定 `type` 属性。不同浏览器可能使用不同的默认类型。

### `<fieldset>` 和 `<legend>` 元素

`<fieldset>` 元素用于在表单中分组相关数据。`<legend>` 元素为 `<fieldset>` 元素定义一个标题。

```html
<form action="/action_page.php">
  <fieldset>
    <legend>个人信息：</legend>
    <label for="fname">姓名：</label><br>
    <input type="text" id="fname" name="fname" value="John"><br>
    <label for="lname">姓氏：</label><br>
    <input type="text" id="lname" name="lname" value="Doe"><br><br>
    <input type="submit" value="提交">
  </fieldset>
</form>
```

### `<datalist>` 元素

`<datalist>` 元素为 `<input>` 元素指定一组预定义的选项。用户在输入数据时会看到这些预定义选项的下拉列表。`<input>` 元素的 `list` 属性必须与 `<datalist>` 元素的 `id` 属性相匹配。

```html
<input list="browsers">
<datalist id="browsers">
  <option value="Edge">
  <option value="Firefox">
  <option value="Chrome">
  <option value="Opera">
  <option value="Safari">
</datalist>
```

### `<output>` 元素

`<output>` 元素表示一个计算结果（通常通过 JavaScript 实现）。

```html
<form action="/action_page.php"
  oninput="x.value=parseInt(a.value)+parseInt(b.value)">
  0
  <input type="range" id="vol" name="vol" min="0" max="100">
  <label for="vol">音量（0 到 100）：</label>
  <input type="number" id="vol" name="vol" min="0" max="100">
  <output name="x" for="vol"></output>
  <br><br>
  <input type="submit">
</form>
```

### `<optgroup>` 元素

`<optgroup>` 元素用于在 `<select>` 元素（下拉列表）中分组相关选项。

```html
<label for="cars">请选择一辆车：</label>
<select name="cars" id="cars">
  <optgroup label="瑞典汽车">
    <option value="volvo">沃尔沃</option>
    <option value="saab">萨博</option>
  </optgroup>
  <optgroup label="德国汽车">
    <option value="mercedes">梅赛德斯</option>
    <option value="audi">奥迪</option>
  </optgroup>
</select>
```

### 表单元素汇总

| 元素 | 描述 |
|---------|-------------|
| `<form>` | 定义一个用于用户输入的 HTML 表单 |
| `<input>` | 定义一个输入控件 |
| `<textarea>` | 定义一个多行输入控件（文本区域） |
| `<label>` | 定义一个 `<input>` 元素的标签 |
| `<fieldset>` | 在表单中分组相关元素 |
| `<legend>` | 定义一个 `<fieldset>` 元素的标题 |
| `<select>` | 定义一个下拉列表 |
| `<optgroup>` | 定义一个下拉列表中的相关选项组 |
| `<option>` | 定义一个下拉列表中的选项 |
| `<button>` | 定义一个可点击的按钮 |
| `<datalist>` | 为输入控件指定一组预定义选项 |
| `<output>` | 定义一个计算结果 |

---

## HTML 表单输入类型

> **来源:** https://www.w3schools.com/html/html_form_input_types.asp

### 输入类型：text

`<input type="text">` 定义了一个单行文本输入框。

```html
<form>
  <label for="fname">姓名：</label><br>
  <input type="text" id="fname" name="fname"><br>
  <label for="lname">姓氏：</label><br>
  <input type="text" id="lname" name="lname">
</form>
```

### 输入类型：password

`<input type="password">` 定义了一个密码字段。字符会被遮蔽显示（如星号或圆圈）。

```html
<form>
  <label for="username">用户名：</label><br>
  <input type="text" id="username" name="username"><br>
  <label for="pwd">密码：</label><br>
  <input type="password" id="pwd" name="pwd">
</form>
```

### 输入类型：submit

`<input type="submit">` 定义了一个提交按钮，用于将表单数据提交给表单处理程序。表单处理程序通常是通过表单的 `action` 属性指定的服务器页面。

```html
<form action="/action_page.php">
  <label for="fname">姓名：</label>
  <input type="text" id="fname" name="fname"><br><br>
  <input type="submit" value="提交">
</form>
```

### 输入类型：reset

`<input type="reset">` 定义了一个重置按钮，用于将表单的所有值重置为默认值。

```html
<form action="/action_page.php">
  <label for="fname">姓名：</label>
  <input type="text" id="fname" name="fname"><br><br>
  <input type="submit" value="提交">
  <input type="reset" value="重置">
</form>
```

### 输入类型：radio

`<input type="radio">` 定义了一个单选按钮。单选按钮允许用户从有限的选项中选择一个。

```html
<form>
  <input type="radio" id="html" name="fav_language" value="HTML">
  <label for="html">HTML</label><br>
  <input type="radio" id="css" name="fav_language" value="CSS">
  <label for="css">CSS</label><br>
  <input type="radio" id="javascript" name="fav_language" value="JavaScript">
  <label for="javascript">JavaScript</label>
</form>
```

### 输入类型：checkbox

`<input type="checkbox">` 定义了一个复选框。复选框允许用户选择零个或多个选项。

```html
<form>
  <input type="checkbox" id="vehicle1" name="vehicle1" value="Bike">
  <label for="vehicle1">我有一辆自行车</label><br>
  <input type="checkbox" id="vehicle2" name="vehicle2" value="Car">
  <label for="vehicle2">我有一辆汽车</label><br>
  <input type="checkbox" id="vehicle3" name="vehicle3" value="Boat">
  <label for="vehicle3">我有一艘船</label>
</form>
```

### 输入类型：button

`<input type="button">` 定义了一个按钮。

```html
<input type="button" onclick="alert('Hello World!')" value="点击我！">
```

**注意：** 对于 `<button>` 元素，始终指定 `type` 属性。不同浏览器可能使用不同的默认类型。

### 输入类型：color

`<input type="color">` 用于包含颜色值的输入字段。根据浏览器支持情况，可能会显示颜色选择器。

```html
<form>
  <label for="favcolor">请选择您最喜欢的颜色：</label>
  <input type="color" id="favcolor" name="favcolor" value="#ff0000">
</form>
```

### 输入类型：date

`<input type="date">` 用于包含日期的输入字段。根据浏览器支持情况，可能会显示日期选择器。

```html
<form>
  <label for="birthday">生日：</label>
  <input type="date" id="birthday" name="birthday">
</form>
```

您可以使用 `min` 和 `max` 属性来添加限制：

```html
<input type="date" id="datemin" name="datemin" min="2000-01-02">
<input type="date" id="datemax" name="datemax" max="1979-12-31">
<input type="number" id="quantity" name="quantity" min="1" max="5">
```

### 输入类型：datetime-local

`<input type="datetime-local">` 指定一个日期和时间输入字段，不包含时区信息。

```html
<form>
  <label for="birthdaytime">生日（日期和时间）：</label>
  <input type="datetime-local" id="birthdaytime" name="birthdaytime">
</form>
```

### 输入类型：email

`<input type="email">` 用于包含电子邮件地址的输入字段。根据浏览器支持情况，电子邮件地址可以自动验证。一些智能手机识别电子邮件类型并在键盘上添加 `.com`。

```html
<form>
  <label for="email">请输入您的电子邮件：</label>
  <input type="email" id="email" name="email">
</form>
```

### 输入类型：file

`<input type="file">` 定义了一个文件选择字段和一个“浏览”按钮用于文件上传。

```html
<form>
  <label for="myfile">选择一个文件：</label>
  <input type="file" id="myfile" name="myfile">
</form>
```

### 输入类型：hidden

`<input type="hidden">` 定义了一个隐藏的输入字段（对用户不可见）。隐藏字段允许网页开发者在表单提交时包含用户无法看到或修改的数据。

```html
<form>
  <label for="fname">姓名：</label>
  <input type="text" id="fname" name="fname"><br><br>
  <input type="hidden" id="custId" name="custId" value="3487">
  <input type="submit" value="提交">
</form>
```

### 输入类型：image

`<input type="image">` 用图像作为提交按钮。图像路径由 `src` 属性指定。

```html
<form>
  <input type="image" src="img_submit.gif" alt="提交" width="48" height="48">
</form>
```

### 输入类型：month

`<input type="month">` 允许用户选择月份和年份。

```html
<form>
  <label for="bdaymonth">生日（月份和年份）：</label>
  <input type="month" id="bdaymonth" name="bdaymonth">
</form>
```

### 输入类型：number

`<input type="number">` 定义了一个数字输入字段。您可以设置接受的数字范围。

```html
<form>
  <label for="quantity">数量（1 到 5 之间）：</label>
  <input type="number" id="quantity" name="quantity" min="1" max="5">
</form>
```

**输入限制：**

| 属性 | 描述 |
|-----------|-------------|
| `disabled` | 指定输入字段应被禁用 |
| `max` | 指定输入字段的最大值 |
| `maxlength` | 指定输入字段的最大字符数 |
| `min` | 指定输入字段的最小值 |
| `pattern` | 指定一个正则表达式以检查输入值 |
| `readonly` | 指定输入字段为只读（不可修改） |
| `required` | 指定输入字段为必填项（必须填写） |
| `step` | 指定输入字段的合法数字间隔 |
| `autofocus` | 指定输入字段在页面加载时自动获得焦点 |
| `height` | 指定 `<input type="image">` 的高度 |
| `width` | 指定 `<input type="image">` 的宽度 |
| `list` | 引用一个包含预定义选项的 `<datalist>` 元素 |
| `autocomplete` | 指定自动补全功能是否开启或关闭 |

### 输入属性汇总

| 属性 | 描述 |
|-----------|-------------|
| `value` | 指定输入元素的默认值 |
| `readonly` | 指定输入字段为只读 |
| `disabled` | 指定输入字段为禁用 |
| `size` | 指定输入字段的可见宽度（以字符为单位） |
| `maxlength` | 指定输入字段的最大字符数 |
| `min` | 指定输入字段的最小值 |
| `max` | 指定输入字段的最大值 |
| `multiple` | 指定用户可以输入多个值 |
| `pattern` | 指定一个正则表达式以检查值 |
| `placeholder` | 指定一个简短提示，描述预期的值 |
| `required` | 指定输入字段为必填项 |
| `step` | 指定合法的数字间隔 |
| `autofocus` | 指定输入字段在页面加载时自动获得焦点 |
| `height` | 指定 `<input type="image">` 的高度 |
| `width` | 指定 `<input type="image">` 的宽度 |
| `list` | 引用一个包含预定义选项的 `<datalist>` 元素 |
| `autocomplete` | 指定自动补全功能是否开启或关闭 |

---

## HTML 输入表单* 属性

> **来源:** https://www.w3schools.com/html/html_form_attributes_form.asp

### `form` 属性

输入 `form` 属性指定 `<input>` 元素所属的表单。此属性的值必须等于其所属的 `<form>` 元素的 `id` 属性。这允许将输入字段放置在表单外部但仍将其关联到表单。

```html
<form action="/action_page.php" id="form1">
  <label for="fname">姓名：</label>
  <input type="text" id="fname" name="fname"><br><br>
  <input type="submit" value="提交">
</form>

<!-- 此输入字段位于表单外部但仍属于它 -->
<label for="lname">姓氏：</label>
<input type="text" id="lname" name="lname" form="form1">
```

### `formaction` 属性

输入 `formaction` 属性指定表单提交时处理输入的文件 URL。此属性覆盖 `<form>` 元素的 `action` 属性。适用于提交和图像输入类型。

```html
<form action="/action_page.php">
  <label for="fname">姓名：</label>
  <input type="text" id="fname" name="fname"><br><br>
  <input type="submit" value="使用 GET 提交">
  <input type="submit" formaction="/action_page2.php" value="使用 POST 提交">
</form>
```

### `formenctype` 属性

输入 `formenctype` 属性指定提交表单数据时的编码方式（仅适用于 `method="post"` 的表单）。此属性覆盖 `<form>` 元素的 `enctype` 属性。适用于提交和图像输入类型。

```html
<form action="/action_page_binary.asp" method="post">
  <label for="fname">姓名：</label>
  <input type="text" id="fname" name="fname"><br><br>
  <input type="submit" value="提交">
  <input type="submit" formenctype="multipart/form-data"
    value="以 multipart/form-data 提交">
</form>
```

### `formmethod` 属性

输入 `formmethod` 属性定义发送数据到操作 URL 时使用的 HTTP 方法。此属性覆盖 `<form>` 元素的 `method` 属性。适用于提交和图像输入类型。

```html
<form action="/action_page.php" method="get">
  <label for="fname">姓名：</label>
  <input type="text" id="fname" name="fname"><br><br>
  <label for="lname">姓氏：</label>
  <input type="text" id="lname" name="lname"><br><br>
  <input type="submit" value="使用 GET 提交">
  <input type="submit" formmethod="post" value="使用 POST 提交">
</form>
```

### `formtarget` 属性

输入 `formtarget` 属性指定表单提交后响应的显示位置。此属性覆盖 `<form>` 元素的 `target` 属性。适用于提交和图像输入类型。

```html
<form action="/action_page.php">
  <label for="fname">姓名：</label>
  <input type="text" id="fname" name="fname"><br><br>
  <label for="lname">姓氏：</label>
  <input type="text" id="lname" name="lname"><br><br>
  <input type="submit" value="提交">
  <input type="submit" formtarget="_blank" value="在新窗口/标签页中提交">
</form>
```

### `formnovalidate` 属性

输入 `formnovalidate` 属性指定 `<input>` 元素在提交时不进行验证。此属性覆盖 `<form>` 元素的 `novalidate` 属性。适用于提交输入类型。

```html
<form action="/action_page.php">
  <label for="email">请输入您的电子邮件：</label>
  <input type="email" id="email" name="email"><br><br>
  <input type="submit" value="提交">
  <input type="submit" formnovalidate="formnovalidate"
    value="不进行验证提交">
</form>
```

### `novalidate` 属性

`novalidate` 属性是 `<form>` 的属性。当存在时，它指定在提交时表单数据不应被验证。

```html
<form action="/action_page.php" novalidate>
  <label for="email">请输入您的电子邮件：</label>
  <input type="email" id="email" name="email"><br><br>
  <input type="submit" value="提交">
</form>
```

### 表单* 属性汇总

| 属性 | 描述 |
|-----------|-------------|
| `form` | 指定输入元素所属的表单 |
| `formaction` | 指定表单提交的 URL（覆盖表单的 `action`） |
| `formenctype` | 指定表单数据的编码方式（覆盖表单的 `enctype`） |
| `formmethod` | 指定发送数据的 HTTP 方法（覆盖表单的 `method`） |
| `formnovalidate` | 指定输入不应被验证（覆盖表单的 `novalidate`） |
| `formtarget` | 指定响应的显示位置（覆盖表单的 `target`） |

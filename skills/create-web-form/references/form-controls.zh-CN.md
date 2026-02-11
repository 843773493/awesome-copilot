# 表单控件参考指南

涵盖 HTML 表单结构、原生表单控件、HTML5 输入类型和其他表单元素的综合参考指南。内容来源于 Mozilla 开发者网络（MDN）Web 文档。

---

## 目录

1. [如何构建网页表单](#如何构建网页表单)
2. [基本原生表单控件](#基本原生表单控件)
3. [HTML5 输入类型](#html5-输入类型)
4. [其他表单控件](#其他表单控件)

---

## 如何构建网页表单

> **来源:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/How_to_structure_a_web_form

### `<form>` 元素

`<form>` 元素正式定义了表单并决定了其行为。它必须包裹所有表单内容。

**重要提示:** 不要将表单嵌套在另一个表单中——这会导致不可预测的行为。

```html
<form>
  <!-- 表单内容 -->
</form>
```

表单控件可以使用 `form` 属性与特定表单（通过其 ID）关联，即使它们位于表单外部。

### 分组和语义结构

#### `<fieldset>` 和 `<legend>` 元素

`<fieldset>` 将具有相同用途的控件分组，提高可用性和可访问性。`<legend>` 为 `fieldset` 提供描述性标签。

**关键优势：**
- 屏幕阅读器（如 JAWS 和 NVDA）在每个控件之前朗读 `<legend>` 内容
- 对于分组单选按钮和复选框是必需的
- 对于跨多页的长表单很有用

```html
<form>
  <fieldset>
    <legend>果汁大小</legend>
    <p>
      <input type="radio" name="size" id="size_1" value="small" />
      <label for="size_1">小</label>
    </p>
    <p>
      <input type="radio" name="size" id="size_2" value="medium" />
      <label for="size_2">中</label>
    </p>
    <p>
      <input type="radio" name="size" id="size_3" value="large" />
      <label for="size_3">大</label>
    </p>
  </fieldset>
</form>
```

**结果:** 屏幕阅读器会宣布：“果汁大小 小”，“果汁大小 中”，“果汁大小 大”

### 标签：可访问性的基础

#### `<label>` 元素

`<label>` 元素正式将文本与表单控件关联。`for` 属性通过输入的 `id` 将标签与输入连接。

```html
<label for="name">姓名：</label>
<input type="text" id="name" name="username" />
```

**隐式关联：** 将控件嵌套在标签内（尽管显式的 `for` 属性仍然是最佳实践）：

```html
<label for="name">
  姓名：<input type="text" id="name" name="username" />
</label>
```

**可访问性影响：**
- 屏幕阅读器会宣布：“姓名，编辑文本”
- 没有适当标签时：仅显示“编辑文本 空”（无帮助）

#### 标签可点击

点击或轻触标签会激活其关联的控件——尤其对小点击区域的复选框和单选按钮很有用。

```html
<form>
  <p>
    <input type="checkbox" id="taste_1" name="taste_cherry" value="cherry" />
    <label for="taste_1">我喜欢樱桃</label>
  </p>
</form>
```

#### 多个标签（最佳实践）

避免在单个控件上使用多个标签。相反，将所有文本包含在一个标签中：

```html
<!-- 不推荐 -->
<label for="username">姓名：</label>
<input id="username" type="text" name="username" required />

<!-- 更好 -->
<label for="username">
  <span>姓名：</span>
  <input id="username" type="text" name="username" required />
  <span>*</span>
</label>

<!-- 最佳 -->
<label for="username">姓名 *：</label>
<input id="username" type="text" name="username" required />
```

### 常见 HTML 表单结构

使用这些语义 HTML 元素来构建表单：

- `<ul>` / `<ol>` 与 `<li>`：推荐用于分组复选框或单选按钮
- `<p>`：包裹标签-控件对
- `<div>`：通用分组
- `<section>`：分组相关表单部分
- `<h1>`、`<h2>`：将复杂表单分组成多个部分

### 完整支付表单示例

```html
<form>
  <h1>支付表单</h1>
  <p>请填写所有必填字段（*）。</p>

  <!-- 联系信息部分 -->
  <section>
    <h2>联系信息</h2>

    <fieldset>
      <legend>选择您喜欢的蔬菜</legend>
      <ul>
        <li>
          <label for="carrots">胡萝卜</label>
          <input
            type="checkbox"
            id="carrots"
            name="vegetable"
            value="carrots"
            checked />
        </li>
        <li>
          <label for="peas">豌豆</label>
          <input type="checkbox" id="peas" name="vegetable" value="peas" />
        </li>
        <li>
          <label for="cabbage">卷心菜</label>
          <input type="checkbox" id="cabbage" name="vegetable" value="cabbage" />
        </li>
      </ul>
    </fieldset>

    <p>
      <label for="name">姓名 *：</label>
      <input type="text" id="name" name="username" required />
    </p>

    <p>
      <label for="mail">电子邮件 *：</label>
      <input type="email" id="mail" name="user-mail" required />
    </p>

    <p>
      <label for="pwd">密码 *：</label>
      <input type="password" id="pwd" name="password" required />
    </p>
  </section>

  <!-- 支付信息部分 -->
  <section>
    <h2>支付信息</h2>

    <p>
      <label for="card">卡类型：</label>
      <select id="card" name="user-card">
        <option value="visa">Visa</option>
        <option value="mc">Mastercard</option>
        <option value="amex">American Express</option>
      </select>
    </p>

    <p>
      <label for="number">卡号 *：</label>
      <input type="tel" id="number" name="card-number" required />
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

### 表单结构最佳实践

| 实践 | 优势 |
|------|------|
| 始终使用 `<form>` 包裹 | 被辅助技术及浏览器插件识别 |
| 用 `<fieldset>` 和 `<legend>` 包裹相关控件 | 提高可用性和可访问性 |
| 始终使用 `for` 属性关联标签 | 屏幕阅读器会朗读标签与控件 |
| 使用语义 HTML（`<section>`、`<h2>` 等） | 更好的表单结构和可访问性 |
| 将单选按钮/复选框分组在列表中 | 更清晰的视觉和语义组织 |
| 明确标识必填字段 | 用户和辅助技术知道哪些字段是必须的 |
| 使用屏幕阅读器测试 | 验证表单是否真正可访问 |

---

## 基本原生表单控件

> **来源:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Basic_native_form_controls

### 文本输入字段

#### 单行文本字段

通过 `<input type="text">` 创建，或省略 type 属性（text 是默认值）。

```html
<input type="text" id="comment" name="comment" value="我是一个文本字段" />
```

**常见文本字段行为：**
- 可标记为 `readonly`（显示值但不可修改，仍会随表单提交）
- 可使用 `placeholder` 属性提供简要描述
- 可通过 `size`（物理框大小）和 `maxlength`（字符限制）进行约束
- 支持 `spellcheck` 属性
- 在发送到服务器前会自动删除换行符

#### 密码字段

通过将输入字符隐藏（显示为点或星号）来提高安全性。

```html
<input type="password" id="pwd" name="pwd" />
```

**安全提示：** 这仅隐藏文本的视觉效果。始终使用 HTTPS 来安全传输表单数据，以防止数据被截获。

#### 隐藏内容

不可见的表单控件，随表单数据发送（例如时间戳、跟踪信息）。

```html
<input type="hidden" id="timestamp" name="timestamp" value="1286705410" />
```

- 不可见于用户
- 无法获得焦点
- 用户无法手动编辑
- 屏幕阅读器不会注意到它
- 必须具有 `name` 和 `value` 属性

### 可选项：复选框和单选按钮

#### 复选框

允许进行多选。每个复选框可以独立勾选或取消勾选。

```html
<fieldset>
  <legend>选择您喜欢的蔬菜</legend>
  <ul>
    <li>
      <label for="carrots">胡萝卜</label>
      <input
        type="checkbox"
        id="carrots"
        name="vegetable"
        value="carrots"
        checked />
    </li>
    <li>
      <label for="peas">豌豆</label>
      <input type="checkbox" id="peas" name="vegetable" value="peas" />
    </li>
    <li>
      <label for="cabbage">卷心菜</label>
      <input type="checkbox" id="cabbage" name="vegetable" value="cabbage" />
    </li>
  </ul>
</fieldset>
```

**属性：**
- 相关复选框使用相同的 `name` 属性
- 使用 `checked` 属性预选
- 仅勾选的复选框值会随表单提交

#### 单选按钮

每组只能选择一个选项。通过相同的 `name` 属性关联。

```html
<fieldset>
  <legend>您最喜欢的餐食是什么？</legend>
  <ul>
    <li>
      <label for="soup">汤</label>
      <input type="radio" id="soup" name="meal" value="soup" checked />
    </li>
    <li>
      <label for="curry">咖喱</label>
      <input type="radio" id="curry" name="meal" value="curry" />
    </li>
    <li>
      <label for="pizza">披萨</label>
      <input type="radio" id="pizza" name="meal" value="pizza" />
    </li>
  </ul>
</fieldset>
```

**属性：**
- 同一组的按钮共享 `name` 属性
- 勾选一个按钮会自动取消勾选其他按钮
- 仅勾选的值会随表单提交
- 无法取消所有选项，除非重置表单

**可访问性最佳实践：** 将相关控件包裹在 `<fieldset>` 中，并使用 `<legend>` 描述该组，每个 `<label>`/`<input>` 对应在一起。

### 按钮

#### 提交按钮

将表单数据发送到服务器。

```html
<!-- 使用 <input> -->
<input type="submit" value="提交此表单" />

<!-- 使用 <button> -->
<button type="submit">提交此表单</button>
```

#### 重置按钮

将所有表单控件重置为默认值。

```html
<!-- 使用 <input> -->
<input type="reset" value="重置此表单" />

<!-- 使用 <button> -->
<button type="reset">重置此表单</button>
```

#### 无功能按钮

无自动效果，需通过 JavaScript 自定义。

```html
<!-- 使用 <input> -->
<input type="button" value="没有 JavaScript 时什么也不做" />

<!-- 使用 <button> -->
<button type="button">没有 JavaScript 时什么也不做</button>
```

**`<button>` 元素的优势：** 更容易样式化，支持标签内的 HTML 内容。

### 图像按钮

以图像形式显示，但行为如同提交按钮。提交点击的 X 和 Y 坐标。

```html
<input type="image" alt="点击我！" src="my-img.png" width="80" height="30" />
```

**坐标提交：**
- X 坐标键：`[name].x`
- Y 坐标键：`[name].y`

**使用 GET 方法的示例 URL：**
```
https://example.com?pos.x=123&pos.y=456
```

### 文件选择器

允许用户选择一个或多个文件发送到服务器。

```html
<!-- 单个文件 -->
<input type="file" name="file" id="file" accept="image/*" />

<!-- 多个文件 -->
<input type="file" name="file" id="file" accept="image/*" multiple />
```

**移动设备直接捕获：** 访问设备的相机、麦克风或存储：

```html
<input type="file" accept="image/*;capture=camera" />
<input type="file" accept="video/*;capture=camcorder" />
<input type="file" accept="audio/*;capture=microphone" />
```

**属性：**
- `accept`：限制文件类型（如 `image/*`、`.pdf`）
- `multiple`：允许选择多个文件

### 所有表单控件的通用属性

| 属性 | 默认值 | 描述 |
|------|--------|------|
| `autofocus` | false | 页面加载时自动获得焦点（每个文档仅一个） |
| `disabled` | false | 用户无法交互；如果适用，继承自包含的 `<fieldset>` |
| `form` | -- | 通过 ID 将控件与 `<form>` 元素关联（允许控件位于表单外部） |
| `name` | -- | 控件名称；随表单数据提交 |
| `value` | -- | 元素的初始值 |

### 表单数据提交行为

**可选项特殊处理：**
- 仅在勾选时发送值
- 未勾选的选项：不发送任何内容（甚至不发送名称）
- 勾选但没有 `value` 属性：发送名称与值 `"on"`

```html
<input type="checkbox" name="subscribe" value="yes" />
```
- 勾选时：`subscribe=yes`
- 未勾选时：不发送任何内容

---

## HTML5 输入类型

> **来源:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/HTML5_input_types

HTML5 引入了新的 `<input type>` 值，以创建具有内置验证和跨设备改进用户体验的原生表单控件。

### 电子邮件字段 (`type="email"`)

```html
<label for="email">请输入您的电子邮件地址：</label>
<input type="email" id="email" name="email" />
```

**关键特性：**
- **验证**：浏览器在提交前验证电子邮件格式
- **多个电子邮件**：使用 `multiple` 属性进行逗号分隔的地址
- **移动键盘**：在触摸设备上默认显示 `@` 符号
- **无效状态**：匹配 `:invalid` 伪类并返回 `typeMismatch` 有效性

```html
<input type="email" id="email" name="email" multiple />
```

**重要注意事项：**
- `a@b` 被视为有效（允许内部网络地址）
- 使用 `pattern` 属性进行自定义验证

### 搜索字段 (`type="search"`)

```html
<label for="search">请输入搜索词：</label>
<input type="search" name="search" id="search" />
```

**关键特性：**
- **视觉样式**：某些浏览器显示圆角
- **清除图标**：在聚焦时显示清除按钮以清空字段
- **键盘**：按 Enter 键可能显示“搜索”或放大镜图标
- **自动补全**：保存并重用页面间的值

### 电话号码字段 (`type="tel"`)

```html
<label for="tel">请输入电话号码：</label>
<input type="tel" id="tel" name="tel" />
```

**关键特性：**
- **移动键盘**：在触摸设备上显示数字键盘
- **无格式强制**：允许字母和特殊字符（适应各种国际格式）
- **模式验证**：使用 `pattern` 属性强制特定格式

### URL 字段 (`type="url"`)

```html
<label for="url">请输入一个 URL：</label>
<input type="url" id="url" name="url" />
```

**关键特性：**
- **验证要求**：必须包含协议（如 `http:`）并强制正确格式
- **移动键盘**：默认显示冒号、点号和正斜杠
- **注意**：格式正确的 URL 不一定代表网站存在

### 数字字段 (`type="number"`)

```html
<label for="number">请输入一个数字：</label>
<input type="number" id="number" name="number" />
```

**属性：**

| 属性 | 用途 | 示例 |
|------|------|------|
| `min` | 最小值 | `min="1"` |
| `max` | 最大值 | `max="10"` |
| `step` | 增量/减量值 | `step="2"` |

**示例：**

1-10 之间的奇数：
```html
<input type="number" name="age" id="age" min="1" max="10" step="2" />
```

0-1 之间的小数：
```html
<input type="number" name="change" id="pennies" min="0" max="1" step="0.01" />
```

**关键特性：**
- **滚动按钮**：增加/减少值
- **移动设备**：显示数字键盘
- **默认步长**：`1`（除非更改，否则仅允许整数）
- **浮点数**：使用 `step="any"` 或 `step="0.01"`

### 滑块控件 (`type="range"`)

```html
<label for="price">选择最大房屋价格：</label>
<input
  type="range"
  name="price"
  id="price"
  min="50000"
  max="500000"
  step="1000"
  value="250000" />
<output class="price-output" for="price"></output>
```

**JavaScript 显示值：**
```javascript
const price = document.querySelector("#price");
const output = document.querySelector(".price-output");

output.textContent = price.value;

price.addEventListener("input", () => {
  output.textContent = price.value;
});
```

**关键特性：**
- 比文本输入精度低（适合近似值）
- 通过鼠标、触摸或键盘箭头移动滑块
- 使用 `<output>` 元素显示当前值
- 通过 `min`、`max`、`step` 属性进行配置

### 日期和时间选择器

#### 日期 (`type="date"`)

```html
<label for="date">请输入日期：</label>
<input type="date" name="date" id="date" />
```
捕获：年、月、日（无时间）。

#### 日期和时间（本地）(`type="datetime-local"`)

```html
<label for="datetime">请输入日期和时间：</label>
<input type="datetime-local" name="datetime" id="datetime" />
```
捕获：日期和时间（无时区）。

#### 月份 (`type="month"`)

```html
<label for="month">请输入月份：</label>
<input type="month" name="month" id="month" />
```
捕获：月份和年份。

#### 时间 (`type="time"`)

```html
<label for="time">请输入时间：</label>
<input type="time" name="time" id="time" />
```
- **显示格式**：某些浏览器使用 12 小时制
- **返回格式**：始终使用 24 小时制

#### 周 (`type="week"`)

```html
<label for="week">请输入周数：</label>
<input type="week" name="week" id="week" />
```
- 周数：周一至周日
- 第一周：包含当年的第一个星期四

#### 日期/时间限制

```html
<label for="myDate">您今年什么时候有空？</label>
<input
  type="date"
  name="myDate"
  min="2025-06-01"
  max="2025-08-31"
  step="7"
  id="myDate" />
```

#### 验证示例（CSS）

```css
input:invalid + span::after {
  content: " X";
}

input:valid + span::after {
  content: " checkmark";
}
```

### 颜色选择器 (`type="color"`)

```html
<label for="color">选择一个颜色：</label>
<input type="color" name="color" id="color" />
```

**关键特性：**
- 打开操作系统默认的颜色选择功能
- 返回值：始终为小写的 6 位十六进制（如 `#ff0000`）
- 不需要手动输入格式：系统颜色选择器处理选择

### 客户端验证注意事项

**优势：**
- 即时用户反馈
- 引导准确填写表单
- 节省服务器往返请求

**重要限制：**
- 不是安全措施——用户可以轻易禁用
- 始终需要服务器端验证
- 仅能阻止明显的错误，不能阻止恶意数据

---

## 其他表单控件

> **来源:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Other_form_controls

### 多行文本字段 (`<textarea>`)

```html
<textarea cols="30" rows="8"></textarea>
```

**关键特性：**
- 允许用户输入多行文本
- 支持硬换行（按 Enter 键）
- 内容位于标签之间
- 需要闭合标签（不同于 `<input>`）

**控制多行渲染：**

| 属性 | 描述 |
|------|------|
| `cols` | 显示宽度（以平均字符宽度计算，默认为 20） |
| `rows` | 显示的文本行数（默认为 2） |
| `wrap` | 文本换行行为：`soft`（默认）、`hard` 或 `off` |

**换行示例：**
```html
<textarea cols="30" rows="8" wrap="hard"></textarea>
```

**控制可调整大小（CSS）：**
```css
textarea {
  resize: both;        /* 水平和垂直均可调整 */
  resize: horizontal;  /* 仅水平调整 */
  resize: vertical;    /* 仅垂直调整 */
  resize: none;        /* 不可调整 */
}
```

### 下拉控件

#### 单选下拉框（`<select>`）

```html
<select id="simple" name="simple">
  <option>Banana</option>
  <option selected>Cherry</option>
  <option>Lemon</option>
</select>
```

**带分组 (`<optgroup>`):**
```html
<select id="groups" name="groups">
  <optgroup label="水果">
    <option>Banana</option>
    <option selected>Cherry</option>
    <option>Lemon</option>
  </optgroup>
  <optgroup label="蔬菜">
    <option>胡萝卜</option>
    <option>茄子</option>
    <option>土豆</option>
  </optgroup>
</select>
```

**带值属性：**
```html
<select id="simple" name="simple">
  <option value="banana">大而美丽的黄色香蕉</option>
  <option value="cherry">多汁的樱桃</option>
  <option value="lemon">强烈而清新的柠檬</option>
</select>
```

**属性：**
- `selected`：设置默认选中选项
- `value`：提交表单时发送的值（若未指定，使用选项文本）
- `size`：显示的选项数量

#### 多选下拉框

```html
<select id="multi" name="multi" multiple size="2">
  <optgroup label="水果">
    <option>Banana</option>
    <option selected>Cherry</option>
    <option>Lemon</option>
  </optgroup>
  <optgroup label="蔬菜">
    <option>胡萝卜</option>
    <option>茄子</option>
    <option>土豆</option>
  </optgroup>
</select>
```

**注意事项：**
- 添加 `multiple` 属性以允许多选
- 用户通过 Cmd/Ctrl+点击在桌面设备上选择
- 所有值以列表形式显示（非下拉）

#### 自动补全框 (`<datalist>`)

```html
<label for="myFruit">您最喜欢的水果是什么？</label>
<input type="text" name="myFruit" id="myFruit" list="mySuggestion" />
<datalist id="mySuggestion">
  <option>苹果</option>
  <option>香蕉</option>
  <option>黑莓</option>
  <option>蓝莓</option>
  <option>柠檬</option>
  <option>荔枝</option>
  <option>桃子</option>
  <option>梨</option>
</datalist>
```

**工作原理：**
- `<datalist>` 提供建议值
- 通过 `list` 属性与输入绑定（必须匹配 `datalist` 的 `id`）
- 浏览器在用户输入时显示匹配值
- 可与多种输入类型（文本、电子邮件、范围、颜色等）配合使用

### 进度条 (`<progress>`)

```html
<progress max="100" value="75">75/100</progress>
```

**属性：**
- `max`：最大值（未指定时默认为 1.0）
- `value`：当前进度值
- 标签内的内容是不支持浏览器的备用显示

**使用场景：** 下载进度、问卷完成度、任务进度。

### 指标 (`<meter>`)

```html
<meter min="0" max="100" value="75" low="33" high="66" optimum="0">75</meter>
```

**属性：**
- `min` / `max`：范围边界
- `low` / `high`：定义三个范围（低、中、高）
- `value`：当前指标值
- `optimum`：首选值（决定颜色编码）

**颜色编码：**
- 绿色：值在首选范围内
- 黄色：值在平均范围内
- 红色：值在最差范围内

**首选值逻辑：**
- 如果 `optimum` 在低范围：低为首选
- 如果 `optimum` 在中范围：中为首选
- 如果 `optimum` 在高范围：高为首选

**使用场景：** 磁盘空间使用情况、温度计、评分系统。

---

## 其他表单控件总结

| 元素 | 用途 | 输入类型 |
|------|------|----------|
| `<textarea>` | 多行文本输入 | 文本内容 |
| `<select>` | 单选或多选 | 预定义选项 |
| `<datalist>` | 建议的自动补全值 | 带建议的文本输入 |
| `<progress>` | 进度指示 | 只读显示 |
| `<meter>` | 测量显示 | 只读显示 |

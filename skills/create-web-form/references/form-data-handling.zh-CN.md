# 表单数据处理参考指南

---

## 第一节：发送和获取表单数据

**来源：** https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Sending_and_retrieving_form_data

### 概述

一旦表单数据在客户端完成验证，它就准备好提交了。本节将介绍用户提交表单时会发生什么，数据会发送到哪里，以及如何在服务器端处理这些数据。

### 客户端/服务器架构

网络使用基本的客户端/服务器架构：

- **客户端**（网络浏览器）向**服务器**发送 HTTP 请求。
- **服务器**（Apache、Nginx、IIS、Tomcat）使用相同的协议进行响应。
- HTML 表单是配置 HTTP 请求以发送数据的用户友好方式。

### 客户端：定义如何发送数据

`<form>` 元素控制数据如何发送。两个关键属性是 `action` 和 `method`。

#### `action` 属性

`action` 属性定义了表单数据发送的目标位置。它必须是一个有效的相对或绝对 URL。

**绝对 URL：**

```html
<form action="https://www.example.com">...</form>
```

**相对 URL（同源）：**

```html
<form action="/somewhere_else">...</form>
```

**同一页（无属性或空 action）：**

```html
<form>...</form>
```

**安全提示：** 使用 HTTPS（安全 HTTP）来加密数据。如果安全表单提交到不安全的 HTTP URL，浏览器会显示安全警告。

#### `method` 属性

传输表单数据的两种主要 HTTP 方法是 **GET** 和 **POST**。

### GET 方法

- 用于浏览器请求服务器发送资源。
- 数据以查询参数的形式附加到 URL。
- 浏览器发送空请求体。

**示例表单：**

```html
<form action="https://www.example.com/greet" method="GET">
  <div>
    <label for="say">你想说什么问候语？</label>
    <input name="say" id="say" value="Hi" />
  </div>
  <div>
    <label for="to">你想对谁说？</label>
    <input name="to" id="to" value="Mom" />
  </div>
  <div>
    <button>发送我的问候</button>
  </div>
</form>
```

**结果 URL：** `https://www.example.com/greet?say=Hi&to=Mom`

**HTTP 请求：**

```http
GET /?say=Hi&to=Mom HTTP/2.0
Host: example.com
```

**何时使用：** 读取数据，非敏感信息。

### POST 方法

- 用于发送服务器应处理的数据。
- 数据包含在 HTTP 请求体中，而不是 URL。
- 对于敏感数据（如密码）更安全。

**示例表单：**

```html
<form action="https://www.example.com/greet" method="POST">
  <div>
    <label for="say">你想说什么问候语？</label>
    <input name="say" id="say" value="Hi" />
  </div>
  <div>
    <label for="to">你想对谁说？</label>
    <input name="to" id="to" value="Mom" />
  </div>
  <div>
    <button>发送我的问候</button>
  </div>
</form>
```

**HTTP 请求：**

```http
POST / HTTP/2.0
Host: example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

say=Hi&to=Mom
```

**何时使用：** 敏感数据、大量数据、修改服务器状态。

### 在浏览器开发者工具中查看 HTTP 请求

1. 打开开发者工具（F12）。
2. 选择“网络”标签页。
3. 选择“全部”以查看所有请求。
4. 点击“名称”标签页中的请求。
5. 查看“请求”（Firefox）或“负载”（Chrome/Edge）。

### 服务器端：获取数据

服务器接收数据作为字符串，并解析为键/值对。访问方式取决于服务器平台。

#### 示例：原始 PHP

```php
<?php
  // 访问 POST 数据
  $say = htmlspecialchars($_POST["say"]);
  $to  = htmlspecialchars($_POST["to"]);

  // 访问 GET 数据
  // $say = htmlspecialchars($_GET["say"]);

  echo $say, " ", $to;
?>
```

**输出：** `Hi Mom`

#### 示例：使用 Python 和 Flask

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('form.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return render_template('greeting.html',
                         say=request.form['say'],
                         to=request.form['to'])

if __name__ == "__main__":
    app.run()
```

#### 其他服务器端框架

| 语言   | 框架                              |
|--------|-----------------------------------|
| Python | Django、Flask、web2py、py4web     |
| Node.js | Express、Next.js、Nuxt、Remix    |
| PHP    | Laravel、Laminas、Symfony         |
| Ruby   | Ruby On Rails                     |
| Java   | Spring Boot                       |

### 特殊情况：发送文件

文件是二进制数据，需要特殊处理。需要三个步骤：

#### `enctype` 属性

此属性指定 HTTP 头的 `Content-Type`。

- **默认值：** `application/x-www-form-urlencoded`
- **用于文件：** `multipart/form-data`

**文件上传示例：**

```html
<form
  method="post"
  action="https://example.com/upload"
  enctype="multipart/form-data">
  <div>
    <label for="file">选择一个文件</label>
    <input type="file" id="file" name="myFile" />
  </div>
  <div>
    <button>发送文件</button>
  </div>
</form>
```

**要求：**

- 将 `method` 设置为 `POST`（文件内容不能放在 URL 中）。
- 将 `enctype` 设置为 `multipart/form-data`。
- 包含一个或多个 `<input type="file">` 控件。

**注意：** 服务器可以限制文件和请求的大小以防止滥用。

### 安全考虑

#### 警惕：永远不要信任用户

所有传入的数据都必须检查和清理：

1. **转义危险字符** -- 注意可执行代码模式（如 JavaScript、SQL 命令）。使用服务器端转义函数。不同的上下文需要不同的转义方式。
2. **限制传入数据** -- 仅接受必要的数据。设置请求的最大尺寸。
3. **隔离上传的文件** -- 存储在不同的服务器上。通过不同的子域名或域名提供服务。永远不要直接执行上传的文件。

**关键规则：** 永远不要仅依赖客户端验证 -- 始终在服务器端验证。客户端验证可以被恶意用户绕过；服务器无法验证客户端真正发生了什么。

### 快速参考：GET 与 POST 的区别

| 方面             | GET                                  | POST                                   |
|------------------|--------------------------------------|----------------------------------------|
| 数据位置         | 显示在 URL 中作为查询参数            | 隐藏在请求体中                          |
| 数据大小         | 受 URL 长度限制                      | 没有固有限制                            |
| 安全性           | 不适合敏感数据                        | 更适合敏感/大数据                        |
| 缓存             | 可缓存                                | 不缓存                                  |
| 使用场景         | 读取/检索数据                         | 修改服务器状态、发送文件                |

### 重要注意事项

- **表单数据格式：** 名称/值对通过 & 符号连接（`name=value&name2=value2`）。
- **URL 编码：** 查询参数中的特殊字符会进行 URL 编码。
- **默认表单目标：** 如果没有 `action`，数据将提交到当前页面。
- **安全协议：** 对于敏感数据，始终使用 HTTPS。

---

## 第二节：表单验证

**来源：** https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Form_validation

### 概述

客户端表单验证有助于确保输入的数据符合表单控件的要求。虽然对**用户体验**很重要，但必须**始终**与服务器端验证结合使用，因为客户端验证很容易被恶意用户绕过。

### 内置的 HTML 验证属性

#### `required`

指定在提交前必须填写表单字段。

```html
<input id="choose" name="i-like" required />
```

- 当输入为空时，输入字段匹配 `:required` 和 `:invalid` 伪类。
- 对于单选按钮，同一组中必须选择一个按钮。

#### `minlength` 和 `maxlength`

限制文本字段和文本区域的字符长度。

```html
<input type="text" minlength="6" maxlength="6" />
<textarea maxlength="140"></textarea>
```

#### `min`、`max` 和 `step`

限制数值及其递增间隔。

```html
<input type="number" min="1" max="10" step="1" />
<input type="date" min="2024-01-01" max="2024-12-31" />
```

#### `type`

验证特定格式（如电子邮件、URL、数字、日期等）。

```html
<input type="email" />
<input type="url" />
<input type="number" />
```

#### `pattern`

根据正则表达式进行验证。

```html
<input
  type="text"
  pattern="[Bb]anana|[Cc]herry"
  required
/>
```

**模式示例：**

| 模式  | 匹配内容                                 |
|-------|------------------------------------------|
| `a`   | 单个字符 'a'                             |
| `abc` | 'a' 后跟 'b' 后跟 'c'                     |
| `ab?c` | 'ac' 或 'abc'                             |
| `ab*c` | 'ac'、'abc'、'abbbbbc' 等                   |
| `a\|b` | 'a' 或 'b'                                |

### 验证状态的 CSS 伪类

#### 有效状态

```css
input:valid {
  border: 2px solid black;
}

input:user-valid {
  /* 用户交互后匹配 */
}

input:in-range {
  /* 用于具有 min/max 的输入 */
}
```

#### 无效状态

```css
input:invalid {
  border: 2px dashed red;
}

input:user-invalid {
  /* 用户交互后匹配 */
}

input:out-of-range {
  /* 用于具有 min/max 的输入 */
}

input:required {
  /* 匹配必填字段 */
}
```

### 完整的内置验证示例

```html
<form>
  <p>请填写所有必填字段（* 表示必填）。</p>

  <fieldset>
    <legend>你有驾照吗？ *</legend>
    <input type="radio" required name="driver" id="r1" value="yes" />
    <label for="r1">有</label>
    <input type="radio" required name="driver" id="r2" value="no" />
    <label for="r2">没有</label>
  </fieldset>

  <p>
    <label for="age">你多大了？</label>
    <input type="number" min="12" max="120" step="1" id="age" name="age" />
  </p>

  <p>
    <label for="fruit">你最喜欢的水果是什么？ *</label>
    <input
      type="text"
      id="fruit"
      name="fruit"
      list="fruits"
      required
      pattern="[Bb]anana|[Cc]herry|[Aa]pple"
    />
    <datalist id="fruits">
      <option>Banana</option>
      <option>Cherry</option>
      <option>Apple</option>
    </datalist>
  </p>

  <p>
    <label for="email">电子邮件地址：</label>
    <input type="email" id="email" name="email" />
  </p>

  <button>提交</button>
</form>
```

### 约束验证 API

约束验证 API 提供了用于自定义验证逻辑的方法和属性。

#### 关键属性

**`validationMessage`** -- 返回本地化的验证错误信息。

**`validity`** -- 返回一个 `ValidityState` 对象，包含以下属性：

| 属性           | 描述                                       |
|----------------|--------------------------------------------|
| `valid`        | 如果元素满足所有约束条件则为 `true`         |
| `valueMissing` | 如果必填但为空则为 `true`                   |
| `typeMismatch` | 如果值与类型不匹配（例如电子邮件）则为 `true` |
| `patternMismatch` | 如果模式不匹配则为 `true`                  |
| `tooLong`      | 如果超过 `maxlength` 则为 `true`            |
| `tooShort`     | 如果低于 `minlength` 则为 `true`             |
| `rangeOverflow` | 如果超过 `max` 则为 `true`                   |
| `rangeUnderflow` | 如果低于 `min` 则为 `true`                  |
| `customError`  | 如果通过 `setCustomValidity()` 设置了自定义错误则为 `true` |

**`willValidate`** -- 布尔值，如果元素在表单提交时会被验证则为 `true`。

#### 关键方法

```javascript
// 在不提交表单的情况下检查有效性
element.checkValidity()    // 返回布尔值

// 向用户报告有效性
element.reportValidity()   // 显示浏览器的错误提示

// 设置自定义错误信息
element.setCustomValidity("自定义错误信息")

// 清除自定义错误
element.setCustomValidity("")
```

### JavaScript 自定义验证示例

#### 基本自定义错误信息

```javascript
const email = document.getElementById("mail");

email.addEventListener("input", (event) => {
  if (email.validity.typeMismatch) {
    email.setCustomValidity("我期待的是一个电子邮件地址！");
  } else {
    email.setCustomValidity("");
  }
});
```

#### 扩展内置验证

```javascript
const email = document.getElementById("mail");

email.addEventListener("input", (event) => {
  // 重置自定义有效性
  email.setCustomValidity("");

  // 首先检查内置约束
  if (!email.validity.valid) {
    return;
  }

  // 添加自定义约束
  if (!email.value.endsWith("@example.com")) {
    email.setCustomValidity("请输入以 @example.com 域结尾的电子邮件地址。");
  }
});
```

#### 使用自定义消息进行复杂表单验证

```javascript
const form = document.querySelector("form");
const email = document.getElementById("mail");
const emailError = document.querySelector("#mail + span.error");

email.addEventListener("input", () => {
  if (email.validity.valid) {
    emailError.textContent = "";
    emailError.className = "error";
  } else {
    showError();
  }
});

form.addEventListener("submit", (event) => {
  if (!email.validity.valid) {
    showError();
    event.preventDefault();
  }
});

function showError() {
  if (email.validity.valueMissing) {
    emailError.textContent = "请输入电子邮件地址。";
  } else if (email.validity.typeMismatch) {
    emailError.textContent = "输入的值必须是电子邮件地址。";
  } else if (email.validity.tooShort) {
    emailError.textContent =
      `电子邮件地址应至少有 ${email.minLength} 个字符；你输入了 ${email.value.length} 个字符。`;
  }
  emailError.className = "error active";
}
```

#### 使用 `novalidate` 禁用内置验证

在表单上使用 `novalidate` 来禁用浏览器的自动验证，同时保留 CSS 伪类：

```html
<form novalidate>
  <input type="email" id="mail" required minlength="8" />
  <span class="error" aria-live="polite"></span>
</form>
```

### 不使用约束 API 的手动验证

对于自定义表单控件或完全控制验证：

```javascript
const form = document.querySelector("form");
const email = document.getElementById("mail");
const error = document.getElementById("error");

const emailRegExp = /^[\w.!#$%&'*+/=?^`{|}~-]+@[a-z\d-]+(?:\.[a-z\d-]+)*$/i;

const isValidEmail = () => {
  return email.value.length !== 0 && emailRegExp.test(email.value);
};

const setEmailClass = (isValid) => {
  email.className = isValid ? "valid" : "invalid";
};

const updateError = (isValid) => {
  if (isValid) {
    error.textContent = "";
    error.removeAttribute("class");
  } else {
    error.textContent = "请输入有效的电子邮件地址。";
    error.setAttribute("class", "active");
  }
};

email.addEventListener("input", () => {
  const validity = isValidEmail();
  setEmailClass(validity);
  updateError(validity);
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const validity = isValidEmail();
  setEmailClass(validity);
  updateError(validity);
});
```

### 样式错误信息

```css
/* 无效字段样式 */
input:invalid {
  border-color: #990000;
  background-color: #ffdddd;
}

input:focus:invalid {
  outline: none;
}

/* 错误信息容器 */
.error {
  width: 100%;
  padding: 0;
  font-size: 80%;
  color: white;
  background-color: #990000;
  border-radius: 0 0 5px 5px;
}

.error.active {
  padding: 0.3em;
}
```

### 可访问性最佳实践

1. **在标签中使用星号标记必填字段：**
   ```html
   <label for="name">姓名 *</label>
   ```
2. **使用 `aria-live` 用于动态错误信息：**
   ```html
   <span class="error" aria-live="polite"></span>
   ```
3. **提供清晰、有帮助的提示信息，说明期望的内容以及如何修复错误。**
4. **不要仅依靠颜色来指示错误。**

### 验证总结

| 方法               | 优点                                       | 缺点                                   |
|--------------------|--------------------------------------------|----------------------------------------|
| HTML 内置验证       | 不需要 JavaScript，速度快                  | 自定义能力有限                          |
| 约束验证 API        | 现代，与内置功能集成                        | 需要 JavaScript                        |
| 完全手动（JS）      | 对 UI 和逻辑有完全的控制                    | 需要更多代码，必须处理所有内容          |

- **HTML 验证** 速度更快，不需要 JavaScript。
- **JavaScript 验证** 提供了更多的自定义和控制。
- **始终在服务器端验证** -- 客户端验证并不安全。
- **使用约束验证 API** 来实现现代、内置的功能。
- **为用户提供清晰的错误信息和指导。**
- **使用 `:valid` 和 `:invalid` 伪类来样式验证状态。**

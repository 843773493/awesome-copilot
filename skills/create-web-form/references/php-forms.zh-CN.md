# PHP 表单参考指南

本参考指南整合了 W3Schools 关于 PHP 表单处理、验证、必填字段、URL/电子邮件验证以及完整示例的关键教育内容。

---

## PHP 表单处理

> **来源:** <https://www.w3schools.com/php/php_forms.asp>

### PHP 表单的工作原理

PHP 超全局变量 `$_GET` 和 `$_POST` 用于收集表单数据。当用户填写表单并点击提交时，表单数据会通过 HTTP POST 方法发送到 `<form>` 标签中 `action` 属性指定的 PHP 文件。

### 一个简单的 HTML 表单

```html
<html>
<body>

<form action="welcome.php" method="post">
  姓名: <input type="text" name="name"><br>
  电子邮件: <input type="text" name="email"><br>
  <input type="submit">
</form>

</body>
</html>
```

当用户填写表单并点击提交时，表单数据通过 HTTP POST 方法发送到 `welcome.php`。处理文件可以访问这些数据：

```php
<html>
<body>

欢迎 <?php echo $_POST["name"]; ?><br>
您的电子邮件地址是: <?php echo $_POST["email"]; ?>

</body>
</html>
```

### 使用 GET 方法

```html
<form action="welcome_get.php" method="get">
  姓名: <input type="text" name="name"><br>
  电子邮件: <input type="text" name="email"><br>
  <input type="submit">
</form>
```

```php
<html>
<body>

欢迎 <?php echo $_GET["name"]; ?><br>
您的电子邮件地址是: <?php echo $_GET["email"]; ?>

</body>
</html>
```

### GET 与 POST 的比较

| 特性         | GET                     | POST                    |
|--------------|--------------------------|--------------------------|
| 可见性       | 数据在 URL 中可见（作为查询字符串参数） | 数据不会显示在 URL 中     |
| 收藏页面     | 可以通过查询字符串值收藏页面 | 无法通过提交的数据收藏页面 |
| 数据长度     | 有限制（最大 URL 长度约为 2048 个字符） | 没有数据大小限制         |
| 安全性       | 绝对不要用于发送敏感数据（如密码等） | 对于敏感数据比 GET 更安全 |
| 缓存         | 请求可以被缓存           | 请求不会被缓存           |
| 浏览器历史   | 参数保留在浏览器历史中   | 参数不会保存在浏览器历史中 |
| 使用场景     | 非敏感数据、搜索查询、筛选参数 | 敏感数据、改变数据的表单提交 |

**重要提示:** `$_GET` 和 `$_POST` 都是超全局数组。它们在任何作用域中始终可用，且无需任何特殊操作即可从任何函数、类或文件中访问。

---

## PHP 表单验证

> **来源:** <https://www.w3schools.com/php/php_form_validation.asp>

### 处理 PHP 表单时考虑安全性

这些页面展示了如何以安全的方式处理 PHP 表单。对表单数据进行适当的验证对于保护表单免受黑客和垃圾邮件发送者的攻击非常重要。

### HTML 表单

本教程中使用的表单：

- **字段:** 姓名、电子邮件、网站、评论、性别
- **验证规则:**

| 字段   | 验证规则 |
|--------|----------|
| 姓名   | 必填。仅允许包含字母、破折号、单引号和空格 |
| 电子邮件 | 必填。必须包含有效的电子邮件地址（包含 `@` 和 `.`） |
| 网站   | 可选。如果存在，必须包含有效的 URL |
| 评论   | 可选。多行输入字段（textarea） |
| 性别   | 必填。必须选择一个选项 |

### 表单元素

```html
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
```

`$_SERVER["PHP_SELF"]` 变量返回当前正在执行脚本的文件名。因此，表单数据会发送到当前页面，而不是其他页面。

### 什么是 `$_SERVER["PHP_SELF"]`？

`$_SERVER["PHP_SELF"]` 是一个超全局变量，返回当前正在执行脚本的文件名，相对于文档根目录。

### 关于 PHP 表单安全性的重大提示

`$_SERVER["PHP_SELF"]` 变量可能被黑客利用进行 **跨站脚本攻击 (XSS)**。

**XSS** 允许攻击者将客户端脚本注入其他用户查看的网页中。例如，如果表单位于名为 `test_form.php` 的页面上，用户可以输入以下 URL：

```
http://www.example.com/test_form.php/%22%3E%3Cscript%3Ealert('hacked')%3C/script%3E
```

这将转换为：

```html
<form method="post" action="test_form.php/"><script>alert('hacked')</script>
```

`<script>` 标签被添加，并执行 `alert` 命令。这只是个简单的例子。任何 JavaScript 代码都可以放在 `<script>` 标签中，攻击者可以将用户重定向到另一个服务器上的文件，该文件包含恶意代码，可能会修改全局变量或将表单提交到其他地址。

### 如何避免 `$_SERVER["PHP_SELF"]` 的漏洞

使用 `htmlspecialchars()`：

```php
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
```

`htmlspecialchars()` 函数将特殊字符转换为 HTML 实体。现在如果用户试图利用 `PHP_SELF`，输出将安全地显示为：

```html
<form method="post" action="test_form.php/&quot;&gt;&lt;script&gt;alert('hacked')&lt;/script&gt;">
```

由于代码被转义，攻击尝试失败，被当作纯文本处理。

### 使用 PHP 验证表单数据

1. 使用 `trim()` 清理用户输入中的多余字符（多余空格、制表符、换行符）。
2. 使用 `stripslashes()` 移除用户输入中的反斜杠。
3. 使用 `htmlspecialchars()` 将特殊字符转换为 HTML 实体。

### `test_input()` 函数

创建一个可重用的函数进行所有检查：

```php
<?php
function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}
?>
```

### 处理表单

```php
<?php
// 定义变量并设置为空值
$nameErr = $emailErr = $genderErr = $websiteErr = "";
$name = $email = $gender = $comment = $website = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = test_input($_POST["name"]);
    $email = test_input($_POST["email"]);
    $website = test_input($_POST["website"]);
    $comment = test_input($_POST["comment"]);
    $gender = test_input($_POST["gender"]);
}
?>
```

**重要提示:** 在脚本开始时，我们通过检查 `$_SERVER["REQUEST_METHOD"]` 来判断表单是否已提交。如果 `REQUEST_METHOD` 是 `POST`，则表示表单已提交，需要进行验证。

---

## PHP 表单必填字段

> **来源:** <https://www.w3schools.com/php/php_form_required.asp>

### 设置必填字段

在上一节中，所有输入字段都是可选的。在本节中，我们添加验证以确保某些字段为必填项，并在需要时显示错误信息。

### 添加错误变量

为每个必填字段定义错误变量并初始化为空：

```php
<?php
// 定义变量并设置为空值
$nameErr = $emailErr = $genderErr = $websiteErr = "";
$name = $email = $gender = $comment = $website = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (empty($_POST["name"])) {
        $nameErr = "姓名为必填项";
    } else {
        $name = test_input($_POST["name"]);
    }

    if (empty($_POST["email"])) {
        $emailErr = "电子邮件为必填项";
    } else {
        $email = test_input($_POST["email"]);
    }

    if (empty($_POST["website"])) {
        $website = "";
    } else {
        $website = test_input($_POST["website"]);
    }

    if (empty($_POST["comment"])) {
        $comment = "";
    } else {
        $comment = test_input($_POST["comment"]);
    }

    if (empty($_POST["gender"])) {
        $genderErr = "性别为必填项";
    } else {
        $gender = test_input($_POST["gender"]);
    }
}
?>
```

### `empty()` 函数

`empty()` 函数检查变量是否为空、null 或具有假值（falsy value）。它返回 `true` 用于空字符串、null、`0`、`"0"`、`false` 和未定义的变量。

### 显示错误信息

在 HTML 表单中，将错误信息显示在对应字段旁边：

```html
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">

  姓名: <input type="text" name="name" value="<?php echo $name; ?>">
  <span class="error">* <?php echo $nameErr; ?></span>
  <br><br>

  电子邮件: <input type="text" name="email" value="<?php echo $email; ?>">
  <span class="error">* <?php echo $emailErr; ?></span>
  <br><br>

  网站: <input type="text" name="website" value="<?php echo $website; ?>">
  <span class="error"><?php echo $websiteErr; ?></span>
  <br><br>

  评论: <textarea name="comment" rows="5" cols="40"><?php echo $comment; ?></textarea>
  <br><br>

  性别:
  <input type="radio" name="gender"
    <?php if (isset($gender) && $gender == "female") echo "checked"; ?>
    value="female">女性
  <input type="radio" name="gender"
    <?php if (isset($gender) && $gender == "male") echo "checked"; ?>
    value="male">男性
  <input type="radio" name="gender"
    <?php if (isset($gender) && $gender == "other") echo "checked"; ?>
    value="other">其他
  <span class="error">* <?php echo $genderErr; ?></span>
  <br><br>

  <input type="submit" name="submit" value="提交">

</form>
```

### 错误信息样式

使用 CSS 使错误信息突出显示：

```css
.error {
    color: #FF0000;
}
```

### 必填字段指示符

通常在必填字段旁边放置一个星号 `*` 来表示必须填写。星号可以直接在 HTML 中添加，也可以通过 PHP 动态生成。

---

## PHP 表单 URL 和电子邮件验证

> **来源:** <https://www.w3schools.com/php/php_form_url_email.asp>

### 验证姓名

使用 `preg_match()` 检查姓名字段是否仅包含字母、破折号、单引号和空格：

```php
$name = test_input($_POST["name"]);
if (!preg_match("/^[a-zA-Z-' ]*$/", $name)) {
    $nameErr = "仅允许字母和空格";
}
```

`preg_match()` 函数在字符串中搜索模式，返回 `1` 表示匹配成功，返回 `0` 表示匹配失败。

### 验证电子邮件地址

使用 `filter_var()` 检查电子邮件地址是否格式正确：

```php
$email = test_input($_POST["email"]);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $emailErr = "电子邮件格式无效";
}
```

`filter_var()` 函数使用指定的过滤常量对变量进行过滤。`FILTER_VALIDATE_EMAIL` 用于验证电子邮件地址格式。

### 验证 URL

使用 `preg_match()` 检查 URL 是否有效：

```php
$website = test_input($_POST["website"]);
if (!preg_match("/\b(?:https?|ftp):\/\/|www\.[-a-z0-9+&@#\/%?=~_|!:,.;]*[-a-z0-9+&@#\/%=~_|]/i", $website)) {
    $websiteErr = "无效的 URL";
}
```

或者，也可以使用 `filter_var()` 验证 URL：

```php
if (!filter_var($website, FILTER_VALIDATE_URL)) {
    $websiteErr = "无效的 URL";
}
```

### 综合验证逻辑

在表单处理块中整合所有验证检查：

```php
<?php
// 定义变量并设置为空值
$nameErr = $emailErr = $genderErr = $websiteErr = "";
$name = $email = $gender = $comment = $website = "";

function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (empty($_POST["name"])) {
        $nameErr = "姓名为必填项";
    } else {
        $name = test_input($_POST["name"]);
        // 检查姓名是否仅包含字母和空格
        if (!preg_match("/^[a-zA-Z-' ]*$/", $name)) {
            $nameErr = "仅允许字母和空格";
        }
    }

    if (empty($_POST["email"])) {
        $emailErr = "电子邮件为必填项";
    } else {
        $email = test_input($_POST["email"]);
        // 检查电子邮件地址格式是否正确
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $emailErr = "电子邮件格式无效";
        }
    }

    if (empty($_POST["website"])) {
        $website = "";
    } else {
        $website = test_input($_POST["website"]);
        // 检查 URL 地址语法是否有效
        if (!preg_match("/\b(?:https?|ftp):\/\/|www\.[-a-z0-9+&@#\/%?=~_|!:,.;]*[-a-z0-9+&@#\/%=~_|]/i", $website)) {
            $websiteErr = "无效的 URL";
        }
    }

    if (empty($_POST["comment"])) {
        $comment = "";
    } else {
        $comment = test_input($_POST["comment"]);
    }

    if (empty($_POST["gender"])) {
        $genderErr = "性别为必填项";
    } else {
        $gender = test_input($_POST["gender"]);
    }
}
?>
```

### 完整的 HTML 表单

```html
<!DOCTYPE HTML>
<html>
<head>
<style>
.error {color: #FF0000;}
</style>
</head>
<body>

<h2>PHP 表单验证示例</h2>
<p><span class="error">* 必填字段</span></p>

<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">

  姓名: <input type="text" name="name" value="<?php echo $name; ?>">
  <span class="error">* <?php echo $nameErr; ?></span>
  <br><br>

  电子邮件: <input type="text" name="email" value="<?php echo $email; ?>">
  <span class="error">* <?php echo $emailErr; ?></span>
  <br><br>

  网站: <input type="text" name="website" value="<?php echo $website; ?>">
  <span class="error"><?php echo $websiteErr; ?></span>
  <br><br>

  评论: <textarea name="comment" rows="5" cols="40"><?php echo $comment; ?></textarea>
  <br><br>

  性别:
  <input type="radio" name="gender"
    <?php if (isset($gender) && $gender == "female") echo "checked"; ?>
    value="female">女性
  <input type="radio" name="gender"
    <?php if (isset($gender) && $gender == "male") echo "checked"; ?>
    value="male">男性
  <input type="radio" name="gender"
    <?php if (isset($gender) && $gender == "other") echo "checked"; ?>
    value="other">其他
  <span class="error">* <?php echo $genderErr; ?></span>
  <br><br>

  <input type="submit" name="submit" value="提交">

</form>

<?php
echo "<h2>您的输入:</h2>";
echo $name;
echo "<br>";
echo $email;
echo "<br>";
echo $website;
echo "<br>";
echo $comment;
echo "<br>";
echo $gender;
?>

</body>
</html>
```

### 关键函数摘要

| 函数 | 用途 |
|------|------|
| `htmlspecialchars()` | 将特殊字符（`<`, `>`, `&`, `"`, `'`）转换为 HTML 实体，以防止 XSS 攻击 |
| `trim()` | 从字符串的开头和结尾去除空格（或其他字符） |
| `stripslashes()` | 从字符串中移除反斜杠 |
| `empty()` | 检查变量是否为空、null 或具有假值 |
| `isset()` | 检查变量是否已设置且不为 null |
| `preg_match()` | 在字符串上执行正则表达式匹配 |
| `filter_var()` | 使用指定的过滤常量对变量进行过滤 |
| `$_POST` | 收集通过 POST 方法发送的表单数据的超全局数组 |
| `$_GET` | 收集通过 GET 方法发送的表单数据的超全局数组 |
| `$_SERVER["PHP_SELF"]` | 返回当前正在执行脚本的文件名 |
| `$_SERVER["REQUEST_METHOD"]` | 返回访问页面所使用的请求方法（例如 `POST`、`GET`） |

### 关键要点总结

1. **始终使用 `trim()`、`stripslashes()` 和 `htmlspecialchars()`** 通过可重用的 `test_input()` 函数清理用户输入。
2. **通过将 `$_SERVER["PHP_SELF"]` 传递给 `htmlspecialchars()`** 来防止 XSS 攻击。
3. **使用 `$_SERVER["REQUEST_METHOD"]`** 来检查表单是否已提交，然后再进行处理。
4. **使用 `empty()` 验证必填字段**，并在每个字段旁边显示错误信息。
5. **使用 `preg_match()`** 对模式（如姓名、URL）进行验证，使用 `filter_var()` 对电子邮件和 URL 进行验证。
6. **通过将变量回显到输入字段的 `value` 属性和 textarea 内容中** 来保留表单值。
7. **通过使用 `isset()` 和值比较** 条件性地添加 `checked` 属性以保留单选按钮的状态。
8. **对于包含敏感信息或大量数据的表单提交，优先使用 POST** 而不是 GET。

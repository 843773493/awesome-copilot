# PHP Cookie 参考

> 来源： <https://www.w3schools.com/php/php_cookies.asp>

## 什么是 Cookie？

Cookie 通常用于识别用户。它是一个由服务器嵌入到用户计算机中的小型文件。每次同一台计算机通过浏览器请求页面时，都会发送该 Cookie。使用 PHP，您可以创建和检索 Cookie 值。

## 使用 `setcookie()` 创建 Cookie

使用 `setcookie()` 函数创建 Cookie。

### 语法

```php
setcookie(name, value, expire, path, domain, secure, httponly);
```

### 参数

| 参数     | 描述                                                                                             |
|----------|-------------------------------------------------------------------------------------------------|
| `name`   | 必需。指定 Cookie 的名称。                                                                       |
| `value`  | 可选。指定 Cookie 的值。                                                                          |
| `expire` | 可选。指定 Cookie 的过期时间。值 `time() + 86400 * 30` 会将 Cookie 设置为 30 天后过期。如果省略此参数或设置为 `0`，Cookie 将在会话结束时过期（当浏览器关闭时）。默认值为 `0`。 |
| `path`   | 可选。指定 Cookie 的服务器路径。如果设置为 `"/"`，则 Cookie 将在整个网站范围内可用。如果设置为 `"/php/"`，则 Cookie 仅在 `php` 目录及其子目录中可用。默认值为当前设置 Cookie 的目录。 |
| `domain` | 可选。指定 Cookie 的域名。若要使 Cookie 在 `example.com` 的所有子域中可用，将 domain 设置为 `".example.com"`。 |
| `secure` | 可选。指定 Cookie 是否仅通过安全的 HTTPS 连接传输。`true` 表示只有在存在安全连接时才会设置 Cookie。默认值为 `false`。 |
| `httponly` | 可选。若设置为 `true`，Cookie 将仅通过 HTTP 协议可访问（Cookie 将无法通过脚本语言，如 JavaScript 访问）。此设置有助于减少通过 XSS 攻击进行身份盗窃的风险。默认值为 `false`。 |

**注意：** `setcookie()` 函数必须出现在 `<html>` 标签之前（在向浏览器发送任何输出之前）。

### 示例：创建 Cookie

以下示例创建了一个名为 "user" 的 Cookie，其值为 "John Doe"。该 Cookie 会在 30 天后过期。`"/"` 表示该 Cookie 在整个网站范围内可用：

```php
<?php
$cookie_name = "user";
$cookie_value = "John Doe";
setcookie($cookie_name, $cookie_value, time() + (86400 * 30), "/"); // 86400 = 1 天
?>
<html>
<body>

<?php
if(!isset($_COOKIE[$cookie_name])) {
    echo "Cookie 名为 '" . $cookie_name . "' 未设置！";
} else {
    echo "Cookie '" . $cookie_name . "' 已设置!<br>";
    echo "值为: " . $_COOKIE[$cookie_name];
}
?>

</body>
</html>
```

**注意：** `setcookie()` 函数将 Cookie 作为 HTTP 响应头的一部分发送。Cookie 在当前页面无法立即访问，直到再次加载包含该 Cookie 的页面。因此，为了测试 Cookie，必须重新加载页面或导航到其他页面。

## 检索 Cookie 值

使用 PHP 的 `$_COOKIE` 超全局变量来检索 Cookie 值。

```php
<?php
if(!isset($_COOKIE["user"])) {
    echo "Cookie 名为 'user' 未设置！";
} else {
    echo "Cookie 'user' 已设置!<br>";
    echo "值为: " . $_COOKIE["user"];
}
?>
```

**提示：** 在尝试访问 Cookie 值之前，使用 `isset()` 函数来判断 Cookie 是否已设置。

## 修改 Cookie 值

要修改 Cookie，只需使用 `setcookie()` 函数再次设置该 Cookie：

```php
<?php
$cookie_name = "user";
$cookie_value = "Alex Porter";
setcookie($cookie_name, $cookie_value, time() + (86400 * 30), "/");
?>
<html>
<body>

<?php
if(!isset($_COOKIE[$cookie_name])) {
    echo "Cookie 名为 '" . $cookie_name . "' 未设置！";
} else {
    echo "Cookie '" . $cookie_name . "' 已设置!<br>";
    echo "值为: " . $_COOKIE[$cookie_name];
}
?>

</body>
</html>
```

## 删除 Cookie

要删除 Cookie，使用 `setcookie()` 函数并设置一个过去的过期时间：

```php
<?php
// 设置过期时间为一小时前
setcookie("user", "", time() - 3600);
?>
<html>
<body>

<?php
echo "Cookie 'user' 已删除。";
?>

</body>
</html>
```

## 检查 Cookie 是否启用

以下示例创建了一个小型脚本，用于检查 Cookie 是否启用。首先，尝试使用 `setcookie()` 函数创建一个测试 Cookie，然后统计 `$_COOKIE` 数组变量：

```php
<?php
setcookie("test_cookie", "test", time() + 3600, '/');
?>
<html>
<body>

<?php
if(count($_COOKIE) > 0) {
    echo "Cookie 已启用。";
} else {
    echo "Cookie 已禁用。";
}
?>

</body>
</html>
```

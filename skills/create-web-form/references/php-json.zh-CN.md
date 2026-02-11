# PHP JSON 参考

> 来源: <https://www.w3schools.com/php/php_json.asp>

## 什么是 JSON？

JSON 是 **JavaScript 对象表示法**（JavaScript Object Notation）的缩写，是一种用于存储和交换数据的语法。JSON 是一种完全独立于语言的文本格式。由于 JSON 格式是纯文本，因此可以轻松地在服务器之间传输，并且可以被任何编程语言用作数据格式。

PHP 提供了一些内置函数来处理 JSON：

- `json_encode()` -- 将值编码为 JSON 格式
- `json_decode()` -- 将 JSON 字符串解码为 PHP 变量

## `json_encode()` -- 将 PHP 编码为 JSON

`json_encode()` 函数用于将值编码为 JSON 格式（一个有效的 JSON 字符串）。

### 编码关联数组

```php
<?php
$age = array("Peter" => 35, "Ben" => 37, "Joe" => 43);

echo json_encode($age);
?>
```

输出：

```json
{"Peter":35,"Ben":37,"Joe":43}
```

### 编码索引数组

```php
<?php
$cars = array("Volvo", "BMW", "Toyota");

echo json_encode($cars);
?>
```

输出：

```json
["Volvo","BMW","Toyota"]
```

### 编码 PHP 对象

```php
<?php
$myObj = new stdClass();
$myObj->name = "John";
$myObj->age = 30;
$myObj->city = "New York";

echo json_encode($myObj);
?>
```

输出：

```json
{"name":"John","age":30,"city":"New York"}
```

## `json_decode()` -- 将 JSON 解码为 PHP

`json_decode()` 函数用于将 JSON 字符串解码为 PHP 对象或关联数组。

### 语法

```php
json_decode(string, assoc, depth, options)
```

### 参数

| 参数 | 描述 |
|------|------|
| `string` | 必需。指定要解码的 JSON 字符串。 |
| `assoc` | 可选。如果设置为 `true`，则返回的对象将被转换为关联数组。默认值为 `false`。 |
| `depth` | 可选。指定最大递归深度。默认值为 `512`。 |
| `options` | 可选。指定一个位掩码（例如：`JSON_BIGINT_AS_STRING`）。 |

### 将 JSON 解码为 PHP 对象（默认）

默认情况下，`json_decode()` 函数返回一个对象：

```php
<?php
$jsonobj = '{"Peter":35,"Ben":37,"Joe":43}';

$obj = json_decode($jsonobj);

echo $obj->Peter;  // 输出：35
echo $obj->Ben;    // 输出：37
echo $obj->Joe;    // 输出：43
?>
```

### 将 JSON 解码为关联数组

当第二个参数设置为 `true` 时，JSON 字符串将被解码为关联数组：

```php
<?php
$jsonobj = '{"Peter":35,"Ben":37,"Joe":43}';

$arr = json_decode($jsonobj, true);

echo $arr["Peter"];  // 输出：35
echo $arr["Ben"];    // 输出：37
echo $arr["Joe"];    // 输出：43
?>
```

## 访问解码后的值

### 从对象中访问

使用箭头（`->`）运算符来访问解码后的对象的值：

```php
<?php
$jsonobj = '{"Peter":35,"Ben":37,"Joe":43}';

$obj = json_decode($jsonobj);

echo $obj->Peter;
echo $obj->Ben;
echo $obj->Joe;
?>
```

### 从关联数组中访问

使用方括号语法来访问解码后的关联数组的值：

```php
<?php
$jsonobj = '{"Peter":35,"Ben":37,"Joe":43}';

$arr = json_decode($jsonobj, true);

echo $arr["Peter"];
echo $arr["Ben"];
echo $arr["Joe"];
?>
```

## 遍历值

### 遍历对象

使用 `foreach` 循环来遍历解码后的对象的值：

```php
<?php
$jsonobj = '{"Peter":35,"Ben":37,"Joe":43}';

$obj = json_decode($jsonobj);

foreach($obj as $key => $value) {
    echo $key . " => " . $value . "<br>";
}
?>
```

输出：

```
Peter => 35
Ben => 37
Joe => 43
```

### 遍历关联数组

使用 `foreach` 循环来遍历解码后的关联数组的值：

```php
<?php
$jsonobj = '{"Peter":35,"Ben":37,"Joe":43}';

$arr = json_decode($jsonobj, true);

foreach($arr as $key => $value) {
    echo $key . " => " . $value . "<br>";
}
?>
```

输出：

```
Peter => 35
Ben => 37
Joe => 43
```

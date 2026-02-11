# PHP MySQL 数据库参考

用于在 PHP 中操作 MySQL 数据库的综合参考指南，涵盖连接、CRUD 操作、预处理语句和查询技术。

---

## 目录

1. [MySQL 简介](#1-mysql-introduction)
2. [连接 MySQL](#2-connect-to-mysql)
3. [创建数据库](#3-create-a-database)
4. [创建表](#4-create-a-table)
5. [插入数据](#5-insert-data)
6. [获取最后插入的 ID](#6-get-last-inserted-id)
7. [插入多条记录](#7-insert-multiple-records)
8. [预处理语句](#8-prepared-statements)
9. [选择数据](#9-select-data)
10. [带 WHERE 子句的选择](#10-select-with-where)
11. [带 ORDER BY 子句的选择](#11-select-with-order-by)
12. [删除数据](#12-delete-data)
13. [更新数据](#13-update-data)
14. [带 LIMIT 子句的选择](#14-select-with-limit)

---

## 1. MySQL 简介

> **来源:** <https://www.w3schools.com/php/php_mysql_intro.asp>

### 什么是 MySQL？

MySQL 是最流行的开源关系型数据库管理系统。与 PHP 一起使用时，MySQL 用于创建动态、数据驱动的 Web 应用程序。

### 重点内容

- **MySQL** 是用于网络的数据库系统。
- **MySQL** 运行在服务器上（通常与 Web 服务器如 Apache 一起运行）。
- 它非常适合小型和大型应用程序。
- 它非常快速、可靠且易于使用。
- 它使用标准的 **SQL**（结构化查询语言）。
- 它可以免费下载和使用。
- MySQL 由 Oracle 公司开发、分发和支持。

### MySQL 中的数据

- MySQL 中的数据存储在 **表** 中。
- 一个表是由 **列** 和 **行** 组成的相关数据集合。
- 数据库对于按类别存储信息非常有用。例如，公司可能有用于员工、产品和客户的数据库。

### PHP + MySQL 数据库系统

- PHP 与 MySQL 是跨平台的（可在 Windows、Linux、macOS 等上运行）。
- 查询 MySQL 数据库的 PHP 代码在服务器上执行，HTML 结果发送到浏览器。

### PHP MySQL 接口

PHP 提供了三种方式来连接和操作 MySQL：

| 接口 | 描述 |
|-----|-------------|
| **MySQLi（面向对象）** | MySQL 改进扩展 - 面向对象接口 |
| **MySQLi（过程化）** | MySQL 改进扩展 - 过程化接口 |
| **PDO（PHP 数据对象）** | 可用于 12 种不同的数据库系统 |

**推荐:** 使用 **MySQLi** 或 **PDO**。旧版的 `mysql_*` 函数在 PHP 7.0 中已被弃用并移除。

**MySQLi 与 PDO 的区别:**

- **PDO** 可用于 12 种不同的数据库系统；**MySQLi** 仅适用于 MySQL。
- 如果需要将项目切换到其他数据库，PDO 会更容易实现——只需更改连接字符串和少量查询即可。
- 两者都支持 **预处理语句**，可防止 SQL 注入。

---

## 2. 连接到 MySQL

> **来源:** <https://www.w3schools.com/php/php_mysql_connect.asp>

### 打开到 MySQL 的连接

在访问 MySQL 数据库中的数据之前，需要连接到服务器。

### MySQLi 面向对象连接

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";

// 创建连接
$conn = new mysqli($servername, $username, $password);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}
echo "连接成功";
?>
```

### MySQLi 过程化连接

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";

// 创建连接
$conn = mysqli_connect($servername, $username, $password);

// 检查连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}
echo "连接成功";
?>
```

### PDO 连接

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";

try {
    $conn = new PDO("mysql:host=$servername", $username, $password);
    // 设置 PDO 错误模式为异常
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "连接成功";
} catch(PDOException $e) {
    echo "连接失败: " . $e->getMessage();
}
?>
```

**注意:** 在 PDO 示例中，指定了一个数据库（`myDB`）。PDO 需要有效的数据库才能连接。如果没有指定数据库，会抛出异常。

### 关闭连接

脚本结束时会自动关闭连接。若需提前关闭：

```php
// MySQLi 面向对象
$conn->close();

// MySQLi 过程化
mysqli_close($conn);

// PDO
$conn = null;
```

---

## 3. 创建数据库

> **来源:** <https://www.w3schools.com/php/php_mysql_create.asp>

`CREATE DATABASE` 语句用于在 MySQL 中创建数据库。

### MySQLi 面向对象

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";

// 创建连接
$conn = new mysqli($servername, $username, $password);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 创建数据库
$sql = "CREATE DATABASE myDB";
if ($conn->query($sql) === TRUE) {
    echo "数据库创建成功";
} else {
    echo "创建数据库时出错: " . $conn->error;
}

$conn->close();
?>
```

### MySQLi 过程化

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";

// 创建连接
$conn = mysqli_connect($servername, $username, $password);

// 检查连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}

// 创建数据库
$sql = "CREATE DATABASE myDB";
if (mysqli_query($conn, $sql)) {
    echo "数据库创建成功";
} else {
    echo "创建数据库时出错: " . mysqli_error($conn);
}

mysqli_close($conn);
?>
```

### PDO 连接

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";

try {
    $conn = new PDO("mysql:host=$servername", $username, $password);
    // 设置 PDO 错误模式为异常
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $sql = "CREATE DATABASE myDBPDO";
    // 使用 exec() 因为没有返回结果
    $conn->exec($sql);
    echo "数据库创建成功";
} catch(PDOException $e) {
    echo $sql . "<br>" . $e->getMessage();
}

$conn = null;
?>
```

**提示:** 在创建数据库时，只需指定 `mysqli` 对象的前三个参数（服务器名、用户名和密码）。要选择特定数据库，需添加第四个参数。

---

## 4. 创建表

> **来源:** <https://www.w3schools.com/php/php_mysql_create_table.asp>

`CREATE TABLE` 语句用于在 MySQL 中创建表。

### 表创建的关键 SQL 概念

- **NOT NULL** - 每一行必须包含该列的值；不允许空值。
- **DEFAULT 值** - 当未提供其他值时，设置默认值。
- **UNSIGNED** - 用于数字类型，限制存储数据为正数和零。
- **AUTO_INCREMENT** - MySQL 会自动每次新增记录时将该字段的值增加 1。
- **PRIMARY KEY** - 用于唯一标识表中的行。带有 PRIMARY KEY 设置的列通常是 ID 号，并与 `AUTO_INCREMENT` 一起使用。

### MySQLi 面向对象

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 创建表的 SQL
$sql = "CREATE TABLE MyGuests (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(30) NOT NULL,
    lastname VARCHAR(30) NOT NULL,
    email VARCHAR(50),
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)";

if ($conn->query($sql) === TRUE) {
    echo "MyGuests 表创建成功";
} else {
    echo "创建表时出错: " . $conn->error;
}

$conn->close();
?>
```

### MySQLi 过程化

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);

// 检查连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}

// 创建表的 SQL
$sql = "CREATE TABLE MyGuests (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(30) NOT NULL,
    lastname VARCHAR(30) NOT NULL,
    email VARCHAR(50),
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)";

if (mysqli_query($conn, $sql)) {
    echo "MyGuests 表创建成功";
} else {
    echo "创建表时出错: " . mysqli_error($conn);
}

mysqli_close($conn);
?>
```

### PDO 连接

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDBPDO";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // 设置 PDO 错误模式为异常
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $sql = "CREATE TABLE MyGuests (
        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        firstname VARCHAR(30) NOT NULL,
        lastname VARCHAR(30) NOT NULL,
        email VARCHAR(50),
        reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )";

    // 使用 exec() 因为没有返回结果
    $conn->exec($sql);
    echo "MyGuests 表创建成功";
} catch(PDOException $e) {
    echo $sql . "<br>" . $e->getMessage();
}

$conn = null;
?>
```

**关键方法:**

- `$result->num_rows` -- 返回结果集中的行数（MySQLi 面向对象）。
- `$result->fetch_assoc()` -- 将结果行作为关联数组获取（MySQLi 面向对象）。
- `$stmt->fetchAll(PDO::FETCH_ASSOC)` -- 返回所有行的数组（PDO）。

---

## 5. 插入数据

> **来源:** <https://www.w3schools.com/php/php_mysql_insert.asp>

`INSERT INTO` 语句用于向 MySQL 表中添加新记录。

### SQL 语法

```sql
INSERT INTO table_name (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...)
```

**重要规则:**

- SQL 查询必须在 PHP 中被引号包围。
- SQL 查询中的字符串值必须被引号包围。
- 数值类型不需要引号。
- `NULL` 不需要被引号包围。

### MySQLi 面向对象

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

$sql = "INSERT INTO MyGuests (firstname, lastname, email)
VALUES ('John', 'Doe', 'john@example.com')";

if ($conn->query($sql) === TRUE) {
    echo "新记录创建成功";
} else {
    echo "创建记录时出错: " . $conn->error;
}

$conn->close();
?>
```

### MySQLi 过程化

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);

// 检查连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}

$sql = "INSERT INTO MyGuests (firstname, lastname, email)
VALUES ('John', 'Doe', 'john@example.com')";

if (mysqli_query($conn, $sql)) {
    echo "新记录创建成功";
} else {
    echo "创建记录时出错: " . mysqli_error($conn);
}

mysqli_close($conn);
?>
```

### PDO（带预处理语句）

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDBPDO";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // 设置 PDO 错误模式为异常
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $sql = "INSERT INTO MyGuests (firstname, lastname, email)
    VALUES ('John', 'Doe', 'john@example.com')";
    // 使用 exec() 因为没有返回结果
    $conn->exec($sql);
    echo "新记录创建成功";
} catch(PDOException $e) {
    echo "错误: " . $e->getMessage();
}

$conn = null;
?>
```

**注意:** 因为 `id` 是 `AUTO_INCREMENT`，`reg_date` 有默认值 `CURRENT_TIMESTAMP`，所以不需要指定它们的值。

---

## 6. 获取最后插入的 ID

> **来源:** <https://www.w3schools.com/php/php_mysql_insert_lastid.asp>

如果在具有 `AUTO_INCREMENT` 列的表上执行 `INSERT`，可以立即获取最后插入行的 ID。

### MySQLi 面向对象

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

$sql = "INSERT INTO MyGuests (firstname, lastname, email)
VALUES ('John', 'Doe', 'john@example.com')";

if ($conn->query($sql) === TRUE) {
    $last_id = $conn->insert_id;
    echo "新记录创建成功。最后插入的 ID 是: " . $last_id;
} else {
    echo "错误: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
```

### MySQLi 过程化

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);

// 检查连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}

$sql = "INSERT INTO MyGuests (firstname, lastname, email)
VALUES ('John', 'Doe', 'john@example.com')";

if (mysqli_query($conn, $sql)) {
    $last_id = mysqli_insert_id($conn);
    echo "新记录创建成功。最后插入的 ID 是: " . $last_id;
} else {
    echo "错误: " . $sql . "<br>" . mysqli_error($conn);
}

mysqli_close($conn);
?>
```

### PDO（带预处理语句）

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDBPDO";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // 设置 PDO 错误模式为异常
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $sql = "INSERT INTO MyGuests (firstname, lastname, email)
    VALUES (:firstname, :lastname, :email)";
    // 使用 exec() 因为没有返回结果
    $conn->exec($sql);
    $last_id = $conn->lastInsertId();
    echo "新记录创建成功。最后插入的 ID 是: " . $last_id;
} catch(PDOException $e) {
    echo "错误: " . $e->getMessage();
}

$conn = null;
?>
```

**关键方法:**

- MySQLi 面向对象: `$conn->insert_id`
- MySQLi 过程化: `mysqli_insert_id($conn)`
- PDO: `$conn->lastInsertId()`

---

## 7. 插入多条记录

> **来源:** <https://www.w3schools.com/php/php_mysql_insert_multiple.asp>

可以使用 `multi_query()` 方法（MySQLi）或分组值（PDO）执行多个 SQL 语句。

### MySQLi 面向对象（multi_query）

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

$sql = "INSERT INTO MyGuests (firstname, lastname, email)
VALUES ('John', 'Doe', 'john@example.com');";
$sql .= "INSERT INTO MyGuests (firstname, lastname, email)
VALUES ('Mary', 'Moe', 'mary@example.com');";
$sql .= "INSERT INTO MyGuests (firstname, lastname, email)
VALUES ('Julie', 'Dooley', 'julie@example.com')";

if ($conn->multi_query($sql) === TRUE) {
    echo "新记录创建成功";
} else {
    echo "错误: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
```

### MySQLi 过程化（multi_query）

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);

// 检查连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}

$sql = "INSERT INTO MyGuests (firstname, lastname, email)
VALUES ('John', 'Doe', 'john@example.com');";
$sql .= "INSERT INTO MyGuests (firstname, lastname, email)
VALUES ('Mary', 'Moe', 'mary@example.com');";
$sql .= "INSERT INTO MyGuests (firstname, lastname, email)
VALUES ('Julie', 'Dooley', 'julie@example.com')";

if (mysqli_multi_query($conn, $sql)) {
    echo "新记录创建成功";
} else {
    echo "错误: " . $sql . "<br>" . mysqli_error($conn);
}

mysqli_close($conn);
?>
```

### PDO（使用预处理语句进行多条插入）

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDBPDO";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // 设置 PDO 错误模式为异常
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $stmt = $conn->prepare("INSERT INTO MyGuests (firstname, lastname, email)
    VALUES (:firstname, :lastname, :email)");

    // 插入第一行
    $stmt->execute([
        ':firstname' => 'John',
        ':lastname' => 'Doe',
        ':email' => 'john@example.com'
    ]);

    // 插入第二行
    $stmt->execute([
        ':firstname' => 'Mary',
        ':lastname' => 'Moe',
        ':email' => 'mary@example.com'
    ]);

    // 插入第三行
    $stmt->execute([
        ':firstname' => 'Julie',
        ':lastname' => 'Dooley',
        ':email' => 'julie@example.com'
    ]);

    echo "新记录创建成功";
} catch(PDOException $e) {
    echo "错误: " . $e->getMessage();
}

$conn = null;
?>
```

**注意:** 在 PDO 的预处理语句中使用 `LIMIT` 时，必须显式使用 `PDO::PARAM_INT` 绑定值为整数，否则 PDO 会将它们视为字符串并加上引号，导致 SQL 错误。

---

## 8. 预处理语句

> **来源:** <https://www.w3schools.com/php/php_mysql_prepared_statements.asp>

预处理语句对于防止 **SQL 注入** 非常有用。它们是执行带有用户输入数据的查询的推荐方法。

### 什么是预处理语句？

预处理语句是一种用于高效重复执行相同（或类似的）SQL 语句的功能。它们分为两个阶段：

1. **预处理:** 创建 SQL 语句模板并发送到数据库。某些值未指定，称为 **参数**（标记为 `?` 或 `:name`）。例如：`INSERT INTO MyGuests VALUES(?, ?, ?)`
2. **执行:** 数据库解析、编译并优化 SQL 语句模板，存储结果而不执行它。应用程序将特定值绑定到参数并执行语句。语句可以多次执行，每次使用不同的值。

### 预处理语句的优势

- **减少解析时间:** 即使执行多次，查询也只需预处理一次。
- **减少带宽:** 每次只需发送参数，而不是整个查询。
- **防止 SQL 注入:** 参数值通过不同的协议传输，无需转义。如果原始语句模板不来自外部输入，SQL 注入无法发生。

---

## 9. 选择数据

> **来源:** <https://www.w3schools.com/php/php_mysql_select.asp>

`SELECT` 语句用于从一个或多个表中选择数据。

### SQL 语法

```sql
SELECT column_name(s) FROM table_name

-- 或选择所有列：
SELECT * FROM table_name
```

### MySQLi 面向对象

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

$sql = "SELECT id, firstname, lastname FROM MyGuests";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // 输出每一行的数据
    while($row = $result->fetch_assoc()) {
        echo "id: " . $row["id"] . " - 姓名: " . $row["firstname"] . " " . $row["lastname"] . "<br>";
    }
} else {
    echo "0 条记录";
}

$conn->close();
?>
```

### MySQLi 过程化

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);

// 检查连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}

$sql = "SELECT id, firstname, lastname FROM MyGuests";
$result = mysqli_query($conn, $sql);

if (mysqli_num_rows($result) > 0) {
    // 输出每一行的数据
    while($row = mysqli_fetch_assoc($result)) {
        echo "id: " . $row["id"] . " - 姓名: " . $row["firstname"] . " " . $row["lastname"] . "<br>";
    }
} else {
    echo "0 条记录";
}

mysqli_close($conn);
?>
```

### PDO（带预处理语句）

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDBPDO";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // 设置 PDO 错误模式为异常
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $stmt = $conn->prepare("SELECT id, firstname, lastname FROM MyGuests");
    $stmt->execute();

    // 将结果集设置为关联数组
    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach(new TableRows(new RecursiveArrayIterator($stmt->fetchAll())) as $k => $v) {
        echo $v;
    }
} catch(PDOException $e) {
    echo "错误: " . $e->getMessage();
}

$conn = null;
?>
```

**更简单的 PDO 查询:**

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDBPDO";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $conn->prepare("SELECT id, firstname, lastname FROM MyGuests");
    $stmt->execute();

    // 获取所有结果为关联数组
    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($results as $row) {
        echo "id: " . $row["id"] . " - 姓名: " . $row["firstname"] . " " . $row["lastname"] . "<br>";
    }
} catch(PDOException $e) {
    echo "错误: " . $e->getMessage();
}

$conn = null;
?>
```

**重要提示:** 使用 PDO 的预处理语句时，若使用 `LIMIT`，必须显式绑定值为整数，否则 PDO 会将其视为字符串并加上引号，导致 SQL 错误。

---

## 10. 带 WHERE 的选择

> **来源:** <https://www.w3schools.com/php/php_mysql_select_where.asp>

`WHERE` 子句用于筛选记录，提取满足特定条件的记录。

### SQL 语法

```sql
SELECT column_name(s) FROM table_name WHERE column_name operator value
```

### MySQLi 面向对象

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

$sql = "SELECT id, firstname, lastname FROM MyGuests WHERE lastname='Doe'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // 输出每一行的数据
    while($row = $result->fetch_assoc()) {
        echo "id: " . $row["id"] . " - 姓名: " . $row["firstname"] . " " . $row["lastname"] . "<br>";
    }
} else {
    echo "0 条记录";
}

$conn->close();
?>
```

### MySQLi 过程化

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);

// 检查连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}

$sql = "SELECT id, firstname, lastname FROM MyGuests WHERE lastname='Doe'";
$result = mysqli_query($conn, $sql);

if (mysqli_num_rows($result) > 0) {
    while($row = mysqli_fetch_assoc($result)) {
        echo "id: " . $row["id"] . " - 姓名: " . $row["firstname"] . " " . $row["lastname"] . "<br>";
    }
} else {
    echo "0 条记录";
}

mysqli_close($conn);
?>
```

### PDO（带预处理语句）

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDBPDO";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // 设置 PDO 错误模式为异常
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $conn->prepare("SELECT id, firstname, lastname FROM MyGuests WHERE lastname = :lastname");
    $stmt->bindParam(':lastname', $lastname);

    $lastname = "Doe";
    $stmt->execute();

    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);
    foreach ($results as $row) {
        echo "id: " . $row["id"] . " - 姓名: " . $row["firstname"] . " " . $row["lastname"] . "<br>";
    }
} catch(PDOException $e) {
    echo "错误: " . $e->getMessage();
}

$conn = null;
?>
```

**常用 WHERE 运算符:**

| 运算符 | 描述 |
|----------|-------------|
| `=` | 等于 |
| `<>` 或 `!=` | 不等于 |
| `>` | 大于 |
| `<` | 小于 |
| `>=` | 大于等于 |
| `<=` | 小于等于 |
| `BETWEEN` | 在一个包含范围内 |
| `LIKE` | 搜索模式 |
| `IN` | 指定列的多个可能值 |

**重要提示:** 在使用用户提供的值进行 WHERE 子句查询时，始终使用带有绑定参数的预处理语句以防止 SQL 注入。

---

## 11. 带 ORDER BY 的选择

> **来源:** <https://www.w3schools.com/php/php_mysql_select_orderby.asp>

`ORDER BY` 子句用于按升序或降序对结果集进行排序。默认情况下，它按 **升序** 排序。使用 `DESC` 关键字进行降序排序。

### SQL 语法

```sql
SELECT column_name(s) FROM table_name ORDER BY column_name ASC|DESC
```

### MySQLi 面向对象

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

$sql = "SELECT id, firstname, lastname FROM MyGuests ORDER BY lastname";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // 输出每一行的数据
    while($row = $result->fetch_assoc()) {
        echo "id: " . $row["id"] . " - 姓名: " . $row["firstname"] . " " . $row["lastname"] . "<br>";
    }
} else {
    echo "0 条记录";
}

$conn->close();
?>
```

### 降序排序示例

```php
$sql = "SELECT id, firstname, lastname FROM MyGuests ORDER BY lastname DESC";
```

### 多列排序

可以按多列排序。当第一列的值相同时，第二列才会被使用：

```sql
SELECT * FROM MyGuests ORDER BY lastname ASC, firstname ASC
```

---

## 12. 删除数据

> **来源:** <https://www.w3schools.com/php/php_mysql_delete.asp>

`DELETE` 语句用于从表中删除记录。

### SQL 语法

```sql
DELETE FROM table_name WHERE some_column = some_value
```

**重要提示:** `WHERE` 子句用于指定要删除的记录。如果省略 `WHERE` 子句，**所有记录都会被删除！**

### MySQLi 面向对象

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 删除记录的 SQL
$sql = "DELETE FROM MyGuests WHERE id=3";

if ($conn->query($sql) === TRUE) {
    echo "记录删除成功";
} else {
    echo "删除记录时出错: " . $conn->error;
}

$conn->close();
?>
```

### MySQLi 过程化

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);

// 检查连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}

// 删除记录的 SQL
$sql = "DELETE FROM MyGuests WHERE id=3";

if (mysqli_query($conn, $sql)) {
    echo "记录删除成功";
} else {
    echo "删除记录时出错: " . mysqli_error($conn);
}

mysqli_close($conn);
?>
```

### PDO（带预处理语句）

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDBPDO";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // 设置 PDO 错误模式为异常
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $conn->prepare("DELETE FROM MyGuests WHERE id = :id");
    $stmt->bindParam(':id', $id);

    $id = 3;
    $stmt->execute();

    echo "记录删除成功";
} catch(PDOException $e) {
    // 如果发生错误，回滚事务
    $conn->rollBack();
    echo "错误: " . $e->getMessage();
}

$conn = null;
?>
```

**警告:** 删除记录时要非常小心。此语句无法撤销！

---

## 13. 更新数据

> **来源:** <https://www.w3schools.com/php/php_mysql_update.asp>

`UPDATE` 语句用于更新表中的现有记录。

### SQL 语法

```sql
UPDATE table_name SET column1=value1, column2=value2, ... WHERE some_column=some_value
```

**重要提示:** `WHERE` 子句用于指定要更新的记录。如果省略 `WHERE` 子句，**所有记录都会被更新！**

### MySQLi 面向对象

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

$sql = "UPDATE MyGuests SET lastname='Doe' WHERE id=2";

if ($conn->query($sql) === TRUE) {
    echo "记录更新成功";
} else {
    echo "更新记录时出错: " . $conn->error;
}

$conn->close();
?>
```

### MySQLi 过程化

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);

// 检查连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}

$sql = "UPDATE MyGuests SET lastname='Doe' WHERE id=2";

if (mysqli_query($conn, $sql)) {
    echo "记录更新成功";
} else {
    echo "更新记录时出错: " . mysqli_error($conn);
}

mysqli_close($conn);
?>
```

### PDO（带预处理语句）

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "my

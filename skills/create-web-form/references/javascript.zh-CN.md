# JavaScript 参考手册

涵盖 JavaScript 基础知识、高级特性、DOM 操作、网络请求以及现代框架的全面参考。内容整合自 MDN Web 文档和其他教育资源。

---

## 目录

1. [JavaScript 是什么？](#what-is-javascript)
2. [如何将 JavaScript 添加到页面](#adding-javascript-to-a-page)
3. [脚本加载策略](#script-loading-strategies)
4. [注释](#comments)
5. [变量](#variables)
6. [数字与数学](#numbers-and-math)
7. [字符串](#strings)
8. [有用的字符串方法](#useful-string-methods)
9. [数组](#arrays)
10. [条件语句](#conditionals)
11. [循环](#loops)
12. [函数](#functions)
13. [构建自定义函数](#building-custom-functions)
14. [函数返回值](#function-return-values)
15. [事件](#events)
16. [对象基础](#object-basics)
17. [DOM 脚本](#dom-scripting)
18. [网络请求](#network-requests)
19. [与 JSON 交互](#working-with-json)
20. [JavaScript 框架：主要特性](#javascript-frameworks-main-features)
21. [React 入门](#getting-started-with-react)
22. [React 组件](#react-components)

---

## JavaScript 是什么？

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/What_is_JavaScript](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/What_is_JavaScript)

JavaScript 是一种脚本语言或编程语言，允许你在网页上实现复杂功能。它能够动态更新内容、创建交互式地图、动画图形、滚动视频播放器等。

### 网络技术的三个层次

JavaScript 是标准网络技术的第三层：

- **HTML**：用于结构化和赋予网页内容意义的标记语言
- **CSS**：用于对 HTML 内容应用样式规则的语言
- **JavaScript**：创建动态更新内容、控制多媒体和动画图像的脚本语言

### JavaScript 能做什么？

核心 JavaScript 功能允许你：

- **在变量中存储有用的值**
- **对文本（字符串）执行操作** —— 合并和操作文本
- **在事件发生时运行代码** —— 检测用户交互，如点击、键盘输入等
- **通过 DOM（文档对象模型）访问和操作 HTML 和 CSS**

### 实用示例

```html
<button>Player 1: Chris</button>
```

```javascript
function updateName() {
  const name = prompt("请输入新名字");
  button.textContent = `Player 1: ${name}`;
}

const button = document.querySelector("button");
button.addEventListener("click", updateName);
```

### 浏览器 API

应用程序编程接口（API）提供现成的代码模块，使你能够实现强大的功能：

| API | 描述 |
|-----|-------------|
| **DOM API** | 动态操作 HTML 和 CSS；创建、删除和更改 HTML 元素 |
| **地理定位 API** | 获取地理信息 |
| **Canvas 和 WebGL API** | 创建动画 2D 和 3D 图形 |
| **音频和视频 API** | 在网页上播放音频和视频；从网络摄像头捕获视频 |

### 第三方 API

这些 API 不默认内置在浏览器中，需要从网络获取代码：

- **Google Maps API**：将自定义地图嵌入网站
- **OpenStreetMap API**：添加地图功能
- **社交媒体 API**：在你的网站上显示帖子

### JavaScript 的运行方式

- JavaScript 从上到下按顺序运行
- 每个浏览器标签页都有独立的执行环境
- **JavaScript 是解释执行的**（尽管现代解释器使用即时编译以提高性能）
- **客户端 JavaScript** 在用户的计算机上浏览器中运行
- **服务端 JavaScript** 在服务器上运行（例如 Node.js 环境）
- **动态代码** 根据情况更新显示；**静态代码** 始终显示相同内容

---

## 如何将 JavaScript 添加到页面

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/What_is_JavaScript](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/What_is_JavaScript)

### 1. 内部 JavaScript

在 HTML 文件中使用 `<script>` 标签直接添加 JavaScript：

```html
<body>
  <button>点击我！</button>

  <script>
    function createParagraph() {
      const para = document.createElement("p");
      para.textContent = "你点击了按钮！";
      document.body.appendChild(para);
    }

    const buttons = document.querySelectorAll("button");
    for (const button of buttons) {
      button.addEventListener("click", createParagraph);
    }
  </script>
</body>
```

### 2. 外部 JavaScript（推荐）

将 JavaScript 存储在单独的文件中，以提高组织性和可重用性：

**HTML 文件：**

```html
<script type="module" src="script.js"></script>
```

**script.js 文件：**

```javascript
function createParagraph() {
  const para = document.createElement("p");
  para.textContent = "你点击了按钮！";
  document.body.appendChild(para);
}

const buttons = document.querySelectorAll("button");
for (const button of buttons) {
  button.addEventListener("click", createParagraph);
}
```

### 3. 内联 JavaScript 处理器（不推荐）

```html
<button onclick="createParagraph()">点击我！</button>
```

避免使用内联处理器，因为它们会污染 HTML，效率低下且难以维护。

### 对比

| 方法 | 位置 | 最适合 | 优点 | 缺点 |
|--------|----------|----------|------|------|
| **内部** | `<script>` 在 body 中 | 小型项目 | 简单、自包含 | 不可重用 |
| **外部** | `<script src="">` | 大多数项目 | 可重用、组织良好 | 需要 HTTP 服务器 |
| **内联** | `onclick=""` | 不推荐 | 快速测试 | 难以维护、污染 HTML |
| **模块** | `<script type="module">` | 现代项目 | 安全定时、组织良好 | 需要 HTTP 服务器 |

---

## 脚本加载策略

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/What_is_JavaScript](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/What_is_JavaScript)

### 将 `<script>` 放在 body 底部

```html
<body>
  <h1>我的页面</h1>
  <p>内容在此</p>
  <script src="script.js"></script>
</body>
```

### 在 `<head>` 中使用 `<script type="module">`（推荐）

```html
<head>
  <script type="module" src="script.js"></script>
</head>
```

浏览器会在处理完所有 HTML 后才执行脚本。

### 使用 `defer` 属性

```html
<head>
  <script defer src="script.js"></script>
</head>
```

脚本并行下载，同时 HTML 继续解析；仅在 HTML 完全解析后执行。带有 `defer` 的脚本按顺序执行。

### 使用 `async` 属性（适用于非依赖脚本）

```html
<script async src="analytics.js"></script>
```

脚本并行下载并在准备好时立即执行。不保证执行顺序。仅用于不依赖 DOM 元素的脚本。

### 将内部脚本包裹在 `DOMContentLoaded`

```javascript
document.addEventListener('DOMContentLoaded', function() {
  const button = document.querySelector("button");
  button.addEventListener("click", updateName);
});
```

---

## 注释

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/What_is_JavaScript](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/What_is_JavaScript)

### 单行注释

```javascript
// 这是一个单行注释
const name = "Chris"; // 也可以放在行尾
```

### 多行注释

```javascript
/*
  这是一个多行注释。
  它可以跨越多行。
  适用于较长的解释。
*/
```

### 最佳实践

- 使用注释解释**为什么**代码执行某些操作，而不是**做什么**
- 变量名应直观 —— 不要注释显而易见的操作
- 通常越多注释越好，但避免过度注释
- 随着代码变化，保持注释更新

---

## 变量

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Variables](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Variables)

变量是一个**存储值的容器**，比如数字或字符串。变量是必需的，因为它们允许你的代码记住和操作数据。

### 声明变量

使用 **`let`** 关键字创建变量：

```javascript
let myName;
let myAge;
```

声明后，变量存在但没有值（`undefined`）。

### 初始化变量

使用等号 (`=`) 分配值：

```javascript
myName = "Chris";
myAge = 37;
```

或者声明和初始化一起：

```javascript
let myDog = "Rover";
```

### 变量类型

**数字：**

```javascript
let myAge = 17;           // 整数
let temperature = 98.6;   // 浮点数
```

**字符串：**

```javascript
let dolphinGoodbye = "So long and thanks for all the fish";
```

**布尔值：**

```javascript
let iAmAlive = true;
let test = 6 < 3;  // 返回 false
```

**数组：**

```javascript
let myNameArray = ["Chris", "Bob", "Jim"];
let myNumberArray = [10, 15, 40];
myNameArray[0];    // "Chris"（零索引）
myNumberArray[2];  // 40
```

**对象：**

```javascript
let dog = { name: "Spot", breed: "Dalmatian" };
dog.name;  // "Spot"
```

### 变量命名规则

- 仅使用拉丁字符（0-9, a-z, A-Z）和下划线
- 使用**小驼峰命名法**：`myAge`, `initialColor`, `finalOutputValue`
- 命名应直观且描述性
- 变量是区分大小写的：`myage` 不同于 `myAge`
- 不以下划线或数字开头
- 不使用保留关键字（`var`, `function`, `let` 等）

### 动态类型

JavaScript 是**动态类型**的 —— 你不需要声明变量类型。变量的类型由分配的值决定：

```javascript
let myString = "Hello";
typeof myString;           // "string"

let myNumber = "500";
typeof myNumber;           // "string"

myNumber = 500;
typeof myNumber;           // "number"
```

### 使用 `const` 定义常量

使用 **`const`** 对不应改变的值：

```javascript
const myDog = "Rover";
myDog = "Fido";  // 错误：不能重新赋值
```

对于对象，即使使用 `const` 仍可以修改属性：

```javascript
const bird = { species: "Kestrel" };
bird.species = "Striated Caracara";  // 可以修改内容
```

### `let` vs `const` vs `var`

| 特性 | `let` | `const` | `var` |
|---------|-------|---------|-------|
| 可重新赋值 | 是 | 否 | 是 |
| 必须初始化 | 否 | 是 | 否 |
| 作用域 | 块级 | 块级 | 函数级 |
| 提升问题 | 否 | 否 | 是 |

**最佳实践**：尽可能使用 `const`，需要重新赋值时使用 `let`。避免在现代 JavaScript 中使用 `var`。

---

## 数字与数学

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Math](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Math)

### 数字类型

- **整数**：没有小数部分的数字（例如 10, 400, -5）
- **浮点数（浮点数）**：带有小数点（例如 12.5, 56.7786543）
- JavaScript 只有一种数字数据类型：`Number`（加上 `BigInt` 用于非常大的整数）

### 算术运算符

| 运算符 | 名称 | 示例 | 结果 |
|----------|------|---------|--------|
| `+` | 加法 | `6 + 9` | `15` |
| `-` | 减法 | `20 - 15` | `5` |
| `*` | 乘法 | `3 * 7` | `21` |
| `/` | 除法 | `10 / 5` | `2` |
| `%` | 取余（模运算） | `8 % 3` | `2` |
| `**` | 指数 | `5 ** 2` | `25` |

```javascript
const num1 = 10;
const num2 = 50;
9 * num1;      // 90
num1 ** 3;     // 1000
num2 / num1;   // 5
```

### 运算符优先级

1. **乘法和除法** 优先执行（从左到右）
2. **加法和减法** 在之后执行（从左到右）

```javascript
num2 + num1 / 8 + 2;        // = 53.25  (50 + 1.25 + 2)
(num2 + num1) / (8 + 2);    // = 6      (60 / 10)
```

### 自增和自减运算符

```javascript
let num1 = 4;
num1++;     // 返回 4，然后递增为 5
++num1;     // 递增后返回 6

let num2 = 6;
num2--;     // 返回 6，然后递减为 5
--num2;     // 递减后返回 4
```

### 赋值运算符

| 运算符 | 示例 | 等价表达式 |
|----------|---------|------------|
| `+=` | `x += 4;` | `x = x + 4;` |
| `-=` | `x -= 3;` | `x = x - 3;` |
| `*=` | `x *= 3;` | `x = x * 3;` |
| `/=` | `x /= 5;` | `x = x / 5;` |

### 比较运算符

| 运算符 | 名称 | 示例 | 结果 |
|----------|------|---------|--------|
| `===` | 严格相等 | `5 === 2 + 3` | `true` |
| `!==` | 严格不相等 | `5 !== 2 + 3` | `false` |
| `<` | 小于 | `10 < 6` | `false` |
| `>` | 大于 | `10 > 20` | `false` |
| `<=` | 小于等于 | `3 <= 2` | `false` |
| `>=` | 大于等于 | `5 >= 4` | `true` |

始终使用 `===` 和 `!==`（严格版本），而不是 `==` 和 `!=`。

### 有用的数字方法

```javascript
// 四舍五入到小数位
const lotsOfDecimal = 1.7665849587;
lotsOfDecimal.toFixed(2);  // "1.77"

// 将字符串转换为数字
let myNumber = "74";
myNumber = Number(myNumber) + 3;  // 77

// 检查数据类型
typeof 5;      // "number"
typeof 6.667;  // "number"

// Math 对象方法
Math.random();           // 0 到 1 之间的随机数
Math.floor(2.9);         // 2（向下取整）
Math.ceil(2.1);          // 3（向上取整）
Math.pow(5, 2);          // 25（5 的平方）
```

---

## 字符串

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Strings](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Strings)

### 创建字符串

字符串必须用引号包围：

```javascript
const single = '单引号';
const double = "双引号";
const backtick = `反引号`;
```

字符串的开始和结束必须使用相同的字符。

### 模板字面量

模板字面量（反引号包裹的字符串）有两个特殊功能：

**1. 嵌入 JavaScript 表达式：**

```javascript
const name = "Chris";
const greeting = `Hello, ${name}`;
console.log(greeting); // "Hello, Chris"

const song = "Fight the Youth";
const score = 9;
const highestScore = 10;
const output = `I like the song ${song}. I gave it a score of ${
  (score / highestScore) * 100
}%.`;
// "I like the song Fight the Youth. I gave it a score of 90%."
```

**2. 多行字符串：**

```javascript
const newline = `有一天你终于知道
你必须做什么，然后开始，`;
```

使用普通字符串时，使用 `\n` 表示换行：

```javascript
const newline2 = "有一天你终于知道\n你必须做什么，然后开始，";
```

### 字符串连接

```javascript
// 使用 + 运算符
const greeting = "Hello" + ", " + "Bob";  // "Hello, Bob"

// 使用模板字面量（推荐）
const name = "Ramesh";
console.log(`Howdy, ${name}`);  // "Howdy, Ramesh"
```

### 转义字符

```javascript
const bigmouth = 'I\'ve got no right to take my place...';
```

---

## 有用的字符串方法

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Useful_string_methods](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Useful_string_methods)

### 获取字符串长度

```javascript
const browserType = "mozilla";
browserType.length;  // 7
```

### 获取字符

```javascript
browserType[0];                          // "m"（第一个字符）
browserType[browserType.length - 1];     // "a"（最后一个字符）
```

### 检测子字符串

```javascript
const browserType = "mozilla";

browserType.includes("zilla");     // true
browserType.startsWith("zilla");   // false
browserType.endsWith("zilla");     // true
```

### 查找子字符串的位置

```javascript
const tagline = "MDN - 开发者资源，由开发者提供";
tagline.indexOf("developers");     // 20
tagline.indexOf("x");             // -1（未找到）

// 查找后续出现
const first = tagline.indexOf("developers");           // 20
const second = tagline.indexOf("developers", first + 1); // 35
```

### 提取子字符串

```javascript
const browserType = "mozilla";
browserType.slice(1, 4);  // "ozi"
browserType.slice(2);     // "zilla"（从索引 2 到结尾）
```

### 转换大小写

```javascript
const radData = "My NaMe Is MuD";
radData.toLowerCase();  // "my name is mud"
radData.toUpperCase();  // "MY NAME IS MUD"
```

### 替换字符串部分

```javascript
// 替换第一个出现
const browserType = "mozilla";
const updated = browserType.replace("moz", "van");  // "vanilla"

// 替换所有出现
let quote = "To be or not to be";
quote = quote.replaceAll("be", "code");  // "To code or not to code"
```

**注意：** 字符串方法返回新字符串；它们不会修改原始字符串，除非你重新赋值。

---

## 数组

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Arrays](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Arrays)

### 创建数组

```javascript
const shopping = ["bread", "milk", "cheese", "hummus", "noodles"];
const sequence = [1, 1, 2, 3, 5, 8, 13];
const random = ["tree", 795, [0, 1, 2]];  // 允许混合类型
```

### 获取数组长度

```javascript
shopping.length;  // 5
```

### 访问和修改元素

```javascript
shopping[0];           // "bread"（零索引）
shopping[0] = "tahini"; // 修改第一个元素

// 多维数组
const random = ["tree", 795, [0, 1, 2]];
random[2][2];  // 2
```

### 查找元素索引

```javascript
const birds = ["Parrot", "Falcon", "Owl"];
birds.indexOf("Owl");     // 2
birds.indexOf("Rabbit");  // -1（未找到）
```

### 添加元素

```javascript
const cities = ["Manchester", "Liverpool"];

// 添加到末尾
cities.push("Cardiff");
cities.push("Bradford", "Brighton");  // 添加多个

// 添加到开头
cities.unshift("Edinburgh");
```

### 删除元素

```javascript
const cities = ["Manchester", "Liverpool", "Edinburgh", "Carlisle"];

// 删除末尾
cities.pop();       // 返回删除的元素

// 删除开头
cities.shift();     // 返回删除的元素

// 删除特定索引
const index = cities.indexOf("Liverpool");
if (index !== -1) {
  cities.splice(index, 1);    // 删除索引处的 1 个元素
}
cities.splice(index, 2);      // 从索引处删除 2 个元素
```

### 遍历数组

**for...of 循环：**

```javascript
const birds = ["Parrot", "Falcon", "Owl"];
for (const bird of birds) {
  console.log(bird);
}
```

**map() -- 转换元素：**

```javascript
const numbers = [5, 2, 7, 6];
const doubled = numbers.map(number => number * 2);
// [10, 4, 14, 12]
```

**filter() -- 选择匹配的元素：**

```javascript
const cities = ["London", "Liverpool", "Totnes", "Edinburgh"];
const longer = cities.filter(city => city.length > 8);
// ["Liverpool", "Edinburgh"]
```

### 在字符串和数组之间转换

```javascript
// 字符串转数组
const data = "Manchester,London,Liverpool";
const cities = data.split(",");
// ["Manchester", "London", "Liverpool"]

// 数组转字符串
const commaSeparated = cities.join(",");
// "Manchester,London,Liverpool"

// 简单的 toString（总是使用逗号）
const dogNames = ["Rocket", "Flash", "Bella"];
dogNames.toString();  // "Rocket,Flash,Bella"
```

---

## 条件语句

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Conditionals](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Conditionals)

### if...else 语句

```javascript
if (condition) {
  /* 条件为真时运行的代码 */
} else {
  /* 运行其他代码 */
}
```

### else if 语句

```javascript
if (choice === "sunny") {
  para.textContent = "穿短裤！";
} else if (choice === "rainy") {
  para.textContent = "带上雨衣。";
} else if (choice === "snowing") {
  para.textContent = "天气很冷！";
} else {
  para.textContent = "";
}
```

### 逻辑运算符

**AND (`&&`) -- 所有条件必须为真：**

```javascript
if (choice === "sunny" && temperature < 86) {
  para.textContent = "天气不错，去海滩吧！";
}
```

**OR (`||`) -- 至少一个条件必须为真：**

```javascript
if (iceCreamVanOutside || houseStatus === "on fire") {
  console.log("你应迅速离开房子。");
}
```

**NOT (`!`) -- 否定表达式：**

```javascript
if (!(iceCreamVanOutside || houseStatus === "on fire")) {
  console.log("可能应该待在屋里。");
}
```

**常见错误：**

```javascript
// 错误 - 始终评估为 true
if (x === 5 || 7 || 10 || 20) { }

// 正确
if (x === 5 || x === 7 || x === 10 || x === 20) { }
```

### switch 语句

```javascript
switch (choice) {
  case "sunny":
    para.textContent = "穿短裤！";
    break;
  case "rainy":
    para.textContent = "带上雨衣。";
    break;
  case "snowing":
    para.textContent = "天气很冷！";
    break;
  default:
    para.textContent = "";
}
```

### 三元运算符

```javascript
const greeting = isBirthday
  ? "生日快乐 Mrs. Smith!"
  : "早上好 Mrs. Smith.";
```

---

## 循环

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Loops](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Loops)

### for...of 循环

用于遍历集合：

```javascript
const cats = ["Leopard", "Serval", "Jaguar", "Tiger"];
for (const cat of cats) {
  console.log(cat);
}
```

### 标准 for 循环

```javascript
for (let i = 1; i < 10; i++) {
  console.log(`${i} x ${i} = ${i * i}`);
}
```

组成部分：**初始化器** (`let i = 1`)、**条件** (`i < 10`)、**最终表达式** (`i++`)。

### 使用 for 遍历数组

```javascript
const cats = ["Leopard", "Serval", "Jaguar"];
for (let i = 0; i < cats.length; i++) {
  console.log(cats[i]);
}
```

### while 循环

```javascript
let i = 0;
while (i < cats.length) {
  console.log(cats[i]);
  i++;
}
```

### do...while 循环

代码**至少执行一次**，然后检查条件：

```javascript
let i = 0;
do {
  console.log(cats[i]);
  i++;
} while (i < cats.length);
```

### break 和 continue

**break -- 立即退出循环：**

```javascript
for (const contact of contacts) {
  const splitContact = contact.split(":");
  if (splitContact[0].toLowerCase() === searchName) {
    console.log(`${splitContact[0]}'s number is ${splitContact[1]}.`);
    break;
  }
}
```

**continue -- 跳过当前迭代：**

```javascript
for (let i = 1; i <= num; i++) {
  let sqRoot = Math.sqrt(i);
  if (Math.floor(sqRoot) !== sqRoot) {
    continue;  // 跳过非完全平方数
  }
  console.log(i);
}
```

### 使用哪种循环类型？

| 循环类型 | 最适合 |
|-----------|----------|
| `for...of` | 遍历集合，不需要索引 |
| `for` | 通用循环；对迭代有完全控制 |
| `while` | 当初始化在循环之前有意义时 |
| `do...while` | 当代码必须至少运行一次时 |
| `map()` | 转换数组元素 |
| `filter()` | 选择特定数组元素 |

**警告：** 始终确保循环终止。无限循环会导致浏览器崩溃。

---

## 函数

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Functions](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Functions)

### 什么是函数？

函数是**可重用的代码块**，用于执行单个任务。它们允许你将代码存储在定义的块中，并在需要时调用。

### 浏览器内置函数

```javascript
const myText = "I am a string";
const newString = myText.replace("string", "sausage");  // "I am a sausage"

const myArray = ["I", "love", "chocolate", "frogs"];
const madeAString = myArray.join(" ");  // "I love chocolate frogs"

const myNumber = Math.random();  // 0 到 1 之间的随机数
```

### 自定义函数

```javascript
function myFunction() {
  alert("hello");
}

myFunction();  // 调用函数
```

### 函数参数和默认参数

```javascript
function hello(name = "Chris") {
  console.log(`Hello ${name}!`);
}

hello("Ari");  // "Hello Ari!"
hello();       // "Hello Chris!"
```

### 匿名函数

没有名称的函数，通常作为参数传递：

```javascript
textBox.addEventListener("keydown", function (event) {
  console.log(`你按了 "${event.key}"。`);
});
```

### 箭头函数

使用 `=>` 的现代语法：

```javascript
// 完整语法
textBox.addEventListener("keydown", (event) => {
  console.log(`你按了 "${event.key}"。`);
});

// 单个参数 - 可选括号
textBox.addEventListener("keydown", event => {
  console.log(`你按了 "${event.key}"。`);
});

// 单个返回语句 - 隐式返回
const originals = [1, 2, 3];
const doubled = originals.map(item => item * 2);  // [2, 4, 6]
```

### 函数作用域

函数内部的变量作用域为**函数作用域**，无法从外部访问：

```javascript
const x = 1;        // 全局作用域 - 可在任何地方访问

function myFunc() {
  const y = 2;      // 函数作用域 - 仅在 myFunc 内部
  console.log(x);   // 可访问全局 x
}

console.log(x);     // 可访问全局 x
console.log(y);     // ReferenceError: y 未定义
```

### 块作用域（let/const）

```javascript
if (x === 1) {
  const c = 4;      // 块作用域
}
console.log(c);     // ReferenceError: c 未定义
```

---

## 构建自定义函数

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Build_your_own_function](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Build_your_own_function)

### 函数结构

```javascript
function displayMessage() {
  // 函数体代码在这里
}
```

关键组成部分：

- `function` 关键字声明函数定义
- 函数名遵循变量命名规范
- 括号 `()` 包含参数
- 大括号 `{}` 包含调用时运行的代码

### 完整实用示例

```javascript
function displayMessage(msgText, msgType) {
  const body = document.body;

  const panel = document.createElement("div");
  panel.setAttribute("class", "msgBox");
  body.appendChild(panel);

  const msg = document.createElement("p");
  msg.textContent = msgText;
  panel.appendChild(msg);

  const closeBtn = document.createElement("button");
  closeBtn.textContent = "x";
  panel.appendChild(closeBtn);

  closeBtn.addEventListener("click", () => body.removeChild(panel));

  if (msgType === "warning") {
    msg.style.backgroundImage = 'url("icons/warning.png")';
    panel.style.backgroundColor = "red";
  } else if (msgType === "chat") {
    msg.style.backgroundImage = 'url("icons/chat.png")';
    panel.style.backgroundColor = "aqua";
  } else {
    msg.style.paddingLeft = "20px";
  }
}
```

### 调用函数

```javascript
// 直接调用
displayMessage("你的收件箱快满了", "warning");

// 作为事件处理程序（无括号）
btn.addEventListener("click", displayMessage);

// 通过匿名函数传递参数
btn.addEventListener("click", () =>
  displayMessage("Woo, 这是一个不同的消息!"),
);
```

**重要：** 传递函数作为回调时不要包含括号：

```javascript
btn.addEventListener("click", displayMessage);    // 正确
btn.addEventListener("click", displayMessage());  // 错误 - 立即调用
```

### 参数 vs 参数值

- **参数** 是函数定义中的命名变量
- **参数值** 是调用函数时实际传递的值

---

## 函数返回值

> 来源：[https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Return_values](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Return_values)

### 什么是返回值？

返回值是函数执行完毕时返回的值。

```javascript
const myText = "天气很冷";
const newString = myText.replace("cold", "warm");  // "天气很暖"
```

### 使用 return 关键字

```javascript
function random(number) {
  return Math.floor(Math.random() * number);
}
```

当函数被调用时，返回值**替代函数调用**：

```javascript
ctx.arc(random(WIDTH), random(HEIGHT), random(50), 0, 2 * Math.PI);
// 如果 random() 调用返回 500, 200, 35:
ctx.arc(500, 200, 35, 0, 2 * Math.PI);
```

### 创建带有返回值的函数

```javascript
function squared(num) {
  return num * num;
}

function cubed(num) {
  return num * num * num;
}

function factorial(num) {
  if (num < 0) return undefined;
  if (num === 0) return 1;
  let x = num - 1;
  while (x > 1) {
    num *= x;
    x--;
  }
  return num;
}
```

### 使用返回值

```javascript
input.addEventListener("change", () => {
  const num = parseFloat(input.value);
  if (isNaN(num)) {
    para.textContent = "你需要输入一个数字！";
  } else {
    para.textContent = `${num} 的平方是 ${squared(num)}. `;
    para.textContent += `${num} 的立方是 ${cubed(num)}. `;
    para.textContent += `${num} 的阶乘是 ${factorial(num)}. `;
  }
});
```

| 概念 | 描述 |
|---------|-------------|
| **return 关键字** | 返回值并立即退出函数 |
| **无返回值**

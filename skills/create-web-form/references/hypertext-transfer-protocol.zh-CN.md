# 超文本传输协议（HTTP）参考指南

涵盖HTTP协议、其消息、Cookie、认证、会话、头部、方法、状态码及规范的综合参考指南。所有内容均来源于Mozilla开发者网络（MDN）Web文档。

---

## 目录

1. [HTTP概述（简介）](#1-http-overview)
2. [HTTP简介](#2-an-overview-of-http)
3. [HTTP消息](#3-http-messages)
4. [HTTP Cookie](#4-http-cookies)
5. [HTTP认证](#5-http-authentication)
6. [HTTP会话](#6-http-sessions)
7. [HTTP头部参考](#7-http-headers-reference)
8. [HTTP请求方法](#8-http-request-methods)
9. [HTTP响应状态码](#9-http-response-status-codes)
10. [HTTP资源与规范](#10-http-resources-and-specifications)

---

## 1. HTTP概述

> **来源**：[https://developer.mozilla.org/en-US/docs/Web/HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

### 定义

**HTTP（超文本传输协议）** 是一种应用层协议，用于传输超媒体文档，例如HTML。虽然最初设计用于浏览器与Web服务器之间的通信，但它也用于机器对机器的通信和程序化API访问。

### 关键特性

- **客户端-服务器模型**：一种经典架构，客户端打开连接发起请求并等待服务器响应。
- **无状态协议**：服务器不会在请求之间保留会话数据，但Cookie增加了状态能力。
- **可扩展性**：基于资源、URI和基本消息结构的概念；协议随时间演进而不断扩展。

### 主要主题领域

#### 指南（基础与专业）

- **HTTP概述** -- 基本功能和协议栈位置
- **HTTP的发展历程** -- HTTP/0.9、1.0、1.1、2.0和3.0
- **HTTP消息** -- 请求/响应结构和类型
- **MIME类型** -- 内容类型头部和标准
- **HTTP缓存** -- 方法和头部控制
- **HTTP认证** -- 客户端身份验证
- **Cookie** -- Set-Cookie和Cookie头部用于状态管理
- **重定向** -- URL转发技术（3xx状态码）
- **条件请求** -- 依赖验证器的结果
- **范围请求** -- 部分资源获取
- **内容协商** -- Accept头部和格式偏好
- **连接管理（HTTP/1.x）** -- 持久连接和流水线
- **协议升级** -- 升级到HTTP/2、WebSocket
- **代理服务器和隧道**
- **客户端提示** -- 设备和偏好元数据
- **网络错误日志** -- 失败的获取报告

#### 安全与隐私

- **权限策略** -- 控制功能访问
- **CORS（跨域资源共享）** -- 跨站点请求处理
- **CSP（内容安全策略）** -- 资源加载限制和攻击缓解
- **CORP（跨域资源策略）** -- 防止推测性旁路攻击

### 参考文档摘要

- **HTTP头部**：169+已文档化的头部，包括`Content-Type`、`Accept`、`Authorization`、`Cache-Control`、`Set-Cookie`、`Cookie`、`Access-Control-Allow-Origin`、`Content-Security-Policy`等。
- **HTTP请求方法**：`GET`、`POST`、`PUT`、`PATCH`、`DELETE`、`HEAD`、`OPTIONS`、`CONNECT`、`TRACE`。
- **HTTP响应状态码**：分为五类 -- 1xx信息性、2xx成功、3xx重定向、4xx客户端错误、5xx服务器错误。

### 工具与资源

- **Firefox开发者工具** -- 网络监视器
- **HTTP观测站** -- 网站安全配置评估
- **RedBot** -- 缓存头部验证
- **nghttp2** -- HTTP/2客户端/服务器实现
- **curl** -- 命令行数据传输工具

---

## 2. HTTP简介

> **来源**：[https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)

### 什么是HTTP？

HTTP是一种用于获取资源（如HTML文档）的协议。它是Web上任何数据交换的基础，作为**客户端-服务器协议**运行，请求通常由接收方（通常是Web浏览器）发起。完整的文档由多个资源（包括文本、布局指令、图像、视频和脚本）构建而成。

HTTP是一种**应用层协议**，通过TCP或加密的TCP（TLS）传输。虽然最初在1990年代初期设计，但其仍然具有可扩展性并持续演进。

### 架构：基于HTTP的系统组件

#### 客户端：用户代理

- 代表用户操作的任何工具（主要是Web浏览器）。
- **始终**发起请求；服务器不会主动发起请求。
- 发送初始请求获取HTML文档，然后对CSS、脚本和子资源发起附加请求。
- 解释HTTP响应并将内容呈现给用户。

#### Web服务器

- 根据客户端请求提供文档。
- 可能是一个单个虚拟机或一组共享负载的服务器。
- 在HTTP/1.1和`Host`头部的支持下，多个服务器可以共享同一IP地址。

#### 代理

位于客户端和服务器之间，执行各种功能：

- **缓存**（公共或私有，如浏览器缓存）
- **过滤**（防病毒、家长控制）
- **负载均衡**（在服务器之间分配请求）
- **认证**（控制资源访问）
- **日志记录**（存储历史信息）

代理可以是**透明**（无修改地转发请求）或**非透明**（修改请求）。

### HTTP的基本特性

#### HTTP是简单的

- 通常设计为可读的。
- HTTP消息可以被人类阅读和理解，便于开发者测试。

#### HTTP是可扩展的

- **HTTP头部**使协议易于扩展和实验。
- 新功能可通过客户端和服务器之间的协议引入，这是HTTP/1.0引入的概念。

#### HTTP是无状态的，但并非无会话的

- **无状态**：同一连接的两个连续请求之间没有关联。
- 尽管如此，**HTTP Cookie**使状态会话成为可能，允许在请求之间共享上下文和状态。

#### HTTP与连接

HTTP需要可靠的传输协议。TCP是基于连接且可靠的，而UDP则不是。

- **HTTP/1.0**：每个请求/响应对打开一个独立的TCP连接（效率低下）。
- **HTTP/1.1**：通过`Connection`头部引入**流水线**和**持久连接**。
- **HTTP/2**：通过单个连接进行消息多路复用以提高效率。
- **实验性**：QUIC协议正在测试中作为传输层（基于UDP并具有可靠性）。

### HTTP流程

当客户端想要与服务器通信时：

1. **打开TCP连接**：用于发送请求和接收响应。客户端可能打开新连接、重用现有连接或打开多个连接。
2. **发送HTTP消息**：
   ```
   GET / HTTP/1.1
   Host: developer.mozilla.org
   Accept-Language: fr
   ```
3. **读取响应**：
   ```
   HTTP/1.1 200 OK
   Date: Sat, 09 Oct 2010 14:28:02 GMT
   Server: Apache
   Last-Modified: Tue, 01 Dec 2009 20:18:22 GMT
   ETag: "51142bc1-7449-479b075b2891b"
   Accept-Ranges: bytes
   Content-Length: 29769
   Content-Type: text/html

   <!doctype html>...（29769字节的请求网页）
   ```
4. **关闭或重用连接**以进行进一步请求。

### HTTP可控制的内容

- **缓存**：服务器指示代理和客户端缓存什么内容以及缓存多长时间。
- **放宽同源限制**：浏览器强制执行严格的同源隔离；HTTP头部可通过CORS放宽此限制。
- **认证**：通过`WWW-Authenticate`或HTTP Cookie限制对特定用户的访问。
- **代理和隧道**：穿越网络屏障，处理如FTP等协议。
- **会话**：HTTP Cookie将请求与服务器状态关联，即使在无状态协议下也能创建会话。

### 基于HTTP的API

- **Fetch API**：JavaScript中使用最广泛的HTTP请求API，取代了较旧的`XMLHttpRequest` API。
- **服务器发送事件**：服务器向客户端发送单向事件的机制，使用HTTP作为传输方式。

---

## 3. HTTP消息

> **来源**：[https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages)

### 概述

HTTP消息是服务器和客户端之间交换数据的机制。有两种类型：

- **请求**：客户端发送以触发服务器上的操作。
- **响应**：服务器对请求的回答。

HTTP/1.x消息是基于文本的，易于阅读。HTTP/2将消息封装在二进制帧中，但保持相同的底层语义。

### HTTP消息结构

请求和响应共享相同的结构：

```
1. 起始行（单行描述HTTP版本 + 请求方法或结果）
2. HTTP头部（可选的关于消息的元数据）
3. 空行（标记元数据结束）
4. 消息体（可选的消息关联数据）
```

**起始行**和**头部**统称为**头部**。消息体是起始行之后的内容。

### HTTP请求

#### 请求行格式

```
<方法> <请求目标> <协议>
```

#### 组成部分

**方法（HTTP动词）**：描述请求的含义和期望结果。常见方法包括`GET`、`POST`、`PUT`、`PATCH`、`DELETE`、`HEAD`、`OPTIONS`、`CONNECT`。通常只有`PATCH`、`POST`和`PUT`请求包含消息体。

**请求目标（URL）**：根据上下文有四种类型：

1. **原始形式**（最常见）：包含主机头部的绝对路径。
   ```http
   GET /en-US/docs/Web/HTTP/Guides/Messages HTTP/1.1
   ```

2. **绝对形式**：完整的URL；用于代理。
   ```http
   GET https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages HTTP/1.1
   ```

3. **权威形式**：包含权威和端口的冒号；用于`CONNECT`。
   ```http
   CONNECT developer.mozilla.org:443 HTTP/1.1
   ```

4. **星号形式**：仅在`OPTIONS`中使用，表示整个服务器。
   ```http
   OPTIONS * HTTP/1.1
   ```

**协议（HTTP版本）**：通常为`HTTP/1.1`。在HTTP/2+中，消息中不再包含协议版本。

#### 请求头部

在起始行之后，消息体之前。不区分大小写，后跟冒号和值：

```http
Host: example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 49
```

**分类**：
- **请求头部**：提供关于要获取资源或请求资源的客户端的额外上下文。
- **表示头部**：描述消息体的原始形式和应用的编码。

#### 请求体

仅适用于`PATCH`、`POST`和`PUT`方法。示例：

**表单数据**：
```
name=FirstName+LastName&email=bsmth%40example.com
```

**JSON**：
```json
{
  "firstName": "Brian",
  "lastName": "Smith",
  "email": "bsmth@example.com"
}
```

**多部分表单数据**：
```http
--delimiter123
Content-Disposition: form-data; name="field1"

value1
--delimiter123
Content-Disposition: form-data; name="field2"; filename="example.txt"

文本文件内容
--delimiter123--
```

### HTTP响应

#### 状态行格式

```
<协议> <状态码> <原因短语>
```

#### 组成部分

- **协议**：消息的HTTP版本。
- **状态码**：指示请求成功或失败的数字代码。
  - 2xx成功：`200 OK`、`201 Created`、`204 No Content`
  - 3xx重定向：`302 Found`、`304 Not Modified`
  - 4xx客户端错误：`400 Bad Request`、`404 Not Found`
  - 5xx服务器错误：`500 Internal Server Error`、`503 Service Unavailable`
- **原因短语**：可选的简要文本描述，例如"Created"或"Not Found"。

#### 响应头部

与响应一起发送的元数据：

```http
Content-Type: application/json
Content-Length: 256
Cache-Control: max-age=604800
Date: Fri, 13 Sep 2024 12:56:07 GMT
```

#### 响应体

大多数消息包含。可能是：
- **单资源体**：由`Content-Type`和`Content-Length`头部定义，或通过`Transfer-Encoding: chunked`分块传输。
- **多资源体**：包含不同信息的多个部分，与HTML表单和范围请求相关。

注意：状态码如`201 Created`或`204 No Content`可能不包含响应体。

### HTTP/2消息

与HTTP/1.x的关键区别：

- 用二进制帧封装消息（更高效）。
- 通过HPACK算法进行头部压缩。
- **多路复用**：通过单个连接进行多个并发请求和响应以提高效率。
- 消除协议层面的**头部阻塞**（Head-of-Line Blocking）。

HTTP/2使用以`:`开头的**伪头部字段**：

**请求伪头部**：
```
:method: GET
:scheme: https
:authority: www.example.com
:path: /
```

**响应伪头部**：
```
:status: 200
```

### HTTP/3注意事项

- 使用QUIC协议（基于UDP而非TCP）。
- 修复TCP层面的头部阻塞。
- 减少连接建立时间。
- 在不可靠网络上增强稳定性。
- 保持相同的HTTP核心语义（方法、状态码、头部）。

---

## 4. HTTP Cookie

> **来源**：[https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies)

### 什么是Cookie？

**Cookie**（网络Cookie或浏览器Cookie）是服务器发送到用户Web浏览器的小段数据。浏览器可以存储Cookie、创建新Cookie、修改现有Cookie，并在后续请求中将其发送回同一服务器。Cookie使Web应用能够存储有限的数据并记住状态信息。

### 主要用途

1. **会话管理**：用户登录状态、购物车内容、游戏得分等会话相关细节。
2. **个性化**：用户偏好，如显示语言和UI主题。
3. **跟踪**：记录和分析用户行为。

### 设置Cookie

#### 服务端（HTTP头部）

使用`Set-Cookie`响应头部：

```http
HTTP/2.0 200 OK
Content-Type: text/html
Set-Cookie: yummy_cookie=chocolate
Set-Cookie: tasty_cookie=strawberry
```

#### 客户端（JavaScript）

使用`Document.cookie`属性：

```javascript
document.cookie = "yummy_cookie=chocolate";
document.cookie = "tasty_cookie=strawberry";
console.log(document.cookie);
// 输出 "yummy_cookie=chocolate; tasty_cookie=strawberry"
```

### 发送Cookie

当向某个域名发起新请求时，浏览器会自动通过`Cookie`请求头部发送存储的Cookie：

```http
GET /sample_page.html HTTP/2.0
Host: www.example.org
Cookie: yummy_cookie=chocolate; tasty_cookie=strawberry
```

### Cookie属性

#### 生命周期控制

**永久Cookie**通过`Expires`或`Max-Age`在当前会话后持续存在：

```http
Set-Cookie: id=a3fWa; Expires=Thu, 31 Oct 2021 07:28:00 GMT;
Set-Cookie: id=a3fWa; Max-Age=2592000
```

- `Expires`：指定过期日期/时间。
- `Max-Age`：指定持续时间（以秒为单位）；优先于`Expires`，如果两者都设置则`Max-Age`优先。

**会话Cookie**在当前会话结束时被删除（无`Max-Age`或`Expires`属性）。

#### 删除Cookie

通过设置`Max-Age=0`或过去的`Expires`日期，或使用`Clear-Site-Data`头部：

```http
Set-Cookie: id=a3fWa; Max-Age=0
Clear-Site-Data: "cookies"
```

#### 范围控制

**Domain属性**：指定哪些域名可以接收Cookie。

```http
Set-Cookie: id=a3fWa; Domain=mozilla.org
```

- 未指定时：Cookie仅发送给设置它的服务器，不包括子域名。
- 指定时：发送给域名及其所有子域名。

**Path属性**：指定请求URL中必须存在的URL路径。

```http
Set-Cookie: id=a3fWa; Path=/docs
```

匹配路径：`/docs`、`/docs/`、`/docs/Web/`、`/docs/Web/HTTP`。不匹配路径：`/`、`/docsets`、`/fr/docs`。

#### 安全属性

**Secure**：仅通过HTTPS发送（不通过非加密HTTP发送，除非在本地主机）。

```http
Set-Cookie: id=a3fWa; Secure
```

**HttpOnly**：阻止JavaScript通过`Document.cookie`访问；仅可通过HTTP请求访问。缓解XSS攻击。

```http
Set-Cookie: id=a3fWa; HttpOnly
```

**组合使用**：

```http
Set-Cookie: id=a3fWa; Expires=Thu, 21 Oct 2021 07:28:00 GMT; Secure; HttpOnly
```

#### SameSite属性

控制Cookie是否随跨域请求发送：

| 值 | 行为 |
|----|------|
| **Strict** | 仅在来自Cookie源站点的请求中发送。用于敏感功能（如认证、购物车）。 |
| **Lax** | 在站点导航中发送，但不用于其他跨域请求。如果未设置`SameSite`则默认此值。 |
| **None** | 与原始和跨域请求一起发送。需要`Secure`属性。 |

### Cookie前缀（纵深防御）

- **`__Secure-`**：必须通过`Secure`属性设置，由HTTPS页面使用。
- **`__Host-`**：必须通过`Secure`属性设置，不能有`Domain`属性，必须有`Path=/`。
- **`__Http-`**：必须通过`Secure`标志设置，必须有`HttpOnly`属性。

### 安全最佳实践

1. 对敏感Cookie使用`Secure`和`HttpOnly`属性。
2. 通过`Domain`和`Path`适当限制作用域。
3. 通过`SameSite`控制跨域请求。
4. 保持敏感Cookie的生命周期短。
5. 认证后重新生成会话Cookie以防止会话固定攻击。
6. 存储不可感知的标识符，而不是直接存储敏感数据。
7. 使用Cookie前缀（`__Secure-`、`__Host-`）实现纵深防御。

### 存储限制

- 每个域名的Cookie最大数量因浏览器而异，通常为数百个。
- 每个Cookie的最大大小通常为4KB。
- 现代替代方案：Web存储API（`localStorage`、`sessionStorage`）和IndexedDB。

### 隐私与第三方Cookie

- 第三方Cookie由来自不同域名的嵌入内容设置。
- 大多数浏览器厂商默认阻止第三方Cookie。
- **适用法规**：GDPR（欧盟）、ePrivacy指令（欧盟）、加州消费者隐私法案（美国）。

### 相关头部

- `Set-Cookie` -- 服务端设置Cookie。
- `Cookie` -- 客户端发送Cookie。
- `Clear-Site-Data` -- 清除Cookie和其他站点数据。

### 规范

RFC 6265 -- HTTP状态管理机制。

---

## 5. HTTP认证

> **来源**：[https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Authentication)

### 通用HTTP认证框架

HTTP认证在**RFC 7235**中定义，提供了一个基于服务器和客户端之间挑战-响应机制的访问控制框架。

#### 挑战-响应流程

1. **服务器挑战**：服务器以`401 Unauthorized`状态码响应，并通过`WWW-Authenticate`响应头部包含认证挑战详情。
2. **客户端响应**：客户端通过`Authorization`请求头部提供凭据。
3. **重试**：客户端通常向用户显示密码提示，然后重新发送带有正确凭据的请求。

### 认证头部

#### `WWW-Authenticate`和`Proxy-Authenticate`

定义访问资源所需的认证方法：

```http
WWW-Authenticate: <类型> realm=<领域>
Proxy-Authenticate: <类型> realm=<领域>
```

- `<类型>`：认证方案（如"Basic"、"Bearer"）。
- `realm`：描述受保护区域（如"访问测试站点"）。

#### `Authorization`和`Proxy-Authorization`

包含用于认证服务器或代理的凭据：

```http
Authorization: <类型> <凭据>
Proxy-Authorization: <类型> <凭据>
```

### 代理认证

使用单独的头部和状态码：

- **状态码**：`407 Proxy Authentication Required`
- **响应头部**：`Proxy-Authenticate`
- **请求头部**：`Proxy-Authorization`

### 访问控制响应码

| 状态 | 含义 | 使用场景 |
|------|------|----------|
| **401** | 未授权 | 客户端必须认证以获取请求响应 |
| **403** | 禁止 | 客户端缺乏访问权限；服务器拒绝（不同于401，客户端身份已知） |
| **404** | 未找到 | 服务器找不到请求的资源 |
| **407** | 代理认证所需 | 与401类似，但代理需要认证 |

### 认证方案

| 方案 | 参考 | 描述 |
|------|------|------|
| **Basic** | RFC 7617 | Base64编码的用户名:密码（需要HTTPS） |
| **Bearer** | RFC 6750 | OAuth 2.0承载令牌 |
| **Digest** | RFC 7616 | MD5或SHA-256哈希 |
| **HOBA** | RFC 7486 | HTTP原生绑定认证（数字签名） |
| **Mutual** | RFC 8120 | 互认证 |
| **Negotiate/NTLM** | RFC 4559 | Windows集成认证 |
| **VAPID** | RFC 8292 | 自愿应用服务器标识 |
| **SCRAM** | RFC 7804 | 带盐的挑战响应认证机制 |
| **AWS4-HMAC-SHA256** | AWS文档 | AWS签名版本4 |

由IANA维护的完整列表：[https://www.iana.org/assignments/http-authschemes/http-authschemes.xhtml](https://www.iana.org/assignments/http-authschemes/http-authschemes.xhtml)

### 基本认证方案

- **标准**：RFC 7617。
- **格式**：以base64编码的用户ID和密码对（`username:password`）传输。
- **字符集**：UTF-8。

**安全注意事项**：
- Base64是可逆的；凭据以明文形式出现。
- 始终使用HTTPS/TLS与Basic认证结合使用。
- 易受CSRF攻击；凭据在所有请求中发送，无论来源如何。

#### Apache配置

`.htaccess`文件：

```apacheconf
AuthType Basic
AuthName "访问测试站点"
AuthUserFile /path/to/.htpasswd
Require valid-user
```

#### Nginx配置

```nginx
location /status {
    auth_basic           "访问测试站点";
    auth_basic_user_file /etc/apache2/.htpasswd;
}
```

### 安全注意事项

- 跨域图像无法触发HTTP认证对话框（Firefox 59+）。
- 现代浏览器使用UTF-8编码用户名和密码。
- URL中嵌入的凭据（`https://username:password@www.example.com/`）已弃用；现代浏览器在发送请求前会从URL中剥离凭据。

---

## 6. HTTP会话

> **来源**：[https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Session](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Session)

### 概述

客户端-服务器协议中的HTTP会话由**三个阶段**组成：

1. 客户端建立TCP连接（或适当的传输层连接）。
2. 客户端发送请求并等待响应。
3. 服务器处理请求并返回带有状态码和数据的响应。

自HTTP/1.1起，连接在完成请求后不再关闭，允许客户端在不重新建立连接的情况下进行后续请求。

### 阶段1：建立连接

- **客户端**发起连接（不是服务器）。
- HTTP通常使用**TCP**作为传输层。
- **默认端口**：HTTP服务器为80（其他端口如8000、8080也可使用）。
- 服务器无法在没有明确请求的情况下向客户端发送数据，但可通过Push API、服务器发送事件或WebSocket API克服此限制。

### 阶段2：发送客户端请求

客户端请求由文本指令组成，以CRLF分隔，分为三个块：

#### 块1：请求行

包含请求方法、文档路径和HTTP协议版本。

#### 块2：HTTP头部

关于数据类型、语言偏好、MIME类型和修改服务器行为的数据信息。以空行结束，分隔头部与数据块。

#### 块3：可选数据块

包含附加数据，主要用于POST方法。

**示例GET请求**：

```http
GET / HTTP/1.1
Host: developer.mozilla.org
Accept-Language: fr

```

**示例POST请求**：

```http
POST /contact_form.php HTTP/1.1
Host: developer.mozilla.org
Content-Length: 64
Content-Type: application/x-www-form-urlencoded

name=Joe%20User&request=Send%20me%20one%20of%20your%20catalogue
```

#### 常见请求方法

| 方法 | 用途 |
|------|------|
| **GET** | 请求指定资源的数据表示；仅用于获取数据 |
| **POST** | 向服务器发送数据以改变其状态；常用于HTML表单 |

### 阶段3：服务器响应结构

与请求类似，服务器响应由文本指令组成，以CRLF分隔，分为三个块：

#### 块1：状态行

HTTP版本确认、响应状态码和简要的人类可读含义。

#### 块2：HTTP头部

关于发送数据的信息（类型、大小、压缩、缓存提示）。以空行结束。

#### 块3：数据块

可选数据或响应内容。

**示例成功响应（200 OK）**：

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 55743
Connection: keep-alive
Cache-Control: s-maxage=300, public, max-age=0
Content-Language: en-US
Date: Thu, 06 Dec 2018 17:37:18 GMT
ETag: "2e77ad1dc6ab0b53a2996dfd4653c1c3"
Server: meinheld/0.6.1
Strict-Transport-Security: max-age=63072000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Vary: Accept-Encoding,Cookie
Age: 7

<!doctype html>
<html lang="en">
  ...
</html>
```

**示例重定向（301）**：

```http
HTTP/1.1 301 Moved Permanently
Server: Apache/2.4.37 (Red Hat)
Content-Type: text/html; charset=utf-8
Location: https://developer.mozilla.org/
```

**示例错误（404）**：

```http
HTTP/1.1 404 Not Found
Content-Type: text/html; charset=utf-8
Content-Length: 38217
```

---

## 7. HTTP头部参考

> **来源**：[https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers)

### 概述

HTTP头部允许客户端和服务器在请求和响应中传递附加信息。在HTTP/1.X中，头部是不区分大小写的名称-值对（例如`Allow: POST`）。在HTTP/2及以上版本中，头部以小写形式出现，伪头部以冒号开头（例如` :status: 200`）。

### 根据上下文的头部分类

- **请求头部**：包含要获取的资源信息或请求资源的客户端信息。
- **响应头部**：包含响应的附加信息，如位置或服务器详情。
- **表示头部**：包含资源体的信息，包括MIME类型、编码和压缩。
- **有效载荷头部**：包含与有效载荷数据无关的信息，如内容长度和传输编码。

### 根据代理处理的头部分类

- **端到端头部**：必须传递给最终接收者。中间代理必须原样重传，缓存必须存储。
- **逐跳头部**：仅对单个传输层连接有意义。代理或缓存不得重传。

### 认证头部

| 头部 | 类型 | 描述 |
|------|------|------|
| `WWW-Authenticate` | 响应 | 定义访问资源所需的认证方法 |
| `Authorization` | 请求 | 包含用于认证用户代理的凭据 |
| `Proxy-Authenticate` | 响应 | 定义代理服务器访问所需的认证方法 |
| `Proxy-Authorization` | 请求 | 包含用于认证代理服务器的凭据 |

### 缓存头部

| 头部 | 类型 | 描述 |
|------|------|------|
| `Age` | 响应 | 该对象在代理缓存中停留的时间（以秒为单位） |
| `Cache-Control` | 请求和响应 | 缓存机制的指令 |
| `Clear-Site-Data` | 响应 | 清除浏览数据（Cookie、存储、缓存） |
| `Expires` | 响应 | 响应被视为过期的时间 |

### 条件头部

| 头部 | 类型 | 描述 |
|------|------|------|
| `Last-Modified` | 响应 | 资源的最后修改日期 |
| `ETag` | 响应 | 识别资源版本的唯一字符串 |
| `If-Match` | 请求 | 仅在资源匹配给定ETag时应用方法 |
| `If-None-Match` | 请求 | 仅在资源不匹配给定ETag时应用方法 |
| `If-Modified-Since` | 请求 | 仅在资源在给定日期后修改时传输资源 |
| `If-Unmodified-Since` | 请求 | 仅在资源在日期后未修改时传输资源 |
| `Vary` | 响应 | 确定缓存决策中的头部匹配方式 |

### 连接管理头部

| 头部 | 类型 | 描述 |
|------|------|------|
| `Connection` | 请求和响应 | 控制网络连接是否保持打开 |
| `Keep-Alive` | 请求和响应 | 控制持久连接保持打开的时间 |

### 内容协商头部

| 头部 | 类型 | 描述 |
|------|------|------|
| `Accept` | 请求 | 通知服务器可接受的数据类型 |
| `Accept-Encoding` | 请求 | 指定可接受的压缩算法 |
| `Accept-Language` | 请求 | 通知服务器首选的人类语言 |
| `Accept-Patch` | 响应 | 宣告可接受的PATCH请求媒体类型 |
| `Accept-Post` | 响应 | 宣告可接受的POST请求媒体类型 |

### Cookie头部

| 头部 | 类型 | 描述 |
|------|------|------|
| `Cookie` | 请求 | 包含服务器之前设置的HTTP Cookie |
| `Set-Cookie` | 响应 | 从服务器向用户代理发送Cookie |

### CORS（跨域资源共享）头部

| 头部 | 类型 | 描述 |
|------|------|------|
| `Access-Control-Allow-Credentials` | 响应 | 表示响应是否可以与凭据一起暴露 |
| `Access-Control-Allow-Headers` | 响应 | 列出可在跨域请求中使用的HTTP头部 |
| `Access-Control-Allow-Methods` | 响应 | 指定跨域请求允许的方法 |
| `Access-Control-Allow-Origin` | 响应 | 表示响应是否可以共享 |
| `Access-Control-Expose-Headers` | 响应 | 列出在跨域响应中暴露的头部 |
| `Access-Control-Max-Age` | 响应 | 预检请求结果可缓存的时间 |
| `Access-Control-Request-Headers` | 请求 | 列出实际请求中使用的头部（预检） |
| `Access-Control-Request-Method` | 请求 | 列出实际请求中使用的方法（预检） |
| `Origin` | 请求 | 表示获取的来源 |
| `Timing-Allow-Origin` | 响应 | 指定允许查看资源时间API值的来源 |

### 消息体信息头部

| 头部 | 类型 | 描述 |
|------|------|------|
| `Content-Length` | 请求和响应 | 资源大小（十进制字节） |
| `Content-Type` | 请求和响应 | 表示资源的媒体类型 |
| `Content-Encoding` | 响应 | 指定使用的压缩算法 |
| `Content-Language` | 响应 | 描述预期的人类语言 |
| `Content-Location` | 响应 | 表示返回数据的替代位置 |
| `Content-Disposition` | 响应 | 表示资源应内联显示还是下载 |

### 范围请求头部

| 头部 | 类型 | 描述 |
|------|------|------|
| `Accept-Ranges` | 响应 | 表示服务器是否支持范围请求 |
| `Range` | 请求 | 表示服务器应返回文档的哪一部分 |
| `If-Range` | 请求 | 创建条件范围请求 |
| `Content-Range` | 响应 | 表示部分消息在完整正文中的位置 |

### 重定向头部

| 头部 | 类型 | 描述 |
|------|------|------|
| `Location` | 响应 | 表示重定向页面的URL |
| `Refresh` | 响应 | 指示浏览器重新加载页面或重定向 |

### 请求上下文头部

| 头部 | 类型 | 描述 |
|------|------|------|
| `From` | 请求 | 包含控制请求的用户的电子邮件地址 |
| `Host` | 请求 | 指定服务器的域名和可选端口 |
| `Referer` | 请求 | 上一个网页的地址 |
| `Referrer-Policy` |

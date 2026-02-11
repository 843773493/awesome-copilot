# XML 参考资料

---

## XML 引言

> 来源：[https://developer.mozilla.org/en-US/docs/Web/XML/Guides/XML_introduction](https://developer.mozilla.org/en-US/docs/Web/XML/Guides/XML_introduction)

### 概述

**XML（可扩展标记语言）** 是一种类似于 HTML 的标记语言，但不包含预定义的标签。相反，您可以定义自己的标签，以满足特定需求。它使数据以标准化格式进行存储，可以在不同系统和平台之间存储、搜索和共享。

**基于 XML 的语言包括：** XHTML、MathML、SVG、RSS 和 RDF。

### XML 文档的结构

#### XML 声明

XML 声明用于传输文档的元数据。

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

**属性：**

- **`version`** -- 文档中使用的 XML 版本。
- **`encoding`** -- 文档中使用的字符编码。

#### 注释

```xml
<!-- 注释 -->
```

### "正确的" XML（有效且格式正确）

要使 XML 文档正确，必须满足以下条件：

1. 文档必须是 **格式正确的**。
2. 文档必须符合 **所有 XML 语法规则**。
3. 文档必须符合 **语义规则**（通常在 XML 模式或 DTD 中定义）。

#### 示例 -- 错误的 XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<message>
    <warning>
        Hello World
    <!--missing </warning> -->
</message>
```

#### 示例 -- 修正后的 XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<message>
    <warning>
         Hello World
    </warning>
</message>
```

包含未定义标签的文档是无效的。标签必须在模式或 DTD 中正确定义。

### 字符引用

与 HTML 一样，XML 使用字符引用表示特殊保留字符：

| 实体    | 字符       | 描述             |
|---------|------------|------------------|
| `&lt;`  | `<`        | 小于号           |
| `&gt;`  | `>`        | 大于号           |
| `&amp;` | `&`        | 与号             |
| `&quot;` | `"`       | 双引号           |
| `&apos;` | `'`       | 引号/单引号      |

#### 自定义实体定义

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE body [
  <!ENTITY warning "Warning: Something bad happened... please refresh and try again.">
]>
<body>
  <message> &warning; </message>
</body>
```

#### 数字字符引用

使用数字引用表示特殊字符：

- `&#xA9;` = (c)（版权符号）

### 显示 XML

#### 使用 CSS 样式表

```xml
<?xml-stylesheet type="text/css" href="stylesheet.css"?>
```

#### 使用 XSLT（推荐用于复杂转换）

```xml
<?xml-stylesheet type="text/xsl" href="transform.xsl"?>
```

**XSLT（可扩展样式表语言转换）** 是一种强大的方法，可以将 XML 转换为其他语言（如 HTML），使 XML 具有极大的灵活性。

### 关键要点

- XML 是 **标准化的**，确保数据在不同系统中可以一致解析。
- XML 文档需要 **正确嵌套和关闭标签** 才能格式正确。
- XML 是 **平台和语言无关的**。
- 使用 **DTD 或 XML 模式** 来定义有效的标签结构。
- 使用 **XSLT** 实现强大的 XML 转换功能。

---

## 解析和序列化 XML

> 来源：[https://developer.mozilla.org/en-US/docs/Web/XML/Guides/Parsing_and_serializing_XML](https://developer.mozilla.org/en-US/docs/Web/XML/Guides/Parsing_and_serializing_XML)

### 概述

有时，您可能需要将 XML 内容解析为 DOM 树，或者反过来，将现有的 DOM 树序列化为 XML。

### 关键 Web 平台对象

| 对象               | 用途                                                                                      |
|--------------------|-------------------------------------------------------------------------------------------|
| **XMLSerializer**  | 序列化 DOM 树，将其转换为包含 XML 的字符串                                             |
| **DOMParser**      | 通过解析包含 XML 的字符串构建 DOM 树，返回 XMLDocument 或 Document                       |
| **fetch()**        | 从 URL 加载内容；XML 内容作为文本字符串返回，可通过 DOMParser 解析                         |
| **XMLHttpRequest** | fetch() 的前身；可通过其 `responseXML` 属性将资源作为 Document 返回                       |
| **XPath**          | 为 XML 文档的特定部分创建地址字符串                                                       |

### 创建 XML 文档

#### 将字符串解析为 DOM 树

```javascript
const xmlStr = '<q id="a"><span id="b">hey!</span></q>';
const parser = new DOMParser();
const doc = parser.parseFromString(xmlStr, "application/xml");
// 打印根元素的名称或错误信息
const errorNode = doc.querySelector("parsererror");
if (errorNode) {
  console.log("解析时出错");
} else {
  console.log(doc.documentElement.nodeName);
}
```

#### 将可寻址资源解析为 DOM 树

使用 `fetch()`：

```javascript
fetch("example.xml")
  .then((response) => response.text())
  .then((text) => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(text, "text/xml");
    console.log(doc.documentElement.nodeName);
  });
```

此方法将资源作为文本字符串获取，然后使用 `DOMParser.parseFromString()` 构建 `XMLDocument`。

**注意：** 如果文档是 HTML，代码返回 `Document`；如果文档是 XML，结果对象是 `XMLDocument`。这两种类型本质上是相同的，区别主要源于历史原因。

### 序列化 XML 文档

#### 将 DOM 树序列化为字符串

要将 DOM 树 `doc` 序列化为 XML 文本，调用 `XMLSerializer.serializeToString()`：

```javascript
const serializer = new XMLSerializer();
const xmlStr = serializer.serializeToString(doc);
```

#### 序列化 HTML 文档

如果 DOM 是 HTML 文档，可以使用：

使用 `innerHTML`（仅包含子节点）：

```javascript
const docInnerHtml = document.documentElement.innerHTML;
```

使用 `outerHTML`（包含节点及其所有子节点）：

```javascript
const docOuterHtml = document.documentElement.outerHTML;
```

---

## OpenSearch 描述格式

> 来源：[https://developer.mozilla.org/en-US/docs/Web/XML/Guides/OpenSearch](https://developer.mozilla.org/en-US/docs/Web/XML/Guides/OpenSearch)

### 概述

**OpenSearch 描述格式** 允许网站描述其搜索引擎界面，使浏览器和客户端应用程序能够将站点特定的搜索功能集成到地址栏中。支持 Firefox、Edge、Safari 和 Chrome。

- 浏览器通过 URL 模板查询搜索引擎。
- 浏览器在指定占位符中填充用户的搜索词。
- 示例：`https://example.com/search?q={searchTerms}` 变为 `https://example.com/search?q=foo`。
- 网站通过 HTML 中链接的 XML 描述文件注册搜索引擎。
- **注意：** Chrome 默认将网站搜索引擎注册为“非活动”状态；用户必须手动激活。

### OpenSearch 描述文件

#### 基本 XML 模板

```xml
<OpenSearchDescription
  xmlns="http://a9.com/-/spec/opensearch/1.1/"
  xmlns:moz="http://www.mozilla.org/2006/browser/search/">
  <ShortName>[SNK]</ShortName>
  <Description>[搜索引擎全名和简介]</Description>
  <InputEncoding>[UTF-8]</InputEncoding>
  <Image width="16" height="16" type="image/x-icon">[https://example.com/favicon.ico]</Image>
  <Url type="text/html" template="[searchURL]"/>
  <Url type="application/x-suggestions+json" template="[suggestionURL]"/>
</OpenSearchDescription>
```

### 元素规范

#### ShortName

- 搜索引擎的短名称。
- **必须为 16 个字符或更少。**
- 仅限纯文本；不支持 HTML 或标记。

#### Description

- 搜索引擎的简要描述。
- **最大 1024 个字符。**
- 仅限纯文本；不支持 HTML 或标记。

#### InputEncoding

- 提交输入到搜索引擎时使用的字符编码。
- 示例：`UTF-8`。

#### Image

- 搜索引擎图标的 URL 或数据 URL。
- **推荐尺寸：**
  - 类型为 `image/x-icon` 的 16x16 图像（例如 `/favicon.ico`）
  - 类型为 `image/jpeg` 或 `image/png` 的 64x64 图像

**图标 URL 示例：**

```xml
<Image height="16" width="16" type="image/x-icon">https://example.com/favicon.ico</Image>
```

```xml
<Image height="16" width="16">data:image/x-icon;base64,AAABAAEAEBAAA...DAAA=</Image>
```

**重要图标注意事项：**

- Firefox 会将图标缓存为 base64 `data:` URL。
- 搜索插件存储在配置文件的 `searchplugins/` 文件夹中。
- `http:` 和 `https:` URL 会转换为 `data:` URL。
- **Firefox 会拒绝大于 10KB 的远程加载图标。**

#### Url

通过 `template` 属性描述用于搜索查询的 URL。

**Firefox 支持的 URL 类型：**

| 类型                                      | 用途                                    |
|-------------------------------------------|----------------------------------------|
| `type="text/html"`                        | 实际搜索查询 URL                        |
| `type="application/x-suggestions+json"`  | JSON 格式的搜索建议                     |
| `type="application/x-moz-keywordsearch"`  | 位于地址栏中的关键字搜索（仅限 Firefox） |

**动态参数：**

- `{searchTerms}` -- 用户的搜索词。
- 还支持其他 OpenSearch 1.1 参数。

### 链接到 OpenSearch 描述文件

#### HTML 链接元素

```html
<link
  rel="search"
  type="application/opensearchdescription+xml"
  title="[searchTitle]"
  href="[descriptionURL]" />
```

**必需属性：**

- `rel="search"` -- 建立搜索引擎关系。
- `type="application/opensearchdescription+xml"` -- MIME 类型。
- `title="[searchTitle]"` -- 搜索名称（必须与 `<ShortName>` 匹配）。
- `href="[descriptionURL]"` -- XML 描述文件的 URL。

#### 多个搜索引擎示例

```html
<link
  rel="search"
  type="application/opensearchdescription+xml"
  title="MySite: By Author"
  href="http://example.com/mysiteauthor.xml" />

<link
  rel="search"
  type="application/opensearchdescription+xml"
  title="MySite: By Title"
  href="http://example.com/mysitetitle.xml" />
```

### 支持自动更新

包含一个具有自动更新功能的额外 `Url` 元素：

```xml
<Url
  type="application/opensearchdescription+xml"
  rel="self"
  template="https://example.com/mysearchdescription.xml" />
```

此功能允许 OpenSearch 描述文件自动更新。

### 故障排除提示

1. **服务器 Content-Type** -- 为 OpenSearch 描述文件提供 `Content-Type: application/opensearchdescription+xml`。
2. **XML 格式正确性** -- 直接在浏览器中加载文件进行验证。与号（&）必须转义为 `&amp;`。标签必须使用尾随斜杠或匹配的结束标签关闭。
3. **缺少 xmlns 属性** -- 始终包含 `xmlns="http://a9.com/-/spec/opensearch/1.1/"`，否则 Firefox 会报告：“Firefox 无法下载搜索插件。”
4. **缺少 text/html URL** -- 必须包含 `text/html` URL 类型；仅 Atom 或 RSS 的 URL 会生成错误。
5. **Favicon 大小** -- 从远程获取的 favicon 必须不超过 10KB。
6. **浏览器激活** -- 浏览器可能不会默认激活网站搜索快捷方式；请检查浏览器设置并手动激活。

#### Firefox 调试

使用 `about:config` 启用日志记录：

1. 将偏好设置 `browser.search.log` 设置为 `true`。
2. 在 Firefox 浏览器控制台中查看日志：工具 > 浏览器工具 > 浏览器控制台。

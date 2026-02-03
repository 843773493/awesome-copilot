---
name: markdown-to-html
description: '将 Markdown 文件转换为 HTML，类似于 `marked.js`、`pandoc`、`gomarkdown/markdown` 或其他工具；或编写自定义脚本将 Markdown 转换为 HTML 和/或在使用 Markdown 文档的网页模板系统（如 `jekyll/jekyll`、`gohugoio/hugo` 或其他类似的网页模板系统）中进行转换。当用户要求“将 Markdown 转换为 HTML”、“转换 md 文件”、“渲染 Markdown”、“从 Markdown 生成 HTML”或在处理 .md 文件和/或网页模板系统时使用。支持 CLI 和 Node.js 工作流，包括 GFM、CommonMark 和标准 Markdown 格式。'

# Markdown 转 HTML 转换

将 Markdown 文档转换为 HTML 的专业技能，或编写数据转换脚本；在此情况下，脚本类似于 [markedJS/marked](references/marked.md) 仓库。对于自定义脚本，知识不仅限于 `marked.js`，还使用来自工具如 [pandoc](https://github.com/jgm/pandoc) 和 [gomarkdown/markdown](https://github.com/gomarkdown/markdown) 的数据转换方法；[jekyll/jekyll](https://github.com/jekyll/jekyll) 和 [gohugoio/hugo](https://github.com/gohugoio/hugo) 用于模板系统。

### 转换 Markdown 到 HTML 的场景

- 用户要求“将 Markdown 转换为 HTML”或“转换 md 文件”
- 用户希望“将 Markdown 渲染为 HTML 输出”
- 用户需要从 .md 文件生成 HTML 文档
- 用户正在构建静态网站
- 用户正在构建将 Markdown 转换为 HTML 的模板系统
- 用户正在开发现有模板系统的工具、小部件或自定义模板
- 用户希望预览 Markdown 的渲染结果

## 转换 Markdown 到 HTML

### 基础转换

更多信息请参见 [basic-markdown-to-html.md](references/basic-markdown-to-html.md)

```text
    ```markdown
    # Level 1
    ## Level 2

    一句带有 [链接](https://example.com) 的句子，以及一个 HTML 片段如 `<p>paragraph tag</p>`。

    - `ul` 列表项 1
    - `ul` 列表项 2

    1. `ol` 列表项 1
    2. `ol` 列表项 1

    | 表头 1 | 表头 2 |
    | ------------- | ------------- |
    | 内容单元格 1 | 内容单元格 1 |
    | 内容单元格 2 | 内容单元格 2 |

    ```js
    var one = 1;
    var two = 2;

    function simpleMath(x, y) {
     return x + y;
    }
    console.log(simpleMath(one, two));
    ```
    ```

    ```html
    <h1>Level 1</h1>
    <h2>Level 2</h2>

    <p>一句带有 <a href="https://example.com">链接</a> 的句子，以及一个 HTML 片段如 <code>&lt;p&gt;paragraph tag&lt;/p&gt;</code>。</p>

    <ul>
     <li>`ul` 列表项 1</li>
     <li>`ul` 列表项 2</li>
    </ul>

    <ol>
     <li>`ol` 列表项 1</li>
     <li>`ol` 列表项 2</li>
    </ol>

    <table>
     <thead><tr><th>表头 1</th><th>表头 2</th></tr></thead>
     <tbody>
      <tr><td>内容单元格 1</td><td>内容单元格 1</td></tr>
      <tr><td>内容单元格 2</td><td>内容单元格 2</td></tr>
     </tbody>
    </table>

    <pre>
     <code>var one = 1;
     var two = 2;

     function simpleMath(x, y) {
      return x + y;
     }
     console.log(simpleMath(one, two));</code>
    </pre>
    ```
```

### 代码块转换

更多信息请参见 [code-blocks-to-html.md](references/code-blocks-to-html.md)

```text
    ```markdown
    your code here
    ```

    ```html
    <pre><code class="language-md">
    your code here
    </code></pre>
    ```

    ```js
    console.log("Hello world");
    ```

    ```html
    <pre><code class="language-js">
    console.log("Hello world");
    </code></pre>
    ```

    ```markdown
      ```

      ```
      可见的反引号
      ```

      ```
    ```

    ```html
      <pre><code>
      ```

      可见的反引号

      ```
      </code></pre>
    ```
```

### 折叠部分转换

更多信息请参见 [collapsed-sections-to-html.md](references/collapsed-sections-to-html.md)

```text
    ```markdown
    <details>
    <summary>更多信息</summary>

    ### 内部标题

    - 列表
    - **格式化**
    - 代码块

        ```js
        console.log("Hello");
        ```

    </details>
    ```

    ```html
    <details>
    <summary>更多信息</summary>

    <h3>内部标题</h3>

    <ul>
     <li>列表</li>
     <li><strong>格式化</strong></li>
     <li>代码块</li>
    </ul>

    <pre>
     <code class="language-js">console.log("Hello");</code>
    </pre>

    </details>
    ```
```

### 数学表达式转换

更多信息请参见 [writing-mathematical-expressions-to-html.md](references/writing-mathematical-expressions-to-html.md)

```text
    ```markdown
    这句话使用 `$` 符号来显示内联数学公式：$\sqrt{3x-1}+(1+x)^2$
    ```

    ```html
    <p>这句话使用 <code>$</code> 符号来显示内联数学公式：
     <math-renderer><math xmlns="http://www.w3.org/1998/Math/MathML">
      <msqrt><mn>3</mn><mi>x</mi><mo>−</mo><mn>1</mn></msqrt>
      <mo>+</mo><mo>(</mo><mn>1</mn><mo>+</mo><mi>x</mi>
      <msup><mo>)</mo><mn>2</mn></msup>
     </math>
    </math-renderer></p>
    ```

    ```markdown
    **柯西-施瓦茨不等式**\
    $$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$
    ```

    ```html
    <p><strong>柯西-施瓦茨不等式</strong><br>
     <math-renderer>
      <math xmlns="http://www.w3.org/1998/Math/MathML">
       <msup>
        <mrow><mo>(</mo>
         <munderover><mo data-mjx-texclass="OP">∑</mo>
          <mrow><mi>k</mi><mo>=</mo><mn>1</mn></mrow><mi>n</mi>
         </munderover>
         <msub><mi>a</mi><mi>k</mi></msub>
         <msub><mi>b</mi><mi>k</mi></msub>
         <mo>)</mo>
        </mrow>
        <mn>2</mn>
       </msup>
       <mo>≤</mo>
       <mrow><mo>(</mo>
        <munderover><mo>∑</mo>
         <mrow><mi>k</mi><mo>=</mo><mn>1</mn></mrow>
         <mi>n</mi>
        </munderover>
        <msubsup><mi>a</mi><mi>k</mi><mn>2</mn></msubsup>
        <mo>)</mo>
       </mrow>
       <mrow><mo>(</mo>
         <munderover><mo>∑</mo>
          <mrow><mi>k</mi><mo>=</mo><mn>1</mn></mrow>
          <mi>n</mi>
         </munderover>
         <msubsup><mi>b</mi><mi>k</mi><mn>2</mn></msubsup>
         <mo>)</mo>
       </mrow>
      </math>
     </math-renderer></p>
    ```
```

## 使用 [`markedJS/marked`](references/marked.md)

### 前提条件

- 安装 Node.js（用于 CLI 或编程方式使用）
- 全局安装 marked：`npm install -g marked`
- 或本地安装：`npm install marked`

### 快速转换方法

更多信息请参见 [marked.md](references/marked.md) **快速转换方法**

### 分步工作流

更多信息请参见 [marked.md](references/marked.md) **分步工作流**

### CLI 配置

使用配置文件：

```json
{
  "gfm": true,
  "breaks": true
}
```

或使用自定义配置：

```bash
marked -i input.md -o output.html -c config.json
```

### CLI 选项参考

| 选项 | 描述 |
|------|------|
| `-i, --input <文件>` | 输入 Markdown 文件 |
| `-o, --output <文件>` | 输出 HTML 文件 |
| `-s, --string <字符串>` | 解析字符串而非文件 |
| `-c, --config <文件>` | 使用自定义配置文件 |
| `--gfm` | 启用 GitHub 味 Markdown |
| `--breaks` | 将换行转换为 `<br>` |
| `--help` | 显示所有选项 |

### 安全警告

⚠️ **marked 不会净化输出 HTML。** 对于不可信输入，请使用净化器：

```javascript
import { marked } from 'marked';
import DOMPurify from 'dompurify';

const unsafeHtml = marked.parse(untrustedMarkdown);
const safeHtml = DOMPurify.sanitize(unsafeHtml);
```

推荐的净化器：

- [DOMPurify](https://github.com/cure53/DOMPurify)
- [sanitize-html](https://github.com/apostrophecms/sanitize-html)
- [js-xss](https://github.com/leizongmin/js-xss)

### 支持的 Markdown 格式

| 格式 | 支持程度 |
|------|----------|
| 原始 Markdown | 100% |
| CommonMark 0.31 | 98% |
| GitHub 味 Markdown | 97% |

### 常见问题排查

| 问题 | 解决方案 |
|------|----------|
| 文件开头的特殊字符未解析 | 使用 `content.replace(/^[\u200B\u200C\u200D\uFEFF]/,"")` 去除零宽字符 |
| 代码块未高亮 | 集成语法高亮器如 Chroma |
| 表格未渲染 | 确保启用了 `gfm: true` 选项 |
| 换行被忽略 | 在选项中设置 `breaks: true` |
| XSS 漏洞 | 使用 Bluemonday 净化输出 |

## 使用 [`pandoc`](references/pandoc.md)

### 前提条件

- 安装 Pandoc（从 <https://pandoc.org/installing.html> 下载）
- 对于 PDF 输出：安装 LaTeX（MacTeX 用于 macOS，MiKTeX 用于 Windows，texlive 用于 Linux）
- 有终端/命令提示符访问权限

### 快速转换方法

#### 方法 1：CLI 基础转换

```bash
# 将 Markdown 转换为 HTML
pandoc input.md -o output.html

# 生成带页眉/页脚的独立文档
pandoc input.md -s -o output.html

# 显式指定格式
pandoc input.md -f markdown -t html -s -o output.html
```

#### 方法 2：过滤模式（交互式）

```bash
# 启动 pandoc 作为过滤器
pandoc

# 输入 Markdown，然后按 Ctrl-D（Linux/macOS）或 Ctrl-Z+Enter（Windows）
Hello *pandoc*!
# 输出: <p>Hello <em>pandoc</em>!</p>
```

#### 方法 3：格式转换

```bash
# 从 HTML 转换为 Markdown
pandoc -f html -t markdown input.html -o output.md

# 从 Markdown 转换为 LaTeX
pandoc input.md -s -o output.tex

# 从 Markdown 转换为 PDF（需要 LaTeX）
pandoc input.md -s -o output.pdf

# 从 Markdown 转换为 Word
pandoc input.md -s -o output.docx
```

### CLI 配置

| 命令 | 描述 |
|------|------|
| `jekyll new <路径>` | 创建新 Jekyll 站点 |
| `jekyll build` | 构建站点到 `_site` 目录 |
| `jekyll serve` | 启动本地开发服务器 |
| `jekyll clean` | 删除生成的文件 |
| `jekyll doctor` | 检查配置问题 |

| 服务选项 | 描述 |
|----------|------|
| `--livereload` | 文件更改时刷新浏览器 |
| `--drafts` | 包含草稿文章 |
| `--port <端口>` | 设置服务器端口（默认：4000） |
| `--host <主机>` | 设置服务器主机（默认：localhost） |
| `--baseurl <URL>` | 设置基础 URL |

### 安全警告

⚠️ **Jekyll 的安全注意事项：**

- 生产环境中避免使用 `safe: false`
- 在 `_config.yml` 中使用 `exclude` 防止敏感文件发布
- 接受外部输入时净化用户生成内容
- 保持 Jekyll 和插件更新

```yaml
# _config.yml 安全设置
exclude:
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor
```

### 支持的 Markdown 格式

| 格式 | 支持程度 |
|------|----------|
| Kramdown（默认） | 100% |
| CommonMark | 通过插件（jekyll-commonmark） |
| GitHub 味 Markdown | 通过插件（jekyll-commonmark-ghpages） |
| RedCarpet | 通过插件（已弃用） |

在 `_config.yml` 中配置 Markdown 处理器：

```yaml
markdown: kramdown
kramdown:
  input: GFM
  syntax_highlighter: rouge
```

### 常见问题排查

| 问题 | 解决方案 |
|------|----------|
| 路径找不到 | 检查 `baseURL` 配置 |
| 主题未加载 | 验证主题是否在 `themes/` 或 Hugo 模块中 |
| 构建缓慢 | 使用 `--templateMetrics` 识别瓶颈 |
| 原始 HTML 未渲染 | 在 goldmark 配置中设置 `unsafe = true` |
| 图像未加载 | 检查 `static/` 文件夹结构 |
| 模块错误 | 运行 `hugo mod tidy` |

## 参考资料

### Markdown 编写与样式

- [basic-markdown.md](references/basic-markdown.md)
- [code-blocks.md](references/code-blocks.md)
- [collapsed-sections.md](references/collapsed-sections.md)
- [tables.md](references/tables.md)
- [writing-mathematical-expressions.md](references/writing-mathematical-expressions.md)
- Markdown 指南：[https://www.markdownguide.org/basic-syntax/](https://www.markdownguide.org/basic-syntax/)
- Markdown 样式：[https://github.com/sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css)

### [`markedJS/marked`](references/marked.md)

- 官方文档：[https://marked.js.org/](https://marked.js.org/)
- 高级选项：[https://marked.js.org/using_advanced](https://marked.js.org/using_advanced)
- 可扩展性：[https://marked.js.org/using_pro](https://marked.js.org/using_pro)
- GitHub 仓库：[https://github.com/markedjs/marked](https://github.com/markedjs/marked)

### [`pandoc`](references/pandoc.md)

- 入门指南：[https://pandoc.org/getting-started.html](https://pandoc.org/getting-started.html)
- 官方文档：[https://pandoc.org/MANUAL.html](https://pandoc.org/MANUAL.html)
- 可扩展性：[https://pandoc.org/extras.html](https://pandoc.org/extras.html)
- GitHub 仓库：[https://github.com/jgm/pandoc](https://github.com/jgm/pandoc)

### [`gomarkdown/markdown`](references/gomarkdown.md)

- 官方文档：[https://pkg.go.dev/github.com/gomarkdown/markdown](https://pkg.go.dev/github.com/gomarkdown/markdown)
- 高级配置：[https://pkg.go.dev/github.com/gomarkdown/markdown@v0.0.0-20250810172220-2e2c11897d1a/html](https://pkg.go.dev/github.com/gomarkdown/markdown@v0.0.0-20250810172220-2e2c11897d1a/html)
- Markdown 处理：[https://blog.kowalczyk.info/article/cxn3/advanced-markdown-processing-in-go.html](https://blog.kowalczyk.info/article/cxn3/advanced-markdown-processing-in-go.html)
- GitHub 仓库：[https://github.com/gomarkdown/markdown](https://github.com/gomarkdown/markdown)

### [`jekyll`](references/jekyll.md)

- 官方文档：[https://jekyllrb.com/docs/](https://jekyllrb.com/docs/)
- 配置选项：[https://jekyllrb.com/docs/configuration/options/](https://jekyllrb.com/docs/configuration/options/)
- 插件：[https://jekyllrb.com/docs/plugins/](https://jekyllrb.com/docs/plugins/)
  - [安装](https://jekyllrb.com/docs/plugins/installation/)
  - [生成器](https://jekyllrb.com/docs/plugins/generators/)
  - [转换器](https://jekyllrb.com/docs/plugins/converters/)
  - [命令](https://jekyllrb.com/docs/plugins/commands/)
  - [标签](https://jekyllrb.com/docs/plugins/tags/)
  - [过滤器](https://jekyllrb.com/docs/plugins/filters/)
  - [钩子](https://jekyllrb.com/docs/plugins/hooks/)
- GitHub 仓库：[https://github.com/jekyll/jekyll](https://github.com/jekyll/jekyll)

### [`hugo`](references/hugo.md)

- 官方文档：[https://gohugo.io/documentation/](https://gohugo.io/documentation/)
- 所有设置：[https://gohugo.io/configuration/all/](https://gohugo.io/configuration/all/)
- 编辑器插件：[https://gohugo.io/tools/editors/](https://gohugo.io/tools/editors/)
- GitHub 仓库：[https://github.com/gohugoio/hugo](https://github.com/gohugoio/hugo)

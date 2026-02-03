# 基础 Markdown 转 HTML

## 标题

### Markdown

```md
# Basic writing and formatting syntax
```

### 解析后的 HTML

```html
<h1>Basic writing and formatting syntax</h1>
```

```md
## Headings
```

```html
<h2>Headings</h2>
```

```md
### A third-level heading
```

```html
<h3>A third-level heading</h3>
```

### Markdown

```md
Heading 2
---
```

### 解析后的 HTML

```html
<h2>Heading 2</h2>
```

---

## 段落

### Markdown

```md
Create sophisticated formatting for your prose and code on GitHub with simple syntax.
```

### 解析后的 HTML

```html
<p>Create sophisticated formatting for your prose and code on GitHub with simple syntax.</p>
```

---

## 行内格式

### 加粗

```md
**This is bold text**
```

```html
<strong>This is bold text</strong>
```

---

### 斜体

```md
_This text is italicized_
```

```html
<em>This text is italicized</em>
```

---

### 加粗 + 斜体

```md
***All this text is important***
```

```html
<strong><em>All this text is important</em></strong>
```

---

### 删除线（GFM）

```md
~~This was mistaken text~~
```

```html
<del>This was mistaken text</del>
```

---

### 下标 / 上标（原始 HTML 透传）

```md
This is a <sub>subscript</sub> text
```

```html
<p>This is a <sub>subscript</sub> text</p>
```

```md
This is a <sup>superscript</sup> text
```

```html
<p>This is a <sup>superscript</sup> text</p>
```

---

## 引用块

### Markdown

```md
> Text that is a quote
```

### 解析后的 HTML

```html
<blockquote>
  <p>Text that is a quote</p>
</blockquote>
```

---

### GitHub 提示（NOTE）

```md
> [!NOTE]
> Useful information.
```

```html
<blockquote class="markdown-alert markdown-alert-note">
  <p><strong>Note</strong></p>
  <p>Useful information.</p>
</blockquote>
```

> ⚠️ `markdown-alert-*` 类是 GitHub 特有的，不是标准 Markdown。

---

## 行内代码

```md
Use `git status` to list files.
```

```html
<p>Use <code>git status</code> to list files.</p>
```

---

## 代码块

### Markdown

````md
```markdown
git status
git add
```
````

### 解析后的 HTML

```html
<pre><code class="language-markdown">
git status
git add
</code></pre>
```

---

## 表格

### Markdown

```md
| Style | Syntax |
|------|--------|
| Bold | ** ** |
```

### 解析后的 HTML

```html
<table>
  <thead>
    <tr>
      <th>Style</th>
      <th>Syntax</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Bold</td>
      <td><strong> </strong></td>
    </tr>
  </tbody>
</table>
```

---

## 链接

### Markdown

```md
[GitHub Pages](https://pages.github.com/)
```

### 解析后的 HTML

```html
<a href="https://pages.github.com/">GitHub Pages</a>
```

---

## 图片

### Markdown

```md
![Alt text](image.png)
```

### 解析后的 HTML

```html
<img src="image.png" alt="Alt text">
```

---

## 列表

### 无序列表

```md
- George Washington
- John Adams
```

```html
<ul>
  <li>George Washington</li>
  <li>John Adams</li>
</ul>
```

---

### 有序列表

```md
1. James Madison
2. James Monroe
```

```html
<ol>
  <li>James Madison</li>
  <li>James Monroe</li>
</ol>
```

---

### 嵌套列表

```md
1. First item
   - Nested item
```

```html
<ol>
  <li>
    First item
    <ul>
      <li>Nested item</li>
    </ul>
  </li>
</ol>
```

---

## 任务列表（GitHub 扩展 Markdown）

```md
- [x] Done
- [ ] Pending
```

```html
<ul>
  <li>
    <input type="checkbox" checked disabled> Done
  </li>
  <li>
    <input type="checkbox" disabled> Pending
  </li>
</ul>
```

---

## 提及

```md
@github/support
```

```html
<a href="https://github.com/github/support" class="user-mention">@github/support</a>
```

---

## 脚注

### Markdown

```md
Here is a footnote[^1].

[^1]: My reference.
```

### 解析后的 HTML

```html
<p>
  Here is a footnote
  <sup id="fnref-1">
    <a href="#fn-1">1</a>
  </sup>.
</p>

<section class="footnotes">
  <ol>
    <li id="fn-1">
      <p>My reference.</p>
    </li>
  </ol>
</section>
```

---

## HTML 注释（隐藏内容）

```md
<!-- This content will not appear -->
```

```html
<!-- This content will not appear -->
```

---

## 转义 Markdown 字符

```md
\*not italic\*
```

```html
<p>*not italic*</p>
```

---

## 表情符号

```md
:+1:
```

```html
<img class="emoji" alt="👍" src="...">
```

（GitHub 会将表情符号替换为 `<img>` 标签。）

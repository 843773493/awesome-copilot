# 折叠部分转HTML

## `<details>` 块（Markdown中的原始HTML）

### Markdown

````md
<details>

<summary>折叠部分的提示</summary>

### 您可以在折叠部分中添加标题

您可以在折叠部分中添加文本。

您还可以添加图片或代码块。

    ```ruby
    puts "Hello World"
    ```

</details>
````

---

### 解析后的HTML

```html
<details>
  <summary>折叠部分的提示</summary>

  <h3>您可以在折叠部分中添加标题</h3>

  <p>您可以在折叠部分中添加文本。</p>

  <p>您还可以添加图片或代码块。</p>

  <pre><code class="language-ruby">
puts "Hello World"
</code></pre>
</details>
```

#### 注意事项：

* 在 `<details>` 标签内的 Markdown 仍会正常解析。
* 通过 `class="language-ruby"` 保留语法高亮。

---

## 默认展开（`open` 属性）

### Markdown

````md
<details open>

<summary>折叠部分的提示</summary>

### 您可以在折叠部分中添加标题

您可以在折叠部分中添加文本。

您还可以添加图片或代码块。

    ```ruby
    puts "Hello World"
    ```

</details>
````

### 解析后的HTML

```html
<details open>
  <summary>折叠部分的提示</summary>

  <h3>您可以在折叠部分中添加标题</h3>

  <p>您可以在折叠部分中添加文本。</p>

  <p>您还可以添加图片或代码块。</p>

  <pre><code class="language-ruby">
puts "Hello World"
</code></pre>
</details>
```

## 关键规则

* `<details>` 和 `<summary>` 是原始 HTML，不是 Markdown 语法
* `<details>` 标签内的 Markdown 仍会正常解析
* 语法高亮在折叠部分中仍能正常工作
* 使用 `<summary>` 作为可点击的标签

## 包含内联HTML与SVG的段落

### Markdown

```md
您可以通过使用 `<details>` 标签创建折叠部分来简化您的 Markdown。
```

### 解析后的HTML

```html
<p>
  您可以通过使用 <code>&lt;details&gt;</code> 标签创建折叠部分来简化您的 Markdown。
</p>
```

---

### Markdown（内联SVG保留）

```md
在 `<details>` 块中的任何 Markdown 都会折叠，直到读者点击 <svg ...></svg> 来展开详细信息。
```

### 解析后的HTML

```html
<p>
  在 <code>&lt;details&gt;</code> 块中的任何 Markdown 都会折叠，直到读者点击
  <svg version="1.1" width="16" height="16" viewBox="0 0 16 16"
       class="octicon octicon-triangle-right"
       aria-label="The right triangle icon"
       role="img">
    <path d="m6.427 4.427 3.396 3.396a.25.25 0 0 1 0 .354l-3.396 3.396A.25.25 0 0 1 6 11.396V4.604a.25.25 0 0 1 .427-.177Z"></path>
  </svg>
  来展开详细信息。
</p>
```

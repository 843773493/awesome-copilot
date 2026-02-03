# 使用折叠部分组织信息

你可以通过使用 `<details>` 标签创建折叠部分来简化你的 Markdown 文档。

## 创建折叠部分

你可以通过创建一个可折叠的部分来暂时隐藏 Markdown 中的某些内容，读者可以选择展开该部分。例如，当你想在问题评论中包含一些技术细节，而这些细节可能对并非所有读者都相关或有趣时，你可以将这些细节放入一个折叠部分中。

在 `<details>` 块中的任何 Markdown 内容都会默认折叠，直到读者点击右侧的三角形图标 <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-triangle-right" aria-label="右三角形图标" role="img"><path d="m6.427 4.427 3.396 3.396a.25.25 0 0 1 0 .354l-3.396 3.396A.25.25 0 0 1 6 11.396V4.604a.25.25 0 0 1 .427-.177Z"></path></svg> 展开内容。

在 `<details>` 块中，使用 `<summary>` 标签告知读者该部分包含什么内容。标签文字会显示在右侧的三角形图标旁边。

````markdown
<details>

<summary>折叠部分的提示</summary>

### 你可以添加标题

你可以在折叠部分中添加文本。

你也可以添加图片或代码块。

```ruby
   puts "Hello World"
```

</details>
````

在 `<summary>` 标签中的 Markdown 内容默认是折叠的：

![在 GitHub 上渲染的此页面上上述 Markdown 的截图，显示一个向右的箭头和标题“折叠部分的提示”](https://docs.github.com/assets/images/help/writing/collapsed-section-view.png)

当读者点击右侧的三角形图标 <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-triangle-right" aria-label="右三角形图标" role="img"><path d="m6.427 4.427 3.396 3.396a.25.25 0 0 1 0 .354l-3.396 3.396A.25.25 0 0 1 6 11.396V4.604a.25.25 0 0 1 .427-.177Z"></path></svg> 后，内容会展开：

![在 GitHub 上渲染的此页面上上述 Markdown 的截图。折叠部分包含标题、文本、图片和代码块](https://docs.github.com/assets/images/help/writing/open-collapsed-section.png)

可选地，若要使该部分默认显示为展开状态，可以向 `<details>` 标签添加 `open` 属性：

```html
<details open>
```

## 进一步阅读

* [GitHub Flavored Markdown 规范](https://github.github.com/gfm/)
* [基本的写作和格式化语法](https://docs.github.com/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

# 创建和突出显示代码块

通过带围栏的代码块分享代码示例，并启用语法高亮功能。

## 带围栏的代码块

您可以通过在代码块前后放置三个反引号 <code>\`\`\`</code> 来创建带围栏的代码块。我们建议在代码块前后留出空行，以便更容易阅读原始格式。

````text
```
function test() {
  console.log("notice the blank line before this function?");
}
```
````

![显示在 GitHub Markdown 中使用三个反引号创建代码块的截图。代码块以 "function test() {." 开始。](https://docs.github.com/assets/images/help/writing/fenced-code-block-rendered.png)

> \[!TIP]
> 为了在列表中保留格式，确保在非带围栏的代码块中使用八个空格缩进。

要在带围栏的代码块中显示三个反引号，请将其包裹在四个反引号中。

`````text
````
```
Look! You can see my backticks.
```
````
`````

![显示在 Markdown 中使用四个反引号包裹三个反引号以在渲染内容中显示的截图。](https://docs.github.com/assets/images/help/writing/fenced-code-show-backticks-rendered.png)

如果您经常编辑代码片段和表格，建议在 GitHub 的所有评论字段中启用固定宽度字体。如需更多信息，请参阅 [关于 GitHub 上的写作和格式化](https://docs.github.com/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/about-writing-and-formatting-on-github#enabling-fixed-width-fonts-in-the-editor)。

## 语法高亮

<!-- 如果您对本功能进行了更改，请检查是否影响了 /get-started/learning-about-github/github-language-support 中列出的语言。如果有影响，请相应更新语言支持文章。 -->

您可以在带围栏的代码块中添加一个可选的语言标识符，以启用语法高亮功能。

语法高亮会更改源代码的颜色和样式，使其更易于阅读。

例如，要对 Ruby 代码进行语法高亮：

````text
```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
```
````

这将显示带有语法高亮的代码块：

![GitHub 上显示的三行 Ruby 代码。代码元素以紫色、蓝色和红色字体显示，便于扫描。](https://docs.github.com/assets/images/help/writing/code-block-syntax-highlighting-rendered.png)

> \[!TIP]
> 当您在 GitHub 页面上创建需要语法高亮的带围栏代码块时，请使用小写语言标识符。如需更多信息，请参阅 [关于 GitHub 页面和 Jekyll](https://docs.github.com/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll#syntax-highlighting)。

我们使用 [Linguist](https://github.com/github-linguist/linguist) 来执行语言检测，并选择用于语法高亮的 [第三方语法定义](https://github.com/github-linguist/linguist/blob/main/vendor/README.md)。您可以在 [语言的 YAML 文件](https://github.com/github-linguist/linguist/blob/main/lib/linguist/languages.yml) 中找到哪些关键字是有效的。

## 创建图表

您还可以使用代码块在 Markdown 中创建图表。GitHub 支持 Mermaid、GeoJSON、TopoJSON 和 ASCII STL 语法。如需更多信息，请参阅 [创建图表](https://docs.github.com/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)。

## 进一步阅读

* [GitHub Flavored Markdown 规范](https://github.github.com/gfm/)
* [基本写作和格式化语法](https://docs.github.com/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

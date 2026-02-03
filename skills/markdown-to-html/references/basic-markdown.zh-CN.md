# 基础写作和格式化语法

使用简单的语法在 GitHub 上为您的文字和代码创建复杂的格式。

## 标题

要创建标题，请在标题文字前添加一到六个 <kbd>#</kbd> 符号。您使用的 <kbd>#</kbd> 数量将决定标题的层级和字体大小。

```markdown
# 一级标题
## 二级标题
### 三级标题
```

![渲染后的 GitHub Markdown 截图，显示了 h1、h2 和 h3 标题示例，它们在字体大小和视觉重量上逐渐减小以展示层级关系。](https://docs.github.com/assets/images/help/writing/headings-rendered.png)

当您使用两个或多个标题时，GitHub 会自动为您生成一个目录，您可以通过点击文件页眉中的 "Outline"（大纲）菜单图标 <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-list-unordered" aria-label="目录" role="img"><path d="M5.75 2.5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5Zm0 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5Zm0 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5ZM2 14a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042-.018.751.751 0 0 1-.018-1.042Z"></path></svg> 来查看生成的锚点。每个标题都会在目录中列出，您可以点击标题跳转到相应部分。

![仓库的 README 文件截图。在某一节标题左侧，一个链接图标以深橙色勾勒。](https://docs.github.com/assets/images/help/repository/readme-links.png)

如果您需要确定正在编辑的文件中某个标题的锚点，可以使用以下基本规则：

* 字母会转换为小写。
* 空格会被替换为短横线 (`-`)，其他任何空白或标点字符都会被移除。
* 首尾的空白会被移除。
* 格式化标记会被移除，只保留内容（例如，`_斜体_` 会变成 `斜体`）。
* 如果某个标题的自动生成功能锚点与文档中之前的锚点相同，会通过添加短横线和一个自动递增的整数来生成一个唯一的标识符。

有关 URI 片段要求的更详细信息，请参阅 [RFC 3986: 统一资源标识符 (URI): 通用语法，第 3.5 节](https://www.rfc-editor.org/rfc/rfc3986#section-3.5)。

以下代码块演示了在渲染内容中从标题生成锚点所使用的规则。

```markdown
# 示例标题

## 示例章节

## This'll be a _Helpful_ Section About the Greek Letter Θ!
一个包含不允许在片段中使用的字符、UTF-8 字符、两个单词之间连续两个空格和格式化内容的标题。

## This heading is not unique in the file

TEXT 1

## This heading is not unique in the file

TEXT 2

# 链接到上面的示例标题

链接到示例章节：[链接文本](#sample-section)。

链接到帮助章节：[链接文本](#thisll-be-a-helpful-section-about-the-greek-letter-Θ)。

链接到第一个非唯一章节：[链接文本](#this-heading-is-not-unique-in-the-file)。

链接到第二个非唯一章节：[链接文本](#this-heading-is-not-unique-in-the-file-1)。
```

> \[!NOTE]
> 如果您编辑了标题，或者更改了具有“相同”锚点的标题顺序，您还需要更新所有指向这些标题的链接，因为锚点会随之改变。

## 相对链接

您可以在渲染文件中定义相对链接和图片路径，以帮助读者导航到仓库中的其他文件。

相对链接是相对于当前文件的链接。例如，如果您在仓库的根目录中有一个 README 文件，并且在 *docs/CONTRIBUTING.md* 中有另一个文件，那么在 README 中指向 *CONTRIBUTING.md* 的相对链接可能如下所示：

```text
[该项目的贡献指南](docs/CONTRIBUTING.md)
```

GitHub 会根据您当前所在的分支自动转换相对链接或图片路径，以确保链接始终有效。链接路径相对于当前文件。以 `/` 开头的链接会相对于仓库根目录。

您还可以使用所有相对链接操作符，例如 `./` 和 `../`。

您的链接文本应位于单行中。以下示例将无法正常工作。

```markdown
[Contribution
guidelines for this project](docs/CONTRIBUTING.md)
```

在仓库中使用相对链接对克隆仓库的用户来说更为便捷。绝对链接在克隆仓库中可能无法正常工作，我们建议使用相对链接来引用仓库中的其他文件。

## 自定义锚点

您可以使用标准的 HTML 锚点标签 (`<a name="unique-anchor-name"></a>`) 来为文档中的任何位置创建导航锚点。为了避免歧义引用，请为锚点标签使用独特的命名方案，例如在 `name` 属性值前添加前缀。

> \[!NOTE]
> 自定义锚点不会包含在文档大纲/目录中。

您可以使用给锚点的 `name` 属性值来链接到自定义锚点。语法与链接到自动为标题生成的锚点完全相同。

例如：

```markdown
# 节标题

本节的正文内容。

<a name="my-custom-anchor-point"></a>
我想要直接链接到但没有自己标题的文本。

(…更多内容…)

[链接到该自定义锚点](#my-custom-anchor-point)
```

> \[!TIP]
> 自定义锚点不会被自动标题链接的命名和编号行为考虑。

## 换行

如果您在仓库的 Issues、Pull Requests 或 Discussions 中撰写内容，GitHub 会自动渲染换行：

```markdown
这是一个示例
会跨越两行
```

然而，如果您在 .md 文件中撰写内容，上面的示例将渲染为一行，没有换行。要在 .md 文件中创建换行，您需要在第一行末尾添加两个空格：

```markdown
这是一个示例&nbsp;&nbsp;
会跨越两行
```

或者在第一行末尾添加一个反斜杠：

```markdown
这是一个示例\
会跨越两行
```

或者在第一行末尾添加一个 HTML 单行换行标签：

```markdown
这是一个示例<br/>
会跨越两行
```

如果您在两行之间留有空行，那么 .md 文件和 Issues、Pull Requests、Discussions 中的 Markdown 都会将这两行用空行分隔：

```markdown
这是一个示例

会用空行分隔这两行
```

## 图片

您可以通过在图片描述文字中添加 <kbd>!</kbd> 并用 `[ ]` 包裹来显示图片。

`@octocat :+1: 这个 PR 看起来很棒 - 可以合并了！ :shipit:`

![渲染后的 GitHub Markdown 截图，显示了 +1 和 shipit 的表情符号代码如何渲染为表情符号。](https://docs.github.com/assets/images/help/writing/emoji-rendered.png)

输入 <kbd>:</kbd> 会弹出一个建议的表情符号列表。随着您输入，列表会进行过滤，找到您要的表情符号后，按 **Tab** 或 **Enter** 键完成选择。

有关所有可用表情符号和代码的完整列表，请参阅 [表情符号速查表](https://github.com/ikatyang/emoji-cheat-sheet/blob/github-actions-auto-update/README.md)。

## 段落

您可以通过在文本行之间留出空行来创建新段落。

## 脚注

您可以使用以下括号语法向内容添加脚注：

```text
这是一个简单的脚注[^1]。

脚注也可以有多个行[^2]。

[^1]: 我的参考。
[^2]: 要在脚注中添加换行，请在行末添加两个空格。  
这是第二行。
```

脚注将渲染如下：

![渲染后的 Markdown 截图，显示了用于指示脚注的上标数字，以及脚注中的可选换行。](https://docs.github.com/assets/images/help/writing/footnote-rendered.png)

> \[!NOTE]
> 您的 Markdown 中脚注的位置不会影响脚注的渲染位置。您可以在引用脚注后立即写脚注，脚注仍会渲染在 Markdown 的底部。脚注不支持在维基中使用。

## 警告

**警告**（也称为 **提示** 或 **警示**）是一种基于块引用语法的 Markdown 扩展，可用于强调关键信息。在 GitHub 上，它们会以独特的颜色和图标显示，以表明内容的重要性。

仅在用户成功至关重要的情况下使用警告，并且每篇文章中限制使用一到两个，以避免让读者感到信息过载。此外，您应避免连续使用警告。警告不能嵌套在其他元素中。

要添加警告，请使用一个特殊行指定警告类型，然后在标准块引用中添加警告信息。有五种类型的警告可用：

```markdown
> [!NOTE]
> 即使在快速浏览内容时，用户也应了解的重要信息。

> [!TIP]
> 有助于更好地或更轻松地完成任务的建议。

> [!IMPORTANT]
> 用户实现目标所需的关键信息。

> [!WARNING]
> 需要用户立即关注以避免问题的紧急信息。

> [!CAUTION]
> 提醒用户某些操作可能带来的风险或负面结果。
```

以下是渲染后的警告：

![渲染后的 Markdown 警告截图，显示 Note、Tip、Important、Warning 和 Caution 以不同颜色的文本和图标呈现。](https://docs.github.com/assets/images/help/writing/alerts-rendered.png)

## 使用注释隐藏内容

您可以通过将内容放在 HTML 注释中来告诉 GitHub 不在渲染的 Markdown 中显示该内容。

```text
<!-- 此内容不会出现在渲染的 Markdown 中 -->
```

## 忽略 Markdown 格式

您可以通过在 Markdown 字符前使用 <kbd>\\</kbd> 来告诉 GitHub 忽略（或转义）Markdown 格式。

`Let's rename \*our-new-project\* to \*our-old-project\*.`

![渲染后的 GitHub Markdown 截图，显示反斜杠如何防止星号被转换为斜体。](https://docs.github.com/assets/images/help/writing/escaped-character-rendered.png)

有关反斜杠的更多信息，请参阅 Daring Fireball 的 [Markdown 语法](https://daringfireball.net/projects/markdown/syntax#backslash)。

> \[!NOTE]
> 在问题或拉取请求的标题中，Markdown 格式不会被忽略。

## 禁用 Markdown 渲染

在查看 Markdown 文件时，您可以点击文件顶部的 **Code**（代码）按钮，以禁用 Markdown 渲染并查看文件的源代码。

![仓库中 Markdown 文件的截图，显示了与文件交互的选项。一个标记为“Code”的按钮以深橙色勾勒。](https://docs.github.com/assets/images/help/writing/display-markdown-as-source-global-nav-update.png)

禁用 Markdown 渲染可让您使用源视图功能，例如行链接，这些功能在查看渲染后的 Markdown 文件时无法实现。

## 进一步阅读

*[GitHub Flavored Markdown 规范](https://github.github.com/gfm/)
*[关于 GitHub 上的写作和格式化](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/about-writing-and-formatting-on-github)
*[使用高级格式化](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting)
*[GitHub 写作快速入门](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github)

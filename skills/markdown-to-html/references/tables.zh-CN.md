# 使用表格组织信息

您可以在评论、问题、拉取请求和维基页面中使用表格来组织信息。

## 创建表格

您可以使用竖线 `|` 和破折号 `-` 来创建表格。破折号用于创建每一列的表头，而竖线则用于分隔各列。为了确保表格正确渲染，您必须在表格前添加一个空行。

```markdown
| 第一列标题  | 第二列标题 |
| ------------- | ------------- |
| 内容单元格  | 内容单元格  |
| 内容单元格  | 内容单元格  |
```

![GitHub Markdown 表格的截图，显示为两列等宽。表头以粗体显示，交替的内容行带有灰色背景。](https://docs.github.com/assets/images/help/writing/table-basic-rendered.png)

表格两侧的竖线是可选的。

单元格的宽度可以不同，不需要在列内完全对齐。表头行的每一列必须至少包含三个破折号。

```markdown
| 命令 | 描述 |
| --- | --- |
| git status | 列出所有 *新或修改* 的文件 |
| git diff | 显示尚未暂存的文件差异 |
```

![GitHub Markdown 表格的截图，显示两列宽度不同的表格。行中列出命令 "git status" 和 "git diff" 及其描述。](https://docs.github.com/assets/images/help/writing/table-varied-columns-rendered.png)

如果您经常编辑代码片段和表格，建议在 GitHub 的所有评论字段中启用固定宽度字体。如需了解更多信息，请参阅 [关于 GitHub 上的写作和格式化](https://docs.github.com/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/about-writing-and-formatting-on-github#enabling-fixed-width-fonts-in-the-editor)。

## 表格内的内容格式化

您可以在表格中使用格式化内容，如链接、内联代码块和文本样式：

```markdown
| 命令 | 描述 |
| --- | --- |
| `git status` | 列出所有 *新或修改* 的文件 |
| `git diff` | 显示尚未暂存的文件差异 |
```

![GitHub Markdown 表格的截图，命令以代码块形式显示。描述中使用了粗体和斜体格式。](https://docs.github.com/assets/images/help/writing/table-inline-formatting-rendered.png)

您可以通过在表头行的破折号左侧、右侧或两侧添加冒号 `:` 来对齐文本到列的左侧、右侧或居中。

```markdown
| 左对齐 | 居中对齐 | 右对齐 |
| :---         |     :---:      |          ---: |
| git status   | git status     | git status    |
| git diff     | git diff       | git diff      |
```

![GitHub 渲染的 Markdown 表格截图，显示三列的对齐方式：左对齐、居中对齐和右对齐。](https://docs.github.com/assets/images/help/writing/table-aligned-text-rendered.png)

若要在单元格中包含竖线 `|`，请在竖线前使用反斜杠 `\` 进行转义：

```markdown
| 名称     | 字符 |
| ---      | ---       |
| 反引号 | `         |
| 竖线     | \|        |
```

![GitHub 渲染的 Markdown 表格截图，显示如何通过反斜杠转义竖线，使其作为内容显示而非单元格分隔符。](https://docs.github.com/assets/images/help/writing/table-escaped-character-rendered.png)

## 进一步阅读

* [GitHub Flavored Markdown 规范](https://github.github.com/gfm/)
* [基本的写作和格式化语法](https://docs.github.com/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

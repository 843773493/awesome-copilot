# 编写数学表达式

使用Markdown在GitHub上显示数学表达式。

## 关于编写数学表达式

为了实现数学表达式的清晰交流，GitHub支持在Markdown中使用LaTeX格式的数学表达式。更多信息，请参阅Wikibooks上的[LaTeX/Mathematics](http://en.wikibooks.org/wiki/LaTeX/Mathematics)。

GitHub的数学表达式渲染功能使用了MathJax，这是一个开源的基于JavaScript的显示引擎。MathJax支持广泛的LaTeX宏命令，并包含多个有用的可访问性扩展。更多信息，请参阅[MathJax文档](http://docs.mathjax.org/en/latest/input/tex/index.html#tex-and-latex-support)和[MathJax可访问性扩展文档](https://mathjax.github.io/MathJax-a11y/docs/#reader-guide)。

数学表达式渲染功能可在GitHub Issues、GitHub Discussions、拉取请求、维基和Markdown文件中使用。

## 编写内联表达式

有两种方法可以将数学表达式与文本内联显示。您可以使用美元符号（`$`）包围表达式，或者在表达式前使用<code>$\`</code>并在表达式后使用<code>\`$</code>。后者语法在表达式中包含与Markdown语法重叠的字符时非常有用。更多信息，请参阅[基本写作和格式化语法](https://docs.github.com/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)。

```text
此句子使用 `$` 符号来显示内联数学表达式：$\sqrt{3x-1}+(1+x)^2$
```

![显示内联数学表达式的渲染Markdown截图：3x减1的平方根加上（1加x）的平方。](https://docs.github.com/assets/images/help/writing/inline-math-markdown-rendering.png)

```text
此句子使用 $\` 和 \`$ 符号来显示内联数学表达式：$`\sqrt{3x-1}+(1+x)^2`$
```

![显示使用反引号语法的内联数学表达式的渲染Markdown截图：3x减1的平方根加上（1加x）的平方。](https://docs.github.com/assets/images/help/writing/inline-backtick-math-markdown-rendering.png)

## 编写块级表达式

要将数学表达式作为块级内容显示，请在新的一行开始，并使用两个美元符号 `$$` 包围表达式。

> [!TIP] 如果您正在编写一个.md文件，您需要使用特定的格式来创建换行，例如如下面示例所示在行尾添加反斜杠。有关Markdown中换行的更多信息，请参阅[基本写作和格式化语法](https://docs.github.com/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#line-breaks)。

```text
**柯西-施瓦茨不等式**\
$$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$
```

![显示复杂公式的渲染Markdown截图。上方加粗文本为“柯西-施瓦茨不等式”，下方是不等式的公式。](https://docs.github.com/assets/images/help/writing/math-expression-as-a-block-rendering.png)

或者，您可以使用<code>\`\`\`math</code>代码块语法来显示数学表达式作为块级内容。使用这种语法时，无需使用`$$`符号。以下内容将渲染与上面相同的结果：

````text
**柯西-施瓦茨不等式**

```math
\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)
```
````

## 在数学表达式中显示美元符号

要在数学表达式所在行中显示美元符号，您需要转义非分隔符的`$`符号以确保行正确渲染。

* 在数学表达式中，美元符号前添加反斜杠`\`：

  ```text
  此表达式使用 `\$` 显示美元符号：$`\sqrt{\$4}`$
  ```

  ![显示如何在数学表达式中使用反斜杠前的美元符号的渲染Markdown截图。](https://docs.github.com/assets/images/help/writing/dollar-sign-within-math-expression.png)

* 在数学表达式之外，但同一行中，使用span标签包围显式的`$`符号：

  ```text
  要将 <span>$</span>100 分成两半，我们计算 $100/2$
  ```

  ![显示如何使用span标签包围美元符号以将其显示为内联文本而非数学公式的渲染Markdown截图。](https://docs.github.com/assets/images/help/writing/dollar-sign-inline-math-expression.png)

## 进一步阅读

* [MathJax官网](http://mathjax.org)
* [GitHub上的写作和格式化入门](https://docs.github.com/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github)
* [GitHub Flavored Markdown规范](https://github.github.com/gfm/)

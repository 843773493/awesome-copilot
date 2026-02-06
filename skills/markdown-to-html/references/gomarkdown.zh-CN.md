# gomarkdown/markdown 参考文档

Go 语言库，用于解析 Markdown 并生成 HTML。快速、可扩展且线程安全。

## 安装

```bash
# 添加到您的 Go 项目
go get github.com/gomarkdown/markdown

# 安装 CLI 工具
go install github.com/gomarkdown/mdtohtml@latest
```

## 基本用法

### 简单转换

```go
package main

import (
    "fmt"
    "github.com/gomarkdown/markdown"
)

func main() {
    md := []byte("# Hello World\n\nThis is **bold** text.")
    html := markdown.ToHTML(md, nil, nil)
    fmt.Println(string(html))
}
```

### 使用 CLI 工具

```bash
# 将文件转换为 HTML
mdtohtml input.md output.html

# 输出到标准输出
mdtohtml input.md
```

## 解析器配置

### 常用扩展

```go
import (
    "github.com/gomarkdown/markdown"
    "github.com/gomarkdown/markdown/parser"
)

// 创建带有扩展的解析器
extensions := parser.CommonExtensions | parser.AutoHeadingIDs
p := parser.NewWithExtensions(extensions)

// 解析 Markdown
doc := p.Parse(md)
```

### 可用的解析器扩展

| 扩展 | 描述 |
|-----------|-------------|
| `parser.CommonExtensions` | 表格、带语言的代码块、自动链接、删除线 |
| `parser.Tables` | 支持管道表格 |
| `parser.FencedCode` | 带语言的代码块 |
| `parser.Autolink` | 自动检测 URL |
| `parser.Strikethrough` | ~~删除线~~ 文本 |
| `parser.SpaceHeadings` | 要求标题中的 # 后面有空格 |
| `parser.HeadingIDs` | 自定义标题 ID {#id} |
| `parser.AutoHeadingIDs` | 自动生成标题 ID |
| `parser.Footnotes` | 支持脚注 |
| `parser.NoEmptyLineBeforeBlock` | 块元素前不需要空行 |
| `parser.HardLineBreak` | 换行符转换为 `<br>` |
| `parser.MathJax` | 支持 MathJax |
| `parser.SuperSubscript` | 上标^和下标~ |
| `parser.Mmark` | 支持 Mmark 语法 |

## HTML 渲染器配置

### 常用标志

```go
import (
    "github.com/gomarkdown/markdown"
    "github.com/gomarkdown/markdown/html"
    "github.com/gomarkdown/markdown/parser"
)

// 解析器
p := parser.NewWithExtensions(parser.CommonExtensions)

// 渲染器
htmlFlags := html.CommonFlags | html.HrefTargetBlank
opts := html.RendererOptions{
    Flags: htmlFlags,
    Title: "我的文档",
    CSS: "style.css",
}
renderer := html.NewRenderer(opts)

// 转换
html := markdown.ToHTML(md, p, renderer)
```

### 可用的 HTML 标志

| 标志 | 描述 |
|------|-------------|
| `html.CommonFlags` | 常用合理默认设置 |
| `html.HrefTargetBlank` | 在链接中添加 `target="_blank"` |
| `html.CompletePage` | 生成完整的 HTML 文档 |
| `html.UseXHTML` | 使用 XHTML 输出 |
| `html.FootnoteReturnLinks` | 在脚注中添加返回链接 |
| `html.FootnoteNoHRTag` | 脚注前不添加 `<hr>` 标签 |
| `html.Smartypants` | 智能标点 |
| `html.SmartypantsFractions` | 智能分数（1/2 → ½） |
| `html.SmartypantsDashes` | 智能破折号（-- → –） |
| `html.SmartypantsLatexDashes` | LaTeX 风格的破折号 |

### 渲染器选项

```go
opts := html.RendererOptions{
    Flags:          htmlFlags,
    Title:          "文档标题",
    CSS:            "path/to/style.css",
    Icon:           "favicon.ico",
    Head:           []byte("<meta name='author' content='...'>"),
    RenderNodeHook: customRenderHook,
}
```

## 完整示例

```go
package main

import (
    "os"
    "github.com/gomarkdown/markdown"
    "github.com/gomarkdown/markdown/html"
    "github.com/gomarkdown/markdown/parser"
)

func mdToHTML(md []byte) []byte {
    // 带扩展的解析器
    extensions := parser.CommonExtensions | 
                  parser.AutoHeadingIDs | 
                  parser.NoEmptyLineBeforeBlock
    p := parser.NewWithExtensions(extensions)
    doc := p.Parse(md)

    // 带选项的 HTML 渲染器
    htmlFlags := html.CommonFlags | html.HrefTargetBlank
    opts := html.RendererOptions{Flags: htmlFlags}
    renderer := html.NewRenderer(opts)

    return markdown.Render(doc, renderer)
}

func main() {
    md, _ := os.ReadFile("input.md")
    html := mdToHTML(md)
    os.WriteFile("output.html", html, 0644)
}
```

## 安全性：清理输出

**重要：** gomarkdown 不会清理 HTML 输出。对于不受信任的输入，请使用 Bluemonday：

```go
import (
    "github.com/microcosm-cc/bluemonday"
    "github.com/gomarkdown/markdown"
)

// 将 Markdown 转换为潜在不安全的 HTML
unsafeHTML := markdown.ToHTML(md, nil, nil)

// 使用 Bluemonday 清理
p := bluemonday.UGCPolicy()
safeHTML := p.SanitizeBytes(unsafeHTML)
```

### Bluemonday 策略

| 策略 | 描述 |
|--------|-------------|
| `UGCPolicy()` | 用户生成内容（最常见） |
| `StrictPolicy()` | 删除所有 HTML 标签 |
| `StripTagsPolicy()` | 删除标签，保留文本 |
| `NewPolicy()` | 构建自定义策略 |

## 使用 AST

### 访问 AST

```go
import (
    "github.com/gomarkdown/markdown/ast"
    "github.com/gomarkdown/markdown/parser"
)

p := parser.NewWithExtensions(parser.CommonExtensions)
doc := p.Parse(md)

// 遍历 AST
ast.WalkFunc(doc, func(node ast.Node, entering bool) ast.WalkStatus {
    if heading, ok := node.(*ast.Heading); ok && entering {
        fmt.Printf("找到标题级别 %d\n", heading.Level)
    }
    return ast.GoToNext
})
```

### 自定义渲染器

```go
type MyRenderer struct {
    *html.Renderer
}

func (r *MyRenderer) RenderNode(w io.Writer, node ast.Node, entering bool) ast.WalkStatus {
    // 自定义渲染逻辑
    if heading, ok := node.(*ast.Heading); ok && entering {
        fmt.Fprintf(w, "<h%d class='custom'>", heading.Level)
        return ast.GoToNext
    }
    return r.Renderer.RenderNode(w, node, entering)
}
```

## 处理换行符

Windows 和 Mac 换行符需要规范化：

```go
// 在解析前规范化换行符
normalized := parser.NormalizeNewlines(input)
html := markdown.ToHTML(normalized, nil, nil)
```

## 资源

- [包文档](https://pkg.go.dev/github.com/gomarkdown/markdown)
- [高级处理指南](https://blog.kowalczyk.info/article/cxn3/advanced-markdown-processing-in-go.html)
- [GitHub 仓库](https://github.com/gomarkdown/markdown)
- [CLI 工具](https://github.com/gomarkdown/mdtohtml)
- [Bluemonday 清理工具](https://github.com/microcosm-cc/bluemonday)

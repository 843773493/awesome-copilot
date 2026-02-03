# Pandoc 参考指南

Pandoc 是一个通用的文档转换工具，可以将多种标记格式相互转换，包括 Markdown、HTML、LaTeX、Word 等。

## 安装

### Windows

```powershell
# 使用 Chocolatey
choco install pandoc

# 使用 Scoop
scoop install pandoc

# 或者从 https://pandoc.org/installing.html 下载安装程序
```

### macOS

```bash
# 使用 Homebrew
brew install pandoc
```

### Linux

```bash
# Debian/Ubuntu
sudo apt-get install pandoc

# Fedora
sudo dnf install pandoc

# 或者从 https://pandoc.org/installing.html 下载
```

## 基本用法

### 将 Markdown 转换为 HTML

```bash
# 基础转换
pandoc input.md -o output.html

# 生成带有标题的独立文档
pandoc input.md -s -o output.html

# 使用自定义 CSS
pandoc input.md -s --css=style.css -o output.html
```

### 转换为其他格式

```bash
# 转换为 PDF（需要 LaTeX 支持）
pandoc input.md -s -o output.pdf

# 转换为 Word
pandoc input.md -s -o output.docx

# 转换为 LaTeX
pandoc input.md -s -o output.tex

# 转换为 EPUB
pandoc input.md -s -o output.epub
```

### 从其他格式转换

```bash
# 从 HTML 转换为 Markdown
pandoc -f html -t markdown input.html -o output.md

# 从 Word 转换为 Markdown
pandoc input.docx -o output.md

# 从 LaTeX 转换为 HTML
pandoc -f latex -t html input.tex -o output.html
```

## 常用选项

| 选项 | 描述 |
|------|------|
| `-f, --from <格式>` | 输入格式 |
| `-t, --to <格式>` | 输出格式 |
| `-s, --standalone` | 生成自包含文档 |
| `-o, --output <文件>` | 输出文件 |
| `--toc` | 包含目录 |
| `--toc-depth <n>` | 目录深度（默认：3） |
| `-N, --number-sections` | 为章节编号 |
| `--css <URL>` | 链接到 CSS 样式表 |
| `--template <文件>` | 使用自定义模板 |
| `--metadata <键>=<值>` | 设置元数据 |
| `--mathml` | 使用 MathML 渲染数学公式 |
| `--mathjax` | 使用 MathJax 渲染数学公式 |
| `-V, --variable <键>=<值>` | 设置模板变量 |

## Markdown 扩展

Pandoc 支持多种 Markdown 扩展：

```bash
# 启用特定扩展
pandoc -f markdown+emoji+footnotes input.md -o output.html

# 禁用特定扩展
pandoc -f markdown-pipe_tables input.md -o output.html

# 使用严格模式的 Markdown
pandoc -f markdown_strict input.md -o output.html
```

### 常用扩展

| 扩展 | 描述 |
|------|------|
| `pipe_tables` | 管道表格（默认启用） |
| `footnotes` | 脚注支持 |
| `emoji` | 表情符号缩写码 |
| `smart` | 智能引号和破折号 |
| `task_lists` | 任务列表复选框 |
| `strikeout` | 删除线文本 |
| `superscript` | 上标文本 |
| `subscript` | 下标文本 |
| `raw_html` | 原始 HTML 透传 |

## 模板

### 使用内置模板

```bash
# 查看默认模板
pandoc -D html

# 使用自定义模板
pandoc --template=mytemplate.html input.md -o output.html
```

### 模板变量

```html
<!DOCTYPE html>
<html>
<head>
  <title>$title$</title>
  $for(css)$
  <link rel="stylesheet" href="$css$">
  $endfor$
</head>
<body>
$body$
</body>
</html>
```

## YAML 元数据

在 Markdown 文件中包含元数据：

```markdown
---
title: 我的文档
author: John Doe
date: 2025-01-28
abstract: |
  这是摘要。
---

# 引言

文档内容在此...
```

## 过滤器

### 使用 Lua 过滤器

```bash
pandoc --lua-filter=filter.lua input.md -o output.html
```

示例 Lua 过滤器（`filter.lua`）:

```lua
function Header(el)
  if el.level == 1 then
    el.classes:insert("main-title")
  end
  return el
end
```

### 使用 Pandoc 过滤器

```bash
pandoc --filter pandoc-citeproc input.md -o output.html
```

## 批量转换

### Bash 脚本

```bash
#!/bin/bash
for file in *.md; do
  pandoc "$file" -s -o "${file%.md}.html"
done
```

### PowerShell 脚本

```powershell
Get-ChildItem -Filter *.md | ForEach-Object {
  $output = $_.BaseName + ".html"
  pandoc $_.Name -s -o $output
}
```

## 资源

- [Pandoc 用户指南](https://pandoc.org/MANUAL.html)
- [Pandoc 示例](https://pandoc.org/demos.html)
- [Pandoc 常见问题](https://pandoc.org/faqs.html)
- [GitHub 仓库](https://github.com/jgm/pandoc)

# Hugo 参考指南

Hugo 是世界上最快的静态网站生成器。它可以在毫秒内构建网站，并支持高级内容管理功能。

## 安装

### Windows

```powershell
# 使用 Chocolatey
choco install hugo-extended

# 使用 Scoop
scoop install hugo-extended

# 使用 Winget
winget install Hugo.Hugo.Extended
```

### macOS

```bash
# 使用 Homebrew
brew install hugo
```

### Linux

```bash
# Debian/Ubuntu (snap)
snap install hugo --channel=extended

# 使用包管理器（可能不是最新版本）
sudo apt-get install hugo

# 或者从 https://gohugo.io/installation/ 下载
```

## 快速入门

### 创建新站点

```bash
# 创建站点
hugo new site mysite
cd mysite

# 初始化 Git 并添加主题
git init
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke themes/ananke
echo "theme = 'ananke'" >> hugo.toml

# 创建第一个文章
hugo new content posts/my-first-post.md

# 启动开发服务器
hugo server -D
```

### 目录结构

```
mysite/
├── archetypes/      # 内容模板
│   └── default.md
├── assets/          # 需要处理的资源（SCSS、JS）
├── content/         # Markdown 内容
│   └── posts/
├── data/            # 数据文件（YAML、JSON、TOML）
├── i18n/            # 国际化
├── layouts/         # 模板
│   ├── _default/
│   ├── partials/
│   └── shortcodes/
├── static/          # 静态文件（原样复制）
├── themes/          # 主题
└── hugo.toml        # 配置
```

## 命令行接口命令

| 命令 | 描述 |
|------|------|
| `hugo new site <name>` | 创建新站点 |
| `hugo new content <path>` | 创建内容文件 |
| `hugo` | 构建到 `public/` 目录 |
| `hugo server` | 启动开发服务器 |
| `hugo mod init` | 初始化 Hugo 模块 |
| `hugo mod tidy` | 清理模块 |

### 构建选项

```bash
# 基础构建
hugo

# 启用压缩构建
hugo --minify

# 启用草稿构建
hugo -D

# 为特定环境构建
hugo --environment production

# 构建到自定义目录
hugo -d ./dist

# 显示详细输出
hugo -v
```

### 服务器选项

```bash
# 启用草稿
hugo server -D

# 绑定到所有接口
hugo server --bind 0.0.0.0

# 使用自定义端口
hugo server --port 8080

# 禁用实时重载
hugo server --disableLiveReload

# 导航到更改的内容
hugo server --navigateToChanged
```

## 配置 (hugo.toml)

```toml
# 基础设置
baseURL = 'https://example.com/'
languageCode = 'en-us'
title = 'My Hugo Site'
theme = 'ananke'

# 构建设置
[build]
  writeStats = true

# Markdown 配置
[markup]
  [markup.goldmark]
    [markup.goldmark.extensions]
      definitionList = true
      footnote = true
      linkify = true
      strikethrough = true
      table = true
      taskList = true
    [markup.goldmark.parser]
      autoHeadingID = true
      autoHeadingIDType = 'github'
    [markup.goldmark.renderer]
      unsafe = false
  [markup.highlight]
    style = 'monokai'
    lineNos = true

# 分类和标签
[taxonomies]
  category = 'categories'
  tag = 'tags'
  author = 'authors'

# 菜单
[menus]
  [[menus.main]]
    name = 'Home'
    pageRef = '/'
    weight = 10
  [[menus.main]]
    name = 'Posts'
    pageRef = '/posts'
    weight = 20

# 参数
[params]
  description = 'My awesome site'
  author = 'John Doe'
```

## 前置内容（Front Matter）

Hugo 支持 TOML、YAML 和 JSON 前置内容：

### TOML（默认）

```markdown
+++
title = 'My First Post'
date = 2025-01-28T12:00:00-05:00
draft = false
tags = ['hugo', 'tutorial']
categories = ['blog']
author = 'John Doe'
+++

内容在此...
```

### YAML

```markdown
---
title: "My First Post"
date: 2025-01-28T12:00:00-05:00
draft: false
tags: ["hugo", "tutorial"]
---

内容在此...
```

## 模板

### 基础模板 (_default/baseof.html)

```html
<!DOCTYPE html>
<html>
<head>
  <title>{{ .Title }} | {{ .Site.Title }}</title>
  {{ partial "head.html" . }}
</head>
<body>
  {{ partial "header.html" . }}
  <main>
    {{ block "main" . }}{{ end }}
  </main>
  {{ partial "footer.html" . }}
</body>
</html>
```

### 单页模板 (_default/single.html)

```html
{{ define "main" }}
<article>
  <h1>{{ .Title }}</h1>
  <time>{{ .Date.Format "January 2, 2006" }}</time>
  {{ .Content }}
</article>
{{ end }}
```

### 列表页模板 (_default/list.html)

```html
{{ define "main" }}
<h1>{{ .Title }}</h1>
{{ range .Pages }}
  <article>
    <h2><a href="{{ .Permalink }}">{{ .Title }}</a></h2>
    <p>{{ .Summary }}</p>
  </article>
{{ end }}
{{ end }}
```

## 短代码（Shortcodes）

### 内置短代码

```markdown
{{< figure src="/images/photo.jpg" title="My Photo" >}}

{{< youtube dQw4w9WgXcQ >}}

{{< gist user 12345 >}}

{{< highlight go >}}
fmt.Println("Hello")
{{< /highlight >}}
```

### 自定义短代码 (layouts/shortcodes/alert.html)

```html
<div class="alert alert-{{ .Get "type" | default "info" }}">
  {{ .Inner | markdownify }}
</div>
```

使用示例：

```markdown
{{< alert type="warning" >}}
**警告:** 这是重要信息！
{{< /alert >}}
```

## 内容组织

### 页面捆绑

```
content/
├── posts/
│   └── my-post/           # 页面捆绑
│       ├── index.md       # 内容
│       └── image.jpg      # 资源
└── _index.md              # 部分页面
```

### 访问资源

```html
{{ $image := .Resources.GetMatch "image.jpg" }}
{{ with $image }}
  <img src="{{ .RelPermalink }}" alt="...">
{{ end }}
```

## Hugo 管道（Asset Processing）

### SCSS 编译

```html
{{ $styles := resources.Get "scss/main.scss" | toCSS | minify }}
<link rel="stylesheet" href="{{ $styles.RelPermalink }}">
```

### JavaScript 打包

```html
{{ $js := resources.Get "js/main.js" | js.Build | minify }}
<script src="{{ $js.RelPermalink }}"></script>
```

## 分类和标签（Taxonomies）

### 配置

```toml
[taxonomies]
  tag = 'tags'
  category = 'categories'
```

### 在前置内容中使用

```markdown
+++
tags = ['go', 'hugo']
categories = ['tutorials']
+++
```

### 列出分类术语

```html
{{ range .Site.Taxonomies.tags }}
  <a href="{{ .Page.Permalink }}">{{ .Page.Title }} ({{ .Count }})</a>
{{ end }}
```

## 多语言站点

```toml
defaultContentLanguage = 'en'

[languages]
  [languages.en]
    title = 'My Site'
    weight = 1
  [languages.es]
    title = 'Mi Sitio'
    weight = 2
```

## 常见问题排查

| 问题 | 解决方案 |
|------|----------|
| 页面未找到 | 检查 `baseURL` 配置 |
| 主题未加载 | 验证配置中的主题路径 |
| 原始 HTML 未显示 | 在 goldmark 配置中设置 `unsafe = true` |
| 构建缓慢 | 使用 `--templateMetrics` 调试 |
| 模块错误 | 运行 `hugo mod tidy` |
| CSS 未更新 | 清除浏览器缓存或使用指纹技术 |

## 资源

- [Hugo 文档](https://gohugo.io/documentation/)
- [Hugo 主题](https://themes.gohugo.io/)
- [Hugo 讨论区](https://discourse.gohugo.io/)
- [GitHub 仓库](https://github.com/gohugoio/hugo)
- [快速参考](https://gohugo.io/quick-reference/)

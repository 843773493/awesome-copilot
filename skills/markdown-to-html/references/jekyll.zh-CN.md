# Jekyll 参考指南

Jekyll 是一个静态网站生成器，它将 Markdown 内容转换为完整的网站。它支持博客功能并为 GitHub Pages 提供支持。

## 安装

### 先决条件

- Ruby 2.7.0 或更高版本
- RubyGems
- GCC 和 Make

### 安装 Jekyll

```bash
# 安装 Jekyll 和 Bundler
gem install jekyll bundler
```

### 平台特定安装

```bash
# macOS（首先安装 Xcode 命令行工具）
xcode-select --install
gem install jekyll bundler

# Ubuntu/Debian
sudo apt-get install ruby-full build-essential zlib1g-dev
gem install jekyll bundler

# Windows（使用 RubyInstaller）
# 下载地址：https://rubyinstaller.org/
gem install jekyll bundler
```

## 快速入门

### 创建新站点

```bash
# 创建新的 Jekyll 站点
jekyll new myblog

# 进入站点目录
cd myblog

# 构建并运行本地服务器
bundle exec jekyll serve

# 打开 http://localhost:4000
```

### 目录结构

```
myblog/
├── _config.yml      # 站点配置
├── _posts/          # 博客文章
│   └── 2025-01-28-welcome.md
├── _layouts/        # 页面模板
├── _includes/       # 可重用组件
├── _data/           # 数据文件（YAML、JSON、CSV）
├── _sass/           # Sass 部分
├── assets/          # CSS、JS、图片
├── index.md         # 首页
└── Gemfile          # Ruby 依赖文件
```

## 命令行命令

| 命令 | 描述 |
|------|------|
| `jekyll new <name>` | 创建新站点 |
| `jekyll build` | 构建到 `_site/` 目录 |
| `jekyll serve` | 本地构建并运行服务器 |
| `jekyll clean` | 删除生成的文件 |
| `jekyll doctor` | 检查问题 |

### 构建选项

```bash
# 构建站点
bundle exec jekyll build

# 在生产环境构建
JEKYLL_ENV=production bundle exec jekyll build

# 构建到自定义目录
bundle exec jekyll build --destination ./public

# 使用增量再生构建
bundle exec jekyll build --incremental
```

### 服务选项

```bash
# 使用实时重新加载
bundle exec jekyll serve --livereload

# 包含草稿文章
bundle exec jekyll serve --drafts

# 指定端口
bundle exec jekyll serve --port 8080

# 绑定到所有接口
bundle exec jekyll serve --host 0.0.0.0
```

## 配置 (_config.yml)

```yaml
# 站点设置
title: My Blog
description: 一个很棒的博客
baseurl: ""
url: "https://example.com"

# 构建设置
markdown: kramdown
theme: minima
plugins:
  - jekyll-feed
  - jekyll-seo-tag

# Kramdown 设置
kramdown:
  input: GFM                    # GitHub Flavored Markdown
  syntax_highlighter: rouge
  syntax_highlighter_opts:
    block:
      line_numbers: true

# 收集（Collections）
collections:
  docs:
    output: true
    permalink: /docs/:name/

# 默认设置
defaults:
  - scope:
      path: ""
      type: "posts"
    values:
      layout: "post"

# 排除处理
exclude:
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor
```

## 前置内容（Front Matter）

每个内容文件都需要 YAML 前置内容：

```markdown
---
layout: post
title: "我的第一篇文章"
date: 2025-01-28 12:00:00 -0500
categories: 博客 教程
tags: [jekyll, markdown]
author: John Doe
excerpt: "简要介绍..."
published: true
---

你的内容在这里...
```

## Markdown 处理器

### Kramdown（默认）

```yaml
# _config.yml
markdown: kramdown
kramdown:
  input: GFM                    # GitHub Flavored Markdown
  syntax_highlighter: rouge
  syntax_highlighter_opts:
    block:
      line_numbers: true
```

### CommonMark

```ruby
# Gemfile
gem 'jekyll-commonmark-ghpages'
```

```yaml
# _config.yml
markdown: CommonMarkGhPages
commonmark:
  options: ["SMART", "FOOTNOTES"]
  extensions: ["strikethrough", "autolink", "table"]
```

## Liquid 模板引擎

### 变量

```liquid
{{ page.title }}
{{ site.title }}
{{ content }}
{{ page.date | date: "%B %d, %Y" }}
```

### 循环

```liquid
{% for post in site.posts %}
  <article>
    <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
    <p>{{ post.excerpt }}</p>
  </article>
{% endfor %}
```

### 条件语句

```liquid
{% if page.title %}
  <h1>{{ page.title }}</h1>
{% endif %}

{% unless page.draft %}
  {{ content }}
{% endunless %}
```

### 包含

```liquid
{% include header.html %}
{% include footer.html param="value" %}
```

## 布局

### 基础布局 (_layouts/default.html)

```html
<!DOCTYPE html>
<html>
<head>
  <title>{{ page.title }} | {{ site.title }}</title>
  <link rel="stylesheet" href="{{ '/assets/css/style.css' | relative_url }}">
</head>
<body>
  {% include header.html %}
  <main>
    {{ content }}
  </main>
  {% include footer.html %}
</body>
</html>
```

### 文章布局 (_layouts/post.html)

```html
---
layout: default
---
<article>
  <h1>{{ page.title }}</h1>
  <time>{{ page.date | date: "%B %d, %Y" }}</time>
  {{ content }}
</article>
```

## 插件

### 常用插件

```ruby
# Gemfile
group :jekyll_plugins do
  gem 'jekyll-feed'        # RSS 首页
  gem 'jekyll-seo-tag'     # SEO 元标签
  gem 'jekyll-sitemap'     # XML 站点地图
  gem 'jekyll-paginate'    # 分页功能
  gem 'jekyll-archives'    # 归档页面
end
```

### 使用插件

```yaml
# _config.yml
plugins:
  - jekyll-feed
  - jekyll-seo-tag
  - jekyll-sitemap
```

## 常见问题排查

| 问题 | 解决方案 |
|------|----------|
| Ruby 3.0+ Webrick 错误 | `bundle add webrick` |
| 权限被拒绝 | 使用 `--user-install` 或 rbenv |
| 构建缓慢 | 使用 `--incremental` |
| Liquid 错误 | 检查未转义的 `{` `}` |
| 编码问题 | 在配置中添加 `encoding: utf-8` |
| 插件未加载 | 在 Gemfile 和 _config.yml 中都添加 |

## 资源

- [Jekyll 文档](https://jekyllrb.com/docs/)
- [Liquid 模板语言](https://shopify.github.io/liquid/)
- [Kramdown 文档](https://kramdown.gettalong.org/)
- [GitHub 仓库](https://github.com/jekyll/jekyll)
- [Jekyll 主题](https://jekyllthemes.io/)

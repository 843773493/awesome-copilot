# Marked

## 快速转换方法

`SKILL.md` 中的 `### Quick Conversion Methods` 部分扩展内容。

### 方法 1：CLI（推荐用于单个文件）

```bash
# 将文件转换为 HTML
marked -i input.md -o output.html

# 直接转换字符串
marked -s "# Hello World"

# 输出： <h1>Hello World</h1>
```

### 方法 2：Node.js 脚本

```javascript
import { marked } from 'marked';
import { readFileSync, writeFileSync } from 'fs';

const markdown = readFileSync('input.md', 'utf-8');
const html = marked.parse(markdown);
writeFileSync('output.html', html);
```

### 方法 3：浏览器使用

```html
<script src="https://cdn.jsdelivr.net/npm/marked/lib/marked.umd.js"></script>
<script>
  const html = marked.parse('# Markdown 内容');
  document.getElementById('output').innerHTML = html;
</script>
```

---

## 分步工作流

`SKILL.md` 中的 `### Step-by-Step Workflows` 部分扩展内容。

### 工作流 1：单个文件转换

1. 确保已安装 marked：`npm install -g marked`
2. 运行转换：`marked -i README.md -o README.html`
3. 验证输出文件是否已生成

### 工作流 2：批量转换（多个文件）

创建一个名为 `convert-all.js` 的脚本：

```javascript
import { marked } from 'marked';
import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join, basename } from 'path';

const inputDir = './docs';
const outputDir = './html';

readdirSync(inputDir)
  .filter(file => file.endsWith('.md'))
  .forEach(file => {
    const markdown = readFileSync(join(inputDir, file), 'utf-8');
    const html = marked.parse(markdown);
    const outputFile = basename(file, '.md') + '.html';
    writeFileSync(join(outputDir, outputFile), html);
    console.log(`转换完成：${file} → ${outputFile}`);
  });
```

运行方式：`node convert-all.js`

### 工作流 3：使用自定义选项进行转换

```javascript
import { marked } from 'marked';

// 配置选项
marked.setOptions({
  gfm: true,           // GitHub 风格的 Markdown
  breaks: true,        // 将 \n 转换为 <br>
  pedantic: false,     // 不遵循原始 markdown.pl 规范
});

const html = marked.parse(markdownContent);
```

### 工作流 4：完整的 HTML 文档

将转换后的内容包装在完整的 HTML 模板中：

```javascript
import { marked } from 'marked';
import { readFileSync, writeFileSync } from 'fs';

const markdown = readFileSync('input.md', 'utf-8');
const content = marked.parse(markdown);

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>文档</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; }
    pre { background: #f4f4f4; padding: 1rem; overflow-x: auto; }
    code { background: #f4f4f4; padding: 0.2rem 0.4rem; border-radius: 3px; }
  </style>
</head>
<body>
${content}
</body>
</html>`;

writeFileSync('output.html', html);
```

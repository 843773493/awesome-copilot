# 表格转HTML

## 创建表格

### Markdown

```markdown
| 第一列标题  | 第二列标题 |
| ------------- | ------------- |
| 内容单元格  | 内容单元格  |
| 内容单元格  | 内容单元格  |
```

### 解析后的HTML

```html
<table>
 <thead>
  <tr>
   <th>第一列标题</th>
   <th>第二列标题</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>内容单元格</td>
   <td>内容单元格</td>
  </tr>
  <tr>
   <td>内容单元格</td>
   <td>内容单元格</td>
  </tr>
 </tbody>
</table>
```

### Markdown

```markdown
| 命令 | 描述 |
| --- | --- |
| git status | 列出所有新文件或修改的文件 |
| git diff | 显示尚未提交的文件差异 |
```

### 解析后的HTML

```html
<table>
 <thead>
  <tr>
   <th>命令</th>
   <th>描述</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td><code>git status</code></td>
   <td>列出所有<em>新或修改的</em>文件</td>
  </tr>
  <tr>
   <td><code>git diff</code></td>
   <td>显示尚未提交的文件差异</td>
  </tr>
 </tbody>
</table>
```

## 表格内容格式化

### Markdown

```markdown
| 命令 | 描述 |
| --- | --- |
| `git status` | 列出所有 *新或修改的* 文件 |
| `git diff` | 显示尚未提交的文件差异 |
```

### 解析后的HTML

```html
<table>
 <thead>
  <tr>
   <th>命令</th>
   <th>描述</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td><code>git status</code></td>
   <td>列出所有 <em>新或修改的</em> 文件</td>
  </tr>
  <tr>
   <td><code>git diff</code></td>
   <td>显示尚未提交的文件差异</td>
  </tr>
 </tbody>
</table>
```

### Markdown

```markdown
| 左对齐 | 居中对齐 | 右对齐 |
| :---         |     :---:      |          ---: |
| git status   | git status     | git status    |
| git diff     | git diff       | git diff      |
```

### 解析后的HTML

```html
<table>
  <thead>
   <tr>
    <th align="left">左对齐</th>
    <th align="center">居中对齐</th>
    <th align="right">右对齐</th>
   </tr>
  </thead>
  <tbody>
   <tr>
    <td align="left">git status</td>
    <td align="center">git status</td>
    <td align="right">git status</td>
   </tr>
   <tr>
    <td align="left">git diff</td>
    <td align="center">git diff</td>
    <td align="right">git diff</td>
   </tr>
  </tbody>
</table>
```

### Markdown

```markdown
| 名称     | 字符 |
| ---      | ---       |
| 反引号 | `         |
| 竖线     | \|        |
```

### 解析后的HTML

```html
<table>
 <thead>
  <tr>
   <th>名称</th>
   <th>字符</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>反引号</td>
   <td>`</td>
  </tr>
  <tr>
   <td>竖线</td>
   <td>|</td>
  </tr>
 </tbody>
</table>
```

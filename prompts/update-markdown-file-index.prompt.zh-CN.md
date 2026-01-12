

---
agent: 'agent'
description: '使用指定文件夹 `${input:folder}` 中的文件索引/表格更新Markdown文件 `${file}`。'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'extensions', 'fetch', 'findTestFiles', 'githubRepo', 'openSimpleBrowser', 'problems', 'runCommands', 'runTasks', 'runTests', 'search', 'search/searchResults', 'runCommands/terminalLastCommand', 'runCommands/terminalSelection', 'testFailure', 'usages', 'vscodeAPI']
---
# 更新Markdown文件索引

使用指定文件夹 `${input:folder}` 中的文件索引/表格更新Markdown文件 `${file}`。

## 流程

1. **扫描**：读取目标Markdown文件 `${file}` 以了解现有结构
2. **发现**：列出指定文件夹 `${input:folder}` 中匹配模式 `${input:pattern}` 的所有文件
3. **分析**：确定是否存在需要更新的现有表格/索引部分，或创建新结构
4. **结构**：根据文件类型和现有内容生成适当的表格/列表格式
5. **更新**：替换现有部分或添加新的文件索引部分
6. **验证**：确保Markdown语法有效且格式一致

## 文件分析

对每个发现的文件，提取以下信息：

- **文件名**：根据上下文包含或不包含扩展名的文件名
- **类型**：文件扩展名和类别（例如 `.md`, `.js`, `.py`）
- **描述**：第一行注释、标题或推断出的目的
- **大小**：文件大小作为参考（可选）
- **修改时间**：最后修改日期（可选）

## 表格结构选项

根据文件类型和现有内容选择格式：

### 选项1：简单列表

```markdown
## ${folder} 中的文件

- [filename.ext](path/to/filename.ext) - 描述
- [filename2.ext](path/to/filename2.ext) - 描述
```

### 选项2：详细表格

| 文件 | 类型 | 描述 |
|------|------|-------------|
| [filename.ext](path/to/filename.ext) | 扩展名 | 描述 |
| [filename2.ext](path/to/filename2.ext) | 扩展名 | 描述 |

### 选项3：分组部分

按类型/类别分组，使用单独的部分或子表格。

## 更新策略

- 🔄 **更新现有**：如果存在表格/索引部分，则替换内容同时保留结构
- ➕ **添加新部分**：如果没有现有部分，则使用最适合的格式创建新部分
- 📋 **保留**：保持现有的Markdown格式、标题级别和文档流程
- 🔗 **链接**：在仓库内使用相对路径进行文件链接

## 部分识别

查找现有部分的这些模式：

- 标题包含： "索引"、"文件"、"内容"、"目录"、"列表"
- 包含文件相关列的表格
- 包含文件链接的列表
- 标记文件索引部分的HTML注释

## 要求

- 保留现有的Markdown结构和格式
- 使用相对路径进行文件链接
- 在有描述时包含文件描述
- 默认按字母顺序排序文件
- 处理文件名中的特殊字符
- 验证所有生成的Markdown语法
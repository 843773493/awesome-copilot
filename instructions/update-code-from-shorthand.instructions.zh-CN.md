

---
描述: "简写代码将位于提示中提供的文件或原始数据中，并在提示中包含文本 `UPDATE CODE FROM SHORTHAND` 时用于更新代码文件。"
应用到: "**/${input:file}"
---

# 从简写指令更新代码

提示中将提供一个或多个文件。对于每个文件，请查找以下标记：
`${openMarker}` 和 `${closeMarker}`。

编辑标记之间的所有内容可能包含自然语言和简写代码；请将其转换为适用于目标文件类型及其扩展名的有效代码。

## 角色

10倍软件工程师。擅长根据简写指令解决问题并生成创新解决方案，类似于头脑风暴。简写代码类似于客户给建筑师的手绘草图，您需要从中提取整体构想并运用专家判断力，生成完整且高质量的实现方案。

## 从简写指令更新代码文件的规则

- 提示的最开始处必须包含 `${openPrompt}` 文本。
- 接着 `${openPrompt}` 的是 `${REQUIRED_FILE}`。
- 在代码文件或提示中查找编辑标记 - 例如：

```text
 ${openMarker} 
 ()=> 简写代码 
 ${closeMarker}
```

- 使用简写代码来编辑，有时甚至需要根据简写代码创建代码文件的内容。
- 如果任何注释中包含 `REMOVE COMMENT`、`NOTE` 或类似文本，则**该注释**需要被删除；并且该行很可能需要正确的语法、函数、方法或代码块。
- 如果文本后跟随的文件名暗示 "无需编辑代码"，则很可能这是要更新数据文件（如 `JSON` 或 `XML`），意味着编辑应专注于格式化数据。
- 如果文本后跟随的文件名暗示 "无需编辑代码" 且 "添加数据"，则很可能这是要更新数据文件（如 `JSON` 或 `XML`），意味着编辑应专注于格式化和添加符合数据文件现有格式的额外数据。

### 应用指令和规则的时机

- 仅当提示的最开始处包含 `${openPrompt}` 文本时才相关。
  - 如果 `${openPrompt}` 不在提示的最开始处，则忽略该提示的这些指令。
- `${REQUIRED_FILE}` 将包含两个标记：
  1. 开始标记 `${openMarker}`
  2. 结束标记 `${closeMarker}`
  - 称之为“编辑标记”。
- 编辑标记之间的内容决定了需要更新 `${REQUIRED_FILE}` 或其他引用文件的内容。
- 应用更新后，从受影响的文件中删除 `${openMarker}` 和 `${closeMarker}` 行。

#### 遵循规则的提示反馈

```bash
[user]
> 编辑代码文件 ${REQUIRED_FILE}.
[agent]
> 您是指在提示前添加 "${openPrompt}" 吗？
[user]
> ${openMarker} - 编辑代码文件 ${REQUIRED_FILE}.
```

## 请务必

- 删除所有 `${openMarker}` 或 `${language:comment} start-shorthand` 的出现。
  - 例如：`// start-shorthand`。
- 删除所有 `${closeMarker}` 或 `${language:comment} end-shorthand` 的出现。
  - 例如：`// end-shorthand`。

## 简写指令键

- **`()=>`** = 90% 的注释和 10% 的混合语言伪代码块。
  - 当行以 `()=>` 开头时，请使用您的 **角色** 来确定实现目标的解决方案。

## 变量

- REQUIRED_FILE = `${input:file}`;
- openPrompt = "UPDATE CODE FROM SHORTHAND";
- language:comment = "编程语言的单行或多行注释。"
- openMarker = "${language:comment} start-shorthand";
- closeMarker = "${language:comment} end-shorthand";

## 使用示例

### 提示输入

```bash
[user prompt]
UPDATE CODE FROM SHORTHAND 
#file:script.js 
使用 #file:index.html:94-99 查看转换后的 markdown 到 html 将被解析的位置 `id="a"`。
```

### 代码文件

```js
// script.js
// 解析 markdown 文件，应用 html 渲染输出。

var file = "file.md";
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
 if (this.readyState == 4 && this.status == 200) {
  let data = this.responseText;
  let a = document.getElementById("a");
  let output = "";
  // start-shorthand
  ()=> let apply_html_to_parsed_markdown = (md) => {
   ()=> md.forEach(line => {
    // 根据行数据使用正则表达式插入 html 元素，将 markdown 转换为 html
    ()=> output += line.replace(/^(regex to add html elements from markdonw line)(.*)$/g, $1$1);
   });
   // 输出从 markdown 转换为 html 的文件。
   return output;
  };
  ()=>a.innerHTML = apply_html_to_parsed_markdown(data);
  // end-shorthand
 }
};
xhttp.open("GET", file, true);
xhttp.send();
```
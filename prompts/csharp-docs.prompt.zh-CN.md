

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems']
description: '确保C#类型使用XML注释进行文档说明，并遵循文档说明的最佳实践。'
---

# C# 文档最佳实践

- 公共成员应使用XML注释进行文档说明。
- 鼓励对内部成员进行文档说明，尤其是当它们较为复杂或不够直观时。

## 所有API的指导原则

- 使用 `<summary>` 提供一个简短的、一句话的描述，说明该类型或成员的作用。以现在时的第三人称动词开头。
- 使用 `<remarks>` 提供额外信息，可以包括实现细节、使用说明或其他相关上下文。
- 使用 `<see langword>` 说明特定于语言的关键字，如 `null`、`true`、`false`、`int`、`bool` 等。
- 使用 `<c>` 插入内联代码片段。
- 使用 `<example>` 提供成员的使用示例。
  - 使用 `<code>` 标记代码块。`<code>` 标签应放置在 `<example>` 标签内。通过 `language` 属性添加代码示例的语言，例如 `<code language="csharp">`。
- 使用 `<see cref>` 用于在句子中引用其他类型或成员。
- 使用 `<seealso>` 用于在线文档“另请参阅”部分的独立引用（不在句子中）。
- 使用 `<inheritdoc/>` 从基类或接口继承文档。
  - 除非有重大的行为变更，否则应文档说明差异。

## 方法

- 使用 `<param>` 描述方法参数。
  - 描述应为一个名词短语，不指定数据类型。
  - 以一个引导性冠词开头。
  - 如果参数是标志位枚举，则描述应以 "A bitwise combination of the enumeration values that specifies..." 开头。
  - 如果参数是非标志位枚举，则描述应以 "One of the enumeration values that specifies..." 开头。
  - 如果参数是布尔值，则描述应为 "`<see langword="true" />` 用于...；否则，`<see langword="false" />`。"。
  - 如果参数是 "out" 参数，则描述应为 "当此方法返回时，包含...。此参数被视为未初始化。"。
- 使用 `<paramref>` 在文档中引用参数名称。
- 使用 `<typeparam>` 描述泛型类型或方法的类型参数。
- 使用 `<typeparamref>` 在文档中引用类型参数。
- 使用 `<returns>` 描述方法返回的内容。
  - 描述应为一个名词短语，不指定数据类型。
  - 以一个引导性冠词开头。
  - 如果返回类型是布尔值，则描述应为 "`<see langword="true" />` 如果...；否则，`<see langword="false" />`。"。

## 构造函数

- 总结的表述应为 "Initializes a new instance of the <Class> class [or struct]。"（初始化 <Class> 类 [或结构] 的新实例。）

## 属性

- `<summary>` 应以以下方式开头：
  - "Gets or sets..."（获取或设置...）用于可读写的属性。
  - "Gets..."（获取...）用于只读属性。
  - "Gets [or sets] a value that indicates whether..."（获取[或设置]一个指示...的值）用于返回布尔值的属性。
- 使用 `<value>` 描述属性的值。
  - 描述应为一个名词短语，不指定数据类型。
  - 如果属性有默认值，用单独的句子说明，例如 "The default is `<see langword="false" />`"（默认值为 `<see langword="false" />`）。
  - 如果值类型是布尔值，则表述应为 "`<see langword="true" />` 如果...；否则，`<see langword="false" />`。默认值为...。"。

## 异常

- 使用 `<exception cref>` 文档说明由构造函数、属性、索引器、方法、运算符和事件抛出的异常。
- 文档说明所有由成员直接抛出的异常。
- 对于由嵌套成员抛出的异常，仅文档说明用户最可能遇到的异常。
- 异常的描述说明其抛出的条件。
  - 避免在句子开头使用 "Thrown if ..." 或 "If ..."。直接陈述条件，例如 "在访问消息队列API时发生错误。"
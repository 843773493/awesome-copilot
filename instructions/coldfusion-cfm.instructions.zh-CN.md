

---
description: 'ColdFusion cfm 文件和应用程序模式'
applyTo: "**/*.cfm"
---

# ColdFusion 编码规范

- 尽可能使用 CFScript 以获得更清晰的语法。
- 避免使用已弃用的标签和函数。
- 遵循一致的变量和组件命名规范。
- 使用 `cfqueryparam` 来防止 SQL 注入。
- 在 <cfoutput> 块内使用 ## 转义 CSS 哈希符号。
- 当在 <cfoutput> 块内使用 HTMX 时，使用双井号 (##) 转义井号 (#)，以防止意外的变量插值。
- 如果您正在 HTMX 目标文件中，请确保第一行是：<cfsetting showDebugOutput = "false">

# 其他最佳实践

- 使用 Application.cfc 来处理应用程序设置和请求。
- 将代码组织成可重用的 CFC（组件），以提高可维护性。
- 验证和清理所有用户输入。
- 使用 cftry/cfcatch 进行错误处理和日志记录。
- 避免在源文件中硬编码凭证或敏感数据。
- 使用一致的缩进（2 个空格，符合全球标准）。
- 对复杂逻辑进行注释，并用用途和参数文档化函数。
- 优先使用 cfinclude 包含共享模板，但避免循环包含。

- 尽可能使用三元运算符
- 确保制表符对齐一致。
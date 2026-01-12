

---
description: 'TypeScript 模式用于 Azure Functions'
applyTo: '**/*.ts, **/*.js, **/*.json'
---

## 代码生成指南
- 为 Node.js 生成现代 TypeScript 代码
- 使用 `async/await` 进行异步代码编写
- 在可能的情况下，使用 Node.js v20 内置模块而非外部包
- 始终使用 Node.js 的异步函数，例如 `node:fs/promises` 而不是 `fs`，以避免阻塞事件循环
- 在向项目添加任何额外依赖项之前，请先询问
- 该 API 使用 Azure Functions 和 `@azure/functions@4` 包构建。
- 每个端点应有自己的函数文件，并使用以下命名规范：`src/functions/<resource-name>-<http-verb>.ts`
- 在对 API 进行更改时，请确保相应地更新 OpenAPI 模式（如果存在）和 `README.md` 文件。
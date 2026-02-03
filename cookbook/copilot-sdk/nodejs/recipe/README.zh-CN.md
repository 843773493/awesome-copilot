# 可运行的食谱示例

此文件夹包含每个烹饪书食谱的独立、可执行的 TypeScript 示例。每个文件都可以直接通过 `tsx` 或 npm 脚本运行。

## 前提条件

- Node.js 18 或更高版本
- 安装依赖项（此链接指向仓库中的本地 SDK）：

```bash
npm install
```

## 运行示例

每个 `.ts` 文件都是一个完整的、可运行的程序。您可以通过以下两种方式运行它们：

### 使用 npm 脚本：

```bash
npm run <script-name>
```

### 直接使用 tsx：

```bash
npx tsx <filename>.ts
```

### 可用的食谱

| 食谱               | npm 脚本                     | 直接命令                    | 描述                                |
| -------------------- | ------------------------------ | --------------------------------- | ------------------------------------------ |
| 错误处理       | `npm run error-handling`       | `npx tsx error-handling.ts`       | 演示错误处理模式       |
| 多个会话    | `npm run multiple-sessions`    | `npx tsx multiple-sessions.ts`    | 管理多个独立的对话 |
| 管理本地文件 | `npm run managing-local-files` | `npx tsx managing-local-files.ts` | 使用 AI 分组来组织文件          |
| PR 可视化     | `npm run pr-visualization`     | `npx tsx pr-visualization.ts`     | 生成 PR 年龄图表                    |
| 会话持久化  | `npm run persisting-sessions`  | `npx tsx persisting-sessions.ts`  | 在重启之间保存和恢复会话   |

### 带参数的示例

**使用特定仓库的 PR 可视化：**

```bash
npx tsx pr-visualization.ts --repo github/copilot-sdk
```

**管理本地文件（修改文件以更改目标文件夹）：**

```bash
# 首先编辑 managing-local-files.ts 中的 targetFolder 变量
npx tsx managing-local-files.ts
```

## 本地 SDK 开发

`package.json` 使用 `"*"` 引用本地 Copilot SDK，该引用解析为本地 SDK 源代码。这意味着：

- 对 SDK 源代码的更改会立即生效
- 无需发布或从 npm 安装
- 非常适合测试和开发

如果您修改了 SDK 源代码，可能需要重新构建：

```bash
cd ../../src
npm run build
```

## TypeScript 特性

这些示例使用了现代的 TypeScript/Node.js 特性：

- 顶层 await（需要 package.json 中的 `"type": "module"`）
- ESM 导入
- 通过 TypeScript 实现类型安全
- async/await 模式

## 学习资源

- [TypeScript 文档](https://www.typescriptlang.org/docs/)
- [Node.js 文档](https://nodejs.org/docs/latest/api/)
- [GitHub Copilot SDK for Node.js](https://github.com/github/copilot-sdk/blob/main/nodejs/README.md)
- [父级烹饪书](../README.md)

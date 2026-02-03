# 按元数据分组文件

使用 Copilot 根据文件的元数据智能地对文件夹中的文件进行分类整理。

> **可运行示例：** [recipe/managing-local-files.ts](recipe/managing-local-files.ts)
>
> ```bash
> cd recipe && npm install
> npx tsx managing-local-files.ts
> # 或：npm run managing-local-files
> ```

## 示例场景

您有一个包含大量文件的文件夹，希望根据元数据（如文件类型、创建日期、文件大小或其他属性）将它们组织到子文件夹中。Copilot 可以分析这些文件并建议或执行分组策略。

## 示例代码

```typescript
import { CopilotClient } from "@github/copilot-sdk";
import * as os from "node:os";
import * as path from "node:path";

// 创建并启动客户端
const client = new CopilotClient();
await client.start();

// 创建会话
const session = await client.createSession({
    model: "gpt-5",
});

// 事件处理程序
session.on((event) => {
    switch (event.type) {
        case "assistant.message":
            console.log(`\nCopilot: ${event.data.content}`);
            break;
        case "tool.execution_start":
            console.log(`  → 正在运行: ${event.data.toolName} ${event.data.toolCallId}`);
            break;
        case "tool.execution_complete":
            console.log(`  ✓ 完成: ${event.data.toolCallId}`);
            break;
    }
});

// 请求 Copilot 对文件进行整理
const targetFolder = path.join(os.homedir(), "Downloads");

await session.sendAndWait({
    prompt: `
分析 "${targetFolder}" 中的文件并将其组织到子文件夹中。

1. 首先列出所有文件及其元数据
2. 预览按文件扩展名分组的结果
3. 创建适当的子文件夹（例如："images"、"documents"、"videos"）
4. 将每个文件移动到对应的子文件夹中

在移动任何文件前请确认。
`,
});

await session.destroy();
await client.stop();
```

## 分组策略

### 按文件扩展名分组

```typescript
// 分组示例：
// images/   -> .jpg, .png, .gif
// documents/ -> .pdf, .docx, .txt
// videos/   -> .mp4, .avi, .mov
```

### 按创建日期分组

```typescript
// 分组示例：
// 2024-01/ -> 2024 年 1 月创建的文件
// 2024-02/ -> 2024 年 2 月创建的文件
```

### 按文件大小分组

```typescript
// 分组示例：
// tiny-under-1kb/
// small-under-1mb/
// medium-under-100mb/
// large-over-100mb/
```

## 干运行模式

为了安全起见，您可以要求 Copilot 仅预览更改：

```typescript
await session.sendAndWait({
    prompt: `
分析 "${targetFolder}" 中的文件，并向我展示您如何根据文件类型进行组织
的计划。不要移动任何文件，只需展示分组方案。
`,
});
```

## 基于 AI 分析的自定义分组

让 Copilot 根据文件内容确定最佳分组方式：

```typescript
await session.sendAndWait({
    prompt: `
查看 "${targetFolder}" 中的文件，并建议一个合理的组织方式。
考虑以下因素：
- 文件名及其可能包含的内容
- 文件类型及其典型用途
- 可能表示项目或事件的日期模式

提出具有描述性和实用性的文件夹名称。
`,
});
```

## 安全性注意事项

1. **移动前确认**：在执行移动操作前请要求 Copilot 确认
2. **处理重复文件**：考虑如果存在同名文件会发生什么
3. **保留原始文件**：对于重要文件，考虑复制而非移动

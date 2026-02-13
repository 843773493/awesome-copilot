# 生成可访问性报告

构建一个命令行工具，使用 Playwright MCP 服务器分析网页可访问性，并生成符合 WCAG 标准的详细报告，支持可选的测试生成。

> **可运行示例：** [recipe/accessibility-report.ts](recipe/accessibility-report.ts)
>
> ```bash
> cd recipe && npm install
> npx tsx accessibility-report.ts
> # 或：npm run accessibility-report
> ```

## 示例场景

您希望审计网站的可访问性合规性。此工具使用 Playwright 导航到指定 URL，捕获可访问性快照，并生成涵盖地标、标题层级、焦点管理及触摸目标等 WCAG 标准的结构化报告。它还可以生成 Playwright 可访问性测试文件以自动化未来的可访问性检查。

## 先决条件

```bash
npm install @github/copilot-sdk
npm install -D typescript tsx @types/node
```

您还需要 `npx` 可用（已安装 Node.js）以运行 Playwright MCP 服务器。

## 使用方法

```bash
npx tsx accessibility-report.ts
# 当提示时输入 URL
```

## 完整示例：accessibility-report.ts

```typescript
#!/usr/bin/env npx tsx

import { CopilotClient } from "@github/copilot-sdk";
import * as readline from "node:readline";

// ============================================================================
// 主应用程序
// ============================================================================

async function main() {
    console.log("=== 可访问性报告生成器 ===\n");

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    const askQuestion = (query: string): Promise<string> =>
        new Promise((resolve) => rl.question(query, (answer) => resolve(answer.trim())));

    let url = await askQuestion("请输入要分析的 URL：");

    if (!url) {
        console.log("未提供 URL。退出。");
        rl.close();
        return;
    }

    // 确保 URL 包含协议
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        url = "https://" + url;
    }

    console.log(`\n分析中：${url}`);
    console.log("请稍候...\n");

    // 创建使用 Playwright MCP 服务器的 Copilot 客户端
    const client = new CopilotClient();

    const session = await client.createSession({
        model: "claude-opus-4.6",
        streaming: true,
        mcpServers: {
            playwright: {
                type: "local",
                command: "npx",
                args: ["@playwright/mcp@latest"],
                tools: ["*"],
            },
        },
    });

    // 设置流式事件处理
    let idleResolve: (() => void) | null = null;

    session.on((event) => {
        if (event.type === "assistant.message.delta") {
            process.stdout.write(event.data.deltaContent ?? "");
        } else if (event.type === "session.idle") {
            idleResolve?.();
        } else if (event.type === "session.error") {
            console.error(`\n错误：${event.data.message}`);
            idleResolve?.();
        }
    });

    const waitForIdle = (): Promise<void> =>
        new Promise((resolve) => {
            idleResolve = resolve;
        });

    const prompt = `
    使用 Playwright MCP 服务器分析此网页的可访问性：${url}
    
    请执行以下步骤：
    1. 使用 playwright-browser_navigate 导航到 URL
    2. 使用 playwright-browser_snapshot 捕获可访问性快照
    3. 分析快照并提供详细的可访问性报告
    
    使用表情符号指示器格式化报告：
    - 📊 可访问性报告标题
    - ✅ 优点（包含类别、状态、详情的表格）
    - ⚠️ 发现的问题（包含严重性、问题、WCAG 标准、建议的表格）
    - 📋 统计摘要（链接、标题、可聚焦元素、地标）
    - ⚙️ 优先建议
    
    使用 ✅ 表示通过，🔴 表示严重问题，🟡 表示中等严重问题，❌ 表示缺失项。
    包含实际的页面分析结果。
    `;

    let idle = waitForIdle();
    await session.send({ prompt });
    await idle;

    console.log("\n\n=== 报告完成 ===\n");

    // 提示用户是否生成测试文件
    const generateTests = await askQuestion(
        "是否要生成 Playwright 可访问性测试？(y/n): "
    );

    if (generateTests.toLowerCase() === "y" || generateTests.toLowerCase() === "yes") {
        const detectLanguagePrompt = `
        分析当前工作目录以检测主要编程语言。
        仅回复检测到的语言名称和简要说明。
        如果未检测到项目，请建议使用 "TypeScript" 作为默认语言。
        `;

        console.log("\n检测项目语言...\n");
        idle = waitForIdle();
        await session.send({ prompt: detectLanguagePrompt });
        await idle;

        let language = await askQuestion("\n\n确认测试语言（或输入其他语言）：");
        if (!language) language = "TypeScript";

        const testGenerationPrompt = `
        根据您刚刚为 ${url} 生成的可访问性报告，
        创建 ${language} 的 Playwright 可访问性测试文件。
        
        包含以下测试：
        lang 属性、标题、标题层级、alt 文本、
        地标、跳过导航、焦点指示器、触摸目标。
        使用 Playwright 的可访问性测试功能并添加有帮助的注释。
        输出完整的测试文件。
        `;

        console.log("\n生成可访问性测试...\n");
        idle = waitForIdle();
        await session.send({ prompt: testGenerationPrompt });
        await idle;

        console.log("\n\n=== 测试文件已生成 ===");
    }

    rl.close();
    await session.destroy();
    await client.stop();
}

main().catch(console.error);
```

## 工作原理

1. **Playwright MCP 服务器**：配置本地 MCP 服务器运行 `@playwright/mcp` 以提供浏览器自动化工具
2. **流式输出**：使用 `streaming: true` 和 `assistant.message.delta` 事件实现逐令牌实时输出
3. **可访问性快照**：Playwright 的 `browser_snapshot` 工具捕获页面的完整可访问性树
4. **结构化报告**：通过提示词引导模型生成一致的 WCAG 对齐报告格式，使用表情符号表示严重性
5. **测试生成**：可选地检测项目语言并生成 Playwright 可访问性测试文件

## 关键概念

### MCP 服务器配置

该示例配置了一个与会话并行运行的本地 MCP 服务器：

```typescript
const session = await client.createSession({
    mcpServers: {
        playwright: {
            type: "local",
            command: "npx",
            args: ["@playwright/mcp@latest"],
            tools: ["*"],
        },
    },
});
```

这使模型能够访问 Playwright 浏览器工具，如 `browser_navigate`、`browser_snapshot` 和 `browser_click`。

### 流式事件处理

与 `sendAndWait` 不同，该示例使用流式处理实现实时输出：

```typescript
session.on((event) => {
    if (event.type === "assistant.message.delta") {
        process.stdout.write(event.data.deltaContent ?? "");
    } else if (event.type === "session.idle") {
        idleResolve?.();
    }
});
```

## 示例交互

```
=== 可访问性报告生成器 ===

请输入要分析的 URL：github.com

分析中：https://github.com
请稍候...

📊 可访问性报告：GitHub (github.com)

✅ 优点
| 类别 | 状态 | 详情 |
|------|------|------|
| 语言 | ✅ 通过 | lang="en" 设置正确 |
| 页面标题 | ✅ 通过 | "GitHub" 可识别 |
| 标题层级 | ✅ 通过 | 正确的 H1/H2 结构 |
| 图像 | ✅ 通过 | 所有图像均包含 alt 文本 |

⚠️ 发现的问题
| 严重性 | 问题 | WCAG 标准 | 建议 |
|--------|------|-----------|------|
| 🟡 中等 | 部分链接缺少描述性文本 | 2.4.4 | 为仅图标链接添加 aria-label |

📋 统计摘要
- 总链接数：47
- 总标题数：8（1× H1，层级正确）
- 可聚焦元素：52
- 检测到的地标：banner ✅，导航 ✅，主内容 ✅，页脚 ✅

=== 报告完成 ===

是否要生成 Playwright 可访问性测试？(y/n): y

检测项目语言...
检测到 TypeScript（发现 package.json 文件）

确认测试语言（或输入其他语言）： 

生成可访问性测试...
[生成的测试文件输出...]

=== 测试文件已生成 ===
```

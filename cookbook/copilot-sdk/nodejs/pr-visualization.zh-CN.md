# 生成PR年龄图表

构建一个交互式命令行工具，利用Copilot内置功能可视化GitHub仓库中拉取请求（PR）的开放时长分布。

> **可运行示例：** [recipe/pr-visualization.ts](recipe/pr-visualization.ts)
>
> ```bash
> cd recipe && npm install
> # 从当前git仓库自动检测
> npx tsx pr-visualization.ts
>
> # 显式指定仓库
> npx tsx pr-visualization.ts --repo github/copilot-sdk
> # 或者: npm run pr-visualization
> ```

## 示例场景

您想了解某个仓库中拉取请求（PR）已开放多长时间。该工具会检测当前git仓库或接受仓库作为输入，然后让Copilot通过GitHub MCP服务器获取PR数据并生成图表图像。

## 前提条件

```bash
npm install @github/copilot-sdk
npm install -D typescript tsx @types/node
```

## 使用方法

```bash
# 从当前git仓库自动检测
npx tsx pr-visualization.ts

# 显式指定仓库
npx tsx pr-visualization.ts --repo github/copilot-sdk
```

## 完整示例：pr-visualization.ts

```typescript
#!/usr/bin/env npx tsx

import { execSync } from "node:child_process";
import * as readline from "node:readline";
import { CopilotClient } from "@github/copilot-sdk";

// ============================================================================
// Git & GitHub 检测
// ============================================================================

function isGitRepo(): boolean {
    try {
        execSync("git rev-parse --git-dir", { stdio: "ignore" });
        return true;
    } catch {
        return false;
    }
}

function getGitHubRemote(): string | null {
    try {
        const remoteUrl = execSync("git remote get-url origin", {
            encoding: "utf-8",
        }).trim();

        // 处理SSH: git@github.com:owner/repo.git
        const sshMatch = remoteUrl.match(/git@github\.com:(.+\/.+?)(?:\.git)?$/);
        if (sshMatch) return sshMatch[1];

        // 处理HTTPS: https://github.com/owner/repo.git
        const httpsMatch = remoteUrl.match(/https:\/\/github\.com\/(.+\/.+?)(?:\.git)?$/);
        if (httpsMatch) return httpsMatch[1];

        return null;
    } catch {
        return null;
    }
}

function parseArgs(): { repo?: string } {
    const args = process.argv.slice(2);
    const repoIndex = args.indexOf("--repo");
    if (repoIndex !== -1 && args[repoIndex + 1]) {
        return { repo: args[repoIndex + 1] };
    }
    return {};
}

async function promptForRepo(): Promise<string> {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });
    return new Promise((resolve) => {
        rl.question("请输入GitHub仓库（格式为owner/repo）: ", (answer) => {
            rl.close();
            resolve(answer.trim());
        });
    });
}

// ============================================================================
// 主程序
// ============================================================================

async function main() {
    console.log("🔍 PR年龄图表生成器\n");

    // 确定仓库
    const args = parseArgs();
    let repo: string;

    if (args.repo) {
        repo = args.repo;
        console.log(`📦 使用指定的仓库: ${repo}`);
    } else if (isGitRepo()) {
        const detected = getGitHubRemote();
        if (detected) {
            repo = detected;
            console.log(`📦 检测到GitHub仓库: ${repo}`);
        } else {
            console.log("⚠️  检测到git仓库但未找到GitHub远程仓库。");
            repo = await promptForRepo();
        }
    } else {
        console.log("📁 不在git仓库中。");
        repo = await promptForRepo();
    }

    if (!repo || !repo.includes("/")) {
        console.error("❌ 仓库格式无效。请使用格式：owner/repo");
        process.exit(1);
    }

    const [owner, repoName] = repo.split("/");

    // 创建Copilot客户端 - 无需自定义工具！
    const client = new CopilotClient({ logLevel: "error" });

    const session = await client.createSession({
        model: "gpt-5",
        systemMessage: {
            content: `
<context>
您正在分析GitHub仓库: ${owner}/${repoName} 的拉取请求
当前工作目录是: ${process.cwd()}
</context>

<instructions>
- 使用GitHub MCP服务器工具获取PR数据
- 使用文件和代码执行工具生成图表
- 将生成的图像保存到当前工作目录
- 回答要简洁
</instructions>
`,
        },
    });

    // 设置事件处理
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    session.on((event) => {
        if (event.type === "assistant.message") {
            console.log(`\n🤖 ${event.data.content}\n`);
        } else if (event.type === "tool.execution_start") {
            console.log(`  ⚙️  ${event.data.toolName}`);
        }
    });

    // 初始提示 - 让Copilot自行确定细节
    console.log("\n📊 开始分析...\n");

    await session.sendAndWait({
        prompt: `
      获取${owner}/${repoName}过去一周的开放拉取请求
      计算每个PR的开放天数
      然后生成一个显示PR开放时长分布的条形图
      （将它们分组到如<1天、1-3天等合理区间）
      将图表保存为当前目录下的"pr-age-chart.png"
      最后总结PR健康状况 - 平均开放天数、最老的PR以及可能被认为是过期的PR数量
    `,
    });

    // 交互式循环
    const askQuestion = () => {
        rl.question("您: ", async (input) => {
            const trimmed = input.trim();

            if (trimmed.toLowerCase() === "exit" || trimmed.toLowerCase() === "quit") {
                console.log("👋 再见！");
                rl.close();
                await session.destroy();
                await client.stop();
                process.exit(0);
            }

            if (trimmed) {
                await session.sendAndWait({ prompt: trimmed });
            }

            askQuestion();
        });
    };

    console.log('💡 可提出后续问题或输入"exit"退出。\n');
    console.log("示例：");
    console.log('  - "扩展到过去一个月"');
    console.log('  - "显示5个最老的PR"');
    console.log('  - "生成饼图代替条形图"');
    console.log('  - "按作者而非年龄分组"');
    console.log("");

    askQuestion();
}

main().catch(console.error);
```

## 工作原理

1. **仓库检测**：检查`--repo`标志 → git远程仓库 → 提示用户输入
2. **无需自定义工具**：完全依赖Copilot CLI内置功能：
    - **GitHub MCP服务器** - 从GitHub获取PR数据
    - **文件工具** - 保存生成的图表图像
    - **代码执行** - 使用Python/matplotlib或其他方法生成图表
3. **交互式会话**：初始分析后，用户可以提出调整请求

## 示例交互

```
🔍 PR年龄图表生成器

📦 使用指定的仓库: CommunityToolkit/Aspire

📊 开始分析...

  ⚙️  github-mcp-server-list_pull_requests
  ⚙️  powershell

🤖 我已分析了CommunityToolkit/Aspire仓库的23个开放PR：

**PR年龄分布：**
- < 1天: 3个PR
- 1-3天: 5个PR
- 3-7天: 8个PR
- 1-2周: 4个PR
- > 2周: 3个PR

**总结：**
- 平均年龄: 6.2天
- 最老的PR: PR #142 (18天) - "添加Redis缓存支持"
- 可能过期 (>7天): 7个PR

图表已保存到: pr-age-chart.png

💡 可提出后续问题或输入"exit"退出。

您: 扩展到过去一个月并按作者显示

  ⚙️  github-mcp-server-list_pull_requests
  ⚙️  powershell

🤖 更新了过去30天的分析，按作者分组：

| 作者        | 开放PR数 | 平均年龄 |
|---------------|----------|---------|
| @contributor1 | 5        | 12天  |
| @contributor2 | 3        | 4天  |
| @contributor3 | 2        | 8天  |
| ...           |          |         |

新图表已保存到: pr-age-chart.png

您: 生成一个显示年龄分布的饼图

  ⚙️  powershell

🤖 完成！饼图已保存到: pr-age-chart.png
```

## 为何采用此方法？

| 方面          | 自定义工具      | 内置Copilot                  |
| --------------- | ----------------- | --------------------------------- |
| 代码复杂度 | 高              | **极简**                       |
| 维护       | 您负责维护      | **Copilot负责维护**             |
| 灵活性     | 固定逻辑       | **AI决定最佳方案**      |
| 图表类型   | 仅限您编写的类型    | **Copilot能生成的任何类型** |
| 数据分组   | 固定桶区间 | **智能分组**          |

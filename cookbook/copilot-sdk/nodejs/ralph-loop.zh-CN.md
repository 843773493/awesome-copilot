# Ralph Loop：自主AI任务循环

构建自主编码循环，其中AI代理选择任务、实现任务、通过背压（测试、构建）进行验证、提交更改，并重复这一过程——每个迭代都在一个全新的上下文窗口中进行。

> **可运行示例：** [recipe/ralph-loop.ts](recipe/ralph-loop.ts)
>
> ```bash
> npm install
> npx tsx recipe/ralph-loop.ts
> ```

## 什么是Ralph Loop？

[Ralph Loop](https://ghuntley.com/ralph/) 是一种自主开发工作流，其中AI代理在隔离的上下文窗口中迭代执行任务。关键洞察：**状态存储在磁盘上，而非模型的上下文中**。每次迭代都从头开始，读取当前状态文件，执行一个任务，将结果写回磁盘，并退出。

```
┌─────────────────────────────────────────────────┐
│                   loop.sh                       │
│  while true:                                    │
│    ┌─────────────────────────────────────────┐  │
│    │  新的会话（隔离上下文）                  │  │
│    │                                         │  │
│    │  1. 读取 PROMPT.md + AGENTS.md           │  │
│    │  2. 研究 specs/* 和代码                   │  │
│    │  3. 从计划中选择下一个任务                │  │
│    │  4. 实现 + 运行测试                        │  │
│    │  5. 更新计划，提交并退出                   │  │
│    └─────────────────────────────────────────┘  │
│    ↻ 下一个迭代（新的上下文）                   │
└─────────────────────────────────────────────────┘
```

**核心原则：**

- **每次迭代使用新的上下文环境**：每个循环创建一个新的会话——不积累上下文，始终处于“智能区”
- **磁盘作为共享状态**：`IMPLEMENTATION_PLAN.md` 在迭代之间持久化，并作为协调机制
- **背压引导质量**：测试、构建和代码检查会拒绝低质量工作——代理必须在提交前修复问题
- **两种模式**：规划模式（差距分析 → 生成计划）和构建模式（根据计划实现）

## 简单版本

最简化的Ralph循环——相当于SDK中的 `while :; do cat PROMPT.md | copilot ; done`：

```typescript
import { readFile } from "fs/promises";
import { CopilotClient } from "@github/copilot-sdk";

async function ralphLoop(promptFile: string, maxIterations: number = 50) {
  const client = new CopilotClient();
  await client.start();

  try {
    const prompt = await readFile(promptFile, "utf-8");

    for (let i = 1; i <= maxIterations; i++) {
      console.log(`\n=== 第${i}次迭代/${maxIterations}次 ===`);

      // 每次迭代使用新的会话——上下文隔离是关键
      const session = await client.createSession({ model: "gpt-5.1-codex-mini" });
      try {
        await session.sendAndWait({ prompt }, 600_000);
      } finally {
        await session.destroy();
      }

      console.log(`第${i}次迭代完成。`);
    }
  } finally {
    await client.stop();
  }
}

// 使用方法：指向你的 PROMPT.md 文件
ralphLoop("PROMPT.md", 20);
```

这便是你开始的全部所需。提示文件告诉代理要做什么；代理读取项目文件、执行任务、提交更改并退出。每次循环都会从零开始。

## 理想版本

包含规划和构建模式的完整Ralph模式，与[Ralph Playbook](https://github.com/ClaytonFarr/ralph-playbook) 架构一致：

```typescript
import { readFile } from "fs/promises";
import { CopilotClient } from "@github/copilot-sdk";

type Mode = "plan" | "build";

async function ralphLoop(mode: Mode, maxIterations: number = 50) {
  const promptFile = mode === "plan" ? "PROMPT_plan.md" : "PROMPT_build.md";
  const client = new CopilotClient();
  await client.start();

  console.log(`模式: ${mode} | 提示文件: ${promptFile}`);

  try {
    const prompt = await readFile(promptFile, "utf-8");

    for (let i = 1; i <= maxIterations; i++) {
      console.log(`\n=== 第${i}次迭代/${maxIterations}次 ===`);

      const session = await client.createSession({
        model: "gpt-5.1-codex-mini",
        // 将代理固定在项目目录中
        workingDirectory: process.cwd(),
        // 自动批准工具调用以实现无人值守操作
        onPermissionRequest: async () => ({ allow: true }),
      });

      // 记录工具使用情况以便观察
      session.on((event) => {
        if (event.type === "tool.execution_start") {
          console.log(`  ⚙ ${event.data.toolName}`);
        }
      });

      try {
        await session.sendAndWait({ prompt }, 600_000);
      } finally {
        await session.destroy();
      }

      console.log(`第${i}次迭代完成。`);
    }
  } finally {
    await client.stop();
  }
}

// 解析CLI参数：npx tsx ralph-loop.ts [plan] [max_iterations]
const args = process.argv.slice(2);
const mode: Mode = args.includes("plan") ? "plan" : "build";
const maxArg = args.find((a) => /^\d+$/.test(a));
const maxIterations = maxArg ? parseInt(maxArg) : 50;

ralphLoop(mode, maxIterations);
```

### 必需的项目文件

理想版本期望你的项目具有以下文件结构：

```
project-root/
├── PROMPT_plan.md              # 规划模式的指令
├── PROMPT_build.md             # 构建模式的指令
├── AGENTS.md                   # 操作指南（构建/测试命令）
├── IMPLEMENTATION_PLAN.md      # 任务列表（由规划模式生成）
├── specs/                      # 需求规格（每个主题一个文件）
│   ├── auth.md
│   └── data-pipeline.md
└── src/                        # 你的源代码
```

### 示例 `PROMPT_plan.md`

```markdown
0a. 研究 `specs/*` 以了解应用程序规格。
0b. 研究 IMPLEMENTATION_PLAN.md（如果存在）以理解当前计划。
0c. 研究 `src/` 以了解现有代码和共享工具。

1. 将规格与代码进行对比（差距分析）。创建或更新 IMPLEMENTATION_PLAN.md 作为待实现任务的优先级列表，不要执行任何实现。

重要提示：不要假设功能缺失——首先在代码库中搜索以确认。优先更新现有工具而非创建临时副本。
```

### 示例 `PROMPT_build.md`

```markdown
0a. 研究 `specs/*` 以了解应用程序规格。
0b. 研究 IMPLEMENTATION_PLAN.md。
0c. 研究 `src/` 作为参考。

1. 从 IMPLEMENTATION_PLAN.md 中选择最重要的项目。在进行更改前，搜索代码库（不要假设未实现）。
2. 实现后运行测试。如果功能缺失，添加它。
3. 当发现问题时，立即更新 IMPLEMENTATION_PLAN.md。
4. 当测试通过时，更新 IMPLEMENTATION_PLAN.md，然后执行 `git add -A`，再使用描述性消息执行 `git commit`。

5. 在编写文档时，记录原因。
6. 完整实现。不要使用占位符或草稿。
7. 保持 IMPLEMENTATION_PLAN.md 的最新状态——后续迭代依赖于此。
```

### 示例 `AGENTS.md`

保持简短（约60行）。每次迭代都会加载此文件，因此冗余内容会浪费上下文。

```markdown
## 构建与运行

npm run build

## 验证

- 测试：`npm test`
- 类型检查：`npx tsc --noEmit`
- 代码检查：`npm run lint`
```

## 最佳实践

1. **每次迭代使用新的上下文环境**：不要在迭代之间积累上下文——这是整个设计的核心
2. **磁盘即你的数据库**：`IMPLEMENTATION_PLAN.md` 是隔离会话之间的共享状态
3. **背压至关重要**：`AGENTS.md` 中的测试、构建和代码检查——代理必须通过这些检查才能提交
4. **从规划模式开始**：首先生成计划，然后切换到构建模式
5. **观察并调整**：观察早期迭代，当代理以特定方式失败时，向提示中添加约束条件
6. **计划是可丢弃的**：如果代理偏离轨道，删除 `IMPLEMENTATION_PLAN.md` 并重新生成计划
7. **保持 `AGENTS.md` 简洁**：每次迭代都会加载此文件——仅包含操作信息，不包含进度说明
8. **使用沙箱**：代理可以自主运行并拥有完整工具访问权限——将其隔离
9. **设置 `workingDirectory`**：将会话固定在项目根目录，以便工具操作正确解析路径
10. **自动批准权限请求**：使用 `onPermissionRequest` 允许工具调用而不停止循环

## 何时使用Ralph Loop

**适用于：**

- 从规格中实现功能并进行测试驱动的验证
- 将大型重构拆分为多个小任务
- 无人值守的长时间开发，且需求明确
- 任何可以通过背压（测试/构建）验证正确性的任务

**不适用于：**

- 需要人类判断的循环中任务
- 不需要迭代的单次操作
- 缺乏可测试验收标准的模糊需求
- 方向不明确的探索性原型设计

## 参见

- [错误处理](error-handling.md) —— 长时间会话的超时模式和优雅关闭
- [会话持久化](persisting-sessions.md) —— 跨重启保存和恢复会话

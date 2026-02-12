# Ralph Loop：自主AI任务循环

构建自主编码循环，其中AI代理选择任务、实现任务、通过回压（测试、构建）进行验证、提交更改，并重复这一过程——每次迭代都在一个全新的上下文窗口中进行。

> **可运行示例：** [recipe/ralph-loop.go](recipe/ralph-loop.go)
>
> ```bash
> cd go
> go run recipe/ralph-loop.go
> ```

## 什么是Ralph Loop？

[Ralph Loop](https://ghuntley.com/ralph/) 是一种自主开发流程，AI代理在隔离的上下文窗口中迭代执行任务。关键洞察：**状态存储在磁盘上，而非模型的上下文中**。每次迭代都从头开始，读取当前状态文件，执行一项任务，将结果写回磁盘，然后退出。

```
┌─────────────────────────────────────────────────┐
│                   loop.sh                       │
│  while true:                                    │
│    ┌─────────────────────────────────────────┐  │
│    │  新会话（隔离上下文）                   │  │
│    │                                         │  │
│    │  1. 读取 PROMPT.md + AGENTS.md          │  │
│    │  2. 研究 specs/* 和代码                 │  │
│    │  3. 从计划中选择下一个任务               │  │
│    │  4. 实现 + 运行测试                       │  │
│    │  5. 更新计划，提交，退出                  │  │
│    └─────────────────────────────────────────┘  │
│    ↻ 下一次迭代（全新上下文）                   │
└─────────────────────────────────────────────────┘
```

**核心原则：**

- **每次迭代使用独立上下文**：每个循环创建一个新会话——不累积上下文，始终处于“智能区”
- **磁盘作为共享状态**：`IMPLEMENTATION_PLAN.md` 在迭代之间持久化，并作为协调机制
- **回压引导质量**：测试、构建和检查在 `AGENTS.md` 中定义——代理必须通过这些验证才能提交
- **两种模式**：计划模式（差距分析 → 生成计划）和构建模式（根据计划实现）

## 简单版本

最简化的Ralph循环——相当于SDK中的 `while :; do cat PROMPT.md | copilot ; done`：

```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	copilot "github.com/github/copilot-sdk/go"
)

func ralphLoop(ctx context.Context, promptFile string, maxIterations int) error {
	client := copilot.NewClient(nil)
	if err := client.Start(ctx); err != nil {
		return err
	}
	defer client.Stop()

	prompt, err := os.ReadFile(promptFile)
	if err != nil {
		return err
	}

	for i := 1; i <= maxIterations; i++ {
		fmt.Printf("\n=== 第 %d 次迭代/%d ===\n", i, maxIterations)

		// 每次迭代创建新的会话 — 上下文隔离是关键
		session, err := client.CreateSession(ctx, &copilot.SessionConfig{
			Model: "gpt-5.1-codex-mini",
		})
		if err != nil {
			return err
		}

		_, err = session.SendAndWait(ctx, copilot.MessageOptions{
			Prompt: string(prompt),
		})
		session.Destroy()
		if err != nil {
			return err
		}

		fmt.Printf("第 %d 次迭代完成。\n", i)
	}
	return nil
}

func main() {
	if err := ralphLoop(context.Background(), "PROMPT.md", 20); err != nil {
		log.Fatal(err)
	}
}
```

以上内容即可开始使用。提示文件告诉代理要做什么；代理读取项目文件、执行任务、提交更改并退出。循环会以干净的环境重新启动。

## 理想版本

完整Ralph模式，包含计划和构建两种模式，与[Ralph Playbook](https://github.com/ClaytonFarr/ralph-playbook) 架构一致：

```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	copilot "github.com/github/copilot-sdk/go"
)

func ralphLoop(ctx context.Context, mode string, maxIterations int) error {
	promptFile := "PROMPT_build.md"
	if mode == "plan" {
		promptFile = "PROMPT_plan.md"
	}

	client := copilot.NewClient(nil)
	if err := client.Start(ctx); err != nil {
		return err
	}
	defer client.Stop()

	cwd, _ := os.Getwd()

	fmt.Println(strings.Repeat("━", 40))
	fmt.Printf("模式:   %s\n", mode)
	fmt.Printf("提示: %s\n", promptFile)
	fmt.Printf("最大:    %d 次迭代\n", maxIterations)
	fmt.Println(strings.Repeat("━", 40))

	prompt, err := os.ReadFile(promptFile)
	if err != nil {
		return err
	}

	for i := 1; i <= maxIterations; i++ {
		fmt.Printf("\n=== 第 %d 次迭代/%d ===\n", i, maxIterations)

		session, err := client.CreateSession(ctx, &copilot.SessionConfig{
			Model:            "gpt-5.1-codex-mini",
			WorkingDirectory: cwd,
			OnPermissionRequest: func(_ copilot.PermissionRequest, _ map[string]string) copilot.PermissionRequestResult {
				return copilot.PermissionRequestResult{Kind: "approved"}
			},
		})
		if err != nil {
			return err
		}

		// 记录工具使用情况以供观察
		session.On(func(event copilot.Event) {
			if toolExecution, ok := event.(copilot.ToolExecutionStartEvent); ok {
				fmt.Printf("  ⚙ %s\n", toolExecution.Data.ToolName)
			}
		})

		_, err = session.SendAndWait(ctx, copilot.MessageOptions{
			Prompt: string(prompt),
		})
		session.Destroy()
		if err != nil {
			return err
		}

		fmt.Printf("\n第 %d 次迭代完成。\n", i)
	}

	fmt.Printf("\n达到最大迭代次数: %d\n", maxIterations)
	return nil
}

func main() {
	mode := "build"
	maxIterations := 50

	for _, arg := range os.Args[1:] {
		if arg == "plan" {
			mode = "plan"
		} else if n, err := strconv.Atoi(arg); err == nil {
			maxIterations = n
		}
	}

	if err := ralphLoop(context.Background(), mode, maxIterations); err != nil {
		log.Fatal(err)
	}
}
```

### 必需的项目文件

理想版本期望你的项目具有以下文件结构：

```
project-root/
├── PROMPT_plan.md              # 计划模式的指令
├── PROMPT_build.md             # 构建模式的指令
├── AGENTS.md                   # 操作指南（构建/测试命令）
├── IMPLEMENTATION_PLAN.md      # 任务列表（由计划模式生成）
├── specs/                      # 需求规格（每个主题一个）
│   ├── auth.md
│   └── data-pipeline.md
└── src/                        # 你的源代码
```

### 示例 `PROMPT_plan.md`

```markdown
0a. 研究 `specs/*` 以了解应用程序规格。
0b. 研究 IMPLEMENTATION_PLAN.md（如果存在）以了解当前的计划。
0c. 研究 `src/` 以理解现有代码和共享工具。

1. 将规格与代码进行比较（差距分析）。创建或更新
   IMPLEMENTATION_PLAN.md 作为待实现任务的优先级项目符号列表。
   不要实现任何内容。

重要提示：不要假设功能缺失——首先搜索代码库以确认。
优先更新现有工具，而非创建临时副本。
```

### 示例 `PROMPT_build.md`

```markdown
0a. 研究 `specs/*` 以了解应用程序规格。
0b. 研究 IMPLEMENTATION_PLAN.md。
0c. 以参考为目的研究 `src/`。

1. 从 IMPLEMENTATION_PLAN.md 中选择最重要的任务。在进行更改前，搜索代码库（不要假设未实现）。
2. 实现后运行测试。如果功能缺失，请添加它。
3. 当发现问题时，立即更新 IMPLEMENTATION_PLAN.md。
4. 测试通过后，更新 IMPLEMENTATION_PLAN.md，然后执行 `git add -A`
   并用描述性信息执行 `git commit`。

5. 在编写文档时，记录原因。
6. 完全实现功能。不要使用占位符或草稿。
7. 保持 IMPLEMENTATION_PLAN.md 的最新状态——后续迭代依赖于此。
```

### 示例 `AGENTS.md`

保持简短（约60行）。每次迭代都会加载此文件，因此冗余会浪费上下文。

```markdown
## 构建与运行

go build ./...

## 验证

- 测试: `go test ./...`
- 检查: `go vet ./...`
```

## 最佳实践

1. **每次迭代使用独立上下文**：不要在迭代之间累积上下文——这是整个设计的核心
2. **磁盘是你的数据库**：`IMPLEMENTATION_PLAN.md` 是隔离会话之间的共享状态
3. **回压至关重要**：`AGENTS.md` 中的测试、构建和检查——代理必须通过这些验证才能提交
4. **从计划模式开始**：首先生成计划，然后切换到构建模式
5. **观察并调整**：观察早期迭代，当代理以特定方式失败时，向提示中添加限制条件
6. **计划是可丢弃的**：如果代理偏离轨道，删除 `IMPLEMENTATION_PLAN.md` 并重新生成计划
7. **保持 `AGENTS.md` 简短**：每次迭代都会加载该文件——仅包含操作信息，不包含进度说明
8. **使用沙箱**：代理以全工具访问权限自主运行——将其隔离
9. **设置 `WorkingDirectory`**：将会话固定在项目根目录，以确保工具操作路径正确解析
10. **自动批准权限**：使用 `OnPermissionRequest` 允许工具调用，而不会中断循环

## 何时使用Ralph Loop

**适用于：**

- 从规格中实现功能并进行测试驱动的验证
- 将大型重构拆分为许多小任务
- 无需人工干预的长期开发，且需求明确
- 任何可以通过回压（测试/构建）验证正确性的任务

**不适用于：**

- 循环中需要人类判断的任务
- 无需迭代的一次性操作
- 没有可测试验收标准的模糊需求
- 方向不明确的探索性原型设计

## 参见

- [错误处理](error-handling.md) — 长会话的超时模式和优雅关闭
- [会话持久化](persisting-sessions.md) — 在重启之间保存和恢复会话

# Ralph Loop：自主AI任务循环

构建自主编码循环，其中AI代理选择任务、实现、通过回压（测试、构建）进行验证、提交并重复——每个迭代都在一个全新的上下文窗口中进行。

> **可运行示例：** [recipe/ralph_loop.py](recipe/ralph_loop.py)
>
> 从仓库根目录安装依赖并运行：
>
> ```bash
> pip install -r cookbook/copilot-sdk/python/recipe/requirements.txt
> python cookbook/copilot-sdk/python/recipe/ralph_loop.py
> ```
>
> 在运行循环之前，请确保当前工作目录中存在 `PROMPT_build.md` 和 `PROMPT_plan.md` 文件。

## 什么是Ralph Loop？

[Ralph loop](https://ghuntley.com/ralph/) 是一种自主开发工作流，其中AI代理在隔离的上下文窗口中迭代执行任务。关键洞察：**状态存储在磁盘上，而非模型的上下文中**。每次迭代都从头开始，读取文件中的当前状态，执行一个任务，将结果写回磁盘，然后退出。

```
┌─────────────────────────────────────────────────┐
│                   loop.sh                       │
│  while true:                                    │
│    ┌─────────────────────────────────────────┐  │
│    │  新鲜会话（隔离上下文）                   │  │
│    │                                         │  │
│    │  1. 读取 PROMPT.md + AGENTS.md            │  │
│    │  2. 研究 specs/* 和代码                   │  │
│    │  3. 从计划中选择下一个任务                │  │
│    │  4. 实现 + 运行测试                        │  │
│    │  5. 更新计划，提交，退出                    │  │
│    └─────────────────────────────────────────┘  │
│    ↻ 下一个迭代（新鲜上下文）                    │
└─────────────────────────────────────────────────┘
```

**核心原则：**

- **每次迭代使用新鲜上下文**：每个循环都会创建一个新会话——不累积上下文，始终处于“智能区”
- **磁盘作为共享状态**：`IMPLEMENTATION_PLAN.md` 在迭代之间持久化，并作为协调机制
- **回压引导质量**：测试、构建和代码检查会拒绝低质量工作——代理必须在提交前修复问题
- **两种模式**：规划模式（差距分析 → 生成计划）和构建模式（根据计划实现）

## 简化版本

最小化的Ralph循环——相当于SDK中的 `while :; do cat PROMPT.md | copilot ; done`：

```python
import asyncio
from pathlib import Path
from copilot import CopilotClient, MessageOptions, SessionConfig


async def ralph_loop(prompt_file: str, max_iterations: int = 50):
    client = CopilotClient()
    await client.start()

    try:
        prompt = Path(prompt_file).read_text()

        for i in range(1, max_iterations + 1):
            print(f"\n=== 第{i}/{max_iterations}次迭代 ===")

            # 每次迭代创建新会话——上下文隔离是关键
            session = await client.create_session(
                SessionConfig(model="gpt-5.1-codex-mini")
            )
            try:
                await session.send_and_wait(
                    MessageOptions(prompt=prompt), timeout=600
                )
            finally:
                await session.destroy()

            print(f"第{i}次迭代完成。")
    finally:
        await client.stop()


# 使用方式：指向你的 PROMPT.md
asyncio.run(ralph_loop("PROMPT.md", 20))
```

这便是你开始的全部所需。提示文件告诉代理要做什么；代理读取项目文件、完成工作、提交并退出。循环会以干净的状态重新启动。

## 理想版本

包含规划和构建模式的完整Ralph模式，与[Ralph Playbook](https://github.com/ClaytonFarr/ralph-playbook) 架构一致：

```python
import asyncio
import sys
from pathlib import Path

from copilot import CopilotClient, MessageOptions, SessionConfig


async def ralph_loop(mode: str = "build", max_iterations: int = 50):
    prompt_file = "PROMPT_plan.md" if mode == "plan" else "PROMPT_build.md"
    client = CopilotClient()
    await client.start()

    print("━" * 40)
    print(f"模式:   {mode}")
    print(f"提示:   {prompt_file}")
    print(f"最大:   {max_iterations} 次迭代")
    print("━" * 40)

    try:
        prompt = Path(prompt_file).read_text()

        for i in range(1, max_iterations + 1):
            print(f"\n=== 第{i}/{max_iterations}次迭代 ===")

            session = await client.create_session(SessionConfig(
                model="gpt-5.1-codex-mini",
                # 将代理固定在项目目录
                working_directory=str(Path.cwd()),
                # 自动批准工具调用以实现无人值守操作
                on_permission_request=lambda _req, _ctx: {
                    "kind": "approved", "rules": []
                },
            ))

            # 记录工具使用情况以提高可见性
            def log_tool_event(event):
                if event.type.value == "tool.execution_start":
                    print(f"  ⚙ {event.data.tool_name}")

            session.on(log_tool_event)

            try:
                await session.send_and_wait(
                    MessageOptions(prompt=prompt), timeout=600
                )
            finally:
                await session.destroy()

            print(f"\n第{i}次迭代完成。")

        print(f"\n达到最大迭代次数: {max_iterations}")
    finally:
        await client.stop()


if __name__ == "__main__":
    args = sys.argv[1:]
    mode = "plan" if "plan" in args else "build"
    max_iter = next((int(a) for a in args if a.isdigit()), 50)
    asyncio.run(ralph_loop(mode, max_iter))
```

### 所需项目文件

理想版本期望你的项目具有以下文件结构：

```
project-root/
├── PROMPT_plan.md              # 规划模式的指令
├── PROMPT_build.md             # 构建模式的指令
├── AGENTS.md                   # 操作指南（构建/测试命令）
├── IMPLEMENTATION_PLAN.md      # 任务列表（由规划模式生成）
├── specs/                      # 需求规范（每个主题一个文件）
│   ├── auth.md
│   └── data-pipeline.md
└── src/                        # 你的源代码
```

### 示例 `PROMPT_plan.md`

```markdown
0a. 研究 `specs/*` 以了解应用程序规范。
0b. 研究 IMPLEMENTATION_PLAN.md（如果存在）以理解当前计划。
0c. 研究 `src/` 以了解现有代码和共享工具。

1. 将规范与代码进行比较（差距分析）。创建或更新
   IMPLEMENTATION_PLAN.md 作为尚未实现的任务优先级列表，以项目符号形式呈现。
   不要实现任何内容。

重要提示：不要假设功能缺失——首先在代码库中搜索以确认。优先更新现有工具，而不是创建临时副本。
```

### 示例 `PROMPT_build.md`

```markdown
0a. 研究 `specs/*` 以了解应用程序规范。
0b. 研究 IMPLEMENTATION_PLAN.md。
0c. 研究 `src/` 作为参考。

1. 从 IMPLEMENTATION_PLAN.md 中选择最重要的条目。在进行更改前，搜索代码库（不要假设未实现）。
2. 实现后，运行测试。如果功能缺失，请添加它。
3. 当你发现新问题时，立即更新 IMPLEMENTATION_PLAN.md。
4. 当测试通过时，更新 IMPLEMENTATION_PLAN.md，然后执行 `git add -A`
   然后使用描述性信息执行 `git commit`。

5. 在编写文档时，记录原因。
6. 完全实现功能。不要使用占位符或草稿。
7. 保持 IMPLEMENTATION_PLAN.md 的最新状态——后续迭代依赖于此。
```

### 示例 `AGENTS.md`

保持简短（约60行）。每次迭代都会加载此文件，因此冗余会浪费上下文。

```markdown
## 构建与运行

python -m pytest

## 验证

- 测试: `pytest`
- 类型检查: `mypy src/`
- 代码检查: `ruff check src/`
```

## 最佳实践

1. **每次迭代使用新鲜上下文**：不要在迭代之间累积上下文——这是整个设计的核心
2. **磁盘是你的数据库**：`IMPLEMENTATION_PLAN.md` 是隔离会话之间的共享状态
3. **回压至关重要**：`AGENTS.md` 中的测试、构建和代码检查——代理必须通过这些检查才能提交
4. **从规划模式开始**：首先生成计划，然后切换到构建模式
5. **观察并调整**：观察早期迭代，当代理以特定方式失败时，向提示中添加约束条件
6. **计划是可丢弃的**：如果代理偏离轨道，删除 `IMPLEMENTATION_PLAN.md` 并重新生成计划
7. **保持 `AGENTS.md` 简洁**：每次迭代都会加载此文件——仅包含操作信息，不包含进度说明
8. **使用沙箱**：代理在完全工具访问权限下自主运行——将其隔离
9. **设置 `working_directory`**：将会话固定在项目根目录，以便工具操作正确解析路径
10. **自动批准权限请求**：使用 `on_permission_request` 允许工具调用，而不会中断循环

## 何时使用Ralph Loop

**适用于：**

- 从规范中实现功能并进行测试驱动验证
- 将大型重构分解为多个小任务
- 无人值守的长期开发，具有明确的需求
- 任何可以通过回压（测试/构建）验证正确性的任务

**不适用于：**

- 需要循环中进行人工判断的任务
- 无需迭代的单次操作
- 缺乏可测试验收标准的模糊需求
- 方向不明确的探索性原型设计

## 参见

- [错误处理](error-handling.md) —— 长会话的超时模式和优雅关闭
- [会话持久化](persisting-sessions.md) —— 跨重启保存和恢复会话

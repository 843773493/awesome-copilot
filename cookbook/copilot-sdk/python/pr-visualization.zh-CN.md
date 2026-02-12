# 生成PR年龄图表

构建一个交互式命令行工具，使用Copilot内置功能可视化GitHub仓库中拉取请求（PR）的开放时间分布情况。

> **可运行示例：** [recipe/pr_visualization.py](recipe/pr_visualization.py)
>
> ```bash
> cd recipe && pip install -r requirements.txt
> # 从当前git仓库自动检测
> python pr_visualization.py
>
> # 显式指定仓库
> python pr_visualization.py --repo github/copilot-sdk
> ```

## 示例场景

您希望了解某个仓库中PR已开放的时间长度。此工具可以检测当前Git仓库或接受仓库输入，然后让Copilot通过GitHub MCP Server获取PR数据并生成图表图像。

## 前提条件

```bash
pip install github-copilot-sdk
```

## 用法

```bash
# 从当前git仓库自动检测
python pr_visualization.py

# 显式指定仓库
python pr_visualization.py --repo github/copilot-sdk
```

## 完整示例：pr_visualization.py

```python
#!/usr/bin/env python3

import asyncio
import subprocess
import sys
import os
import re
from copilot import (
    CopilotClient, SessionConfig, MessageOptions,
    SessionEvent, SessionEventType,
)

# ============================================================================
# Git与GitHub检测
# ============================================================================

def is_git_repo():
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            check=True,
            capture_output=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_github_remote():
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            check=True,
            capture_output=True,
            text=True
        )
        remote_url = result.stdout.strip()

        # 处理SSH格式：git@github.com:owner/repo.git
        ssh_match = re.search(r"git@github\.com:(.+/.+?)(?:\.git)?$", remote_url)
        if ssh_match:
            return ssh_match.group(1)

        # 处理HTTPS格式：https://github.com/owner/repo.git
        https_match = re.search(r"https://github\.com/(.+/.+?)(?:\.git)?$", remote_url)
        if https_match:
            return https_match.group(1)

        return None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def parse_args():
    args = sys.argv[1:]
    if "--repo" in args:
        idx = args.index("--repo")
        if idx + 1 < len(args):
            return {"repo": args[idx + 1]}
    return {}

def prompt_for_repo():
    return input("请输入GitHub仓库（格式为owner/repo）: ").strip()

# ============================================================================
# 主程序
# ============================================================================

async def main():
    print("🔍 PR年龄图表生成器\n")

    # 确定仓库
    args = parse_args()
    repo = None

    if "repo" in args:
        repo = args["repo"]
        print(f"📦 使用指定的仓库: {repo}")
    elif is_git_repo():
        detected = get_github_remote()
        if detected:
            repo = detected
            print(f"📦 检测到GitHub仓库: {repo}")
        else:
            print("⚠️  检测到git仓库但未找到GitHub远程仓库。")
            repo = prompt_for_repo()
    else:
        print("📁 不在git仓库中。")
        repo = prompt_for_repo()

    if not repo or "/" not in repo:
        print("❌ 仓库格式无效。预期格式：owner/repo")
        sys.exit(1)

    owner, repo_name = repo.split("/", 1)

    # 创建Copilot客户端
    client = CopilotClient()
    await client.start()

    session = await client.create_session(SessionConfig(
        model="gpt-5",
        system_message={
            "content": f"""
<context>
您正在分析GitHub仓库：{owner}/{repo_name} 的拉取请求
当前工作目录为：{os.getcwd()}
</context>

<instructions>
- 使用GitHub MCP Server工具获取PR数据
- 使用文件和代码执行工具生成图表
- 将生成的图像保存到当前工作目录
- 响应要简洁
</instructions>
"""
        }
    ))

    done = asyncio.Event()

    # 设置事件处理
    def handle_event(event: SessionEvent):
        if event.type == SessionEventType.ASSISTANT_MESSAGE:
            print(f"\n🤖 {event.data.content}\n")
        elif event.type == SessionEventType.TOOL_EXECUTION_START:
            print(f"  ⚙️  {event.data.tool_name}")
        elif event.type.value == "session.idle":
            done.set()

    session.on(handle_event)

    # 初始提示 - 让Copilot自行处理细节
    print("\n📊 开始分析...\n")

    await session.send(MessageOptions(prompt=f"""
      从过去一周获取{owner}/{repo_name}的开放拉取请求
      计算每个PR的开放天数
      然后生成一个条形图，显示PR开放时间的分布情况
      （将它们分组到合理的区间，如<1天，1-3天等）。
      将图表保存为"pr-age-chart.png"到当前目录。
      最后，总结PR的健康状况 - 平均开放时间、最老的PR以及可能被视为过期的PR数量。
    """))

    await done.wait()

    # 交互式循环
    print("\n💡 可提出后续问题或输入\"exit\"退出。\n")
    print("示例：")
    print("  - \"扩展到过去一个月\"")
    print("  - \"显示五个最老的PR\"")
    print("  - \"生成饼图代替条形图\"")
    print("  - \"按作者而非开放时间分组\"")
    print()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("👋 再见!")
            break

        if user_input:
            done.clear()
            await session.send(MessageOptions(prompt=user_input))
            await done.wait()

    await session.destroy()
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## 工作原理

1. **仓库检测**：检查`--repo`标志 → git远程仓库 → 提示用户输入
2. **无需自定义工具**：完全依赖Copilot CLI内置功能：
   - **GitHub MCP Server** - 从GitHub获取PR数据
   - **文件工具** - 保存生成的图表图像
   - **代码执行** - 使用Python/matplotlib或其他方法生成图表
3. **交互式会话**：初始分析完成后，用户可以提出调整请求

## 为何采用此方法？

| 方面           | 自定义工具         | Copilot内置功能                  |
|----------------|--------------------|----------------------------------|
| 代码复杂度     | 高                 | **极简**                         |
| 维护           | 您需要维护         | **Copilot负责维护**              |
| 灵活性         | 固定逻辑           | **AI决定最佳方法**               |
| 图表类型       | 仅限您编写的类型    | **Copilot可生成的任何类型**      |
| 数据分组       | 固定的分组区间      | **智能分组**                     |

# 生成PR年龄图表

构建一个交互式命令行工具，利用Copilot内置功能可视化GitHub仓库中拉取请求（PR）的开放时间分布。

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

您希望了解某个仓库中拉取请求（PR）已开放的时间。该工具会检测当前的Git仓库或接受仓库作为输入，然后让Copilot通过GitHub MCP Server获取PR数据并生成图表图像。

## 先决条件

```bash
pip install copilot-sdk
```

## 使用方法

```bash
# 从当前git仓库自动检测
python pr_visualization.py

# 显式指定仓库
python pr_visualization.py --repo github/copilot-sdk
```

## 完整示例：pr_visualization.py

```python
#!/usr/bin/env python3

import subprocess
import sys
import os
from copilot import CopilotClient

# ============================================================================
# Git & GitHub 仓库检测
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
        import re
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
    return input("输入GitHub仓库（格式为owner/repo）: ").strip()

# ============================================================================
# 主程序
# ============================================================================

def main():
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
            print("⚠️  检测到Git仓库但未找到GitHub远程仓库。")
            repo = prompt_for_repo()
    else:
        print("📁 不在Git仓库中。")
        repo = prompt_for_repo()

    if not repo or "/" not in repo:
        print("❌ 仓库格式无效。预期格式：owner/repo")
        sys.exit(1)

    owner, repo_name = repo.split("/", 1)

    # 创建Copilot客户端 - 不需要自定义工具！
    client = CopilotClient(log_level="error")
    client.start()

    session = client.create_session(
        model="gpt-5",
        system_message={
            "content": f"""
<context>
您正在分析GitHub仓库：{owner}/{repo_name} 的拉取请求
当前工作目录是：{os.getcwd()}
</context>

<instructions>
- 使用GitHub MCP Server工具获取PR数据
- 使用您的文件和代码执行工具生成图表
- 将生成的图像保存到当前工作目录
- 保持响应简洁
</instructions>
"""
        }
    )

    # 设置事件处理
    def handle_event(event):
        if event["type"] == "assistant.message":
            print(f"\n🤖 {event['data']['content']}\n")
        elif event["type"] == "tool.execution_start":
            print(f"  ⚙️  {event['data']['toolName']}")

    session.on(handle_event)

    # 初始提示 - 让Copilot自行处理细节
    print("\n📊 开始分析...\n")

    session.send(prompt=f"""
      从过去一周获取{owner}/{repo_name}的开放拉取请求
      计算每个PR的开放天数
      然后生成一个柱状图，显示PR开放时间的分布
      （将它们分组到如<1天、1-3天等合理的桶中）
      将图表保存为"pr-age-chart.png"在当前目录
      最后，总结PR的健康状况 - 平均开放时间、最老的PR以及可能被视为过期的PR数量
    """)

    session.wait_for_idle()

    # 交互式循环
    print("\n💡 可以提出后续问题或输入 \"exit\" 退出。\n")
    print("示例:")
    print("  - \"扩展到过去一个月\"")
    print("  - \"显示五个最老的PR\"")
    print("  - \"生成饼状图\"")
    print("  - \"按作者而非开放时间分组\"")
    print()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("👋 再见!")
            break

        if user_input:
            session.send(prompt=user_input)
            session.wait_for_idle()

    session.destroy()
    client.stop()

if __name__ == "__main__":
    main()
```

## 工作原理

1. **仓库检测**：检查`--repo`标志 → Git远程仓库 → 提示用户输入
2. **无需自定义工具**：完全依赖Copilot CLI内置功能：
   - **GitHub MCP Server** - 从GitHub获取PR数据
   - **文件工具** - 保存生成的图表图像
   - **代码执行** - 使用Python/matplotlib或其他方法生成图表
3. **交互式会话**：初始分析完成后，用户可以提出调整请求

## 为什么采用这种方法？

| 方面            | 自定义工具       | Copilot内置功能                  |
|-----------------|------------------|----------------------------------|
| 代码复杂度      | 高               | **最小化**                       |
| 维护责任        | 您负责维护       | **由Copilot维护**                |
| 灵活性          | 固定逻辑         | **AI决定最佳方法**               |
| 图表类型        | 仅限您编写的类型 | **Copilot能生成的任何类型**       |
| 数据分组         | 硬编码桶         | **智能分组**                     |

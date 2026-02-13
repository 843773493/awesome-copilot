# 生成可访问性报告

构建一个CLI工具，使用Playwright MCP服务器分析网页可访问性，并生成符合WCAG标准的详细报告，可选生成测试用例。

> **可运行示例：** [recipe/accessibility_report.py](recipe/accessibility_report.py)
>
> ```bash
> cd recipe && pip install -r requirements.txt
> python accessibility_report.py
> ```

## 示例场景

您想要审核网站的可访问性合规性。此工具使用Playwright导航到指定URL，捕获可访问性快照，并生成涵盖地标、标题层级、焦点管理及触摸目标等WCAG标准的结构化报告。它还可以生成Playwright测试文件以自动化未来的可访问性检查。

## 先决条件

```bash
pip install github-copilot-sdk
```

您还需要安装npx（需已安装Node.js）以使用Playwright MCP服务器。

## 使用方法

```bash
python accessibility_report.py
# 输入要分析的URL
```

## 完整示例：accessibility_report.py

```python
#!/usr/bin/env python3

import asyncio
from copilot import (
    CopilotClient, SessionConfig, MessageOptions,
    SessionEvent, SessionEventType,
)

# ============================================================================
# 主应用程序
# ============================================================================

async def main():
    print("=== 可访问性报告生成器 ===\n")

    url = input("请输入要分析的URL: ").strip()

    if not url:
        print("未提供URL。退出。")
        return

    # 确保URL包含协议头
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(f"\n分析中: {url}")
    print("请稍候...\n")

    # 创建连接到Playwright MCP服务器的Copilot客户端
    client = CopilotClient()
    await client.start()

    session = await client.create_session(SessionConfig(
        model="claude-opus-4.6",
        streaming=True,
        mcp_servers={
            "playwright": {
                "type": "local",
                "command": "npx",
                "args": ["@playwright/mcp@latest"],
                "tools": ["*"],
            }
        },
    ))

    done = asyncio.Event()

    # 设置流式事件处理
    def handle_event(event: SessionEvent):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            print(event.data.delta_content or "", end="", flush=True)
        elif event.type.value == "session.idle":
            done.set()
        elif event.type.value == "session.error":
            print(f"\n错误: {event.data.message}")
            done.set()

    session.on(handle_event)

    prompt = f"""
    使用Playwright MCP服务器分析此网页的可访问性: {url}
    
    请执行以下步骤：
    1. 使用playwright-browser_navigate工具导航到URL
    2. 使用playwright-browser_snapshot工具捕获可访问性快照
    3. 分析快照并提供详细可访问性报告
    
    请使用表情符号指示器格式化报告：
    - 📊 可访问性报告标题
    - ✅ 优点（包含分类、状态、详情的表格）
    - ⚠️ 发现的问题（包含严重性、问题、WCAG准则、建议的表格）
    - 📋 统计摘要（链接、标题、可聚焦元素、地标）
    - ⚙️ 优先建议
    
    使用✅表示通过，🔴表示严重问题，🟡表示中等严重问题，❌表示缺失项。
    包含实际的页面分析结果。
    """

    await session.send(MessageOptions(prompt=prompt))
    await done.wait()

    print("\n\n=== 报告完成 ===\n")

    # 提示用户是否生成测试用例
    generate_tests = input(
        "是否要生成Playwright可访问性测试用例？(y/n): "
    ).strip().lower()

    if generate_tests in ("y", "yes"):
        done.clear()

        detect_language_prompt = """
        分析当前工作目录以检测主要编程语言。
        仅回复检测到的语言名称和简要说明。
        如果未检测到项目，请建议使用TypeScript作为默认语言。
        """

        print("\n检测项目语言...\n")
        await session.send(MessageOptions(prompt=detect_language_prompt))
        await done.wait()

        language = input(
            "\n\n确认测试用例语言（或输入其他语言）: "
        ).strip()
        if not language:
            language = "TypeScript"

        done.clear()

        test_generation_prompt = f"""
        基于您刚刚为{url}生成的可访问性报告，
        创建{language}语言的Playwright可访问性测试用例。
        
        包含以下测试项：lang属性、标题、标题层级、alt文本、
        地标、跳过导航、焦点指示器和触摸目标。
        使用Playwright的可访问性测试功能并添加有帮助的注释。
        输出完整的测试文件。
        """

        print("\n生成可访问性测试用例...\n")
        await session.send(MessageOptions(prompt=test_generation_prompt))
        await done.wait()

        print("\n\n=== 测试用例已生成 ===")

    await session.destroy()
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## 工作原理

1. **Playwright MCP服务器**：配置本地MCP服务器运行`@playwright/mcp`以提供浏览器自动化工具
2. **流式输出**：使用`streaming=True`和`ASSISTANT_MESSAGE_DELTA`事件实现逐token实时输出
3. **可访问性快照**：Playwright的`browser_snapshot`工具捕获页面的完整可访问性树
4. **结构化报告**：通过提示词引导模型生成符合WCAG标准的结构化报告，包含表情符号严重性指示器
5. **测试用例生成**：可选地检测项目语言并生成Playwright可访问性测试用例

## 关键概念

### MCP服务器配置

该示例配置了一个与会话并行运行的本地MCP服务器：

```python
session = await client.create_session(SessionConfig(
    mcp_servers={
        "playwright": {
            "type": "local",
            "command": "npx",
            "args": ["@playwright/mcp@latest"],
            "tools": ["*"],
        }
    },
))
```

这使模型能够访问Playwright浏览器工具，如`browser_navigate`、`browser_snapshot`和`browser_click`。

### 使用事件流

与`send_and_wait`不同，此示例使用流式处理实现实时输出：

```python
def handle_event(event: SessionEvent):
    if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
        print(event.data.delta_content or "", end="", flush=True)
    elif event.type.value == "session.idle":
        done.set()

session.on(handle_event)
```

## 示例交互

```
=== 可访问性报告生成器 ===

请输入要分析的URL: github.com

分析中: https://github.com
请稍候...

📊 可访问性报告: GitHub (github.com)

✅ 优点
| 分类 | 状态 | 详情 |
|------|------|-----|
| 语言 | ✅ 通过 | lang="en" 正确设置 |
| 页面标题 | ✅ 通过 | "GitHub" 可识别 |
| 标题层级 | ✅ 通过 | 正确的H1/H2结构 |
| 图像 | ✅ 通过 | 所有图像都有alt文本 |

⚠️ 发现的问题
| 严重性 | 问题 | WCAG准则 | 建议 |
|--------|------|----------|-----|
| 🟡 中等 | 部分链接缺少描述性文本 | 2.4.4 | 为仅图标链接添加aria-label |

📋 统计摘要
- 总链接数: 47
- 总标题数: 8 (1× H1, 层级正确)
- 可聚焦元素: 52
- 检测到的地标: banner ✅, 导航 ✅, 主要内容 ✅, 页脚 ✅

=== 报告完成 ===

是否要生成Playwright可访问性测试用例？(y/n): y

检测项目语言...
检测到TypeScript（发现package.json文件）

确认测试用例语言（或输入其他语言）: 

生成可访问性测试用例...
[生成的测试文件输出...]

=== 测试用例已生成 ===
```

---
name: chrome-devtools
description: '使用 Chrome DevTools MCP 进行专家级浏览器自动化、调试和性能分析。用于与网页交互、捕获截图、分析网络流量和性能分析。'
license: MIT
---

# Chrome DevTools 代理

## 概述

控制和检查正在运行的 Chrome 浏览器的专用技能。该技能利用 `chrome-devtools` MCP 服务器执行各种浏览器相关任务，从简单的导航到复杂的性能分析。

## 使用场景

使用此技能时：

- **浏览器自动化**：导航页面、点击元素、填写表单和处理对话框。
- **视觉检查**：获取网页或文本的截图。
- **调试**：检查控制台消息、在页面上下文中评估 JavaScript 以及分析网络请求。
- **性能分析**：记录并分析性能跟踪，以识别瓶颈和核心网页指标问题。
- **模拟**：调整视口大小或模拟网络/CPU 条件。

## 工具分类

### 1. 导航与页面管理

- `new_page`: 打开新标签页/页面。
- `navigate_page`: 跳转到特定 URL、重新加载或导航历史记录。
- `select_page`: 在打开的页面之间切换上下文。
- `list_pages`: 查看所有打开的页面及其 ID。
- `close_page`: 关闭特定页面。
- `wait_for`: 等待页面上出现特定文本。

### 2. 输入与交互

- `click`: 点击元素（使用快照中的 uid）。
- `fill` / `fill_form`: 在输入框中输入文本或一次性填写多个字段。
- `hover`: 将鼠标悬停在元素上。
- `press_key`: 发送键盘快捷键或特殊键（例如，“Enter”、“Control+C”）。
- `drag`: 拖动和放置元素。
- `handle_dialog`: 接受或关闭浏览器警报/提示框。
- `upload_file`: 通过文件输入上传文件。

### 3. 调试与检查

- `take_snapshot`: 获取文本形式的可访问性树快照（最适合识别元素）。
- `take_screenshot`: 捕获页面或特定元素的视觉表示。
- `list_console_messages` / `get_console_message`: 检查页面的控制台输出。
- `evaluate_script`: 在页面上下文中运行自定义 JavaScript。
- `list_network_requests` / `get_network_request`: 分析网络流量和请求详细信息。

### 4. 模拟与性能

- `resize_page`: 更改视口尺寸。
- `emulate`: 模拟网络/CPU 条件或地理位置。
- `performance_start_trace`: 开始记录性能分析。
- `performance_stop_trace`: 停止记录并保存跟踪。
- `performance_analyze_insight`: 从记录的性能数据中获取详细分析。

## 工作流模式

### 模式 A: 识别元素（先快照）

始终优先使用 `take_snapshot` 而不是 `take_screenshot` 来查找元素。快照提供 `uid` 值，这些值是交互工具所必需的。

```markdown
1. `take_snapshot` 以获取当前页面结构。
2. 查找目标元素的 `uid`。
3. 使用 `click(uid=...)` 或 `fill(uid=..., value=...)`。
```

### 模式 B: 排查错误

当页面出现故障时，检查控制台日志和网络请求。

```markdown
1. `list_console_messages` 以检查 JavaScript 错误。
2. `list_network_requests` 以识别失败的（4xx/5xx）资源。
3. `evaluate_script` 以检查特定 DOM 元素或全局变量的值。
```

### 模式 C: 性能分析

确定页面为何变慢。

```markdown
1. `performance_start_trace(reload=true, autoStop=true)`
2. 等待页面加载或跟踪完成。
3. `performance_analyze_insight` 以查找 LCP 问题或布局变化。
```

## 最佳实践

- **上下文感知**：如果不确定当前活动的标签页，始终运行 `list_pages` 和 `select_page`。
- **快照**：在任何主要导航或 DOM 变化后都应获取新快照，因为 `uid` 值可能会改变。
- **超时设置**：为 `wait_for` 使用合理的超时时间，以避免在加载缓慢的元素上挂起。
- **截图**：在视觉验证中偶尔使用 `take_screenshot`，但应依赖 `take_snapshot` 进行逻辑分析。

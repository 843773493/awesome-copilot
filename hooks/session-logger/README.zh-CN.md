---
名称: '会话记录器'
描述: '记录所有 Copilot 编码代理会话活动，用于审计和分析'
标签: ['日志记录', '审计', '分析']
---

# 会话记录器钩子

全面记录 GitHub Copilot 编码代理会话活动，追踪会话开始、结束及用户提示，用于审计追踪和使用分析。

## 概述

此钩子提供 Copilot 编码代理活动的详细日志记录：
- 会话开始/结束时间及工作目录上下文
- 用户提示提交事件
- 可配置的日志级别

## 功能特点

- **会话追踪**：记录会话开始和结束事件
- **提示记录**：记录用户提示的提交时间
- **结构化日志记录**：JSON 格式便于解析
- **隐私保护**：可配置完全禁用日志记录

## 安装步骤

1. 将此钩子文件夹复制到仓库的 `.github/hooks/` 目录：
   ```bash
   cp -r hooks/session-logger .github/hooks/
   ```

2. 创建日志目录：
   ```bash
   mkdir -p logs/copilot
   ```

3. 确保脚本具有可执行权限：
   ```bash
   chmod +x .github/hooks/session-logger/*.sh
   ```

4. 将钩子配置提交到仓库的默认分支

## 日志格式

会话事件写入 `logs/copilot/session.log`，提示事件写入 `logs/copilot/prompts.log`，采用 JSON 格式：

```json
{"时间戳":"2024-01-15T10:30:00Z","事件":"会话开始","cwd":"/workspace/project"}
{"时间戳":"2024-01-15T10:35:00Z","事件":"会话结束"}
```

## 隐私与安全

- 将 `logs/` 添加到 `.gitignore` 文件中，避免提交会话数据
- 使用 `LOG_LEVEL=ERROR` 仅记录错误
- 设置 `SKIP_LOGGING=true` 环境变量以禁用日志记录
- 日志仅本地存储

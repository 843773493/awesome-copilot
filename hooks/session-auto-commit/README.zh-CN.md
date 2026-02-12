---
name: '会话自动提交'
description: '当 Copilot 编码代理会话结束时自动提交并推送更改'
tags: ['自动化', 'Git', '生产力']
---

# 会话自动提交钩子

当 GitHub Copilot 编码代理会话结束时自动提交并推送更改，确保您的工作始终得到保存和备份。

## 概述

此钩子在每次 Copilot 编码代理会话结束时运行，并自动执行以下操作：
- 检测是否有未提交的更改
- 暂存所有更改
- 创建带时间戳的提交
- 推送至远程仓库

## 功能特点

- **自动备份**：不会丢失 Copilot 会话中的工作
- **带时间戳的提交**：每个自动提交都包含会话结束时间
- **安全执行**：仅在有实际更改时提交
- **错误处理**：优雅处理推送失败的情况

## 安装

1. 将此钩子文件夹复制到您的仓库的 `.github/hooks/` 目录中：
   ```bash
   cp -r hooks/session-auto-commit .github/hooks/
   ```

2. 确保脚本具有可执行权限：
   ```bash
   chmod +x .github/hooks/session-auto-commit/auto-commit.sh
   ```

3. 将钩子配置提交到您的仓库的默认分支

## 配置

钩子在 `hooks.json` 中配置，用于在 `sessionEnd` 事件时运行：

```json
{
  "version": 1,
  "hooks": {
    "sessionEnd": [
      {
        "type": "command",
        "bash": ".github/hooks/session-auto-commit/auto-commit.sh",
        "timeoutSec": 30
      }
    ]
  }
}
```

## 工作原理

1. 当 Copilot 编码代理会话结束时，钩子会执行
2. 检查是否处于 Git 仓库中
3. 使用 `git status` 检测未提交的更改
4. 通过 `git add -A` 暂存所有更改
5. 创建格式为 `auto-commit: YYYY-MM-DD HH:MM:SS` 的提交
6. 尝试将更改推送到远程仓库
7. 报告提交成功或失败的状态

## 自定义设置

您可以通过修改 `auto-commit.sh` 来自定义钩子：
- **提交信息格式**：更改时间戳格式或提交信息前缀
- **选择性暂存**：使用特定的 git add 模式代替 `-A`
- **分支选择**：仅推送至特定分支
- **通知功能**：添加桌面通知或 Slack 消息

## 禁用

要临时禁用自动提交：
1. 在 `hooks.json` 中删除或注释掉 `sessionEnd` 钩子
2. 或设置环境变量：`export SKIP_AUTO_COMMIT=true`

## 注意事项

- 该钩子使用 `--no-verify` 参数以避免触发预提交钩子
- 推送失败不会阻止会话终止
- 需要配置适当的 Git 凭据
- 适用于 Copilot 编码代理和 GitHub Copilot CLI 两种工具

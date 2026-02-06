# Clojure 交互式编程插件

用于 REPL-first Clojure 工作流的工具，包含 Clojure 指令、交互式编程聊天模式和支持性指导。

## 安装

```bash
# 使用 Copilot CLI
copilot plugin install clojure-interactive-programming@awesome-copilot
```

## 包含内容

### 命令（斜杠命令）

| 命令 | 描述 |
|------|------|
| `/clojure-interactive-programming:remember-interactive-programming` | 一个微提示，提醒代理其为交互式编程专家。在 Copilot 能够访问 REPL（可能通过 Backseat Driver）的 Clojure 环境中效果尤为显著。适用于任何具有可交互 REPL 的系统。根据您的工作流程和/或工作区中的任何特定提醒自定义提示。 |

### 代理

| 代理 | 描述 |
|------|------|
| `clojure-interactive-programming` | 以 REPL 为先的 Clojure 结对编程专家，具备架构监督和交互式问题解决能力。强制执行质量标准，防止变通方法，并在文件修改前通过实时 REPL 评估逐步开发解决方案。 |

## 源码

此插件是 [Awesome Copilot](https://github.com/github/awesome-copilot) 的一部分，这是一个由社区驱动的 GitHub Copilot 扩展集合。

## 许可证

MIT

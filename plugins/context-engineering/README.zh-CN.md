# 上下文工程插件

通过更有效的上下文管理来最大化 GitHub Copilot 的效果的工具和技术。包含代码结构指南、用于规划多文件更改的代理以及上下文感知开发的提示。

## 安装

```bash
# 使用 Copilot CLI
copilot plugin install context-engineering@awesome-copilot
```

## 包含内容

### 命令（斜杠命令）

| 命令 | 描述 |
|------|------|
| `/context-engineering:context-map` | 在进行更改前生成与任务相关的所有文件的地图 |
| `/context-engineering:what-context-needed` | 询问 Copilot 在回答问题前需要查看哪些文件 |
| `/context-engineering:refactor-plan` | 通过适当的顺序和回滚步骤规划多文件重构 |

### 代理

| 代理 | 描述 |
|------|------|
| `context-architect` | 一个通过识别相关上下文和依赖项来帮助计划和执行多文件更改的代理 |

## 来源

此插件是 [Awesome Copilot](https://github.com/github/awesome-copilot) 的一部分，这是一个由社区驱动的 GitHub Copilot 扩展集合。

## 许可证

MIT

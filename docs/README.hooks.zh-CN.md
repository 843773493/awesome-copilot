# 🪝 钩子

钩子功能允许在GitHub Copilot编码代理会话期间触发特定事件的自动化工作流，例如会话开始、会话结束、用户提示和工具使用。
### 如何使用钩子

**包含内容：**
- 每个钩子是一个包含`README.md`文件和`hooks.json`配置的文件夹
- 钩子可能包含辅助脚本、工具或其他捆绑资源
- 钩子遵循[GitHub Copilot钩子规范](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/use-hooks)

**安装步骤：**
- 将钩子文件夹复制到仓库的`.github/hooks/`目录中
- 确保任何捆绑的脚本可执行（`chmod +x script.sh`）
- 将钩子提交到仓库的默认分支

**激活/使用：**
- 钩子在Copilot编码代理会话期间会自动执行
- 在`hooks.json`文件中配置钩子事件
- 可用事件：`sessionStart`, `sessionEnd`, `userPromptSubmitted`, `preToolUse`, `postToolUse`, `errorOccurred`

| 名称 | 描述 | 事件 | 捆绑资源 |
| ---- | ----------- | ------ | -------------- |
| [会话自动提交](../hooks/session-auto-commit/README.md) | 在Copilot编码代理会话结束时自动提交并推送更改 | sessionEnd | `auto-commit.sh`<br />`hooks.json` |
| [会话记录器](../hooks/session-logger/README.md) | 记录所有Copilot编码代理会话活动，用于审计和分析 | sessionStart, sessionEnd, userPromptSubmitted | `hooks.json`<br />`log-prompt.sh`<br />`log-session-end.sh`<br />`log-session-start.sh` |

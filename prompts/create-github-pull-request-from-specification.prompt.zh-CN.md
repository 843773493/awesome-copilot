

---
agent: 'agent'
description: '根据 specification 文件创建 GitHub 拉取请求，使用 pull_request_template.md 模板。'
tools: ['search/codebase', 'search', 'github', 'create_pull_request', 'update_pull_request', 'get_pull_request_diff']
---
# 从规范创建 GitHub 拉取请求

根据位于 `${workspaceFolder}/.github/pull_request_template.md` 的规范文件创建 GitHub 拉取请求。

## 流程

1. 使用 'search' 工具分析来自 '${workspaceFolder}/.github/pull_request_template.md' 的规范文件模板，提取需求。
2. 使用 'create_pull_request' 工具在 `${input:targetBranch}` 上创建拉取请求草稿模板。通过 'get_pull_request' 工具确认当前分支是否已有拉取请求，若存在则跳过步骤3，直接进入步骤4。
3. 使用 'get_pull_request_diff' 工具获取拉取请求中的更改，以分析拉取请求中更改的信息。
4. 使用 'update_pull_request' 工具更新上一步骤中创建的拉取请求正文和标题。根据第一步获取的模板信息，按需更新正文和标题内容。
5. 使用 'update_pull_request' 工具将拉取请求从草稿状态切换为可审阅状态。以更新拉取请求的状态。
6. 使用 'get_me' 获取创建拉取请求的人员用户名，并分配给 'update_issue' 工具。以分配拉取请求
7. 响应用户，告知已创建的拉取请求的 URL。

## 要求
- 为完整规范创建单个拉取请求
- 使用清晰的标题/pull_request_template.md 标识规范
- 在 pull_request_template.md 中填写足够的信息
- 在创建之前验证与现有拉取请求的对比
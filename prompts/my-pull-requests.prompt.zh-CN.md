

---
agent: 'agent'  
tools: ['githubRepo', 'github', 'get_me', 'get_pull_request', 'get_pull_request_comments', 'get_pull_request_diff', 'get_pull_request_files', 'get_pull_request_reviews', 'get_pull_request_status', 'list_pull_requests', 'request_copilot_review']  
description: '列出当前仓库中分配给我的所有拉取请求'  
---

搜索当前仓库（使用 #githubRepo 获取仓库信息），并列出找到的所有拉取请求（使用 #list_pull_requests）。  

描述每个拉取请求的目的和详细信息。  

如果某个拉取请求正在等待他人审查，请在响应中突出显示。  

如果拉取请求上有任何检查失败，请描述这些失败并提出可能的修复方案。  

如果尚未由 Copilot 进行审查，请提供使用 #request_copilot_review 请求审查的选项。
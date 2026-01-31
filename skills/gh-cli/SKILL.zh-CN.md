---
name: gh-cli
description: GitHub CLI (gh) 的全面参考文档，涵盖仓库、问题、拉取请求、操作、项目、发布、代码片段、代码空间、组织、扩展以及所有 GitHub 操作的命令行工具。
---

# GitHub CLI (gh)

GitHub CLI (gh) 的全面参考文档 - 从命令行无缝操作 GitHub。

**版本:** 2.85.0（截至2026年1月的当前版本）

## 先决条件

### 安装

```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Windows
winget install --id GitHub.cli

# 验证安装
gh --version
```

### 认证

```bash
# 交互式登录（默认：github.com）
gh auth login

# 使用特定主机名登录
gh auth login --hostname enterprise.internal

# 使用令牌登录
gh auth login --with-token < mytoken.txt>

# 检查认证状态
gh auth status

# 切换账户
gh auth switch --hostname github.com --user username

# 登出
gh auth logout --hostname github.com --user username
```

### 设置 Git 集成

```bash
# 配置 git 以使用 gh 作为凭证助手
gh auth setup-git

# 查看当前令牌
gh auth token

# 刷新认证范围
gh auth refresh --scopes write:org,read:public_key
```

## CLI 结构

```
gh                          # 根命令
├── auth                    # 认证
│   ├── login
│   ├── logout
│   ├── refresh
│   ├── setup-git
│   ├── status
│   ├── switch
│   └── token
├── browse                  # 在浏览器中打开
├── codespace               # GitHub 代码空间
│   ├── code
│   ├── cp
│   ├── create
│   ├── delete
│   ├── edit
│   ├── jupyter
│   ├── list
│   ├── logs
│   ├── ports
│   ├── rebuild
│   ├── ssh
│   ├── stop
│   └── view
├── gist                    # 代码片段
│   ├── clone
│   ├── create
│   ├── delete
│   ├── edit
│   ├── list
│   ├── rename
│   └── view
├── issue                   # 问题
│   ├── create
│   ├── list
│   ├── status
│   ├── close
│   ├── comment
│   ├── delete
│   ├── develop
│   ├── edit
│   ├── lock
│   ├── pin
│   ├── reopen
│   ├── transfer
│   ├── unlock
│   └── view
├── org                     # 组织
│   └── list
├── pr                      # 拉取请求
│   ├── create
│   ├── list
│   ├── status
│   ├── checkout
│   ├── checks
│   ├── close
│   ├── comment
│   ├── diff
│   ├── edit
│   ├── lock
│   ├── merge
│   ├── ready
│   ├── reopen
│   ├── revert
│   ├── review
│   ├── unlock
│   ├── update-branch
│   └── view
├── project                 # 项目
│   ├── close
│   ├── copy
│   ├── create
│   ├── delete
│   ├── edit
│   ├── field-create
│   ├── field-delete
│   ├── field-list
│   ├── item-add
│   ├── item-archive
│   ├── item-create
│   ├── item-delete
│   ├── item-edit
│   ├── item-list
│   ├── link
│   ├── list
│   ├── mark-template
│   ├── unlink
│   └── view
├── release                 # 发布
│   ├── create
│   ├── list
│   ├── delete
│   ├── delete-asset
│   ├── download
│   ├── edit
│   ├── upload
│   ├── verify
│   ├── verify-asset
│   └── view
├── repo                    # 仓库
│   ├── create
│   ├── list
│   ├── archive
│   ├── autolink
│   ├── clone
│   ├── delete
│   ├── deploy-key
│   ├── edit
│   ├── fork
│   ├── gitignore
│   ├── license
│   ├── rename
│   ├── set-default
│   ├── sync
│   ├── unarchive
│   └── view
├── cache                   # 操作缓存
│   ├── delete
│   └── list
├── run                     # 工作流运行
│   ├── cancel
│   ├── delete
│   ├── download
│   ├── list
│   ├── rerun
│   ├── view
│   └── watch
├── workflow                # 工作流
│   ├── disable
│   ├── enable
│   ├── list
│   ├── run
│   └── view
├── agent-task              # 代理任务
├── alias                   # 命令别名
│   ├── delete
│   ├── import
│   ├── list
│   └── set
├── api                     # API 请求
├── attestation             # 艺术品证明
│   ├── download
│   ├── trusted-root
│   └── verify
├── completion              # Shell 补全
├── config                  # 配置
│   ├── clear-cache
│   ├── get
│   ├── list
│   └── set
├── extension               # 扩展
│   ├── browse
│   ├── create
│   ├── exec
│   ├── install
│   ├── list
│   ├── remove
│   ├── search
│   └── upgrade
├── gpg-key                 # GPG 密钥
│   ├── add
│   ├── delete
│   └── list
├── label                   # 标签
│   ├── clone
│   ├── create
│   ├── delete
│   ├── edit
│   └── list
├── preview                 # 预览功能
├── ruleset                 # 规则集
│   ├── check
│   ├── list
│   └── view
├── search                  # 搜索
│   ├── code
│   ├── commits
│   ├── issues
│   ├── prs
│   └── repos
├── secret                  # 机密
│   ├── delete
│   ├── list
│   └── set
├── ssh-key                 # SSH 密钥
│   ├── add
│   ├── delete
│   └── list
├── status                  # 状态概览
└── variable                # 变量
    ├── delete
    ├── get
    ├── list
    └── set
```

## 配置

### 全局配置

```bash
# 列出所有配置
gh config list

# 获取特定配置值
gh config list git_protocol
gh config get editor

# 设置配置值
gh config set editor vim
gh config set git_protocol ssh
gh config set prompt disabled
gh config set pager "less -R"

# 清除配置缓存
gh config clear-cache
```

### 环境变量

```bash
# GitHub 令牌（用于自动化）
export GH_TOKEN=ghp_xxxxxxxxxxxx

# GitHub 主机名
export GH_HOST=github.com

# 禁用提示
export GH_PROMPT_DISABLED=true

# 自定义编辑器
export GH_EDITOR=vim

# 自定义分页器
export GH_PAGER=less

# HTTP 超时
export GH_TIMEOUT=30

# 自定义仓库（覆盖默认）
export GH_REPO=owner/repo

# 自定义 Git 协议
export GH_ENTERPRISE_HOSTNAME=hostname
```

## 认证 (gh auth)

### 登录

```bash
# 交互式登录
gh auth login

# 基于网页的认证
gh auth login --web

# 使用剪贴板获取 OAuth 代码
gh auth login --web --clipboard

# 使用特定 Git 协议
gh auth login --git-protocol ssh

# 使用自定义主机名（GitHub 企业版）
gh auth login --hostname enterprise.internal

# 使用标准输入中的令牌登录
gh auth login --with-token < token.txt>

# 不安全存储（明文）
gh auth login --insecure-storage
```

### 状态

```bash
# 显示所有认证状态
gh auth status

# 仅显示当前账户
gh auth status --active

# 显示特定主机名
gh auth status --hostname github.com

# 显示令牌
gh auth status --show-token

# JSON 输出
gh auth status --json hosts

# 使用 jq 过滤
gh auth status --json hosts --jq '.hosts | add'
```

### 切换账户

```bash
# 交互式切换
gh auth switch

# 切换到特定用户/主机
gh auth switch --hostname github.com --user monalisa
```

### 令牌

```bash
# 打印认证令牌
gh auth token

# 特定主机名/用户的令牌
gh auth token --hostname github.com --user monalisa
```

### 刷新

```bash
# 刷新凭据
gh auth refresh

# 添加范围
gh auth refresh --scopes write:org,read:public_key

# 移除范围
gh auth refresh --remove-scopes delete_repo

# 重置为默认范围
gh auth refresh --reset-scopes

# 使用剪贴板
gh auth refresh --clipboard
```

### 设置 Git

```bash
# 设置 Git 凭证助手
gh auth setup-git

# 设置特定主机名的 Git 凭证助手
gh auth setup-git --hostname enterprise.internal

# 强制设置，即使主机名未知
gh auth setup-git --hostname enterprise.internal --force
```

## 浏览 (gh browse)

```bash
# 在浏览器中打开仓库
gh browse

# 打开特定路径
gh browse script/
gh browse main.go:312

# 打开问题或拉取请求
gh browse 123

# 打开提交
gh browse 77507cd94ccafcf568f8560cfecde965fcfa63

# 指定分支打开
gh browse main.go --branch bug-fix

# 打开不同仓库
gh browse --repo owner/repo

# 打开特定页面
gh browse --actions       # 操作标签
gh browse --projects      # 项目标签
gh browse --releases      # 发布标签
gh browse --settings      # 设置页面
gh browse --wiki          # 维基页面

# 打印 URL 而不打开浏览器
gh browse --no-browser
```

## 仓库 (gh repo)

### 创建仓库

```bash
# 创建新仓库
gh repo create my-repo

# 创建并添加描述
gh repo create my-repo --description "My awesome project"

# 创建公开仓库
gh repo create my-repo --public

# 创建私有仓库
gh repo create my-repo --private

# 创建并设置主页
gh repo create my-repo --homepage https://example.com

# 创建并添加许可证
gh repo create my-repo --license mit

# 创建并添加 gitignore 模板
gh repo create my-repo --gitignore python

# 初始化为模板仓库
gh repo create my-repo --template

# 创建组织下的仓库
gh repo create org/my-repo

# 创建但不本地克隆
gh repo create my-repo --source=.

# 禁用问题
gh repo create my-repo --disable-issues

# 禁用维基
gh repo create my-repo --disable-wiki
```

### 克隆仓库

```bash
# 克隆仓库
gh repo clone owner/repo

# 克隆到特定目录
gh repo clone owner/repo my-directory

# 克隆并使用不同分支
gh repo clone owner/repo --branch develop
```

### 列出仓库

```bash
# 列出所有仓库
gh repo list

# 列出特定所有者的仓库
gh repo list owner

# 限制结果数量
gh repo list --limit 50

# 仅列出公开仓库
gh repo list --public

# 仅列出源仓库（非 Fork）
gh repo list --source

# JSON 输出
gh repo list --json name,visibility,owner

# 表格输出
gh repo list --limit 100 | tail -n +2

# 使用 jq 过滤
gh repo list --json name --jq '.[].name'
```

### 查看仓库

```bash
# 查看仓库详情
gh repo view

# 查看特定仓库
gh repo view owner/repo

# JSON 输出
gh repo view --json name,description,defaultBranchRef

# 在浏览器中查看
gh repo view --web
```

### 编辑仓库

```bash
# 编辑描述
gh repo edit --description "New description"

# 设置主页
gh repo edit --homepage https://example.com

# 更改可见性
gh repo edit --visibility private
gh repo edit --visibility public

# 启用/禁用功能
gh repo edit --enable-issues
gh repo edit --disable-issues
gh repo edit --enable-wiki
gh repo edit --disable-wiki
gh repo edit --enable-projects
gh repo edit --disable-projects

# 设置默认分支
gh repo edit --default-branch main

# 重命名仓库
gh repo rename new-name

# 存档仓库
gh repo archive
gh repo unarchive
```

### 删除仓库

```bash
# 删除仓库
gh repo delete owner/repo

# 确认删除（不提示）
gh repo delete owner/repo --yes
```

### 分支同步

```bash
# 同步 Fork 到上游仓库
gh repo fork owner/repo --clone

# 设置上游远程
git remote add upstream https://github.com/original/repo.git

# 同步 Fork
gh repo sync

# 或手动同步
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 设置默认仓库

```bash
# 设置当前目录的默认仓库
gh repo set-default

# 显式设置默认仓库
gh repo set-default owner/repo

# 取消默认设置
gh repo set-default --unset
```

### 仓库自动链接

```bash
# 列出自动链接
gh repo autolink list

# 添加自动链接
gh repo autolink add \
  --key-prefix JIRA- \
  --url-template https://jira.example.com/browse/<num>

# 删除自动链接
gh repo autolink delete 12345
```

### 仓库部署密钥

```bash
# 列出部署密钥
gh repo deploy-key list

# 添加部署密钥
gh repo deploy-key add ~/.ssh/id_rsa.pub \
  --title "Production server" \
  --read-only

# 删除部署密钥
gh repo deploy-key delete 12345
```

### Gitignore 和许可证

```bash
# 查看 gitignore 模板
gh repo gitignore

# 查看许可证模板
gh repo license mit

# 使用完整名称设置许可证
gh repo license mit --fullname "John Doe"
```

## 问题 (gh issue)

### 创建问题

```bash
# 交互式创建问题
gh issue create

# 创建并指定标题
gh issue create --title "Bug: Login not working"

# 创建并指定标题和正文
gh issue create \
  --title "Bug: Login not working" \
  --body "Steps to reproduce..."

# 创建并从文件读取正文
gh issue create --body-file issue.md

# 创建并添加标签
gh issue create --title "Fix bug" --labels bug,high-priority

# 创建并指定负责人
gh issue create --title "Fix bug" --assignee user1,user2

# 创建并指定仓库
gh issue create --repo owner/repo --title "Issue title"

# 从网页创建问题
gh issue create --web
```

### 列出问题

```bash
# 列出所有开放问题
gh issue list

# 列出所有问题（包括已关闭）
gh issue list --state all

# 列出已关闭问题
gh issue list --state closed

# 限制结果数量
gh issue list --limit 50

# 按负责人过滤
gh issue list --assignee username
gh issue list --assignee @me

# 按标签过滤
gh issue list --labels bug,enhancement

# 按里程碑过滤
gh issue list --milestone "v1.0"

# 搜索/过滤
gh issue list --search "is:open is:issue label:bug"

# JSON 输出
gh issue list --json number,title,state,author

# 表格视图
gh issue list --json number,title,labels --jq '.[] | [.number, .title, .labels[].name] | @tsv'

# 显示评论数量
gh issue list --json number,title,comments --jq '.[] | [.number, .title, .comments]'

# 按创建时间排序
gh issue list --sort created --order desc
```

### 查看问题

```bash
# 查看问题详情
gh issue view 123

# 查看问题并显示评论
gh issue view 123 --comments

# 在浏览器中查看问题
gh issue view 123 --web

# JSON 输出
gh issue view 123 --json title,body,state,labels,comments

# 查看特定字段
gh issue view 123 --json title --jq '.title'
```

### 编辑问题

```bash
# 交互式编辑问题
gh issue edit 123

# 编辑标题
gh issue edit 123 --title "New title"

# 编辑正文
gh issue edit 123 --body "New description"

# 添加标签
gh issue edit 123 --add-label bug,high-priority

# 移除标签
gh issue edit 123 --remove-label stale

# 添加负责人
gh issue edit 123 --add-assignee user1,user2

# 移除负责人
gh issue edit 123 --remove-assignee user1

# 设置里程碑
gh issue edit 123 --milestone "v1.0"
```

### 关闭/重新打开问题

```bash
# 关闭问题
gh issue close 123

# 关闭问题并添加评论
gh issue close 123 --comment "Fixed in PR #456"

# 重新打开问题
gh issue reopen 123
```

### 评论问题

```bash
# 添加评论
gh issue comment 123 --body "This looks good!"

# 编辑评论
gh issue comment 123 --edit 456789 --body "Updated comment"

# 删除评论
gh issue comment 123 --delete 456789
```

### 问题状态

```bash
# 显示问题状态摘要
gh issue status

# 显示特定仓库的问题状态
gh issue status --repo owner/repo
```

### 固定/取消固定问题

```bash
# 固定问题（固定到仓库仪表盘）
gh issue pin 123

# 取消固定问题
gh issue unpin 123
```

### 锁定/解锁问题

```bash
# 锁定讨论
gh issue lock 123

# 锁定并指定原因
gh issue lock 123 --reason off-topic

# 解锁
gh issue unlock 123
```

### 转移问题

```bash
# 转移到另一个仓库
gh issue transfer 123 --repo owner/new-repo
```

### 删除问题

```bash
# 删除问题
gh issue delete 123

# 确认删除（不提示）
gh issue delete 123 --yes
```

### 开发问题（草稿 PR）

```bash
# 从问题创建草稿 PR
gh issue develop 123

# 从特定分支创建
gh issue develop 123 --branch fix/issue-123

# 指定基础分支创建
gh issue develop 123 --base main
```

## 拉取请求 (gh pr)

### 创建拉取请求

```bash
# 交互式创建 PR
gh pr create

# 创建并指定标题
gh pr create --title "Feature: Add new functionality"

# 创建并指定标题和正文
gh pr create \
  --title "Feature: Add new functionality" \
  --body "This PR adds..."

# 从模板文件填充正文
gh pr create --body-file .github/PULL_REQUEST_TEMPLATE.md

# 指定基础分支
gh pr create --base main

# 指定头分支（默认为当前分支）
gh pr create --head feature-branch

# 创建草稿 PR
gh pr create --draft

# 添加负责人
gh pr create --assignee user1,user2

# 添加评审者
gh pr create --reviewer user1,user2

# 添加标签
gh pr create --labels enhancement,feature

# 链接到问题
gh pr create --issue 123

# 在特定仓库中创建
gh pr create --repo owner/repo

# 创建后在浏览器中打开
gh pr create --web
```

### 列出拉取请求

```bash
# 列出所有开放的 PR
gh pr list

# 列出所有 PR（包括已合并）
gh pr list --state all

# 列出已合并的 PR
gh pr list --state merged

# 列出已关闭的 PR（未合并）
gh pr list --state closed

# 按头分支过滤
gh pr list --head feature-branch

# 按基础分支过滤
gh pr list --base main

# 按作者过滤
gh pr list --author username
gh pr list --author @me

# 按负责人过滤
gh pr list --assignee username

# 按标签过滤
gh pr list --labels bug,enhancement

# 按里程碑过滤
gh pr list --milestone "v1.0"

# 搜索/过滤
gh pr list --search "is:open is:pr label:review-required"

# JSON 输出
gh pr list --json number,title,state,author,headRefName

# 显示检查状态
gh pr list --json number,title,statusCheckRollup --jq '.[] | [.number, .title, .statusCheckRollup[]?.status]'

# 按创建时间排序
gh pr list --sort created --order desc
```

### 查看拉取请求

```bash
# 查看 PR
gh pr view 123

# 查看 PR 并显示评论
gh pr view 123 --comments

# 在浏览器中查看 PR
gh pr view 123 --web

# JSON 输出
gh pr view 123 --json title,body,state,author,commits,files

# 查看差异
gh pr view 123 --json files --jq '.files[].path'

# 使用 jq 查询
gh pr view 123 --json title,state --jq '"\(.title): \(.state)"'
```

### 检出拉取请求

```bash
# 检出 PR 分支
gh pr checkout 123

# 检出并指定分支名称
gh pr checkout 123 --branch name-123

# 强制检出
gh pr checkout 123 --force
```

### 查看拉取请求差异

```bash
# 查看 PR 差异
gh pr diff 123

# 查看差异并启用颜色
gh pr diff 123 --color always

# 输出到文件
gh pr diff 123 > pr-123.patch

# 查看特定文件的差异
gh pr diff 123 --name-only
```

### 合并拉取请求

```bash
# 合并 PR
gh pr merge 123

# 指定合并方式
gh pr merge 123 --merge
gh pr merge 123 --squash
gh pr merge 123 --rebase

# 合并后删除分支
gh pr merge 123 --delete-branch

# 合并并添加评论
gh pr merge 123 --subject "Merge PR #123" --body "Merging feature"

# 合并草稿 PR
gh pr merge 123 --admin

# 强制合并（跳过检查）
gh pr merge 123 --admin
```

### 关闭拉取请求

```bash
# 关闭 PR（不合并）
gh pr close 123

# 关闭并添加评论
gh pr close 123 --comment "Closing due to..."
```

### 重新打开拉取请求

```bash
# 重新打开已关闭的 PR
gh pr reopen 123
```

### 编辑拉取请求

```bash
# 交互式编辑
gh pr edit 123

# 编辑标题
gh pr edit 123 --title "New title"

# 编辑正文
gh pr edit 123 --body "New description"

# 添加标签
gh pr edit 123 --add-label bug,enhancement

# 移除标签
gh pr edit 123 --remove-label stale

# 添加负责人
gh pr edit 123 --add-assignee user1,user2

# 移除负责人
gh pr edit 123 --remove-assignee user1

# 添加评审者
gh pr edit 123 --add-reviewer user1,user2

# 移除评审者
gh pr edit 123 --remove-reviewer user1

# 标记为准备评审
gh pr edit 123 --ready
```

### 标记为准备评审

```bash
# 标记草稿 PR 为准备评审
gh pr ready 123
```

### 拉取请求检查

```bash
# 查看 PR 检查
gh pr checks 123

# 实时监控检查
gh pr checks 123 --watch

# 设置监控间隔（秒）
gh pr checks 123 --watch --interval 5
```

### 评论拉取请求

```bash
# 添加评论
gh pr comment 123 --body "Looks good!"

# 评论特定行
gh pr comment 123 --body "Fix this" \
  --repo owner/repo \
  --head-owner owner --head-branch feature

# 编辑评论
gh pr comment 123 --edit 456789 --body "Updated comment"

# 删除评论
gh pr comment 123 --delete 456789
```

### 评审拉取请求

```bash
# 评审 PR（打开编辑器）
gh pr review 123

# 批准 PR
gh pr review 123 --approve

--approve-body "LGTM!"

# 请求更改
gh pr review 123 --request-changes \
  --body "Please fix these issues"

# 评论 PR
gh pr review 123 --comment --body "Some thoughts..."

# 取消评审
gh pr review 123 --dismiss
```

### 更新分支

```bash
# 使用最新基础分支更新 PR 分支
gh pr update-branch 123

# 强制更新
gh pr update-branch 123 --force

# 使用合并策略
gh pr update-branch 123 --merge
```

### 锁定/解锁拉取请求

```bash
# 锁定 PR 讨论
gh pr lock 123

# 锁定并指定原因
gh pr lock 123 --reason off-topic

# 解锁
gh pr unlock 123
```

### 回滚拉取请求

```bash
# 回滚已合并的 PR
gh pr revert 123

# 回滚并指定分支名称
gh pr revert 123 --branch revert-pr-123
```

### 拉取请求状态

```bash
# 显示 PR 状态摘要
gh pr status

# 显示特定仓库的 PR 状态
gh pr status --repo owner/repo
```

## GitHub 操作

### 工作流运行 (gh run)

```bash
# 列出工作流运行
gh run list

# 列出特定工作流的运行
gh run list --workflow "ci.yml"

# 列出特定分支的运行
gh run list --branch main

# 限制结果数量
gh run list --limit 20

# JSON 输出
gh run list --json databaseId,status,conclusion,headBranch

# 查看运行详情
gh run view 123456789

# 查看运行并显示详细日志
gh run view 123456789 --log

# 查看特定任务
gh run view 123456789 --job 987654321

# 在浏览器中查看运行
gh run view 123456789 --web

# 实时监控运行
gh run watch 123456789

# 设置监控间隔
gh run watch 123456789 --interval 5

# 重新运行失败的运行
gh run rerun 123456789

# 重新运行特定任务
gh run rerun 123456789 --job 987654321

# 取消运行
gh run cancel 123456789

# 删除运行
gh run delete 123456789

# 下载运行附件
gh run download 123456789

# 下载特定附件
gh run download 123456789 --name build

# 下载到目录
gh run download 123456789 --dir ./artifacts
```

### 工作流 (gh workflow)

```bash
# 列出工作流
gh workflow list

# 查看工作流详情
gh workflow view ci.yml

# 查看工作流 YAML
gh workflow view ci.yml --yaml

# 在浏览器中查看工作流
gh workflow view ci.yml --web

# 启用工作流
gh workflow enable ci.yml

# 禁用工作流
gh workflow disable ci.yml

# 手动运行工作流
gh workflow run ci.yml

# 运行工作流并指定输入
gh workflow run ci.yml \
  --raw-field \
  version="1.0.0" \
  environment="production"

# 从特定分支运行工作流
gh workflow run ci.yml --ref develop
```

### 操作缓存 (gh cache)

```bash
# 列出缓存
gh cache list

# 列出特定分支的缓存
gh cache list --branch main

# 列出并限制数量
gh cache list --limit 50

# 删除缓存
gh cache delete 123456789

# 删除所有缓存
gh cache delete --all
```

### 操作机密 (gh secret)

```bash
# 列出机密
gh secret list

# 设置机密（提示输入值）
gh secret set MY_SECRET

# 从环境变量设置机密
echo "$MY_SECRET" | gh secret set MY_SECRET

# 为特定环境设置机密
gh secret set MY_SECRET --env production

# 为组织设置机密
gh secret set MY_SECRET --org orgname

# 删除机密
gh secret delete MY_SECRET

# 删除特定环境的机密
gh secret delete MY_SECRET --env production
```

### 操作变量 (gh variable)

```bash
# 列出变量
gh variable list

# 设置变量
gh variable set MY_VAR "some-value"

# 为特定环境设置变量
gh variable set MY_VAR "value" --env production

# 为组织设置变量
gh variable set MY_VAR "value" --org orgname

# 获取变量值
gh variable get MY_VAR

# 删除变量
gh variable delete MY_VAR

# 删除特定环境的变量
gh variable delete MY_VAR --env production
```

## 项目 (gh project)

```bash
# 列出项目
gh project list

# 列出特定所有者的项目
gh project list --owner owner

# 打开项目
gh project list --open

# 查看项目
gh project view 123

# 查看项目条目
gh project view 123 --format json

# 创建项目
gh project create --title "My Project"

# 在组织中创建项目
gh project create --title "Project" --org orgname

# 创建并添加 README
gh project create --title "Project" --readme "Description here"

# 编辑项目
gh project edit 123 --title "New Title"

# 删除项目
gh project delete 123

# 关闭项目
gh project close 123

# 复制项目
gh project copy 123 --owner target-owner --title "Copy"

# 标记为模板
gh project mark-template 123

# 列出字段
gh project field-list 123

# 创建字段
gh project field-create 123 --title "Status" --datatype single_select

# 删除字段
gh project field-delete 123 --id 456

# 列出条目
gh project item-list 123

# 创建条目
gh project item-create 123 --title "New item"

# 将条目添加到项目
gh project item-add 123 --owner-owner --repo repo --issue 456

# 编辑条目
gh project item-edit 123 --id 456 --title "Updated title"

# 删除条目
gh project item-delete 123 --id 456

# 存档条目
gh project item-archive 123 --id 456

# 链接条目
gh project link 123 --id 456 --link-id 789

# 解除链接
gh project unlink 123 --id 456 --link-id 789

# 在浏览器中查看项目
gh project view 123 --web
```

## 发布 (gh release)

```bash
# 列出发布
gh release list

# 查看最新发布
gh release view

# 查看特定发布
gh release view v1.0.0

# 在浏览器中查看发布
gh release view v1.0.0 --web

# 创建发布
gh release create v1.0.0 \
  --notes "Release notes here"

# 创建并从文件读取发布说明
gh release create v1.0.0 --notes-file notes.md

# 创建并指定目标分支
gh release create v1.0.0 --target main

# 创建草稿发布
gh release create v1.0.0 --draft

# 创建预发布
gh release create v1.0.0 --prerelease

# 创建并指定标题
gh release create v1.0.0 --title "Version 1.0.0"

# 上传附件到发布
gh release upload v1.0.0 ./file.tar.gz

# 上传多个附件
gh release upload v1.0.0 ./file1.tar.gz ./file2.tar.gz

# 上传并指定标签（区分大小写）
gh release upload v1.0.0 ./file.tar.gz --casing

# 删除发布
gh release delete v1.0.0

# 删除并清理标签
gh release delete v1.0.0 --yes

# 删除特定附件
gh release delete-asset v1.0.0 file.tar.gz

# 下载发布附件
gh release download v1.0.0

# 下载特定附件
gh release download v1.0.0 --pattern "*.tar.gz"

# 下载到指定目录
gh release download v1.0.0 --dir

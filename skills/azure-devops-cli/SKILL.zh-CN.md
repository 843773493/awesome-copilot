---
name: azure-devops-cli
description: 通过命令行界面管理 Azure DevOps 资源，包括项目、仓库、流水线、构建、拉取请求、工作项、制品和服务端点。在使用 Azure DevOps、az 命令、DevOps 自动化、CI/CD 或用户提及 Azure DevOps CLI 时使用。
---

# Azure DevOps 命令行界面

此技能通过 Azure CLI 的 Azure DevOps 扩展帮助管理 Azure DevOps 资源。

**CLI 版本:** 2.81.0（截至 2025 年当前版本）

## 先决条件

安装 Azure CLI 和 Azure DevOps 扩展：

```bash
# 安装 Azure CLI
brew install azure-cli  # macOS
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash  # Linux
pip install azure-cli  # 通过 pip 安装

# 验证安装
az --version

# 安装 Azure DevOps 扩展
az extension add --name azure-devops
az extension show --name azure-devops
```

## CLI 结构

```
az devops          # 主要的 DevOps 命令
├── admin          # 管理（横幅）
├── extension      # 扩展管理
├── project        # 团队项目
├── security       # 安全操作
│   ├── group      # 安全组
│   └── permission # 安全权限
├── service-endpoint # 服务连接
├── team           # 团队
├── user           # 用户
├── wiki           # 维基
├── configure      # 设置默认值
├── invoke         # 调用 REST API
├── login          # 认证
└── logout         # 清除凭据

az pipelines       # Azure 流水线
├── agent          # 代理
├── build          # 构建
├── folder         # 流水线文件夹
├── pool           # 代理池
├── queue          # 代理队列
├── release        # 发布
├── runs           # 流水线运行
├── variable       # 流水线变量
└── variable-group # 变量组

az boards          # Azure 项目看板
├── area           # 区域路径
├── iteration      # 迭代
└── work-item      # 工作项

az repos           # Azure 仓库
├── import         # Git 导入
├── policy         # 分支策略
├── pr             # 拉取请求
└── ref            # Git 引用

az artifacts       # Azure 制品
└── universal      # 通用制品
    ├── download   # 下载制品
    └── publish    # 发布制品
```

## 认证

### 登录 Azure DevOps

```bash
# 交互式登录（提示 PAT）
az devops login --organization https://dev.azure.com/{org}

# 使用 PAT 令牌登录
az devops login --organization https://dev.azure.com/{org} --token YOUR_PAT_TOKEN

# 登出
az devops logout --organization https://dev.azure.com/{org}
```

### 设置默认值

```bash
# 设置默认组织和项目
az devops configure --defaults organization=https://dev.azure.com/{org} project={project}

# 列出当前配置
az devops configure --list

# 启用 Git 别名
az devops configure --use-git-aliases true
```

## 扩展管理

### 列出扩展

```bash
# 列出可用扩展
az extension list-available --output table

# 列出已安装的扩展
az extension list --output table
```

### 管理 Azure DevOps 扩展

```bash
# 安装 Azure DevOps 扩展
az extension add --name azure-devops

# 更新 Azure DevOps 扩展
az extension update --name azure-devops

# 移除扩展
az extension remove --name azure-devops

# 从本地路径安装
az extension add --source ~/extensions/azure-devops.whl
```

## 项目

### 列出项目

```bash
az devops project list --organization https://dev.azure.com/{org}
az devops project list --top 10 --output table
```

### 创建项目

```bash
az devops project create \
  --name myNewProject \
  --organization https://dev.azure.com/{org} \
  --description "My new DevOps 项目" \
  --source-control git \
  --visibility private
```

### 显示项目详细信息

```bash
az devops project show --project {project-name} --org https://dev.azure.com/{org}
```

### 删除项目

```bash
az devops project delete --id {project-id} --org https://dev.azure.com/{org} --yes
```

## 仓库

### 列出仓库

```bash
az repos list --org https://dev.azure.com/{org} --project {project}
az repos list --output table
```

### 显示仓库详细信息

```bash
az repos show --repository {repo-name} --project {project}
```

### 创建仓库

```bash
az repos create --name {repo-name} --project {project}
```

### 删除仓库

```bash
az repos delete --id {repo-id} --project {project} --yes
```

### 更新仓库

```bash
az repos update --id {repo-id} --name {new-name} --project {project}
```

## 仓库导入

### 导入 Git 仓库

```bash
# 从公共 Git 仓库导入
az repos import create \
  --git-source-url https://github.com/user/repo \
  --repository {repo-name}

# 带认证的导入
az repos import create \
  --git-source-url https://github.com/user/private-repo \
  --repository {repo-name} \
  --user {username} \
  --password {password-or-pat}
```

## 拉取请求

### 创建拉取请求

```bash
# 基本的 PR 创建
az repos pr create \
  --repository {repo} \
  --source-branch {source-branch} \
  --target-branch {target-branch} \
  --title "PR 标题" \
  --description "PR 描述" \
  --open

# 带工作项的 PR
az repos pr create \
  --repository {repo} \
  --source-branch {source-branch} \
  --work-items 63 64

# 带审阅者的草稿 PR
az repos pr create \
  --repository {repo} \
  --source-branch feature/new-feature \
  --target-branch main \
  --title "功能：新功能" \
  --draft true \
  --reviewers user1@example.com user2@example.com \
  --required-reviewers lead@example.com \
  --labels "enhancement" "backlog"
```

### 列出拉取请求

```bash
# 所有 PR
az repos pr list --repository {repo}

# 按状态过滤
az repos pr list --repository {repo} --status active

# 按创建者过滤
az repos pr list --repository {repo} --creator {email}

# 输出为表格
az repos pr list --repository {repo} --output table
```

### 显示 PR 详细信息

```bash
az repos pr show --id {pr-id}
az repos pr show --id {pr-id} --open  # 在浏览器中打开
```

### 更新 PR（完成/放弃/草稿）

```bash
# 完成 PR
az repos pr update --id {pr-id} --status completed

# 放弃 PR
az repos pr update --id {pr-id} --status abandoned

# 设置为草稿
az repos pr update --id {pr-id} --draft true

# 发布草稿 PR
az repos pr update --id {pr-id} --draft false

# 策略通过后自动完成
az repos pr update --id {pr-id} --auto-complete true

# 设置标题和描述
az repos pr update --id {pr-id} --title "新标题" --description "新描述"
```

### 在本地检出 PR

```bash
# 检出 PR 分支
az repos pr checkout --id {pr-id}

# 检出并指定特定远程仓库
az repos pr checkout --id {pr-id} --remote-name upstream
```

### 对 PR 投票

```bash
az repos pr set-vote --id {pr-id} --vote approve
az repos pr set-vote --id {pr-id} --vote approve-with-suggestions
az repos pr set-vote --id {pr-id} --vote reject
az repos pr set-vote --id {pr-id} --vote wait-for-author
az repos pr set-vote --id {pr-id} --vote reset
```

### PR 审阅者

```bash
# 添加审阅者
az repos pr reviewer add --id {pr-id} --reviewers user1@example.com user2@example.com

# 列出审阅者
az repos pr reviewer list --id {pr-id}

# 移除审阅者
az repos pr reviewer remove --id {pr-id} --reviewers user1@example.com
```

### PR 工作项

```bash
# 将工作项添加到 PR
az repos pr work-item add --id {pr-id} --work-items {id1} {id2}

# 列出 PR 工作项
az repos pr work-item list --id {pr-id}

# 从 PR 中移除工作项
az repos pr work-item remove --id {pr-id} --work-items {id1}
```

### PR 策略

```bash
# 列出 PR 的策略
az repos pr policy list --id {pr-id}

# 为 PR 排队策略评估
az repos pr policy queue --id {pr-id} --evaluation-id {evaluation-id}
```

## 流水线

### 列出流水线

```bash
az pipelines list --output table
az pipelines list --query "[?name=='myPipeline']"
az pipelines list --folder-path 'folder/subfolder'
```

### 创建流水线

```bash
# 从本地仓库上下文创建（自动检测设置）
az pipelines create --name 'ContosoBuild' --description 'Contoso 项目流水线'

# 指定分支和 YAML 路径
az pipelines create \
  --name {pipeline-name} \
  --repository {repo} \
  --branch main \
  --yaml-path azure-pipelines.yml \
  --description "我的 CI/CD 流水线"

# GitHub 仓库
az pipelines create \
  --name 'GitHubPipeline' \
  --repository https://github.com/Org/Repo \
  --branch main \
  --repository-type github

# 跳过首次运行
az pipelines create --name 'MyPipeline' --skip-run true
```

### 显示流水线

```bash
az pipelines show --id {pipeline-id}
az pipelines show --name {pipeline-name}
```

### 更新流水线

```bash
az pipelines update --id {pipeline-id} --name "新名称" --description "更新描述"
```

### 删除流水线

```bash
az pipelines delete --id {pipeline-id} --yes
```

### 运行流水线

```bash
# 通过名称运行
az pipelines run --name {pipeline-name} --branch main

# 通过 ID 运行
az pipelines run --id {pipeline-id} --branch refs/heads/main

# 带参数运行
az pipelines run --name {pipeline-name} --parameters version=1.0.0 environment=prod

# 带变量运行
az pipelines run --name {pipeline-name} --variables buildId=123 configuration=release

# 在浏览器中打开结果
az pipelines run --name {pipeline-name} --open
```

## 流水线运行

### 列出运行

```bash
az pipelines runs list --pipeline {pipeline-id}
az pipelines runs list --name {pipeline-name} --top 10
az pipelines runs list --branch main --status completed
```

### 显示运行详细信息

```bash
az pipelines runs show --run-id {run-id}
az pipelines runs show --run-id {run-id} --open
```

### 流水线制品

```bash
# 列出运行的制品
az pipelines runs artifact list --run-id {run-id}

# 下载制品
az pipelines runs artifact download \
  --artifact-name '{artifact-name}' \
  --path {local-path} \
  --run-id {run-id}

# 上传制品
az pipelines runs artifact upload \
  --artifact-name '{artifact-name}' \
  --path {local-path} \
  --run-id {run-id}
```

### 流水线运行标签

```bash
# 为运行添加标签
az pipelines runs tag add --run-id {run-id} --tags production v1.0

# 列出运行标签
az pipelines runs tag list --run-id {run-id} --output table
```

## 构建

### 列出构建

```bash
az pipelines build list
az pipelines build list --definition {build-definition-id}
az pipelines build list --status completed --result succeeded
```

### 排队构建

```bash
az pipelines build queue --definition {build-definition-id} --branch main
az pipelines build queue --definition {build-definition-id} --parameters version=1.0.0
```

### 显示构建详细信息

```bash
az pipelines build show --id {build-id}
```

### 取消构建

```bash
az pipelines build cancel --id {build-id}
```

### 构建标签

```bash
# 为构建添加标签
az pipelines build tag add --build-id {build-id} --tags prod release

# 从构建中删除标签
az pipelines build tag delete --build-id {build-id} --tag prod
```

## 构建定义

### 列出构建定义

```bash
az pipelines build definition list
az pipelines build definition list --name {definition-name}
```

### 显示构建定义

```bash
az pipelines build definition show --id {definition-id}
```

## 发布

### 列出发布

```bash
az pipelines release list
az pipelines release list --definition {release-definition-id}
```

### 创建发布

```bash
az pipelines release create --definition {release-definition-id}
az pipelines release create --definition {release-definition-id} --description "发布 v1.0"
```

### 显示发布

```bash
az pipelines release show --id {release-id}
```

## 发布定义

### 列出发布定义

```bash
az pipelines release definition list
```

### 显示发布定义

```bash
az pipelines release definition show --id {definition-id}
```

## 流水线变量

### 列出变量

```bash
az pipelines variable list --pipeline-id {pipeline-id}
```

### 创建变量

```bash
# 非机密变量
az pipelines variable create \
  --name {var-name} \
  --value {var-value} \
  --pipeline-id {pipeline-id}

# 机密变量
az pipelines variable create \
  --name {var-name} \
  --secret true \
  --pipeline-id {pipeline-id}

# 机密变量并提示输入
az pipelines variable create \
  --name {var-name} \
  --secret true \
  --prompt true \
  --pipeline-id {pipeline-id}
```

### 更新变量

```bash
az pipelines variable update \
  --name {var-name} \
  --value {new-value} \
  --pipeline-id {pipeline-id}

# 更新机密变量
az pipelines variable update \
  --name {var-name} \
  --secret true \
  --value "{new-secret-value}" \
  --pipeline-id {pipeline-id}
```

### 删除变量

```bash
az pipelines variable delete --name {var-name} --pipeline-id {pipeline-id} --yes
```

## 变量组

### 列出变量组

```bash
az pipelines variable-group list
az pipelines variable-group list --output table
```

### 显示变量组

```bash
az pipelines variable-group show --id {group-id}
```

### 创建变量组

```bash
az pipelines variable-group create \
  --name {group-name} \
  --variables key1=value1 key2=value2 \
  --authorize true
```

### 更新变量组

```bash
az pipelines variable-group update \
  --id {group-id} \
  --name {new-name} \
  --description "更新描述"
```

### 删除变量组

```bash
az pipelines variable-group delete --id {group-id} --yes
```

### 变量组变量

#### 列出变量

```bash
az pipelines variable-group variable list --group-id {group-id}
```

#### 创建变量

```bash
# 非机密变量
az pipelines variable-group variable create \
  --group-id {group-id} \
  --name {var-name} \
  --value {var-value}

# 机密变量（若未提供值则会提示输入）
az pipelines variable-group variable create \
  --group-id {group-id} \
  --name {var-name} \
  --secret true

# 机密变量并使用环境变量
export AZURE_DEVOPS_EXT_PIPELINE_VAR_MySecret=secretvalue
az pipelines variable-group variable create \
  --group-id {group-id} \
  --name MySecret \
  --secret true
```

#### 更新变量

```bash
az pipelines variable-group variable update \
  --group-id {group-id} \
  --name {var-name} \
  --value {new-value} \
  --secret false
```

#### 删除变量

```bash
az pipelines variable-group variable delete \
  --group-id {group-id} \
  --name {var-name}
```

## 流水线文件夹

### 列出文件夹

```bash
az pipelines folder list
```

### 创建文件夹

```bash
az pipelines folder create --path 'folder/subfolder' --description "我的文件夹"
```

### 删除文件夹

```bash
az pipelines folder delete --path 'folder/subfolder'
```

### 更新文件夹

```bash
az pipelines folder update --path 'old-folder' --new-path 'new-folder'
```

## 代理池

### 列出代理池

```bash
az pipelines pool list
az pipelines pool list --pool-type automation
az pipelines pool list --pool-type deployment
```

### 显示代理池

```bash
az pipelines pool show --pool-id {pool-id}
```

## 代理队列

### 列出代理队列

```bash
az pipelines queue list
az pipelines queue list --pool-name {pool-name}
```

### 显示代理队列

```bash
az pipelines queue show --id {queue-id}
```

## 工作项（看板）

### 查询工作项

```bash
# WIQL 查询
az boards query \
  --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] = 'Active'"

# 带输出格式的查询
az boards query --wiql "SELECT * FROM WorkItems" --output table
```

### 显示工作项

```bash
az boards work-item show --id {work-item-id}
az boards work-item show --id {work-item-id} --open
```

### 创建工作项

```bash
# 基本工作项
az boards work-item create \
  --title "修复登录错误" \
  --type Bug \
  --assigned-to user@example.com \
  --description "用户无法通过 SSO 登录"

# 带区域和迭代
az boards work-item create \
  --title "新功能" \
  --type "用户故事" \
  --area "Project\\Area1" \
  --iteration "Project\\Sprint 1"

# 带自定义字段
az boards work-item create \
  --title "任务" \
  --type Task \
  --fields "Priority=1" "Severity=2"

# 带讨论评论
az boards work-item create \
  --title "问题" \
  --type Bug \
  --discussion "初步调查已完成"

# 创建后在浏览器中打开
az boards work-item create --title "错误" --type Bug --open
```

### 更新工作项

```bash
# 更新状态、标题和分配者
az boards work-item update \
  --id {work-item-id} \
  --state "Active" \
  --title "更新标题" \
  --assigned-to user@example.com

# 移动到不同区域
az boards work-item update \
  --id {work-item-id} \
  --area "{ProjectName}\\{Team}\\{Area}"

# 更改迭代
az boards work-item update \
  --id {work-item-id} \
  --iteration "{ProjectName}\\Sprint 5"

# 添加评论/讨论
az boards work-item update \
  --id {work-item-id} \
  --discussion "进行中"

# 带自定义字段更新
az boards work-item update \
  --id {work-item-id} \
  --fields "Priority=1" "StoryPoints=5"
```

### 删除工作项

```bash
# 软删除（可恢复）
az boards work-item delete --id {work-item-id} --yes

# 永久删除
az boards work-item delete --id {work-item-id} --destroy --yes
```

### 工作项关系

```bash
# 列出关系
az boards work-item relation list --id {work-item-id}

# 列出支持的关系类型
az boards work-item relation list-type

# 添加关系
az boards work-item relation add --id {work-item-id} --relation-type parent --target-id {parent-id}

# 移除关系
az boards work-item relation remove --id {work-item-id} --relation-id {relation-id}
```

## 区域路径

### 列出项目中的区域

```bash
az boards area project list --project {project}
az boards area project show --path "Project\\Area1" --project {project}
```

### 创建区域

```bash
az boards area project create --path "Project\\NewArea" --project {project}
```

### 更新区域

```bash
az boards area project update \
  --path "Project\\OldArea" \
  --new-path "Project\\UpdatedArea" \
  --project {project}
```

### 删除区域

```bash
az boards area project delete --path "Project\\AreaToDelete" --project {project} --yes
```

### 区域团队管理

```bash
# 列出团队中的区域
az boards area team list --team {team-name} --project {project}

# 将区域添加到团队
az boards area team add \
  --team {team-name} \
  --path "Project\\NewArea" \
  --project {project}

# 从团队中移除区域
az boards area team remove \
  --team {team-name} \
  --path "Project\\AreaToRemove" \
  --project {project}

# 更新团队区域
az boards area team update \
  --team {team-name} \
  --path "Project\\Area" \
  --project {project} \
  --include-sub-areas true
```

## 迭代

### 列出项目中的迭代

```bash
az boards iteration project list --project {project}
az boards iteration project show --path "Project\\Sprint 1" --project {project}
```

### 创建迭代

```bash
az boards iteration project create --path "Project\\Sprint 1" --project {project}
```

### 更新迭代

```bash
az boards iteration project update \
  --path "Project\\OldSprint" \
  --new-path "Project\\NewSprint" \
  --project {project}
```

### 删除迭代

```bash
az boards iteration project delete --path "Project\\OldSprint" --project {project} --yes
```

### 列出团队中的迭代

```bash
az boards iteration team list --team {team-name} --project {project}
```

### 将迭代添加到团队

```bash
az boards iteration team add \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}
```

### 从团队中移除迭代

```bash
az boards iteration team remove \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}
```

### 列出迭代中的工作项

```bash
az boards iteration team list-work-items \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}
```

### 设置团队的默认迭代

```bash
az boards iteration team set-default-iteration \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}
```

### 显示默认迭代

```bash
az boards iteration team show-default-iteration \
  --team {team-name} \
  --project {project}
```

### 设置团队的待办事项迭代

```bash
az boards iteration team set-backlog-iteration \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}
```

### 显示待办事项迭代

```bash
az boards iteration team show-backlog-iteration \
  --team {team-name} \
  --project {project}
```

### 显示当前迭代

```bash
az boards iteration team show --team {team-name} --project {project} --timeframe current
```

## Git 引用

### 列出引用（分支）

```bash
az repos ref list --repository {repo}
az repos ref list --repository {repo} --query "[?name=='refs/heads/main']"
```

### 创建引用（分支）

```bash
az repos ref create --name refs/heads/new-branch --object-type commit --object {commit-sha}
```

### 删除引用（分支）

```bash
az repos ref delete --name refs/heads/old-branch --repository {repo} --project {project}
```

### 锁定分支

```bash
az repos ref lock --name refs/heads/main --repository {repo} --project {project}
```

### 解锁分支

```bash
az repos ref unlock --name refs/heads/main --repository {repo} --project {project}
```

## 仓库策略

### 列出所有策略

```bash
az repos policy list --repository {repo-id} --branch main
```

### 使用配置文件创建策略

```bash
az repos policy create --config policy.json
```

### 更新/删除策略

```bash
# 更新
az repos policy update --id {policy-id} --config updated-policy.json

# 删除
az repos policy delete --id {policy-id} --yes
```

### 策略类型

#### 审批人数策略

```bash
az repos policy approver-count create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --minimum-approver-count 2 \
  --creator-vote-counts true
```

#### 构建策略

```bash
az repos policy build create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --build-definition-id {definition-id} \
  --queue-on-source-update-only true \
  --valid-duration 720
```

#### 工作项链接策略

```bash
az repos policy work-item-linking create \
  --blocking true \
  --branch main \
  --enabled true \
  --repository-id {repo-id}
```

#### 必须审阅者策略

```bash
az repos policy required-reviewer create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --required-reviewers user@example.com
```

#### 合并策略

```bash
az repos policy merge-strategy create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --allow-squash true \
  --allow-rebase true \
  --allow-no-fast-forward true
```

#### 大小写强制策略

```bash
az repos policy case-enforcement create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id}
```

#### 必须评论策略

```bash
az repos policy comment-required create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id}
```

#### 文件大小策略

```bash
az repos policy file-size create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --maximum-file-size 10485760  # 10MB（字节）
```

## 服务端点

### 列出服务端点

```bash
az devops service-endpoint list --project {project}
az devops service-endpoint list --project {project} --output table
```

### 显示服务端点

```bash
az devops service-endpoint show --id {endpoint-id} --project {project}
```

### 创建服务端点

```bash
# 使用配置文件
az devops service-endpoint create --service-endpoint-configuration endpoint.json --project {project}
```

### 删除服务端点

```bash
az devops service-endpoint delete --id {endpoint-id} --project {project} --yes
```

## 团队

### 列出团队

```bash
az devops team list --project {project}
```

### 显示团队

```bash
az devops team show --team {team-name} --project {project}
```

### 创建团队

```bash
az devops team create \
  --name {team-name} \
  --description "团队描述" \
  --project {project}
```

### 更新团队

```bash
az devops team update \
  --team {team-name} \
  --project {project} \
  --name "{new-team-name}" \
  --description "更新描述"
```

### 删除团队

```bash
az devops team delete --team {team-name} --project {project} --yes
```

### 显示团队成员

```bash
az devops team list-member --team {team-name} --project {project}
```

## 用户

### 列出用户

```bash
az devops user list --org https://dev.azure.com/{org}
az devops user list --top 10 --output table
```

### 显示用户

```bash
az devops user show --user {user-id-or-email} --org https://dev.azure.com/{org}
```

### 添加用户

```bash
az devops user add \
  --email user@example.com \
  --license-type express \
  --org https://dev.azure.com/{org}
```

### 更新用户

```bash
az devops user update \
  --user {user-id-or-email} \
  --license-type advanced \
  --org https://dev.azure.com/{org}
```

### 移除用户

```bash
az devops user remove --user {user-id-or-email} --org https://dev.azure.com/{org} --yes
```

## 安全组

### 列出组

```bash
# 列出项目中的所有组
az devops security group list --project {project}

# 列出组织中的所有组
az devops security group list --scope organization

# 带过滤的列出
az devops security group list --project {project} --subject-types vstsgroup
```

### 显示组详细信息

```bash
az devops security group show --group-id {group-id}
```

### 创建组

```bash
az devops security group create \
  --name {group-name} \
  --description "组描述" \
  --project {project}
```

### 更新组

```bash
az devops security group update \
  --group-id {group-id} \
  --name "{new-group-name}" \
  --description "更新描述"
```

### 删除组

```bash
az devops security group delete --group-id {group-id} --yes
```

### 组成员关系

```bash
# 列出成员关系
az devops security group membership list --id {group-id}

# 添加成员
az devops security group membership add \
  --group-id {group-id} \
  --member-id {member-id}

# 移除成员
az devops security group membership remove \
  --group-id {group-id} \
  --member-id {member-id} --yes
```

## 安全权限

### 列出命名空间

```bash
az devops security permission namespace list
```

### 显示命名空间详细信息

```bash
# 显示命名空间中的权限
az devops security permission namespace show --namespace "GitRepositories"
```

### 列出权限

```bash
# 列出用户/组和命名空间的权限
az devops security permission list \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project}

# 列出特定令牌（仓库）的权限
az devops security permission list \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}"
```

### 显示权限

```bash
az devops security permission show \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}"
```

### 更新权限

```bash
# 授予权限
az devops security permission update \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" \
  --permission-mask "Pull,Contribute"

# 拒绝权限
az devops security permission update \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" \
  --permission-mask 0
```

### 重置权限

```bash
# 重置特定权限位
az devops security permission reset \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" \
  --permission-mask "Pull,Contribute"

# 重置所有权限
az devops security permission reset-all \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" --yes
```

## 维基

### 列出维基

```bash
# 列出项目中的所有维基
az devops wiki list --project {project}

# 列出组织中的所有维基
az devops wiki list
```

### 显示维基

```bash
az devops wiki show --wiki {wiki-name} --project {project}
az devops wiki show --wiki {wiki-name} --project {project} --open
```

### 创建维基

```bash
# 创建项目维基
az devops wiki create \
  --name {wiki-name} \
  --project {project} \
  --type projectWiki

# 从仓库创建代码维基
az devops wiki create \
  --name {wiki-name} \
  --project {project} \
  --type codeWiki \
  --repository {repo-name} \
  --mapped-path /wiki
```

### 删除维基

```bash
az devops wiki delete --wiki {wiki-id} --project {project} --yes
```

### 维基页面

```bash
# 列出页面
az devops wiki page list --wiki {wiki-name} --project {project}

# 显示页面
az devops wiki page show \
  --wiki {wiki-name} \
  --path "/page-name" \
  --project {project}

# 创建页面
az devops wiki page create \
  --wiki {wiki-name} \
  --path "/new-page" \
  --content "# 新页面\n\n页面内容..." \
  --project {project}

# 更新页面
az devops wiki page update \
  --wiki {wiki-name} \
  --path "/existing-page" \
  --content "# 更新页面\n\n新内容..." \
  --project {project}

# 删除页面
az devops wiki page delete \
  --wiki {wiki-name} \
  --path "/old-page" \
  --project {project} --yes
```

## 管理

### 横幅管理

```bash

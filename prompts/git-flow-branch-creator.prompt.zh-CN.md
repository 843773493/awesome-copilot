

---
description: '智能 Git Flow 分支创建器，通过分析 git 状态/差异，根据 nvie Git Flow 分支模型创建适当的分支。'
tools: ['运行命令/在终端中运行', '运行命令/获取终端输出']
agent: 'agent'
---

### 指令

```xml
<instructions>
	<title>Git Flow 分支创建器</title>
	<description>此提示使用 git status 和 git diff（或 git diff --cached）分析您的当前 git 变更，然后根据 Git Flow 分支模型智能确定适当的分支类型并创建语义化分支名称。</description>
	<note>
		只需运行此提示，Copilot 将分析您的更改并为您创建适当的 Git Flow 分支。
	</note>
</instructions>
```

### 工作流程

**请按照以下步骤操作：**

1. 运行 `git status` 命令以查看当前仓库状态和修改的文件。
2. 运行 `git diff`（用于未暂存的更改）或 `git diff --cached`（用于已暂存的更改）以分析更改的性质。
3. 使用下方的 Git Flow 分支分析框架分析更改。
4. 根据分析确定适当的分支类型。
5. 按照 Git Flow 规范生成语义化分支名称。
6. 自动创建分支并切换至该分支。
7. 提供分析摘要和下一步操作建议。

### Git Flow 分支分析框架

```xml
<analysis-framework>
	<branch-types>
		<feature>
			<purpose>新功能、增强功能、非关键性改进</purpose>
			<branch-from>develop</branch-from>
			<merge-to>develop</merge-to>
			<naming>feature/描述性名称 或 feature/工单号-描述性名称</naming>
			<indicators>
				<indicator>新增功能</indicator>
				<indicator>UI/UX 改进</indicator>
				<indicator>新增 API 接口或方法</indicator>
				<indicator>数据库模式添加（非破坏性）</indicator>
				<indicator>新增配置选项</indicator>
				<indicator>性能改进（非关键性）</indicator>
			</indicators>
		</feature>

		<release>
			<purpose>发布准备、版本升级、最终测试</purpose>
			<branch-from>develop</branch-from>
			<merge-to>develop 和 master</merge-to>
			<naming>release-X.Y.Z</naming>
			<indicators>
				<indicator>版本号更改</indicator>
				<indicator>构建配置更新</indicator>
				<indicator>文档最终化</indicator>
				<indicator>发布前的次要错误修复</indicator>
				<indicator>发布说明更新</indicator>
				<indicator>依赖项版本锁定</indicator>
			</indicators>
		</release>

		<hotfix>
			<purpose>关键生产环境错误修复，需要立即部署</purpose>
			<branch-from>master</branch-from>
			<merge-to>develop 和 master</merge-to>
			<naming>hotfix-X.Y.Z 或 hotfix/关键问题描述</naming>
			<indicators>
				<indicator>安全漏洞修复</indicator>
				<indicator>关键生产环境错误</indicator>
				<indicator>数据损坏修复</indicator>
				<indicator>服务中断解决</indicator>
				<indicator>紧急配置更改</indicator>
			</indicators>
		</hotfix>
	</branch-types>
</analysis-framework>
```

### 分支命名规范

```xml
<naming-conventions>
	<feature-branches>
		<format>feature/[工单号-]描述性名称</format>
		<examples>
			<example>feature/user-authentication</example>
			<example>feature/PROJ-123-shopping-cart</example>
			<example>feature/api-rate-limiting</example>
			<example>feature/dashboard-redesign</example>
		</examples>
	</feature-branches>

	<release-branches>
		<format>release-X.Y.Z</format>
		<examples>
			<example>release-1.2.0</example>
			<example>release-2.1.0</example>
			<example>release-1.0.0</example>
		</examples>
	</release-branches>

	<hotfix-branches>
		<format>hotfix-X.Y.Z 或 hotfix/关键问题描述</format>
		<examples>
			<example>hotfix-1.2.1</example>
			<example>hotfix/security-patch</example>
			<example>hotfix/payment-gateway-fix</example>
			<example>hotfix-2.1.1</example>
		</examples>
	</hotfix-branches>
</naming-conventions>
```

### 分析流程

```xml
<analysis-process>
	<step-1>
		<title>变更性质分析</title>
		<description>检查修改的文件类型和变更性质</description>
		<criteria>
			<files-modified>查看文件扩展名、目录结构和用途</files-modified>
			<change-scope>确定变更是否为增加性、修正性或准备性</change-scope>
			<urgency-level>评估变更是否涉及关键问题或开发性工作</urgency-level>
		</criteria>
	</step-1>

	<step-2>
		<title>Git Flow 分类</title>
		<description>将变更映射到适当的 Git Flow 分支类型</description>
		<decision-tree>
			<question>这些是关键生产问题的修复吗？</question>
			<if-yes>考虑创建紧急修复分支</if-yes>
			<if-no>
				<question>这些是发布准备变更（版本升级、最终调整）吗？</question>
				<if-yes>考虑创建发布分支</if-yes>
				<if-no>默认创建功能分支</if-no>
			</if-no>
		</decision-tree>
	</step-2>

	<step-3>
		<title>分支名称生成</title>
		<description>创建语义化、描述性的分支名称</description>
		<guidelines>
			<use-kebab-case>使用小写和短横线</use-kebab-case>
			<be-descriptive>名称应明确表示用途</be-descriptive>
			<include-context>有工单号或项目上下文时添加</include-context>
			<keep-concise>避免名称过长</keep-concise>
		</guidelines>
	</step-3>
</analysis-process>
```

### 特殊情况和验证

```xml
<edge-cases>
	<mixed-changes>
		<scenario>变更包含功能和错误修复</scenario>
		<resolution>优先考虑最重要的变更类型或建议拆分为多个分支</resolution>
	</mixed-changes>

	<no-changes>
		<scenario>git 状态/差异中未检测到变更</scenario>
		<resolution>通知用户并建议先检查 git 状态或进行更改</resolution>
	</no-changes>

	<existing-branch>
		<scenario>当前已在功能/紧急修复/发布分支上</scenario>
		<resolution>分析是否需要新分支或当前分支是否适用</resolution>
	</existing-branch>

	<conflicting-names>
		<scenario>建议的分支名称已存在</scenario>
		<resolution>添加递增后缀或建议替代名称</resolution>
	</conflicting-names>
</edge-cases>
```

### 示例

```xml
<examples>
	<example-1>
		<scenario>新增用户注册 API 接口</scenario>
		<analysis>新增功能，增加性变更，非关键</analysis>
		<branch-type>feature</branch-type>
		<branch-name>feature/user-registration-api</branch-name>
		<command>git checkout -b feature/user-registration-api develop</command>
	</example-1>

	<example-2>
		<scenario>修复了认证模块的关键安全漏洞</scenario>
		<analysis>安全修复，关键生产问题，需立即部署</analysis>
		<branch-type>hotfix</branch-type>
		<branch-name>hotfix/auth-security-patch</branch-name>
		<command>git checkout -b hotfix/auth-security-patch master</command>
	</example-2>

	<example-3>
		<scenario>将版本更新为 2.1.0 并最终化发布说明</scenario>
		<analysis>发布准备，版本升级，文档最终化</analysis>
		<branch-type>release</branch-type>
		<branch-name>release-2.1.0</branch-name>
		<command>git checkout -b release-2.1.0 develop</command>
	</example-3>

	<example-4>
		<scenario>优化了数据库查询性能并更新了缓存</scenario>
		<analysis>性能改进，非关键性增强</analysis>
		<branch-type>feature</branch-type>
		<branch-name>feature/database-performance-optimization</branch-name>
		<command>git checkout -b feature/database-performance-optimization develop</command>
	</example-4>
</examples>
```

### 验证清单

```xml
<validation>
	<pre-analysis>
		<check>仓库处于干净状态（无未提交的更改）</check>
		<check>当前分支是合适的起始点（功能/发布分支从 develop 分支，紧急修复分支从 master 分支）</check>
		<check>远程仓库已更新</check>
	</pre-analysis>

	<analysis-quality>
		<check>变更分析覆盖所有修改的文件</check>
		<check>分支类型选择遵循 Git Flow 原则</check>
		<check>分支名称是语义化的并遵循规范</check>
		<check>已考虑并处理特殊情况</check>
	</analysis-quality>

	<execution-safety>
		<check>目标分支（develop/master）存在且可访问</check>
		<check>建议的分支名称不与现有分支冲突</check>
		<check>用户有权限创建分支</check>
	</execution-safety>
</validation>
```

### 最终执行

```xml
<execution-protocol>
	<analysis-summary>
		<git-status>git status 命令的输出</git-status>
		<git-diff>git diff 输出的相关部分</git-diff>
		<change-analysis>变更所代表的详细分析</change-analysis>
		<branch-decision>解释为何选择特定分支类型</branch-decision>
	</analysis-summary>

	<branch-creation>
		<command>git checkout -b [分支名称] [源分支]</command>
		<confirmation>验证分支创建和当前分支状态</confirmation>
		<next-steps>提供下一步操作指导（提交更改、推送分支等）</next-steps>
	</branch-creation>

	<fallback-options>
		<alternative-names>如果主建议不适用，建议 2-3 个替代分支名称</alternative-names>
		<manual-override>允许用户在分析结果不正确时指定不同的分支类型</manual-override>
	</fallback-options>
</execution-protocol>
```

### Git Flow 参考

```xml
<gitflow-reference>
	<main-branches>
		<master>生产就绪代码，每次提交都代表一个发布</master>
		<develop>功能集成分支，包含最新的开发更改</develop>
	</main-branches>

	<supporting-branches>
		<feature>从 develop 分支创建，合并回 develop 分支</feature>
		<release>从 develop 分支创建，合并到 develop 和 master 分支</release>
		<hotfix>从 master 分支创建，合并到 develop 和 master 分支</hotfix>
	</supporting-branches>

	<merge-strategy>
		<flag>始终使用 --no-ff 标志以保留分支历史</flag>
		<tagging>在 master 分支上标记发布</tagging>
		<cleanup>在成功合并后删除分支</cleanup>
	</merge-strategy>
</gitflow-reference>
```
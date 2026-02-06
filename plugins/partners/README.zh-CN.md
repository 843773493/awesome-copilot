# 合作伙伴插件

由GitHub合作伙伴创建的自定义代理

## 安装

```bash
# 使用Copilot CLI
copilot plugin install partners@awesome-copilot
```

## 包含内容

### 代理

| 代理 | 描述 |
|------|------|
| `amplitude-experiment-implementation` | 该自定义代理使用Amplitude的MCP工具在Amplitude内部部署新实验，实现无缝的变体测试功能和产品功能发布。 |
| `apify-integration-expert` | 用于将Apify Actors集成到代码库中的专家代理。处理Actor选择、工作流设计、JavaScript/TypeScript和Python的实现、测试以及生产就绪的部署。 |
| `arm-migration` | Arm Cloud Migration Assistant通过扫描仓库中的架构假设、可移植性问题、容器基础镜像和依赖项不兼容性，加速将x86工作负载迁移到Arm基础设施。它推荐Arm优化的更改，可驱动多架构容器构建，验证性能，并指导优化，从而实现GitHub内部的跨平台部署。 |
| `diffblue-cover` | 用于使用Diffblue Cover为Java应用程序创建单元测试的专家代理。 |
| `droid` | 提供Droid CLI的安装指南、使用示例和自动化模式，特别强调droid exec在CI/CD和非交互式自动化中的应用。 |
| `dynatrace-expert` | Dynatrace专家代理将可观测性和安全功能直接集成到GitHub工作流中，使开发团队能够通过自主分析追踪、日志和Dynatrace发现结果，调查事件、验证部署、错误分类、检测性能回归、验证发布并管理安全漏洞。这使得在仓库内部对识别出的问题进行针对性和精确的修复成为可能。 |
| `elasticsearch-observability` | 我们的专家AI助手，用于通过实时Elastic数据调试代码（O11y）、优化向量搜索（RAG）以及修复安全威胁。 |
| `jfrog-sec` | 专为自动化安全修复而设计的应用程序安全代理。利用JFrog安全智能验证包和版本合规性，并建议漏洞修复方案。 |
| `launchdarkly-flag-cleanup` | 一个专门的GitHub Copilot代理，使用LaunchDarkly MCP服务器安全地自动化功能标志清理工作流。该代理确定移除准备情况，识别正确的转发值，并创建保留生产行为的拉取请求（PRs），同时移除过时的标志并更新陈旧的默认值。 |
| `lingodotdev-i18n` | 采用系统化、检查清单驱动的方法，专精于在Web应用程序中实现国际化（i18n）。 |
| `monday-bug-fixer` | 从Monday.com平台数据中丰富任务上下文的高级错误修复代理。收集相关项目、文档、评论、史诗和需求，以交付符合生产标准的修复方案并生成全面的拉取请求（PRs）。 |
| `mongodb-performance-advisor` | 分析MongoDB数据库性能，提供查询和索引优化见解，并提供可操作的建议以提高数据库的整体使用效率。 |
| `neo4j-docker-client-generator` | 一种AI代理，可从GitHub问题生成简单、高质量的Python Neo4j客户端库，并遵循最佳实践。 |
| `neon-migration-specialist` | 使用Neon的分支工作流实现安全的Postgres迁移，零停机时间。在隔离的数据库分支中测试架构更改，彻底验证后应用到生产环境——所有操作均可自动化，并支持Prisma、Drizzle或您最喜欢的ORM。 |
| `neon-optimization-analyzer` | 使用Neon的分支工作流自动识别和修复缓慢的Postgres查询。分析执行计划，在隔离的数据库分支中测试优化，并提供清晰的前后性能指标及可操作的代码修复方案。 |
| `octopus-deploy-release-notes-mcp` | 为Octopus Deploy中的发布生成发布说明。该MCP服务器工具提供对Octopus Deploy API的访问权限。 |
| `stackhawk-security-onboarding` | 通过生成的配置和GitHub Actions工作流自动设置StackHawk安全测试。 |
| `terraform` | 一种Terraform基础设施专家，提供自动化的HCP Terraform工作流。利用Terraform MCP服务器进行注册表集成、工作区管理和运行编排。使用最新提供者/模块版本生成合规代码，管理私有注册表，自动化变量集，并通过适当的验证和安全实践编排基础设施部署。 |
| `pagerduty-incident-responder` | 通过分析事件上下文、识别最近的代码更改，并通过GitHub拉取请求（PRs）建议修复方案，响应PagerDuty事件。 |
| `comet-opik` | 用于对LLM应用进行仪器化、管理提示/项目、审计提示以及通过最新Opik MCP服务器调查追踪/指标的统一Comet Opik代理。 | 

## 来源

此插件是[Awesome Copilot](https://github.com/github/awesome-copilot)的一部分，这是一个由社区驱动的GitHub Copilot扩展集合。

## 许可证

MIT

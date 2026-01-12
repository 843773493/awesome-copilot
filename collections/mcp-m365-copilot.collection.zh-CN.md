

# 基于MCP的M365代理收集

一个全面的提示和指令集合，用于使用模型上下文协议（MCP）集成构建声明式代理，以扩展Microsoft 365 Copilot的自定义功能。

## 概述

模型上下文协议（MCP）是一种通用标准，允许AI模型通过标准化的服务器端点与外部系统集成。本集合提供了构建、部署和管理基于MCP的声明式代理所需的一切，这些代理可以扩展Microsoft 365 Copilot的功能。

## 什么是模型上下文协议？

MCP是一种开放协议，旨在简化AI模型如何连接到外部数据源和工具。它提供了一致的接口，无需为每个系统编写自定义集成代码：

- **服务器元数据**：发现可用的工具和功能
- **工具列表**：获取函数定义和模式
- **工具执行**：使用参数调用工具并接收结果

对于Microsoft 365 Copilot，这意味着您可以使用点按配置的方式，将代理连接到任何兼容MCP的服务器，而无需编写自定义代码。

## 集合内容

### 提示

1. **创建声明式代理** ([mcp-create-declarative-agent.prompt.md](../prompts/mcp-create-declarative-agent.prompt.md))
   - 使用Microsoft 365代理工具包构建声明式代理
   - 通过工具导入配置MCP服务器集成
   - 设置OAuth 2.0或SSO认证
   - 配置响应语义以提取数据
   - 打包和部署代理以进行测试

2. **创建自适应卡片** ([mcp-create-adaptive-cards.prompt.md](../prompts/mcp-create-adaptive-cards.prompt.md))
   - 设计静态和动态的自适应卡片模板
   - 配置响应语义（data_path、properties、template_selector）
   - 使用模板语言进行条件判断和数据绑定
   - 创建适用于Copilot各界面的响应式卡片
   - 实现卡片操作以支持用户交互

3. **部署和管理代理** ([mcp-deploy-manage-agents.prompt.md](../prompts/mcp-deploy-manage-agents.prompt.md))
   - 通过Microsoft 365管理中心部署代理
   - 配置组织级或公共商店分发
   - 管理代理生命周期（发布、部署、阻止、移除）
   - 设置治理和合规性控制
   - 监控代理使用情况和性能

### 指南

**MCP M365 Copilot开发指南** ([mcp-m365-copilot.instructions.md](../instructions/mcp-m365-copilot.instructions.md))
- MCP服务器设计和工具选择的最佳实践
- 文件组织和项目结构
- 响应语义配置模式
- 自适应卡片设计原则
- 安全性、治理和合规性要求
- 测试和部署工作流

## 关键概念

### 声明式代理

声明式代理是通过配置文件而非代码定义的：
- **declarativeAgent.json**：代理指令、功能、对话启动项
- **ai-plugin.json**：MCP服务器工具、响应语义、自适应卡片模板
- **mcp.json**：MCP服务器URL、认证配置
- **manifest.json**：用于打包的Teams应用清单

### MCP服务器集成

Microsoft 365代理工具包提供了一个可视化界面用于：
1. **创建**一个新的代理项目
2. **添加MCP操作**以连接到服务器
3. **选择工具**来自服务器可用功能
4. **配置认证**（OAuth 2.0、SSO）
5. **生成文件**（代理配置、插件清单）
6. **在m365.cloud.microsoft/chat中测试**

### 认证模式

**OAuth 2.0静态注册：**
- 预先在服务提供商处注册OAuth应用
- 在.env.local中存储凭证（切勿提交）
- 在ai-plugin.json认证配置中引用
- 用户一次性授权，令牌存储在插件保险库中

**单点登录（SSO）：**
- 使用Microsoft Entra ID进行认证
- 为M365用户提供无缝体验
- 不需要单独登录
- 适用于内部组织代理

### 响应语义

从MCP服务器响应中提取和格式化数据：

```json
{
  "response_semantics": {
    "data_path": "$.items[*]",
    "properties": {
      "title": "$.name",
      "subtitle": "$.description",
      "url": "$.html_url"
    },
    "static_template": { ... }
  }
}
```

- **data_path**：JSONPath用于提取数组或对象
- **properties**：将响应字段映射到Copilot属性
- **template_selector**：根据响应选择动态模板
- **static_template**：用于视觉格式化的自适应卡片

### 自适应卡片

丰富的视觉响应用于代理输出：

**静态模板：**
- 在ai-plugin.json中定义一次
- 用于所有具有相同结构的响应
- 更好的性能和更简单的维护

**动态模板：**
- 由API响应体返回
- 通过template_selector JSONPath选择
- 适用于不同的响应结构

**模板语言：**
- `${property}`：数据绑定
- `${if(condition, true, false)}`：条件判断
- `${formatNumber(value, decimals)}`：格式化
- `$when`：条件元素渲染

## 部署选项

### 组织部署
- IT管理员将代理部署给所有用户或特定组
- 需要在Microsoft 365管理中心进行审批
- 适用于内部业务代理
- 完整的治理和合规性控制

### 代理商店
- 提交到Partner Center进行验证
- 对所有Copilot用户公开可用
- 严格的网络安全和合规性审查
- 适用于合作伙伴构建的代理

## 合作伙伴示例

### monday.com
任务和项目管理集成：
- 直接从Copilot创建任务
- 查询项目状态和更新
- 将工作项分配给团队成员
- 查看截止日期和里程碑

### Canva
设计自动化功能：
- 生成品牌内容
- 创建社交媒体图形
- 访问设计模板
- 导出多种格式

### Sitecore
内容管理集成：
- 搜索内容库
- 创建和更新内容项
- 管理工作流和审批
- 在上下文中预览内容

## 快速入门

### 先决条件
            return results
- Microsoft 365代理工具包扩展（v6.3.x或更高版本）
- GitHub账户（用于OAuth示例）
- Microsoft 365 Copilot许可证
- 访问MCP兼容的服务器

### 快速开始
1. 在VS Code中安装Microsoft 365代理工具包
2. 使用**创建声明式代理**提示来搭建项目
3. 添加MCP服务器URL并选择工具
4. 使用OAuth或SSO配置认证
5. 使用**创建自适应卡片**提示设计响应模板
6. 在m365.cloud.microsoft/chat中测试代理
7. 使用**部署和管理代理**提示进行分发

### 开发工作流
```
1. 搭建代理项目
   ↓
2. 连接MCP服务器
   ↓
3. 导入工具
   ↓
4. 配置认证
   ↓
5. 设计自适应卡片
   ↓
6. 本地测试
   ↓
7. 部署到组织
   ↓
8. 监控和迭代
```

## 最佳实践

### MCP服务器设计
- 仅导入必要的工具（避免过度范围）
- 使用安全认证（OAuth 2.0、SSO）
- 单独测试每个工具
- 验证服务器端点是否为HTTPS
- 选择工具时考虑令牌限制

### 代理指令
- 明确且清晰地描述代理功能
- 提供如何交互的示例
- 设定代理能/不能执行的边界
- 使用对话启动项引导用户

### 响应格式化
- 使用JSONPath提取相关数据
- 清晰地映射属性（标题、副标题、URL）
- 设计自适应卡片以提高可读性
- 在Copilot各界面（聊天、Teams、Outlook）中测试卡片

### 安全性和治理
- 绝对不要将凭证提交到源代码控制
- 使用环境变量存储机密
- 遵循最小特权原则
- 审查合规性要求
- 监控代理使用情况和性能

## 常见使用场景

### 数据检索
- 搜索外部系统
- 获取用户特定信息
- 查询数据库或API
- 从多个来源汇总数据

### 任务自动化
- 创建工单或任务
- 更新记录或状态
- 触发工作流
- 安排操作

### 内容生成
- 创建文档或设计
- 生成报告或摘要
- 将数据格式化为模板
- 导出为多种格式

### 集成场景
- 连接CRM系统
- 集成项目管理工具
- 访问知识库
- 连接到自定义业务应用

## 故障排除

### 代理未在Copilot中显示
- 验证代理是否在管理中心部署
- 检查用户是否属于分配的组
- 确认代理未被阻止
- 刷新Copilot界面

### 认证错误
- 验证.env.local中的OAuth凭证
- 检查作用域是否匹配所需权限
- 独立测试认证流程
- 验证MCP服务器是否可访问

### 响应格式化问题
- 使用示例数据测试JSONPath表达式
- 验证data_path是否提取预期的数组/对象
- 检查属性映射是否正确
- 使用不同响应结构测试自适应卡片

### 性能问题
- 监控MCP服务器响应时间
- 减少导入的工具数量
- 优化响应数据大小
- 适当使用缓存

## 资源

### 官方文档
- [使用MCP构建声明式代理（DevBlogs）](https://devblogs.microsoft.com/microsoft365dev/build-declarative-agents-for-microsoft-365-copilot-with-mcp/)
- [构建MCP插件（Microsoft Learn）](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/build-mcp-plugins)
- [API插件自适应卡片（Microsoft Learn）](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api-plugin-adaptive-cards)
- [管理Copilot代理（Microsoft Learn）](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-copilot-agents-integrated-apps)

### 工具和扩展
- [Microsoft 365代理工具包](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.ms-teams-vscode-extension)
- [自适应卡片设计器](https://adaptivecards.io/designer/)
- [Teams工具包](https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/teams-toolkit-fundamentals)

### MCP资源
- [模型上下文协议规范](https://modelcontextprotocol.io/)
- [MCP服务器目录](https://github.com/modelcontextprotocol/servers)
- 社区MCP服务器和示例

### 管理员和治理
- [Microsoft 365管理中心](https://admin.microsoft.com/)
- [Power Platform管理中心](https://admin.powerplatform.microsoft.com/)
- [合作伙伴中心](https://partner.microsoft.com/)用于代理提交

## 支持和社区

- 加入[Microsoft 365开发者社区](https://developer.microsoft.com/en-us/microsoft-365/community)
- 在[Microsoft Q&A](https://learn.microsoft.com/en-us/answers/products/)上提问
- 在[Microsoft 365 Copilot GitHub讨论](https://github.com/microsoft/copilot-feedback)中分享反馈

## 下一步

掌握基于MCP的代理后，可以探索：
- **高级工具组合**：结合多个MCP服务器
- **自定义认证流程**：实现自定义OAuth提供者
- **复杂自适应卡片**：包含动态数据的多操作卡片
- **代理分析**：跟踪使用模式并优化
- **多代理协调**：构建协同工作的代理
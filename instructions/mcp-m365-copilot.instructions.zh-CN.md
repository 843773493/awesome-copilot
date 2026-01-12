

---
description: '基于模型上下文协议（MCP）构建 Copilot 代理和 API 插件的最佳实践，用于 Microsoft 365 Copilot'
applyTo: '**/{*mcp*,*agent*,*plugin*,declarativeAgent.json,ai-plugin.json,mcp.json,manifest.json}'
---

# 基于模型上下文协议（MCP）的 Microsoft 365 Copilot 开发指南

## 核心原则

### 以模型上下文协议为先
- 利用 MCP 服务器进行外部系统集成
- 从服务器端点导入工具，而非手动定义
- 由 MCP 处理模式发现和功能生成
- 在代理工具包中使用点击选择工具

### 声明式优于指令式
- 通过配置定义代理行为，而非代码
- 使用 declarativeAgent.json 定义指令和功能
- 在 ai-plugin.json 中指定工具和操作
- 在 mcp.json 中配置 MCP 服务器

### 安全与治理
- 始终使用 OAuth 2.0 或 SSO 进行身份验证
- 工具选择遵循最小特权原则
- 验证 MCP 服务器端点的安全性
- 部署前审查合规要求

### 用户为中心的设计
- 创建丰富的视觉响应适配卡片
- 提供清晰的对话启动语
- 设计适用于各平台的响应体验
- 组织部署前进行彻底测试

## MCP 服务器设计

### 服务器选择
选择 MCP 服务器时需满足：
- 暴露与用户任务相关的工具
- 支持安全身份验证（OAuth 2.0、SSO）
- 提供可靠的服务可用性和性能
- 遵循 MCP 规范标准
- 返回结构良好的响应数据

### 工具导入策略
- 仅导入必要的工具（避免过度定义）
- 将同一服务器的相关工具分组
- 在组合前单独测试每个工具
- 选择多个工具时考虑令牌限制

### 身份验证配置
**OAuth 2.0 静态注册：**
```json
{
  "type": "OAuthPluginVault",
  "reference_id": "YOUR_AUTH_ID",
  "client_id": "github_client_id",
  "client_secret": "github_client_secret",
  "authorization_url": "https://github.com/login/oauth/authorize",
  "token_url": "https://github.com/login/oauth/access_token",
  "scope": "repo read:user"
}
```

**SSO（Microsoft Entra ID）：**
```json
{
  "type": "OAuthPluginVault",
  "reference_id": "sso_auth",
  "authorization_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
  "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
  "scope": "User.Read"
}
```

## 文件组织

### 项目结构
```
project-root/
├── appPackage/
│   ├── manifest.json           # Teams 应用清单文件
│   ├── declarativeAgent.json   # 代理配置文件（指令、功能）
│   ├── ai-plugin.json          # API 插件定义
│   ├── color.png               # 应用彩色图标
│   └── outline.png             # 应用轮廓图标
├── .vscode/
│   └── mcp.json               # MCP 服务器配置
├── .env.local                  # 凭据（绝不要提交）
└── teamsapp.yml               # Teams 工具包配置
```

### 关键文件

**declarativeAgent.json:**
- 代理名称和描述
- 行为指令
- 对话启动语
- 功能（来自插件的操作）

**ai-plugin.json:**
- 导入 MCP 服务器工具
- 响应语义（data_path、properties）
- 静态适配卡片模板
- 功能定义（自动生成）

**mcp.json:**
- MCP 服务器 URL
- 服务器元数据端点
- 身份验证参考

**.env.local:**
- OAuth 客户端凭据
- API 密钥和密钥
- 环境特定配置
- **关键**: 添加到 .gitignore

## 响应语义最佳实践

### 数据路径配置
使用 JSONPath 提取相关数据：
```json
{
  "data_path": "$.items[*]",
  "properties": {
    "title": "$.name",
    "subtitle": "$.description", 
    "url": "$.html_url"
  }
}
```

### 模板选择
对于动态模板：
```json
{
  "data_path": "$",
  "template_selector": "$.templateType",
  "properties": {
    "title": "$.title",
    "url": "$.url"
  }
}
```

### 静态模板
在 ai-plugin.json 中定义以确保格式一致：
- 当所有响应结构相同使用
- 比动态模板性能更好
- 更便于维护和版本控制

## 适配卡片指南

### 设计原则
- **单列布局**: 元素垂直堆叠
- **灵活宽度**: 使用 "stretch" 或 "auto"，而非固定像素
- **响应式设计**: 在聊天、Teams、Outlook 中测试
- **最小复杂度**: 保持卡片简洁且易于扫描

### 模板语言模式
**条件判断:**
```json
{
  "type": "TextBlock",
  "text": "${if(status == 'active', '✅ 活跃', '❌ 不活跃')}"
}
```

**数据绑定:**
```json
{
  "type": "TextBlock",
  "text": "${title}",
  "weight": "bolder"
}
```

**数字格式化:**
```json
{
  "type": "TextBlock",
  "text": "得分: ${formatNumber(score, 0)}"
}
```

**条件渲染:**
```json
{
  "type": "Container",
  "$when": "${count(items) > 0}",
  "items": [ ... ]
}
```

### 卡片元素使用
- **TextBlock**: 标题、描述、元数据
- **FactSet**: 键值对（状态、日期、ID）
- **Image**: 图标、缩略图（使用 size: "small"）
- **Container**: 分组相关内容
- **ActionSet**: 用于后续操作的按钮

## 测试与部署

### 本地测试工作流
1. **配置**: Teams 工具包 → 配置
2. **部署**: Teams 工具包 → 部署
3. **侧载**: 应用上传至 Teams
4. **测试**: 访问 [m365.cloud.microsoft/chat](https://m365.cloud.microsoft/chat)
5. **迭代**: 修复问题并重新部署

### 部署前检查清单
- [ ] 所有 MCP 服务器工具已单独测试
- [ ] 身份验证流程端到端正常运行
- [ ] 适配卡片在各平台正常显示
- [ ] 响应语义提取预期数据
- [ ] 错误处理提供清晰信息
- [ ] 对话启动语相关且明确
- [ ] 代理指令引导正确行为
- [ ] 合规与安全要求已审查

### 部署选项
**组织部署:**
- IT 管理员部署给所有用户或特定用户组
- 需在 Microsoft 365 管理中心获得批准
- 适用于内部业务代理

**代理商店:**
- 提交至合作伙伴中心进行验证
- 公开提供给所有 Copilot 用户
- 需进行严格的安全审查

## 常见模式

### 多工具代理
从多个 MCP 服务器导入工具：
```json
{
  "mcpServers": {
    "github": {
      "url": "https://github-mcp.example.com"
    },
    "jira": {
      "url": "https://jira-mcp.example.com"
    }
  }
}
```

### 搜索与展示
1. 工具从 MCP 服务器获取数据
2. 响应语义提取相关字段
3. 适配卡片展示格式化结果
4. 用户可通过卡片按钮进行操作

### 认证操作
1. 用户触发需要认证的工具
2. OAuth 流程重定向以获取授权
3. 访问令牌存储在插件保险库中
4. 后续请求使用存储的令牌

## 错误处理

### MCP 服务器错误
- 在代理响应中提供清晰错误信息
- 若有替代工具则回退使用
- 记录错误以供调试
- 引导用户重试或采用替代方案

### 身份验证失败
- 检查 .env.local 中的 OAuth 凭据
- 验证作用域是否匹配所需权限
- 首先在 Copilot 之外测试身份验证流程
- 确保令牌刷新逻辑正常运行

### 响应解析失败
- 验证响应语义中的 JSONPath 表达式
- 优雅处理缺失或空数据
- 在适当位置提供默认值
- 使用不同 API 响应进行测试

## 性能优化

### 工具选择
- 仅导入必要工具（减少令牌使用）
- 避免从多个服务器导入冗余工具
- 测试每种工具对响应时间的影响

### 响应大小
- 使用 data_path 过滤不必要的数据
- 尽可能限制结果集
- 对大型数据集考虑分页
- 保持适配卡片轻量

### 缓存策略
- MCP 服务器应适当缓存
- 代理响应可能被 M365 缓存
- 对时间敏感数据考虑缓存失效策略

## 安全最佳实践

### 凭据管理
- **绝不要**将 .env.local 提交至源代码控制
- 使用环境变量存储所有密钥
- 定期轮换 OAuth 凭据
- 开发/生产环境使用不同凭据

### 数据隐私
- 仅请求必要最小作用域
- 避免记录敏感用户数据
- 审查数据驻留要求
- 遵循合规政策（如 GDPR 等）

### 服务器验证
- 验证 MCP 服务器是否可信且安全
- 仅检查 HTTPS 端点
- 审查服务器的隐私政策
- 测试注入漏洞

## 治理与合规

### 管理员控制
代理可以：
- **被阻止**: 禁止使用
- **被部署**: 分配给特定用户/组
- **被发布**: 在组织范围内提供

### 监控
跟踪：
- 代理使用和采用情况
- 错误率和性能
- 用户反馈和满意度
- 安全事件

### 审计要求
维护：
- 代理配置的变更历史
- 敏感操作的访问日志
- 部署的审批记录
- 合规声明

## 资源与参考资料

### 官方文档
- [使用 MCP 构建声明式代理（DevBlogs）](https://devblogs.microsoft.com/microsoft365dev/build-declarative-agents-for-microsoft-365-copilot-with-mcp/)
- [构建 MCP 插件（Learn）](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/build-mcp-plugins)
- [API 插件适配卡片（Learn）](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api-plugin-adaptive-cards)
- [管理 Copilot 代理（Learn）](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-copilot-agents-integrated-apps)

### 工具与 SDK
- Microsoft 365 代理工具包（VS Code 扩展 v6.3.x+）
- 代理打包的 Teams 工具包
- 适配卡片设计器
- MCP 规范文档

### 合作伙伴示例
- monday.com: 任务管理集成
- Canva: 设计自动化
- Sitecore: 内容管理


---
description: 专为 Microsoft 365 Copilot 声明式代理开发的完整工具包，包含三个全面的工作流（基础、高级、验证）、TypeSpec 支持以及 Microsoft 365 Agents Toolkit 集成
---

# Microsoft 365 声明式代理开发工具包

我将帮助您使用最新的 v1.5 架构创建和开发 Microsoft 365 Copilot 声明式代理，提供全面的 TypeSpec 支持和 Microsoft 365 Agents Toolkit 集成。您可以选择以下三种专用工作流之一：

## 工作流 1：基础代理创建
**适用于**：新开发者、简单代理、快速原型

我将引导您完成以下步骤：
1. **代理规划**：定义代理的目的、目标用户和核心功能
2. **能力选择**：从 11 种可用能力中选择（网络搜索、OneDrive 和 SharePoint、Graph 连接器等）
3. **基础架构创建**：生成符合规范的 JSON 制定文件并确保适当约束
4. **TypeSpec 替代方案**：创建现代类型安全定义，可编译为 JSON
5. **测试设置**：配置 Agents Playground 以进行本地测试
6. **工具包集成**：利用 Microsoft 365 Agents Toolkit 实现增强开发

## 工作流 2：高级企业代理设计
**适用于**：复杂的企业场景、生产部署、高级功能

我将协助您进行架构设计：
1. **企业需求分析**：多租户考虑、合规性、安全性
2. **高级能力配置**：复杂能力组合与交互
3. **行为覆盖实现**：自定义响应模式和专用行为
4. **本地化策略**：多语言支持与资源管理
5. **对话启动器**：为用户互动设计战略对话入口
6. **生产部署**：环境管理、版本控制和生命周期规划
7. **监控与分析**：实现跟踪和性能优化

## 工作流 3：验证与优化
**适用于**：现有代理、故障排查、性能优化

我将执行以下操作：
1. **架构合规性验证**：全面检查 v1.5 规范符合性
2. **字符限制优化**：名称（100 字）、描述（1000 字）、指令（8000 字）
3. **能力审计**：验证能力配置和使用是否恰当
4. **TypeSpec 迁移**：将现有 JSON 转换为现代 TypeSpec 定义
5. **测试协议**：使用 Agents Playground 进行全面验证
6. **性能分析**：识别瓶颈并寻找优化机会
7. **最佳实践审查**：与 Microsoft 指南和建议对齐

## 所有工作流共有的核心功能

### Microsoft 365 Agents Toolkit 集成
- **VS Code 插件**：与 `teamsdevapp.ms-teams-vscode-extension` 完全集成
- **TypeSpec 开发**：现代类型安全代理定义
- **本地调试**：与 Agents Playground 集成用于测试
- **环境管理**：开发、预发布、生产配置
- **生命周期管理**：创建、测试、部署、监控

### TypeSpec 示例
```typespec
// 现代声明式代理定义
模型 MyAgent {
  名称: 字符串;
  描述: 字符串;
  指令: 字符串;
  能力: AgentCapability[];
  对话启动器?: ConversationStarter[];
}
```

### JSON Schema v1.5 验证
- 完全符合最新 Microsoft 规范
- 强制执行字符限制（名称：100 字，描述：1000 字，指令：8000 字）
- 数组约束验证（对话启动器：最多 4 个，能力：最多 5 个）
- 必填字段验证和类型检查

### 可用能力（最多选择 5 个）
1. **网络搜索**：互联网搜索功能
2. **OneDrive 和 SharePoint**：文件及内容访问
3. **Graph 连接器**：企业数据集成
4. **Microsoft Graph**：Microsoft 365 服务集成
5. **Teams 和 Outlook**：通信平台访问
6. **PowerPlatform**：Power Apps 和 Power Automate 集成
7. **企业数据处理**：企业数据分析
8. **Word 和 Excel**：文档和电子表格操作
9. **Microsoft 365 Copilot**：高级 Copilot 功能
10. **企业应用**：第三方系统集成
11. **自定义连接器**：自定义 API 和服务集成

### 环境变量支持
```json
{
  "名称": "${AGENT_NAME}",
  "描述": "${AGENT_DESCRIPTION}",
  "指令": "${AGENT_INSTRUCTIONS}"
}
```

**您想从哪个工作流开始？** 请分享您的需求，我将为您提供针对 Microsoft 365 Copilot 声明式代理开发的专门指导，全面支持 TypeSpec 和 Microsoft 365 Agents Toolkit。
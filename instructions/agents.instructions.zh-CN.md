

---
描述：'为 GitHub Copilot 创建自定义代理文件的指南'
适用范围：'**/*.agent.md'
---

# 自定义代理文件指南

为创建高效且可维护的自定义代理文件，以提供特定开发任务的专业知识的指导。

## 项目背景

- 目标受众：为 GitHub Copilot 创建自定义代理的开发者
- 文件格式：带有 YAML 前置信息的 Markdown 格式
- 文件命名规范：小写加连字符（例如：`test-specialist.agent.md`）
- 存储位置：`.github/agents/` 目录（仓库级别）或 `agents/` 目录（组织/企业级别）
- 目的：定义具有定制专业知识、工具和指令的特定任务代理
- 官方文档：https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents

## 必需的前置信息

每个代理文件必须包含 YAML 前置信息，包含以下字段：

```yaml
---
描述: '代理目的和功能的简要说明'
名称: '代理的显示名称'
工具: ['读取', '编辑', '搜索']
模型: 'Claude Sonnet 4.5'
目标: 'vscode'
推断: true
---
```

### 核心前置信息属性

#### **描述**（必需）
- 单引号字符串，明确说明代理的目的和专业领域
- 应简洁（50-150 字符）且具有行动导向
- 示例：'专注于测试覆盖率、质量及测试最佳实践'

#### **名称**（可选）
- 代理在 UI 中的显示名称
- 若省略，默认使用文件名（不含 `.md` 或 `.agent.md`）
- 使用标题格式并描述性命名
- 示例：'Testing Specialist'

#### **工具**（可选）
- 代理可以使用的工具名称或别名列表
- 支持逗号分隔字符串或 YAML 数组格式
- 若省略，代理可以使用所有可用工具
- 详见下方的“工具配置”部分

#### **模型**（强烈推荐）
- 指定代理应使用的 AI 模型
- 支持 VS Code、JetBrains IDEs、Eclipse 和 Xcode
- 示例：'Claude Sonnet 4.5'，'gpt-4'，'gpt-4o'
- 根据代理复杂度和所需功能选择

#### **目标**（可选）
- 指定目标环境：'vscode' 或 'github-copilot'
- 若省略，代理可在两种环境中使用
- 当代理具有环境特定功能时使用

#### **推断**（可选）
- 布尔值，控制 Copilot 是否根据上下文自动使用此代理
- 默认：若省略则为 true
- 设置为 false 时需手动选择代理

#### **元数据**（可选，仅限 GitHub.com）
- 用于代理注释的名称值对对象
- 示例：`元数据: { 类别: '测试', 版本: '1.0' }`
- 不支持 VS Code

#### **mcp-servers**（可选，仅限组织/企业）
- 配置仅对本代理可用的 MCP 服务器
- 仅支持组织/企业级别的代理
- 详见下方的“MCP 服务器配置”部分

## 工具配置

### 工具规格策略

**启用所有工具**（默认）：
```yaml
# 完全省略 tools 属性，或使用：
工具: ['*']
```

**启用特定工具**：
```yaml
工具: ['读取', '编辑', '搜索', '执行']
```

**启用 MCP 服务器工具**：
```yaml
工具: ['读取', '编辑', 'github/*', 'playwright/navigate']
```

**禁用所有工具**：
```yaml
工具: []
```

### 标准工具别名

所有别名不区分大小写：

| 别名 | 替代名称 | 类别 | 描述 |
|-------|------------------|----------|-------------|
| `执行` | shell, Bash, powershell | shell 执行 | 在适当的 shell 中执行命令 |
| `读取` | 读取, NotebookRead, 查看 | 文件读取 | 读取文件内容 |
| `编辑` | 编辑, 多编辑, 写入, NotebookEdit | 文件编辑 | 编辑和修改文件 |
| `搜索` | Grep, Glob, 搜索 | 代码搜索 | 在文件或文件夹中搜索文本 |
| `代理` | custom-agent, 任务 | 代理调用 | 调用其他自定义代理 |
| `网络` | WebSearch, WebFetch | 网络访问 | 获取网络内容和搜索 |
| `待办` | TodoWrite | 任务管理 | 创建和管理任务列表（仅限 VS Code） |

### 内置 MCP 服务器工具

**GitHub MCP 服务器**：
```yaml
工具: ['github/*']  # 所有 GitHub 工具
工具: ['github/get_file_contents', 'github/search_repositories']  # 特定工具
```
- 默认提供所有只读工具
- 令牌作用域限定于源仓库

**Playwright MCP 服务器**：
```yaml
工具: ['playwright/*']  # 所有 Playwright 工具
工具: ['playwright/navigate', 'playwright/screenshot']  # 特定工具
```
- 配置为仅访问本地主机
- 适用于浏览器自动化和测试

### 工具选择最佳实践

- **最小权限原则**：仅启用代理所需工具
- **安全性**：除非明确需要，否则限制 `执行` 访问
- **专注**：工具越少，代理目的越清晰，性能越好
- **文档**：对复杂配置的指令进行注释说明为何需要特定工具

## 子代理调用（代理编排）

代理可以通过 `runSubagent` 调用其他代理，以编排多步骤工作流。

### 工作原理

将 `代理` 添加到工具列表中以启用子代理调用：

```yaml
工具: ['读取', '编辑', '搜索', '代理']
```

然后通过 `runSubagent` 调用其他代理：

```javascript
const result = await runSubagent({
  描述: '此步骤的作用',
  提示: `你是 [Specialist] 专家。

上下文：
- 参数: ${parameterValue}
- 输入: ${inputPath}
- 输出: ${outputPath}

任务：
1. 执行具体工作
2. 将结果写入输出位置
3. 返回完成摘要`
});
```

### 基本模式

为每个子代理调用构建结构：

1. **描述**：子代理调用的清晰单行目的
2. **提示**：包含替换变量的详细指令

提示应包括：
- 子代理的角色（专家角色）
- 所需的上下文（参数、路径）
- 执行的任务（具体操作）
- 输出位置
- 返回的内容（摘要）

### 示例：多步骤处理

```javascript
// 步骤 1：处理数据
const processing = await runSubagent({
  描述: '转换原始输入数据',
  提示: `你是文档专家。

项目: ${projectName}
输入: ${basePath}/src/
输出: ${basePath}/docs/

任务：
1. 从 ${inputPath} 读取源文件
2. 根据项目配置处理文件
3. 写入结果到 ${outputPath}/index.md
4. 包含代码示例和使用指南

返回：生成的文档摘要（文件数量、字数）`
});

// 步骤 2：分析（依赖步骤 1）
const analysis = await runSubagent({
  描述: '分析处理后的数据',
  提示: `你是测试覆盖率专家。

项目: ${projectName}
PR: ${prNumber}
更改内容: ${basePath}/changes/

任务：
1. 分析修改文件的代码覆盖率
2. 识别未测试的关键路径
3. 将报告写入 ${basePath}/coverage-report.md

返回：当前覆盖率百分比和缺失部分`
});

// 步骤 3：汇总结果
const finalReport = await runSubagent({
  描述: '汇总所有审查结果',
  提示: `你是审查汇总专家。

项目: ${projectName}
报告: ${basePath}/*.md

任务：
1. 从 ${basePath}/ 读取所有审查报告
2. 合并结果为单个报告
3. 确定总体结论（批准/需要修复/阻塞）
4. 写入 ${basePath}/final-review.md

返回：最终结论和执行摘要`
});

return finalReport;
```

此模式适用于任何编排场景：提取变量，使用清晰上下文调用子代理，等待结果。

### 变量最佳实践

#### 1. **清晰文档**
始终记录预期的变量：

```markdown
## 必需变量
- **projectName**：项目名称（字符串，必需）
- **basePath**：项目文件根目录（路径，必需）

## 可选变量
- **mode**：处理模式 - 快速/标准/详细（枚举，默认：标准）
- **outputFormat**：输出格式 - markdown/json/html（枚举，默认：markdown）

## 派生变量
- **outputDir**：自动设置为 ${basePath}/output
- **logFile**：自动设置为 ${basePath}/.log.md
```

#### 2. **一致命名**
使用一致的变量命名规范：

```javascript
// 好：清晰、描述性命名
const variables = {
  projectName,          // 要处理的项目名称
  basePath,            // 项目文件所在路径
  outputDirectory,     // 保存结果的目录
  processingMode,      // 处理方式（详细程度）
  configurationPath    // 配置文件所在路径
};

// 避免：模糊或不一致
const bad_variables = {
  name,     // 太通用
  path,     // 不明确是哪个路径
  mode,     // 太短
  config    // 太模糊
};
```

#### 3. **验证和约束**
记录有效值和约束条件：

```markdown
## 变量约束

**projectName**：
- 类型：字符串（允许字母数字、连字符、下划线）
- 长度：1-100 个字符
- 必需：是
- 模式：`/^[a-zA-Z0-9_-]+$/

**processingMode**：
- 类型：枚举
- 有效值："快速"（< 5 分钟）、"标准"（5-15 分钟）、"详细"（15 分钟以上）
- 默认："标准"
- 必需：否
```

## MCP 服务器配置（仅限组织/企业）

MCP 服务器通过额外工具扩展代理功能。仅支持组织和企业级别的代理。

### 配置格式

```yaml
---
名称: my-custom-agent
描述: '支持 MCP 集成的代理'
工具: ['读取', '编辑', 'custom-mcp/tool-1']
mcp-servers:
  custom-mcp:
    类型: '本地'
    命令: 'some-command'
    参数: ['--arg1', '--arg2']
    工具: ["*"]
    环境变量:
      ENV_VAR_NAME: ${{ secrets.API_KEY }}
---
```

### MCP 服务器属性

- **类型**：服务器类型（'本地' 或 'stdio'）
- **命令**：启动 MCP 服务器的命令
- **参数**：命令参数数组
- **工具**：从该服务器启用的工具（["*"] 表示全部）
- **环境变量**：环境变量（支持密钥）

### 环境变量和密钥

密钥必须在仓库设置的 "copilot" 环境中配置。

**支持的语法**：
```yaml
环境变量:
  # 仅环境变量
  VAR_NAME: COPILOT_MCP_ENV_VAR_VALUE

  # 带有头信息的变量
  VAR_NAME: $COPILOT_MCP_ENV_VAR_VALUE
  VAR_NAME: ${COPILOT_MCP_ENV_VAR_VALUE}

  # GitHub Actions 风格（仅限 YAML）
  VAR_NAME: ${{ secrets.COPILOT_MCP_ENV_VAR_VALUE }}
  VAR_NAME: ${{ var.COPILOT_MCP_ENV_VAR_VALUE }}
```

## 文件组织和命名

### 仓库级别代理
- 存储位置：`.github/agents/`
- 作用域：仅限特定仓库
- 访问权限：使用仓库配置的 MCP 服务器

### 组织/企业级别代理
- 存储位置：`.github-private/agents/`（然后移动到 `agents/` 根目录）
- 作用域：在组织/企业内的所有仓库中可用
- 访问权限：可以配置专用 MCP 服务器

### 命名规范
- 使用小写加连字符：`test-specialist.agent.md`
- 名称应反映代理的目的
- 文件名成为默认代理名称（若未指定 `名称`）
- 允许的字符：`.`, `-`, `_`, `a-z`, `A-Z`, `0-9`

## 代理处理和行为

### 版本控制
- 基于代理文件的 Git 提交 SHA 值
- 为不同代理版本创建分支/标签
- 使用最新版本实例化仓库/分支
- PR 交互使用相同代理版本以确保一致性

### 名称冲突
优先级（从高到低）：
1. 仓库级别代理
2. 组织级别代理
3. 企业级别代理

同名的低级别配置会覆盖高级别配置。

### 工具处理
- `工具` 列表过滤可用工具（内置和 MCP）
- 未指定工具 = 启用所有工具
- 空列表（[]）= 禁用所有工具
- 特定列表 = 仅启用这些工具
- 未识别的工具名称会被忽略（允许环境特定工具）

### MCP 服务器处理顺序
1. 开箱即用的 MCP 服务器（例如：GitHub MCP）
2. 自定义代理 MCP 配置（仅限组织/企业）
3. 仓库级别 MCP 配置

每个层级都可以覆盖前一层级的设置。

## 代理创建检查清单

### 前置信息
- [ ] `描述` 字段存在且描述清晰（50-150 字符）
- [ ] `描述` 使用单引号包裹
- [ ] 指定 `名称`（可选但推荐）
- [ ] `工具` 配置适当（或有意省略）
- [ ] 指定 `模型` 以优化性能
- [ ] 若代理环境特定，设置 `目标`
- [ ] 若需手动选择代理，将 `推断` 设置为 `false`

### 提示内容
- [ ] 明确代理身份和角色
- [ ] 明确列出核心职责
- [ ] 解释方法和流程
- [ ] 指定指南和约束条件
- [ ] 文档化输出期望
- [ ] 在需要时提供示例
- [ ] 指令具体且可操作
- [ ] 明确定义作用域和边界
- [ ] 总内容不超过 30,000 字符

### 文件结构
- [ ] 文件名遵循小写带连字符的规范
- [ ] 文件放置在正确目录（`.github/agents/` 或 `agents/`）
- [ ] 文件名仅使用允许的字符
- [ ] 文件扩展名为 `.agent.md`

### 质量检查
- [ ] 代理目的独特且不重复
- [ ] 工具最少且必要
- [ ] 指令清晰且无歧义
- [ ] 代理已通过代表性任务测试
- [ ] 文档引用为最新
- [ ] 已处理安全考虑（如适用）

## 常见代理模式

### 测试专家
**目的**：专注于测试覆盖率和质量
**工具**：所有工具（用于全面测试创建）
**方法**：分析、识别差距、编写测试、避免修改生产代码

### 实现规划者
**目的**：创建详细的技术计划和规范
**工具**：仅限 `['读取', '搜索', '编辑']`
**方法**：分析需求、创建文档、避免实现

### 代码审查员
**目的**：审查代码质量并提供反馈
**工具**：仅限 `['读取', '搜索']`
**方法**：分析、建议改进、不直接修改代码

### 重构专家
**目的**：改进代码结构和可维护性
**工具**：`['读取', '搜索', '编辑']`
**方法**：分析模式、提出重构建议、安全实施

### 安全审计员
**目的**：识别安全问题和漏洞
**工具**：`['读取', '搜索', '网络']`
**方法**：扫描代码、检查 OWASP、报告发现

## 常见错误避免

### 前置信息错误
- ❌ 缺少 `描述` 字段
- ❌ 描述未用引号包裹
- ❌ 使用未检查文档的无效工具名称
- ❌ YAML 语法错误（缩进、引号）

### 工具配置问题
- ❌ 不必要地授予过多工具访问权限
- ❌ 缺少代理所需工具
- ❌ 未一致使用工具别名
- ❌ 忽略 MCP 服务器命名空间（server-name/tool）

### 提示内容问题
- ❌ 模糊、有歧义的指令
- ❌ 冲突或矛盾的指南
- ❌ 缺乏明确的作用域定义
- ❌ 缺少输出期望
- ❌ 指令过于冗长（超出字符限制）
- ❌ 复杂任务缺少示例或上下文

### 组织问题
- ❌ 文件名未反映代理目的
- ❌ 目录错误（混淆仓库与组织级别）
- ❌ 文件名使用空格或特殊字符
- ❌ 重复代理名称导致冲突

## 测试和验证

### 手动测试
1. 创建包含正确前置信息的代理文件
2. 重新加载 VS Code 或刷新 GitHub.com
3. 从 Copilot 聊天的下拉菜单中选择代理
4. 使用代表性用户查询进行测试
5. 验证工具访问是否按预期工作
6. 确认输出是否符合预期

### 集成测试
- 在作用域内的不同文件类型中测试代理
- 验证 MCP 服务器连接（如配置）
- 检查代理在缺少上下文时的行为
- 测试错误处理和边界情况
- 验证代理切换和交接

### 质量检查
- 运行代理创建检查清单
- 审查常见错误列表
- 与仓库中的示例代理进行比较
- 对复杂代理进行同行评审
- 文档化任何特殊配置需求

## 其他资源

### 官方文档
- [创建自定义代理](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)
- [自定义代理配置](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [VS Code 中的自定义代理](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [MCP 集成](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/extend-coding-agent-with-mcp)

### 社区资源
- [Awesome Copilot 代理集合](https://github.com/github/awesome-copilot/tree/main/agents)
- [自定义库示例](https://docs.github.com/en/copilot/tutorials/customization-library/custom-agents)
- [你的第一个自定义代理教程](https://docs.github.com/en/copilot/tutorials/customization-library/custom-agents/your-first-custom-agent)

### 相关文件
- [提示文件指南](./prompt.instructions.md) - 用于创建提示文件
- [指令文件指南](./instructions.instructions.md) - 用于创建指令文件

## 版本兼容性说明

### GitHub.com（编码代理）
- ✅ 完全支持所有标准前置信息属性
- ✅ 仓库和组织/企业级别的代理
- ✅ MCP 服务器配置（组织/企业）
- ❌ 不支持 `模型`、`argument-hint`、`handoffs` 属性

### VS Code / JetBrains / Eclipse / Xcode
- ✅ 支持 `模型` 属性以选择 AI 模型
- ✅ 支持 `argument-hint` 和 `handoffs` 属性
- ✅ 支持用户配置文件和工作区级别的代理
- ❌ 无法在仓库级别配置 MCP 服务器
- ⚠️ 某些属性可能在不同环境中表现不同

在为多个环境创建代理时，专注于通用属性并测试所有目标环境。必要时使用 `目标` 属性创建环境特定代理。
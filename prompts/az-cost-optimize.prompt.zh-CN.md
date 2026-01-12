

---
agent: 'agent'
description: '分析应用程序中使用的 Azure 资源（IaC 文件和/或目标 rg 中的资源），并生成成本优化建议 - 为每个发现的优化机会创建 GitHub 问题。'
---

# Azure 成本优化

此工作流分析基础设施即代码（IaC）文件和 Azure 资源，以生成成本优化建议。它会为每个优化机会创建独立的 GitHub 问题，并创建一个 EPIC 问题以协调实施，从而实现成本节约计划的高效跟踪和执行。

## 前提条件
- 配置并认证 Azure MCP 服务器
- 配置并认证 GitHub MCP 服务器  
- 确定目标 GitHub 仓库
- 部署 Azure 资源（IaC 文件可选但有助于分析）
- 优先使用 Azure MCP 工具（`azmcp-*`）而不是直接使用 Azure CLI（如有可用）

## 工作流步骤

### 步骤 1：获取 Azure 最佳实践
**操作**：在分析之前检索成本优化最佳实践
**工具**：Azure MCP 最佳实践工具
**流程**：
1. **加载最佳实践**：
   - 执行 `azmcp-bestpractices-get` 以获取部分最新的 Azure 优化指南。这可能不涵盖所有场景，但提供了基础。
   - 尽可能使用这些最佳实践来指导后续分析和建议
   - 在优化建议中引用最佳实践，无论是来自 MCP 工具输出还是通用 Azure 文档

### 步骤 2：发现 Azure 基础设施
**操作**：动态发现并分析 Azure 资源和配置
**工具**：Azure MCP 工具 + Azure CLI 作为备用 + 本地文件系统访问
**流程**：
1. **资源发现**：
   - 执行 `azmcp-subscription-list` 以查找可用的订阅
   - 执行 `azmcp-group-list --subscription <subscription-id>` 以查找资源组
   - 获取相关资源组中所有资源的列表：
     - 使用 `az resource list --subscription <id> --resource-group <name>`
   - 对于每种资源类型，优先使用 MCP 工具，然后使用 CLI 作为备用：
     - `azmcp-cosmos-account-list --subscription <id>` - Cosmos DB 账户
     - `azmcp-storage-account-list --subscription <id>` - 存储账户  
     - `azmcp-monitor-workspace-list --subscription <id>` - Log Analytics 工作区
     - `azmcp-keyvault-key-list` - 密钥保管库
     - `az webapp list` - Web 应用（备用 - 没有 MCP 工具可用）
     - `az appservice plan list` - 应用服务计划（备用）
     - `az functionapp list` - 函数应用（备用）
     - `az sql server list` - SQL 服务器（备用）
     - `az redis list` - Redis 缓存（备用）
     - ... 其他资源类型的类似操作

2. **IaC 检测**：
   - 使用 `file_search` 扫描 IaC 文件： "**/*.bicep", "**/*.tf", "**/main.json", "**/*template*.json"
   - 解析资源定义以理解预期配置
   - 将发现的资源与实际资源进行对比以识别差异
   - 记录 IaC 文件的存在以供后续实施建议使用
   - **不要使用仓库中的其他文件**，仅使用 IaC 文件。使用其他文件是**不允许的**，因为它们不是真实来源。
   - 如果未找到 IaC 文件，则**停止**并报告未找到 IaC 文件给用户。

3. **配置分析**：
   - 提取每种资源的当前 SKU、层级和设置
   - 识别资源之间的关系和依赖
   - 映射可用的资源使用模式

### 步骤 3：收集使用指标并验证当前成本
**操作**：收集使用数据并验证实际资源成本
**工具**：Azure MCP 监控工具 + Azure CLI
**流程**：
1. **查找监控源**：
   - 使用 `azmcp-monitor-workspace-list --subscription <id>` 查找 Log Analytics 工作区
   - 使用 `azmcp-monitor-table-list --subscription <id> --workspace <name> --table-type "CustomLog"` 发现可用数据

2. **执行使用查询**：
   - 使用 `azmcp-monitor-log-query` 执行这些预定义查询：
     - 查询： "recent" 用于最近的活动模式
     - 查询： "errors" 用于指示问题的错误日志
   - 对于自定义分析，使用 KQL 查询：
   ```kql
   // App Service 的 CPU 使用率
   AppServiceAppLogs
   | where TimeGenerated > ago(7d)
   | summarize avg(CpuTime) by Resource, bin(TimeGenerated, 1h)
   
   // Cosmos DB 的 RU 消耗  
   AzureDiagnostics
   | where ResourceProvider == "MICROSOFT.DOCUMENTDB"
   | where TimeGenerated > ago(7d)
   | summarize avg(RequestCharge) by Resource
   
   // 存储账户的访问模式
   StorageBlobLogs
   | where TimeGenerated > ago(7d)
   | summarize RequestCount=count() by AccountName, bin(TimeGenerated, 1d)
   ```

3. **计算基准指标**：
   - CPU/内存使用率的平均值
   - 数据库吞吐量模式
   - 存储访问频率
   - 函数执行率

4. **验证当前成本**： 
   - 使用步骤 2 中发现的 SKU/层级配置
   - 通过 https://azure.microsoft.com/pricing/ 或 `az billing` 命令查找当前 Azure 定价
   - 记录：资源 → 当前 SKU → 估算月成本
   - 在继续建议之前计算现实的当前月总成本

### 步骤 4：生成成本优化建议
**操作**：分析资源以识别优化机会
**工具**：使用收集的数据进行本地分析
**流程**：
1. **基于发现的资源类型应用优化模式**：
   
   **计算优化**：
   - 应用服务计划：根据 CPU/内存使用率进行调整
   - 函数应用：对于低使用率，将 Premium 计划改为 Consumption 计划
   - 虚拟机：缩减超大实例
   
   **数据库优化**：
   - Cosmos DB： 
     - 将托管模式改为无服务器模式以适应可变工作负载
     - 根据实际使用量调整 RU/s
   - SQL 数据库：根据 DTU 使用量调整服务层级
   
   **存储优化**：
   - 实施生命周期策略（热 → 冷 → 归档）
   - 合并冗余的存储账户
   - 根据访问模式调整存储层级
   
   **基础设施优化**：
   - 移除未使用的/冗余的资源
   - 在合适的地方实施自动扩展
   - 安排非生产环境的调度

2. **计算基于证据的节省**： 
   - 当前验证成本 → 目标成本 = 节省
   - 记录当前和目标配置的定价来源

3. **计算每个建议的优先级评分**：
   ```
   优先级评分 = (价值评分 × 每月节省) / (风险评分 × 实施天数)
   
   高优先级：评分 > 20
   中优先级：评分 5-20
   低优先级：评分 < 5
   ```

4. **验证建议**：
   - 确保 Azure CLI 命令准确
   - 验证估算节省的计算
   - 评估实施风险和前提条件
   - 确保所有节省计算都有支持证据

### 步骤 5：用户确认
**操作**：展示摘要并获取批准后再创建 GitHub 问题
**流程**：
1. **显示优化摘要**：
   ```
   🎯 Azure 成本优化摘要
   
   📊 分析结果：
   • 分析的资源总数：X
   • 当前月成本：$X 
   • 潜在月节省：$Y 
   • 优化机会：Z
   • 高优先级项目：N
   
   🏆 建议：
   1. [资源]: [当前 SKU] → [目标 SKU] = $X/月节省 - [风险等级] | [实施工作量]
   2. [资源]: [当前配置] → [目标配置] = $Y/月节省 - [风险等级] | [实施工作量]
   3. [资源]: [当前配置] → [目标配置] = $Z/月节省 - [风险等级] | [实施工作量]
   ... 依此类推
   
   💡 这将创建：
   • Y 个独立的 GitHub 问题（每个优化一个）
   • 1 个 EPIC 问题以协调实施
   
   ❓ 是否继续创建 GitHub 问题？(y/n)
   ```

2. **等待用户确认**：只有在用户确认后才继续

### 步骤 6：创建独立的优化问题
**操作**：为每个优化机会创建单独的 GitHub 问题。标记为 "cost-optimization"（绿色）、"azure"（蓝色）。
**所需 MCP 工具**：为每个建议使用 `create_issue`
**流程**：
1. **使用此模板创建独立问题**：

   **标题格式**：`[COST-OPT] [资源类型] - [简要描述] - $X/月节省`
   
   **正文模板**：
   ```markdown
   ## 💰 成本优化：[简要标题]
   
   **每月节省**：$X | **风险等级**：[低/中/高] | **实施工作量**：X 天
   
   ### 📋 描述
   [清晰解释优化内容及必要性]
   
   ### 🔧 实施
   
   **检测到的 IaC 文件**：[是/否 - 基于 file_search 结果]
   
   ```bash
   # 如果检测到 IaC 文件：显示 IaC 修改 + 部署
   # 文件：infrastructure/bicep/modules/app-service.bicep
   # 修改：sku.name: 'S3' → 'B2'
   az deployment group create --resource-group [rg] --template-file infrastructure/bicep/main.bicep
   
   # 如果未检测到 IaC 文件：直接 Azure CLI 命令 + 警告
   # ⚠️ 未找到 IaC 文件。如果它们存在于其他位置，请修改那些文件。
   az appservice plan update --name [plan] --sku B2
   ```
   
   ### 📊 证据
   - 当前配置：[详细信息]
   - 使用模式：[来自监控数据的证据]
   - 成本影响：$X/月 → $Y/月
   - 最佳实践对齐：[如适用，引用 Azure 最佳实践]
   
   ### ✅ 验证步骤
   - [ ] 在非生产环境中测试
   - [ ] 验证无性能下降
   - [ ] 在 Azure 成本管理中确认成本降低
   - [ ] 如有需要，更新监控和警报
   
   ### ⚠️ 风险与注意事项
   - [风险 1 和缓解措施]
   - [风险 2 和缓解措施]
   
   **优先级评分**：X | **价值**：X/10 | **风险**：X/10
   ```

### 步骤 7：创建 EPIC 协调问题
**操作**：创建主问题以跟踪所有优化工作。标记为 "cost-optimization"（绿色）、"azure"（蓝色）、"epic"（紫色）。
**关于 mermaid 图表的注意事项**：确保验证 mermaid 语法正确，并在创建图表时考虑无障碍指南（样式、颜色等）。
**流程**：
1. **创建 EPIC 问题**：

   **标题**：`[EPIC] Azure 成本优化计划 - $X/月潜在节省`
   
   **正文模板**：
   ```markdown
   # 🎯 Azure 成本优化 EPIC
   
   **总潜在节省**：$X/月 | **实施时间线**：X 周
   
   ## 📊 执行摘要
   - **分析的资源**：X
   - **优化机会**：Y  
   - **总月节省潜力**：$X
   - **高优先级项目**：N
   
   ## 🏗️ 当前架构概览
   
   ```mermaid
   graph TB
       subgraph "资源组: [名称]"
           [生成的架构图显示当前资源和成本]
       end
   ```
   
   ## 📋 实施跟踪
   
   ### 🚀 高优先级（优先实施）
   - [ ] #[issue-number]: [标题] - $X/月节省
   - [ ] #[issue-number]: [标题] - $X/月节省
   
   ### ⚡ 中优先级 
   - [ ] #[issue-number]: [标题] - $X/月节省
   - [ ] #[issue-number]: [标题] - $X/月节省
   
   ### 🔄 低优先级（可选）
   - [ ] #[issue-number]: [标题] - $X/月节省
   
   ## 📈 进度跟踪
   - **已完成**：Y 个优化中的 0 个
   - **已实现节省**：$0/月（总 $X/月）
   - **实施状态**：未开始
   
   ## 🎯 成功标准
   - [ ] 所有高优先级优化已实施
   - [ ] 实现了超过 80% 的估算节省
   - [ ] 未观察到性能下降
   - [ ] 成本监控仪表板已更新
   
   ## 📝 备注
   - 在问题完成时审查和更新此 EPIC
   - 监控实际节省与估算节省的差异
   - 考虑定期安排成本优化审查
   ```

## 错误处理
- **成本验证**：如果节省估算缺乏支持证据或与 Azure 定价不一致，实施前需重新验证配置和定价来源
- **Azure 认证失败**：提供手动 Azure CLI 设置步骤
- **未找到资源**：创建关于 Azure 资源部署的信息性问题
- **GitHub 创建失败**：将格式化的建议输出到控制台
- **使用数据不足**：说明限制并仅提供基于配置的建议

## 成功标准
- ✅ 所有成本估算已验证实际资源配置和 Azure 定价
- ✅ 为每个优化创建了独立问题（可跟踪和分配）
- ✅ EPIC 问题提供了全面的协调和跟踪
- ✅ 所有建议包含具体的、可执行的 Azure CLI 命令
- ✅ 优先级评分支持以投资回报率为导向的实施
- ✅ 架构图准确反映当前状态
- ✅ 用户确认防止不必要的问题创建
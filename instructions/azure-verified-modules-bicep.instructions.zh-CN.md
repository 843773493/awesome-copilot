

---
description: 'Azure 验证模块（AVM）和 Bicep'
applyTo: '**/*.bicep, **/*.bicepparam'
---

# Azure 验证模块（AVM）Bicep

## 概述

Azure 验证模块（AVM）是遵循 Azure 最佳实践的预构建、测试和验证的 Bicep 模块。使用这些模块可以放心地创建、更新或审查 Azure 基础设施即代码（IaC）。

## 模块发现

### Bicep 公共注册表

- 搜索模块：`br/public:avm/res/{service}/{resource}:{version}`
- 浏览可用模块：`https://github.com/Azure/bicep-registry-modules/tree/main/avm/res`
- 示例：`br/public:avm/res/storage/storage-account:0.30.0`

### 官方 AVM 索引

- **Bicep 资源模块**：`https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/BicepResourceModules.csv`
- **Bicep 模式模块**：`https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/BicepPatternModules.csv`

### 模块文档

- **GitHub 仓库**：`https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}`
- **README**：每个模块都包含详细的文档和示例

## 模块使用

### 从示例中使用

1. 查看 `https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}` 中的模块 README
2. 从模块文档中复制示例代码
3. 使用 `br/public:avm/res/{service}/{resource}:{version}` 引用模块
4. 配置必需参数和可选参数

### 示例用法

```bicep
module storageAccount 'br/public:avm/res/storage/storage-account:0.30.0' = {
  name: 'storage-account-deployment'
  scope: resourceGroup()
  params: {
    name: storageAccountName
    location: location
    skuName: 'Standard_LRS'
    tags: tags
  }
}
```

### 当 AVM 模块不可用时

如果不存在 AVM 模块，请使用最新稳定 API 版本的原生 Bicep 资源声明。

## 命名规范

### 模块引用

- **资源模块**：`br/public:avm/res/{service}/{resource}:{version}`
- **模式模块**：`br/public:avm/ptn/{pattern}:{version}`
- 示例：`br/public:avm/res/network/virtual-network:0.7.2`

### 符号名称

- 所有名称（变量、参数、资源、模块）均使用 lowerCamelCase 格式
- 使用资源类型描述性名称（例如：`storageAccount` 而不是 `storageAccountName`）
- 避免在符号名称中使用 'name' 后缀，因为它们表示资源本身，而非资源名称
- 避免通过后缀区分变量和参数

## 版本管理

### 版本固定最佳实践

- 始终固定到特定模块版本：`:{version}`
- 使用语义化版本（例如：`:0.30.0`）
- 升级前查看模块变更日志
- 首先在非生产环境中测试版本升级

## 开发最佳实践

### 模块发现和使用

- ✅ **始终**在创建原始资源之前检查是否存在 AVM 模块
- ✅ **实施前**审查模块文档和示例
- ✅ **显式固定**模块版本
- ✅ **使用**模块中的类型（从模块导入类型）
- ✅ **优先使用**AVM 模块而非原始资源声明

### 代码结构

- ✅ **在文件顶部声明**参数并使用 `@sys.description()` 注释
- ✅ **为命名参数指定** `@minLength()` 和 `@maxLength()`
- ✅ **谨慎使用** `@allowed()` 注释，避免阻止有效部署
- ✅ **为测试环境设置**安全的默认值（低成本 SKU）
- ✅ **使用变量**处理复杂表达式，而非直接嵌入资源属性
- ✅ **使用** `loadJsonContent()` 处理外部配置文件

### 资源引用

- ✅ **使用符号名称**（例如：`storageAccount.id`）而非 `reference()` 或 `resourceId()`
- ✅ **通过符号名称创建**依赖关系，而非显式 `dependsOn`
- ✅ **使用** `existing` 关键字访问其他资源的属性
- ✅ **通过点符号访问**模块输出（例如：`storageAccount.outputs.resourceId`）

### 资源命名

- ✅ **使用** `uniqueString()` 与有意义的前缀生成唯一名称
- ✅ **添加前缀**，因为某些资源不允许以数字开头
- ✅ **遵守资源特定的命名限制**（长度、字符）

### 子资源

- ✅ **避免**过度嵌套子资源
- ✅ **使用** `parent` 属性或嵌套结构，而非手动构造名称

### 安全性

- ❌ **永远不要**在输出中包含机密或密钥
- ✅ **直接使用资源属性**在输出中（例如：`storageAccount.outputs.primaryBlobEndpoint`）
- ✅ **尽可能启用**托管身份
- ✅ **在启用网络隔离时**禁用公共访问

### 类型

- ✅ **在可用时从模块导入**类型：`import { deploymentType } from './module.bicep'`
- ✅ **使用用户定义的类型**处理复杂参数结构
- ✅ **利用类型推断**处理变量

### 文档

- ✅ **为复杂逻辑添加**有帮助的 `//` 注释
- ✅ **在所有参数上使用** `@sys.description()` 并提供清晰解释
- ✅ **记录**非显而易见的设计决策

## 验证要求

### 构建验证（必需）

在对 Bicep 文件进行任何更改后，运行以下命令以确保所有文件成功构建：

```shell
# 确保 Bicep CLI 已更新
az bicep upgrade

# 构建并验证更改的 Bicep 文件
az bicep build --file main.bicep
```

### Bicep 参数文件

- ✅ **始终**在修改 `*.bicep` 文件时更新配套的 `*.bicepparam` 文件
- ✅ **验证**参数文件与当前参数定义匹配
- ✅ **在提交前**使用参数文件测试部署

## 工具集成

### 使用可用工具

- **架构信息**：使用 `azure_get_schema_for_Bicep` 获取资源架构
- **部署指南**：使用 `azure_get_deployment_best_practices` 工具
- **服务文档**：使用 `microsoft.docs.mcp` 获取 Azure 服务特定指南

### GitHub Copilot 集成

在使用 Bicep 时：

1. 在创建资源前检查是否存在 AVM 模块
2. 使用官方模块示例作为起点
3. 在所有更改后运行 `az bicep build`
4. 更新配套的 `.bicepparam` 文件
5. 文档自定义或偏离示例的情况

## 故障排除

### 常见问题

1. **模块版本**：在模块引用中始终指定确切版本
2. **缺少依赖项**：确保在依赖模块之前创建资源
3. **验证失败**：运行 `az bicep build` 以识别语法/类型错误
4. **参数文件**：在参数更改时确保更新 `.bicepparam` 文件

### 支持资源

- **AVM 文档**：`https://azure.github.io/Azure-Verified-Modules/`
- **Bicep 注册表**：`https://github.com/Azure/bicep-registry-modules`
- **Bicep 文档**：`https://learn.microsoft.com/azure/azure-resource-manager/bicep/`
- **最佳实践**：`https://learn.microsoft.com/azure/azure-resource-manager/bicep/best-practices`

## 合规性检查清单

在提交任何 Bicep 代码前：

- [ ] 在可用时使用 AVM 模块
- [ ] 固定模块版本
- [ ] 代码成功构建（`az bicep build`）
- [ ] 更新配套的 `.bicepparam` 文件
- [ ] 所有参数使用 `@sys.description()`
- [ ] 使用符号名称进行引用
- [ ] 输出中不含机密
- [ ] 适当导入/定义类型
- [ ] 为复杂逻辑添加注释
- [ ] 遵循 lowerCamelCase 命名规范
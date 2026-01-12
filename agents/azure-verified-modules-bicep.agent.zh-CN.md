

---
description: "使用 Azure 验证模块 (AVM) 创建、更新或审查 Bicep 中的 Azure 基础设施即代码 (IaC)。"
name: "Azure AVM Bicep 模式"
tools: ["更改", "代码库", "编辑/编辑文件", "扩展", "获取", "查找测试文件", "GitHub 仓库", "新建", "打开简单浏览器", "问题", "运行命令", "运行任务", "运行测试", "搜索", "搜索结果", "终端最后命令", "终端选择", "测试失败", "用法", "VSCode API", "microsoft.docs.mcp", "azure_get_deployment_best_practices", "azure_get_schema_for_Bicep"]
---

# Azure AVM Bicep 模式

使用 Azure 验证模块 (AVM) 为 Bicep 强制实施 Azure 最佳实践，通过预构建的模块。

## 发现模块

- AVM 索引: `https://azure.github.io/Azure-Verified-Modules/indexes/bicep/bicep-resource-modules/`
- GitHub: `https://github.com/Azure/bicep-registry-modules/tree/main/avm/`

## 使用方法

- **示例**: 从模块文档复制内容，更新参数，固定版本
- **注册表**: 引用 `br/public:avm/res/{service}/{resource}:{version}`

## 版本控制

- MCR 端点: `https://mcr.microsoft.com/v2/bicep/avm/res/{service}/{resource}/tags/list`
- 固定到特定版本标签

## 来源

- GitHub: `https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}`
- 注册表: `br/public:avm/res/{service}/{resource}:{version}`

## 命名规范

- 资源: avm/res/{service}/{resource}
- 模式: avm/ptn/{pattern}
- 工具: avm/utl/{utility}

## 最佳实践

- 在可用的情况下始终使用 AVM 模块
- 固定模块版本
- 从官方示例开始
- 审查模块参数和输出
- 在进行更改后始终运行 `bicep lint`
- 使用 `azure_get_deployment_best_practices` 工具获取部署指导
- 使用 `azure_get_schema_for_Bicep` 工具进行架构验证
- 使用 `microsoft.docs.mcp` 工具查找 Azure 服务特定指导
# AzureRM Set 类型属性参考

此文档解释了 `azurerm_set_attributes.json` 的概述和维护方法。

> **最后更新时间**: 2026年1月28日

## 概述

`azurerm_set_attributes.json` 是 AzureRM Provider 中将属性视为 Set 类型的定义文件。`analyze_plan.py` 脚本通过读取此 JSON 文件来识别 Terraform 计划中的“假阳性差异”。

### 什么是 Set 类型属性？

Terraform 的 Set 类型是一种**不保证顺序**的集合。
因此，在添加或删除元素时，未发生变化的元素可能会显示为“已更改”。
这被称为“假阳性差异”。

## JSON 文件结构

### 基本格式

```json
{
  "resources": {
    "azurerm_resource_type": {
      "attribute_name": "key_attribute"
    }
  }
}
```

- **key_attribute**: 用于唯一标识 Set 元素的属性（例如 `name`、`id`）
- **null**: 当没有键属性时（比较整个元素）

### 嵌套格式

当 Set 属性包含另一个 Set 属性时：

```json
{
  "rewrite_rule_set": {
    "_key": "name",
    "rewrite_rule": {
      "_key": "name",
      "condition": "variable",
      "request_header_configuration": "header_name"
    }
  }
}
```

- **`_key`**: 该层级 Set 元素的键属性
- **其他键**: 嵌套 Set 属性的定义

### 示例：azurerm_application_gateway

```json
"azurerm_application_gateway": {
  "backend_address_pool": "name",           // 简单集合（键为名称）
  "rewrite_rule_set": {                     // 嵌套集合
    "_key": "name",
    "rewrite_rule": {
      "_key": "name",
      "condition": "variable"
    }
  }
}
```

## 维护

### 添加新属性

1. **检查官方文档**
   - 在 [Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs) 中搜索资源
   - 确认该属性被列为“Set of ...”
   - 某些资源如 `azurerm_application_gateway` 会明确标注 Set 属性

2. **检查源代码（更可靠）**
   - 在 [AzureRM Provider GitHub](https://github.com/hashicorp/terraform-provider-azurerm) 中搜索资源
   - 确认 `Type: pluginsdk.TypeSet` 在 schema 定义中
   - 识别 Set 的 `Schema` 中可以作为 `_key` 的属性

3. **添加到 JSON**
   ```json
   "azurerm_new_resource": {
     "set_attribute": "key_attribute"
   }
   ```

4. **测试**
   ```bash
   # 通过实际计划验证
   python3 scripts/analyze_plan.py your_plan.json
   ```

### 识别键属性

| 常见键属性 | 使用场景 |
|------------|----------|
| `name` | 命名块（最常见） |
| `id` | 资源 ID 引用 |
| `location` | 地理位置 |
| `address` | 网络地址 |
| `host_name` | 主机名 |
| `null` | 当没有键属性时（比较整个元素） |

## 相关工具

### analyze_plan.py

分析 Terraform 计划 JSON 文件以识别假阳性差异。

```bash
# 基本用法
terraform show -json plan.tfplan | python3 scripts/analyze_plan.py

# 从文件读取
python3 scripts/analyze_plan.py plan.json

# 使用自定义属性文件
python3 scripts/analyze_plan.py plan.json --attributes /path/to/custom.json
```

## 支持的资源

请直接参考 `azurerm_set_attributes.json` 获取当前支持的资源列表：

```bash
# 列出资源
jq '.resources | keys' azurerm_set_attributes.json
```

关键资源：
- `azurerm_application_gateway` - 后端池、监听器、规则等
- `azurerm_firewall_policy_rule_collection_group` - 规则集合
- `azurerm_frontdoor` - 后端池、路由
- `azurerm_network_security_group` - 安全规则
- `azurerm_virtual_network_gateway` - IP 配置、VPN 客户端配置

## 注意事项

- 属性行为可能因 Provider/API 版本不同而有所差异
- 需要随着新资源和属性的发布持续添加
- 定义深度嵌套结构的所有层级可提高准确性

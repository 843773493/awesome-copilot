# 预检报告模板

在项目根目录生成 `preflight-report.md` 时使用此模板结构。

---

## 模板

```markdown
# Azure 部署预检报告

**生成时间:** {timestamp}
**状态:** {overall-status}

---

## 概述

| 属性 | 值 |
|------|----|
| **模板文件** | {bicep-files} |
| **参数文件** | {param-files-or-none} |
| **项目类型** | {azd-project | standalone-bicep} |
| **部署范围** | {resourceGroup | subscription | managementGroup | tenant} |
| **目标** | {resource-group-name | subscription-name | mg-id} |
| **验证级别** | {Provider | ProviderNoRbac} |

### 验证结果

| 检查项 | 状态 | 详情 |
|--------|------|------|
| Bicep 语法 | {✅ 通过 | ❌ 失败 | ⚠️ 警告 | ⏭️ 跳过} | {details} |
| What-If 分析 | {✅ 通过 | ❌ 失败 | ⏭️ 跳过} | {details} |
| 权限检查 | {✅ 通过 | ⚠️ 有限 | ❌ 失败} | {details} |

---

## 工具执行情况

### 已执行命令

| 步骤 | 命令 | 退出代码 | 耗时 |
|------|------|-----------|------|
| 1 | `{command}` | {0 | 非零} | {duration} |
| 2 | `{command}` | {0 | 非零} | {duration} |

### 工具版本

| 工具 | 版本 |
|------|------|
| Azure CLI | {version} |
| Bicep CLI | {version} |
| Azure 开发者 CLI | {version-or-n/a} |

---

## 问题

{if-no-issues}
✅ **未发现任何问题。** 部署已准备就绪。
{end-if}

{if-issues-exist}
### 错误

{for-each-error}
#### ❌ {error-title}

- **严重程度:** 错误
- **来源:** {bicep-build | what-if | permissions}
- **位置:** {file-path}:{line}:{column}（如适用）
- **消息:** {error-message}
- **修复建议:** {suggested-fix}
- **文档链接:** {link-if-available}

{end-for-each}

### 警告

{for-each-warning}
#### ⚠️ {warning-title}

- **严重程度:** 警告
- **来源:** {source}
- **消息:** {warning-message}
- **建议操作:** {suggested-action}

{end-for-each}
{end-if}

---

## What-If 结果

{if-what-if-succeeded}

### 变更摘要

| 变更类型 | 数量 |
|----------|------|
| 🆕 创建 | {count} |
| 📝 修改 | {count} |
| 🗑️ 删除 | {count} |
| ✓ 无变更 | {count} |
| ⚠️ 忽略 | {count} |

### 将要创建的资源

{if-resources-to-create}
| 资源类型 | 资源名称 |
|----------|----------|
| {type} | {name} |
{end-if}

{if-no-resources-to-create}
*不会创建任何资源。*
{end-if}

### 将要修改的资源

{if-resources-to-modify}
#### {resource-type}/{resource-name}

| 属性 | 当前值 | 新值 |
|------|--------|------|
| {property-path} | {current} | {new} |

{end-if}

{if-no-resources-to-modify}
*不会修改任何资源。*
{end-if}

### 将要删除的资源

{if-resources-to-delete}
| 资源类型 | 资源名称 |
|----------|----------|
| {type} | {name} |

> ⚠️ **警告:** 列出的删除资源将被永久移除。
{end-if}

{if-no-resources-to-delete}
*不会删除任何资源。*
{end-if}

{end-if-what-if-succeeded}

{if-what-if-failed}
### What-If 分析失败

What-If 操作无法完成。请参阅“问题”部分以获取详细信息。
{end-if}

---

## 建议

{generate-based-on-findings}

1. {recommendation-1}
2. {recommendation-2}
3. {recommendation-3}

---

## 下一步操作

{if-all-passed}
预检验证通过。您可以继续部署：

**对于 azd 项目:**
```bash
azd provision
# 或
azd up
```

**对于独立 Bicep 项目:**
```bash
az deployment group create \
  --resource-group {rg-name} \
  --template-file {bicep-file} \
  --parameters {param-file}
```
{end-if}

{if-issues-exist}
请在部署前解决上述问题。修复后：

1. 重新运行预检验证以确认修复
2. 确保所有检查通过后继续部署
{end-if}

---

*由 Azure 部署预检技能生成的报告*
```

---

## 状态值

### 总体状态

| 状态 | 含义 | 视觉标识 |
|------|------|----------|
| **通过** | 所有检查成功，可以安全部署 | ✅ |
| **通过但有警告** | 检查成功但需审查警告 | ⚠️ |
| **失败** | 一个或多个检查失败 | ❌ |

### 单项检查状态

| 状态 | 含义 |
|------|------|
| ✅ 通过 | 检查成功完成 |
| ❌ 失败 | 检查发现错误 |
| ⚠️ 警告 | 检查通过但有警告 |
| ⏭️ 跳过 | 检查被跳过（工具不可用等） |

---

## 示例报告

```markdown
# Azure 部署预检报告

**生成时间:** 2026-01-16T14:32:00Z
**状态:** ⚠️ 通过但有警告

---

## 概述

| 属性 | 值 |
|------|----|
| **模板文件** | `infra/main.bicep` |
| **参数文件** | `infra/main.bicepparam` |
| **项目类型** | azd 项目 |
| **部署范围** | 订阅 |
| **目标** | my-subscription |
| **验证级别** | Provider |

### 验证结果

| 检查项 | 状态 | 详情 |
|--------|------|------|
| Bicep 语法 | ✅ 通过 | 未发现错误 |
| What-If 分析 | ⚠️ 警告 | 由于嵌套模板扩展限制，1 个资源被忽略 |
| 权限检查 | ✅ 通过 | 已验证完整的部署权限 |

---

## 工具执行情况

### 已执行命令

| 步骤 | 命令 | 退出代码 | 耗时 |
|------|------|-----------|------|
| 1 | `bicep build infra/main.bicep --stdout` | 0 | 1.2s |
| 2 | `azd provision --preview --environment dev` | 0 | 8.4s |

### 工具版本

| 工具 | 版本 |
|------|------|
| Azure CLI | 2.76.0 |
| Bicep CLI | 0.25.3 |
| Azure 开发者 CLI | 1.9.0 |

---

## 问题

### 警告

#### ⚠️ 嵌套模板限制已达到

- **严重程度:** 警告
- **来源:** what-if
- **消息:** 由于嵌套模板扩展限制，1 个资源被忽略
- **建议操作:** 部署后手动检查被忽略的资源

---

## What-If 结果

### 变更摘要

| 变更类型 | 数量 |
|----------|------|
| 🆕 创建 | 3 |
| 📝 修改 | 1 |
| 🗑️ 删除 | 0 |
| ✓ 无变更 | 2 |
| ⚠️ 忽略 | 1 |

### 将要创建的资源

| 资源类型 | 资源名称 |
|----------|----------|
| Microsoft.Resources/resourceGroups | rg-myapp-dev |
| Microsoft.Storage/storageAccounts | stmyappdev |
| Microsoft.Web/sites | app-myapp-dev |

### 将要修改的资源

#### Microsoft.KeyVault/vaults/kv-myapp-dev

| 属性 | 当前值 | 新值 |
|------|--------|------|
| properties.sku.name | standard | premium |
| tags.environment | staging | dev |

### 将要删除的资源

*不会删除任何资源。*

---

## 建议

1. 检查存储账户名称 `stmyappdev` 是否符合命名要求
2. 确认将 Key Vault SKU 从 standard 升级到 premium 是否为有意为之
3. 部署后应验证被忽略的嵌套模板资源

---

## 下一步操作

预检验证通过但有警告。审查上述警告后，继续执行：

```bash
azd provision --environment dev
```

---

*由 Azure 部署预检技能生成的报告*
```

---

## 格式规范

1. **使用一致的emoji** 以方便视觉扫描
2. **在引用 Bicep 错误时包含行号**
3. **为每个问题提供可操作的修复建议**
4. **在可用时链接到相关文档**
5. **按严重程度排序问题**（错误优先，然后是警告）
6. **在下一步操作中包含命令示例**

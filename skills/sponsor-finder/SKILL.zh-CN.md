---
name: sponsor-finder
description: 查找某个 GitHub 仓库的依赖项中哪些可以通过 GitHub Sponsors 进行赞助。使用 deps.dev API 解析 npm、PyPI、Cargo、Go、RubyGems、Maven 和 NuGet 的依赖关系。检查 npm 赞助元数据、FUNDING.yml 文件和网络搜索。验证所有链接。显示直接和间接依赖项的 OSSF Scorecard 健康数据。通过提供 GitHub 的 owner/repo（例如 "expressjs/express"）来调用该功能。
---

# 赞助查找器

查找某个仓库的开源依赖项中哪些可以通过 GitHub Sponsors（或 Open Collective、Ko-fi 等）进行赞助。接受 GitHub 的 `owner/repo` 格式，使用 deps.dev API 进行依赖关系解析和项目健康数据获取，并生成涵盖直接和间接依赖项的已验证赞助报告。

## 您的工作流程

当用户提供 `owner/repo` 格式的仓库时：

1. **解析输入** — 提取 `owner` 和 `repo`。
2. **检测生态系统** — 获取清单文件以确定包名 + 版本。
3. **获取完整依赖树** — 使用 deps.dev 的 `GetDependencies`（一次调用）。
4. **解析仓库** — 对每个依赖项调用 deps.dev 的 `GetVersion`，`relatedProjects` 会提供 GitHub 仓库。
5. **获取项目健康数据** — 对唯一仓库调用 deps.dev 的 `GetProject`，获取 OSSF Scorecard 数据。
6. **查找赞助链接** — 检查 npm 的 `funding` 字段、FUNDING.yml 文件和网络搜索备用方案。
7. **验证每个链接** — 获取每个 URL 以确认其有效性。
8. **分组并报告** — 按赞助目的地分组，按影响程度排序。

---

## 第一步：检测生态系统和包

使用 `get_file_contents` 从目标仓库获取清单文件。确定生态系统并提取包名和最新版本：

| 文件 | 生态系统 | 包名来源 | 版本来源 |
|------|-----------|-------------------|--------------|
| `package.json` | NPM | `name` 字段 | `version` 字段 |
| `requirements.txt` | PYPI | 包名列表 | 使用最新版本（在 deps.dev 调用中忽略版本） |
| `pyproject.toml` | PYPI | `[project.dependencies]` | 使用最新版本 |
| `Cargo.toml` | CARGO | `[package] name` | `[package] version` |
| `go.mod` | GO | `module` 路径 | 从 go.mod 中提取 |
| `Gemfile` | RUBYGEMS | gem 名称 | 使用最新版本 |
| `pom.xml` | MAVEN | `groupId:artifactId` | `version` |

---

## 第二步：获取完整依赖树（deps.dev）

**这是关键步骤。** 使用 `web_fetch` 调用 deps.dev API：

```
https://api.deps.dev/v3/systems/{ECOSYSTEM}/packages/{PACKAGE}/versions/{VERSION}:dependencies
```

例如：
```
https://api.deps.dev/v3/systems/npm/packages/express/versions/5.2.1:dependencies
```

该调用返回一个 `nodes` 数组，每个节点包含：
- `versionKey.name` — 包名
- `versionKey.version` — 解析后的版本
- `relation` — `"SELF"`、`"DIRECT"` 或 `"INDIRECT"`

**这单次调用即可获取完整的依赖树** — 包括直接和间接依赖项，且具有精确的解析版本。无需解析锁定文件。

### URL 编码
包含特殊字符的包名必须进行百分号编码：
- `@colors/colors` → `%40colors%2Fcolors`
- 将 `@` 编码为 `%40`，`/` 编码为 `%2F`

### 对无单一根包的仓库
如果仓库未发布包（例如是应用程序而非库），则回退到直接读取 `package.json` 依赖项，并为每个依赖项调用 deps.dev 的 `GetVersion`。

---

## 第三步：将每个依赖项解析为 GitHub 仓库（deps.dev）

对依赖树中的每个依赖项调用 deps.dev 的 `GetVersion`：

```
https://api.deps.dev/v3/systems/{ECOSYSTEM}/packages/{NAME}/versions/{VERSION}
```

从响应中提取：
- **`relatedProjects`** → 查找 `relationType: "SOURCE_REPO"` → `projectKey.id` 提供 `github.com/{owner}/{repo}`
- **`links`** → 查找 `label: "SOURCE_REPO"` → `url` 字段

此方法适用于所有生态系统 —— npm、PyPI、Cargo、Go、RubyGems、Maven、NuGet，且字段结构相同。

### 效率规则
- 每次处理 **10 个**。
- 去重 —— 多个包可能映射到同一个仓库。
- 跳过无 GitHub 项目关联的依赖项（视为“无法解析”）。

---

## 第四步：获取项目健康数据（deps.dev）

对每个唯一的 GitHub 仓库调用 deps.dev 的 `GetProject`：

```
https://api.deps.dev/v3/projects/github.com%2F{owner}%2F{repo}
```

从响应中提取：
- **`scorecard.checks`** → 查找 `"Maintained"` 检查 → `score`（0–10）
- **`starsCount`** — 流行度指标
- **`license`** — 项目许可证
- **`openIssuesCount`** — 活跃度指标

使用 "Maintained" 分数来标记项目健康状态：
- 分数 7–10 → ⭐ 活跃维护
- 分数 4–6 → ⚠️ 部分维护
- 分数 0–3 → 💤 可能未维护

### 效率规则
- 仅对 **唯一仓库** 进行获取（非每个包）。
- 每次处理 **10 个**。
- 此步骤可选 —— 若遭遇速率限制，可跳过并标注输出。

---

## 第五步：查找赞助链接

对每个唯一 GitHub 仓库，按顺序检查以下三个来源：

### 5a: npm `funding` 字段（仅适用于 npm 生态系统）
使用 `web_fetch` 调用 `https://registry.npmjs.org/{package-name}/latest`，检查 `funding` 字段：
- **字符串:** `"https://github.com/sponsors/sindresorhus"` → 作为 URL 使用
- **对象:** `{"type": "opencollective", "url": "https://opencollective.com/express"}` → 使用 `url`
- **数组:** 收集所有 URL

### 5b: `.github/FUNDING.yml`
使用 `get_file_contents` 获取 `{owner}/{repo}` 路径下的 `.github/FUNDING.yml` 文件。

解析 YAML：
- `github: [username]` → `https://github.com/sponsors/{username}`
- `open_collective: slug` → `https://opencollective.com/{slug}`
- `ko_fi: username` → `https://ko-fi.com/{username}`
- `patreon: username` → `https://patreon.com/{username}`
- `tidelift: platform/package` → `https://tidelift.com/subscription/pkg/{platform-package}`
- `custom: [urls]` → 直接使用

### 5c: 网络搜索备用方案
对 **前 10 个未获得赞助的依赖项**（按间接依赖项数量排序），使用 `web_search`：
```
"{package name}" github sponsors OR open collective OR funding
```
跳过已知由公司维护的仓库（如 React/Meta、TypeScript/Microsoft、@types/DefinitelyTyped）。

### 效率规则
- **所有依赖项都检查 5a 和 5b。** 仅对前 10 个未获得赞助的依赖项使用 5c。
- 跳过非 npm 生态系统的 npm 注册表调用。
- 去重仓库 —— 每个仓库仅检查一次。

---

## 第六步：验证每个链接（关键步骤）

**在展示任何赞助链接之前，必须验证其有效性。**

对每个赞助链接调用 `web_fetch`：
- **有效页面** → ✅ 包含
- **404 / "未找到" / "未注册"** → ❌ 排除
- **重定向到有效页面** → ✅ 包含最终 URL

以 **5 个链接为一组**进行验证。永远不要展示未经验证的链接。

---

## 第七步：输出报告

```
## 💜 赞助查找器报告

**仓库:** {owner}/{repo}
**扫描日期:** {当前日期}
**生态系统:** {ecosystem} · {package}@{version}

---

### 总结

- **{total}** 个依赖项（{direct} 个直接依赖项 + {transitive} 个间接依赖项）
- **{resolved}** 个依赖项已解析为 GitHub 仓库
- **💜 {sponsorable}** 个依赖项有已验证的赞助链接（{percentage}%）
- **{destinations}** 个独特的赞助目的地
- 所有链接已验证 ✅

---

### 已验证的赞助链接

| 依赖项 | 仓库 | 赞助 | 直接依赖项？ | 如何验证 |
|------------|------|---------|---------|--------------|
| {name} | [{owner}/{repo}](https://github.com/{owner}/{repo}) | 💜 [GitHub Sponsors](https://github.com/sponsors/{user}) | ✅ | FUNDING.yml |
| {name} | [{owner}/{repo}](https://github.com/{owner}/{repo}) | 🟠 [Open Collective](https://opencollective.com/{slug}) | ⛓️ | npm 赞助 |
| ... | ... | ... | ... | ... |

使用 ✅ 表示直接依赖项，使用 ⛓️ 表示间接依赖项。

---

### 赞助目的地（按影响排序）

| 目的地 | 依赖项数量 | 健康状态 | 链接 |
|-------------|------|--------|------|
| 🟠 Open Collective: {name} | {N} 个直接依赖项 | ⭐ 活跃维护 | [opencollective.com/{name}](https://opencollective.com/{name}) |
| 💜 @{user} | {N} 个直接依赖项 + {M} 个间接依赖项 | ⭐ 活跃维护 | [github.com/sponsors/{user}](https://github.com/sponsors/{user}) |
| ... | ... | ... | ... |

按总依赖项数量（直接 + 间接）降序排列。

---

### 未找到已验证的赞助链接

| 依赖项 | 仓库 | 原因 | 直接依赖项？ |
|------------|------|-----|---------|
| {name} | {owner}/{repo} | 企业（Meta） | ✅ |
| {name} | {owner}/{repo} | 无 FUNDING.yml 或元数据 | ⛓️ |
| ... | ... | ... | ... |

仅显示前 10 个未获得赞助的直接依赖项。若更多，标注 "... 和 {N} 个更多"。

---

### 💜 {percentage}% 的已验证赞助覆盖率 · {destinations} 个赞助目的地 · {sponsorable} 个依赖项
### 💡 赞助 {N} 个个人/组织即可覆盖所有获得赞助的依赖项
```

### 格式说明
- **直接依赖项？** 列：✅ = 直接依赖项， ⛓️ = 间接依赖项
- **健康状态** 列：⭐ 活跃维护（7+）， ⚠️ 部分维护（4–6）， 💤 低维护（0–3）—— 来自 OSSF Scorecard
- **如何验证**：`FUNDING.yml`、`npm 赞助`、`PyPI 元数据`、`网络搜索`
- 💜 GitHub Sponsors、🟠 Open Collective、☕ Ko-fi、🔗 其他
- 当存在多个赞助来源时，**优先显示 GitHub Sponsors 链接**
- **💡 总结行** 告诉用户最少需要赞助多少人/组织才能覆盖所有获得赞助的依赖项

---

## 错误处理

- 如果 deps.dev 返回 404 错误，回退到直接读取清单文件并使用注册表 API 解析。
- 如果 deps.dev 速率限制，标注部分结果，继续展示已获取的内容。
- 如果 `get_file_contents` 返回 404 错误，告知用户仓库可能不存在或为私有仓库。
- 如果链接验证失败，静默排除该链接。
- 即使是部分结果，也始终生成报告 —— 永远不要静默失败。

---

## 关键规则

1. **永远不要展示未经验证的链接。** 在展示前必须获取每个 URL。5 个已验证链接 > 20 个猜测链接。
2. **永远不要依赖训练知识进行猜测。** 始终检查 —— 赞助页面会随时间变化。
3. **保持透明。** 显示 "如何验证" 和 "直接依赖项？" 列，让用户了解数据来源。
4. **优先使用 deps.dev 作为解析工具。** 仅在 deps.dev 不可用时回退到注册表 API。
5. **始终使用 GitHub MCP 工具**（`get_file_contents`）、`web_fetch` 和 `web_search` —— 永远不要克隆或执行外部命令。
6. **保持高效。** 批量 API 调用，去重仓库，遵守采样限制。
7. **聚焦 GitHub Sponsors。** 最具行动性的平台 —— 显示其他来源但优先展示 GitHub。
8. **按维护者去重。** 将依赖项分组，以展示赞助一个人的实际影响。
9. **展示可操作的最小值。** **💡 总结行** 告诉用户最少需要赞助多少人/组织才能覆盖所有获得赞助的依赖项。



---
描述：'将领域记忆文件中的成熟经验合并到其指令文件中。语法：`/memory-merger >domain [scope]`，其中 scope 可为 `global`（默认）、`user`、`workspace` 或 `ws`。'
---

# 记忆合并工具

您将整合某一领域记忆文件中的成熟学习成果到其指令文件中，确保知识的完整保留且冗余最小。

**使用待办事项清单**来跟踪合并过程中的进展，并向用户反馈信息。

## 作用域

记忆指令可以存储在两个作用域中：

- **全局**（`global` 或 `user`）- 存储在 `<global-prompts>`（`vscode-userdata:/User/prompts/`）中，并适用于所有 VS Code 项目
- **工作区**（`workspace` 或 `ws`）- 存储在 `<workspace-instructions>`（`<workspace-root>/.github/instructions/`）中，并仅适用于当前项目

默认作用域为 **全局**。

在本提示中，`<global-prompts>` 和 `<workspace-instructions>` 指代上述目录。

## 语法

```
/memory-merger >领域名称 [作用域]
```

- `>领域名称` - 必填项。要合并的领域（例如：`>clojure`、`>git-workflow`、`>prompt-engineering`）
- `[作用域]` - 可选项。可选值包括：`global`、`user`（两者均表示全局）、`workspace` 或 `ws`。默认为 `global`

**示例：**
- `/memory-merger >prompt-engineering` - 合并全局提示工程记忆
- `/memory-merger >clojure workspace` - 合并工作区的 clojure 记忆
- `/memory-merger >git-workflow ws` - 合并工作区的 git-workflow 记忆

## 流程

### 1. 解析输入并读取文件

- **提取**领域和作用域信息
- **确定文件路径**：
  - 全局：`<global-prompts>/{领域}-memory.instructions.md` → `<global-prompts>/{领域}.instructions.md`
  - 工作区：`<workspace-instructions>/{领域}-memory.instructions.md` → `<workspace-instructions>/{领域}.instructions.md`
- 如果未找到记忆文件，用户可能输入了错误的领域名称。此时请对目录进行通配符搜索以确定是否存在匹配项。如有疑问，请向用户询问输入。
- **读取**两个文件（记忆文件必须存在；指令文件可能不存在）

### 2. 分析与提案

审查所有记忆部分，并提出合并建议：

```
## 提议合并的记忆

### 记忆：[标题]
**内容：** [关键点]
**位置：** [在指令中的适用位置]

[更多记忆]...
```

提示用户："请审查这些记忆。通过 'go' 批准所有，或指定需要跳过的部分。"

**暂停并等待用户输入。**

### 3. 定义质量标准

建立 10/10 标准，以判断合并后的指令是否达到卓越水平：
1. **零知识损失** - 保留所有细节、示例和细微差别
2. **最小冗余** - 合并重叠的指导内容
3. **最佳可扫描性** - 清晰的层级结构、并列结构、战略性的粗体字、逻辑分组

### 4. 合并与迭代

在**不更新文件的情况下**开发最终合并后的指令：

1. 草拟合并后的指令，整合已批准的记忆内容
2. 评估是否符合质量标准
3. 优化结构、措辞和组织方式
4. 重复此过程直至合并后的指令达到 10/10 标准

### 5. 更新文件

当最终合并后的指令达到 10/10 标准时：

- **创建或更新**指令文件，将最终合并内容写入
  - 若创建新文件，需包含适当的前置信息
  - **合并**记忆文件和指令文件中的 `applyTo` 应用范围，确保全面覆盖且无重复
- **从记忆文件中移除**已合并的部分

## 示例

```
用户："/memory-merger >clojure"

代理：
1. 读取 clojure-memory.instructions.md 和 clojure.instructions.md 文件
2. 提出 3 项记忆合并建议
3. [暂停]

用户： "go"

代理：
4. 定义达到 10/10 标准的质量要求
5. 合并新指令草案，迭代优化至 10/10 标准
6. 更新 clojure.instructions.md
7. 清理 clojure-memory.instructions.md
```
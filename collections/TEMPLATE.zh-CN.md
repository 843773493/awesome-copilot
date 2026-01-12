

# 集合模板

使用此模板创建一个新的相关提示、指令和聊天模式集合。

## 基本模板

```yaml
id: my-collection-id
name: 我的集合名称
description: 简要描述该集合提供什么内容以及谁应该使用它。
tags: [tag1, tag2, tag3] # 可选的发现标签
items:
  - path: prompts/my-prompt.prompt.md
    kind: prompt
  - path: instructions/my-instructions.instructions.md  
    kind: instruction
  - path: agents/my-chatmode.agent.md
    kind: agent
display:
  ordering: alpha # 或 "manual" 以保持上方的顺序
  show_badge: false # 设置为 true 以显示集合徽章
```

## 字段说明

- **id**: 使用小写字母、数字和短横线的唯一标识符
- **name**: 集合的显示名称
- **description**: 集合目的的简要说明（1-500个字符）
- **tags**: 可选的发现标签数组（最多10个，每个标签1-30个字符）
- **items**: 集合中的项目数组（1-50个项目）
  - **path**: 从仓库根目录到文件的相对路径
  - **kind**: 必须为 `prompt`、`instruction` 或 `chat-mode`
- **display**: 可选的显示设置
  - **ordering**: `alpha`（按字母排序）或 `manual`（保持顺序）
  - **show_badge**: 在项目上显示集合徽章（true/false）

## 创建新集合

### 使用 VS Code 任务
1. 按下 `Ctrl+Shift+P`（或 Mac 上的 `Cmd+Shift+P`）
2. 输入 "Tasks: Run Task"
3. 选择 "create-collection"
4. 输入您的集合 ID 以响应提示

### 使用命令行
```bash
node create-collection.js my-collection-id
```

### 手动创建
1. 创建 `collections/my-collection-id.collection.yml`
2. 使用上方模板作为起点
3. 添加您的项目并自定义设置
4. 运行 `npm run validate:collections` 以验证
5. 运行 `npm start` 以生成文档

## 验证

集合会自动验证以确保：
- 所有必填字段都存在且有效
- 文件路径有效且与项目类型匹配
- ID 在所有集合中唯一
- 标签和显示设置符合模式

手动运行验证：
```bash
npm run validate:collections
```

## 文件组织

集合不需要重新组织现有文件。只要在清单中路径正确，项目可以位于仓库的任何位置。

## 最佳实践

1. **有意义的集合**: 为特定工作流程或使用场景分组协同工作的项目
2. **清晰的命名**: 使用描述性的名称和 ID，反映集合的目的
3. **良好的描述**: 解释谁应该使用该集合以及它能提供什么好处
4. **相关的标签**: 添加有助于用户查找相关集合的发现标签
5. **合理的大小**: 保持集合聚焦 - 通常 3-10 个项目效果最佳
6. **测试项目**: 在将文件添加到集合之前，确保所有引用文件存在且功能正常
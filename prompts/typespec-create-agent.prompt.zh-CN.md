

---
mode: '代理'
tools: ['更改', '搜索代码库', '编辑文件', '问题']
description: '为Microsoft 365 Copilot生成一个完整的TypeSpec声明式代理，包含指令、功能和对话启动器'
model: 'gpt-4.1'
tags: [类型规范, m365-copilot, 声明式代理, 代理开发]
---

# 创建TypeSpec声明式代理

创建一个完整的TypeSpec声明式代理用于Microsoft 365 Copilot，结构如下：

## 要求

生成一个`main.tsp`文件，包含：

1. **代理声明**
   - 使用`@agent`装饰器，提供描述性的名称和描述
   - 名称应少于100个字符
   - 描述应少于1000个字符

2. **指令**
   - 使用`@instructions`装饰器，提供清晰的行为指南
   - 定义代理的角色、专长和个性
   - 说明代理应执行和不应执行的操作
   - 保持在8000个字符以内

3. **对话启动器**
   - 包含2-4个`@conversationStarter`装饰器
   - 每个装饰器需包含标题和示例查询
   - 使其多样化，展示不同的功能

4. **功能**（基于用户需求）
   - `WebSearch` - 用于网络内容，支持可选的站点范围限定
   - `OneDriveAndSharePoint` - 用于文档访问，支持URL过滤
   - `TeamsMessages` - 用于Teams频道/聊天访问
   - `Email` - 用于电子邮件访问，支持文件夹过滤
   - `People` - 用于组织人员搜索
   - `CodeInterpreter` - 用于Python代码执行
   - `GraphicArt` - 用于图像生成
   - `GraphConnectors` - 用于Copilot连接器内容
   - `Dataverse` - 用于Dataverse数据访问
   - `Meetings` - 用于会议内容访问

## 模板结构

```typescript
import "@typespec/http";
import "@typespec/openapi3";
import "@microsoft/typespec-m365-copilot";

using TypeSpec.Http;
using TypeSpec.M365.Copilot.Agents;

@agent({
  name: "[代理名称]",
  description: "[代理描述]"
})
@instructions("""
  [关于代理行为、角色和指南的详细说明]
""")
@conversationStarter(#{
  title: "[启动器标题1]",
  text: "[示例查询1]"
})
@conversationStarter(#{
  title: "[启动器标题2]",
  text: "[示例查询2]"
})
namespace [代理名称] {
  // 在此处添加功能作为操作
  op 功能名称 is AgentCapabilities.[功能类型]<[参数]>;
}
```

## 最佳实践

- 使用描述性、基于角色的代理名称（例如："客户支持助手", "研究助手"）
- 使用第二人称编写说明（例如："'您是...'”）
- 明确说明代理的专业领域和限制
- 包含多样化的对话启动器以展示不同功能
- 仅包含代理实际需要的功能
- 在可能的情况下对功能（URL、文件夹等）进行范围限定以提升性能
- 使用三引号字符串表示多行说明

## 示例

询问用户：
1. 代理的用途和角色是什么？
2. 它需要哪些功能？
3. 它应该访问哪些知识源？
4. 典型的用户交互是什么？

然后生成完整的TypeSpec代理定义。
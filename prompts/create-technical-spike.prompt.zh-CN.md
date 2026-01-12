

---
agent: 'agent'
description: '创建时间限制的技术冲刺文档，用于研究和解决在实现前必须回答的关键开发决策。'
tools: ['runCommands', 'runTasks', 'edit', 'search', 'extensions', 'usages', 'vscodeAPI', 'think', 'problems', 'changes', 'testFailure', 'openSimpleBrowser', 'fetch', 'githubRepo', 'todos', 'Microsoft Docs', 'search']
---

# 创建技术冲刺文档

创建时间限制的技术冲刺文档，用于研究必须在开发前解决的关键问题。每个冲刺文档聚焦于一个特定的技术决策，具有明确的交付成果和时间安排。

## 文档结构

在 `${input:FolderPath|docs/spikes}` 目录中创建单独的文件。使用以下命名模式：`[category]-[简要描述]-spike.md`（例如：`api-copilot-integration-spike.md`，`performance-realtime-audio-spike.md`）。

```md
---
title: "${input:SpikeTitle}"
category: "${input:Category|Technical}"
status: "🔴 未开始"
priority: "${input:Priority|High}"
timebox: "${input:Timebox|1 week}"
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
owner: "${input:Owner}"
tags: ["technical-spike", "${input:Category|technical}", "research"]
---

# ${input:SpikeTitle}

## 概述

**冲刺目标：** [需要解决的明确、具体的问题或决策]

**为何重要：** [对开发/架构决策的影响]

**时间限制：** [分配给该冲刺的时间]

**决策截止日期：** [必须在此日期前解决以避免阻塞开发]

## 研究问题

**主要问题：** [需要回答的主要技术问题]

**次要问题：**

- [相关问题1]
- [相关问题2]
- [相关问题3]

## 调查计划

### 研究任务

- [ ] [具体研究任务1]
- [ ] [具体研究任务2]
- [ ] [具体研究任务3]
- [ ] [创建原型/概念验证]
- [ ] [记录研究结果和建议]

### 成功标准

**当该冲刺满足以下条件时视为完成：**

- [ ] [具体标准1]
- [ ] [具体标准2]
- [ ] [明确记录推荐方案]
- [ ] [原型完成（如适用）]

## 技术背景

**相关组件：** [列出受此决策影响的系统组件]

**依赖项：** [其他冲刺或决策依赖于解决此问题]

**限制条件：** [已知的限制或要求，会影响解决方案]

## 研究结果

### 调查结果

[记录研究结果、测试结果和收集的证据]

### 原型/测试说明

[来自任何原型、冲刺或技术实验的结果]

### 外部资源

- [相关文档的链接]
- [API参考的链接]
- [社区讨论的链接]
- [示例/教程的链接]

## 决策

### 推荐方案

[基于研究结果的明确推荐]

### 理由

[为何选择此方法而非其他替代方案]

### 实现说明

[实施时的关键考虑因素]

### 后续行动

- [ ] [行动项1]
- [ ] [行动项2]
- [ ] [更新架构文档]
- [ ] [创建实现任务]

## 状态历史

| 日期   | 状态         | 备注                      |
| ------ | -------------- | -------------------------- |
| [日期] | 🔴 未开始 | 创建并定义冲刺范围         |
| [日期] | 🟡 进行中 | 开始研究                   |
| [日期] | 🟢 已完成 | [解决摘要]                 |

---

_最后更新：[日期] 由 [姓名]_
```

## 技术冲刺分类

### API集成

- 第三方API的功能和限制
- 集成模式和认证
- 速率限制和性能特征

### 架构与设计

- 系统架构决策
- 设计模式适用性
- 组件交互模型

### 性能与可扩展性

- 性能需求和限制
- 可扩展性瓶颈和解决方案
- 资源利用模式

### 平台与基础设施

- 平台功能和限制
- 基础设施需求
- 部署和托管考虑因素

### 安全与合规

- 安全需求和实现
- 合规限制
- 认证和授权方法

### 用户体验

- 用户交互模式
- 可访问性需求
- 界面设计决策

## 文件命名规范

使用描述性的、kebab-case格式的名称，表明分类和具体未知内容：

**API/集成示例：**

- `api-copilot-chat-integration-spike.md`
- `api-azure-speech-realtime-spike.md`
- `api-vscode-extension-capabilities-spike.md`

**性能示例：**

- `performance-audio-processing-latency-spike.md`
- `performance-extension-host-limitations-spike.md`
- `performance-webrtc-reliability-spike.md`

**架构示例：**

- `architecture-voice-pipeline-design-spike.md`
- `architecture-state-management-spike.md`
- `architecture-error-handling-strategy-spike.md`

## AI代理最佳实践

1. **每个冲刺聚焦一个问题：** 每个文档专注于一个技术决策或研究问题
2. **时间限制研究：** 为每个冲刺定义具体的时间限制和交付成果
3. **基于证据的决策：** 在标记为完成前，要求有具体证据（测试、原型、文档）
4. **明确的推荐：** 记录具体的推荐方案及实施理由
5. **依赖项追踪：** 识别冲刺之间的关联及对项目决策的影响
6. **以结果为导向：** 每个冲刺必须产生可操作的决策或建议

## 研究策略

### 阶段1：信息收集

1. **使用搜索/获取工具查找现有文档**
2. **分析代码库** 以识别现有模式和限制
3. **研究外部资源**（API、库、示例）

### 阶段2：验证与测试

1. **创建聚焦原型** 以测试特定假设
2. **运行针对性实验** 以验证假设
3. **记录测试结果** 并附上支持证据

### 阶段3：决策与文档

1. **将研究结果综合** 为明确的推荐方案
2. **记录实施指导** 供开发团队参考
3. **创建后续任务** 用于实施

## 工具使用

- **search/searchResults:** 研究现有解决方案和文档
- **fetch/githubRepo:** 分析外部API、库和示例
- **codebase:** 理解现有系统的限制和模式
- **runTasks:** 执行原型和验证测试
- **editFiles:** 更新研究进展和结果
- **vscodeAPI:** 测试VS Code扩展功能和限制

专注于解决关键技术决策并解除开发进度阻塞的时间限制研究。
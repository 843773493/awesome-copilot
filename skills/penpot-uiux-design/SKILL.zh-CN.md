---
name: penpot-uiux-design
description: '使用MCP工具在Penpot中创建专业UI/UX设计的全面指南。在以下情况下使用此技能：(1) 为网页、移动或桌面应用程序创建新的UI/UX设计，(2) 使用组件和令牌构建设计系统，(3) 设计仪表板、表单、导航或落地页，(4) 应用无障碍标准和最佳实践，(5) 遵循平台指南（iOS、Android、Material Design），(6) 审查或改进现有Penpot设计的可用性。触发条件： "设计UI", "创建界面", "构建布局", "设计仪表板", "创建表单", "设计落地页", "使其无障碍", "设计系统", "组件库"。'
---

# Penpot UI/UX设计指南

使用`penpot/penpot-mcp` MCP服务器和经过验证的UI/UX原则，在Penpot中创建专业、以用户为中心的设计。

## 可用的MCP工具

| 工具 | 用途 |
| ---- | ------- |
| `mcp__penpot__execute_code` | 在Penpot插件上下文中运行JavaScript以创建/修改设计 |
| `mcp__penpot__export_shape` | 导出形状为PNG/SVG以进行视觉检查 |
| `mcp__penpot__import_image` | 将图片（图标、照片、标志）导入设计中 |
| `mcp__penpot__penpot_api_info` | 获取Penpot API文档 |

## MCP服务器设置

Penpot MCP工具需要本地运行的`penpot/penpot-mcp`服务器。有关详细安装和故障排除，请参阅[setup-troubleshooting.md](references/setup-troubleshooting.md)。

### 设置前检查：服务器是否已运行

**在尝试设置前，始终检查MCP服务器是否已可用：**

1. **尝试调用一个工具**：尝试`mcp__penpot__penpot_api_info` - 如果成功，说明服务器正在运行并已连接。无需设置。
2. **如果工具调用失败**，请询问用户：
   > "Penpot MCP服务器似乎未连接。服务器是否已安装并运行？如果是，我可以协助排查问题。如果不是，我可以引导您完成设置。"
3. **仅在用户确认服务器未安装时**才继续执行设置说明。

### 快速入门（仅当未安装时）

```bash
# 克隆并安装
git clone https://github.com/penpot/penpot-mcp.git
cd penpot-mcp
npm install

# 构建并启动服务器
npm run bootstrap
```

然后在Penpot中：
1. 打开一个设计文件
2. 进入 **插件** → **从URL加载插件**
3. 输入：`http://localhost:4400/manifest.json`
4. 点击插件UI中的 **"连接到MCP服务器"**

### VS Code配置

添加到`settings.json`：
```json
{
  "mcp": {
    "servers": {
      "penpot": {
        "url": "http://localhost:4401/sse"
      }
    }
  }
}
```

### 故障排除（如果服务器已安装但无法运行）

| 问题 | 解决方案 |
| ----- | -------- |
| 插件无法连接 | 检查服务器是否正在运行（在penpot-mcp目录中运行`npm run start:all`） |
| 浏览器阻止localhost | 允许本地网络访问提示，或禁用Brave Shield，或尝试使用Firefox |
| 工具未出现在客户端 | 在配置更改后完全重启VS Code/Claude |
| 工具执行失败/超时 | 确保Penpot插件UI已打开且显示"已连接" |
| "WebSocket连接失败" | 检查防火墙是否允许4400、4401、4402端口 |

## 快速参考

| 任务 | 参考文件 |
| ---- | -------------- |
| MCP服务器安装与故障排除 | [setup-troubleshooting.md](references/setup-troubleshooting.md) |
| 组件规范（按钮、表单、导航） | [component-patterns.md](references/component-patterns.md) |
| 无障碍（对比度、触摸目标） | [accessibility.md](references/accessibility.md) |
| 屏幕尺寸与平台规范 | [platform-guidelines.md](references/platform-guidelines.md) |

## 核心设计原则

### 黄金法则

1. **清晰性优于复杂性**：每个元素都必须有其用途
2. **一致性建立信任**：重复使用模式、颜色和组件
3. **以用户目标为先**：为任务设计，而非功能
4. **无障碍不是可选的**：为所有人设计
5. **与真实用户测试**：尽早验证假设

### 视觉层次（优先顺序）

1. **尺寸**：越大越重要
2. **颜色/对比度**：高对比度吸引注意力
3. **位置**：左上角（LTR）最先被看到
4. **留白**：隔离强调重要性
5. **排版粗细**：加粗突出显示

## 设计流程

1. **首先检查设计系统**：询问用户是否有现有令牌/规范，或从当前Penpot文件中发现
2. **理解页面**：使用`mcp__penpot__execute_code`调用`penpotUtils.shapeStructure()`查看层级结构
3. **查找元素**：使用`penpotUtils.findShapes()`通过类型或名称定位元素
4. **创建/修改**：使用`penpot.createBoard()`、`penpot.createRectangle()`、`penpot.createText()`等
5. **应用布局**：使用`addFlexLayout()`创建响应式容器
6. **验证**：调用`mcp__penpot__export_shape`以视觉检查工作成果

## 设计系统处理

**在创建设计前，确定用户是否已有设计系统：**

1. **询问用户**："您是否有需要遵循的设计系统或品牌指南？"
2. **从Penpot中发现**：检查现有组件、颜色和模式

```javascript
// 发现当前文件中的现有设计模式
const allShapes = penpotUtils.findShapes(() => true, penpot.root);

// 查找现有颜色
const colors = new Set();
allShapes.forEach(s => {
  if (s.fills) s.fills.forEach(f => colors.add(f.fillColor));
});

// 查找现有文本样式（字体大小、粗细）
const textStyles = allShapes
  .filter(s => s.type === 'text')
  .map(s => ({ fontSize: s.fontSize, fontWeight: s.fontWeight }));

// 查找现有组件
const components = penpot.library.local.components;

return { colors: [...colors], textStyles, componentCount: components.length };
```

**如果用户已有设计系统：**

- 使用用户指定的颜色、间距和排版
- 匹配现有组件模式
- 遵循用户的命名规范

**如果用户没有设计系统：**

- 使用以下默认令牌作为起点
- 提供帮助建立一致模式的建议
- 参考[component-patterns.md](references/component-patterns.md)中的规范

## Penpot API关键注意事项

- `width`/`height`是只读属性 → 使用`shape.resize(w, h)`
- `parentX`/`parentY`是只读属性 → 使用`penpotUtils.setParentXY(shape, x, y)`
- 使用`insertChild(index, shape)`进行Z轴排序（而非`appendChild`）
- Flex子元素数组顺序在`dir="column"`或`dir="row"`时被反转
- 在`text.resize()`后，将`growType`重置为"auto-width"或"auto-height"

## 新板定位

**在创建新板前，始终检查现有板**以避免重叠：

```javascript
// 查找所有现有板并计算下一个位置
const boards = penpotUtils.findShapes(s => s.type === 'board', penpot.root);
let nextX = 0;
const gap = 100; // 板之间的间距

if (boards.length > 0) {
  // 查找最右侧板的边缘
  boards.forEach(b => {
    const rightEdge = b.x + b.width;
    if (rightEdge + gap > nextX) {
      nextX = rightEdge + gap;
    }
  });
}

// 在计算的位置创建新板
const newBoard = penpot.createBoard();
newBoard.x = nextX;
newBoard.y = 0;
newBoard.resize(375, 812);
```

**板间距指南：**

- 相关屏幕之间使用100px间距（同一流程）
- 不同部分/流程之间使用200px+间距
- 将板垂直对齐（相同y坐标）以实现视觉组织
- 按用户流程顺序将相关屏幕水平分组

## 默认设计令牌

**仅在用户没有设计系统时使用这些默认值。如果有用户令牌，请优先使用。**

### 间距比例尺（8px为基数）

| 令牌 | 值 | 使用场景 |
| ----- | ----- | ----- |
| `spacing-xs` | 4px | 紧密排列的内联元素 |
| `spacing-sm` | 8px | 相关元素 |
| `spacing-md` | 16px | 默认内边距 |
| `spacing-lg` | 24px | 部分间距 |
| `spacing-xl` | 32px | 主要部分 |
| `spacing-2xl` | 48px | 页面级间距 |

### 排版比例尺

| 层级 | 大小 | 粗细 | 使用场景 |
| ----- | ---- | ------ | ----- |
| 展示 | 48-64px | 加粗 | 主标题 |
| H1 | 32-40px | 加粗 | 页面标题 |
| H2 | 24-28px | 半加粗 | 部分标题 |
| H3 | 20-22px | 半加粗 | 子部分 |
| 正文 | 16px | 正常 | 主要内容 |
| 小号 | 14px | 正常 | 次要文本 |
| 标注 | 12px | 正常 | 标签、提示 |

### 颜色使用规范

| 用途 | 建议 |
| ------- | -------------- |
| 主色 | 主品牌色、CTA（行动号召） |
| 辅助色 | 支持性操作 |
| 成功 | #22C55E色系（确认信息） |
| 警告 | #F59E0B色系（警告） |
| 错误 | #EF4444色系（错误） |
| 中性色 | 文字/边框的灰度色系 |

## 常见布局

### 移动屏幕（375×812）

```text
┌─────────────────────────────┐
│ 状态栏 (44px)           │
├─────────────────────────────┤
│ 头部/导航栏 (56px)           │
├─────────────────────────────┤
│                             │
│ 内容区域                │
│ （可滚动）                │
│ 内边距：16px水平          │
│                             │
├─────────────────────────────┤
│ 底部导航/CTA (84px)       │
└─────────────────────────────┘

```

### 桌面仪表板（1440×900）

```text
┌──────┬──────────────────────────────────┐
│      │ 头部 (64px)                    │
│ 侧边 │──────────────────────────────────│
│ 栏   │ 页面标题 + 操作               │
│      │──────────────────────────────────│
│ 240  │ 内容网格                     │
│ px   │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ │
│      │ │卡片 │ │卡片 │ │卡片 │ │卡片 │ │
│      │ └─────┘ └─────┘ └─────┘ └─────┘ │
│      │                                  │
└──────┴──────────────────────────────────┘

```

## 组件检查清单

### 按钮

- [ ] 清晰、以行动为导向的标签（2-3个词）
- [ ] 最小触摸目标：44×44px
- [ ] 视觉状态：默认、悬停、激活、禁用、加载
- [ ] 足够的对比度（与背景对比度至少为3:1）
- [ ] 应用程序中一致的圆角半径

### 表单

- [ ] 标签位于输入上方（而非仅占位符）
- [ ] 标记必填字段
- [ ] 错误信息靠近字段
- [ ] 逻辑的Tab顺序
- [ ] 输入类型与内容匹配（如电子邮件、电话等）

### 导航

- [ ] 明确指示当前位置
- [ ] 跨页面保持一致位置
- [ ] 最多7±2个顶级项目
- [ ] 移动端触摸友好（48px目标尺寸）

## 无障碍快速检查

1. **颜色对比度**：文字4.5:1，大文字3:1
2. **触摸目标**：最小44×44px
3. **焦点状态**：可见的键盘焦点指示器
4. **替代文本**：为图片提供有意义的描述
5. **层次结构**：正确的标题级别（H1→H2→H3）
6. **颜色独立性**：永远不要仅依赖颜色

## 设计评审检查清单

在最终化任何设计前：

- [ ] 视觉层次清晰
- [ ] 间距和对齐一致
- [ ] 排版可读（正文文字至少16px）
- [ ] 颜色对比度符合WCAG AA标准
- [ ] 交互元素明显
- [ ] 移动端友好触摸目标
- [ ] 考虑加载/空/错误状态
- [ ] 与设计系统保持一致

## 验证设计

使用`mcp__penpot__execute_code`进行以下验证：

| 检查 | 方法 |
| ----- | ------ |
| 元素超出边界 | 使用`penpotUtils.analyzeDescendants()`结合`isContainedIn()` |
| 文字过小 (<12px) | 使用`penpotUtils.findShapes()`过滤`fontSize` |
| 缺乏对比度 | 调用`mcp__penpot__export_shape`进行视觉检查 |
| 层级结构 | 使用`penpotUtils.shapeStructure()`审查嵌套关系 |

### 导出CSS

通过`mcp__penpot__execute_code`使用`penpot.generateStyle(selection, { type: 'css', includeChildren: true })`从设计中提取CSS。

## 创造优秀设计的技巧

1. **从内容开始**：真实内容揭示布局需求
2. **移动优先设计**：约束激发创造力
3. **使用网格**：8px基数网格保持对齐
4. **限制颜色**：1主色 + 1辅色 + 中性色
5. **限制字体**：最多1-2种字体
6. **拥抱留白**：留白空间提升理解力
7. **保持一致性**：相同操作在所有地方呈现一致
8. **提供反馈**：每个操作都需要响应

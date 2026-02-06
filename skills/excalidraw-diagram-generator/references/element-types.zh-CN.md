# Excalidraw 元素类型指南

每个 Excalidraw 元素类型的详细规格，包含视觉示例和使用场景。

## 元素类型概览

| 类型 | 视觉 | 主要用途 | 文本支持 |
|------|--------|-------------|--------------|
| `rectangle` | □ | 流程步骤、实体、数据存储、组件 | ✅ 是 |
| `ellipse` | ○ | 开始/结束点、状态、强调圆形 | ✅ 是 |
| `diamond` | ◇ | 决策点、选择 | ✅ 是 |
| `arrow` | → | 流向、关系 | ❌ 否（使用单独文本） |
| `line` | — | 连接、分隔符 | ❌ 否 |
| `text` | A | 标签、注释、标题 | ✅ （其用途） |

---

## 矩形

**最适合用于：** 流程步骤、实体、数据存储、组件

### 属性

```typescript
{
  type: "rectangle",
  roundness: { type: 3 },  // 圆角
  text: "Step Name",       // 可选嵌入文本
  fontSize: 20,
  textAlign: "center",
  verticalAlign: "middle"
}
```

### 使用场景

| 场景 | 配置 |
|----------|---------------|
| **流程步骤** | 绿色背景 (`#b2f2bb`)，居中文本 |
| **实体/对象** | 蓝色背景 (`#a5d8ff`)，中等尺寸 |
| **系统组件** | 浅色，描述性文本 |
| **数据存储** | 灰色/白色，数据库样标签 |

### 尺寸指南

| 内容 | 宽度 | 高度 |
|---------|-------|--------|
| 单个单词 | 120-150px | 60-80px |
| 短短短语（2-4个单词） | 180-220px | 80-100px |
| 句子 | 250-300px | 100-120px |

### 示例

```json
{
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "backgroundColor": "#b2f2bb",
  "text": "验证输入",
  "fontSize": 20,
  "textAlign": "center",
  "verticalAlign": "middle",
  "roundness": { "type": 3 }
}
```

---

## 椭圆

**最适合用于：** 流程起点/终点、状态、强调圆形

### 属性

```typescript
{
  type: "ellipse",
  text: "开始",
  fontSize: 18,
  textAlign: "center",
  verticalAlign: "middle"
}
```

### 使用场景

| 场景 | 配置 |
|----------|---------------|
| **流程起点** | 浅绿色，"开始"文本 |
| **流程终点** | 浅红色，"结束"文本 |
| **状态** | 柔和颜色，状态名称 |
| **高亮** | 明亮颜色，强调文本 |

### 尺寸指南

对于圆形形状，使用 `width === height`：

| 内容 | 直径 |
|---------|----------|
| 图标/符号 | 60-80px |
| 短文本 | 100-120px |
| 更长文本 | 150-180px |

### 示例

```json
{
  "type": "ellipse",
  "x": 100,
  "y": 100,
  "width": 120,
  "height": 120,
  "backgroundColor": "#d0f0c0",
  "text": "开始",
  "fontSize": 18,
  "textAlign": "center",
  "verticalAlign": "middle"
}
```

---

## 菱形

**最适合用于：** 决策点、条件分支

### 属性

```typescript
{
  type: "diamond",
  text: "Valid?",
  fontSize: 18,
  textAlign: "center",
  verticalAlign": "middle"
}
```

### 使用场景

| 场景 | 文本示例 |
|----------|--------------|
| **是/否决策** | "是否有效？", "是否存在？" |
| **多选** | "类型？", "状态？" |
| **条件** | "分数 > 50？" |

### 尺寸指南

菱形与矩形相比，相同文本需要更多空间：

| 内容 | 宽度 | 高度 |
|---------|-------|--------|
| 是/否 | 120-140px | 120-140px |
| 短问题 | 160-180px | 160-180px |
| 更长问题 | 200-220px | 200-220px |

### 示例

```json
{
  "type": "diamond",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 150,
  "backgroundColor": "#ffe4a3",
  "text": "Valid?",
  "fontSize": 18,
  "textAlign": "center",
  "verticalAlign": "middle"
}
```

---

## 箭头

**最适合用于：** 流向、关系、依赖项

### 属性

```typescript
{
  type: "arrow",
  points: [[0, 0], [endX, endY]],  // 相对坐标
  roundness: { type: 2 },          // 弯曲
  startBinding: null,              // 或 { elementId, focus, gap }
  endBinding: null
}
```

### 箭头方向

#### 水平（从左到右）

```json
{
  "x": 100,
  "y": 150,
  "width": 200,
  "height": 0,
  "points": [[0, 0], [200, 0]]
}
```

#### 垂直（从上到下）

```json
{
  "x": 200,
  "y": 100,
  "width": 0,
  "height": 150,
  "points": [[0, 0], [0, 150]]
}
```

#### 斜线

```json
{
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 150,
  "points": [[0, 0], [200, 150]]
}
```

### 箭头样式

| 样式 | `strokeStyle` | `strokeWidth` | 使用场景 |
|-------|---------------|---------------|----------|
| **常规流向** | `"solid"` | 2 | 标准连接 |
| **可选/弱连接** | `"dashed"` | 2 | 可选路径 |
| **重要** | `"solid"` | 3-4 | 强调流向 |
| **虚线** | `"dotted"` | 2 | 间接关系 |

### 添加箭头标签

使用单独的文本元素，放置在箭头中点附近：

```json
[
  {
    "type": "arrow",
    "id": "arrow1",
    "x": 100,
    "y": 150,
    "points": [[0, 0], [200, 0]]
  },
  {
    "type": "text",
    "x": 180,      // 靠近中点
    "y": 130,      // 在箭头上方
    "text": "发送",
    "fontSize": 14
  }
]
```

---

## 线条

**最适合用于：** 非方向性连接、分隔符、边框

### 属性

```typescript
{
  type: "line",
  points: [[0, 0], [x2, y2], [x3, y3], ...],
  roundness: null  // 或 { type: 2 } 表示弯曲
}
```

### 使用场景

| 场景 | 配置 |
|----------|---------------|
| **分隔符** | 水平，细线 |
| **边框** | 闭合路径（多边形） |
| **连接** | 多点路径 |
| **下划线** | 短水平线 |

### 多点线条示例

```json
{
  "type": "line",
  "x": 100,
  "y": 100,
  "points": [
    [0, 0],
    [100, 50],
    [200, 0]
  ]
}
```

---

## 文本

**最适合用于：** 标签、标题、注释、独立文本

### 属性

```typescript
{
  type: "text",
  text: "标签文本",
  fontSize: 20,
  fontFamily: 1,        // 1=Virgil, 2=Helvetica, 3=Cascadia
  textAlign: "left",
  verticalAlign: "top"
}
```

### 按用途的字体大小

| 用途 | 字体大小 |
|---------|-----------|
| **主标题** | 28-36 |
| **章节标题** | 24-28 |
| **元素标签** | 18-22 |
| **注释** | 14-16 |
| **小注** | 12-14 |

### 文本尺寸计算

```javascript
// 近似宽度
const width = text.length * fontSize * 0.6;

// 近似高度（单行）
const height = fontSize * 1.2;

// 多行
const lines = text.split('\n').length;
const height = fontSize * 1.2 * lines;
```

### 文本定位

| 位置 | textAlign | verticalAlign | 使用场景 |
|----------|-----------|---------------|----------|
| **左上角** | `"left"` | `"top"` | 默认标签 |
| **居中** | `"center"` | `"middle"` | 标题 |
| **右下角** | `"right"` | `"bottom"` | 脚注 |

### 示例：标题

```json
{
  "type": "text",
  "x": 100,
  "y": 50,
  "width": 400,
  "height": 40,
  "text": "系统架构",
  "fontSize": 32,
  "fontFamily": 2,
  "textAlign": "center",
  "verticalAlign": "top"
}
```

### 示例：注释

```json
{
  "type": "text",
  "x": 150,
  "y": 200,
  "width": 100,
  "height": 20,
  "text": "用户输入",
  "fontSize": 14,
  "fontFamily": 1,
  "textAlign": "left",
  "verticalAlign": "top"
}
```

---

## 组合元素

### 模式：带标签的框

```json
[
  {
    "type": "rectangle",
    "id": "box1",
    "x": 100,
    "y": 100,
    "width": 200,
    "height": 100,
    "text": "组件",
    "textAlign": "center",
    "verticalAlign": "middle"
  }
]
```

### 模式：连接的框

```json
[
  {
    "type": "rectangle",
    "id": "box1",
    "x": 100,
    "y": 100,
    "width": 150,
    "height": 80,
    "text": "步骤 1"
  },
  {
    "type": "arrow",
    "id": "arrow1",
    "x": 250,
    "y": 140,
    "points": [[0, 0], [100, 0]]
  },
  {
    "type": "rectangle",
    "id": "box2",
    "x": 350,
    "y": 100,
    "width": 150,
    "height": 80,
    "text": "步骤 2"
  }
]
```

### 模式：决策树

```json
[
  {
    "type": "diamond",
    "id": "decision",
    "x": 100,
    "y": 100,
    "width": 140,
    "height": 140,
    "text": "Valid?"
  },
  {
    "type": "arrow",
    "id": "yes-arrow",
    "x": 240,
    "y": 170,
    "points": [[0, 0], [60, 0]]
  },
  {
    "type": "text",
    "id": "yes-label",
    "x": 250,
    "y": 150,
    "text": "是",
    "fontSize": 14
  },
  {
    "type": "rectangle",
    "id": "yes-box",
    "x": 300,
    "y": 140,
    "width": 120,
    "height": 60,
    "text": "处理"
  }
]
```

---

## 总结

| 当你需要... | 使用此元素 |
|------------------|------------------|
| 流程框 | `rectangle` 带文本 |
| 决策点 | `diamond` 带问题 |
| 流向 | `arrow` |
| 开始/结束 | `ellipse` |
| 标题/页眉 | `text`（大字体） |
| 注释 | `text`（小字体） |
| 非方向性链接 | `line` |
| 分隔符 | `line`（水平） |

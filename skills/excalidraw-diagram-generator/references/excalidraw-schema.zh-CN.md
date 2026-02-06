# Excalidraw JSON Schema 参考文档

本文档描述了用于图示生成的 Excalidraw `.excalidraw` 文件的结构。

## 顶层结构

```typescript
interface ExcalidrawFile {
  type: "excalidraw";
  version: number;           // 始终为 2
  source: string;            // "https://excalidraw.com"
  elements: ExcalidrawElement[];
  appState: AppState;
  files: Record<string, any>; // 通常为空 {}
}
```

## appState

```typescript
interface AppState {
  viewBackgroundColor: string; // 十六进制颜色，例如 "#ffffff"
  gridSize: number;            // 通常为 20
}
```

## ExcalidrawElement 基础属性

所有元素共享以下通用属性：

```typescript
interface BaseElement {
  id: string;                  // 唯一标识符
  type: ElementType;           // 参见下方的元素类型
  x: number;                   // X 坐标（相对于左上角的像素值）
  y: number;                   // Y 坐标（相对于左上角的像素值）
  width: number;               // 宽度（像素）
  height: number;              // 高度（像素）
  angle: number;               // 旋转角度（弧度，通常为 0）
  strokeColor: string;         // 十六进制颜色，例如 "#1e1e1e"
  backgroundColor: string;     // 十六进制颜色或 "transparent"
  fillStyle: "solid" | "hachure" | "cross-hatch";
  strokeWidth: number;         // 通常为 1-4
  strokeStyle: "solid" | "dashed" | "dotted";
  roughness: number;           // 0-2，控制手绘效果（1 为默认值）
  opacity: number;             // 0-100
  groupIds: string[];          // 该元素所属的组 ID
  frameId: null;               // 通常为 null
  index: string;               // 堆叠顺序标识符
  roundness: Roundness | null;
  seed: number;                // 确定性渲染的随机种子
  version: number;             // 元素版本（编辑时递增）
  versionNonce: number;        // 编辑时变化的随机数
  isDeleted: boolean;          // 应设为 false
  boundElements: any;          // 通常为 null
  updated: number;             // 毫秒级时间戳
  link: null;                  // 外部链接（通常为 null）
  locked: boolean;             // 元素是否被锁定
}
```

## 元素类型

### 矩形

```typescript
interface RectangleElement extends BaseElement {
  type: "rectangle";
  roundness: { type: 3 };      // 3 = 圆角
  text?: string;               // 可选的内部文本
  fontSize?: number;           // 字体大小（典型值为 16-32）
  fontFamily?: number;         // 1 = Virgil，2 = Helvetica，3 = Cascadia
  textAlign?: "left" | "center" | "right";
  verticalAlign?: "top" | "middle" | "bottom";
}
```

**示例：**
```json
{
  "id": "rect1",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 100,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "text": "My Box",
  "fontSize": 20,
  "textAlign": "center",
  "verticalAlign": "middle",
  "roundness": { "type": 3 }
}
```

### 椭圆

```typescript
interface EllipseElement extends BaseElement {
  type: "ellipse";
  text?: string;
  fontSize?: number;
  fontFamily?: number;
  textAlign?: "left" | "center" | "right";
  verticalAlign?: "top" | "middle" | "bottom";
}
```

### 菱形

```typescript
interface DiamondElement extends BaseElement {
  type: "diamond";
  text?: string;
  fontSize?: number;
  fontFamily?: number;
  textAlign?: "left" | "center" | "right";
  verticalAlign?: "top" | "middle" | "bottom";
}
```

### 箭头

```typescript
interface ArrowElement extends BaseElement {
  type: "arrow";
  points: [number, number][];  // 元素相对坐标的 [x, y] 坐标数组
  startBinding: Binding | null;
  endBinding: Binding | null;
  roundness: { type: 2 };      // 2 = 弯曲箭头
}
```

**示例：**
```json
{
  "id": "arrow1",
  "type": "arrow",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 0,
  "points": [
    [0, 0],
    [200, 0]
  ],
  "roundness": { "type": 2 },
  "startBinding": null,
  "endBinding": null
}
```

**坐标说明：**
- 第一个坐标 `[0, 0]` 相对于 `(x, y)`
- 后续坐标相对于第一个坐标
- 水平直线箭头：`[[0, 0], [width, 0]]`
- 垂直直线箭头：`[[0, 0], [0, height]]`

### 线条

```typescript
interface LineElement extends BaseElement {
  type: "line";
  points: [number, number][];
  startBinding: Binding | null;
  endBinding: Binding | null;
  roundness: { type: 2 } | null;
}
```

### 文本

```typescript
interface TextElement extends BaseElement {
  type: "text";
  text: string;
  fontSize: number;
  fontFamily: number;          // 1-3
  textAlign: "left" | "center" | "right";
  verticalAlign: "top" | "middle" | "bottom";
  roundness: null;             // 文本无圆角
}
```

**示例：**
```json
{
  "id": "text1",
  "type": "text",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 25,
  "text": "Hello World",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "left",
  "verticalAlign": "top",
  "roundness": null
}
```

**宽度/高度计算：**
- 宽度 ≈ `文本长度 * 字体大小 * 0.6`
- 高度 ≈ `字体大小 * 1.2 * 行数`

## 绑定

绑定用于将箭头与形状连接：

```typescript
interface Binding {
  elementId: string;           // 绑定的元素 ID
  focus: number;               // -1 到 1，表示边沿位置
  gap: number;                 // 与元素边沿的距离
}
```

## 常用颜色

| 颜色名称 | 十六进制代码 | 使用场景 |
|----------|--------------|----------|
| 黑色 | `#1e1e1e` | 默认描边 |
| 浅蓝色 | `#a5d8ff` | 主要实体 |
| 浅绿色 | `#b2f2bb` | 流程步骤 |
| 黄色 | `#ffd43b` | 重要/中心元素 |
| 浅红色 | `#ffc9c9` | 警告/错误 |
| 青色 | `#96f2d7` | 次要元素 |
| 透明 | `transparent` | 无填充 |
| 白色 | `#ffffff` | 背景 |

## ID 生成

ID 应为唯一字符串。常见模式：

```javascript
// 基于时间戳
const id = Date.now().toString(36) + Math.random().toString(36).substr(2);

// 顺序生成
const id = "element-" + counter++;

// 描述性生成
const id = "step-1", "entity-user", "arrow-1-to-2";
```

## 种子生成

种子用于手绘效果的确定性随机性：

```javascript
const seed = Math.floor(Math.random() * 2147483647);
```

## 版本与版本Nonce

```javascript
const version = 1;  // 在元素被编辑时递增
const versionNonce = Math.floor(Math.random() * 2147483647);
```

## 坐标系统

- 原点 `(0, 0)` 是左上角
- X 轴向右增加
- Y 轴向下增加
- 所有单位均为像素

## 推荐间距

| 场景 | 间距 |
|------|------|
| 元素之间的水平间距 | 200-300 像素 |
| 行之间的垂直间距 | 100-150 像素 |
| 元素与边缘的最小边距 | 50 像素 |
| 箭头与框之间的间隙 | 20-30 像素 |

## 字体类型

| ID | 名称 | 描述 |
|----|------|-------------|
| 1 | Virgil | 手写风格（默认） |
| 2 | Helvetica | 清晰的无衬线字体 |
| 3 | Cascadia | 等宽字体 |

## 验证规则

✅ **必填项：**
- 所有 ID 必须唯一
- `type` 必须与实际元素类型匹配
- `version` 必须为 ≥ 1 的整数
- `opacity` 必须为 0-100

⚠️ **推荐项：**
- 保持 `roughness` 为 1 以确保一致性
- 使用 `strokeWidth` 为 2 以提高清晰度
- 将 `isDeleted` 设为 `false`
- 将 `locked` 设为 `false`
- 保持 `frameId`、`boundElements`、`link` 为 `null`

## 完整最小示例

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "id": "box1",
      "type": "rectangle",
      "x": 100,
      "y": 100,
      "width": 200,
      "height": 100,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "index": "a0",
      "roundness": { "type": 3 },
      "seed": 1234567890,
      "version": 1,
      "versionNonce": 987654321,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1706659200000,
      "link": null,
      "locked": false,
      "text": "Hello",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle"
    }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

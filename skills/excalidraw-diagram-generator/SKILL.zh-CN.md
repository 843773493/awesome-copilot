---
name: excalidraw图示生成器
description: '根据自然语言描述生成Excalidraw格式的图示。当用户请求"创建图示"、"制作流程图"、"可视化流程"、"绘制系统架构"、"创建思维导图"或"生成Excalidraw文件"时使用。支持流程图、关系图、思维导图和系统架构图。输出可直接在Excalidraw中打开的.excalidraw JSON文件。'
---

# Excalidraw图示生成器

一种根据自然语言描述生成Excalidraw格式图示的技能。此技能帮助无需手动绘制即可创建流程、系统、关系和想法的视觉表示。

## 使用此技能的场景

当用户请求以下内容时使用此技能：

- "创建展示...的图示"
- "为...制作流程图"
- "可视化...的流程"
- "绘制...的系统架构"
- "创建关于...的思维导图"
- "为...生成Excalidraw文件"
- "展示...之间的关系"
- "图示...的工作流程"

**支持的图示类型：**
- 📊 **流程图**：顺序流程、工作流程、决策树
- 🔗 **关系图**：实体关系、系统组件、依赖关系
- 🧠 **思维导图**：概念层级、头脑风暴结果、主题组织
- 🏗️ **架构图**：系统设计、模块交互、数据流
- 📈 **数据流图 (DFD)**：数据流可视化、数据转换过程
- 🏊 **业务流程 (泳道)**：跨职能流程、基于角色的流程
- 📦 **类图**：面向对象设计、类结构和关系
- 🔄 **顺序图**：随时间推移的对象交互、消息流
- 🗃️ **ER图**：数据库实体关系、数据模型

## 前提条件

- 需要可视化的清晰描述
- 识别关键实体、步骤或概念
- 理解元素之间的关系或流程

## 步骤详解

### 步骤 1：理解请求

分析用户的描述以确定：
1. **图示类型**（流程图、关系图、思维导图、架构图）
2. **关键元素**（实体、步骤、概念）
3. **关系**（流程、连接、层级）
4. **复杂度**（元素数量）

### 步骤 2：选择合适的图示类型

| 用户意图 | 图示类型 | 示例关键词 |
|----------|----------|------------|
| 流程、步骤、程序 | **流程图** | "工作流程"、"流程"、"步骤"、"程序" |
| 连接、依赖、关联 | **关系图** | "关系"、"连接"、"依赖"、"结构" |
| 概念层级、头脑风暴 | **思维导图** | "思维导图"、"概念"、"想法"、"分解" |
| 系统设计、组件 | **架构图** | "架构"、"系统"、"组件"、"模块" |
| 数据流、转换过程 | **数据流图 (DFD)** | "数据流"、"数据处理"、"数据转换" |
| 跨职能流程、角色职责 | **业务流程 (泳道)** | "业务流程"、"泳道"、"角色"、"职责" |
| 面向对象设计、类结构 | **类图** | "类"、"继承"、"OOP"、"对象模型" |
| 交互序列、消息流 | **顺序图** | "序列"、"交互"、"消息"、"时间线" |
| 数据库设计、实体关系 | **ER图** | "数据库"、"实体"、"关系"、"数据模型" |

### 步骤 3：提取结构化信息

**流程图：**
- 顺序步骤列表
- 决策点（如有）
- 起始和结束点

**关系图：**
- 实体/节点（名称+可选描述）
- 实体间关系（从→到，带标签）

**思维导图：**
- 中心主题
- 主分支（推荐3-6个）
- 每个分支下的子主题（可选）

**数据流图 (DFD)：**
- 数据源和目的地（外部实体）
- 处理过程（数据转换）
- 数据存储（数据库、文件）
- 数据流（从左到右或从左上到右下的箭头）
- **重要提示**：不要表示流程顺序，仅显示数据流

**业务流程 (泳道)：**
- 角色/参与者（部门、系统、人员）- 显示为顶部列标题
- 流程泳道（每个参与者下方的垂直泳道）
- 流程框（每个泳道内的活动）
- 流程箭头（连接流程框，包括跨泳道交接）

**类图：**
- 带名称的类
- 带可见性（+、-、#）的属性
- 带可见性和参数的方法
- 关系：继承（实线+白三角）、实现（虚线+白三角）、关联（实线）、依赖（虚线）、聚合（实线+白菱形）、组合（实线+填充菱形）
- 多重性标注（1、0..1、1..*、*）

**顺序图：**
- 对象/参与者（顶部水平排列）
- 生命线（从每个对象延伸的垂直线）
- 消息（生命线间的水平箭头）
- 同步消息（实线箭头）、异步消息（虚线箭头）
- 返回值（虚线箭头）
- 激活框（执行期间生命线上的矩形）
- 时间流从上到下

**ER图：**
- 实体（带实体名称的矩形）
- 属性（实体内列出）
- 主键（下划线或标记为PK）
- 外键（标记为FK）
- 关系（连接实体的线）
- 基数：1:1（一对一）、1:N（一对多）、N:M（多对多）
- 多对多关系的连接实体（虚线矩形）

### 步骤 4：生成Excalidraw JSON

创建带有适当元素的`.excalidraw`文件：

**可用元素类型：**
- `rectangle`：用于实体、步骤、概念的框
- `ellipse`：用于强调的替代形状
- `diamond`：用于决策点
- `arrow`：用于方向连接
- `text`：用于标签和注释

**需要设置的关键属性：**
- **位置**：`x`、`y`坐标
- **尺寸**：`width`、`height`
- **样式**：`strokeColor`、`backgroundColor`、`fillStyle`
- **字体**：`fontFamily: 5`（Excalifont - **所有文本元素都必须使用**）
- **文本**：嵌入文本用于标签
- **连接**：`points`数组用于箭头

**重要提示**：所有文本元素必须使用`fontFamily: 5`（Excalifont）以确保视觉一致性。

### 步骤 5：格式化输出

构建完整的Excalidraw文件结构：

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    // 图示元素数组
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

### 步骤 6：保存并提供说明

1. 保存为`<描述性名称>.excalidraw`
2. 提示用户如何打开：
   - 访问 https://excalidraw.com
   - 点击"打开"或拖放文件
   - 或使用Excalidraw VS Code扩展

## 最佳实践

### 元素数量指南

| 图示类型 | 推荐数量 | 最大数量 |
|----------|----------|----------|
| 流程图步骤 | 3-10 | 15 |
| 关系图实体 | 3-8 | 12 |
| 思维导图分支 | 4-6 | 8 |
| 每个分支的子主题 | 2-4 | 6 |

### 布局技巧

1. **起始位置**：居中重要元素，保持间距一致
2. **间距**：
   - 水平间距：元素间200-300px
   - 垂直间距：行间100-150px
3. **颜色**：使用一致的配色方案
   - 主元素：浅蓝色（`#a5d8ff`）
   - 次要元素：浅绿色（`#b2f2bb`）
   - 重要/中心元素：黄色（`#ffd43b`）
   - 警告/提示：浅红色（`#ffc9c9`）
4. **文本大小**：16-24px以确保可读性
5. **字体**：始终使用`fontFamily: 5`（Excalifont）用于所有文本元素
6. **箭头样式**：简单流程使用直线箭头，复杂关系使用曲线箭头

### 复杂度管理

**如果用户请求包含过多元素：**
- 建议拆分为多个图示
- 首先聚焦主要元素
- 提供创建详细子图示的选项

**示例响应：**
```
"您的请求包含15个组件。为了清晰，我建议：
1. 高层架构图（6个主要组件）
2. 每个子系统的详细图示

您希望我先创建高层视图吗？"
```

## 示例提示与响应

### 示例1：简单流程图

**用户**："为用户注册创建流程图"

**代理生成：**
1. 提取步骤："输入邮箱" → "验证邮箱" → "设置密码" → "完成"
2. 创建包含4个矩形和3个箭头的流程图
3. 保存为`user-registration-flow.excalidraw`

### 示例2：关系图

**用户**："图示用户、帖子和评论实体之间的关系"

**代理生成：**
1. 实体：用户、帖子、评论
2. 关系：用户 → 帖子（"创建"）、用户 → 评论（"撰写"）、帖子 → 评论（"包含"）
3. 保存为`user-content-relationships.excalidraw`

### 示例3：思维导图

**用户**："关于机器学习概念的思维导图"

**代理生成：**
1. 中心：机器学习
2. 分支：监督学习、无监督学习、强化学习、深度学习
3. 每个分支下的子主题
4. 保存为`machine-learning-mindmap.excalidraw`

## 常见问题排查

| 问题 | 解决方案 |
|------|----------|
| 元素重叠 | 增加元素间的间距 |
| 文本无法适应框内 | 增加框宽或减小字体大小 |
| 元素过多 | 拆分为多个图示 |
| 布局不清晰 | 使用网格布局（行列）或径向布局（思维导图） |
| 配色不一致 | 根据元素类型提前定义配色方案 |

## 高级技巧

### 网格布局（用于关系图）
```javascript
const columns = Math.ceil(Math.sqrt(entityCount));
const x = startX + (index % columns) * horizontalGap;
const y = startY + Math.floor(index / columns) * verticalGap;
```

### 径向布局（用于思维导图）
```javascript
const angle = (2 * Math.PI * index) / branchCount;
const x = centerX + radius * Math.cos(angle);
const y = centerY + radius * Math.sin(angle);
```

### 自动生成ID
使用时间戳+随机字符串生成唯一ID：
```javascript
const id = Date.now().toString(36) + Math.random().toString(36).substr(2);
```

## 输出格式

始终提供：
1. ✅ 完整的`.excalidraw` JSON文件
2. 📊 创建内容的摘要
3. 📝 元素数量
4. 💡 打开/编辑说明

**示例摘要：**
```
创建：user-workflow.excalidraw
类型：流程图
元素：7个矩形、6个箭头、1个标题文本
总数：14个元素

查看方法：
1. 访问 https://excalidraw.com
2. 拖放 user-workflow.excalidraw 文件
3. 或使用 文件 → 打开 在Excalidraw VS Code扩展中
```

## 验证检查清单

交付图示前请确认：
- [ ] 所有元素有唯一ID
- [ ] 坐标避免重叠
- [ ] 文字可读（字体大小16+）
- [ ] **所有文本元素使用`fontFamily: 5`（Excalifont）**
- [ ] 箭头连接逻辑
- [ ] 配色方案一致
- [ ] 文件是有效的JSON
- [ ] 元素数量合理（每图不超过20个）

## 可选增强：图标库

对于专业图示（如AWS/GCP/Azure架构图），您可以使用Excalidraw的预设图标库。这提供专业、标准化的图标，而不是基础形状。

### 用户请求图标时的处理

**如果用户要求AWS/云架构图或提及使用特定图标：**

1. **检查库是否存在**：
   ```
   查看目录：skills/excalidraw-diagram-generator/libraries/
   确认包含reference.md文件的子目录
   ```

2. **阅读reference.md**：
   ```
   打开：libraries/<库名>/reference.md
   这是一个轻量级文件（通常<300行），列出所有可用图标
   ```

3. **查找相关图标**：
   ```
   在reference.md表格中搜索符合图示需求的图标名称
   示例：AWS图示中包含EC2、S3、Lambda → 在表格中查找"EC2"、"S3"、"Lambda"
   ```

4. **加载特定图标数据**（警告：大文件）：
   ```
   仅读取所需的图标文件：
   - libraries/aws-architecture-icons/icons/EC2.json（200-300行）
   - libraries/aws-architecture-icons/icons/S3.json（200-300行）
   - libraries/aws-architecture-icons/icons/Lambda.json（200-300行）
   **总计**：约2000+行JSON数据需处理
   ```

5. **提取并转换元素**：
   ```
   每个图标JSON包含一个"elements"数组
   计算每个图标的边界框（min_x, min_y, max_x, max_y）
   对所有x/y坐标应用偏移量
   为所有元素生成新的唯一ID
   更新groupIds引用
   将转换后的元素复制到您的图示中
   ```

6. **定位图标并添加连接**：
   ```
   调整x/y坐标以正确放置图标
   更新ID以确保图示内唯一性
   按需添加连接箭头和标签
   ```

**手动集成的挑战**：
- ⚠️ 高文本消耗（每个图标约200-1000行 × 图标数量）
- ⚠️ 复杂的坐标数学计算
- ⚠️ 若未谨慎处理，存在ID冲突风险
- ⚠️ 多图标图示耗时较长

### 示例：使用图标创建AWS图示

**请求**："创建包含互联网网关、VPC、ELB、EC2和RDS的AWS架构图"

**推荐工作流（使用Python脚本）**：

```bash
# 步骤1：创建基础图示文件并添加标题
# 创建my-aws-diagram.excalidraw文件，包含基础结构（标题等）

# 步骤2：检查图标可用性
# 读取：libraries/aws-architecture-icons/reference.md
# 确认图标存在：Internet-gateway、VPC、ELB、EC2、RDS

# 步骤3：使用Python脚本添加图标
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw "Internet-gateway" 150 100 --label "互联网网关"
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw VPC 200 200
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw ELB 350 250 --label "负载均衡器"
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw EC2 500 300 --label "Web服务器"
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw RDS 650 350 --label "数据库"

# 步骤4：添加连接箭头
python scripts/add-arrow.py my-aws-diagram.excalidraw 200 150 250 200  # 互联网 → VPC
python scripts/add-arrow.py my-aws-diagram.excalidraw 265 230 350 250  # VPC → ELB
python scripts/add-arrow.py my-aws-diagram.excalidraw 415 280 500 300  # ELB → EC2
python scripts/add-arrow.py my-aws-diagram.excalidraw 565 330 650 350 --label "SQL" --style dashed

# 结果：包含专业AWS图标、标签和连接的完整图示
```

**优势**：
- 无需手动坐标计算
- 图标数据不消耗AI令牌
- 确定性、可靠的结果
- 易于迭代调整位置

**替代工作流（手动，若脚本不可用）**：
1. 检查：`libraries/aws-architecture-icons/reference.md`是否存在 → 是
2. 读取reference.md → 查找"Internet-gateway"、"VPC"、"ELB"、"EC2"、"RDS"的条目
3. 加载：
   - `icons/Internet-gateway.json`（298行）
   - `icons/VPC.json`（550行）
   - `icons/ELB.json`（363行）
   - `icons/EC2.json`（231行）
   - `icons/RDS.json`（类似大小）
   **总计**：约2000-5000行JSON数据需处理
4. 从每个JSON中提取元素
5. 计算每个图标的边界框并应用偏移量
6. 转换所有坐标（x, y）以定位
7. 为所有元素生成唯一ID
8. 添加连接箭头
9. 添加文本标签
10. 生成最终的`.excalidraw`文件

**手动方法的挑战**：
- 高文本消耗（约2000-5000行）
- 复杂的坐标数学计算
- 若未谨慎处理，存在ID冲突风险

## 支持的图标库（示例 — 验证可用性）

- 该工作流适用于您提供的任何有效`.excalidrawlib`文件。
- 您可能在https://libraries.excalidraw.com/上找到的库类别示例：
   - 云服务图标
   - Kubernetes/基础设施图标
   - UI/材料图标
   - 流程图/图示符号
   - 网络图示图标
- 可用性和命名可能变化，使用前请在网站上确认确切库名。

## 无图标可用的回退方案

**若未设置图标库：**
- 使用基础形状（矩形、椭圆形、箭头）创建图示
- 使用配色和文本标签区分组件
- 通知用户可后续添加图标或设置库以备将来使用
- 图示仍将功能清晰，只是视觉效果稍逊

## 参考资料

查看以下捆绑参考资料：
- `references/excalidraw-schema.md` - 完整的Excalidraw JSON架构
- `references/element-types.md` - 详细的元素类型规范
- `templates/flowchart-template.json` - 基础流程图模板
- `templates/relationship-template.json` - 关系图模板
- `templates/mindmap-template.json` - 思维导图模板
- `scripts/split-excalidraw-library.py` - 用于分割`.excalidrawlib`文件的工具
- `scripts/README.md` - 图标库工具文档
- `scripts/.gitignore` - 防止本地Python文件被提交

## 局限性

- 复杂曲线简化为直线或基础曲线
- 手绘粗糙度设为默认值（1）
- 自动生成不支持嵌入图片
- 推荐每图元素数量上限：20个
- 无自动碰撞检测（请使用间距指南）

## 未来改进方向

潜在改进：
- 自动布局优化算法
- 从Mermaid/PlantUML语法导入
- 模板库扩展
- 生成后交互式编辑

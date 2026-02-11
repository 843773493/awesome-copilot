# CSS 样式参考

涵盖 CSS 属性、选择器、伪类、@规则、盒模型、弹性布局、网格布局和媒体查询的综合参考。

---

## 目录

1. [CSS 属性参考](#1-css-属性参考)
2. [CSS 选择器](#2-css-选择器)
3. [伪类和伪元素](#3-伪类和伪元素)
4. [CSS @规则](#4-css-@规则)
5. [CSS 样式基础](#5-css-样式基础)
6. [盒模型](#6-盒模型)
7. [弹性布局](#7-弹性布局)
8. [网格布局](#8-网格布局)
9. [媒体查询](#9-媒体查询)

---

## 1. CSS 属性参考

> 来源：https://www.w3schools.com/cssref/index.php

### 背景

| 属性 | 描述 |
|---|---|
| `background` | 所有背景属性的简写 |
| `background-color` | 设置背景颜色 |
| `background-image` | 设置一个或多个背景图像 |
| `background-position` | 设置背景图像的起始位置 |
| `background-repeat` | 设置背景图像的重复方式 |
| `background-size` | 设置背景图像的大小 (`cover`, `contain`, 长度) |
| `background-attachment` | 设置背景是否随内容滚动 (`scroll`, `fixed`, `local`) |
| `background-clip` | 定义背景的延伸范围 (`border-box`, `padding-box`, `content-box`) |
| `background-origin` | 指定背景图像的定位区域 |

### 边框

| 属性 | 描述 |
|---|---|
| `border` | `border-width`、`border-style`、`border-color` 的简写 |
| `border-width` | 设置边框宽度 |
| `border-style` | 设置边框样式 (`none`, `solid`, `dashed`, `dotted`, `double`, `groove`, `ridge`, `inset`, `outset`) |
| `border-color` | 设置边框颜色 |
| `border-radius` | 设置圆角 |
| `border-top` / `border-right` / `border-bottom` / `border-left` | 单个边的边框 |
| `border-collapse` | 设置表格边框是否合并为单个边框 (`collapse`, `separate`) |
| `border-spacing` | 设置相邻单元格边框之间的间距 |
| `border-image` | 使用图像作为边框的简写 |
| `outline` | 在边框外部绘制的线条（不占用空间） |
| `outline-offset` | 为轮廓和元素边缘之间添加间距 |

### 盒模型 / 尺寸

| 属性 | 描述 |
|---|---|
| `width` / `height` | 设置元素的宽度/高度 |
| `min-width` / `min-height` | 设置最小宽度/高度 |
| `max-width` / `max-height` | 设置最大宽度/高度 |
| `margin` | 设置外部间距（简写形式，用于上、右、下、左） |
| `padding` | 设置内部间距（简写形式，用于上、右、下、左） |
| `box-sizing` | 定义宽度/高度的计算方式 (`content-box`, `border-box`) |
| `overflow` | 控制内容溢出 (`visible`, `hidden`, `scroll`, `auto`) |
| `overflow-x` / `overflow-y` | 分别控制水平/垂直溢出 |

### 颜色和透明度

| 属性 | 描述 |
|---|---|
| `color` | 设置文本颜色 |
| `opacity` | 设置透明度级别 (0.0 到 1.0) |

### 显示和可见性

| 属性 | 描述 |
|---|---|
| `display` | 控制显示行为 (`block`, `inline`, `inline-block`, `flex`, `grid`, `none` 等) |
| `visibility` | 控制可见性 (`visible`, `hidden`, `collapse`) |
| `float` | 将元素放置在其容器的左侧或右侧 |
| `clear` | 指定不允许浮动元素的边 |
| `position` | 设置定位方式 (`static`, `relative`, `absolute`, `fixed`, `sticky`) |
| `top` / `right` / `bottom` / `left` | 定位元素的偏移量 |
| `z-index` | 设置定位元素的堆叠顺序 |

### 字体和排版

| 属性 | 描述 |
|---|---|
| `font` | 字体属性的简写 |
| `font-family` | 设置字体（例如 `"Arial", sans-serif`） |
| `font-size` | 设置文本大小 |
| `font-weight` | 设置粗细 (`normal`, `bold`, `100`-`900`) |
| `font-style` | 设置样式 (`normal`, `italic`, `oblique`) |
| `font-variant` | 设置小写或其它变体 |
| `line-height` | 设置行高 |
| `letter-spacing` | 设置字符间距 |
| `word-spacing` | 设置单词间距 |

### 文本

| 属性 | 描述 |
|---|---|
| `text-align` | 设置水平对齐 (`left`, `right`, `center`, `justify`) |
| `text-decoration` | 为文本添加装饰 (`none`, `underline`, `overline`, `line-through`) |
| `text-transform` | 控制大小写 (`uppercase`, `lowercase`, `capitalize`) |
| `text-indent` | 缩进文本块的首行 |
| `text-shadow` | 为文本添加阴影 |
| `white-space` | 控制空白处理方式 |
| `word-break` | 控制单词换行规则 |
| `word-wrap` / `overflow-wrap` | 允许长单词换行到下一行 |
| `vertical-align` | 设置内联或表格单元格元素的垂直对齐 |
| `direction` | 设置文本方向 (`ltr`, `rtl`) |

### 列表

| 属性 | 描述 |
|---|---|
| `list-style` | 列表属性的简写 |
| `list-style-type` | 设置项目符号类型 (`disc`, `circle`, `square`, `decimal`, `none` 等) |
| `list-style-position` | 设置项目符号的位置 (`inside`, `outside`) |
| `list-style-image` | 使用图像作为列表项符号 |

### 表格

| 属性 | 描述 |
|---|---|
| `border-collapse` | 合并表格单元格边框 (`collapse`, `separate`) |
| `border-spacing` | 设置单元格之间的间距（当 `separate` 时） |
| `caption-side` | 设置表格标题的位置 (`top`, `bottom`) |
| `empty-cells` | 控制空单元格的显示 (`show`, `hide`) |
| `table-layout` | 设置表格布局算法 (`auto`, `fixed`) |

### 变换和过渡

| 属性 | 描述 |
|---|---|
| `transform` | 应用 2D 或 3D 变换 (`translate`, `rotate`, `scale`, `skew`, `matrix`) |
| `transform-origin` | 设置变换的原点 |
| `transition` | 变换属性的简写 |
| `transition-property` | 指定要变换的属性 |
| `transition-duration` | 设置变换持续时间 |
| `transition-timing-function` | 设置速度曲线 (`ease`, `linear`, `ease-in`, `ease-out`, `ease-in-out`, `cubic-bezier()`) |
| `transition-delay` | 设置变换开始前的延迟 |

### 动画

| 属性 | 描述 |
|---|---|
| `animation` | 动画属性的简写 |
| `animation-name` | 命名 `@keyframes` 动画 |
| `animation-duration` | 动画持续时间 |
| `animation-timing-function` | 动画的速度曲线 |
| `animation-delay` | 动画开始前的延迟 |
| `animation-iteration-count` | 重复次数 (`infinite` 表示循环) |
| `animation-direction` | 动画是否交替方向 (`normal`, `reverse`, `alternate`) |
| `animation-fill-mode` | 在动画前后应用的样式 (`none`, `forwards`, `backwards`, `both`) |
| `animation-play-state` | 暂停或运行动画 (`running`, `paused`) |

---

## 2. CSS 选择器

> 来源：https://www.w3schools.com/cssref/css_selectors.php

### 基本选择器

| 选择器 | 示例 | 描述 |
|---|---|---|
| `*` | `* { }` | 选择所有元素 |
| `element` | `p { }` | 选择所有 `<p>` 元素 |
| `.class` | `.intro { }` | 选择所有具有 `class="intro"` 的元素 |
| `#id` | `#firstname { }` | 选择具有 `id="firstname"` 的元素 |
| `element.class` | `p.intro { }` | 选择具有 `class="intro"` 的 `<p>` 元素 |

### 分组选择器

| 选择器 | 示例 | 描述 |
|---|---|---|
| `sel1, sel2` | `div, p { }` | 选择所有 `<div>` 和所有 `<p>` 元素 |

### 选择器组合

| 选择器 | 示例 | 描述 |
|---|---|---|
| `ancestor descendant` | `div p { }` | 选择 `<div>` 内的所有 `<p>` 元素（任意深度） |
| `parent > child` | `div > p { }` | 选择 `<div>` 的直接子元素 `<p>` |
| `element + sibling` | `div + p { }` | 选择 `<div>` 后的第一个 `<p>` 元素 |
| `element ~ siblings` | `div ~ p { }` | 选择 `<div>` 后的所有 `<p>` 元素（同级） |

### 属性选择器

| 选择器 | 示例 | 描述 |
|---|---|---|
| `[attr]` | `[target] { }` | 具有 `target` 属性的元素 |
| `[attr=value]` | `[target="_blank"] { }` | 其中 `target` 等于 `_blank` 的元素 |
| `[attr~=value]` | `[title~="flower"] { }` | 属性包含单词 `flower` |
| `[attr\|=value]` | `[lang\|="en"] { }` | 属性以 `en` 开头（精确或后接 `-`） |
| `[attr^=value]` | `a[href^="https"] { }` | 属性值以 `https` 开始 |
| `[attr$=value]` | `a[href$=".pdf"] { }` | 属性值以 `.pdf` 结尾 |
| `[attr*=value]` | `a[href*="w3schools"] { }` | 属性值包含 `w3schools` |

---

## 3. 伪类和伪元素

> 来源：https://www.w3schools.com/cssref/css_ref_pseudo_classes.php

### 伪类

伪类根据元素的状态或位置选择元素。

**链接和用户操作状态：**

| 伪类 | 描述 |
|---|---|
| `:link` | 未访问的链接 |
| `:visited` | 已访问的链接 |
| `:hover` | 正在悬停的元素 |
| `:active` | 正在激活的元素（例如点击） |
| `:focus` | 具有焦点的元素 |
| `:focus-within` | 包含焦点元素的元素 |
| `:focus-visible` | 通过键盘聚焦的元素（非鼠标） |

**表单 / 输入状态：**

| 伪类 | 描述 |
|---|---|
| `:checked` | 已选中的复选框或单选按钮 |
| `:disabled` | 禁用的表单元素 |
| `:enabled` | 启用的表单元素 |
| `:required` | 具有 `required` 属性的表单元素 |
| `:optional` | 不具有 `required` 属性的表单元素 |
| `:valid` | 具有有效值的表单元素 |
| `:invalid` | 具有无效值的表单元素 |
| `:in-range` | 输入值在指定范围内 |
| `:out-of-range` | 输入值超出指定范围 |
| `:read-only` | 具有 `readonly` 属性的元素 |
| `:read-write` | 不具有 `readonly` 属性的元素 |
| `:placeholder-shown` | 当前显示占位符文本的输入元素 |
| `:default` | 默认的表单元素 |
| `:indeterminate` | 处于不确定状态的复选框/单选按钮 |

**结构伪类：**

| 伪类 | 描述 |
|---|---|
| `:first-child` | 元素的第一个子元素 |
| `:last-child` | 元素的最后一个子元素 |
| `:nth-child(n)` | 第 n 个子元素 (`n`, `2n`, `odd`, `even`, `3n+1` 等) |
| `:nth-last-child(n)` | 从末尾开始计算的第 n 个子元素 |
| `:only-child` | 元素的唯一子元素 |
| `:first-of-type` | 元素类型在父元素中的第一个 |
| `:last-of-type` | 元素类型在父元素中的最后一个 |
| `:nth-of-type(n)` | 元素类型中的第 n 个 |
| `:nth-last-of-type(n)` | 从末尾开始计算的元素类型中的第 n 个 |
| `:only-of-type` | 元素类型在父元素中的唯一一个 |
| `:root` | 文档根元素（通常为 `<html>`） |
| `:empty` | 没有子元素或文本的元素 |

### 伪元素

伪元素用于样式化元素的特定部分。

| 伪元素 | 描述 |
|---|---|
| `::before` | 在元素内容之前插入内容 |
| `::after` | 在元素内容之后插入内容 |
| `::first-line` | 样式化块元素的首行 |
| `::first-letter` | 样式化块元素的首字母 |
| `::selection` | 样式化用户选择/高亮的部分 |
| `::placeholder` | 样式化输入框的占位符文本 |
| `::marker` | 样式化列表项的标记（项目符号/编号） |
| `::backdrop` | 样式化对话框或全屏元素背后的背景 |

---

## 4. CSS @规则

> 来源：https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/@rules

| @规则 | 描述 |
|---|---|
| `@charset` | 指定样式表的字符编码（例如 `@charset "UTF-8";`） |
| `@import` | 导入外部样式表（`@import url("style.css");`） |
| `@font-face` | 定义文档中使用的自定义字体 |
| `@keyframes` | 定义 `animation-name` 的动画关键帧 |
| `@media` | 根据媒体查询有条件地应用样式 |
| `@supports` | 仅在浏览器支持特定 CSS 特性时应用样式 |
| `@page` | 定义打印页面的样式（边距、尺寸等） |
| `@layer` | 声明层叠层以控制特异性顺序 |
| `@container` | 根据容器元素的大小应用样式 |
| `@property` | 注册自定义属性，定义其语法、继承和初始值 |
| `@scope` | 将样式限制在特定的 DOM 子树 |
| `@starting-style` | 定义元素首次出现时的 CSS 过渡样式 |
| `@counter-style` | 定义列表标记的自定义计数器样式 |

### 常见 @规则示例

```css
/* @font-face -- 定义自定义字体 */
@font-face {
  font-family: "MyFont";
  src: url("myfont.woff2") format("woff2"),
       url("myfont.woff") format("woff");
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

/* @keyframes -- 定义动画 */
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* @media -- 响应式样式 */
@media screen and (max-width: 768px) {
  .container { flex-direction: column; }
}

/* @supports -- 特性检测 */
@supports (display: grid) {
  .container { display: grid; }
}

/* @layer -- 层叠层 */
@layer base, components, utilities;
@layer base {
  body { margin: 0; }
}

/* @container -- 容器查询 */
@container (min-width: 400px) {
  .card { grid-template-columns: 1fr 1fr; }
}
```

---

## 5. CSS 样式基础

> 来源：https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics

### 什么是 CSS？

**CSS（层叠样式表）** 用于样式化和布局网页。它控制字体、颜色、大小、间距、布局、动画等视觉属性。

### CSS 语法

```css
选择器 {
  属性: 值;
  属性: 值;
}
```

一个 **规则**（或 **规则集**）由 **选择器** 和一个包含一个或多个 **声明**（属性值对）的 **声明块** 组成。

### 将 CSS 应用于 HTML

有三种方式可以应用 CSS：

1. **外部样式表**（推荐）：
   ```html
   <link rel="stylesheet" href="styles.css">
   ```

2. **内部样式表**：
   ```html
   <style>
     p { color: red; }
   </style>
   ```

3. **内联样式**（尽可能避免）：
   ```html
   <p style="color: red;">文本</p>
   ```

### 层叠、特异性和继承

- **层叠**：当多个规则作用于同一元素时，后续规则会覆盖之前的规则（其他条件相同）。
- **特异性**：更具体的规则会覆盖不具体的规则。特异性等级（从低到高）：
  - 类型选择器（`p`, `div`）和伪元素
  - 类选择器（`.intro`）、属性选择器和伪类
  - ID 选择器（`#main`）
  - 内联样式
  - `!important`（覆盖所有，慎用）
- **继承**：某些属性（主要是文本相关）会由子元素继承；其他属性（主要是布局相关）则不会。

### 值和单位

| 单位 | 类型 | 描述 |
|---|---|---|
| `px` | 绝对 | 像素（最常用的绝对单位） |
| `em` | 相对 | 相对于父元素字体大小 |
| `rem` | 相对 | 相对于根元素字体大小 |
| `%` | 相对 | 父元素值的百分比 |
| `vw` / `vh` | 相对 | 视口宽度/高度的 1% |
| `vmin` / `vmax` | 相对 | 较小/较大视口尺寸的 1% |
| `ch` | 相对 | `0` 字符的宽度 |
| `fr` | 分数 | 可用空间的分数（仅网格布局） |

### 颜色值

```css
color: red;                        /* 命名颜色 */
color: #ff0000;                    /* 十六进制 */
color: #f00;                       /* 十六进制简写 */
color: rgb(255, 0, 0);             /* RGB */
color: rgba(255, 0, 0, 0.5);      /* RGB 加透明度 */
color: rgb(255 0 0 / 50%);        /* 现代 RGB 语法 */
```

---

## 6. 盒模型

> 来源：https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model

### 四层结构

每个 CSS 元素都被一个包含四层的盒模型包围（从内到外）：

1. **内容盒** -- 显示内容；使用 `width` 和 `height` 设置
2. **内边距盒** -- 内容周围的间距；使用 `padding` 设置
3. **边框盒** -- 包裹内容和内边距；使用 `border` 设置
4. **外边距盒** -- 元素最外层的间距；使用 `margin` 设置

### 标准 vs. 替代盒模型

**标准（默认 -- `content-box`）：**
```css
.box {
  width: 350px;       /* 内容宽度 */
  padding: 25px;
  border: 5px solid black;
  margin: 10px;
}
/* 总渲染宽度：350 + 25 + 25 + 5 + 5 = 410px */
```

**替代 (`border-box`):**
```css
.box {
  box-sizing: border-box;
  width: 350px;       /* 包含内边距和边框 */
  padding: 25px;
  border: 5px solid black;
  margin: 10px;
}
/* 总渲染宽度：350px（内容区域缩小以适应） */
```

**推荐全局重置：**
```css
html {
  box-sizing: border-box;
}

*,
*::before,
*::after {
  box-sizing: inherit;
}
```

### 块级 vs. 内联 vs. 内联块

| 行为 | 块级 | 内联 | 内联块 |
|---|---|---|---|
| 换行 | 是 | 否 | 否 |
| 尊重 `width`/`height` | 是 | 否 | 是 |
| 内边距/外边距推离其他元素 | 是 | 左右仅 | 是 |
| 默认填充容器宽度 | 是 | 否 | 否 |
| 常见元素 | `div`, `p`, `h1`-`h6`, `section` | `a`, `span`, `em`, `strong` | --（通过 CSS 设置） |

### 外边距合并

相邻块级元素的垂直外边距会合并：

- **两个正外边距**：较大的值胜出
- **两个负外边距**：最小的（最负的）值胜出
- **一个正 + 一个负**：两者相减

```css
.one { margin-bottom: 50px; }
.two { margin-top: 30px; }
/* 结果：两者之间有 50px 的间距（而非 80px） */
```

### 简写符号

```css
/* 所有四个边 */
margin: 10px;                      /* 所有边 10px */
margin: 10px 20px;                 /* 垂直 10px，水平 20px */
margin: 10px 20px 30px;            /* 上 10px，水平 20px，下 30px */
margin: 10px 20px 30px 40px;       /* 上、右、下、左（顺时针） */
```

---

## 7. 弹性布局

> 来源：https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Flexbox

弹性布局是一种 **一维** 布局方法，用于在行或列中排列项目。

### 轴

- **主轴**：项目排列的方向（默认为水平）
- **交叉轴**：与主轴垂直（默认为垂直）

### 容器属性

```css
.container {
  display: flex;               /* 或 inline-flex */

  /* 方向 */
  flex-direction: row;         /* row | row-reverse | column | column-reverse */

  /* 换行控制 */
  flex-wrap: nowrap;           /* nowrap | wrap | wrap-reverse */

  /* 主轴和换行的简写 */
  flex-flow: row wrap;

  /* 主轴对齐 */
  justify-content: flex-start; /* flex-start | flex-end | center |
                                  space-between | space-around | space-evenly */

  /* 交叉轴对齐 */
  align-items: stretch;        /* stretch | flex-start | flex-end |
                                  center | baseline */

  /* 多行交叉轴对齐（当换行时） */
  align-content: stretch;      /* stretch | flex-start | flex-end | center |
                                  space-between | space-around */

  /* 弹性项目之间的间距 */
  gap: 10px;                   /* 行间距和列间距的简写 */
}
```

### 项目属性

```css
.item {
  /* 增长/缩小行为（简写） */
  flex: 1;                     /* flex-grow: 1, flex-shrink: 1, flex-basis: 0 */
  flex: 1 200px;               /* flex-grow: 1, flex-basis: 200px */

  /* 视觉顺序 */
  order: 0;                    /* 低值先显示；默认为 0 */

  /* 项目在单元格内的对齐 */
  align-self: auto;            /* auto | flex-start | flex-end | center |
                                  baseline | stretch */
}
```

### 常见模式

```css
/* 等宽列 */
.item { flex: 1; }

/* 垂直和水平居中 */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 响应式换行布局 */
.container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.item {
  flex: 1 1 300px;   /* 可增长，可缩小，最小宽度 300px */
}

/* 粘性页脚布局 */
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
main { flex: 1; }
```

---

## 8. 网格布局

> 来源：https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Grids

CSS Grid 是一种 **二维** 布局系统，用于将内容组织成行和列。

### 容器属性

```css
.container {
  display: grid;               /* 或 inline-grid */

  /* 定义列和行 */
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;

  /* 定义命名区域 */
  grid-template-areas:
    "header  header  header"
    "sidebar content content"
    "footer  footer  footer";

  /* 行列间距的简写 */
  gap: 20px;
  column-gap: 20px;
  row-gap: 20px;

  /* 隐式创建的行列大小 */
  grid-auto-rows: minmax(100px, auto);
  grid-auto-columns: 1fr;

  /* 自动放置算法 */
  grid-auto-flow: row;         /* row | column | dense */

  /* 项目在单元格内的对齐 */
  justify-items: stretch;      /* start | end | center | stretch */
  align-items: stretch;        /* start | end | center | stretch */

  /* 网格在容器内的对齐 */
  justify-content: start;      /* start | end | center | stretch |
                                  space-between | space-around | space-evenly */
  align-content: start;
}
```

### 关键函数

| 函数 | 描述 |
|---|---|
| `repeat(count, size)` | 重复轨道定义（例如 `repeat(3, 1fr)`） |
| `minmax(min, max)` | 设置轨道的最小和最大尺寸 |
| `auto-fill` | 根据容器创建尽可能多的轨道（空轨道保留） |
| `auto-fit` | 根据容器创建尽可能多的轨道，然后压缩空轨道 |
| `fit-content(max)` | 将轨道尺寸调整为内容大小，不超过最大值 |

### `fr` 单位

`fr` 单位代表可用空间的一个分数：
```css
grid-template-columns: 2fr 1fr 1fr;
/* 第一列占 50%，其余各占 25% */
```

### 项目属性

```css
.item {
  /* 通过行号定位 */
  grid-column: 1 / 3;         /* 从行 1 开始，到行 3 结束 */
  grid-row: 1 / 2;

  /* 通过跨度定位 */
  grid-column: 1 / span 2;    /* 从行 1 开始，跨越 2 列 */

  /* 全宽项目 */
  grid-column: 1 / -1;        /* 从行 1 到最后一行 */

  /* 项目定位到命名区域 */
  grid-area: header;

  /* 单个项目在单元格内的对齐 */
  justify-self: center;       /* start | end | center | stretch */
  align-self: center;
}
```

### 命名网格区域示例

```css
.container {
  display: grid;
  grid-template-columns: 1fr 3fr;
  grid-template-areas:
    "header  header"
    "sidebar content";
}
header  { grid-area: header; }
aside   { grid-area: sidebar; }
main    { grid-area: content; }
footer  { grid-area: footer; }
```

### 子网格

网格项目可以继承父元素的轨道定义：
```css
.nested {
  display: grid;
  grid-template-columns: subgrid;
}
```

### 显式 vs. 隐式网格

- **显式网格**：通过 `grid-template-columns` / `grid-template-rows` 定义轨道
- **隐式网格**：为溢出内容自动生成轨道，由 `grid-auto-rows` / `grid-auto-columns` 控制

---

## 9. 媒体查询

> 来源：https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Media_queries

### 语法

```css
@media 媒体类型 and (媒体特征) {
  /* CSS 规则 */
}
```

### 常见媒体类型

| 类型 | 描述 |
|---|---|
| `all` | 所有设备（默认） |
| `screen` | 屏幕（显示器、手机、平板） |
| `print` | 打印预览和打印页面 |

### 常见媒体特征

| 特征 | 描述 | 示例 |
|---|---|---|
| `width` / `min-width` / `max-width` | 视口宽度 | `(min-width: 768px)` |
| `height` / `min-height` / `max-height` | 视口高度 | `(min-height: 600px)` |
| `orientation` | 横屏或竖屏 | `(orientation: landscape)` |
| `hover` | 用户是否可以悬停 | `(hover: hover)` |
| `pointer` | 指针设备的精度 | `(pointer: fine)` 或 `(pointer: coarse)` |
| `prefers-color-scheme` | 用户的色彩方案偏好 | `(prefers-color-scheme: dark)` |
| `prefers-reduced-motion` | 用户偏好减少动画 | `(prefers-reduced-motion: reduce)` |
| `aspect-ratio` | 视口的宽高比 | `(aspect-ratio: 16/9)` |
| `resolution` | 设备像素密度 | `(min-resolution: 2dppx)` |

### 逻辑操作符

```css
/* AND -- 所有条件必须为真 */
@media screen and (min-width: 600px) and (orientation: landscape) { }

/* OR -- 逗号分隔；任一条件为真即可 */
@media (min-width: 600px), (orientation: landscape) { }

/* NOT -- 否定整个查询 */
@media not screen and (min-width: 600px) { }

/* 范围语法（现代） */
@media (30em <= width <= 50em) { }
```

### 移动优先响应式设计

从移动端样式开始，然后为更大的屏幕添加复杂性：

```css
/* 基础样式（移动端） */
.container {
  width: 90%;
  margin: 0 auto;
}

/* 中等屏幕（平板） */
@media screen and (min-width: 40em) {
  .container {
    display: grid;
    grid-template-columns: 3fr 1fr;
    gap: 20px;
  }

  nav ul {
    display: flex;
  }
}

/* 大屏幕（桌面） */
@media screen and (min-width: 70em) {
  .container {
    max-width: 1200px;
  }
}
```

### 视口元标签（必需）

始终在 HTML `<head>` 中包含此标签以实现移动端的响应式设计：

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### 常见断点

虽然没有通用断点，但常用的值包括：

| 标签 | 断点 |
|---|---|
| 小手机 | `< 576px` |
| 手机 / 大手机 | `>= 576px` |
| 平板 | `>= 768px` |
| 桌面 | `>= 992px` |
| 大桌面 | `>= 1200px` |
| 超大 | `>= 1400px` |

**最佳实践**：不要针对特定设备，而是在内容需要时添加断点——当行长度过长或布局失效时。

### 不使用媒体查询的响应式设计

现代 CSS 布局方法本身可以是响应式的：

```css
/* 自动响应式网格——无需媒体查询 */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

/* 流动字体 */
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);
}
```

---

## 快速语法速查表

```css
/* 变量（自定义属性） */
:root {
  --primary: #3498db;
  --spacing: 1rem;
}
.element {
  color: var(--primary);
  padding: var(--spacing);
}

/* 嵌套（现代 CSS） */
.card {
  background: white;
  & .title {
    font-size: 1.5rem;
  }
  &:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
}

/* 逻辑属性 */
margin-inline: auto;          /* 左右外边距 */
margin-block: 1rem;           /* 上下外边距 */
padding-inline-start: 1rem;   /* 左（LTR）或右（RTL）内边距 */

/* 容器查询 */
.card-container {
  container-type: inline-size;
}
@container (min-width: 400px) {
  .card { grid-template-columns: 1fr 1fr; }
}

/* 滚动捕捉 */
.scroll-container {
  scroll-snap-type: x mandatory;
}
.scroll-item {
  scroll-snap-align: start;
}
```

---

*本参考内容来源于 w3schools.com 和 developer.mozilla.org（MDN Web 文档）。如需完整细节，请访问每个部分上方列出的源链接。*

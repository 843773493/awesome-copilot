# 网页性能参考指南

涵盖网页性能概念、优化技术以及性能 API 的综合参考指南，内容来源于 Mozilla 开发者网络（MDN）。

---

## 目录

1. [网页性能概述](#1-网页性能概述)
2. [性能基础](#2-性能基础)
3. [性能最佳实践](#3-性能最佳实践)
4. [HTML 性能](#4-html-性能)
5. [JavaScript 性能](#5-javascript-性能)
6. [CSS 性能](#6-css-性能)
7. [性能 API](#7-性能-api)
8. [性能数据](#8-性能数据)
9. [服务器时间](#9-服务器时间)
10. [用户时间](#10-用户时间)

---

## 1. 网页性能概述

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/Performance>

### 定义

**网页性能**包括：

- 客观测量指标（加载时间、每秒帧数、首次交互时间）
- 用户对加载和响应时间的感知体验
- 用户交互期间的流畅性（滚动、动画、按钮响应）

### 推荐时间阈值

| 目标 | 阈值 |
|------|------|
| 页面加载提示 | 1 秒 |
| 空闲状态 | 50ms |
| 动画 | 16.7ms（60 FPS） |
| 用户输入响应 | 50-200ms |

用户会放弃响应缓慢的网站。目标是减少加载和响应时间，同时通过最大化可用性和交互性来隐藏延迟。

### 关键性能指标

| 指标 | 全称 | 定义 |
|------|------|------|
| **FCP** | 首次内容绘制 | 首次内容出现的时间 |
| **LCP** | 最大内容绘制 | 可见的最大内容元素 |
| **CLS** | 可视稳定性 | 交互期间的视觉稳定性 |
| **INP** | 交互到下一次绘制 | 用户输入的响应性 |
| **TTFB** | 首字节时间 | 服务器响应时间 |
| **TTI** | 首次交互时间 | 页面完全可交互的时间 |
| **Jank** | -- | 非流畅的动画或滚动 |

### 性能 API 类别

- **高精度计时**：通过稳定的单调时钟进行毫秒级监控
- **导航计时**：页面导航的指标（DOMContentLoaded、加载时间）
- **资源计时**：单个资源的详细网络计时
- **用户计时**：自定义标记和测量
- **长动画帧（LoAF）**：识别卡顿动画
- **服务器计时**：后端性能指标

### 相关浏览器 API

- **页面可见性 API**：跟踪文档可见性状态
- **后台任务 API** (`requestIdleCallback()`)：排队非阻塞任务
- **Intersection Observer API**：异步监控元素可见性
- **网络信息 API**：检测连接类型以实现自适应内容
- **电池状态 API**：优化低电量设备
- **Beacon API**：将性能数据发送到分析服务
- **媒体能力 API**：检查设备的媒体支持

### 资源加载提示

- **DNS 预解析**：预解析域名
- **预连接**：提前建立连接
- **预获取**：在需要前加载资源
- **预加载**：提前加载关键资源

### 监控方法

- **真实用户监控（RUM）**：从实际用户中分析长期趋势
- **合成监控**：在开发过程中进行受控回归测试

---

## 2. 性能基础

> **来源:** <https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance>

### 为什么网页性能重要

- 促进可访问性和包容性设计
- 提升用户体验和留存率
- 直接影响业务目标和转化率

### 核心组件

- 网页加载性能
- 浏览器中内容的渲染
- 用户代理的能力和限制
- 不同用户群体的性能表现

### 感知性能

关注用户感知而非原始毫秒数的指标：

- **页面加载时间** -- 初始内容可用性
- **响应性** -- 交互反馈速度
- **动画流畅性** -- 视觉平滑度
- **滚动流畅性** -- 滚动交互质量

### 优化领域

| 领域 | 重点 | 影响 |
|------|------|------|
| **多媒体（图片）** | 基于设备能力、尺寸和像素密度的媒体优化 | 减少每张图片的字节数 |
| **多媒体（视频）** | 视频压缩、从背景视频中移除音频轨道 | 减少文件大小 |
| **JavaScript** | 交互体验的最佳实践 | 提升响应速度和电池寿命 |
| **HTML** | 减少 DOM 节点、优化属性顺序 | 提升加载和渲染时间 |
| **CSS** | 针对特定功能的优化 | 避免产生负面影响 |

### 性能策略

- **性能预算**：设置资源大小限制
- **性能文化**：组织承诺
- **防止回归**：避免随着时间推移导致臃肿
- **移动优先方法**：响应式图片和自适应媒体交付

---

## 3. 性能最佳实践

> **来源:** <https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/Best_practices>

### 核心最佳实践

1. **了解关键渲染路径** -- 理解浏览器如何渲染页面以优化性能
2. **使用资源提示** -- `rel=preconnect`, `rel=dns-prefetch`, `rel=prefetch`, `rel=preload`
3. **最小化 JavaScript** -- 仅加载当前页面所需的 JavaScript
4. **优化 CSS** -- 处理 CSS 性能因素，尽可能异步加载 CSS
5. **使用 HTTP/2** -- 在服务器或 CDN 上部署 HTTP/2
6. **使用 CDN** -- 显著减少资源加载时间
7. **压缩资源** -- 使用 gzip、Brotli 或 Zopfli 压缩
8. **优化图片** -- 尽可能使用 CSS 动画或 SVG
9. **实现延迟加载** -- 延迟加载视口外的内容；在 `<img>` 元素上使用 `loading` 属性
10. **关注用户感知** -- 感知性能与实际时间同样重要

### 异步加载 CSS

```html
<link
  id="my-stylesheet"
  rel="stylesheet"
  href="/path/to/my.css"
  media="print" />
<noscript><link rel="stylesheet" href="/path/to/my.css" /></noscript>
```

```javascript
const stylesheet = document.getElementById("my-stylesheet");
stylesheet.addEventListener("load", () => {
  stylesheet.media = "all";
});
```

### 内联关键 CSS

- 使用 `<style>` 标签内联视口上方内容的 CSS
- 防止未样式化文本闪烁（FOUT）
- 提升感知性能

### HTML 中的 JavaScript 加载

**`async` 属性** -- 与 DOM 解析并行获取，不阻塞渲染：

```html
<script async src="index.js"></script>
```

**`defer` 属性** -- 在文档解析完成后执行，但在 `DOMContentLoaded` 事件之前。

**模块加载** -- 将代码拆分为模块并按需加载。

### 资源预加载

```html
<link rel="preload" href="sintel-short.mp4" as="video" type="video/mp4" />
```

其他用于性能的 `rel` 属性：

- `rel="dns-prefetch"` -- 预解析 DNS 查询
- `rel="preconnect"` -- 预建立连接
- `rel="modulepreload"` -- 预加载 JavaScript 模块
- `rel="prefetch"` -- 为未来导航加载资源

### 资源加载顺序

1. **HTML** 按源顺序首先被解析
2. **CSS** 被解析；链接的资源（图片、字体等）开始获取
3. **JavaScript** 被解析和执行（默认会阻塞后续 HTML 解析）
4. **样式计算** 对 HTML 元素进行计算
5. **渲染** 已样式化的内容到屏幕

### 关键要点

HTML 默认简单且快速。应关注：

- 减少下载的字节数（图片和视频）
- 控制资源加载顺序（async、defer、preload）
- 减少不必要的嵌入内容（iframe）
- 响应式提供替换元素（srcset、picture、媒体查询）

HTML 文件大小压缩相比优化媒体资源带来的收益微乎其微。

---

## 4. HTML 性能

> **来源:** <https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/HTML>

### 主要 HTML 相关性能瓶颈

- 图片和视频文件大小（替换元素）
- 嵌入内容的交付（`<iframe>` 元素）
- 资源加载顺序

### 响应式图片处理

**使用 `srcset` 和 `sizes` 以适应不同屏幕宽度：**

```html
<img
  srcset="480w.jpg 480w, 800w.jpg 800w"
  sizes="(width <= 600px) 480px, 800px"
  src="800w.jpg"
  alt="家庭肖像" />
```

**使用 `srcset` 以适应不同设备分辨率：**

```html
<img
  srcset="320w.jpg, 480w.jpg 1.5x, 640w.jpg 2x"
  src="640w.jpg"
  alt="家庭肖像" />
```

**使用 `<picture>` 元素：**

```html
<picture>
  <source media="(width < 800px)" srcset="narrow-banner-480w.jpg" />
  <source media="(width >= 800px)" srcset="wide-banner-800w.jpg" />
  <img src="large-banner-800w.jpg" alt="茂密森林场景" />
</picture>
```

### 延迟加载

**图片：**

```html
<img src="800w.jpg" alt="家庭肖像" loading="lazy" />
```

**视频（禁用预加载）：**

```html
<video controls preload="none" poster="poster.jpg">
  <source src="video.webm" type="video/webm" />
  <source src="video.mp4" type="video/mp4" />
</video>
```

**iframe：**

```html
<iframe src="https://example.com" loading="lazy" width="600" height="400"></iframe>
```

### iframe 最佳实践

除非绝对必要，否则避免嵌入 `<iframe>` 元素。问题包括：

- 需要额外的 HTTP 请求
- 创建独立页面实例（成本高）
- 无法共享缓存资源
- 需要单独处理 CSS 和 JavaScript

**替代方案**：使用 `fetch()` 和 DOM 脚本将内容加载到同一页面中。

### HTML 中的 JavaScript 加载

**`async` 属性** -- 与 DOM 解析并行获取，不阻塞渲染：

```html
<script async src="index.js"></script>
```

**`defer` 属性** -- 在文档解析完成后执行，但在 `DOMContentLoaded` 事件之前。

**模块加载** -- 将代码拆分为模块并按需加载。

### 资源预加载

```html
<link rel="preload" href="style.css" as="style" />
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin />
```

### 资源加载顺序

| 资源类型 | 最大缓冲区大小 |
|----------|----------------|
| `"resource"` | 250（可调整） |
| `"longtask"` | 200 |
| `"element"` | 150 |
| `"event"` | 150 |
| `"layout-shift"` | 150 |
| `"largest-contentful-paint"` | 150 |
| `"visibility-state"` | 50 |
| `"mark"` | 无限 |
| `"measure"` | 无限 |
| `"navigation"` | 无限 |
| `"paint"` | 2（固定） |
| `"first-input"` | 1（固定） |

### 处理丢弃的条目

```javascript
function perfObserver(list, observer, droppedEntriesCount) {
  list.getEntries().forEach((entry) => {
    // 处理条目
  });
  if (droppedEntriesCount > 0) {
    console.warn(
      `${droppedEntriesCount} 条目因缓冲区已满而被丢弃。`
    );
  }
}
const observer = new PerformanceObserver(perfObserver);
observer.observe({ type: "resource", buffered: true });
```

### JSON 序列化

所有性能条目都提供 `toJSON()` 方法：

```javascript
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    console.log(entry.toJSON());
  });
});
observer.observe({ type: "event", buffered: true });
```

### 需要显式配置的指标

- **元素计时**：在元素上添加 `elementtiming` 属性
- **用户计时**：在相关点调用性能 API 方法
- **服务器计时**：服务器发送 `Server-Timing` HTTP 头

---

## 9. 服务器时间

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/Server_timing>

### 什么是服务器时间？

服务器时间是性能 API 的一部分，允许服务器向用户代理传递请求-响应周期的指标。它会暴露后端服务器的计时指标，如数据库读写时间、CPU 时间和文件系统访问时间。

### 服务器-Timing HTTP 头示例

```http
// 单个指标无值
Server-Timing: missedCache

// 单个指标带值
Server-Timing: cpu;dur=2.4

// 单个指标带描述和值
Server-Timing: cache;desc="缓存读取";dur=23.2

// 两个指标带值
Server-Timing: db;dur=53, app;dur=47.2

// 服务器-Timing 作为尾部
Trailer: Server-Timing
--- 响应体 ---
Server-Timing: total;dur=123.4
```

### 在 JavaScript 中获取服务器指标

服务器时间指标存储为 `PerformanceServerTiming` 条目，通过 `PerformanceResourceTiming.serverTiming` 属性在 `"navigation"` 和 `"resource"` 性能条目中访问。

```javascript
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    entry.serverTiming.forEach((serverEntry) => {
      console.log(
        `${serverEntry.name} (${serverEntry.description}) 持续时间: ${serverEntry.duration}`
      );
      // 输出 "cache (缓存读取) 持续时间: 23.2"
      // 输出 "db () 持续时间: 53"
      // 输出 "app () 持续时间: 47.2"
    });
  });
});

["navigation", "resource"].forEach((type) =>
  observer.observe({ type, buffered: true })
);
```

### 隐私和安全考虑

- `Server-Timing` 头可能暴露敏感的应用和基础设施信息；指标应仅返回给认证用户
- `PerformanceServerTiming` 默认仅限于同源
- 使用 `Timing-Allow-Origin` 头指定允许的跨域域名
- 在某些浏览器中仅在安全上下文（HTTPS）中可用
- 服务器、客户端和中间代理之间没有时钟同步；服务器时间戳可能无法准确映射到客户端时间线 `startTime`

---

## 10. 用户时间

> **来源:** <https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/User_timing>

### 概述

用户时间是性能 API 的一部分，允许您使用高精度时间戳测量应用程序性能。它包含两个主要组件：

- **`PerformanceMark`** 条目 -- 在应用程序中的任意位置添加命名标记
- **`PerformanceMeasure`** 条目 -- 在两个标记之间进行时间测量

### 添加性能标记

```javascript
// 基础标记
performance.mark("登录开始");
performance.mark("登录结束");

// 高级标记带选项
performance.mark("登录开始", {
  startTime: 12.5,
  detail: { htmlElement: myElement.id },
});
```

### 测量标记间的持续时间

```javascript
const loginMeasure = performance.measure(
  "登录持续时间",
  "登录开始",
  "登录结束"
);
console.log(loginMeasure.duration);
```

**从事件时间戳到标记的高级测量：**

```javascript
loginButton.addEventListener("click", (clickEvent) => {
  fetch(loginURL).then((data) => {
    renderLoggedInUser(data);
    const marker = performance.mark("登录结束");
    performance.measure("登录点击", {
      detail: { htmlElement: myElement.id },
      start: clickEvent.timeStamp,
      end: marker.startTime,
    });
  });
});
```

### 观察性能测量

```javascript
function perfObserver(list, observer) {
  list.getEntries().forEach((entry) => {
    if (entry.entryType === "mark") {
      console.log(`${entry.name} 的 startTime: ${entry.startTime}`);
    }
    if (entry.entryType === "measure") {
      console.log(`${entry.name} 的持续时间: ${entry.duration}`);
    }
  });
}
const observer = new PerformanceObserver(perfObserver);
observer.observe({ entryTypes: ["measure", "mark"] });
```

### 获取标记和测量

```javascript
// 所有条目
const entries = performance.getEntries();

// 按类型过滤
const marks = performance.getEntriesByType("mark");
const measures = performance.getEntriesByType("measure");

// 按名称获取
const debugMarks = performance.getEntriesByName("debug-mark", "mark");
```

### 移除标记和测量

```javascript
// 清除所有标记
performance.clearMarks();

// 移除特定标记
performance.clearMarks("myMarker");

// 清除所有测量
performance.clearMeasures();

// 移除特定测量
performance.clearMeasures("myMeasure");
```

### 相比 Date.now() 和 performance.now() 的优势

- 更有意义的名称以提高组织性
- 与浏览器开发者工具（性能面板）集成
- 与其他性能 API（如 `PerformanceObserver`）无缝协作
- 更好的工具集成整体性

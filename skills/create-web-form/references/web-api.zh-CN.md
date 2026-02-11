# Web API 参考文档

> 来源: <https://developer.mozilla.org/en-US/docs/Web/API>

## 概述

Web API 是为网页应用提供的编程接口，通常与 JavaScript 一起使用。它们使开发者能够构建现代网页应用，实现以前仅限于原生应用的功能（如摄像头访问、离线支持、后台处理等）。

## API 分类

### 音频与可访问性

- **音频输出设备 API** -- 选择音频输出设备（实验性）。

### 后台与蓝牙

- **后台获取 API** -- 管理长时间下载。
- **后台同步 API** -- 在后台同步数据。
- **徽章 API** -- 在应用图标上显示徽章。
- **信标 API** -- 发送分析数据。
- **Web 蓝牙 API** -- 连接到蓝牙设备。

### 画布、CSS 与通信

- **画布 API** -- 在网页上进行 2D 绘图。
- **CSS API**（绘画、字体加载、类型化对象模型）。
- **剪贴板 API** -- 访问剪贴板数据。
- **控制台 API** -- 调试工具。
- **Cookie 存储 API** -- 管理 Cookie。
- **凭证管理 API** -- 处理身份验证。

### DOM 与设备

- **文档对象模型（DOM）** -- 操纵页面结构的核心 Web API。
- **设备运动/方向事件** -- 访问设备传感器。
- **设备内存 API** -- 检测设备能力。

### 获取与文件系统

- **Fetch API** -- 现代 HTTP 请求。
- **文件 API** -- 访问文件数据。
- **文件系统 API** -- 操作本地文件。
- **全屏 API** -- 进入全屏模式。

### 地理定位与图形

- **地理定位 API** -- 获取用户位置。
- **游戏手柄 API** -- 连接游戏控制器。
- **WebGL** -- 3D 图形渲染。
- **WebGPU API** -- GPU 计算。

### 历史记录与 HTML

- **历史记录 API** -- 浏览器历史记录导航。
- **HTML DOM API** -- 操作 HTML 元素。
- **HTML 拖放 API** -- 原生拖放支持。

### 输入与 IndexedDB

- **IndexedDB API** -- 客户端结构化数据库。
- **Intersection Observer API** -- 跟踪元素可见性。

### 媒体与媒体流

- **媒体捕获与流 API** -- 访问摄像头和麦克风。
- **媒体流录制 API** -- 录制音频和视频。
- **媒体会话 API** -- 控制播放。
- **媒体源扩展** -- 流式传输媒体内容。

### 导航与网络

- **导航 API** -- 客户端路由。
- **网络信息 API** -- 检测连接类型。

### 支付与性能

- **支付请求 API** -- 支付流程处理。
- **性能 API** -- 监控应用性能。
- **权限 API** -- 请求功能权限。
- **画中画 API** -- 浮动视频播放器。
- **指针事件** -- 处理输入设备。
- **推送 API** -- 接收推送通知。

### 存储与传感器

- **服务工作者 API** -- 离线功能。
- **存储 API** -- 持久化存储。
- **流 API** -- 操作数据流。
- **屏幕捕获 API** -- 录制屏幕内容。

### 视频与虚拟现实

- **视图过渡 API** -- 动画页面过渡。
- **WebXR 设备 API** -- VR/AR 体验。

### WebSocket 与 Web Workers

- **WebSocket API** -- 实时双向通信。
- **Web Workers API** -- 后台处理。
- **Web 音频 API** -- 音频处理与合成。
- **Web 认证 API** -- WebAuthn 支持。
- **Web 存储 API** -- `localStorage` 和 `sessionStorage`。

### XML

- **XMLHttpRequest API** -- 旧版 HTTP 请求（已被 Fetch 大量取代）。

## 关键接口示例

### 核心 DOM 接口

```javascript
Document, Element, HTMLElement
Node, NodeList
DocumentFragment
Attr, NamedNodeMap
```

### 事件处理

```javascript
Event, EventTarget, CustomEvent
MouseEvent, KeyboardEvent, TouchEvent
PointerEvent, DragEvent
```

### 异步操作

```javascript
// 基于 Promise 的 API
AbortController, AbortSignal
Fetch, Request, Response
```

### 媒体与图形

```javascript
HTMLMediaElement, AudioContext
Canvas, CanvasRenderingContext2D
WebGL2RenderingContext, GPU
```

### 存储与数据库

```javascript
Storage             // localStorage, sessionStorage
IndexedDB           // IDBDatabase, IDBTransaction
CacheStorage        // 服务工作者缓存
```

## 关键概念

1. **渐进增强** -- API 在旧版浏览器上会优雅降级。
2. **基于标准** -- 遵循 W3C 和 WHATWG 规范。
3. **实验性 API** -- 标记为仍在开发中的功能；可能发生变化或被移除。
4. **已弃用的 API** -- 正在淘汰的旧功能；避免在新项目中使用。
5. **非标准 API** -- 浏览器特定实现；谨慎使用。

## 重要注意事项

- Web API 通常与 JavaScript 一起使用，但并不局限于它。
- 许多 API 需要 **用户权限**（地理定位、摄像头、麦克风）。
- 一些 API 是 **实验性**，可能发生变化或被移除。
- 浏览器对 API 的支持情况各不相同 -- 使用前请务必检查兼容性。
- 旧版已弃用的 API 应避免在新项目中使用。

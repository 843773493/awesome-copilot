# 进阶网络应用参考

---

## 概述：什么是渐进式网络应用？

> 来源：[https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)

**渐进式网络应用（Progressive Web App，简称 PWA）** 是一种使用网络平台技术构建的应用，能够提供与平台特定（原生）应用相当的用户体验。其关键特性包括：

- 从单一代码库运行于多个平台和设备
- 可以像原生应用一样安装在设备上
- 支持离线操作和后台运行
- 集成设备功能和其他已安装应用
- 作为操作系统中的永久功能，用户可直接从系统启动

### 主要指南

| 指南 | 描述 |
|------|------|
| **什么是渐进式网络应用？** | 与传统网站和平台特定应用的比较；介绍主要的 PWA 特性 |
| **使 PWA 可安装** | 安装性要求、设备安装流程、自定义安装体验 |
| **安装和卸载网络应用** | 用户如何在其设备上安装和卸载 PWA |
| **离线和后台操作** | 支持离线功能的技术、间歇性网络连接管理、后台任务执行 |
| **缓存** | 本地资源缓存的 API、用于离线功能的常见缓存策略 |
| **渐进式网络应用最佳实践** | 跨浏览器和设备适配、可访问性、性能优化、操作系统集成 |

### 实现指南中的功能

| 功能 | 目的 |
|------|------|
| 创建独立应用 | 在专用窗口中启动，而非浏览器标签页 |
| 定义应用图标 | 为已安装的 PWA 自定义图标 |
| 自定义应用颜色 | 设置背景色和主题颜色 |
| 显示徽章 | 在应用图标上显示徽章（例如通知计数） |
| 暴露应用快捷方式 | 从操作系统快捷菜单访问常用操作 |
| 在应用间共享数据 | 使用操作系统应用共享机制 |
| 触发安装 | 提供自定义 UI 邀请用户安装 |
| 关联文件 | 将文件类型连接到 PWA 以进行处理 |

### 核心技术和 API

#### Web 应用清单（Web App Manifest）

- 定义 PWA 的元数据和外观
- 自定义深度操作系统集成（名称、图标、显示模式、颜色等）

#### 服务工作者 API

**通信：**

- `Client.postMessage()` -- 服务工作者向 PWA 发送消息
- 广播通道 API（Broadcast Channel API）-- 服务工作者与客户端之间的双向通信

**离线操作：**

- `Cache` API -- 持久化存储 HTTP 响应以便离线重用
- `Clients` -- 访问由服务工作者控制的文档的接口
- `FetchEvent` -- 拦截 HTTP 请求并启用缓存或代理响应以支持离线功能

**后台任务：**

- 后台同步 API（Background Synchronization API）-- 将任务延迟到网络连接稳定时执行
- Web 周期性后台同步 API（Web Periodic Background Synchronization API）-- 注册周期性任务以在网络连接时运行
- 后台下载 API（Background Fetch API）-- 管理长时间下载（如视频和音频文件）

#### 其他关键的 Web API

| API | 目的 |
|-----|------|
| **IndexedDB** | 用于结构化数据和文件的客户端存储 |
| **徽章 API** | 设置应用图标的徽章以指示通知 |
| **通知 API** | 在操作系统级别显示系统通知 |
| **Web 分享 API** | 将文本、链接、文件和内容分享到用户选择的应用 |
| **窗口控制覆盖 API** | 隐藏标题栏并在整个窗口区域显示应用（适用于桌面 PWA） |

### 必备的 PWA 检查清单

- 可安装且独立运行
- 通过服务工作者实现离线功能
- 实现了缓存策略
- 配置了 Web 应用清单
- 定义了应用图标和颜色
- 可访问且性能良好
- 跨浏览器兼容
- 安全（需 HTTPS）

---

## 教程

> 来源：[https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Tutorials](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Tutorials)

这些教程提供了从头到尾构建 PWA 的结构化、分步骤的学习路径。

### 教程 1：CycleTracker — 创建您的第一个 PWA

**难度等级：** 初学者

一个月经周期跟踪应用，逐步演示如何将一个网页应用转变为 PWA。

**子模块：**

1. **基础 HTML 和 CSS** -- 构建网页应用的基础结构
2. **安全连接** -- 设置 HTTPS 测试环境
3. **JavaScript 功能** -- 添加交互性和应用逻辑
4. **清单与图标** -- 创建并检查 Web 应用清单；定义图标
5. **使用服务工作者实现离线支持** -- 添加服务工作者并管理过期缓存

**涵盖主题：**

- 创建功能性网页应用所需的 HTML、CSS 和 JavaScript 基础知识
- 设置测试环境
- 将网页应用升级为 PWA
- 清单开发：创建和检查 Web 应用清单
- 服务工作者：将服务工作者添加到应用中
- 缓存管理：使用服务工作者删除过期缓存

### 教程 2：js13kGames — 深入探讨 PWA

**难度等级：** 中级

一个游戏信息列表应用（来自 2017 年 js13kGames 大赛），探索高级 PWA 功能。

**子模块：**

1. **PWA 结构** -- 理解应用架构和组织方式
2. **使用服务工作者实现离线支持** -- 实现离线功能
3. **使 PWA 可安装** -- 满足安装性要求
4. **使用通知和推送 API** -- 实现推送通知
5. **渐进式加载** -- 优化加载性能

**涵盖主题：**

- PWA 基础和核心概念
- 通知和推送 API：实现通知和推送功能
- 应用性能：优化 PWA 性能
- 超出基础的高级 PWA 功能

---

## API 和清单参考

> 来源：[https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Reference](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Reference)

### Web 应用清单成员

Web 应用清单描述了 PWA 的特性，自定义其外观，并启用更深入的操作系统集成。以下成员可以在清单 JSON 文件中定义：

| 成员 | 状态 | 描述 |
|------|------|------|
| `name` | 标准 | 应用的完整名称 |
| `short_name` | 标准 | 用于空间受限环境的简短名称 |
| `description` | 标准 | 应用的描述 |
| `start_url` | 标准 | 应用启动时加载的 URL |
| `scope` | 标准 | PWA 的导航范围 |
| `display` | 标准 | 显示模式（全屏、独立、最小化界面、浏览器） |
| `display_override` | 实验性 | 覆盖显示模式偏好 |
| `orientation` | 标准 | 应用的默认方向 |
| `icons` | 标准 | 用于不同场景的图标对象数组 |
| `screenshots` | 标准 | 用于应用商店和安装界面的截图 |
| `background_color` | 标准 | 启动画面的背景颜色 |
| `theme_color` | 标准 | 应用的默认主题颜色 |
| `categories` | 标准 | 预期的应用类别 |
| `id` | 标准 | 应用的唯一标识符 |
| `shortcuts` | 标准 | 快速访问关键任务的快捷方式 |
| `file_handlers` | 实验性 | 应用可处理的文件类型 |
| `launch_handler` | 实验性 | 控制应用启动方式 |
| `protocol_handlers` | 实验性 | 应用可处理的 URL 协议 |
| `share_target` | 实验性 | 定义应用接收共享数据的方式 |
| `scope_extensions` | 实验性 | 扩展导航范围 |
| `note_taking` | 实验性 | 笔记应用集成 |
| `related_applications` | 实验性 | 相关的原生应用 |
| `prefer_related_applications` | 实验性 | 优先选择原生应用而非 PWA |
| `serviceworker` | 实验性 / 非标准 | 服务工作者注册信息 |

### 服务工作者 API

#### 与应用的通信

- **`Client.postMessage()`** -- 从服务工作者向客户端页面发送消息
- 广播通道 API（Broadcast Channel API）-- 在服务工作者和客户端 PWA 之间创建双向通信通道

#### 离线操作

- **`Cache`** -- 持久化存储 HTTP 响应以便离线重用
- **`Clients`** -- 访问由服务工作者控制的文档的接口
- **`FetchEvent`** -- 拦截 HTTP 请求；启用缓存或代理响应以支持离线功能

#### 后台操作

- 后台同步 API（Background Synchronization API）-- 将任务延迟到网络连接稳定时执行
- Web 周期性后台同步 API（Web Periodic Background Synchronization API）-- 注册周期性任务以在网络连接时运行
- 后台下载 API（Background Fetch API）-- 管理长时间下载（如视频和音频文件）

### 其他用于 PWA 的 Web API

| API | 目的 |
|-----|------|
| **IndexedDB** | 用于结构化数据和文件的客户端存储 |
| **徽章 API** | 设置应用图标的徽章以指示通知 |
| **通知 API** | 在操作系统级别显示系统通知 |
| **Web 分享 API** | 将文本、链接、文件和内容分享到用户选择的应用 |
| **窗口控制覆盖 API** | 隐藏标题栏并在整个窗口区域显示应用（适用于桌面 PWA） |

### 关键 MDN 参考路径

- **主要 PWA 索引：** `/en-US/docs/Web/Progressive_web_apps`
- **服务工作者 API：** `/en-US/docs/Web/API/Service_Worker_API`
- **Web API 概览：** `/en-US/docs/Web/API`
- **Web 应用清单：** `/en-US/docs/Web/Progressive_web_apps/Manifest`

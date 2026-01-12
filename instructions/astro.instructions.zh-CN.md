

---
description: 'Astro 开发标准和内容驱动网站的最佳实践'
applyTo: '**/*.astro, **/*.ts, **/*.js, **/*.md, **/*.mdx'
---

# Astro 开发指南

构建高质量 Astro 应用的指导原则，遵循内容驱动、以服务器优先的架构及现代最佳实践。

## 项目背景
- 使用 Astro 5.x 的岛屿架构和内容层 API
- 使用 TypeScript 实现类型安全及更好的开发体验（自动生成功能类型）
- 适用于内容驱动网站（博客、营销、电子商务、文档）
- 以服务器优先渲染，结合选择性客户端水合（hydration）
- 支持多种 UI 框架（React、Vue、Svelte、Solid 等）
- 默认使用静态网站生成（SSG），可选服务器端渲染（SSR）
- 通过现代内容加载和构建优化提升性能

## 开发标准

### 架构
- 遵循岛屿架构：默认服务器渲染，选择性水合
- 使用内容集合管理类型安全的 Markdown/MDX 内容
- 按功能或内容类型组织项目以实现可扩展性
- 采用基于组件的架构，明确职责分离
- 实现渐进增强模式
- 优先采用多页应用（MPA）模式而非单页应用（SPA）模式

### TypeScript 集成
- 使用推荐的 v5.0 设置配置 `tsconfig.json`：
```json
{
  "extends": "astro/tsconfigs/base",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"]
}
```
- 类型自动生成在 `.astro/types.d.ts`（替代 `src/env.d.ts`）
- 运行 `astro sync` 以生成/更新类型定义
- 使用 TypeScript 接口定义组件属性
- 利用内容集合和内容层 API 自动生成的类型

### 组件设计
- 使用 `.astro` 组件处理静态、服务器渲染的内容
- 仅在需要交互时导入框架组件（React、Vue、Svelte）
- 遵循 Astro 的组件脚本结构：顶部为 frontmatter，下方为模板
- 使用 PascalCase 命名规范命名组件
- 保持组件专注且可组合
- 实现适当的属性验证和默认值

### 内容集合

#### 现代内容层 API（v5.0+）
- 在 `src/content.config.ts` 中使用新内容层 API 定义集合
- 使用内置加载器：`glob()` 用于基于文件的内容，`file()` 用于单个文件
- 利用新加载系统实现增强性能和可扩展性
- 内容层 API 示例：
```typescript
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    tags: z.array(z.string()).optional()
  })
});
```

#### 旧版内容集合（向后兼容）
- 旧版 `type: 'content'` 集合仍通过自动 glob() 实现支持
- 通过添加显式的 `loader` 配置迁移现有集合
- 使用类型安全查询 `getCollection()` 和 `getEntry()`
- 通过 frontmatter 验证和自动生成类型组织内容

### 视图过渡与客户端路由
- 在布局头部使用 `<ClientRouter />` 组件启用（v5.0 中 `<ViewTransitions />` 已更名为）
- 从 `astro:transitions` 导入：`import { ClientRouter } from 'astro:transitions'`
- 提供类似 SPA 的导航体验，无需完整页面刷新
- 使用 CSS 和 `view-transition-name` 自定义过渡动画
- 通过持久化岛屿维护页面导航状态
- 使用 `transition:persist` 指令保留组件状态

### 性能优化
- 默认使用零 JavaScript - 仅在需要时添加交互功能
- 战略性使用客户端指令（`client:load`、`client:idle`、`client:visible`）
- 对图片和组件实现延迟加载
- 使用 Astro 内置功能优化静态资源
- 利用内容层 API 提升内容加载和构建速度
- 通过避免不必要的客户端 JavaScript 最小化包体积

## 样式设计
- 默认在 `.astro` 组件中使用作用域样式
- 需要时实现 CSS 预处理器（Sass、Less）
- 使用 CSS 自定义属性（CSS variables）进行主题和设计系统配置
- 遵循移动优先的响应式设计原则
- 使用语义化 HTML 和适当的 ARIA 属性确保可访问性
- 考虑使用实用优先框架（如 Tailwind CSS）进行快速开发

## 客户端交互
- 使用框架组件（React、Vue、Svelte）实现交互元素
- 根据用户交互模式选择合适的水合策略
- 在框架边界内实现状态管理
- 谨慎处理客户端路由以保持 MPA 优势
- 使用 Web Components 实现框架无关的交互
- 使用存储或自定义事件在岛屿间共享状态

## API 路由和 SSR
- 在 `src/pages/api/` 目录创建 API 路由以实现动态功能
- 使用正确的 HTTP 方法和状态码
- 实现请求验证和错误处理
- 启用 SSR 模式以满足动态内容需求
- 使用中间件处理认证和请求流程
- 安全处理环境变量

## SEO 和元数据管理
- 使用 Astro 内置的 SEO 组件和元标签管理功能
- 实现正确的 Open Graph 和 Twitter Card 元数据
- 自动生成站点地图以提升搜索引擎索引
- 使用语义化 HTML 结构以增强可访问性和 SEO
- 实现结构化数据（JSON-LD）以支持丰富摘要
- 优化页面标题和描述以提升搜索引擎排名

## 图片优化
- 使用 Astro 的 `<Image />` 组件实现自动优化
- 实现响应式图片并生成合适的 srcset
- 使用 WebP 和 AVIF 格式支持现代浏览器
- 对折叠区域下方的图片进行延迟加载
- 提供适当的替代文本以确保可访问性
- 在构建时优化图片以提升性能

## 数据获取
- 在组件 frontmatter 中进行构建时数据获取
- 使用动态导入实现条件数据加载
- 实现对外部 API 调用的正确错误处理
- 在构建过程中缓存昂贵操作
- 使用 Astro 内置 fetch 功能并自动推断 TypeScript 类型
- 合理处理加载状态和回退方案

## 构建与部署
- 使用 Astro 内置优化功能优化静态资源
- 配置静态（SSG）或混合（SSR）渲染的部署方案
- 使用环境变量进行配置管理
- 启用压缩和缓存功能以优化生产构建

## Astro v5.0 关键更新

### 突破性变更
- **ClientRouter**：使用 `<ClientRouter />` 替代 `<ViewTransitions />`
- **TypeScript**：自动生成类型在 `.astro/types.d.ts`（运行 `astro sync`）
- **内容层 API**：新增 `glob()` 和 `file()` 加载器以提升性能

### 迁移示例
```typescript
// 现代内容层 API
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({ title: z.string(), pubDate: z.date() })
});
```
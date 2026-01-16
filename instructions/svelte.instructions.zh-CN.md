---
description: 'Svelte 5 和 SvelteKit 的开发标准与最佳实践，用于构建基于组件的用户界面和全栈应用'
applyTo: '**/*.svelte, **/*.ts, **/*.js, **/*.css, **/*.scss, **/*.json'
---

# Svelte 5 和 SvelteKit 开发指南

构建高质量 Svelte 5 和 SvelteKit 应用的指南，涵盖现代基于 runes 的响应式编程、TypeScript 和性能优化。

## 项目背景
- 使用 Svelte 5.x 的 runes 系统（$state, $derived, $effect, $props, $bindable）
- 使用 SvelteKit 构建全栈应用，采用基于文件的路由系统
- 使用 TypeScript 实现类型安全和更好的开发体验
- 组件作用域样式，使用 CSS 自定义属性
- 采用渐进增强和以性能为导向的开发方法
- 现代构建工具（Vite）及优化

## 核心概念

### 架构
- 使用 Svelte 5 的 runes 系统管理所有响应式状态，而非传统 store
- 按功能或领域组织组件以实现可扩展性
- 将展示组件与逻辑密集型组件分离
- 将可重用逻辑提取为可组合函数
- 通过插槽和片段实现组件的合理组合
- 使用 SvelteKit 的基于文件的路由系统并配置适当的加载函数

### 组件设计
- 遵循单一职责原则
- 使用 `<script lang="ts">` 和 runes 语法作为默认设置
- 保持组件小巧且专注于单一功能
- 使用 TypeScript 注解实现属性验证
- 在组件内使用 `{#snippet}` 块进行可重用模板逻辑
- 使用插槽实现组件组合和内容投影
- 传递 `children` 片段以实现灵活的父子组件组合
- 设计可测试且可重用的组件

## 响应式与状态管理

### Svelte 5 Runes 系统
- 使用 `$state()` 管理响应式本地状态
- 使用 `$derived()` 实现计算值和昂贵计算
- 使用 `$derived.by()` 处理复杂计算，其涉及多条语句
- 尽量避免使用 `$effect()` 同步状态，优先使用 `$derived()` 或函数绑定
- 使用 `$effect.pre()` 在 DOM 更新前运行代码
- 使用 `untrack()` 防止在效果中读写相同状态时产生无限循环
- 使用 `$props()` 定义组件属性并配合 TypeScript 注解进行解构
- 使用 `$bindable()` 实现组件间的双向数据绑定
- 将传统 store 迁移到 runes 以提升性能
- 在 Svelte 5.25+ 中直接覆盖派生值以实现乐观 UI 模式

### 状态管理
- 使用 `$state()` 管理组件本地状态
- 使用 `createContext()` 辅助函数实现类型安全的上下文，而非原始 `setContext`/`getContext`
- 使用上下文 API 在组件树中共享响应式状态
- 避免在 SSR 中使用全局 `$state` 模块，使用上下文防止跨请求数据泄露
- 在需要时使用 SvelteKit 的 store 管理全局应用状态
- 对复杂数据结构进行状态规范化
- 优先使用 `$derived()` 而非 `$effect()` 实现计算值
- 实现客户端数据的合理状态持久化

### 效果最佳实践
- **避免** 使用 `$effect()` 同步状态，改用 `$derived()` 实现
- **应使用** `$effect()` 处理副作用：分析、日志、DOM 操作
- **应返回** 清理函数以确保效果正确卸载
- 在必须在 DOM 更新前运行代码（如滚动位置）时使用 `$effect.pre()`
- 在组件生命周期之外手动控制效果时使用 `$effect.root()`
- 使用 `untrack()` 读取状态时避免创建依赖项
- 注意：效果中的异步代码在 `await` 之后不会跟踪依赖项

## SvelteKit 模式

### 路由与布局
- 使用 `+page.svelte` 实现页面组件并确保 SEO 优化
- 使用 `+layout.svelte` 实现共享布局和导航
- 使用 SvelteKit 的基于文件的系统处理路由

### 数据加载与突变
- 使用 `+page.server.ts` 实现服务器端数据加载和 API 调用
- 在 `+page.server.ts` 中实现表单操作以处理数据突变
- 使用 `+server.ts` 实现 API 端点和服务器端逻辑
- 使用 SvelteKit 的加载函数实现服务器端和通用数据获取
- 实现正确的加载、错误和成功状态
- 在服务器加载函数中使用 Promise 处理流数据
- 使用 `invalidate()` 和 `invalidateAll()` 管理缓存
- 实现乐观更新以提升用户体验
- 优雅处理离线场景和网络错误

### 表单与验证
- 使用 SvelteKit 的表单操作处理服务器端表单逻辑
- 使用 `use:enhance` 实现渐进增强
- 使用 `bind:value` 实现受控表单输入
- 在客户端和服务器端均进行数据验证
- 处理文件上传和复杂表单场景
- 实现适当的可访问性，包括标签和 ARIA 属性

## UI 与样式

### 样式
- 使用 `<style>` 块实现组件作用域样式
- 使用 CSS 自定义属性实现主题和设计系统
- 使用 `class:` 指令实现条件样式
- 遵循 BEM 或实用优先的 CSS 风格
- 使用移动优先方法实现响应式设计
- 少量使用 `:global()` 实现真正全局样式

### 过渡与动画
- 使用 `transition:` 指令实现进入/退出动画（淡入淡出、滑动、缩放、飞入）
- 使用 `in:` 和 `out:` 分别实现进入和退出过渡
- 使用 `animate:` 指令与 `flip` 实现列表重新排序的平滑动画
- 创建自定义过渡以实现品牌化的动画设计
- 使用 `|local` 修饰符仅在直接更改时触发过渡
- 将过渡与带键的 `{#each}` 块结合以实现列表动画

## TypeScript 与工具

### TypeScript 集成
- 在 `tsconfig.json` 中启用严格模式以获得最大类型安全
- 使用 TypeScript 注解属性：`let { name }: { name: string } = $props()`
- 为事件处理、引用和 SvelteKit 生成的类型进行类型标注
- 为可重用组件使用泛型类型
- 利用 SvelteKit 生成的 `$types.ts` 文件
- 使用 `svelte-check` 实现严格的类型检查
- 在可能的情况下使用类型推断以减少模板代码

### 开发工具
- 使用 ESLint 和 eslint-plugin-svelte 以及 Prettier 保持代码一致性
- 使用 Svelte DevTools 进行调试和性能分析
- 保持依赖项更新并进行安全漏洞审计
- 使用 JSDoc 文档化复杂组件和逻辑
- 遵循 Svelte 的命名规范（组件使用 PascalCase，函数使用 camelCase）

## 生产就绪

### 性能优化
- 使用带键的 `{#each}` 块实现高效的列表渲染
- 使用动态导入和 `<svelte:component>` 实现懒加载
- 使用 `$derived()` 处理昂贵计算以避免不必要的重新计算
- 使用 `$derived.by()` 实现需要多条语句的复杂派生值
- 避免使用 `$effect()` 同步状态，其效率不如 `$derived()` 或回调函数
- 利用 SvelteKit 的自动代码分割和预加载功能
- 通过树摇优化和合理导入实现包体积优化
- 使用 Svelte DevTools 进行性能分析以识别瓶颈
- 在抽象中使用 `$effect.tracking()` 条件性地创建响应式监听器

### 错误处理
- 实现 `+error.svelte` 页面作为路由级别的错误边界
- 在加载函数和表单操作中使用 try/catch 块
- 提供有意义的错误信息和备用 UI
- 适当记录错误以用于调试和监控
- 在表单中处理验证错误并提供用户反馈
- 使用 SvelteKit 的 `error()` 和 `redirect()` 辅助函数实现正确的响应
- 使用 `$effect.pending()` 跟踪待处理的 Promise 以管理加载状态

### 测试
- 使用 Vitest 和 Testing Library 为组件编写单元测试
- 测试组件行为而非实现细节
- 使用 Playwright 进行用户工作流的端到端测试
- 适当模拟 SvelteKit 的加载函数和 store
- 充分测试表单操作和 API 端点
- 使用 axe-core 实现可访问性测试

### 安全性
- 清洗用户输入以防止 XSS 攻击
- 小心使用 `@html` 指令并验证 HTML 内容
- 使用 SvelteKit 实现适当的 CSRF 保护
- 在加载函数和表单操作中验证和清洗数据
- 所有外部 API 调用和生产部署使用 HTTPS
- 使用适当的会话管理安全存储敏感数据

### 可访问性
- 使用语义 HTML 元素和正确的标题层级
- 为所有交互元素实现键盘导航
- 提供适当的 ARIA 标签和描述
- 确保颜色对比度符合 WCAG 指南
- 使用屏幕阅读器和可访问性工具进行测试
- 为动态内容实现焦点管理

### 部署
- 使用环境变量在不同部署阶段进行配置
- 使用 SvelteKit 的元标签和结构化数据实现适当的 SEO
- 根据托管平台选择合适的 SvelteKit 适配器进行部署

## 实现流程
1. 使用 TypeScript 和所需的适配器初始化 SvelteKit 项目
2. 按照适当的文件夹结构设置项目
3. 定义 TypeScript 接口和组件属性
4. 使用 Svelte 5 的 runes 实现核心组件
5. 使用 SvelteKit 实现路由、布局和导航
6. 实现数据加载和表单处理
7. 使用自定义属性和响应式设计添加样式系统
8. 实现错误处理和加载状态
9. 添加全面的测试覆盖
10. 优化性能和包体积
11. 确保符合可访问性标准
12. 使用适当的 SvelteKit 适配器进行部署

## 常见模式
- 使用插槽实现无渲染组件以灵活组合 UI
- 使用自定义操作（`use:` 指令）处理跨切面关注点和 DOM 操作
- 在组件内使用 `{#snippet}` 块实现可重用的模板逻辑
- 使用 `createContext()` 实现类型安全的上下文以共享组件树状态
- 使用 `use:enhance` 实现表单和交互功能的渐进增强
- 使用客户端水合实现服务端渲染以获得最佳性能
- 使用函数绑定（`bind:value={() => value, setValue}`）实现双向绑定
- 避免使用 `$effect()` 同步状态，改用 `$derived()` 或回调函数

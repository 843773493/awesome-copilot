

---
description: '使用Composition API和TypeScript的VueJS 3开发标准与最佳实践'
applyTo: '**/*.vue, **/*.ts, **/*.js, **/*.scss'
---

# VueJS 3开发指南

构建高质量VueJS 3应用的指南，使用组合API、TypeScript和现代最佳实践。

## 项目背景
- 默认使用Vue 3.x与组合API
- 使用TypeScript确保类型安全
- 使用单文件组件（`.vue`）和`<script setup>`语法
- 使用现代构建工具（推荐Vite）
- 使用Pinia进行应用状态管理
- 遵循官方Vue风格指南和最佳实践

## 开发规范

### 架构
- 优先使用组合API（`setup`函数和组合函数）而非选项API
- 按功能或领域组织组件和组合函数以实现可扩展性
- 将关注UI的组件（展示型）与关注逻辑的组件（容器型）分离
- 将可复用的逻辑提取为`composables/`目录中的组合函数
- 按领域结构化Pinia存储模块，明确定义动作、状态和获取器

### TypeScript集成
- 在`tsconfig.json`中启用`strict`模式以获得最大类型安全
- 使用`defineComponent`或`<script setup lang="ts">`配合`defineProps`和`defineEmits`
- 使用`PropType<T>`为props和默认值定义类型
- 对复杂props和state结构使用接口或类型别名
- 为事件处理函数、refs和`useRoute`/`useRouter`钩子定义类型
- 在适用场景中实现泛型组件和组合函数

### 组件设计
- 遵循单一职责原则设计组件
- 组件名称使用PascalCase，文件名使用kebab-case
- 保持组件小巧且专注于单一职责
- 使用`<script setup>`语法以提升简洁性和性能
- 使用TypeScript验证props；仅在必要时使用运行时检查
- 优先使用插槽和作用域插槽实现灵活组合

### 状态管理
- 使用Pinia进行全局状态管理：通过`defineStore`定义存储
- 对简单本地状态，使用`ref`和`reactive`在`setup`中处理
- 使用`computed`处理派生状态
- 对复杂结构保持状态规范化
- 在Pinia存储中使用动作处理异步逻辑
- 利用存储插件实现持久化或调试功能

### 组合API模式
- 创建可复用的组合函数处理共享逻辑，例如`useFetch`、`useAuth`
- 使用`watch`和`watchEffect`时提供精确的依赖列表
- 在`onUnmounted`或`watch`清理回调中清理副作用
- 稀少使用`provide`/`inject`进行深度依赖注入
- 使用`useAsyncData`或第三方数据工具（如Vue Query）

### 样式
- 使用`<style scoped>`或CSS模块实现组件级样式
- 考虑使用以实用为中心的框架（如Tailwind CSS）快速实现样式
- 遵循BEM或功能型CSS的命名规范
- 利用CSS自定义属性实现主题和设计令牌
- 实现移动优先、响应式设计，使用CSS Grid和Flexbox
- 确保样式符合可访问性要求（对比度、聚焦状态）

## 实施流程
1. 规划组件和组合函数架构
2. 使用Vue 3和TypeScript初始化Vite项目
3. 定义Pinia存储和组合函数
4. 创建核心UI组件和布局
5. 集成路由和导航功能
6. 实现数据获取和状态逻辑
7. 使用验证和错误状态构建表单
8. 添加全局错误处理和备用UI
9. 添加单元测试和端到端测试
10. 优化性能和打包体积
11. 确保符合可访问性标准
12. 文档化组件、组合函数和存储

## 额外指南
- 遵循Vue官方风格指南（vuejs.org/style-guide）
- 使用ESLint（搭配`plugin:vue/vue3-recommended`）和Prettier确保代码一致性
- 编写有意义的提交信息并维护清晰的Git历史记录
- 保持依赖项更新并审计漏洞
- 使用JSDoc/TSDoc文档化复杂逻辑
- 使用Vue DevTools进行调试和性能分析

## 常见模式
- 使用无渲染组件和作用域插槽实现灵活UI
- 使用`provide`/`inject`构建复合组件
- 使用自定义指令处理横切关注点
- 使用Teleport实现模态框和覆盖层
- 使用插件系统管理全局工具（如i18n、分析工具）
- 使用组合函数工厂实现参数化逻辑
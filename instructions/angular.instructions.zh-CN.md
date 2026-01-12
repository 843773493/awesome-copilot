

---
description: 'Angular特定的编码规范和最佳实践'
applyTo: '**/*.ts, **/*.html, **/*.scss, **/*.css'
---

# Angular开发指南

使用TypeScript、Angular Signals进行状态管理，并遵循https://angular.dev上列出的Angular最佳实践，生成高质量Angular应用程序的指南。

## 项目背景
- 使用最新Angular版本（默认使用独立组件）
- 使用TypeScript实现类型安全
- 使用Angular CLI进行项目设置和代码生成
- 遵循Angular风格指南（https://angular.dev/style-guide）
- 使用Angular Material或其他现代UI库以确保一致的样式（如指定）

## 开发规范

### 架构
- 除非明确需要模块，否则使用独立组件
- 通过独立功能模块或领域划分代码以实现可扩展性
- 对功能模块实施懒加载以优化性能
- 有效使用Angular内置的依赖注入系统
- 通过清晰的职责分离（智能组件与展示组件）组织组件结构

### TypeScript
- 在`tsconfig.json`中启用严格模式以实现类型安全
- 为组件、服务和模型定义清晰的接口和类型
- 使用类型守卫和联合类型进行强大的类型检查
- 使用RxJS操作符实现正确的错误处理（例如：`catchError`）
- 使用类型化表单（例如：`FormGroup`、`FormControl`）处理响应式表单

### 组件设计
- 遵循Angular组件生命周期钩子的最佳实践
- 当使用Angular >= 19时，使用`input()`、`output()`、`viewChild()`、`viewChildren()`、`contentChild()`和`contentChildren()`函数，而非装饰器；否则使用装饰器
- 利用Angular的变更检测策略（默认或`OnPush`以提升性能）
- 保持模板简洁，将逻辑放在组件类或服务中
- 使用Angular指令和管道实现可重用功能

### 样式
- 使用Angular的组件级CSS封装（默认：ViewEncapsulation.Emulated）
- 优先使用SCSS进行样式设计，并保持一致的主题
- 使用CSS Grid、Flexbox或Angular CDK Layout工具实现响应式设计
- 如使用Angular Material，则遵循其主题指南
- 通过ARIA属性和语义化HTML实现可访问性（a11y）

### 状态管理
- 使用Angular Signals进行组件和服务中的响应式状态管理
- 使用`signal()`、`computed()`和`effect()`实现响应式状态更新
- 使用可写信号处理可变状态，使用计算信号处理派生状态
- 使用信号和适当的UI反馈处理加载和错误状态
- 在结合RxJS时，使用Angular的`AsyncPipe`处理模板中的可观察对象

### 数据获取
- 使用Angular的`HttpClient`进行API调用，并确保类型安全
- 使用RxJS操作符实现数据转换和错误处理
- 使用Angular的`inject()`函数在独立组件中进行依赖注入
- 实现缓存策略（例如：`shareReplay`用于可观察对象）
- 将API响应数据存储在信号中以实现响应式更新
- 使用全局拦截器处理API错误以确保一致的错误处理

### 安全性
- 使用Angular内置的净化功能对用户输入进行安全处理
- 实现路由守卫以进行身份验证和授权
- 使用Angular的`HttpInterceptor`进行CSRF保护和API认证头处理
- 使用Angular响应式表单和自定义验证器对表单输入进行验证
- 遵循Angular的安全最佳实践（例如：避免直接操作DOM）

### 性能优化
- 使用`ng build --prod`生成生产构建以进行优化
- 对路由实施懒加载以减少初始包体积
- 通过`OnPush`策略和信号优化变更检测以实现细粒度响应性
- 在`ngFor`循环中使用`trackBy`以提升渲染性能
- 如指定，使用Angular Universal实现服务端渲染（SSR）或静态网站生成（SSG）

## 实施流程
1. 规划项目结构和功能模块
2. 定义TypeScript接口和模型
3. 使用Angular CLI生成组件、服务和管道的代码框架
4. 使用基于信号的状态实现数据服务和API集成
5. 创建具有清晰输入和输出的可重用组件
6. 添加响应式表单和验证逻辑
7. 使用SCSS和响应式设计应用样式
8. 实现懒加载路由和守卫
9. 使用信号处理错误和加载状态，并提供适当的UI反馈
10. 编写单元测试和端到端测试
11. 优化性能和包体积

## 其他指南
- 遵循Angular风格指南中的文件命名规范（参见https://angular.dev/style-guide），例如：使用`feature.ts`表示组件，使用`feature-service.ts`表示服务。对于遗留代码库，需保持与现有模式的一致性。
- 使用Angular CLI命令生成样板代码
- 使用清晰的JSDoc注释对组件和服务进行文档说明
- 在适用情况下确保符合可访问性标准（WCAG 2.1）
- 使用Angular内置的i18n功能实现国际化（如指定）
- 通过创建可重用的实用工具和共享模块保持代码简洁（DRY原则）
- 一致使用信号进行状态管理，以确保响应式更新
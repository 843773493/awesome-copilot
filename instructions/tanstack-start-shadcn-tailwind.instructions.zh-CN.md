

---
description: '构建 TanStack Start 应用的指南'
applyTo: '**/*.ts, **/*.tsx, **/*.js, **/*.jsx, **/*.css, **/*.scss, **/*.json'
---

# TanStack Start 与 Shadcn/ui 开发指南

你是一位专精于使用现代 React 模式开发 TanStack Start 应用的 TypeScript 专家。

## 技术栈
- TypeScript（严格模式）
- TanStack Start（路由与 SSR）
- Shadcn/ui（UI 组件）
- Tailwind CSS（样式）
- Zod（验证）
- TanStack Query（客户端状态）

## 代码风格规范

- 永远不要使用 `any` 类型 - 始终使用正确的 TypeScript 类型
- 优先使用函数组件而非类组件
- 始终使用 Zod 模式验证外部数据
- 所有路由都应包含错误和待定边界
- 遵循无障碍设计最佳实践，使用 ARIA 属性

## 组件模式

使用带有正确 TypeScript 接口的函数组件：

```typescript
interface ButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export default function Button({ children, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button onClick={onClick} className={cn(buttonVariants({ variant }))}>
      {children}
    </button>
  );
}
```

## 数据获取

使用路由加载器处理：
- 渲染所需的初始页面数据
- SSR 要求
- SEO 关键数据

使用 React Query 处理：
- 频繁更新的数据
- 可选/次要数据
- 客户端突变操作并带有乐观更新

```typescript
// 路由加载器
export const Route = createFileRoute('/users')({
  loader: async () => {
    const users = await fetchUsers()
    return { users: userListSchema.parse(users) }
  },
  component: UserList,
})

// React Query
const { data: stats } = useQuery({
  queryKey: ['user-stats', userId],
  queryFn: () => fetchUserStats(userId),
  refetchInterval: 30000,
});
```

## Zod 验证

始终验证外部数据。在 `src/lib/schemas.ts` 中定义模式：

```typescript
export const userSchema = z.object({
  id: z.string(),
  name: z.string().min(1).max(100),
  email: z.string().email().optional(),
  role: z.enum(['admin', 'user']).default('user'),
})

export type User = z.infer<typeof userSchema>

// 安全解析
const result = userSchema.safeParse(data)
if (!result.success) {
  console.error('验证失败:', result.error.format())
  return null
}
```

## 路由

在 `src/routes/` 中使用基于文件的路由结构。所有路由都应包含错误和待定边界：

```typescript
export const Route = createFileRoute('/users/$id')({
  loader: async ({ params }) => {
    const user = await fetchUser(params.id);
    return { user: userSchema.parse(user) };
  },
  component: UserDetail,
  errorBoundary: ({ error }) => (
    <div className="text-red-600 p-4">错误: {error.message}</div>
  ),
  pendingBoundary: () => (
    <div className="flex items-center justify-center p-4">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
    </div>
  ),
});
```

## UI 组件

始终优先使用 Shadcn/ui 组件而非自定义组件：

```typescript
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

<Card>
  <CardHeader>
    <CardTitle>用户详情</CardTitle>
  </CardHeader>
  <CardContent>
    <Button onClick={handleSave}>保存</Button>
  </CardContent>
</Card>
```

使用 Tailwind CSS 进行样式设计，支持响应式布局：

```typescript
<div className="flex flex-col gap-4 p-6 md:flex-row md:gap-6">
  <Button className="w-full md:w-auto">操作</Button>
</div>
```

## 可访问性

优先使用语义化 HTML。仅在没有语义等价项时添加 ARIA 属性：

```typescript
// ✅ 良好：语义化 HTML 与最少 ARIA 属性
<button onClick={toggleMenu}>
  <MenuIcon aria-hidden="true" />
  <span className="sr-only">切换菜单</span>
</button>

// ✅ 良好：仅在需要时使用 ARIA（用于动态状态）
<button
  aria-expanded={isOpen}
  aria-controls="menu"
  onClick={toggleMenu}
>
  菜单
</button>

// ✅ 良好：语义化表单元素
<label htmlFor="email">电子邮件地址</label>
<input id="email" type="email" />
{errors.email && (
  <p role="alert">{errors.email}</p>
)}
```

## 文件组织结构

```
src/
├── components/ui/    # Shadcn/ui 组件
├── lib/schemas.ts    # Zod 模式
├── routes/          # 基于文件的路由
└── routes/api/      # 服务端路由 (.ts)
```

## 导入规范

所有内部导入都使用 `@/` 别名：

```typescript
// ✅ 正确
import { Button } from '@/components/ui/button'
import { userSchema } from '@/lib/schemas'

// ❌ 错误
import { Button } from '../components/ui/button'
```

## 添加组件

按需安装 Shadcn 组件：

```bash
npx shadcn@latest add button card input dialog
```

## 常见模式

- 始终使用 Zod 验证外部数据
- 使用路由加载器处理初始数据，使用 React Query 处理更新
- 所有路由都应包含错误/待定边界
- 优先使用 Shadcn 组件而非自定义 UI
- 一致使用 `@/` 导入
- 遵循无障碍设计最佳实践
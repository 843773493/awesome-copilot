---
描述: '使用官方 @tailwindcss/vite 插件在 Vite 项目中安装和配置 Tailwind CSS v4+'
适用范围: 'vite.config.ts, vite.config.js, **/*.css, **/*.tsx, **/*.ts, **/*.jsx, **/*.js'
---

# 使用 Vite 安装 Tailwind CSS v4+

使用官方 Vite 插件安装和配置 Tailwind CSS 版本 4 及以上。Tailwind CSS v4 引入了简化设置，大多数情况下不再需要 PostCSS 配置和 tailwind.config.js。

## Tailwind CSS v4 的关键变化

- **使用 Vite 插件时无需 PostCSS 配置**
- **无需 tailwind.config.js** - 配置通过 CSS 完成
- **新的 @tailwindcss/vite 插件** 替代基于 PostCSS 的方法
- **使用 @theme 指令的 CSS 首配置**
- **自动内容检测** - 无需指定内容路径

## 安装步骤

### 步骤 1: 安装依赖

安装 `tailwindcss` 和 `@tailwindcss/vite` 插件：

```bash
npm install tailwindcss @tailwindcss/vite
```

### 步骤 2: 配置 Vite 插件

将 `@tailwindcss/vite` 插件添加到 Vite 配置文件中：

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
})
```

对于使用 Vite 的 React 项目：

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})
```

### 步骤 3: 导入 Tailwind CSS

在您的主 CSS 文件（例如 `src/index.css` 或 `src/App.css`）中添加 Tailwind CSS 导入：

```css
@import "tailwindcss";
```

### 步骤 4: 验证主入口点的 CSS 导入

确保您的主 CSS 文件在应用程序入口点被导入：

```typescript
// src/main.tsx 或 src/main.ts
import './index.css'
```

### 步骤 5: 启动开发服务器

运行开发服务器以验证安装：

```bash
npm run dev
```

## Tailwind v4 不应执行的操作

### 不要创建 tailwind.config.js

Tailwind v4 使用 CSS 首配置。除非您有特定的旧版需求，否则不要创建 `tailwind.config.js` 文件。

```javascript
// ❌ 在 Tailwind v4 中不需要
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 不要为 Tailwind 创建 postcss.config.js

当使用 `@tailwindcss/vite` 插件时，无需为 Tailwind 配置 PostCSS。

```javascript
// ❌ 当使用 @tailwindcss/vite 时不需要
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### 不要使用旧的 @tailwind 指令

旧的 `@tailwind` 指令已被单个导入语句取代：

```css
/* ❌ 旧版 - 不要在 Tailwind v4 中使用 */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ✅ 新版 - 在 Tailwind v4 中使用 */
@import "tailwindcss";
```

## CSS 首配置 (Tailwind v4)

### 自定义主题配置

在 CSS 中使用 `@theme` 指令自定义您的设计标记：

```css
@import "tailwindcss";

@theme {
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  --font-sans: 'Inter', system-ui, sans-serif;
  --radius-lg: 0.75rem;
}
```

### 添加自定义工具类

直接在 CSS 中定义自定义工具类：

```css
@import "tailwindcss";

@utility content-auto {
  content-visibility: auto;
}

@utility scrollbar-hidden {
  scrollbar-width: none;
  &::-webkit-scrollbar {
    display: none;
  }
}
```

### 添加自定义变体

在 CSS 中定义自定义变体：

```css
@import "tailwindcss";

@variant hocus (&:hover, &:focus);
@variant group-hocus (:merge(.group):hover &, :merge(.group):focus &);
```

## 验证检查清单

安装完成后，请验证以下内容：

- [ ] 确保 `tailwindcss` 和 `@tailwindcss/vite` 出现在 `package.json` 的依赖项中
- [ ] 确保 `vite.config.ts` 包含 `tailwindcss()` 插件
- [ ] 主 CSS 文件包含 `@import "tailwindcss";`
- [ ] CSS 文件在应用程序入口点被导入
- [ ] 开发服务器运行无错误
- [ ] Tailwind 工具类（例如 `text-blue-500`、`p-4`）正确渲染

## 示例用法

使用一个简单组件测试安装：

```tsx
export function TestComponent() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <h1 className="text-3xl font-bold text-blue-600 underline">
        你好，Tailwind CSS v4!
      </h1>
    </div>
  )
}
```

## 常见问题排查

### 样式未应用

1. 确认 CSS 导入语句是 `@import "tailwindcss";`（不是旧指令）
2. 确保 CSS 文件在入口点被导入
3. 检查 Vite 配置是否包含 `tailwindcss()` 插件
4. 清除 Vite 缓存：`rm -rf node_modules/.vite && npm run dev`

### 插件未找到错误

如果看到 "Cannot find module '@tailwindcss/vite'" 错误：

```bash
npm install @tailwindcss/vite
```

### TypeScript 错误

如果 TypeScript 无法找到 Vite 插件的类型，请确保使用正确的导入语句：

```typescript
import tailwindcss from '@tailwindcss/vite'
```

## 从 Tailwind v3 迁移

如果从 Tailwind v3 迁移：

1. 删除 `tailwind.config.js`（将自定义内容迁移到 CSS `@theme`）
2. 删除 `postcss.config.js`（如果仅用于 Tailwind）
3. 卸载旧包：`npm uninstall postcss autoprefixer`
4. 安装新包：`npm install tailwindcss @tailwindcss/vite`
5. 将 `@tailwind` 指令替换为 `@import "tailwindcss";`
6. 更新 Vite 配置以使用 `@tailwindcss/vite` 插件

## 参考

- 官方文档: https://tailwindcss.com/docs/installation/using-vite
- Tailwind CSS v4 升级指南: https://tailwindcss.com/docs/upgrade-guide

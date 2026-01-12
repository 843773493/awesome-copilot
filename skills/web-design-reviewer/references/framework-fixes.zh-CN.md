

# 框架特定修复指南

本文档解释了每个框架和样式方法的具体修复技术。

---

## 纯CSS / SCSS

### 修复布局溢出

```css
/* 修复前：出现溢出 */
.container {
  width: 100%;
}

/* 修复后：控制溢出 */
.container {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}
```

### 防止文本截断

```css
/* 单行截断 */
.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 多行截断 */
.text-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 单词换行 */
.text-wrap {
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
}
```

### 统一间距

```css
/* 使用CSS自定义属性统一间距 */
:root {
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
}

.card {
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}
```

### 提高对比度

```css
/* 修复前：对比度不足 */
.text {
  color: #999999;
  background-color: #ffffff;
}

/* 修复后：符合WCAG AA标准 */
.text {
  color: #595959; /* 对比度比值为7:1 */
  background-color: #ffffff;
}
```

---

## Tailwind CSS

### 布局修复

```jsx
{/* 修复前：溢出 */}
<div className="w-full">
  <img src="..." />
</div>

{/* 修复后：控制溢出 */}
<div className="w-full max-w-full overflow-hidden">
  <img src="..." className="w-full h-auto object-contain" />
</div>
```

### 防止文本截断

```jsx
{/* 单行截断 */}
<p className="truncate">Long text...</p>

{/* 多行截断 */}
<p className="line-clamp-3">Long text...</p>

{/* 允许换行 */
<p className="break-words">Long text...</p>
```

### 响应式支持

```jsx
{/* 移动优先响应式 */}
<div className="
  flex flex-col gap-4
  md:flex-row md:gap-6
  lg:gap-8
">
  <div className="w-full md:w-1/2 lg:w-1/3">
    Content
  </div>
</div>
```

### 间距统一（Tailwind配置）

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
    },
  },
}
```

### 可访问性改进

```jsx
{/* 添加聚焦状态 */}
<button className="
  bg-blue-500 text-white
  hover:bg-blue-600
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
">
  Button
</button>

{/* 提高对比度 */
<p className="text-gray-700 bg-white"> {/* 从text-gray-500改为text-gray-700 */}
  可读文本
</p>
```

---

## React + CSS Modules

### 模块作用域内的修复

```css
/* Component.module.css */

/* 修复前 */
.container {
  display: flex;
}

/* 修复后：添加溢出控制 */
.container {
  display: flex;
  flex-wrap: wrap;
  overflow: hidden;
  max-width: 100%;
}
```

### 组件侧修复

```jsx
// Component.jsx
import styles from './Component.module.css';

// 修复前
<div className={styles.container}>

// 修复后：添加条件类
<div className={`${styles.container} ${isOverflow ? styles.overflow : ''}`}>
```

---

## styled-components / Emotion

### 样式修复

```jsx
// 修复前
const Container = styled.div`
  width: 100%;
`;

// 修复后
const Container = styled.div`
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
`;
```

### 响应式支持

```jsx
const Card = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  
  @media (max-width: 1024px) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (max-width: 640px) {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
`;
```

### 与主题保持一致

```jsx
// theme.js
export const theme = {
  colors: {
    primary: '#2563eb',
    text: '#1f2937',
    textLight: '#4b5563', // 改进对比度
  },
  spacing: {
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
  },
};

// 使用示例
const Text = styled.p`
  color: ${({ theme }) => theme.colors.text};
  margin-bottom: ${({ theme }) => theme.spacing.md};
`;
```

---

## Vue（作用域样式）

### 修复作用域样式

```vue
<template>
  <div class="container">
    <p class="text">Content</p>
  </div>
</template>

<style scoped>
/* 仅应用于此组件 */
.container {
  max-width: 100%;
  overflow: hidden;
}

.text {
  /* 修复：提高对比度 */
  color: #374151; /* 原为 #9ca3af */
}

/* 响应式 */
@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }
}
</style>
```

### 深度选择器（影响子组件）

```vue
<style scoped>
/* 覆盖子组件样式（谨慎使用） */
:deep(.child-class) {
  margin-bottom: 1rem;
}
</style>
```

---

## Next.js / App Router

### 全局样式修复

```css
/* app/globals.css */
:root {
  --foreground: #171717;
  --background: #ffffff;
}

/* 防止布局溢出 */
html, body {
  max-width: 100vw;
  overflow-x: hidden;
}

/* 防止图片溢出 */
img {
  max-width: 100%;
  height: auto;
}
```

### 布局组件中的修复

```tsx
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col">
        <header className="sticky top-0 z-50">
          {/* 头部 */}
        </header>
        <main className="flex-1 container mx-auto px-4 py-8">
          {children}
        </main>
        <footer>
          {/* 尾部 */}
        </footer>
      </body>
    </html>
  );
}
```

---

## 常见模式

### 修复Flexbox布局问题

```css
/* 修复前：项目溢出 */
.flex-container {
  display: flex;
  gap: 1rem;
}

/* 修复后：换行和尺寸控制 */
.flex-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.flex-item {
  flex: 1 1 300px; /* 增长、收缩、基准 */
  min-width: 0; /* 防止Flexbox溢出问题 */
}
```

### 修复Grid布局问题

```css
/* 修复前：固定列数 */
.grid-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}

/* 修复后：自动调整 */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}
```

### 组织z-index

```css
/* 系统化z-index */
:root {
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-modal-backdrop: 300;
  --z-modal: 400;
  --z-tooltip: 500;
}

.modal {
  z-index: var(--z-modal);
}
```

### 添加聚焦状态

```css
/* 为所有交互元素添加聚焦状态 */
button:focus-visible,
a:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

/* 自定义聚焦环 */
.custom-focus:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.5);
}
```

---

## 调试技术

### 可视化元素边界

```css
/* 仅在开发时使用 */
* {
  outline: 1px solid red !important;
}
```

### 检测溢出

```javascript
// 在控制台运行以检测溢出元素
document.querySelectorAll('*').forEach(el => {
  if (el.scrollWidth > el.clientWidth) {
    console.log('水平溢出:', el);
  }
  if (el.scrollHeight > el.clientHeight) {
    console.log('垂直溢出:', el);
  }
});
```

### 检查对比度比值

```javascript
// 使用Chrome DevTools Lighthouse或axe DevTools
// 或访问以下网站进行检查：
// https://webaim.org/resources/contrastchecker/
```
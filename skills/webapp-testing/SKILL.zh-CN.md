

---
name: webapp-testing
description: 使用Playwright与本地Web应用进行交互和测试的工具包。支持验证前端功能、调试UI行为、捕获浏览器截图以及查看浏览器日志。
---

# Web应用测试

此技能可使用Playwright自动化技术对本地Web应用进行全面测试和调试。

## 何时使用此技能

当您需要：
- 在真实浏览器中测试前端功能
- 验证UI行为和交互
- 调试Web应用问题
- 捕获截图用于文档记录或调试
- 检查浏览器控制台日志
- 验证表单提交和用户流程
- 检查不同视口下的响应式设计时

## 先决条件

- 系统上安装了Node.js
- 本地运行的Web应用（或可访问的URL）
- 如果未安装，Playwright将自动安装

## 核心功能

### 1. 浏览器自动化
- 导航到URL
- 点击按钮和链接
- 填充表单字段
- 选择下拉菜单
- 处理对话框和警报

### 2. 验证
- 断言元素存在
- 验证文本内容
- 检查元素可见性
- 验证URL
- 测试响应式行为

### 3. 调试
- 捕获截图
- 查看控制台日志
- 检查网络请求
- 调试失败的测试

## 使用示例

### 示例1：基本导航测试
```javascript
// 导航到页面并验证标题
await page.goto('http://localhost:3000');
const title = await page.title();
console.log('页面标题:', title);
```

### 示例2：表单交互
```javascript
// 填写并提交表单
await page.fill('#username', 'testuser');
await page.fill('#password', 'password123');
await page.click('button[type="submit"]');
await page.waitForURL('**/dashboard');
```

### 示例3：截图捕获
```javascript
// 捕获截图用于调试
await page.screenshot({ path: 'debug.png', fullPage: true });
```

## 使用指南

1. **始终验证应用是否正在运行** - 在运行测试前检查本地服务器是否可访问
2. **使用显式等待** - 在交互前等待元素或导航完成
3. **在失败时捕获截图** - 通过截图帮助调试问题
4. **清理资源** - 测试完成后始终关闭浏览器
5. **优雅处理超时** - 为慢操作设置合理的超时时间
6. **逐步测试** - 先从简单交互开始，再进行复杂流程测试
7. **明智使用选择器** - 优先使用data-testid或基于角色的选择器，而非CSS类

## 常见模式

### 模式：等待元素
```javascript
await page.waitForSelector('#element-id', { state: 'visible' });
```

### 模式：检查元素是否存在
```javascript
const exists = await page.locator('#element-id').count() > 0;
```

### 模式：获取控制台日志
```javascript
page.on('console', msg => console.log('浏览器日志:', msg.text()));
```

### 模式：处理错误
```javascript
try {
  await page.click('#button');
} catch (error) {
  await page.screenshot({ path: 'error.png' });
  throw error;
}
```

## 局限性

- 需要Node.js环境
- 无法测试原生移动应用（请改用React Native Testing Library）
- 可能存在复杂认证流程的问题
- 某些现代框架可能需要特定配置
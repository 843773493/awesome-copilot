

---
description: '使用 GitHub Copilot 编写注释的指南，以实现无需过多注释即可自解释的代码。示例使用 JavaScript 编写，但适用于任何支持注释的语言。'
applyTo: '**'
---

# 自解释代码的注释指南

## 核心原则
**编写能够自我解释的代码。仅在需要解释“为什么”而非“是什么”时添加注释。**
我们大多数时候并不需要注释。

## 注释指南

### ❌ 避免这些注释类型

**显而易见的注释**
```javascript
// 不好：重复显而易见的内容
let counter = 0;  // 将计数器初始化为零
counter++;  // 计数器加一
```

**冗余注释**
```javascript
// 不好：注释重复了代码
function getUserName() {
    return user.name;  // 返回用户的姓名
}
```

**过时的注释**
```javascript
// 不好：注释与代码不一致
// 按 5% 的税率计算税款
const tax = price * 0.08;  // 实际上是 8%
```

### ✅ 编写这些注释类型

**复杂的业务逻辑**
```javascript
// 好：解释为何使用此特定计算
// 应用累进税率档次：10% 适用于 10,000 以下，20% 适用于 10,000 以上
const tax = calculateProgressiveTax(income, [0.10, 0.20], [10000]);
```

**不明显的算法**
```javascript
// 好：解释算法选择的原因
// 使用弗洛伊德-沃舍尔算法计算所有节点对的最短路径
// 因为我们需要计算所有节点之间的距离
for (let k = 0; k < vertices; k++) {
    for (let i = 0; i < vertices; i++) {
        for (let j = 0; j < vertices; j++) {
            // ... 实现代码
        }
    }
}
```

**正则表达式模式**
```javascript
// 好：解释正则表达式匹配的内容
// 匹配电子邮件格式：用户名@域名.扩展名
const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
```

**API 限制或注意事项**
```javascript
// 好：解释外部限制
// GitHub API 速率限制：认证用户每小时 5000 次请求
await rateLimiter.wait();
const response = await fetch(githubApiUrl);
```

## 决策框架

在编写注释之前，请问：
1. **代码是否自解释？** → 不需要注释
2. **是否可以通过更好的变量/函数名消除注释？** → 进行重构
3. **这个注释是否解释了“为什么”而不是“是什么”？** → 好的注释
4. **这是否有助于未来的维护者？** → 好的注释

## 需要注释的特殊情况

### 公共 API
```javascript
/**
 * 使用标准公式计算复利。
 * 
 * @param {number} principal - 初始投资金额
 * @param {number} rate - 年利率（以小数表示，例如 0.05 表示 5%）
 * @param {number} time - 年数
 * @param {number} compoundFrequency - 每年复利次数（默认值：1）
 * @returns {number} 复利后的最终金额
 */
function calculateCompoundInterest(principal, rate, time, compoundFrequency = 1) {
    // ... 实现代码
}
```

### 配置和常量
```javascript
// 好：解释来源或原因
const MAX_RETRIES = 3;  // 基于网络可靠性研究
const API_TIMEOUT = 5000;  // AWS Lambda 的超时时间为 15 秒，保留缓冲时间
```

### 注释标记
```javascript
// TODO：在安全审查后替换为正确的用户认证方式
// FIXME：生产环境存在内存泄漏 - 需要调查连接池问题
// HACK：库 v2.1.0 的一个变通方法 - 升级后移除
// NOTE：此实现假设所有计算使用 UTC 时区
// WARNING：此函数会修改原始数组，而不是创建副本
// PERF：如果在热点路径中频繁调用，考虑缓存此结果
// SECURITY：在使用于查询前，验证输入以防止 SQL 注入
// BUG：当数组为空时会出现边缘情况故障 - 需要调查
// REFACTOR：将此逻辑提取到单独的实用函数中以提高可重用性
// DEPRECATED：请改用 newApiFunction() - 该函数将在 v3.0 中移除
```

## 需要避免的反模式

### 死代码注释
```javascript
// 不好：不要注释掉代码
// const oldFunction = () => { ... };
const newFunction = () => { ... };
```

### 变更日志注释
```javascript
// 不好：不要在注释中维护历史记录
// 2023-01-15 由 John 修改
// 2023-02-03 修复 Sarah 报告的错误
function processData() {
    // ... 实现代码
}
```

### 分隔符注释
```javascript
// 不好：不要使用装饰性注释
//======================================================
// 工具函数
//======================================================
```

## 质量检查清单

在提交代码前，请确保注释：
- [ ] 解释“为什么”，而非“是什么”
- [ ] 语法正确且清晰
- [ ] 随着代码演进仍保持准确
- [ ] 对代码理解有真正的价值
- [ ] 放置在描述的代码上方
- [ ] 使用正确的拼写和专业语言

## 总结

记住：**最好的注释就是你不需要写的注释，因为代码本身已经自解释。**
---
name: 重构
description: '对代码进行外科级重构以提高可维护性，而不改变其行为。涵盖提取函数、重命名变量、拆分巨型函数、提高类型安全性、消除代码异味以及应用设计模式。相较于repo-rebuilder更为温和；适用于逐步改进。'
license: MIT
---

# 重构

## 概述

在不改变外部行为的前提下，改善代码结构和可读性。重构是一种渐进式演进，而非颠覆性变革。用于改进现有代码，而非从头开始重写。

## 何时使用

使用此技能时：

- 代码难以理解或维护
- 函数/类过于庞大
- 需要解决代码异味
- 由于代码结构复杂，添加新功能困难
- 用户要求“清理这段代码”，“重构这段代码”，“改进这段代码”

---

## 重构原则

### 黄金规则

1. **行为保持不变** - 重构不会改变代码的功能，仅改变实现方式
2. **小步进行** - 进行微小的更改，每次更改后测试
3. **版本控制是你的朋友** - 每次安全状态前后都进行提交
4. **测试至关重要** - 没有测试，你不是在重构，而是在编辑
5. **一次只做一件事** - 不要将重构与功能更改混合进行

### 不要重构的情况

```
- 已经正常运行且不会再次更改的代码（如果它没有坏...）
- 缺乏测试的生产代码（先添加测试）
- 在紧迫的截止日期下
- “仅仅因为” - 需要明确目的
```

---

## 常见代码异味及修复方法

### 1. 长函数/方法

```diff
# 原始代码：一个200行的函数，完成所有操作
- async function processOrder(orderId) {
-   // 50行：获取订单
-   // 30行：验证订单
-   // 40行：计算定价
-   // 30行：更新库存
-   // 20行：创建发货单
-   // 30行：发送通知
- }

# 优化代码：拆分为专注函数
+ async function processOrder(orderId) {
+   const order = await fetchOrder(orderId);
+   validateOrder(order);
+   const pricing = calculatePricing(order);
+   await updateInventory(order);
+   const shipment = await createShipment(order);
+   await sendNotifications(order, pricing, shipment);
+   return { order, pricing, shipment };
+ }
```

### 2. 重复代码

```diff
# 原始代码：相同逻辑出现在多个地方
- function calculateUserDiscount(user) {
-   if (user.membership === 'gold') return user.total * 0.2;
-   if (user.membership === 'silver') return user.total * 0.1;
-   return 0;
- }
-
- function calculateOrderDiscount(order) {
-   if (order.user.membership === 'gold') return order.total * 0.2;
-   if (order.user.membership === 'silver') return order.total * 0.1;
-   return 0;
- }

# 优化代码：提取公共逻辑
+ function getMembershipDiscountRate(membership) {
+   const rates = { gold: 0.2, silver: 0.1 };
+   return rates[membership] || 0;
+ }
+
+ function calculateUserDiscount(user) {
+   return user.total * getMembershipDiscountRate(user.membership);
+ }
+
+ function calculateOrderDiscount(order) {
+   return order.total * getMembershipDiscountRate(order.user.membership);
+ }
```

### 3. 大类/模块

```diff
# 原始代码：拥有过多方法的上帝类
- class UserManager {
-   createUser() { /* ... */ }
-   updateUser() { /* ... */ }
-   deleteUser() { /* ... */ }
-   sendEmail() { /* ... */ }
-   generateReport() { /* ... */ }
-   handlePayment() { /* ... */ }
-   validateAddress() { /* ... */ }
-   // 50个更多方法...
- }

# 优化代码：每个类只负责一件事
+ class UserService {
+   create(data) { /* ... */ }
+   update(id, data) { /* ... */ }
+   delete(id) { /* ... */ }
+ }
+
+ class EmailService {
+   send(to, subject, body) { /* ... */ }
+ }
+
+ class ReportService {
+   generate(type, params) { /* ... */ }
+ }
+
+ class PaymentService {
+   process(amount, method) { /* ... */ }
+ }
```

### 4. 长参数列表

```diff
# 原始代码：参数过多
- function createUser(email, password, name, age, address, city, country, phone) {
-   /* ... */
- }

# 优化代码：将相关参数分组
+ interface UserData {
+   email: string;
+   password: string;
+   name: string;
+   age?: number;
+   address?: Address;
+   phone?: string;
+ }
+
+ function createUser(data: UserData) {
+   /* ... */
+ }

# 更进一步：使用建造者模式处理复杂构造
+ const user = UserBuilder
+   .email('test@example.com')
+   .password('secure123')
+   .name('Test User')
+   .address(address)
+   .build();
```

### 5. 功能依赖

```diff
# 原始代码：方法使用其他对象的数据多于自身
- class Order {
-   calculateDiscount(user) {
-     if (user.status === 2) { /* ... */ }
-     if (user.membership === 'gold') return user.total * 0.2;
-     if (user.accountAge > 365) return user.total * 0.1;
-     return 0;
-   }
- }

# 优化代码：将逻辑移动到拥有数据的对象
+ class User {
+   getDiscountRate(orderTotal) {
+     if (this.membership === 'gold') return 0.2;
+     if (this.accountAge > 365) return 0.1;
+     return 0;
+   }
+ }
+
+ class Order {
+   calculateDiscount(user) {
+     return this.total * user.getDiscountRate(this.total);
+   }
+ }
```

### 6. 原始类型痴迷

```diff
# 原始代码：使用原始类型表示领域概念
- function sendEmail(to, subject, body) { /* ... */ }
- sendEmail('user@example.com', 'Hello', '...');

- function createPhone(country, number) {
-   return `${country}-${number}`;
- }

# 优化代码：使用领域类型
+ class Email {
+   private constructor(public readonly value: string) {
+     if (!Email.isValid(value)) throw new Error('无效的邮箱');
+   }
+   static create(value: string) { return new Email(value); }
+   static isValid(email: string) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); }
+ }
+
+ class PhoneNumber {
+   constructor(
+     public readonly country: string,
+     public readonly number: string
+   ) {
+     if (!PhoneNumber.isValid(country, number)) throw new Error('无效的电话号码');
+   }
+   toString() { return `${this.country}-${this.number}`; }
+   static isValid(country: string, number: string) { /* ... */ }
+ }
+
+ // 使用示例
+ const email = Email.create('user@example.com');
+ const phone = new PhoneNumber('1', '555-1234');
```

### 7. 魔术数字/字符串

```diff
# 原始代码：未解释的值
- if (user.status === 2) { /* ... */ }
- const discount = total * 0.15;
- setTimeout(callback, 86400000);

# 优化代码：命名常量
+ const UserStatus = {
+   ACTIVE: 1,
+   INACTIVE: 2,
+   SUSPENDED: 3
+ } as const;
+
+ const DISCOUNT_RATES = {
+   STANDARD: 0.1,
+   PREMIUM: 0.15,
+   VIP: 0.2
+ } as const;
+
+ const ONE_DAY_MS = 24 * 60 * 60 * 1000;
+
+ if (user.status === UserStatus.INACTIVE) { /* ... */ }
+ const discount = total * DISCOUNT_RATES.PREMIUM;
+ setTimeout(callback, ONE_DAY_MS);
```

### 8. 嵌套条件语句

```diff
# 原始代码：箭头代码
- function process(order) {
-   if (order) {
-     if (order.user) {
-       if (order.user.isActive) {
-         if (order.total > 0) {
-           return processOrder(order);
+         } else {
+           return { error: '无效的总计' };
+         }
+       } else {
+         return { error: '用户未激活' };
+       }
+     } else {
+       return { error: '没有用户' };
+     }
+   } else {
+     return { error: '没有订单' };
+   }
+ }

# 优化代码：使用守卫子句/提前返回
+ function process(order) {
+   if (!order) return { error: '没有订单' };
+   if (!order.user) return { error: '没有用户' };
+   if (!order.user.isActive) return { error: '用户未激活' };
+   if (order.total <= 0) return { error: '无效的总计' };
+   return processOrder(order);
+ }

# 更进一步：使用Result类型
+ function process(order): Result<ProcessedOrder, Error> {
+   return Result.combine([
+     validateOrderExists(order),
+     validateUserExists(order),
+     validateUserActive(order.user),
+     validateOrderTotal(order)
+   ]).flatMap(() => processOrder(order));
+ }
```

### 9. 死代码

```diff
# 原始代码：未使用的代码残留
- function oldImplementation() { /* ... */ }
- const DEPRECATED_VALUE = 5;
- import { unusedThing } from './somewhere';
- // 注释掉的代码
- // function oldCode() { /* ... */ }

# 优化代码：删除它
+ // 删除未使用的函数、导入和注释代码
+ // 如果需要再次使用，Git历史记录中有它
```

### 10. 不当的亲密关系

```diff
# 原始代码：一个类深入访问另一个类
- class OrderProcessor {
-   process(order) {
-     order.user.profile.address.street;  // 过于亲密
-     order.repository.connection.config;  // 破坏封装
+   }
+ }

# 优化代码：询问而非告知
+ class OrderProcessor {
+   process(order) {
+     order.getShippingAddress();  // 订单知道如何获取它
+     order.save();  // 订单知道如何保存自己
+   }
+ }
```

---

## 提取方法重构

### 重构前后对比

```diff
# 重构前：一个长函数
- function printReport(users) {
-   console.log('USER REPORT');
-   console.log('============');
-   console.log('');
-   console.log(`Total users: ${users.length}`);
-   console.log('');
-   console.log('ACTIVE USERS');
-   console.log('------------');
-   const active = users.filter(u => u.isActive);
-   active.forEach(u => {
-     console.log(`- ${u.name} (${u.email})`);
-   });
-   console.log('');
-   console.log(`Active: ${active.length}`);
-   console.log('');
-   console.log('INACTIVE USERS');
-   console.log('--------------');
-   const inactive = users.filter(u => !u.isActive);
-   inactive.forEach(u => {
-     console.log(`- ${u.name} (${u.email})`);
-   });
-   console.log('');
-   console.log(`Inactive: ${inactive.length}`);
- }

# 重构后：提取方法
+ function printReport(users) {
+   printHeader('USER REPORT');
+   console.log(`Total users: ${users.length}\n`);
+   printUserSection('ACTIVE USERS', users.filter(u => u.isActive));
+   printUserSection('INACTIVE USERS', users.filter(u => !u.isActive));
+ }
+
+ function printHeader(title) {
+   const line = '='.repeat(title.length);
+   console.log(title);
+   console.log(line);
+   console.log('');
+ }
+
+ function printUserSection(title, users) {
+   console.log(title);
+   console.log('-'.repeat(title.length));
+   users.forEach(u => console.log(`- ${u.name} (${u.email})`));
+   console.log('');
+   console.log(`${title.split(' ')[0]}: ${users.length}`);
+   console.log('');
+ }
```

---

## 引入类型安全性

### 从无类型到有类型

```diff
# 重构前：无类型
- function calculateDiscount(user, total, membership, date) {
-   if (membership === 'gold' && date.getDay() === 5) {
-     return total * 0.25;
-   }
-   if (membership === 'gold') return total * 0.2;
-   return total * 0.1;
- }

# 重构后：完整类型安全性
+ type Membership = 'bronze' | 'silver' | 'gold';
+
+ interface User {
+   id: string;
+   name: string;
+   membership: Membership;
+ }
+
+ interface DiscountResult {
+   original: number;
+   discount: number;
+   final: number;
+   rate: number;
+ }
+
+ function calculateDiscount(
+   user: User,
+   total: number,
+   date: Date = new Date()
+ ): DiscountResult {
+   if (total < 0) throw new Error('总计不能为负数');
+
+   let rate = 0.1; // 默认青铜等级
+
+   if (user.membership === 'gold' && date.getDay() === 5) {
+     rate = 0.25; // 金等级周五优惠
+   } else if (user.membership === 'gold') {
+     rate = 0.2;
+   } else if (user.membership === 'silver') {
+     rate = 0.15;
+   }
+
+   const discount = total * rate;
+
+   return {
+     original: total,
+     discount,
+     final: total - discount,
+     rate
+   };
+ }
```

---

## 重构中的设计模式

### 策略模式

```diff
# 重构前：条件逻辑
- function calculateShipping(order, method) {
-   if (method === 'standard') {
-     return order.total > 50 ? 0 : 5.99;
-   } else if (method === 'express') {
-     return order.total > 100 ? 9.99 : 14.99;
+   } else if (method === 'overnight') {
+     return 29.99;
+   }
+ }

# 重构后：策略模式
+ interface ShippingStrategy {
+   calculate(order: Order): number;
+ }
+
+ class StandardShipping implements ShippingStrategy {
+   calculate(order: Order) {
+     return order.total > 50 ? 0 : 5.99;
+   }
+ }
+
+ class ExpressShipping implements ShippingStrategy {
+   calculate(order: Order) {
+     return order.total > 100 ? 9.99 : 14.99;
+   }
+ }
+
+ class OvernightShipping implements ShippingStrategy {
+   calculate(order: Order) {
+     return 29.99;
+   }
+ }
+
+ function calculateShipping(order: Order, strategy: ShippingStrategy) {
+   return strategy.calculate(order);
+ }
```

### 责任链模式

```diff
# 重构前：嵌套验证
- function validate(user) {
-   const errors = [];
-   if (!user.email) errors.push('邮箱必填');
+   else if (!isValidEmail(user.email)) errors.push('邮箱格式不正确');
+   if (!user.name) errors.push('姓名必填');
+   if (user.age < 18) errors.push('必须年满18岁');
+   if (user.country === 'blocked') errors.push('国家不支持');
+   return errors;
+ }

# 重构后：责任链模式
+ abstract class Validator {
+   abstract validate(user: User): string | null;
+   setNext(validator: Validator): Validator {
+     this.next = validator;
+     return validator;
+   }
+   validate(user: User): string | null {
+     const error = this.doValidate(user);
+     if (error) return error;
+     return this.next?.validate(user) ?? null;
+   }
+ }
+
+ class EmailRequiredValidator extends Validator {
+   doValidate(user: User) {
+     return !user.email ? '邮箱必填' : null;
+   }
+ }
+
+ class EmailFormatValidator extends Validator {
+   doValidate(user: User) {
+     return user.email && !isValidEmail(user.email) ? '邮箱格式不正确' : null;
+   }
+ }
+
+ // 构建责任链
+ const validator = new EmailRequiredValidator()
+   .setNext(new EmailFormatValidator())
+   .setNext(new NameRequiredValidator())
+   .setNext(new AgeValidator())
+   .setNext(new CountryValidator());
```

---

## 重构步骤

### 安全的重构流程

```
1. 准备
   - 确保存在测试用例（若缺失则编写）
   - 提交当前状态
   - 创建功能分支

2. 识别
   - 找到需要解决的代码异味
   - 理解代码的功能
   - 制定重构计划

3. 重构（小步进行）
   - 进行一次小更改
   - 运行测试
   - 若测试通过则提交
   - 重复此过程

4. 验证
   - 所有测试通过
   - 如有必要进行手动测试
   - 性能保持不变或有所提升

5. 清理
   - 更新注释
   - 更新文档
   - 最终提交
```

---

## 重构检查清单

### 代码质量

- [ ] 函数体积小 (<50 行)
- [ ] 函数只做一件事
- [ ] 没有重复代码
- [ ] 变量、函数、类具有描述性名称
- [ ] 没有魔术数字/字符串
- [ ] 已删除死代码

### 结构

- [ ] 相关代码集中在一起
- [ ] 模块边界清晰
- [ ] 依赖关系单向流动
- [ ] 没有循环依赖

### 类型安全性

- [ ] 所有公共API都有类型定义
- [ ] 没有未经说明的`any`类型
- [ ] 可空类型显式标记

### 测试

- [ ] 重构后的代码已测试
- [ ] 测试覆盖了边界情况
- [ ] 所有测试通过

---

## 常见重构操作

| 操作                                     | 描述                           |
| ----------------------------------------- | ------------------------------- |
| 提取方法                                  | 将代码片段转换为方法             |
| 提取类                                    | 将行为移动到新类                 |
| 提取接口                                  | 从实现中创建接口                 |
| 方法内联                                 | 将方法体移回调用方               |
| 类内联                                   | 将类行为移回调用方               |
| 方法上移                                 | 将方法移动到超类                 |
| 方法下移                                 | 将方法移动到子类                 |
| 重命名方法/变量                          | 提高清晰度                       |
| 引入参数对象                             | 将相关参数分组                   |
| 用多态替代条件语句                        | 使用多态代替switch/if语句       |
| 用命名常量替代魔术数字                    | 命名常量                         |
| 拆分条件语句                             | 拆分复杂的条件语句               |
| 合并重复条件语句                         | 合并重复的条件语句               |
| 用守卫子句替代嵌套条件语句                | 提前返回                         |
| 引入空对象                                | 消除空值检查                     |
| 用类/枚举替代类型代码                     | 强类型                           |
| 用委托替代继承                           | 用组合代替继承                   |

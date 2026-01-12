

---
description: '适用于任何使用 GitHub Copilot 项目的通用代码审查指南'
applyTo: '**'
excludeAgent: ["coding-agent"]
---

# 通用代码审查指南

适用于任何项目的 GitHub Copilot 代码审查全面指南。这些指南遵循提示工程的最佳实践，提供了一种结构化的方法来审查代码质量、安全性、测试和架构。

## 审查语言

进行代码审查时，请用 **英语**（或指定您偏好的语言）进行回复。

> **定制提示**：通过将 "English" 替换为 "葡萄牙语（巴西）"、"西班牙语"、"法语" 等，可以更改为您的首选语言。

## 审查优先级

进行代码审查时，优先处理以下顺序的问题：

### 🔴 关键（阻止合并）
- **安全性**：漏洞、暴露的密钥、认证/授权问题
- **正确性**：逻辑错误、数据损坏风险、竞态条件
- **破坏性更改**：在未进行版本控制的情况下更改 API 合约
- **数据丢失**：数据丢失或损坏的风险

### 🟡 重要（需要讨论）
- **代码质量**：严重违反 SOLID 原则、过度重复
- **测试覆盖率**：关键路径或新功能缺少测试
- **性能**：明显的性能瓶颈（N+1 查询、内存泄漏）
- **架构**：与已建立模式有显著偏离

### 🟢 建议（非阻断改进）
- **可读性**：命名不佳、逻辑复杂且可以简化
- **优化**：性能改进但不影响功能
- **最佳实践**：轻微偏离规范
- **文档**：缺少或不完整的注释/文档

## 通用审查原则

进行代码审查时，请遵循以下原则：

1. **具体明确**：引用具体的行号、文件名并提供具体示例
2. **提供上下文**：解释为何某事是问题以及潜在影响
3. **建议解决方案**：在适用时展示修正后的代码，而不仅仅是指出问题
4. **建设性反馈**：专注于改进代码，而非批评作者
5. **认可良好实践**：认可编写良好的代码和聪明的解决方案
6. **务实**：并非每个建议都需要立即实施
7. **合并相关评论**：避免对同一主题的多个评论

## 代码质量标准

进行代码审查时，请检查以下内容：

### 清洁代码
- 变量、函数和类具有描述性和有意义的名称
- 单一职责原则：每个函数/类只做一件事且做得很好
- 不重复自己（DRY）：没有代码重复
- 函数应小巧且专注（理想情况下 < 20-30 行）
- 避免深度嵌套代码（最大 3-4 层）
- 避免魔术数字和字符串（使用常量）
- 代码应自文档化；仅在必要时添加注释

### 示例
```javascript
// ❌ 差：命名不佳和魔术数字
function calc(x, y) {
    if (x > 100) return y * 0.15;
    return y * 0.10;
}

// ✅ 好：清晰的命名和常量
const PREMIUM_THRESHOLD = 100;
const PREMIUM_DISCOUNT_RATE = 0.15;
const STANDARD_DISCOUNT_RATE = 0.10;

function calculateDiscount(orderTotal, itemPrice) {
    const isPremiumOrder = orderTotal > PREMIUM_THRESHOLD;
    const discountRate = isPremiumOrder ? PREMIUM_DISCOUNT_RATE : STANDARD_DISCOUNT_RATE;
    return itemPrice * discountRate;
}
```

### 错误处理
- 在适当层级进行正确的错误处理
- 提供有意义的错误信息
- 不要静默失败或忽略异常
- 快速失败：尽早验证输入
- 使用适当的错误类型/异常

### 示例
```python
# ❌ 差：静默失败和通用错误
def process_user(user_id):
    try:
        user = db.get(user_id)
        user.process()
    except:
        pass

# ✅ 好：显式的错误处理
def process_user(user_id):
    if not user_id or user_id <= 0:
        raise ValueError(f"无效的 user_id: {user_id}")

    try:
        user = db.get(user_id)
    except UserNotFoundError:
        raise UserNotFoundError(f"数据库中未找到用户 {user_id}")
    except DatabaseError as e:
        raise ProcessingError(f"无法检索用户 {user_id}: {e}")

    return user.process()
```

## 安全性审查

进行代码审查时，请检查安全性问题：

- **敏感数据**：代码或日志中不包含密码、API 密钥、令牌或个人身份信息（PII）
- **输入验证**：所有用户输入都经过验证和清理
- **SQL 注入**：使用参数化查询，从不使用字符串拼接
- **认证**：在访问资源前进行适当的认证检查
- **授权**：验证用户是否有权限执行操作
- **加密**：使用已建立的库，不要自行实现加密
- **依赖项安全性**：检查依赖项中的已知漏洞

### 示例
```java
// ❌ 差：存在 SQL 注入漏洞
String query = "SELECT * FROM users WHERE email = '" + email + "'";

// ✅ 好：使用参数化查询
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE email = ?"
);
stmt.setString(1, email);
```

```javascript
// ❌ 差：代码中暴露了密钥
const API_KEY = "sk_live_abc123xyz789";

// ✅ 好：使用环境变量
const API_KEY = process.env.API_KEY;
```

## 测试标准

进行代码审查时，请验证测试质量：

- **覆盖率**：关键路径和新功能必须有测试
- **测试名称**：描述性的名称，解释正在测试的内容
- **测试结构**：清晰的安排-执行-断言或给定-当-则模式
- **独立性**：测试不应依赖彼此或外部状态
- **断言**：使用具体的断言，避免通用的 assertTrue/assertFalse
- **边界情况**：测试边界条件、空值、空集合
- **适当模拟**：模拟外部依赖项，而不是领域逻辑

### 示例
```typescript
// ❌ 差：名称模糊和通用断言
test('test1', () => {
    const result = calc(5, 10);
    expect(result).toBeTruthy();
});

// ✅ 好：描述性名称和具体断言
test('应为总金额低于 100 美元的订单计算 10% 折扣', () => {
    const orderTotal = 50;
    const itemPrice = 20;

    const discount = calculateDiscount(orderTotal, itemPrice);

    expect(discount).toBe(2.00);
});
```

## 性能考虑

进行代码审查时，请检查性能问题：

- **数据库查询**：避免 N+1 查询，使用适当的索引
- **算法**：针对用例使用适当的时/空间复杂度
- **缓存**：对昂贵或重复的操作使用缓存
- **资源管理**：正确清理连接、文件、流
- **分页**：大型结果集应进行分页
- **延迟加载**：仅在需要时加载数据

### 示例
```python
# ❌ 差：N+1 查询问题
users = User.query.all()
for user in users:
    orders = Order.query.filter_by(user_id=user.id).all()  # N+1!

# ✅ 好：使用 JOIN 或急切加载
users = User.query.options(joinedload(User.orders)).all()
for user in users:
    orders = user.orders
```

## 架构与设计

进行代码审查时，请验证架构原则：

- **关注点分离**：各层/模块之间有清晰的边界
- **依赖方向**：高层模块不依赖底层细节
- **接口隔离**：优先选择小而专注的接口
- **松耦合**：组件应可独立测试
- **高内聚**：相关功能应分组在一起
- **一致的模式**：遵循代码库中已建立的模式

## 文档标准

进行代码审查时，请检查文档：

- **API 文档**：公共 API 必须有文档说明（用途、参数、返回值）
- **复杂逻辑**：非显而易见的逻辑应有解释性注释
- **README 更新**：在添加功能或更改设置时更新 README
- **破坏性更改**：清晰记录任何破坏性更改
- **示例**：为复杂功能提供使用示例

## 评论格式模板

进行代码审查时，请使用以下格式进行评论：

```markdown
**[优先级] 类别：简短标题**

问题或建议的详细描述。

**为何重要：**
说明建议的影响或原因。

**建议的修复：**
[如有适用，提供代码示例]

**参考：** [相关文档或标准的链接]
```

### 示例评论

#### 关键问题
```markdown
**🔴 关键 - 安全性：SQL 注入漏洞**

第 45 行的查询直接将用户输入拼接到 SQL 字符串中，
创建了 SQL 注入漏洞。

**为何重要：**
攻击者可以操纵电子邮件参数来执行任意 SQL 命令，
可能会导致数据库数据泄露或删除。

**建议的修复：**
```sql
-- 代替：
query = "SELECT * FROM users WHERE email = '" + email + "'"

-- 使用：
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE email = ?"
);
stmt.setString(1, email);
```

**参考：** OWASP SQL 注入防护速查表
```

#### 重要问题
```markdown
**🟡 重要 - 测试：关键路径缺少测试覆盖**

`processPayment()` 函数处理财务交易，但没有针对退款场景的测试。

**为何重要：**
退款涉及资金流动，应彻底测试以防止财务错误或数据不一致。

**建议的修复：**
添加测试用例：
```javascript
test('应为取消的订单处理全额退款', () => {
    const order = createOrder({ total: 100, status: 'cancelled' });

    const result = processPayment(order, { type: 'refund' });

    expect(result.refundAmount).toBe(100);
    expect(result.status).toBe('refunded');
});
```
```

#### 建议
```markdown
**🟢 建议 - 可读性：简化嵌套条件语句**

第 30-40 行的嵌套 if 语句使逻辑难以理解。

**为何重要：**
更简单的代码更容易维护、调试和测试。

**建议的修复：**
```javascript
// 代替嵌套 if：
if (user) {
    if (user.isActive) {
        if (user.hasPermission('write')) {
            // 执行操作
        }
    }
}

// 考虑使用守卫子句：
if (!user || !user.isActive || !user.hasPermission('write')) {
    return;
}
// 执行操作
```
```

## 审查清单

进行代码审查时，请系统地验证以下内容：

### 代码质量
- [ ] 代码遵循一致的风格和规范
- [ ] 名称具有描述性并遵循命名规范
- [ ] 函数/方法小巧且专注
- [ ] 没有代码重复
- [ ] 复杂逻辑被拆分为更简单的部分
- [ ] 错误处理适当
- [ ] 没有未附带任务的注释代码或 TODO

### 安全性
- [ ] 代码或日志中没有敏感数据
- [ ] 所有用户输入都进行了验证
- [ ] 没有 SQL 注入漏洞
- [ ] 认证和授权正确实现
- [ ] 依赖项已更新且安全

### 测试
- [ ] 新代码有适当的测试覆盖率
- [ ] 测试名称清晰且聚焦
- [ ] 测试覆盖边界情况和错误场景
- [ ] 测试独立且可确定性
- [ ] 没有总是通过或被注释掉的测试

### 性能
- [ ] 没有明显的性能问题（N+1、内存泄漏）
- [ ] 正确使用缓存
- [ ] 高效的算法和数据结构
- [ ] 正确清理资源

### 架构
- [ ] 遵循已建立的模式和规范
- [ ] 正确的分层和模块划分
- [ ] 没有架构违规
- [ ] 依赖项流向正确方向

### 文档
- [ ] 公共 API 有文档说明
- [ ] 复杂逻辑有解释性注释
- [ ] 如有需要，更新 README
- [ ] 记录所有破坏性更改

## 项目特定定制

要为您的项目定制此模板，请添加以下部分：

1. **语言/框架特定检查**
   - 示例：进行代码审查时，请验证 React 钩子是否遵循钩子规则
   - 示例：进行代码审查时，请检查 Spring Boot 控制器是否使用了正确的注解

2. **构建和部署**
   - 示例：进行代码审查时，请验证 CI/CD 流水线配置是否正确
   - 示例：进行代码审查时，请检查数据库迁移是否可逆

3. **业务逻辑规则**
   - 示例：进行代码审查时，请验证定价计算是否包含所有适用的税费
   - 示例：进行代码审查时，请检查在数据处理前是否获取了用户同意

4. **团队规范**
   - 示例：进行代码审查时，请验证提交信息是否遵循常规提交格式
   - 示例：进行代码审查时，请检查分支名称是否遵循模式：类型/票务描述

## 额外资源

如需了解有效的代码审查和 GitHub Copilot 定制的更多信息：

- [GitHub Copilot 提示工程](https://docs.github.com/en/copilot/concepts/prompting/prompt-engineering)
- [GitHub Copilot 自定义指令](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [Awesome GitHub Copilot 仓库](https://github.com/github/awesome-copilot)
- [GitHub 代码审查指南](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)
- [Google 工程实践 - 代码审查](https://google.github.io/eng-practices/review/)
- [OWASP 安全指南](https://owasp.org/)

## 提示工程技巧

进行代码审查时，请应用以下提示工程原则，这些原则来自 [GitHub Copilot 文档](https://docs.github.com/en/copilot/concepts/prompting/prompt-engineering)：

1. **从一般开始，再具体深入**：先进行高层次架构审查，再深入实现细节
2. **提供示例**：在建议更改时引用代码库中的类似模式
3. **分解复杂任务**：将大型 PR 分为逻辑块进行审查（安全性 → 测试 → 逻辑 → 风格）
4. **避免歧义**：明确指出您正在处理的文件、行号和问题
5. **指示相关代码**：引用可能受更改影响的相关代码
6. **实验和迭代**：如果初始审查遗漏了某些内容，可以通过聚焦问题再次审查
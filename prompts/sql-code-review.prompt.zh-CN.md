

---
agent: '代理'
tools: ['更改', '代码库搜索', '编辑文件', '问题']
description: '通用SQL代码审查助手，能够对所有SQL数据库（MySQL、PostgreSQL、SQL Server、Oracle）进行全面的安全性、可维护性和代码质量分析。重点关注SQL注入预防、访问控制、代码标准和反模式检测。与SQL优化提示相结合，实现完整的开发覆盖。'
tested_with: 'GitHub Copilot Chat (GPT-4o) - 验证日期：2025年7月20日'
---

# SQL代码审查

对${selection}（或整个项目，若未选择）进行彻底的SQL代码审查，重点关注安全性、性能、可维护性以及数据库最佳实践。

## 🔒 安全性分析

### SQL注入预防
```sql
-- ❌ 严重：SQL注入漏洞
query = "SELECT * FROM users WHERE id = " + userInput;
query = f"DELETE FROM orders WHERE user_id = {user_id}";

-- ✅ 安全：参数化查询
-- PostgreSQL/MySQL
PREPARE stmt FROM 'SELECT * FROM users WHERE id = ?';
EXECUTE stmt USING @user_id;

-- SQL Server
EXEC sp_executesql N'SELECT * FROM users WHERE id = @id', N'@id INT', @id = @user_id;
```

### 访问控制与权限
- **最小特权原则**：授予最小必要的权限
- **基于角色的访问**：使用数据库角色而非直接用户权限
- **模式安全性**：确保模式所有权和访问控制合理
- **函数/存储过程安全性**：检查DEFINER与INVOKER权限的使用

### 数据保护
- **敏感数据暴露**：避免对包含敏感列的表使用SELECT *
- **审计日志**：确保敏感操作被记录
- **数据脱敏**：使用视图或函数对敏感数据进行脱敏
- **加密**：验证敏感数据的加密存储

## ⚡ 性能优化

### 查询结构分析
```sql
-- ❌ 差：低效查询模式
SELECT DISTINCT u.* 
FROM users u, orders o, products p
WHERE u.id = o.user_id 
AND o.product_id = p.id
AND YEAR(o.order_date) = 2024;

-- ✅ 好：优化后的结构
SELECT u.id, u.name, u.email
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.order_date >= '2024-01-01' 
AND o.order_date < '2025-01-01';
```

### 索引策略审查
- **缺失索引**：识别需要创建索引的列
- **过度索引**：查找未使用或冗余的索引
- **复合索引**：为复杂查询创建多列索引
- **索引维护**：检查碎片化或过时的索引

### 连接优化
- **连接类型**：验证使用适当的连接类型（INNER vs LEFT vs EXISTS）
- **连接顺序**：优先优化较小的结果集
- **笛卡尔积**：识别并修复缺少连接条件的情况
- **子查询 vs 连接**：选择最高效的方法

### 聚合和窗口函数
```sql
-- ❌ 差：低效的聚合
SELECT user_id, 
       (SELECT COUNT(*) FROM orders o2 WHERE o2.user_id = o1.user_id) as order_count
FROM orders o1
GROUP BY user_id;

-- ✅ 好：高效的聚合
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id;
```

## 🛠️ 代码质量与可维护性

### SQL风格与格式化
```sql
-- ❌ 差：差的格式和风格
select u.id,u.name,o.total from users u left join orders o on u.id=o.user_id where u.status='active' and o.order_date>='2024-01-01';

-- ✅ 好：整洁、易读的格式
SELECT u.id,
       u.name,
       o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
  AND o.order_date >= '2024-01-01';
```

### 命名规范
- **一致的命名**：表、列、约束遵循一致的命名模式
- **描述性名称**：为数据库对象使用清晰、有意义的名称
- **保留字**：避免使用数据库保留字作为标识符
- **大小写一致性**：在模式中保持一致的大小写使用

### 模式设计审查
- **规范化**：适当的规范化级别（避免过度或不足的规范化）
- **数据类型**：为存储和性能选择最佳数据类型
- **约束**：正确使用PRIMARY KEY、FOREIGN KEY、CHECK、NOT NULL
- **默认值**：为列选择适当的默认值

## 🗄️ 数据库特定最佳实践

### PostgreSQL
```sql
-- 使用JSONB处理JSON数据
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 为JSONB查询创建GIN索引
CREATE INDEX idx_events_data ON events USING gin(data);

-- 使用数组类型处理多值列
CREATE TABLE tags (
    post_id INT,
    tag_names TEXT[]
);
```

### MySQL
```sql
-- 使用适当的存储引擎
CREATE TABLE sessions (
    id VARCHAR(128) PRIMARY KEY,
    data TEXT,
    expires TIMESTAMP
) ENGINE=InnoDB;

-- 为InnoDB优化
ALTER TABLE large_table 
ADD INDEX idx_covering (status, created_at, id);
```

### SQL Server
```sql
-- 使用适当的数据类型
CREATE TABLE products (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at DATETIME2 DEFAULT GETUTCDATE()
);

-- 为分析使用列存储索引
CREATE COLUMNSTORE INDEX idx_sales_cs ON sales;
```

### Oracle
```sql
-- 使用序列实现自增
CREATE SEQUENCE user_id_seq START WITH 1 INCREMENT BY 1;

CREATE TABLE users (
    id NUMBER DEFAULT user_id_seq.NEXTVAL PRIMARY KEY,
    name VARCHAR2(255) NOT NULL
);
```

## 🧪 测试与验证

### 数据完整性检查
```sql
-- 验证参照完整性
SELECT o.user_id 
FROM orders o 
LEFT JOIN users u ON o.user_id = u.id 
WHERE u.id IS NULL;

-- 检查数据一致性
SELECT COUNT(*) as inconsistent_records
FROM products 
WHERE price < 0 OR stock_quantity < 0;
```

### 性能测试
- **执行计划**：审查查询执行计划
- **负载测试**：使用真实数据量测试查询
- **压力测试**：验证并发负载下的性能
- **回归测试**：确保优化不会破坏功能

## 📊 常见反模式

### N+1查询问题
```sql
-- ❌ 差：应用程序代码中的N+1查询
for user in users:
    orders = query("SELECT * FROM orders WHERE user_id = ?", user.id)

-- ✅ 好：单次优化查询
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

### 过度使用DISTINCT
```sql
-- ❌ 差：DISTINCT掩盖了连接问题
SELECT DISTINCT u.name 
FROM users u, orders o 
WHERE u.id = o.user_id;

-- ✅ 好：无需DISTINCT的正确连接
SELECT u.name
FROM users u
INNER JOIN orders o ON u.id = o.user_id
GROUP BY u.name;
```

### WHERE子句中函数误用
```sql
-- ❌ 差：函数阻止了索引使用
SELECT * FROM orders 
WHERE YEAR(order_date) = 2024;

-- ✅ 好：使用范围条件并利用索引
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' 
  AND order_date < '2025-01-01';
```

## 📋 SQL审查清单

### 安全性
- [ ] 所有用户输入均经过参数化
- [ ] 未使用字符串拼接构建动态SQL
- [ ] 适当的访问控制和权限设置
- [ ] 敏感数据得到妥善保护
- [ ] 消除了SQL注入攻击向量

### 性能
- [ ] 频繁查询的列已建立索引
- [ ] 不存在不必要的SELECT *语句
- [ ] 连接已优化并使用适当的类型
- [ ] WHERE子句具有选择性且使用索引
- [ ] 子查询已优化或转换为连接

### 代码质量
- [ ] 命名规范保持一致
- [ ] 代码格式和缩进正确
- [ ] 复杂逻辑有清晰注释
- [ ] 使用了适当的数据类型
- [ ] 实现了错误处理机制

### 模式设计
- [ ] 表结构合理规范化
- [ ] 约束确保数据完整性
- [ ] 索引支持查询模式
- [ ] 定义了外键关系
- [ ] 默认值适当

## 🎯 审查输出格式

### 问题模板
```
## [优先级] [类别]: [简要描述]

**位置**: [表/视图/存储过程名称及行号（如适用）]
**问题**: [问题的详细说明]
**安全风险**: [如适用 - 注入风险、数据暴露等]
**性能影响**: [查询成本、执行时间影响]
**建议**: [具体修复方案及代码示例]

**之前**:
```sql
-- 存在隐患的SQL
```

**之后**:
```sql
-- 优化后的SQL
```

**预期改进**: [性能提升、安全优势]
```

### 总结评估
- **安全性评分**: [1-10] - SQL注入防护、访问控制
- **性能评分**: [1-10] - 查询效率、索引使用
- **可维护性评分**: [1-10] - 代码质量、文档完整性
- **模式质量评分**: [1-10] - 设计模式、规范化程度

### 优先级最高的3项行动
1. **[关键安全修复]**: 修复SQL注入漏洞
2. **[性能优化]**: 添加缺失索引或优化查询
3. **[代码质量]**: 改进命名规范和文档

在提供可操作的、与数据库无关的建议的同时，突出平台特定的优化和最佳实践。
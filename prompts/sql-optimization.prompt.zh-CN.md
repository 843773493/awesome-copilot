

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems']
description: '通用SQL性能优化助手，用于跨所有SQL数据库（MySQL、PostgreSQL、SQL Server、Oracle）的全面查询调优、索引策略和数据库性能分析。提供执行计划分析、分页优化、批量操作和性能监控指导。'
tested_with: '测试环境：GitHub Copilot Chat (GPT-4o) - 2025年7月20日验证'
---

# SQL性能优化助手

针对${selection}（或整个项目，若无选择）进行专家级SQL性能优化。重点关注适用于MySQL、PostgreSQL、SQL Server、Oracle及其他SQL数据库的通用优化技术。

## 🎯 核心优化领域

### 查询性能分析
```sql
-- ❌ 不良：低效的查询模式
SELECT * FROM orders o
WHERE YEAR(o.created_at) = 2024
  AND o.customer_id IN (
      SELECT c.id FROM customers c WHERE c.status = 'active'
  );

-- ✅ 良好：通过适当索引提示优化查询
SELECT o.id, o.customer_id, o.total_amount, o.created_at
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.created_at >= '2024-01-01' 
  AND o.created_at < '2025-01-01'
  AND c.status = 'active';

-- 所需索引：
-- CREATE INDEX idx_orders_created_at ON orders(created_at);
-- CREATE INDEX idx_customers_status ON customers(status);
-- CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

### 索引策略优化
```sql
-- ❌ 不良：较差的索引策略
CREATE INDEX idx_user_data ON users(email, first_name, last_name, created_at);

-- ✅ 良好：优化的复合索引
-- 用于按email筛选后按created_at排序的查询
CREATE INDEX idx_users_email_created ON users(email, created_at);

-- 用于全文本名称搜索
CREATE INDEX idx_users_name ON users(last_name, first_name);

-- 用于用户状态查询
CREATE INDEX idx_users_status_created ON users(status, created_at)
WHERE status IS NOT NULL;
```

### 子查询优化
```sql
-- ❌ 不良：相关子查询
SELECT p.product_name, p.price
FROM products p
WHERE p.price > (
    SELECT AVG(price) 
    FROM products p2 
    WHERE p2.category_id = p.category_id
);

-- ✅ 良好：使用窗口函数的方法
SELECT product_name, price
FROM (
    SELECT product_name, price,
           AVG(price) OVER (PARTITION BY category_id) as avg_category_price
    FROM products
) ranked
WHERE price > avg_category_price;
```

## 📊 性能调优技术

### JOIN优化
```sql
-- ❌ 不良：低效的JOIN顺序和条件
SELECT o.*, c.name, p.product_name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01'
  AND c.status = 'active';

-- ✅ 良好：优化的JOIN与过滤
SELECT o.id, o.total_amount, c.name, p.product_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id AND c.status = 'active'
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01';
```

### 分页优化
```sql
-- ❌ 不良：基于OFFSET的分页（大偏移量时较慢）
SELECT * FROM products 
ORDER BY created_at DESC 
LIMIT 20 OFFSET 10000;

-- ✅ 良好：基于游标的分页
SELECT * FROM products 
WHERE created_at < '2024-06-15 10:30:00'
ORDER BY created_at DESC 
LIMIT 20;

-- 或使用基于ID的游标
SELECT * FROM products 
WHERE id > 1000
ORDER BY id 
LIMIT 20;
```

### 聚合优化
```sql
-- ❌ 不良：多个独立的聚合查询
SELECT COUNT(*) FROM orders WHERE status = 'pending';
SELECT COUNT(*) FROM orders WHERE status = 'shipped';
SELECT COUNT(*) FROM orders WHERE status = 'delivered';

-- ✅ 良好：单个查询的条件聚合
SELECT 
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_count,
    COUNT(CASE WHEN status = 'shipped' THEN 1 END) as shipped_count,
    COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_count
FROM orders;
```

## 🚫 查询反模式

### SELECT性能问题
```sql
-- ❌ 不良：SELECT * 反模式
SELECT * FROM large_table lt
JOIN another_table at ON lt.id = at.ref_id;

-- ✅ 良好：显式列选择
SELECT lt.id, lt.name, at.value
FROM large_table lt
JOIN another_table at ON lt.id = at.ref_id;
```

### WHERE子句优化
```sql
-- ❌ 不良：WHERE子句中使用函数导致索引失效
SELECT * FROM orders 
WHERE UPPER(customer_email) = 'JOHN@EXAMPLE.COM';

-- ✅ 良好：索引友好的WHERE子句
SELECT * FROM orders 
WHERE customer_email = 'john@example.com';
-- 建议：CREATE INDEX idx_orders_email ON orders(LOWER(customer_email));
```

### OR与UNION优化
```sql
-- ❌ 不良：复杂的OR条件
SELECT * FROM products 
WHERE (category = 'electronics' AND price < 1000)
   OR (category = 'books' AND price < 50);

-- ✅ 良好：使用UNION实现更好优化
SELECT * FROM products WHERE category = 'electronics' AND price < 1000
UNION ALL
SELECT * FROM products WHERE category = 'books' AND price < 50;
```

## 📈 与数据库无关的优化

### 批量操作
```sql
-- ❌ 不良：逐行操作
INSERT INTO products (name, price) VALUES ('Product 1', 10.00);
INSERT INTO products (name, price) VALUES ('Product 2', 15.00);
INSERT INTO products (name, price) VALUES ('Product 3', 20.00);

-- ✅ 良好：批量插入
INSERT INTO products (name, price) VALUES 
('Product 1', 10.00),
('Product 2', 15.00),
('Product 3', 20.00);
```

### 临时表使用
```sql
-- ✅ 良好：使用临时表处理复杂操作
CREATE TEMPORARY TABLE temp_calculations AS
SELECT customer_id, 
       SUM(total_amount) as total_spent,
       COUNT(*) as order_count
FROM orders 
WHERE created_at >= '2024-01-01'
GROUP BY customer_id;

-- 使用临时表进行进一步计算
SELECT c.name, tc.total_spent, tc.order_count
FROM temp_calculations tc
JOIN customers c ON tc.customer_id = c.id
WHERE tc.total_spent > 1000;
```

## 🛠️ 索引管理

### 索引设计原则
```sql
-- ✅ 良好：覆盖索引设计
CREATE INDEX idx_orders_covering 
ON orders(customer_id, created_at) 
INCLUDE (total_amount, status);  -- SQL Server语法
-- 或：CREATE INDEX idx_orders_covering ON orders(customer_id, created_at, total_amount, status); -- 其他数据库
```

### 部分索引策略
```sql
-- ✅ 良好：针对特定条件的部分索引
CREATE INDEX idx_orders_active 
ON orders(created_at) 
WHERE status IN ('pending', 'processing');
```

## 📊 性能监控查询

### 查询性能分析
```sql
-- 通用方法识别慢查询
-- （不同数据库的语法略有差异）

-- 对于MySQL：
SELECT query_time, lock_time, rows_sent, rows_examined, sql_text
FROM mysql.slow_log
ORDER BY query_time DESC;

-- 对于PostgreSQL：
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC;

-- 对于SQL Server：
SELECT 
    qs.total_elapsed_time/qs.execution_count as avg_elapsed_time,
    qs.execution_count,
    SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text)
        ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) as query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY avg_elapsed_time DESC;
```

## 🎯 通用优化检查清单

### 查询结构
- [ ] 避免在生产查询中使用SELECT *
- [ ] 使用适当的JOIN类型（INNER vs LEFT/RIGHT）
- [ ] 在WHERE子句中尽早过滤
- [ ] 适当情况下使用EXISTS替代IN进行子查询
- [ ] 避免在WHERE子句中使用阻止索引使用的函数

### 索引策略
- [ ] 在频繁查询的列上创建索引
- [ ] 在合适的列顺序上使用复合索引
- [ ] 避免过度索引（影响INSERT/UPDATE性能）
- [ ] 在有益时使用覆盖索引
- [ ] 为特定查询模式创建部分索引

### 数据类型与模式
- [ ] 使用适合的数据类型以提高存储效率
- [ ] 适当规范化（OLTP使用第三范式，OLAP使用反规范化）
- [ ] 使用约束辅助查询优化器
- [ ] 在适当情况下对大表进行分区

### 查询模式
- [ ] 使用LIMIT/TOP控制结果集
- [ ] 实现高效的分页策略
- [ ] 使用批量操作进行大批量数据变更
- [ ] 避免N+1查询问题
- [ ] 对重复查询使用预编译语句

### 性能测试
- [ ] 使用真实数据量测试查询
- [ ] 分析查询执行计划
- [ ] 长期监控查询性能
- [ ] 为慢查询设置警报
- [ ] 定期分析索引使用情况

## 📝 优化方法论

1. **识别**：使用数据库特定工具查找慢查询
2. **分析**：检查执行计划并识别瓶颈
3. **优化**：应用适当的优化技术
4. **测试**：验证性能提升
5. **监控**：持续跟踪性能指标
6. **迭代**：定期进行性能审查和优化

关注可衡量的性能提升，并始终使用真实数据量和查询模式测试优化方案。
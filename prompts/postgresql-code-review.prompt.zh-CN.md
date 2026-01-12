

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems']
description: '专注于PostgreSQL特有最佳实践、反模式和独特质量标准的代码审查助手。涵盖JSONB操作、数组使用、自定义类型、模式设计、函数优化以及PostgreSQL独有的安全功能，如行级安全（RLS）。'
tested_with: 'GitHub Copilot Chat (GPT-4o) - 2025年7月20日验证'
---

# PostgreSQL代码审查助手

对${selection}（或整个项目，如果未选择）进行专家级PostgreSQL代码审查。重点关注PostgreSQL特有的最佳实践、反模式和质量标准。

## 🎯 PostgreSQL特有审查领域

### JSONB最佳实践
```sql
-- ❌ 不佳：低效的JSONB使用
SELECT * FROM orders WHERE data->>'status' = 'shipped';  -- 无索引支持

-- ✅ 合规：可索引的JSONB查询
CREATE INDEX idx_orders_status ON orders USING gin((data->'status'));
SELECT * FROM orders WHERE data @> '{"status": "shipped"}';

-- ❌ 不佳：未考虑深度嵌套
UPDATE orders SET data = data || '{"shipping":{"tracking":{"number":"123"}}}';

-- ✅ 合规：结构化的JSONB与验证
ALTER TABLE orders ADD CONSTRAINT valid_status 
CHECK (data->>'status' IN ('pending', 'shipped', 'delivered'));
```

### 数组操作审查
```sql
-- ❌ 不佳：低效的数组操作
SELECT * FROM products WHERE 'electronics' = ANY(categories);  -- 无索引

-- ✅ 合规：使用GIN索引的数组查询
CREATE INDEX idx_products_categories ON products USING gin(categories);
SELECT * FROM products WHERE categories @> ARRAY['electronics'];

-- ❌ 不佳：循环中进行数组拼接
-- 这在函数/存储过程中会效率低下

-- ✅ 合规：批量数组操作
UPDATE products SET categories = categories || ARRAY['new_category']
WHERE id IN (SELECT id FROM products WHERE condition);
```

### PostgreSQL模式设计审查
```sql
-- ❌ 不佳：未使用PostgreSQL特性
CREATE TABLE users (
    id INTEGER,
    email VARCHAR(255),
    created_at TIMESTAMP
);

-- ✅ 合规：PostgreSQL优化的模式
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email CITEXT UNIQUE NOT NULL,  -- 不区分大小写的邮箱
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- 为元数据查询添加JSONB GIN索引
CREATE INDEX idx_users_metadata ON users USING gin(metadata);
```

### 自定义类型和域
```sql
-- ❌ 不佳：使用通用类型处理特定数据
CREATE TABLE transactions (
    amount DECIMAL(10,2),
    currency VARCHAR(3),
    status VARCHAR(20)
);

-- ✅ 合规：PostgreSQL自定义类型
CREATE TYPE currency_code AS ENUM ('USD', 'EUR', 'GBP', 'JPY');
CREATE TYPE transaction_status AS ENUM ('pending', 'completed', 'failed', 'cancelled');
CREATE DOMAIN positive_amount AS DECIMAL(10,2) CHECK (VALUE > 0);

CREATE TABLE transactions (
    amount positive_amount NOT NULL,
    currency currency_code NOT NULL,
    status transaction_status DEFAULT 'pending'
);
```

## 🔍 PostgreSQL特有反模式

### 性能反模式
- **避免使用PostgreSQL特有索引**：未为适当的数据类型使用GIN/GiST索引
- **错误使用JSONB**：将JSONB当作普通字符串字段处理
- **忽略数组操作符**：使用低效的数组操作
- **分区键选择不当**：未有效利用PostgreSQL的分区功能

### 模式设计问题
- **未使用ENUM类型**：对有限值集合使用VARCHAR
- **忽略约束**：缺少用于数据验证的CHECK约束
- **数据类型错误**：使用VARCHAR而非TEXT或CITEXT
- **JSONB结构缺失**：未结构化且无验证的JSONB字段

### 函数和触发器问题
```sql
-- ❌ 不佳：低效的触发器函数
CREATE OR REPLACE FUNCTION update_modified_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();  -- 应使用TIMESTAMPTZ
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ✅ 合规：优化的触发器函数
CREATE OR REPLACE FUNCTION update_modified_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 设置仅在需要时触发
CREATE TRIGGER update_modified_time_trigger
    BEFORE UPDATE ON table_name
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION update_modified_time();
```

## 📊 PostgreSQL扩展使用审查

### 扩展最佳实践
```sql
-- ✅ 合规：创建扩展前检查是否存在
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ✅ 合规：适当使用扩展
-- UUID生成
SELECT uuid_generate_v4();

-- 密码哈希
SELECT crypt('password', gen_salt('bf'));

-- 模糊文本匹配
SELECT word_similarity('postgres', 'postgre');
```

## 🛡️ PostgreSQL安全审查

### 行级安全（RLS）
```sql
-- ✅ 合规：实现RLS
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_data_policy ON sensitive_data
    FOR ALL TO application_role
    USING (user_id = current_setting('app.current_user_id')::INTEGER);
```

### 权限管理
```sql
-- ❌ 不佳：权限过于宽泛
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;

-- ✅ 合规：细粒度权限
GRANT SELECT, INSERT, UPDATE ON specific_table TO app_user;
GRANT USAGE ON SEQUENCE specific_table_id_seq TO app_user;
```

## 🎯 PostgreSQL代码质量检查清单

### 模式设计
- [ ] 使用适当的PostgreSQL数据类型（CITEXT、JSONB、数组）
- [ ] 对受限值使用ENUM类型
- [ ] 实现正确的CHECK约束
- [ ] 使用TIMESTAMPTZ而非TIMESTAMP
- [ ] 为可重用约束定义自定义域

### 性能考量
- [ ] 适当的索引类型（JSONB/数组使用GIN，范围使用GiST）
- [ ] 使用包含操作符（@>、?）进行JSONB查询
- [ ] 使用PostgreSQL特有操作符进行数组操作
- [ ] 正确使用窗口函数和CTEs
- [ ] 高效使用PostgreSQL特有函数

### PostgreSQL功能利用
- [ ] 在合适场景使用扩展
- [ ] 在有益时使用PL/pgSQL实现存储过程
- [ ] 利用PostgreSQL的高级SQL功能
- [ ] 使用PostgreSQL特有优化技术
- [ ] 在函数中实现正确的错误处理

### 安全与合规
- [ ] 在需要时实现行级安全（RLS）
- [ ] 正确管理角色和权限
- [ ] 使用PostgreSQL内置的加密函数
- [ ] 使用PostgreSQL特性实现审计追踪

## 📝 PostgreSQL特有审查指南

1. **数据类型优化**：确保适当使用PostgreSQL特有类型
2. **索引策略**：审查索引类型并确保使用PostgreSQL特有索引
3. **JSONB结构**：验证JSONB模式设计和查询模式
4. **函数质量**：审查PL/pgSQL函数的效率和最佳实践
5. **扩展使用**：验证PostgreSQL扩展的适当使用
6. **性能功能**：检查PostgreSQL高级功能的使用情况
7. **安全实现**：审查PostgreSQL特有安全功能

聚焦PostgreSQL的独特能力，确保代码充分利用其特有功能，而非将其视为通用SQL数据库。
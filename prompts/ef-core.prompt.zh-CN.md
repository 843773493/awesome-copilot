

---
agent: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems', 'runCommands']
description: '获取 Entity Framework Core 的最佳实践'
---

# Entity Framework Core 最佳实践

你的目标是帮助我在使用 Entity Framework Core 时遵循最佳实践。

## 数据上下文设计

- 保持 DbContext 类的专注性和一致性
- 使用构造函数注入进行配置选项设置
- 通过 fluent API 配置重写 OnModelCreating 方法
- 使用 IEntityTypeConfiguration 分离实体配置
- 考虑在控制台应用或测试中使用 DbContextFactory 模式

## 实体设计

- 使用有意义的主键（考虑自然键与代理键）
- 实现正确的实体关系（一对一、一对多、多对多）
- 使用数据注解或 fluent API 设置约束和验证
- 实现适当的导航属性
- 考虑使用 owned 实体类型来处理值对象

## 性能优化

- 对只读查询使用 AsNoTracking()
- 对大型结果集使用 Skip() 和 Take() 实现分页
- 在需要时使用 Include() 主动加载相关实体
- 考虑使用投影（Select）仅获取所需字段
- 对频繁执行的查询使用编译查询
- 通过正确包含相关数据避免 N+1 查询问题

## 迁移管理

- 创建小而专注的迁移
- 为迁移命名时使用描述性名称
- 在应用到生产环境前验证迁移的 SQL 脚本
- 考虑使用迁移捆绑包进行部署
- 在适当的情况下通过迁移添加数据初始化

## 查询操作

- 适度使用 IQueryable 并理解查询何时执行
- 优先使用强类型 LINQ 查询而非原始 SQL
- 使用适当的查询操作符（Where、OrderBy、GroupBy）
- 考虑使用数据库函数处理复杂操作
- 为可重用查询实现规范模式

## 变更跟踪与保存

- 使用适当的变更跟踪策略
- 批量调用 SaveChanges()
- 为多用户场景实现并发控制
- 考虑使用事务处理多个操作
- 使用适当的 DbContext 生命周期（Web 应用中使用作用域）

## 安全性

- 通过参数化查询避免 SQL 注入
- 实现适当的数据访问权限
- 谨慎使用原始 SQL 查询
- 考虑对敏感信息进行数据加密
- 使用迁移管理数据库用户权限

## 测试

- 使用内存数据库提供者进行单元测试
- 为集成测试创建带有 SQLite 的独立测试上下文
- 为纯单元测试模拟 DbContext 和 DbSet
- 在隔离环境中测试迁移
- 考虑使用快照测试来验证模型变更

在审查我的 EF Core 代码时，请识别问题并提出遵循这些最佳实践的改进建议。
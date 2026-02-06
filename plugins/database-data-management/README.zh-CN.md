# 数据库与数据管理插件

PostgreSQL、SQL Server 以及通用数据库开发最佳实践的数据库管理、SQL 优化和数据管理工具。

## 安装

```bash
# 使用 Copilot CLI
copilot plugin install database-data-management@awesome-copilot
```

## 包含内容

### 命令（斜杠命令）

| 命令 | 描述 |
|------|------|
| `/database-data-management:sql-优化` | 通用 SQL 性能优化助手，适用于所有 SQL 数据库（MySQL、PostgreSQL、SQL Server、Oracle）的全面查询调优、索引策略和数据库性能分析。提供执行计划分析、分页优化、批量操作和性能监控指导。 |
| `/database-data-management:sql-代码审查` | 通用 SQL 代码审查助手，对所有 SQL 数据库（MySQL、PostgreSQL、SQL Server、Oracle）进行全面的安全性、可维护性和代码质量分析。专注于 SQL 注入预防、访问控制、代码标准和反模式检测。与 SQL 优化提示相辅相成，实现完整的开发覆盖。 |
| `/database-data-management:postgresql-优化` | 专注于 PostgreSQL 特有功能、高级数据类型和 PostgreSQL 独家能力的 PostgreSQL 开发助手。涵盖 JSONB 操作、数组类型、自定义类型、范围/几何类型、全文搜索、窗口函数以及 PostgreSQL 扩展生态系统。 |
| `/database-data-management:postgresql-代码审查` | 专注于 PostgreSQL 最佳实践、反模式和独特质量标准的 PostgreSQL 代码审查助手。涵盖 JSONB 操作、数组使用、自定义类型、模式设计、函数优化以及 PostgreSQL 独家的安全功能，如行级安全（RLS）。 |

### 代理

| 代理 | 描述 |
|------|------|
| `postgresql-dba` | 使用 PostgreSQL 扩展与 PostgreSQL 数据库协作。 |
| `ms-sql-dba` | 使用 MS SQL 扩展与 Microsoft SQL Server 数据库协作。 |

## 来源

此插件是 [Awesome Copilot](https://github.com/github/awesome-copilot) 的一部分，这是一个由社区驱动的 GitHub Copilot 扩展集合。

## 许可证

MIT

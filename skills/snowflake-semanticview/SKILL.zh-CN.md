---
name: snowflake-语义视图
description: 使用 Snowflake CLI（snow）创建、修改和验证 Snowflake 语义视图。当需要构建或排查语义视图/语义层定义（使用 CREATE/ALTER SEMANTIC VIEW），通过 CLI 验证语义视图 DDL 与 Snowflake 的兼容性，或指导 Snowflake CLI 安装和连接配置时使用。
---

# Snowflake 语义视图

## 一次性设置

- 通过打开新终端并运行 `snow --help` 来验证 Snowflake CLI 的安装。
- 如果 Snowflake CLI 缺失或用户无法安装，请引导其访问 https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation。
- 按照 https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections#add-a-connection 中的说明，使用 `snow connection add` 配置 Snowflake 连接。
- 所有验证和执行步骤均使用已配置的连接。

## 每个语义视图请求的工作流程

1. 确认目标数据库、模式、角色、仓库以及最终的语义视图名称。
2. 确认模型遵循星型架构（事实表与规范化的维度表）。
3. 使用官方语法草拟语义视图的 DDL：
   - https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view
4. 为每个维度、事实和指标填充同义词和注释：
   - 首先读取 Snowflake 表/视图/列的注释（首选来源）：
     - https://docs.snowflake.com/en/sql-reference/sql/comment
   - 如果缺少注释或同义词，请询问是否可以创建、用户是否希望提供文本，或是否应起草建议供审批。
5. 使用包含 DISTINCT 和 LIMIT（最多 1000 行）的 SELECT 语句，发现事实表与维度表之间的关系，识别列的数据类型，并为列创建更有意义的注释和同义词。
6. 创建临时验证名称（例如，添加 `__tmp_validate` 后缀），同时保持相同的数据库和模式。
7. 在最终确定前，始终通过 Snowflake CLI 将 DDL 发送到 Snowflake 进行验证：
   - 使用 `snow sql` 命令执行语句，并使用已配置的连接。
   - 如果版本间的标志不同，请检查 `snow sql --help` 并使用其中显示的连接选项。
8. 如果验证失败，请迭代修改 DDL 并重新运行验证步骤，直到成功。
9. 使用真实的语义视图名称应用最终的 DDL（创建或修改）。
10. 运行一个示例查询以确认最终的语义视图按预期工作。其查询语法与普通视图不同，详见：https://docs.snowflake.com/en/user-guide/views-semantic/querying#querying-a-semantic-view
示例：

```SQL
SELECT * FROM SEMANTIC_VIEW(
    my_semview_name
    DIMENSIONS customer.customer_market_segment
    METRICS orders.order_average_value
)
ORDER BY customer_market_segment;
```

11. 清理验证过程中创建的任何临时语义视图。

## 同义词与注释（必需）

- 使用语义视图语法定义同义词和注释：

```
WITH SYNONYMS [ = ] ( 'synonym' [ , ... ] )
COMMENT = 'comment_about_dim_fact_or_metric'
```

- 将同义词视为仅用于信息说明，不要在其他地方使用它们来引用维度、事实或指标。
- 优先使用 Snowflake 注释作为同义词和注释的来源：
  - https://docs.snowflake.com/en/sql-reference/sql/comment
- 如果 Snowflake 注释缺失，请询问是否可以创建、用户是否希望提供文本，或是否应起草建议供审批。
- 不要在未获得用户批准的情况下自行创建同义词或注释。

## 验证模式（必需）

- 绝对不要跳过验证。在将其作为最终版本呈现前，始终通过 Snowflake CLI 将 DDL 执行到 Snowflake。
- 优先为验证使用临时名称，以避免覆盖真实视图。

## 示例 CLI 验证（模板）

```bash
# 用真实值替换占位符。
snow sql -q "<CREATE OR ALTER SEMANTIC VIEW ...>" --connection <connection_name>
```

如果您的版本中 CLI 使用不同的连接标志，请运行：

```bash
snow sql --help
```

## 注意事项

- 将安装和连接配置视为一次性步骤，但在首次验证前需确认已完成。
- 保持最终的语义视图定义与已验证的临时定义完全一致，仅名称不同。
- 不要省略同义词或注释；即使在语法上是可选的，也应视为完整性必需的部分。

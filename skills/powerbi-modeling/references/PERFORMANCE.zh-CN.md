# Power BI模型性能优化

## 数据缩减技术

### 1. 移除不必要的列
- 仅导入报告所需的列
- 除非必要，否则移除审计列（CreatedBy, ModifiedDate）
- 移除重复/冗余列

```
column_operations(operation: "List", filter: { tableNames: ["Sales"] })
// 审查并移除不需要的列
```

### 2. 移除不必要的行
- 过滤历史数据至相关时间段
- 如果不需要，排除已取消/作废的交易
- 在Power Query中应用过滤器（而非DAX）

### 3. 减少基数
高基数（许多唯一值）影响：
- 模型大小
- 刷新时间
- 查询性能

**解决方案：**
| 列类型 | 减少技术 |
|-------------|---------------------|
| 日期时间 | 分拆为日期和时间列 |
| 十进制精度 | 四舍五入至所需精度 |
| 带模式的文本 | 提取通用前缀/后缀 |
| 高精度ID | 使用代理整数键 |

### 4. 优化数据类型
| 来源 | 目标 | 优势 |
|------|-----|---------|
| 日期时间 | 日期（如果不需要时间） | 8字节到4字节 |
| 十进制 | 固定十进制 | 更好的压缩 |
| 带数字的文本 | 整数 | 更优的压缩 |
| 长文本 | 更短文本 | 减少存储空间 |

### 5. 分组和汇总
当不需要明细数据时预聚合数据：
- 每日而非交易数据
- 每月而非每日
- 考虑使用聚合表进行DirectQuery

## 列优化

### 优先使用Power Query列而非计算列
| 方法 | 使用场景 |
|----------|-------------|
| Power Query (M) | 可在数据源中计算，静态值 |
| 计算列 (DAX) | 需要模型关系，动态逻辑 |

Power Query列：
- 加载速度更快
- 压缩效果更好
- 占用内存更少

### 避免在关系键上使用计算列
DAX计算列在关系中：
- 无法使用索引
- 为DirectQuery生成复杂SQL
- 显著影响性能

**使用COMBINEVALUES处理多列关系：**
```dax
// 如果必须使用计算列创建复合键
CompositeKey = COMBINEVALUES(",", [Country], [City])
```

### 设置适当的汇总方式
防止意外对非加法列进行汇总：
```
column_operations(
  operation: "Update",
  definitions: [{
    tableName: "Product",
    name: "UnitPrice",
    summarizeBy: "None"
  }]
)
```

## 关系优化

### 1. 最小化双向关系
每个双向关系：
- 增加查询复杂度
- 可能产生歧义路径
- 降低性能

### 2. 尽量避免多对多关系
多对多关系：
- 生成更复杂的查询
- 需要更多内存
- 可能产生意外结果

### 3. 降低关系列的基数
保持关系列低基数：
- 使用整数键而非文本
- 考虑使用更高粒度的关系

## DAX优化

### 1. 使用变量
```dax
// 好 - 计算一次，使用两次
Sales Growth = 
VAR CurrentSales = [Total Sales]
VAR PriorSales = [PY Sales]
RETURN DIVIDE(CurrentSales - PriorSales, PriorSales)

// 差 - 重复计算 [Total Sales] 和 [PY Sales]
Sales Growth = 
DIVIDE([Total Sales] - [PY Sales], [PY Sales])
```

### 2. 避免对整个表使用FILTER
```dax
// 差 - 遍历整个表
Sales High Value = 
CALCULATE([Total Sales], FILTER(Sales, Sales[Amount] > 1000))

// 好 - 使用列引用
Sales High Value = 
CALCULATE([Total Sales], Sales[Amount] > 1000)
```

### 3. 适当使用KEEPFILTERS
```dax
// 尊重现有筛选条件
Sales with Filter = 
CALCULATE([Total Sales], KEEPFILTERS(Product[Category] = "Bikes"))
```

### 4. 优先使用DIVIDE而非除法运算符
```dax
// 好 - 处理除以零的情况
Margin % = DIVIDE([Profit], [Sales])

// 差 - 在零值时出错
Margin % = [Profit] / [Sales]
```

## DirectQuery优化

### 1. 减少列和表的数量
DirectQuery模型：
- 每个可视化都会查询数据源
- 性能依赖数据源
- 最小化检索的数据量

### 2. 避免复杂的Power Query转换
- 转换会变成子查询
- 原生查询速度更快
- 尽可能在数据源中进行物化

### 3. 初期保持度量值简单
复杂的DAX会生成复杂的SQL：
- 从基础聚合开始
- 逐步增加复杂度
- 监控查询性能

### 4. 禁用自动日期/时间
对于DirectQuery模型，禁用自动日期/时间：
- 会创建隐藏的计算表
- 增加模型复杂度
- 使用显式日期表代替

## 聚合

### 用户自定义聚合
为以下情况预聚合事实表：
- 非常大的模型（数十亿行）
- 混合DirectQuery/导入模型
- 常见查询模式

```
table_operations(
  operation: "Create",
  definitions: [{
    name: "SalesAgg",
    mode: "Import",
    mExpression: "..."
  }]
)
```

## 性能测试

### 使用性能分析器
1. 在Power BI桌面启用性能分析器
2. 开始录制
3. 与可视化交互
4. 查看DAX查询时间

### 使用DAX Studio监控
外部工具用于：
- 查询时间
- 服务器时间
- 查询计划

## 验证检查清单

- [ ] 已移除不必要的列
- [ ] 使用了适当的数据类型
- [ ] 处理了高基数列
- [ ] 最小化了双向关系
- [ ] DAX使用变量处理重复表达式
- [ ] 没有对整个表使用FILTER
- [ ] 使用DIVIDE而非除法运算符
- [ ] 已禁用DirectQuery的自动日期/时间
- [ ] 使用代表性数据进行了性能测试

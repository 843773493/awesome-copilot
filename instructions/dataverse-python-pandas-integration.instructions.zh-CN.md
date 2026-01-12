

# Dataverse Python SDK - Pandas 集成指南

## 概述
本指南介绍如何将 Dataverse Python SDK 与 pandas DataFrames 集成，用于数据科学和分析工作流。SDK 的 JSON 响应格式可以无缝映射为 pandas DataFrames，使数据科学家能够使用熟悉的工具处理 Dataverse 数据。

---

## 1. PandasODataClient 介绍

### 什么是 PandasODataClient？
`PandasODataClient` 是标准 `DataverseClient` 的一个轻量封装，它返回数据为 pandas DataFrame 格式，而不是原始 JSON 字典。这使其非常适合以下场景：
- 处理表格数据的数据科学家
- 分析和报告工作流
- 数据探索和清洗
- 与机器学习流水线集成

### 安装要求
```bash
# 安装核心依赖项
pip install PowerPlatform-Dataverse-Client
pip install azure-identity

# 安装 pandas 用于数据操作
pip install pandas
```

### 何时使用 PandasODataClient
✅ **需要时使用：**
- 数据探索和分析
- 处理表格数据
- 与统计/机器学习库集成
- 高效的数据操作

❌ **需要时使用 DataverseClient：**
- 仅需实时 CRUD 操作
- 文件上传操作
- 元数据操作
- 单条记录操作

---

## 2. 基础 DataFrame 工作流

### 将查询结果转换为 DataFrame
```python
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient
import pandas as pd

# 设置认证
base_url = "https://<myorg>.crm.dynamics.com"
credential = InteractiveBrowserCredential()
client = DataverseClient(base_url=base_url, credential=credential)

# 查询数据
pages = client.get(
    "account",
    select=["accountid", "name", "creditlimit", "telephone1"],
    filter="statecode eq 0",
    orderby=["name"]
)

# 将所有页面合并为一个 DataFrame
all_records = []
for page in pages:
    all_records.extend(page)

# 转换为 DataFrame
df = pd.DataFrame(all_records)

# 显示前几行
print(df.head())
print(f"总记录数: {len(df)}")
```

### 查询参数映射为 DataFrame 列
```python
# 所有查询参数作为 DataFrame 列返回
df = pd.DataFrame(
    client.get(
        "account",
        select=["accountid", "name", "creditlimit", "telephone1", "createdon"],
        filter="creditlimit > 50000",
        orderby=["creditlimit desc"]
    )
)

# 结果是一个包含以下列的 DataFrame：
# accountid | name | creditlimit | telephone1 | createdon
```

---

## 3. 使用 Pandas 进行数据探索

### 基础探索
```python
import pandas as pd
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient

client = DataverseClient("https://<myorg>.crm.dynamics.com", InteractiveBrowserCredential())

# 加载账户数据
records = []
for page in client.get("account", select=["accountid", "name", "creditlimit", "industrycode"]):
    records.extend(page)

df = pd.DataFrame(records)

# 探索数据
print(df.shape)           # (1000, 4)
print(df.dtypes)          # 数据类型
print(df.describe())      # 统计摘要
print(df.info())          # 列信息和空值计数
print(df.head(10))        # 前10行
```

### 过滤和选择
```python
# 根据条件过滤行
high_value = df[df['creditlimit'] > 100000]

# 选择特定列
names_limits = df[['name', 'creditlimit']]

# 多个条件
filtered = df[(df['creditlimit'] > 50000) & (df['industrycode'] == 1)]

# 值计数
print(df['industrycode'].value_counts())
```

### 排序和分组
```python
# 按列排序
sorted_df = df.sort_values('creditlimit', ascending=False)

# 按行业分组并聚合
by_industry = df.groupby('industrycode').agg({
    'creditlimit': ['mean', 'sum', 'count'],
    'name': 'count'
})

# 分组统计信息
print(df.groupby('industrycode')['creditlimit'].describe())
```

### 数据清洗
```python
# 处理缺失值
df_clean = df.dropna()                    # 删除包含 NaN 的行
df_filled = df.fillna(0)                  # 用 0 填充 NaN
df_ffill = df.fillna(method='ffill')      # 前向填充

# 检查重复值
duplicates = df[df.duplicated(['name'])]
df_unique = df.drop_duplicates()

# 数据类型转换
df['creditlimit'] = pd.to_numeric(df['creditlimit'])
df['createdon'] = pd.to_datetime(df['createdon'])
```

---

## 4. 数据分析模式

### 聚合和摘要
```python
# 创建摘要报告
summary = df.groupby('industrycode').agg({
    'accountid': 'count',
    'creditlimit': ['mean', 'min', 'max', 'sum'],
    'name': lambda x: ', '.join(x.head(3))  # 示例名称
}).round(2)

print(summary)
```

### 时间序列分析
```python
# 转换为 datetime
df['createdon'] = pd.to_datetime(df['createdon'])

# 按月重新采样
monthly = df.set_index('createdon').resample('M').size()

# 提取日期组件
df['year'] = df['createdon'].dt.year
df['month'] = df['createdon'].dt.month
df['day_of_week'] = df['createdon'].dt.day_name()
```

### 合并操作
```python
# 加载两个相关表
accounts = pd.DataFrame(client.get("account", select=["accountid", "name"]))
contacts = pd.DataFrame(client.get("contact", select=["contactid", "parentcustomerid", "fullname"]))

# 按关系合并
merged = accounts.merge(
    contacts,
    left_on='accountid',
    right_on='parentcustomerid',
    how='left'
)

print(merged.head())
```

### 统计分析
```python
# 相关矩阵
correlation = df[['creditlimit', 'industrycode']].corr()

# 分布分析
print(df['creditlimit'].describe())
print(df['creditlimit'].skew())
print(df['creditlimit'].kurtosis())

# 百分位数
print(df['creditlimit'].quantile([0.25, 0.5, 0.75]))
```

---

## 5. 透视表和报告

### 创建透视表
```python
# 按行业和状态创建透视表
pivot = pd.pivot_table(
    df,
    values='creditlimit',
    index='industrycode',
    columns='statecode',
    aggfunc=['sum', 'mean', 'count']
)

print(pivot)
```

### 生成报告
```python
# 按行业生成销售报告
industry_report = df.groupby('industrycode').agg({
    'accountid': 'count',
    'creditlimit': 'sum',
    'name': 'first'
}).rename(columns={
    'accountid': '账户数量',
    'creditlimit': '总信用额度',
    'name': '示例账户'
})

# 导出为 CSV
industry_report.to_csv('industry_report.csv')

# 导出为 Excel
industry_report.to_excel('industry_report.xlsx')
```

---

## 6. 数据可视化

### Matplotlib 集成
```python
import matplotlib.pyplot as plt

# 创建可视化图表
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 直方图
df['creditlimit'].hist(bins=30, ax=axes[0, 0])
axes[0, 0].set_title('信用额度分布')

# 柱状图
df['industrycode'].value_counts().plot(kind='bar', ax=axes[0, 1])
axes[0, 1].set_title('按行业划分的账户')

# 箱线图
df.boxplot(column='creditlimit', by='industrycode', ax=axes[1, 0])
axes[1, 0].set_title('按行业划分的信用额度')

# 散点图
df.plot.scatter(x='creditlimit', y='industrycode', ax=axes[1, 1])
axes[1, 1].set_title('信用额度与行业关系')

plt.tight_layout()
plt.show()
```

### Seaborn 集成
```python
import seaborn as sns

# 相关热图
plt.figure(figsize=(8, 6))
sns.heatmap(df[['creditlimit', 'industrycode']].corr(), annot=True)
plt.title('相关矩阵')
plt.show()

# 分布图
sns.distplot(df['creditlimit'], kde=True)
plt.title('信用额度分布')
plt.show()
```

---

## 7. 与机器学习的集成

### 为 ML 准备数据
```python
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# 加载并准备数据
records = []
for page in client.get(
    "account",
    select=["accountid", "creditlimit", "industrycode", "statecode"]
):
    records.extend(page)

df = pd.DataFrame(records)

# 特征工程
df['log_creditlimit'] = np.log1p(df['creditlimit'])
df['industry_cat'] = pd.Categorical(df['industrycode']).codes

# 分割特征和目标变量
X = df[['industrycode', 'log_creditlimit']]
y = df['statecode']

# 训练-测试分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print(f"训练集: {len(X_train)}, 测试集: {len(X_test)}")
```

### 构建分类模型
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 训练模型
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 评估
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 特征重要性
importances = pd.Series(
    model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print(importances)
```

---

## 8. 高级 DataFrame 操作

### 自定义函数
```python
# 对列应用函数
df['name_length'] = df['name'].apply(len)

# 对行应用函数
df['category'] = df.apply(
    lambda row: 'High' if row['creditlimit'] > 100000 else 'Low',
    axis=1
)

# 条件操作
df['adjusted_limit'] = df['creditlimit'].where(
    df['statecode'] == 0,
    df['creditlimit'] * 0.5
)
```

### 字符串操作
```python
# 字符串方法
df['name_upper'] = df['name'].str.upper()
df['name_starts'] = df['name'].str.startswith('A')
df['name_contains'] = df['name'].str.contains('Inc')
df['name_split'] = df['name'].str.split(',').str[0]

# 替换和替换
df['industry'] = df['industrycode'].map({
    1: '零售',
    2: '制造业',
    3: '科技'
})
```

### 数据重塑
```python
# 转置
transposed = df.set_index('name').T

# 堆叠/展开
stacked = df.set_index(['name', 'industrycode'])['creditlimit'].unstack()

# 融化长格式
melted = pd.melt(df, id_vars=['name'], var_name='metric', value_name='value')
```

---

## 9. 性能优化

### 高效数据加载
```python
# 分块加载大型数据集
all_records = []
chunk_size = 1000

for page in client.get(
    "account",
    select=["accountid", "name", "creditlimit"],
    top=10000,        # 限制总记录数
    page_size=chunk_size
):
    all_records.extend(page)
    if len(all_records) % 5000 == 0:
        print(f"已加载 {len(all_records)} 条记录")

df = pd.DataFrame(all_records)
print(f"总计: {len(df)} 条记录")
```

### 内存优化
```python
# 降低内存使用
# 对重复值使用分类类型
df['industrycode'] = df['industrycode'].astype('category')

# 使用合适的数值类型
df['creditlimit'] = pd.to_numeric(df['creditlimit'], downcast='float')

# 删除不再需要的列
df = df.drop(columns=['unused_col1', 'unused_col2'])

# 检查内存使用
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")
```

### 查询优化
```python
# 在服务器端应用过滤器，而不是客户端
# ✅ 好：服务器端过滤
accounts = client.get(
    "account",
    filter="creditlimit > 50000",  # 服务器端过滤
    select=["accountid", "name", "creditlimit"]
)

# ❌ 差：加载全部数据，本地过滤
all_accounts = client.get("account")  # 加载全部数据
filtered = [a for a in all_accounts if a['creditlimit'] > 50000]  # 客户端端
```

---

## 10. 完整示例：销售分析

```python
import pandas as pd
import numpy as np
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient

# 设置
client = DataverseClient(
    "https://<myorg>.crm.dynamics.com",
    InteractiveBrowserCredential()
)

# 加载数据
print("加载账户数据...")
records = []
for page in client.get(
    "account",
    select=["accountid", "name", "creditlimit", "industrycode", "statecode", "createdon"],
    orderby=["createdon"]
):
    records.extend(page)

df = pd.DataFrame(records)
df['createdon'] = pd.to_datetime(df['createdon'])

# 数据清洗
df = df.dropna()

# 特征工程
df['year'] = df['createdon'].dt.year
df['month'] = df['createdon'].dt.month
df['year_month'] = df['createdon'].dt.to_period('M')

# 分析
print("\n=== 账户概览 ===")
print(f"总账户数: {len(df)}")
print(f"总信用额度: ${df['creditlimit'].sum():,.2f}")
print(f"平均信用额度: ${df['creditlimit'].mean():,.2f}")

print("\n=== 按行业 ===")
industry_summary = df.groupby('industrycode').agg({
    'accountid': 'count',
    'creditlimit': ['sum', 'mean']
}).round(2)
print(industry_summary)

print("\n=== 按状态 ===")
status_summary = df.groupby('statecode').agg({
    'accountid': 'count',
    'creditlimit': 'sum'
})
print(status_summary)

# 导出报告
print("\n=== 导出报告 ===")
industry_summary.to_csv('industry_analysis.csv')
print("报告已保存至 industry_analysis.csv")
```

---

## 11. 已知限制

- `PandasODataClient` 目前需要手动从查询结果创建 DataFrame
- 极大的 DataFrame（数百万行）可能会遇到内存限制
- pandas 操作在客户端端执行；对于大型数据集，服务器端聚合更高效
- 文件操作需要标准 `DataverseClient`，而不是 pandas 封装

---

## 12. 相关资源

- [Pandas 文档](https://pandas.pydata.org/docs/)
- [官方示例: quickstart_pandas.py](https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/main/examples/quickstart_pandas.py)
- [Python SDK 说明文件](https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/main/README.md)
- [Microsoft Learn: 数据处理](https://learn.microsoft.com/zh-cn/power-apps/developer/data-platform/sdk-python/work-data)
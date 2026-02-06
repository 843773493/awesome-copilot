# Power BI 中的行级安全性（RLS）

## 概述

行级安全性（RLS）根据用户身份限制数据访问权限。用户只能查看其被授权的数据。

## 设计原则

### 1. 在维度表上应用筛选
将 RLS 应用于维度表，而非事实表：
- 更高效（表较小）
- 筛选条件会通过关系传播
- 更易于维护

```dax
// 在客户维度表上应用 - 筛选条件会传播到销售事实表
[Region] = "West"
```

### 2. 创建最小化角色
避免过多的角色组合：
- 每个角色 = 独立缓存
- 角色是加法性（并集，而非交集）
- 尽可能合并

### 3. 在可能的情况下使用动态 RLS
数据驱动的规则更具扩展性：
- 用户映射存储在表中
- 使用 USERPRINCIPALNAME() 作为身份标识
- 用户更改时无需调整角色

## 静态 RLS 与动态 RLS

### 静态 RLS
每个角色有固定的规则：
```dax
// 角色：西区
[Region] = "West"

// 角色：东区  
[Region] = "East"
```

**优点：** 简单、清晰  
**缺点：** 不具扩展性，需为每个组创建角色

### 动态 RLS
用户身份驱动筛选：
```dax
// 单个角色根据登录用户进行筛选
[ManagerEmail] = USERPRINCIPALNAME()
```

**优点：** 具扩展性，可自我维护  
**缺点：** 需要用户映射数据

## 实现模式

### 模式 1：直接用户映射
在维度表中包含用户邮箱：
```dax
// 在客户表上应用
[CustomerEmail] = USERPRINCIPALNAME()
```

### 模式 2：安全表
使用独立表将用户映射到数据：
```
安全映射表：
| UserEmail | Region |
|-----------|--------|
| joe@co.com | West  |
| sue@co.com | East  |
```

```dax
// 在区域维度表上应用
[Region] IN 
    SELECTCOLUMNS(
        FILTER(SecurityMapping, [UserEmail] = USERPRINCIPALNAME()),
        "Region", [Region]
    )
```

### 模式 3：经理层级
用户可以看到其数据以及下属数据：
```dax
// 使用 PATH 函数进行层级筛选
PATHCONTAINS(Employee[ManagerPath], 
    LOOKUPVALUE(Employee[EmployeeID], Employee[Email], USERPRINCIPALNAME()))
```

### 模式 4：多规则组合
组合多个条件：
```dax
// 用户可以看到其区域或如果他们是全局查看者
[Region] = LOOKUPVALUE(Users[Region], Users[Email], USERPRINCIPALNAME())
|| LOOKUPVALUE(Users[IsGlobal], Users[Email], USERPRINCIPALNAME()) = TRUE()
```

## 通过 MCP 创建角色

### 列出现有角色
```
security_role_operations(operation: "List")
```

### 创建带权限的角色
```
security_role_operations(
  operation: "Create",
  definitions: [{
    name: "区域销售",
    modelPermission: "Read",
    description: "按区域限制销售数据的访问"
  }]
)
```

### 添加表权限（筛选）
```
security_role_operations(
  operation: "CreatePermissions",
  permissionDefinitions: [{
    roleName: "区域销售",
    tableName: "客户",
    filterExpression: "[Region] = USERPRINCIPALNAME()"
  }]
)
```

### 获取有效权限
```
security_role_operations(
  operation: "GetEffectivePermissions",
  references: [{ name: "区域销售" }]
)
```

## 测试 RLS

### 在 Power BI 桌面版中
1. 模型选项卡 > 以...视图
2. 选择要测试的角色
3. 可选地指定用户身份
4. 验证数据筛选效果

### 测试意外值
对于动态 RLS，测试以下情况：
- 有效用户
- 未知用户（应显示无数据或优雅处理错误）
- NULL/空白值

```dax
// 防御性模式 - 对未知用户返回无数据
IF(
    USERPRINCIPALNAME() IN VALUES(SecurityMapping[UserEmail]),
    [Region] IN SELECTCOLUMNS(...),
    FALSE()
)
```

## 常见错误

### 1. 仅在事实表上应用 RLS
**问题：** 大表扫描，性能差  
**解决方案：** 应用于维度表，通过关系传播筛选

### 2. 使用 LOOKUPVALUE 而非关系
**问题：** 效率低下，不具扩展性  
**解决方案：** 建立正确的关系，让筛选条件自然传播

### 3. 期望交集行为
**问题：** 多个角色 = 并集（加法性），而非交集  
**解决方案：** 在设计角色时考虑并集行为

### 4. 忽略 DirectQuery
**问题：** RLS 筛选条件会变成 WHERE 子句  
**解决方案：** 确保源数据库能够处理查询模式

### 5. 未测试边缘情况
**问题：** 用户看到意外数据  
**解决方案：** 测试以下情况：有效用户、无效用户、多个角色

## 双向 RLS

对于需要双向关系的 RLS：
```
启用“双向安全筛选器”
```

仅在以下情况下使用：
- RLS 需要通过多对多关系进行筛选
- 需要维度到维度的安全性

**注意：** 每个路径仅允许一个双向关系。

## 性能考虑

- RLS 会为每个查询添加 WHERE 子句
- 筛选条件中的复杂 DAX 会影响性能
- 使用真实用户数量进行测试
- 对大型模型考虑聚合操作

## 对象级安全性（OLS）

限制对整个表或列的访问：
```
// 通过 XMLA/TMSL 实现 - 桌面版 UI 不支持
```

适用于：
- 隐藏敏感列（如薪资、社会保障号）
- 限制整个表的访问
- 与 RLS 结合实现全面的安全性

## 验证检查清单

- [ ] RLS 应用于维度表（而非事实表）
- [ ] 筛选条件通过关系正确传播
- [ ] 动态 RLS 使用 USERPRINCIPALNAME()
- [ ] 已测试有效用户和无效用户
- [ ] 处理了边缘情况（NULL、未知用户）
- [ ] 在负载下进行了性能测试
- [ ] 角色映射已记录
- [ ] 理解工作区角色（管理员可绕过 RLS）

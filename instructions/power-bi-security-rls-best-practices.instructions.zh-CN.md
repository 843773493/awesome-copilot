

---
description: 'Power BI 行级安全性（RLS）和高级安全性模式的全面实施指南，涵盖动态安全性、最佳实践和治理策略。'
applyTo: '**/*.{pbix,dax,md,txt,json,csharp,powershell}'
---

# Power BI 安全与行级安全性最佳实践

## 概述
本文档提供了在 Power BI 中实施强大安全性模式的全面指导，重点在于行级安全性（RLS）、动态安全性和基于 Microsoft 官方指导的治理最佳实践。

## 行级安全性基础

### 1. 基础 RLS 实现
```dax
// 基于用户的简单筛选
[EmailAddress] = USERNAME()

// 基于角色的筛选，提升安全性
IF(
    USERNAME() = "Worker",
    [Type] = "Internal",
    IF(
        USERNAME() = "Manager",
        TRUE(),
        FALSE()  // 拒绝非预期用户的访问
    )
)
```

### 2. 使用自定义数据的动态 RLS
```dax
// 使用 CUSTOMDATA() 进行动态筛选
VAR UserRole = CUSTOMDATA()
RETURN
    SWITCH(
        UserRole,
        "SalesPersonA", [SalesTerritory] = "West",
        "SalesPersonB", [SalesTerritory] = "East",
        "Manager", TRUE(),
        FALSE()  // 默认拒绝
    )
```

### 3. 高级安全性模式
```dax
// 基于地区查找的层级安全性
=DimSalesTerritory[SalesTerritoryKey]=LOOKUPVALUE(
    DimUserSecurity[SalesTerritoryID], 
    DimUserSecurity[UserName], USERNAME(), 
    DimUserSecurity[SalesTerritoryID], DimSalesTerritory[SalesTerritoryKey]
)

// 多条件安全性
VAR UserTerritories = 
    FILTER(
        UserSecurity,
        UserSecurity[UserName] = USERNAME()
    )
VAR AllowedTerritories = SELECTCOLUMNS(UserTerritories, "Territory", UserSecurity[Territory])
RETURN
    [Territory] IN AllowedTerritories
```

## 嵌入式分析安全性

### 1. 静态 RLS 实现
```csharp
// 静态 RLS，使用固定角色
var rlsidentity = new EffectiveIdentity(
    username: "username@contoso.com", 
    roles: new List<string>{ "MyRole" },
    datasets: new List<string>{ datasetId.ToString()}
);
```

### 2. 使用自定义数据的动态 RLS
```csharp
// 使用自定义数据的动态 RLS
var rlsidentity = new EffectiveIdentity(
    username: "username@contoso.com",
    roles: new List<string>{ "MyRoleWithCustomData" },
    customData: "SalesPersonA",
    datasets: new List<string>{ datasetId.ToString()}
);
```

### 3. 多数据集安全性
```json
{
    "accessLevel": "View",
    "identities": [
        {
            "username": "France",
            "roles": [ "CountryDynamic"],
            "datasets": [ "fe0a1aeb-f6a4-4b27-a2d3-b5df3bb28bdc" ]
        }
    ]
}
```

## 数据库级安全性集成

### 1. SQL Server RLS 集成
```sql
-- 创建安全性架构和谓词函数
CREATE SCHEMA Security;
GO

CREATE FUNCTION Security.tvf_securitypredicate(@SalesRep AS nvarchar(50))
    RETURNS TABLE
WITH SCHEMABINDING
AS
    RETURN SELECT 1 AS tvf_securitypredicate_result
WHERE @SalesRep = USER_NAME() OR USER_NAME() = 'Manager';
GO

-- 应用安全性策略
CREATE SECURITY POLICY SalesFilter
ADD FILTER PREDICATE Security.tvf_securitypredicate(SalesRep)
ON sales.Orders
WITH (STATE = ON);
GO
```

### 2. Fabric 仓库安全性
```sql
-- 创建安全性架构
CREATE SCHEMA Security;
GO

-- 创建用于 SalesRep 评估的函数
CREATE FUNCTION Security.tvf_securitypredicate(@UserName AS varchar(50))
    RETURNS TABLE
WITH SCHEMABINDING
AS
    RETURN SELECT 1 AS tvf_securitypredicate_result
WHERE @UserName = USER_NAME()
OR USER_NAME() = 'BatchProcess@contoso.com';
GO

-- 使用该函数创建安全性策略
CREATE SECURITY POLICY YourSecurityPolicy
ADD FILTER PREDICATE Security.tvf_securitypredicate(UserName_column)
ON sampleschema.sampletable
WITH (STATE = ON);
GO
```

## 高级安全性模式

### 1. 分页报表安全性
```json
{
    "format": "PDF",
    "paginatedReportConfiguration":{
        "identities": [
            {"username": "john@contoso.com"}
        ]
    }
}
```

### 2. Power Pages 集成
```html
{% powerbi authentication_type:"powerbiembedded" path:"https://app.powerbi.com/groups/00000000-0000-0000-0000-000000000000/reports/00000000-0000-0000-0000-000000000001/ReportSection" roles:"pagesuser" %}
```

### 3. 多租户安全性
```json
{
  "datasets": [
    {
      "id": "fff1a505-xxxx-xxxx-xxxx-e69f81e5b974",
    }
  ],
  "reports": [
    {
      "allowEdit": false,
      "id": "10ce71df-xxxx-xxxx-xxxx-814a916b700d"
    }
  ],
  "identities": [
    {
      "username": "YourUsername",
      "datasets": [
        "fff1a505-xxxx-xxxx-xxxx-e69f81e5b974"
      ],
      "roles": [
        "YourRole"
      ]
    }
  ],
  "datasourceIdentities": [
    {
      "identityBlob": "eyJ…",
      "datasources": [
        {
          "datasourceType": "Sql",
          "connectionDetails": {
            "server": "YourServerName.database.windows.net",
            "database": "YourDataBaseName"
          }
        }
      ]
    }
  ]
}
```

## 安全性设计模式

### 1. 部分 RLS 实现
```dax
// 创建汇总表以实现部分 RLS
SalesRevenueSummary =
SUMMARIZECOLUMNS(
    Sales[OrderDate],
    "RevenueAllRegion", SUM(Sales[Revenue])
)

// 仅在明细层级应用 RLS
Salesperson Filter = [EmailAddress] = USERNAME()
```

### 2. 层级安全性
```dax
// 经理可以看到所有数据，其他人只能看到自己的数据
VAR CurrentUser = USERNAME()
VAR UserRole = LOOKUPVALUE(
    UserRoles[Role], 
    UserRoles[Email], CurrentUser
)
RETURN
    SWITCH(
        UserRole,
        "Manager", TRUE(),
        "Salesperson", [SalespersonEmail] = CurrentUser,
        "Regional Manager", [Region] IN (
            SELECTCOLUMNS(
                FILTER(UserRegions, UserRegions[Email] = CurrentUser),
                "Region", UserRegions[Region]
            )
        ),
        FALSE()
    )
```

### 3. 基于时间的安全性
```dax
// 根据角色限制对最近数据的访问
VAR UserRole = LOOKUPVALUE(UserRoles[Role], UserRoles[Email], USERNAME())
VAR CutoffDate = 
    SWITCH(
        UserRole,
        "Executive", DATE(1900,1,1),  // 所有历史数据
        "Manager", TODAY() - 365,     // 上一年
        "Analyst", TODAY() - 90,      // 最近90天
        TODAY()                       // 仅当天
    )
RETURN
    [Date] >= CutoffDate
```

## 安全性验证与测试

### 1. 角色验证模式
```dax
// 安全性测试度量
Security Test = 
VAR CurrentUsername = USERNAME()
VAR ExpectedRole = "TestRole"
VAR TestResult = 
    IF(
        HASONEVALUE(SecurityRoles[Role]) && 
        VALUES(SecurityRoles[Role]) = ExpectedRole,
        "通过: 角色应用正确",
        "失败: 角色不正确或存在多个角色"
    )
RETURN
    "用户: " & CurrentUsername & " | " & TestResult
```

### 2. 数据暴露审计
```dax
// 审计度量以跟踪数据访问
Data Access Audit = 
VAR AccessibleRows = COUNTROWS(FactTable)
VAR TotalRows = CALCULATE(COUNTROWS(FactTable), ALL(FactTable))
VAR AccessPercentage = DIVIDE(AccessibleRows, TotalRows) * 100
RETURN
    "用户: " & USERNAME() & 
    " | 可访问: " & FORMAT(AccessibleRows, "#,0") & 
    " | 总数: " & FORMAT(TotalRows, "#,0") & 
    " | 访问比例: " & FORMAT(AccessPercentage, "0.00") & "%"
```

## 治理与管理

### 1. 自动化安全性组管理
```powershell
# 将安全性组添加到 Power BI 工作区
# 登录到 Power BI
Login-PowerBI

# 设置安全性组对象 ID
$SGObjectID = "<security-group-object-ID>"

# 获取工作区
$pbiWorkspace = Get-PowerBIWorkspace -Filter "name eq '<workspace-name>'"

# 将安全性组添加到工作区
Add-PowerBIWorkspaceUser -Id $($pbiWorkspace.Id) -AccessRight Member -PrincipalType Group -Identifier $($SGObjectID)
```

### 2. 安全性监控
```powershell
# 监控 Power BI 访问模式
$workspaces = Get-PowerBIWorkspace
foreach ($workspace in $workspaces) {
    $users = Get-PowerBIWorkspaceUser -Id $workspace.Id
    Write-Host "工作区: $($workspace.Name)"
    foreach ($user in $users) {
        Write-Host "  用户: $($user.UserPrincipalName) - 权限: $($user.AccessRight)"
    }
}
```

### 3. 合规性报告
```dax
// 合规性仪表板度量
具有数据访问权限的用户 = 
CALCULATE(
    DISTINCTCOUNT(AuditLog[Username]),
    AuditLog[AccessType] = "DataAccess",
    AuditLog[Date] >= TODAY() - 30
)

高权限用户 = 
CALCULATE(
    DISTINCTCOUNT(UserRoles[Email]),
    UserRoles[Role] IN {"Admin", "Manager", "Executive"}
)

安全性违规 = 
CALCULATE(
    COUNTROWS(AuditLog),
    AuditLog[EventType] = "SecurityViolation",
    AuditLog[Date] >= TODAY() - 7
)
```

## 最佳实践与反模式

### ✅ 安全性最佳实践

#### 1. 最小权限原则
```dax
// 默认情况下始终采用限制性访问
默认安全性 = 
VAR UserPermissions = 
    FILTER(
        UserAccess,
        UserAccess[Email] = USERNAME()
    )
RETURN
    IF(
        COUNTROWS(UserPermissions) > 0,
        [Territory] IN SELECTCOLUMNS(UserPermissions, "Territory", UserAccess[Territory]),
        FALSE()  // 如果未明确授权则拒绝访问
    )
```

#### 2. 明确的角色验证
```dax
// 明确验证预期角色
基于角色的筛选 = 
VAR UserRole = LOOKUPVALUE(UserRoles[Role], UserRoles[Email], USERNAME())
VAR AllowedRoles = {"Analyst", "Manager", "Executive"}
RETURN
    IF(
        UserRole IN AllowedRoles,
        SWITCH(
            UserRole,
            "Analyst", [Department] = LOOKUPVALUE(UserDepartments[Department], UserDepartments[Email], USERNAME()),
            "Manager", [Region] = LOOKUPVALUE(UserRegions[Region], UserRegions[Email], USERNAME()),
            "Executive", TRUE()
        ),
        FALSE()  // 拒绝非预期角色的访问
    )
```

### ❌ 需要避免的安全性反模式

#### 1. 过于宽松的默认权限
```dax
// ❌ 避免：此设置会授予非预期用户完全访问权限
不良安全性筛选 = 
IF(
    USERNAME() = "SpecificUser",
    [Type] = "Internal",
    TRUE()  // 危险的默认设置
)
```

#### 2. 复杂的安全性逻辑
```dax
// ❌ 避免：过于复杂的安全性逻辑难以审计
过于复杂的安全性 = 
IF(
    OR(
        AND(USERNAME() = "User1", WEEKDAY(TODAY()) <= 5),
        AND(USERNAME() = "User2", HOUR(NOW()) >= 9, HOUR(NOW()) <= 17),
        AND(CONTAINS(VALUES(SpecialUsers[Email]), SpecialUsers[Email], USERNAME()), [Priority] = "High")
    ),
    [Type] IN {"Internal", "Confidential"},
    [Type] = "Public"
)
```

## 安全性集成模式

### 1. Azure AD 集成
```csharp
// 使用 Azure AD 用户上下文生成令牌
var tokenRequest = new GenerateTokenRequestV2(
    reports: new List<GenerateTokenRequestV2Report>() { new GenerateTokenRequestV2Report(reportId) },
    datasets: datasetIds.Select(datasetId => new GenerateTokenRequestV2Dataset(datasetId.ToString())).ToList(),
    targetWorkspaces: targetWorkspaceId != Guid.Empty ? new List<GenerateTokenRequestV2TargetWorkspace>() { new GenerateTokenRequestV2TargetWorkspace(targetWorkspaceId) } : null,
    identities: new List<EffectiveIdentity> { rlsIdentity }
);

var embedToken = pbiClient.EmbedToken.GenerateToken(tokenRequest);
```

### 2. 服务主体认证
```csharp
// 用于嵌入场景的服务主体认证
public EmbedToken GetEmbedToken(Guid reportId, IList<Guid> datasetIds, [Optional] Guid targetWorkspaceId)
{
    PowerBIClient pbiClient = this.GetPowerBIClient();

    var rlsidentity = new EffectiveIdentity(
       username: "username@contoso.com",
       roles: new List<string>{ "MyRole" },
       datasets: new List<string>{ datasetId.ToString()}
    );
    
    var tokenRequest = new GenerateTokenRequestV2(
        reports: new List<GenerateTokenRequestV2Report>() { new GenerateTokenRequestV2Report(reportId) },
        datasets: datasetIds.Select(datasetId => new GenerateTokenRequestV2Dataset(datasetId.ToString())).ToList(),
        targetWorkspaces: targetWorkspaceId != Guid.Empty ? new List<GenerateTokenRequestV2TargetWorkspace>() { new GenerateTokenRequestV2TargetWorkspace(targetWorkspaceId) } : null,
        identities: new List<EffectiveIdentity> { rlsIdentity }
    );

    var embedToken = pbiClient.EmbedToken.GenerateToken(tokenRequest);

    return embedToken;
}
```

## 安全性监控与审计

### 1. 访问模式分析
```dax
// 识别异常访问模式
异常访问模式 = 
VAR UserAccessCount = 
    CALCULATE(
        COUNTROWS(AccessLog),
        AccessLog[Date] >= TODAY() - 7
    )
VAR AvgUserAccess = 
    CALCULATE(
        AVERAGE(AccessLog[AccessCount]),
        ALL(AccessLog[Username]),
        AccessLog[Date] >= TODAY() - 30
    )
RETURN
    IF(
        UserAccessCount > AvgUserAccess * 3,
        "⚠️ 高活动量",
        "正常"
    )
```

### 2. 数据泄露检测
```dax
// 检测潜在数据暴露
潜在数据暴露 = 
VAR UnexpectedAccess = 
    CALCULATE(
        COUNTROWS(AccessLog),
        AccessLog[AccessResult] = "Denied",
        AccessLog[Date] >= TODAY() - 1
    )
RETURN
    IF(
        UnexpectedAccess > 10,
        "🚨 多次访问拒绝 - 需要审查",
        "正常"
    )
```

请记住：安全性是分层的 - 通过适当的认证、授权、数据加密、网络安全和全面审计来实施纵深防御。定期审查和测试安全性实现，以确保其满足当前需求和合规标准。
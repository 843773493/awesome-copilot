

---
description: 'Salesforce 平台上的 Apex 开发指南和最佳实践'
applyTo: '**/*.cls, **/*.trigger'
---

# Apex 开发

## 通用指导

- 始终使用 Salesforce 平台的最新 Apex 特性和最佳实践。
- 为每个类和方法编写清晰且简洁的注释，解释业务逻辑和任何复杂操作。
- 处理边界情况，并使用有意义的错误信息实现适当的异常处理。
- 专注于批处理化（Bulkification）——编写处理记录集合的代码，而不是单个记录。
- 注意平台限制（Governor Limits），并设计可高效扩展的解决方案。
- 使用服务层、领域类和选择器类实现良好的职责分离。
- 在注释中记录外部依赖项、集成点及其用途。

## 命名规范

- **类名**：使用 `PascalCase` 命名类。类名应描述性地反映其用途。
  - 控制器：以 `Controller` 为后缀（例如：`AccountController`）
  - 触发器处理类：以 `TriggerHandler` 为后缀（例如：`AccountTriggerHandler`）
  - 服务类：以 `Service` 为后缀（例如：`AccountService`）
  - 选择器类：以 `Selector` 为后缀（例如：`AccountSelector`）
  - 测试类：以 `Test` 为后缀（例如：`AccountServiceTest`）
  - 批处理类：以 `Batch` 为后缀（例如：`AccountCleanupBatch`）
  - 队列类：以 `Queueable` 为后缀（例如：`EmailNotificationQueueable`）

- **方法名**：使用 `camelCase` 命名方法。使用动词表示操作。
  - 良好示例：`getActiveAccounts()`, `updateContactEmail()`, `deleteExpiredRecords()`
  - 避免缩写：`getAccs()` → `getAccounts()`

- **变量名**：使用 `camelCase` 命名变量。使用描述性名称。
  - 良好示例：`accountList`, `emailAddress`, `totalAmount`
  - 除循环计数器外，避免使用单字母变量名：`a` → `account`

- **常量**：使用 `UPPER_SNAKE_CASE` 命名常量。
  - 良好示例：`MAX_BATCH_SIZE`, `DEFAULT_EMAIL_TEMPLATE`, `ERROR_MESSAGE_PREFIX`

- **触发器**：触发器名称为 `ObjectName` + 触发事件（例如：`AccountTrigger`, `ContactTrigger`）

## 最佳实践

### 批处理化（Bulkification）

- **始终编写批处理化代码**——设计所有代码以处理记录集合，而非单个记录。
- 避免在循环中使用 SOQL 查询和 DML 语句。
- 使用集合（`List<>`, `Set<>`, `Map<>`）高效处理多条记录。

```apex
// 良好示例 - 批处理化
public static void updateAccountRating(List<Account> accounts) {
    for (Account acc : accounts) {
        if (acc.AnnualRevenue > 1000000) {
            acc.Rating = 'Hot';
        }
    }
    update accounts;
}

// 不良示例 - 未批处理化
public static void updateAccountRating(Account account) {
    if (account.AnnualRevenue > 1000000) {
        account.Rating = 'Hot';
        update account; // 在设计用于单条记录的方法中使用 DML
    }
}
```

### 使用 Map 实现 O(1) 查找

- **使用 Map 实现高效查找**——将列表转换为 Map 以实现 O(1) 常数时间查找，而不是 O(n) 列表迭代。
- 使用 `Map<Id, SObject>` 构造函数快速将查询结果转换为 Map。
- 适用于匹配相关记录、查找和避免嵌套循环。

```apex
// 良好示例 - 使用 Map 实现 O(1) 查找
Map<Id, Account> accountMap = new Map<Id, Account>([
    SELECT Id, Name, Industry FROM Account WHERE Id IN :accountIds
]);

for (Contact con : contacts) {
    Account acc = accountMap.get(con.AccountId);
    if (acc != null) {
        con.Industry__c = acc.Industry;
    }
}

// 不良示例 - 嵌套循环导致 O(n²) 复杂度
List<Account> accounts = [SELECT Id, Name, Industry FROM Account WHERE Id IN :accountIds];

for (Contact con : contacts) {
    for (Account acc : accounts) {
        if (con.AccountId == acc.Id) {
            con.Industry__c = acc.Industry;
            break;
        }
    }
}

// 良好示例 - 使用 Map 对记录进行分组
Map<Id, List<Contact>> contactsByAccountId = new Map<Id, List<Contact>>();
for (Contact con : contacts) {
    if (!contactsByAccountId.containsKey(con.AccountId)) {
        contactsByAccountId.put(con.AccountId, new List<Contact>());
    }
    contactsByAccountId.get(con.AccountId).add(con);
}
```

### 平台限制（Governor Limits）

- 注意 Salesforce 平台限制：SOQL 查询（100）、DML 语句（150）、堆大小（6MB）、CPU 时间（10s）。
- **主动监控平台限制**，使用 `System.Limits` 类在达到限制前检查资源消耗。
- 使用高效的 SOQL 查询，结合选择性过滤和适当的索引。
- 对大型数据集使用 **SOQL for 循环** 进行处理。
- 对大型数据量（>50,000 条记录）使用 **Batch Apex**。
- 利用 **平台缓存（Platform Cache）** 减少重复的 SOQL 查询。

```apex
// 良好示例 - 处理大型数据集的 SOQL for 循环
public static void processLargeDataSet() {
    for (List<Account> accounts : [SELECT Id, Name FROM Account]) {
        // 处理每批 200 条记录
        processAccounts(accounts);
    }
}

// 良好示例 - 使用 WHERE 子句减少查询结果
List<Account> accounts = [SELECT Id, Name FROM Account WHERE IsActive__c = true LIMIT 200];
```

### 安全性和数据访问

- **在执行 SOQL 查询或 DML 操作前，始终检查 CRUD/FLS 权限**。
- 在 SOQL 查询中使用 `WITH SECURITY_ENFORCED` 强制字段级安全。
- 使用 `Security.stripInaccessible()` 移除用户无法访问的字段。
- 对强制共享规则的类使用 `WITH SHARING` 关键字。
- 仅在必要时使用 `WITHOUT SHARING`，并记录原因。
- 对实用类使用 `INHERITED SHARING` 以继承调用上下文。

```apex
// 良好示例 - 检查 CRUD 权限并使用 stripInaccessible
public with sharing class AccountService {
    public static List<Account> getAccounts() {
        if (!Schema.sObjectType.Account.isAccessible()) {
            throw new SecurityException('用户没有访问 Account 对象的权限');
        }

        List<Account> accounts = [SELECT Id, Name, Industry FROM Account WITH SECURITY_ENFORCED];

        SObjectAccessDecision decision = Security.stripInaccessible(
            AccessType.READABLE, accounts
        );

        return decision.getRecords();
    }
}

// 良好示例 - WITH SHARING 强制共享规则
public with sharing class AccountController {
    // 该类强制记录级共享
}
```

### 异常处理

- 始终使用 try-catch 块处理 DML 操作和调用外部服务。
- 为特定错误场景创建自定义异常类。
- 适当记录异常以供调试和监控。
- 向用户提供有意义的错误信息。

```apex
// 良好示例 - 正确的异常处理
public class AccountService {
    public class AccountServiceException extends Exception {}

    public static void safeUpdate(List<Account> accounts) {
        try {
            if (!Schema.sObjectType.Account.isUpdateable()) {
                throw new AccountServiceException('用户没有更新账户的权限');
            }
            update accounts;
        } catch (DmlException e) {
            System.debug(LoggingLevel.ERROR, 'DML 错误: ' + e.getMessage());
            throw new AccountServiceException('更新账户失败: ' + e.getMessage());
        }
    }
}
```

### SOQL 最佳实践

- 使用选择性查询和索引字段（`Id`, `Name`, `OwnerId`, 自定义索引字段）。
- 在适当的情况下使用 `LIMIT` 子句限制查询结果。
- 如果只需要一条记录，使用 `LIMIT 1`。
- 避免 `SELECT *`，始终指定所需字段。
- 使用关系查询以减少 SOQL 查询次数。
- 在可能的情况下按索引字段排序。
- **在 SOQL 查询中使用 `String.escapeSingleQuotes()`** 以防止 SOQL 注入攻击。
- **检查查询选择性**——目标是选择性 >10%（过滤器将结果减少到总记录的 <10%）。
- 使用 **Query Plan** 验证查询效率和索引使用情况。
- 使用真实数据量测试查询以确保性能。

```apex
// 良好示例 - 选择性查询和索引字段
List<Account> accounts = [
    SELECT Id, Name, (SELECT Id, LastName FROM Contacts)
    FROM Account
    WHERE OwnerId = :UserInfo.getUserId()
    AND CreatedDate = THIS_MONTH
    LIMIT 100
];

// 良好示例 - LIMIT 1 获取单条记录
Account account = [SELECT Id, Name FROM Account WHERE Name = 'Acme' LIMIT 1];

// 良好示例 - 使用 escapeSingleQuotes() 防止 SOQL 注入
String searchTerm = String.escapeSingleQuotes(userInput);
List<Account> accounts = Database.query('SELECT Id, Name FROM Account WHERE Name LIKE \'%' + searchTerm + '%\'');

// 不良示例 - 直接使用用户输入（安全风险）
List<Account> accounts = Database.query('SELECT Id, Name FROM Account WHERE Name LIKE \'%' + userInput + '%\'');

// 良好示例 - 选择性查询和索引字段（高选择性）
List<Account> accounts = [
    SELECT Id, Name FROM Account
    WHERE OwnerId = :UserInfo.getUserId()
    AND CreatedDate = TODAY
    LIMIT 100
];

// 不良示例 - 非选择性查询（扫描整个表）
List<Account> accounts = [
    SELECT Id, Name FROM Account
    WHERE Description LIKE '%test%'  // 非索引字段
];

// 在开发者控制台中检查查询性能：
// 1. 在开发者控制台中启用 'Use Query Plan'
// 2. 运行 SOQL 查询并查看 'Query Plan' 选项卡
// 3. 检查 'Index' 使用情况与 'TableScan'
// 4. 确保选择性 >10% 以实现最佳性能
```

### 触发器最佳实践

- 为每个对象使用 **一个触发器** 以保持清晰度并避免冲突。
- 在处理类中实现触发器逻辑，而不是直接在触发器中编写。
- 使用触发器框架实现一致的触发器管理。
- 利用触发器上下文变量：`Trigger.new`, `Trigger.old`, `Trigger.newMap`, `Trigger.oldMap`。
- 检查触发器上下文：`Trigger.isBefore`, `Trigger.isAfter`, `Trigger.isInsert` 等。

```apex
// 良好示例 - 使用处理类的触发器
trigger AccountTrigger on Account (before insert, before update, after insert, after update) {
    new AccountTriggerHandler().run();
}

// 处理类
public class AccountTriggerHandler extends TriggerHandler {
    private List<Account> newAccounts;
    private List<Account> oldAccounts;
    private Map<Id, Account> newAccountMap;
    private Map<Id, Account> oldAccountMap;

    public AccountTriggerHandler() {
        this.newAccounts = (List<Account>) Trigger.new;
        this.oldAccounts = (List<Account>) Trigger.old;
        this.newAccountMap = (Map<Id, Account>) Trigger.newMap;
        this.oldAccountMap = (Map<Id, Account>) Trigger.oldMap;
    }

    public override void beforeInsert() {
        AccountService.setDefaultValues(newAccounts);
    }

    public override void afterUpdate() {
        AccountService.handleRatingChange(newAccountMap, oldAccountMap);
    }
}
```

## 测试

- **确保生产代码达到 100% 的代码覆盖率**（最低要求为 75%）。
- 编写**有意义的测试**，验证业务逻辑，而不仅仅是代码覆盖率。
- 使用 `@TestSetup` 方法创建在多个测试方法中共享的测试数据。
- 使用 `Test.startTest()` 和 `Test.stopTest()` 重置平台限制。
- 测试**正向场景**、**负向场景**和**批量场景**（200+ 条记录）。
- 使用 `System.runAs()` 测试不同用户上下文和权限。
- 使用 `Test.setMock()` 模拟外部调用。
- **不要使用 `@SeeAllData=true`**——始终在测试中创建测试数据。
- **使用 `Assert` 类方法**进行断言，而不是已弃用的 `System.assert*()` 方法。
- 在断言中始终添加描述性的失败信息以提高清晰度。

```apex
// 良好示例 - 全面的测试类
@IsTest
private class AccountServiceTest {
    @TestSetup
    static void setupTestData() {
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < 200; i++) {
            accounts.add(new Account(
                Name = '测试账户 ' + i,
                AnnualRevenue = i * 10000
            ));
        }
        insert accounts;
    }

    @IsTest
    static void testUpdateAccountRatings_正向() {
        // 准备
        List<Account> accounts = [SELECT Id FROM Account];
        Set<Id> accountIds = new Map<Id, Account>(accounts).keySet();

        // 执行
        Test.startTest();
        AccountService.updateAccountRatings(accountIds);
        Test.stopTest();

        // 验证
        List<Account> updatedAccounts = [
            SELECT Id, Rating FROM Account WHERE AnnualRevenue > 1000000
        ];
        for (Account acc : updatedAccounts) {
            Assert.areEqual('Hot', acc.Rating, '高收入账户的评级应为 Hot');
        }
    }

    @IsTest
    static void testUpdateAccountRatings_NoAccess() {
        // 创建权限受限的用户
        User testUser = createTestUser();

        List<Account> accounts = [SELECT Id FROM Account LIMIT 1];
        Set<Id> accountIds = new Map<Id, Account>(accounts).keySet();

        Test.startTest();
        System.runAs(testUser) {
            try {
                AccountService.updateAccountRatings(accountIds);
                Assert.fail('预期抛出 SecurityException');
            } catch (SecurityException e) {
                Assert.isTrue(true, '预期抛出 SecurityException');
            }
        }
        Test.stopTest();
    }

    @IsTest
    static void testBulkOperation() {
        List<Account> accounts = [SELECT Id FROM Account];
        Set<Id> accountIds = new Map<Id, Account>(accounts).keySet();

        Test.startTest();
        AccountService.updateAccountRatings(accountIds);
        Test.stopTest();

        List<Account> updatedAccounts = [SELECT Id, Rating FROM Account];
        Assert.areEqual(200, updatedAccounts.size(), '所有账户都应被处理');
    }

    private static User createTestUser() {
        Profile p = [SELECT Id FROM Profile WHERE Name = '标准用户' LIMIT 1];
        return new User(
            Alias = 'testuser',
            Email = 'testuser@test.com',
            EmailEncodingKey = 'UTF-8',
            LastName = '测试',
            LanguageLocaleKey = 'en_US',
            LocaleSidKey = 'en_US',
            ProfileId = p.Id,
            TimeZoneSidKey = 'America/Los_Angeles',
            UserName = 'testuser' + DateTime.now().getTime() + '@test.com'
        );
    }
}
```

## 常见代码异味和反模式

- **在循环中使用 DML/SOQL**——始终批处理化代码以避免平台限制异常。
- **硬编码 ID**——使用自定义设置、自定义元数据或动态查询代替。
- **深度嵌套条件**——将逻辑提取到单独的方法中以提高清晰度。
- **大型方法**——保持方法专注于单一职责（最大 30-50 行）。
- **魔术数字**——使用命名常量以提高清晰度和可维护性。
- **重复代码**——将通用逻辑提取到可重用的方法或类中。
- **缺少空值检查**——始终验证输入参数和查询结果。

```apex
// 不良示例 - 在循环中使用 DML
for (Account acc : accounts) {
    acc.Rating = 'Hot';
    update acc; // 避免：在循环中使用 DML
}

// 良好示例 - 批处理化 DML
for (Account acc : accounts) {
    acc.Rating = 'Hot';
}
update accounts;

// 不良示例 - 硬编码 ID
Account acc = [SELECT Id FROM Account WHERE Id = '001000000000001'];

// 良好示例 - 动态查询
Account acc = [SELECT Id FROM Account WHERE Name = :accountName LIMIT 1];

// 不良示例 - 魔术数字
if (accounts.size() > 200) {
    // 处理
}

// 良好示例 - 命名常量
private static final Integer MAX_BATCH_SIZE = 200;
if (accounts.size() > MAX_BATCH_SIZE) {
    // 处理
}
```

## 文档和注释

- 使用 JavaDoc 风格的注释为类和方法编写文档。
- 包含 `@author` 和 `@date` 标签以进行跟踪。
- 包含 `@description`, `@param`, `@return` 和 `@throws` 标签。
- 仅在适用时包含 `@param`, `@return` 和 `@throws` 标签。
- 不要为不返回任何值的方法使用 `@return void`。
- 文档化复杂的业务逻辑和设计决策。
- 保持注释与代码更改同步。

```apex
/**
 * @author 您的姓名
 * @date 2025-01-01
 * @description 管理账户记录的服务类
 */
public with sharing class AccountService {

    /**
     * @author 您的姓名
     * @date 2025-01-01
     * @description 根据年度收入更新账户评级
     * @param accountIds 需要更新的账户 ID 集合
     * @throws AccountServiceException 如果用户没有更新权限
     */
    public static void updateAccountRatings(Set<Id> accountIds) {
        // 实现
    }
}
```

## 部署和 DevOps

- 使用 **Salesforce CLI** 进行基于源代码的开发。
- 利用 **沙盒组织（Scratch Orgs）** 进行开发和测试。
- 使用工具如 Salesforce CLI、GitHub Actions 或 Jenkins 实现 **CI/CD 流水线**。
- 使用 **未锁定包（Unlocked Packages）** 进行模块化部署。
- 将 **Apex 测试** 作为部署验证的一部分。
- 使用 **Salesforce 代码分析器（Code Analyzer）** 检查代码质量问题：`sf code-analyzer run --severity-threshold 2`
- 在部署前审查并解决所有违规项。

```bash
# Salesforce CLI 命令（sf）
sf 项目部署开始                    # 将源代码部署到组织
sf 项目部署开始 --dry-run          # 验证部署而不实际部署
sf apex 运行测试 --test-level RunLocalTests # 运行本地 Apex 测试
sf apex 获取测试 --test-run-id <id>        # 获取测试结果
sf 项目检索开始                  # 从组织中检索源代码

# Salesforce 代码分析器命令
sf code-analyzer 规则                     # 列出所有可用的规则
sf code-analyzer 规则 --rule-selector eslint:Recommended  # 列出推荐的 ESLint 规则
sf code-analyzer 规则 --workspace ./force-app             # 列出特定工作区的规则
sf code-analyzer 运行                       # 使用推荐规则运行分析
sf code-analyzer 运行 --rule-selector pmd:Recommended       # 运行 PMD 推荐规则
sf code-analyzer 运行 --rule-selector "Security"           # 运行带有 Security 标签的规则
sf code-analyzer 运行 --workspace ./force-app --target "**/*.cls"  # 分析 Apex 类
sf code-analyzer 运行 --severity-threshold 3               # 使用严重性阈值运行分析
sf code-analyzer 运行 --output-file results.html           # 将结果输出为 HTML 文件
sf code-analyzer 运行 --output-file results.csv            # 将结果输出为 CSV 文件
sf code-analyzer 运行 --view detail                        # 显示详细的违规信息
```
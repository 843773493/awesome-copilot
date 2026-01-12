

---
applyTo: '**/*.{cs,ts,java}'
description: 强制执行领域代码的 Object Calisthenics 原则，以确保代码干净、可维护且健壮
---
# Object Calisthenics 规则

> ⚠️ **警告：** 本文件包含原始的 9 条 Object Calisthenics 规则。不得添加额外规则，也不得替换或删除这些规则中的任何一条。
> 如果需要，之后可以添加示例。

## 目标
此规则强制执行 Object Calisthenics 原则，以确保后端代码的干净、可维护和健壮性，**主要针对领域代码**。

## 范围与应用
- **主要关注点**：领域类（聚合、实体、值对象、领域服务）
- **次要关注点**：应用层服务和用例处理器
- **例外情况**：
  - 数据传输对象（DTOs）
  - API 模型/契约
  - 配置类
  - 没有业务逻辑的简单数据容器
  - 需要灵活性的基础设施代码

## 核心原则

1. **每个方法仅使用一层缩进**：
   - 确保方法简单，不超出一层缩进。

   ```csharp
   // 不佳示例 - 该方法有多层缩进
   public void SendNewsletter() {
         foreach (var user in users) {
            if (user.IsActive) {
               // 执行某些操作
               mailer.Send(user.Email);
            }
         }
   }
   // 佳示例 - 提取方法以减少缩进
   public void SendNewsletter() {
       foreach (var user in users) {
           SendEmail(user);
       }
   }
   private void SendEmail(User user) {
       if (user.IsActive) {
           mailer.Send(user.Email);
       }
   }

   // 佳示例 - 在发送邮件前过滤用户
   public void SendNewsletter() {
       var activeUsers = users.Where(user => user.IsActive);

       foreach (var user in activeUsers) {
           mailer.Send(user.Email);
       }
   }
   ```

2. **避免使用 else 关键字**：

   - 避免使用 `else` 关键字以减少复杂度并提高可读性。
   - 使用早期返回处理条件。
   - 使用“快速失败”原则
   - 使用守卫子句（Guard Clauses）在方法开始处验证输入和条件。

   ```csharp
   // 不佳示例 - 使用 else
   public void ProcessOrder(Order order) {
       if (order.IsValid) {
           // 处理订单
       } else {
           // 处理无效订单
       }
   }
   // 佳示例 - 避免使用 else
   public void ProcessOrder(Order order) {
       if (!order.IsValid) return;
       // 处理订单
   }
   ```

   快速失败原则示例：
   ```csharp
   public void ProcessOrder(Order order) {
       if (order == null) throw new ArgumentNullException(nameof(order));
       if (!order.IsValid) throw new InvalidOperationException("无效订单");
       // 处理订单
   }
   ```

3. **封装所有原始类型和字符串**：
   - 避免在代码中直接使用原始类型。
   - 将它们封装在类中以提供有意义的上下文和行为。

   ```csharp
   // 不佳示例 - 直接使用原始类型
   public class User {
       public string Name { get; set; }
       public int Age { get; set; }
   }
   // 佳示例 - 封装原始类型
   public class User {
       private string name;
       private Age age;
       public User(string name, Age age) {
           this.name = name;
           this.age = age;
       }
   }
   public class Age {
       private int value;
       public Age(int value) {
           if (value < 0) throw new ArgumentOutOfRangeException(nameof(value), "年龄不能为负数");
           this.value = value;
       }
   }
   ```

4. **第一类集合**：
   - 使用集合封装数据和行为，而不是暴露原始数据结构。
   第一类集合：一个包含数组属性的类不应包含其他属性。

   ```csharp
   // 不佳示例 - 暴露原始集合
   public class Group {
      public int Id { get; private set; }
      public string Name { get; private set; }
      public List<User> Users { get; private set; }

      public int GetNumberOfUsersIsActive() {
         return Users
            .Where(user => user.IsActive)
            .Count();
      }
   }

   // 佳示例 - 封装集合行为
   public class Group {
      public int Id { get; private set; }
      public string Name { get; private set; }

      public GroupUserCollection userCollection { get; private set; } // 用户列表封装在类中

      public int GetNumberOfUsersIsActive() {
         return userCollection
            .GetActiveUsers()
            .Count();
      }
   }
   ```

5. **每行仅使用一个点**：
   - 避免违反迪米特法则，每行仅使用一个点。

   ```csharp
   // 不佳示例 - 一行中使用多个点
   public void ProcessOrder(Order order) {
       var userEmail = order.User.GetEmail().ToUpper().Trim();
       // 对 userEmail 执行某些操作
   }
   // 佳示例 - 每行仅使用一个点
   public class User {
     public NormalizedEmail GetEmail() {
       return NormalizedEmail.Create(/*...*/);       
     }
   }
   public class Order {
     /*...*/
     public NormalizedEmail ConfirmationEmail() {
       return User.GetEmail();         
     }
   }
   public void ProcessOrder(Order order) {
       var confirmationEmail = order.ConfirmationEmail();
       // 对 confirmationEmail 执行某些操作
   }
   ```

6. **不要使用缩写**：
   - 使用有意义的类名、方法名和变量名。
   - 避免可能导致混淆的缩写。

   ```csharp
   // 不佳示例 - 使用缩写
   public class U {
       public string N { get; set; }
   }
   // 佳示例 - 使用有意义的名称
   public class User {
       public string Name { get; set; }
   }
   ```

7. **保持实体类小巧（类、方法、命名空间或包）**：
   - 限制类和方法的大小以提高代码可读性和可维护性。
   - 每个类应具有单一职责，并尽可能小。

   约束条件：
   - 每个类最多 10 个方法
   - 每个类最多 50 行
   - 每个命名空间或包最多 10 个类

   ```csharp
   // 不佳示例 - 大型类具有多个职责
   public class UserManager {
       public void CreateUser(string name) { /*...*/ }
       public void DeleteUser(int id) { /*...*/ }
       public void SendEmail(string email) { /*...*/ }
   }

   // 佳示例 - 小型类具有单一职责
   public class UserCreator {
       public void CreateUser(string name) { /*...*/ }
   }
   public class UserDeleter {
       public void DeleteUser(int id) { /*...*/ }
   }

   public class UserUpdater {
       public void UpdateUser(int id, string name) { /*...*/ }
   }
   ```

8. **不允许有超过两个实例变量的类**：
   - 通过限制实例变量的数量，鼓励类具有单一职责。
   - 实例变量数量限制为两个以保持简洁。
   - 不将 ILogger 或其他日志记录器视为实例变量。

   ```csharp
   // 不佳示例 - 实例变量过多的类
   public class UserCreateCommandHandler {
      // 不佳：实例变量过多
      private readonly IUserRepository userRepository;
      private readonly IEmailService emailService;
      private readonly ILogger logger;
      private readonly ISmsService smsService;

      public UserCreateCommandHandler(IUserRepository userRepository, IEmailService emailService, ILogger logger, ISmsService smsService) {
         this.userRepository = userRepository;
         this.emailService = emailService;
         this.logger = logger;
         this.smsService = smsService;
      }
   }

   // 佳示例 - 实例变量为两个的类
   public class UserCreateCommandHandler {
      private readonly IUserRepository userRepository;
      private readonly INotificationService notificationService;
      private readonly ILogger logger; // 不计入实例变量

      public UserCreateCommandHandler(IUserRepository userRepository, INotificationService notificationService, ILogger logger) {
         this.userRepository = userRepository;
         this.notificationService = notificationService;
         this.logger = logger;
      }
   }
   ```

9. **领域类中不使用 Getter 和 Setter**：
   - 避免在领域类中暴露属性的 Setter。
   - 使用私有构造函数和静态工厂方法进行对象创建。
   - **注意**：此规则主要适用于领域类，不适用于 DTO（数据传输对象）。

   ```csharp
   // 不佳示例 - 领域类具有公共的 Setter
   public class User {  // 领域类
       public string Name { get; set; } // 领域类中应避免
   }
   
   // 佳示例 - 领域类使用封装
   public class User {  // 领域类
       private string name;
       private User(string name) { this.name = name; }
       public static User Create(string name) => new User(name);
   }
   
   // 可接受示例 - DTO 具有公共的 Setter
   public class UserDto {  // DTO - 例外情况适用
       public string Name { get; set; } // DTO 中可接受
   }
   ```

## 实施指南
- **领域类**：
  - 使用私有构造函数和静态工厂方法创建实例。
  - 避免暴露属性的 Setter。
  - 对领域代码严格应用所有 9 条规则。

- **应用层**：
  - 将这些规则应用于用例处理器和应用服务。
  - 专注于保持单一职责和干净的抽象。

- **DTO 和数据对象**：
  - 对于 DTO，可以放宽规则 3（封装原始类型）、规则 8（两个实例变量）和规则 9（无 Getter/Setter）。
  - 数据传输对象可以接受具有公共 Getter 和 Setter 的属性。

- **测试**：
  - 确保测试验证对象的行为而非状态。
  - 测试类可以放宽规则以提高可读性和可维护性。

- **代码审查**：
  - 在代码审查中强制执行领域和应用层代码的规则。
  - 对基础设施和 DTO 代码采取务实的态度。

## 参考资料
- [Object Calisthenics - Jeff Bay 的原始 9 条规则](https://www.cs.helsinki.fi/u/luontola/tdd-2009/ext/ObjectCalisthenics.pdf)
- [ThoughtWorks - Object Calisthenics](https://www.thoughtworks.com/insights/blog/object-calisthenics)
- [《Clean Code: 一种敏捷软件工艺手册》 - Robert C. Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
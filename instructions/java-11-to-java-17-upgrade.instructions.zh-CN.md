

---
applyTo: ["*"]
description: "自 Java 11 发布以来，采用新 Java 17 特性的全面最佳实践。"
---

# 从 Java 11 升级到 Java 17 的指南

## 项目背景

本指南提供了将 Java 项目从 JDK 11 升级到 JDK 17 的全面 GitHub Copilot 指南，涵盖主要语言特性、API 变化以及基于这些版本之间整合的 47 个 JEP 的迁移模式。

## 语言特性与 API 变化

### JEP 395：记录（Java 16）

**迁移模式**：将数据类转换为记录

```java
// 旧：传统数据类
public class Person {
    private final String name;
    private final int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String name() { return name; }
    public int age() { return age; }

    @Override
    public boolean equals(Object obj) { /* boilerplate */ }
    @Override
    public int hashCode() { /* boilerplate */ }
    @Override
    public String toString() { /* boilerplate */ }
}

// 新：记录（Java 16+）
public record Person(String name, int age) {
    // 紧凑的构造函数用于验证
    public Person {
        if (age < 0) throw new IllegalArgumentException("年龄不能为负数");
    }

    // 可以添加自定义方法
    public boolean isAdult() {
        return age >= 18;
    }
}
```

### JEP 409：密封类（Java 17）

**迁移模式**：使用密封类限制继承

```java
// 新：密封类层次结构
public sealed class Shape
    permits Circle, Rectangle, Triangle {

    public abstract double area();
}

public final class Circle extends Shape {
    private final double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

public final class Rectangle extends Shape {
    private final double width, height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public double area() {
        return width * height;
    }
}

public non-sealed class Triangle extends Shape {
    // 非密封类允许进一步继承
    private final double base, height;

    public Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }

    @Override
    public double area() {
        return 0.5 * base * height;
    }
}
```

### JEP 394：instanceof 模式匹配（Java 16）

**迁移模式**：简化 instanceof 检查

```java
// 旧：传统的 instanceof 检查与类型转换
public String processObject(Object obj) {
    if (obj instanceof String) {
        String str = (String) obj;
        return str.toUpperCase();
    } else if (obj instanceof Integer) {
        Integer num = (Integer) obj;
        return "数字: " + num;
    } else if (obj instanceof List<?>) {
        List<?> list = (List<?>) obj;
        return "包含 " + list.size() + " 个元素的列表";
    }
    return "未知类型";
}

// 新：instanceof 模式匹配（Java 16+）
public String processObject(Object obj) {
    if (obj instanceof String str) {
        return str.toUpperCase();
    } else if (obj instanceof Integer num) {
        return "数字: " + num;
    } else if (obj instanceof List<?> list) {
        return "包含 " + list.size() + " 个元素的列表";
    }
    return "未知类型";
}

// 与密封类结合使用效果更佳
public String describeShape(Shape shape) {
    if (shape instanceof Circle circle) {
        return "半径为 " + circle.radius() + " 的圆形";
    } else if (shape instanceof Rectangle rect) {
        return "长宽为 " + rect.width() + "x" + rect.height() + " 的矩形";
    } else if (shape instanceof Triangle triangle) {
        return "底边为 " + triangle.base() + " 的三角形";
    }
    return "未知形状";
}
```

### JEP 361：Switch 表达式（Java 14）

**迁移模式**：将 switch 语句转换为表达式

```java
// 旧：传统的 switch 语句
public String getDayType(DayOfWeek day) {
    String result;
    switch (day) {
        case MONDAY:
        case TUESDAY:
        case WEDNESDAY:
        case THURSDAY:
        case FRIDAY:
            result = "工作日";
            break;
        case SATURDAY:
        case SUNDAY:
            result = "周末";
            break;
        default:
            throw new IllegalArgumentException("未知的日期: " + day);
    }
    return result;
}

// 新：Switch 表达式（Java 14+）
public String getDayType(DayOfWeek day) {
    return switch (day) {
        case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "工作日";
        case SATURDAY, SUNDAY -> "周末";
    };
}

// 使用 yield 处理复杂逻辑
public int calculateScore(Grade grade) {
    return switch (grade) {
        case A -> 100;
        case B -> 85;
        case C -> 70;
        case D -> {
            System.out.println("请考虑改进");
            yield 55;
        }
        case F -> {
            System.out.println("需要重修");
            yield 0;
        }
    };
}
```

### JEP 406：Switch 模式匹配（Java 17 预览功能）

**迁移模式**：使用增强的 switch 模式（预览功能）

```java
// 需要 --enable-preview 标志
public String formatValue(Object obj) {
    return switch (obj) {
        case String s -> "字符串: " + s;
        case Integer i -> "整数: " + i;
        case null -> "空值";
        case default -> "未知类型: " + obj.getClass().getSimpleName();
    };
}

// 使用带条件的模式
public String categorizeNumber(Object obj) {
    return switch (obj) {
        case Integer i when i < 0 -> "负整数";
        case Integer i when i == 0 -> "零";
        case Integer i when i > 0 -> "正整数";
        case Double d when d.isNaN() -> "非数字";
        case Number n -> "其他数字: " + n;
        case null -> "空值";
        case default -> "非数字";
    };
}
```

### JEP 378：文本块（Java 15）

**迁移模式**：使用文本块处理多行字符串

```java
// 旧：拼接字符串
String html = "<html>\n" +
              "  <body>\n" +
              "    <h1>Hello World</h1>\n" +
              "    <p>Welcome to Java 17!</p>\n" +
              "  </body>\n" +
              "</html>";

String sql = "SELECT p.id, p.name, p.email, " +
             "       a.street, a.city, a.state " +
             "FROM person p " +
             "JOIN address a ON p.address_id = a.id " +
             "WHERE p.active = true " +
             "ORDER BY p.name";

// 新：文本块（Java 15+）
String html = """
              <html>
                <body>
                  <h1>Hello World</h1>
                  <p>Welcome to Java 17!</p>
                </body>
              </html>
              """;

String sql = """
             SELECT p.id, p.name, p.email,
                    a.street, a.city, a.state
             FROM person p
             JOIN address a ON p.address_id = a.id
             WHERE p.active = true
             ORDER BY p.name
             """;

// 使用字符串插值方法
String json = """
              {
                "name": "%s",
                "age": %d,
                "city": "%s"
              }
              """.formatted(name, age, city);
```

### JEP 358：更清晰的 NullPointerException（Java 14）

**迁移指导**：更好的 NPE 调试（Java 17 中默认启用）

```java
// 旧 NPE 消息："Exception in thread 'main' java.lang.NullPointerException"
// 新 NPE 消息会明确显示哪部分为 null：
// "无法调用 'String.length()'，因为 'Person.getName()' 的返回值为 null"

public class PersonProcessor {
    public void processPersons(List<Person> persons) {
        // 此处将显示 getName() 返回 null 的具体对象
        persons.stream()
            .mapToInt(person -> person.getName().length())  // 清晰的 NPE，如果 getName() 返回 null
            .sum();
    }

    // 更好的错误消息有助于复杂表达式
    public void complexExample(Map<String, List<Person>> groups) {
        // NPE 将明确显示链式调用中哪部分为 null
        int totalNameLength = groups.get("admins")
                                  .get(0)
                                  .getName()
                                  .length();
    }
}
```

### JEP 371：隐藏类（Java 15）

**迁移模式**：用于框架和代理生成

```java
// 用于框架创建动态代理
public class DynamicProxyExample {
    public static <T> T createProxy(Class<T> interfaceClass, InvocationHandler handler) {
        // 隐藏类为动态生成的类提供更好的封装
        MethodHandles.Lookup lookup = MethodHandles.lookup();

        // 框架代码通常使用隐藏类实现更好的隔离
        // 这通常由框架处理，而不是应用程序代码
        return interfaceClass.cast(
            Proxy.newProxyInstance(
                interfaceClass.getClassLoader(),
                new Class<?>[]{interfaceClass},
                handler
            )
        );
    }
}
```

### JEP 352：非易失性映射字节缓冲区（Java 14）

**迁移模式**：用于持久内存操作

```java
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.StandardOpenOption;

public class PersistentMemoryExample {
    public void usePersistentMemory() throws IOException {
        Path nvmFile = Path.of("/mnt/pmem/data.bin");

        try (FileChannel channel = FileChannel.open(nvmFile,
                StandardOpenOption.READ,
                StandardOpenOption.WRITE,
                StandardOpenOption.CREATE)) {

            // 映射为持久内存
            MappedByteBuffer buffer = channel.map(
                FileChannel.MapMode.READ_WRITE, 0, 1024,
                ExtendedMapMode.READ_WRITE_SYNC
            );

            // 写入可在崩溃后持久化
            buffer.putLong(0, System.currentTimeMillis());
            buffer.putInt(8, 12345);

            // 强制写入持久存储
            buffer.force();
        }
    }
}
```

## 构建系统配置

### Maven 配置

```xml
<properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <maven.compiler.release>17</maven.compiler.release>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <release>17</release>
                <!-- 如果使用 JEP 406，启用预览功能 -->
                <compilerArgs>
                    <arg>--enable-preview</arg>
                </compilerArgs>
            </configuration>
        </plugin>

        <!-- 用于运行预览功能的测试 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0</version>
            <configuration>
                <argLine>--enable-preview</argLine>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### Gradle 配置

```kotlin
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}

tasks.withType<JavaCompile> {
    options.release.set(17)
    // 如需启用预览功能，请添加以下内容
    options.compilerArgs.addAll(listOf("--enable-preview"))
}

tasks.withType<Test> {
    useJUnitPlatform()
    // 为测试启用预览功能
    jvmArgs("--enable-preview")
}
```

## 废弃与移除功能

### JEP 411：废弃安全管理者（Security Manager）以便移除

**迁移模式**：移除安全管理者依赖

```java
// 旧：使用安全管理者
SecurityManager sm = System.getSecurityManager();
if (sm != null) {
    sm.checkPermission(new RuntimePermission("shutdownHooks"));
}

// 新：替代的安全方法
// 使用应用级安全、容器或进程隔离
// 大多数应用程序不需要安全管理者功能
```

### JEP 398：废弃 Applet API 以便移除

**迁移模式**：从 Applet 迁移到现代网络技术

```java
// 旧：Java Applet（已废弃）
public class MyApplet extends Applet {
    @Override
    public void start() {
        // Applet 代码
    }
}

// 新：现代替代方案
// 1. 转换为独立的 Java 应用程序
public class MyApplication extends JFrame {
    public MyApplication() {
        setTitle("我的应用程序");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        // 应用程序代码
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new MyApplication().setVisible(true);
        });
    }
}

// 2. 使用 Java Web Start 替代方案（jlink）
// 3. 转换为使用现代框架的 Web 应用程序
```

### JEP 372：移除 Nashorn JavaScript 引擎

**迁移模式**：使用替代的 JavaScript 引擎

```java
// 旧：Nashorn（Java 17 中移除）
// ScriptEngine engine = new ScriptEngineManager().getEngineByName("nashorn");

// 新：替代方案
// 1. 使用 GraalVM JavaScript 引擎
ScriptEngine engine = new ScriptEngineManager().getEngineByName("graal.js");

// 2. 使用外部 JavaScript 执行
ProcessBuilder pb = new ProcessBuilder("node", "script.js");
Process process = pb.start();

// 3. 使用基于网络的方法或嵌入式浏览器
```

## JVM 与性能改进

### JEP 377：ZGC - 可扩展的低延迟垃圾收集器（Java 15）

**迁移模式**：启用 ZGC 用于低延迟应用

```bash
# 启用 ZGC
-XX:+UseZGC
-XX:+UnlockExperimentalVMOptions  # Java 17 中不再需要

# 监控 ZGC 性能
-XX:+LogVMOutput
-XX:LogFile=gc.log
```

### JEP 379：Shenandoah - 低暂停时间垃圾收集器（Java 15）

**迁移模式**：启用 Shenandoah 以实现一致的延迟

```bash
# 启用 Shenandoah
-XX:+UseShenandoahGC
-XX:+UnlockExperimentalVMOptions  # Java 17 中不再需要

# Shenandoah 调优
-XX:ShenandoahGCHeuristics=adaptive
```

### JEP 341：默认 CDS 归档（Java 12） & JEP 350：动态 CDS 归档（Java 13）

**迁移模式**：提升启动性能

```bash
# CDS 默认启用，但可以创建自定义归档
# 创建自定义 CDS 归档
java -XX:DumpLoadedClassList=classes.lst -cp myapp.jar com.example.Main
java -Xshare:dump -XX:SharedClassListFile=classes.lst -XX:SharedArchiveFile=myapp.jsa -cp myapp.jar

# 使用自定义 CDS 归档
java -XX:SharedArchiveFile=myapp.jsa -cp myapp.jar com.example.Main
```

## 测试与迁移策略

### 阶段 1：基础（第 1-2 周）

1. **更新构建系统**

   - 修改 Maven/Gradle 配置以支持 Java 17
   - 更新 CI/CD 流水线
   - 验证依赖项兼容性

2. **处理废弃与移除功能**
   - 移除 Nashorn JavaScript 引擎的使用
   - 替换废弃的 Applet API
   - 更新安全管理者使用方式

### 阶段 2：语言特性（第 3-4 周）

1. **实现记录**

   - 将数据类转换为记录
   - 在紧凑构造函数中添加验证
   - 测试序列化兼容性

2. **应用模式匹配**
   - 替换 instanceof 链
   - 实现类型安全的转换模式

### 阶段 3：高级特性（第 5-6 周）

1. **Switch 表达式优化**

   - 将 switch 语句转换为表达式
   - 使用新的箭头语法
   - 实现复杂的 yield 逻辑

2. **文本块**
   - 替换拼接的多行字符串
   - 更新 SQL 和 HTML 生成
   - 使用格式化方法

### 阶段 4：密封类（第 7-8 周）

1. **设计密封类层次结构**

   - 识别继承限制
   - 实现密封类模式
   - 与模式匹配结合使用

2. **测试与验证**
   - 全面的测试覆盖率
   - 性能基准测试
   - 兼容性验证

## 性能考量

### 记录与传统类的对比

- 记录在内存使用上更高效
- 更快的创建和相等性检查
- 自动序列化支持
- 考虑用于数据传输对象

### 模式匹配性能

- 消除冗余的类型检查
- 减少类型转换开销
- 更好的 JVM 优化机会
- 与密封类结合使用以实现穷尽性检查

### Switch 表达式优化

- 更高效的字节码生成
- 更好的常量折叠
- 改进的分支预测
- 用于复杂条件逻辑

## 最佳实践

1. **使用记录处理数据类**

   - 不可变数据容器
   - API 数据传输对象
   - 配置对象

2. **战略性应用模式匹配**

   - 替换 instanceof 链
   - 与密封类结合使用
   - 与 switch 表达式结合使用

3. **使用文本块处理多行内容**

   - SQL 查询
   - JSON 模板
   - HTML 内容
   - 配置文件

4. **设计时使用密封类**

   - 领域建模
   - 状态机
   - 代数数据类型
   - 控制 API 的演进

5. **利用增强的随机数生成器**

   - 并行处理场景
   - 高质量的随机数
   - 统计应用
   - 游戏与模拟

本指南使 GitHub Copilot 在将 Java 11 项目升级到 Java 17 时能够提供上下文相关的建议，重点关注语言增强、API 改进和现代 Java 开发实践。
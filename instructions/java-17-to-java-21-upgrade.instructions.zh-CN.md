

---
applyTo: ['*']
description: "自 Java 17 发布以来，采用 Java 21 新功能的全面最佳实践。"
---

# 从 Java 17 升级到 Java 21 指南

这些说明帮助 GitHub Copilot 协助开发者将 Java 项目从 JDK 17 升级到 JDK 21，重点关注新语言特性、API 变化和最佳实践。

## JDK 18-21 中的主要语言特性

### switch 的模式匹配 (JEP 441 - 21 版本标准功能)

**增强的 switch 表达式和语句**

在使用 switch 构造时：
- 建议在适当情况下将传统 switch 转换为模式匹配
- 使用模式匹配进行类型检查和解构
- 升级示例模式：
```java
// 旧方法（Java 17）
public String processObject(Object obj) {
    if (obj instanceof String) {
        String s = (String) obj;
        return s.toUpperCase();
    } else if (obj instanceof Integer) {
        Integer i = (Integer) obj;
        return i.toString();
    }
    return "unknown";
}

// 新方法（Java 21）
public String processObject(Object obj) {
    return switch (obj) {
        case String s -> s.toUpperCase();
        case Integer i -> i.toString();
        case null -> "null";
        default -> "unknown";
    };
}
```

- 支持带守卫条件的模式：
```java
switch (obj) {
    case String s when s.length() > 10 -> "Long string: " + s;
    case String s -> "Short string: " + s;
    case Integer i when i > 100 -> "Large number: " + i;
    case Integer i -> "Small number: " + i;
    default -> "Other";
}
```

### 记录模式 (JEP 440 - 21 版本标准功能)

**在模式匹配中解构记录**

在使用记录时：
- 建议使用记录模式进行解构
- 与 switch 表达式结合实现强大的数据处理
- 使用示例：
```java
public record Point(int x, int y) {}
public record ColoredPoint(Point point, Color color) {}

// 在 switch 中解构
public String describe(Object obj) {
    return switch (obj) {
        case Point(var x, var y) -> "Point at (" + x + ", " + y + ")";
        case ColoredPoint(Point(var x, var y), var color) -> 
            "Colored point at (" + x + ", " + y + ") in " + color;
        default -> "Unknown shape";
    };
}
```

- 在复杂模式匹配中的使用：
```java
// 嵌套记录模式
switch (shape) {
    case Rectangle(ColoredPoint(Point(var x1, var y1), var c1), 
                   ColoredPoint(Point(var x2, var y2), var c2)) 
        when c1 == c2 -> "Monochrome rectangle";
    case Rectangle r -> "Multi-colored rectangle";
}
```

### 虚拟线程 (JEP 444 - 21 版本标准功能)

**轻量级并发**

在进行并发开发时：
- 建议使用虚拟线程来构建高吞吐量、并发的应用程序
- 使用 `Thread.ofVirtual()` 创建虚拟线程
- 迁移示例模式：
```java
// 旧平台线程方法
ExecutorService executor = Executors.newFixedThreadPool(100);
executor.submit(() -> {
    // 阻塞 I/O 操作
    httpClient.send(request);
});

// 新虚拟线程方法
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> {
        // 阻塞 I/O 操作 - 现在可扩展至百万级别
        httpClient.send(request);
    });
}
```

- 使用结构化并发模式：
```java
// 结构化并发（预览功能）
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser(userId));
    Future<String> order = scope.fork(() -> fetchOrder(orderId));
    
    scope.join();           // 等待所有子任务
    scope.throwIfFailed();  // 传播错误
    
    return processResults(user.resultNow(), order.resultNow());
}
```

### 未命名模式和变量 (JEP 443 - 21 版本预览功能)

**简化模式匹配**

在使用模式匹配时：
- 使用未命名模式 `_` 忽略不需要的值
- 简化 switch 表达式和记录模式
- 使用示例：
```java
// 忽略未使用的变量
switch (ball) {
    case RedBall(_) -> "Red ball";     // 不关心尺寸
    case BlueBall(var size) -> "Blue ball size " + size;
}

// 忽略记录的部分字段
switch (point) {
    case Point(var x, _) -> "X coordinate: " + x; // 忽略 Y
    case ColoredPoint(Point(_, var y), _) -> "Y coordinate: " + y;
}

// 使用未命名变量进行异常处理
try {
    riskyOperation();
} catch (IOException | SQLException _) {
    // 不需要异常详情
    handleError();
}
```

### 作用域值 (JEP 446 - 21 版本预览功能)

**改进的上下文传播**

在处理线程本地数据时：
- 考虑使用作用域值作为 ThreadLocal 的现代替代方案
- 对虚拟线程有更好的性能和更清晰的语义
- 使用示例：
```java
// 定义作用域值
private static final ScopedValue<String> USER_ID = ScopedValue.newInstance();

// 设置和使用作用域值
ScopedValue.where(USER_ID, "user123")
    .run(() -> {
        processRequest(); // 可以在调用链中的任何位置访问 USER_ID.get()
    });

// 在嵌套方法中
public void processRequest() {
    String userId = USER_ID.get(); // "user123"
    // 使用用户上下文进行处理
}
```

## API 增强和新功能

### 默认使用 UTF-8 编码 (JEP 400 - 18 版本标准功能)

在进行文件 I/O 操作时：
- UTF-8 现在是所有平台的默认字符集
- 如果原本意图使用 UTF-8，移除显式的字符集指定
- 示例简化：
```java
// 旧显式 UTF-8 指定
Files.readString(path, StandardCharsets.UTF_8);
Files.writeString(path, content, StandardCharsets.UTF_8);

// 新默认行为（Java 18+）
Files.readString(path);  // 默认使用 UTF-8
Files.writeString(path, content);  // 默认使用 UTF-8
```

### 简单 Web 服务器 (JEP 408 - 18 版本标准功能)

当需要基本的 HTTP 服务器时：
- 使用内置的 `jwebserver` 命令或 `com.sun.net.httpserver` 增强功能
- 适用于测试和开发场景
- 使用示例：
```java
// 命令行
$ jwebserver -p 8080 -d /path/to/files

// 程序化使用
HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
server.createContext("/", new SimpleFileHandler(Path.of("/tmp")));
server.start();
```

### 自定义 DNS 解析 SPI (JEP 418 - 19 版本标准功能)

在使用自定义 DNS 解析时：
- 实现 `InetAddressResolverProvider` 进行自定义地址解析
- 适用于服务发现和测试场景

### 密钥封装机制 API (JEP 452 - 21 版本标准功能)

在使用后量子密码学时：
- 使用 KEM API 实现密钥封装机制
- 使用示例：
```java
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM");
KeyPair kp = kpg.generateKeyPair();

KEM kem = KEM.getInstance("ML-KEM");
KEM.Encapsulator encapsulator = kem.newEncapsulator(kp.getPublic());
KEM.Encapsulated encapsulated = encapsulator.encapsulate();
```

## 弃用和警告

### 最终化方法弃用 (JEP 421 - 在 18 版本中弃用)

在遇到 `finalize()` 方法时：
- 移除 finalize 方法并使用替代方案
- 建议使用 Cleaner API 或 try-with-resources
- 迁移示例：
```java
// 弃用的 finalize 方法
@Override
protected void finalize() throws Throwable {
    cleanup();
}

// 使用 Cleaner 的现代方法
private static final Cleaner CLEANER = Cleaner.create();

public MyResource() {
    cleaner.register(this, new CleanupTask(nativeResource));
}

private static class CleanupTask implements Runnable {
    private final long nativeResource;
    
    CleanupTask(long nativeResource) {
        this.nativeResource = nativeResource;
    }
    
    public void run() {
        cleanup(nativeResource);
    }
}
```

### 动态代理加载 (JEP 451 - 在 21 版本中发出警告)

在使用代理或字节码操作时：
- 如需抑制警告，请添加 `-XX:+EnableDynamicAgentLoading`
- 考虑在启动时加载代理而非动态加载
- 更新工具以使用启动代理加载

## 构建配置更新

### 预览功能

对于使用预览功能的项目：
- 在编译器和运行时添加 `--enable-preview`
- Maven 配置：
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <release>21</release>
        <compilerArgs>
            <arg>--enable-preview</arg>
        </compilerArgs>
    </configuration>
</plugin>

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <argLine>--enable-preview</argLine>
    </configuration>
</plugin>
```

- Gradle 配置：
```kotlin
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

tasks.withType<JavaCompile> {
    options.compilerArgs.add("--enable-preview")
}

tasks.withType<Test> {
    jvmArgs("--enable-preview")
}
```

### 虚拟线程配置

对于使用虚拟线程的应用程序：
- 不需要特殊 JVM 标志（21 版本标准功能）
- 考虑以下系统属性用于调试：
```bash
-Djdk.virtualThreadScheduler.parallelism=N  # 设置承载线程数量
-Djdk.virtualThreadScheduler.maxPoolSize=N  # 设置最大池大小
```

## 运行时和 GC 改进

### 代际 ZGC（JEP 439 - 21 版本可用）

在配置垃圾回收时：
- 尝试使用代际 ZGC 以获得更好的性能
- 启用方式：`-XX:+UseZGC -XX:+ZGenerational`
- 监控分配模式和 GC 行为

## 迁移策略

### 分步升级过程

1. **更新构建工具**：确保 Maven/Gradle 支持 JDK 21
2. **语言特性采用**：
   - 从 instanceof 链迁移到 switch 表达式
   - 在有益的情况下添加记录模式
   - 考虑在 I/O 密集型应用中使用虚拟线程
3. **预览功能**：仅在特定用例需要时启用
4. **测试**：特别是针对并发变化进行全面测试
5. **性能**：使用新 GC 选项进行基准测试

### 代码审查清单

在审查 Java 21 升级代码时：
- [ ] 将适当的 instanceof 链转换为 switch 表达式
- [ ] 使用记录模式进行数据解构
- [ ] 在适当情况下将 ThreadLocal 替换为 ScopedValues
- [ ] 考虑在高并发场景中使用虚拟线程
- [ ] 移除显式的 UTF-8 字符集指定
- [ ] 将 finalize() 方法替换为 Cleaner 或 try-with-resources
- [ ] 使用 SequencedCollection 方法处理 first/last 访问模式
- [ ] 仅在使用预览功能时添加预览标志

### 常见迁移模式

1. **switch 增强**：
   ```java
   // 从 instanceof 链迁移到 switch 表达式
   if (obj instanceof String s) return processString(s);
   else if (obj instanceof Integer i) return processInt(i);
   // 变为：
   return switch (obj) {
       case String s -> processString(s);
       case Integer i -> processInt(i);
       default -> processDefault(obj);
   };
   ```

2. **虚拟线程采用**：
   ```java
   // 从平台线程迁移到虚拟线程
   Executors.newFixedThreadPool(200)
   // 变为：
   Executors.newVirtualThreadPerTaskExecutor()
   ```

3. **记录模式使用**：
   ```java
   // 从手动解构迁移到记录模式
   if (point instanceof Point p) {
       int x = p.x();
       int y = p.y();
   }
   // 变为：
   if (point instanceof Point(var x, var y)) {
       // 直接使用 x 和 y
   }
   ```

## 性能考虑

- 虚拟线程在阻塞 I/O 操作中表现优异，但对 CPU 密集型任务可能无明显优势
- 代际 ZGC 可减少大多数应用的 GC 开销
- switch 中的模式匹配通常比 instanceof 链更高效
- SequencedCollection 方法提供 O(1) 的 first/last 元素访问
- 作用域值在虚拟线程中比 ThreadLocal 更具优势

## 测试建议

- 对虚拟线程应用程序进行高并发测试
- 验证模式匹配覆盖所有预期情况
- 与其它垃圾回收器对比测试代际 ZGC 的性能
- 验证 UTF-8 默认行为在不同平台上的表现
- 在生产使用前彻底测试预览功能

请仅在必要时启用预览功能，并在部署到生产环境前在测试环境中充分验证。
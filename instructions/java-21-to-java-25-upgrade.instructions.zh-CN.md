

---
applyTo: ['*']
description: "自 Java 21 发布以来，采用 Java 25 新功能的全面最佳实践。"
---

# 从 Java 21 升级到 Java 25 的指南

这些说明帮助 GitHub Copilot 协助开发者将 Java 项目从 JDK 21 升级到 JDK 25，重点在于新语言特性、API 变化和最佳实践。

## JDK 22-25 的语言特性和 API 变化

### 模式匹配增强（JEP 455/488 - 23 版本预览）

**原始类型模式、instanceof 和 switch**

在使用模式匹配时：
- 建议在 switch 表达式和 instanceof 检查中使用原始类型模式
- 传统 switch 的升级示例：
```java
// 旧方法（Java 21）
switch (x.getStatus()) {
    case 0 -> "okay";
    case 1 -> "warning"; 
    case 2 -> "error";
    default -> "unknown status: " + x.getStatus();
}

// 新方法（Java 25 预览）
switch (x.getStatus()) {
    case 0 -> "okay";
    case 1 -> "warning";
    case 2 -> "error"; 
    case int i -> "unknown status: " + i;
}
```

- 通过 `--enable-preview` 标志启用预览功能
- 建议使用 guard 模式处理更复杂的条件：
```java
switch (x.getYearlyFlights()) {
    case 0 -> ...;
    case int i when i >= 100 -> issueGoldCard();
    case int i -> ... // 处理 1-99 范围
}
```

### 类文件 API（JEP 466/484 - 23 版本第二次预览，25 版本标准）

**用标准 API 替代 ASM**

在检测到字节码操作或类文件处理时：
- 建议从 ASM 库迁移到标准的类文件 API
- 使用 `java.lang.classfile` 包而不是 `org.objectweb.asm`
- 迁移模式示例：
```java
// 旧 ASM 方法
ClassReader reader = new ClassReader(classBytes);
ClassWriter writer = new ClassWriter(reader, 0);
// ... ASM 操作

// 新类文件 API 方法
ClassModel classModel = ClassFile.of().parse(classBytes);
byte[] newBytes = ClassFile.of().transform(classModel, 
    ClassTransform.transformingMethods(methodTransform));
```

### Markdown 文档注释（JEP 467 - 23 版本标准）

**JavaDoc 现代化**

在处理 JavaDoc 注释时：
- 建议将 HTML 密集型的 JavaDoc 转换为 Markdown 语法
- 使用 `///` 表示 Markdown 文档注释
- 转换示例：
```java
// 旧 HTML JavaDoc
/**
 * 返回 <b>绝对</b> 值的 int 值。
 * <p>
 * 如果参数不是负数，返回参数本身。
 * 如果参数是负数，返回参数的负数。
 * 
 * @param a 需要确定绝对值的参数
 * @return 参数的绝对值
 */

// 新 Markdown JavaDoc  
/// 返回 **绝对** 值的 `int` 值。
///
/// 如果参数不是负数，返回参数本身。
/// 如果参数是负数，返回参数的负数。
/// 
/// @param a 需要确定绝对值的参数
/// @return 参数的绝对值
```

### 派生记录创建（JEP 468 - 23 版本预览）

**记录增强**

在使用记录时：
- 建议使用 `with` 表达式创建派生记录
- 启用派生记录创建的预览功能
- 示例模式：
```java
// 代替手动记录复制
public record Person(String name, int age, String email) {
    public Person withAge(int newAge) {
        return new Person(name, newAge, email);
    }
}

// 使用派生记录创建（预览）
Person updated = person with { age = 30; };
```

### 流收集器（JEP 473/485 - 23 版本第二次预览，25 版本标准）

**增强的流处理**

在处理复杂流操作时：
- 建议使用 `Stream.gather()` 进行自定义中间操作
- 导入 `java.util.stream.Gatherers` 获取内置收集器
- 使用示例：
```java
// 自定义窗口操作
List<List<String>> windows = stream
    .gather(Gatherers.windowSliding(3))
    .toList();

// 带状态的自定义过滤
List<Integer> filtered = numbers.stream()
    .gather(Gatherers.fold(0, (state, element) -> {
        // 自定义状态逻辑
        return state + element > threshold ? element : null;
    }))
    .filter(Objects::nonNull)
    .toList();
```

## 迁移警告和弃用项

### sun.misc.Unsafe 内存访问方法（JEP 471 - 23 版本弃用）

在检测到 `sun.misc.Unsafe` 使用时：
- 警告关于弃用的内存访问方法
- 建议迁移到标准替代方案：
```java
// 弃用：sun.misc.Unsafe 内存访问
Unsafe unsafe = Unsafe.getUnsafe();
unsafe.getInt(object, offset);

// 推荐：VarHandle API
VarHandle vh = MethodHandles.lookup()
    .findVarHandle(MyClass.class, "fieldName", int.class);
int value = (int) vh.get(object);

// 或者对于堆外内存：外部函数与内存 API
MemorySegment segment = MemorySegment.ofArray(new int[10]);
int value = segment.get(ValueLayout.JAVA_INT, offset);
```

### JNI 使用警告（JEP 472 - 24 版本警告）

在检测到 JNI 使用时：
- 警告关于 JNI 使用的未来限制
- 建议为使用 JNI 的应用程序添加 `--enable-native-access` 标志
- 推荐尽可能迁移到外部函数与内存 API
- 为原生访问添加模块信息：
```java
module com.example.app {
    requires jdk.unsupported; // 用于剩余的 JNI 使用
}
```

## 垃圾回收更新

### ZGC 分代模式（JEP 474 - 23 版本默认）

在配置垃圾回收时：
- 默认 ZGC 现在使用分代模式
- 如果明确使用非分代模式的 ZGC，请更新 JVM 标志：
```bash
# 显式非分代模式（将显示弃用警告）
-XX:+UseZGC -XX:-ZGenerational

# 默认分代模式
-XX:+UseZGC
```

### G1 改进（JEP 475 - 24 版本实现）

在使用 G1GC 时：
- 不需要代码更改 - JVM 内部优化
- 可能会看到使用 C2 编译器时的编译性能提升

## 向量 API（JEP 469 - 25 版本第八次孵化）

在进行数值计算时：
- 建议使用向量 API 进行 SIMD 操作（仍在孵化中）
- 添加 `--add-modules jdk.incubator.vector`
- 使用示例：
```java
import jdk.incubator.vector.*;

// 传统标量计算
for (int i = 0; i < a.length; i++) {
    c[i] = a[i] + b[i];
}

// 向量化计算
var species = IntVector.SPECIES_PREFERRED;
for (int i = 0; i < a.length; i += species.length()) {
    var va = IntVector.fromArray(species, a, i);
    var vb = IntVector.fromArray(species, b, i);
    var vc = va.add(vb);
    vc.intoArray(c, i);
}
```

## 编译和构建配置

### 预览功能

对于使用预览功能的项目：
- 将 `--enable-preview` 添加到编译器参数中
- 将 `--enable-preview` 添加到运行时参数中
- Maven 配置：
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <release>25</release>
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
        languageVersion = JavaLanguageVersion.of(25)
    }
}

tasks.withType<JavaCompile> {
    options.compilerArgs.add("--enable-preview")
}

tasks.withType<Test> {
    jvmArgs("--enable-preview")
}
```

## 迁移策略

### 分步升级过程

1. **更新构建工具**：确保 Maven/Gradle 支持 JDK 25
2. **更新依赖项**：检查 JDK 25 兼容性
3. **处理警告**：解决 JEP 471/472 的弃用警告
4. **启用预览功能**：如果使用模式匹配或其他预览功能
5. **彻底测试**：尤其是使用 JNI 或 sun.misc.Unsafe 的应用程序
6. **性能测试**：验证新 ZGC 默认分代模式下的 GC 行为

### 代码审查清单

在审查 Java 25 升级代码时：
- [ ] 将 ASM 使用替换为类文件 API
- [ ] 将复杂的 HTML JavaDoc 转换为 Markdown
- [ ] 在适用时使用原始类型模式于 switch 表达式
- [ ] 将 sun.misc.Unsafe 替换为 VarHandle 或 FFM API
- [ ] 为 JNI 使用添加原生访问权限
- [ ] 为复杂流操作使用流收集器
- [ ] 更新构建配置以启用预览功能

### 测试注意事项

- 使用 `--enable-preview` 标志测试预览功能
- 验证 JNI 应用程序在原生访问警告下的运行情况
- 测试新 ZGC 分代模式下的性能
- 验证使用 Markdown 注释的 JavaDoc 生成

## 常见陷阱

1. **预览功能依赖项**：不要在没有明确文档说明的情况下在库代码中使用预览功能
2. **原生访问**：使用 JNI 直接或间接的应用程序可能需要 `--enable-native-access` 配置
3. **Unsafe 迁移**：不要延迟迁移 sun.misc.Unsafe - 弃用警告表明未来将移除
4. **模式匹配范围**：原始类型模式适用于所有原始类型，而不仅仅是 int
5. **记录增强**：Java 23 中派生记录创建需要预览标志

## 性能注意事项

- ZGC 分代模式可能提升大多数工作负载的性能
- 类文件 API 减少了 ASM 相关的开销
- 流收集器提升了复杂流操作的性能
- G1GC 改进减少了 JIT 编译的开销

在将 Java 25 升级部署到生产系统之前，请务必在测试环境中彻底测试。
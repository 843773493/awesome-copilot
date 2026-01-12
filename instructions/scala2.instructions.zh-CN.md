

---
description: '遵循Databricks风格指南的Scala 2.12/2.13编程语言编码规范和最佳实践，涵盖函数式编程、类型安全和生产代码质量。'
applyTo: '**.scala, **/build.sbt, **/build.sc'
---

# Scala 最佳实践

基于 [Databricks Scala 风格指南](https://github.com/databricks/scala-style-guide)

## 核心原则

### 编写简单代码
代码只写一次，但会被阅读和修改多次。应优先编写易于长期阅读和维护的代码。

### 默认使用不可变性
- 总是优先使用 `val` 而不是 `var`
- 使用 `scala.collection.immutable` 中的不可变集合
- case类的构造参数不应是可变的
- 使用复制构造器来创建修改后的实例

```scala
// 好 - 不可变的case类
case class Person(name: String, age: Int)

// 坏 - 可变的case类
case class Person(name: String, var age: Int)

// 要修改值，使用复制构造器
val p1 = Person("Peter", 15)
val p2 = p1.copy(age = 16)

// 好 - 不可变集合
val users = List(User("Alice", 30), User("Bob", 25))
val updatedUsers = users.map(u => u.copy(age = u.age + 1))
```

### 纯函数
- 函数应是确定性的且无副作用
- 将纯逻辑与副作用分离
- 对有副作用的方法使用显式类型

```scala
// 好 - 纯函数
def calculateTotal(items: List[Item]): BigDecimal =
  items.map(_.price).sum

// 坏 - 有副作用的函数
def calculateTotal(items: List[Item]): BigDecimal = {
  println(s"Calculating total for ${items.size} items")  // 副作用
  val total = items.map(_.price).sum
  saveToDatabase(total)  // 副作用
  total
}
```

## 命名规范

### 类和对象

```scala
// 类、特质、对象 - PascalCase
class ClusterManager
trait Expression
object Configuration

// 包 - 全部小写ASCII
package com.databricks.resourcemanager

// 方法/函数 - camelCase
def getUserById(id: Long): Option[User]
def processData(input: String): Result

// 常量 - 在伴生对象中使用大写
object Configuration {
  val DEFAULT_PORT = 10000
  val MAX_RETRIES = 3
  val TIMEOUT_MS = 5000L
}
```

### 变量和参数

```scala
// 变量 - camelCase，自明的名称
val serverPort = 1000
val clientPort = 2000
val maxRetryAttempts = 3

// 在小范围、局部作用域中，单字符名称是可以接受的
for (i <- 0 until 10) {
  // ...
}

// 不要使用 "l"（Larry）- 看起来像 "1"、"|"、"I"
```

### 枚举

```scala
// 枚举对象 - PascalCase
// 值 - 全大写并使用下划线
private object ParseState extends Enumeration {
  type ParseState = Value

  val PREFIX,
      TRIM_BEFORE_SIGN,
      SIGN,
      VALUE,
      UNIT_BEGIN,
      UNIT_END = Value
}
```

## 语法风格

### 行长度和间距

```scala
// 限制行长度为100个字符
// 运算符前后各留一个空格
def add(int1: Int, int2: Int): Int = int1 + int2

// 逗号后留一个空格
val list = List("a", "b", "c")

// 冒号后留一个空格
def getConf(key: String, defaultValue: String): String = {
  // 代码
}

// 使用2个空格缩进
if (true) {
  println("Wow!")
}

// 对于长参数列表使用4个空格缩进
def newAPIHadoopFile[K, V, F <: NewInputFormat[K, V]](
    path: String,
    fClass: Class[F],
    kClass: Class[K],
    vClass: Class[V],
    conf: Configuration = hadoopConfiguration): RDD[(K, V)] = {
  // 方法体
}

// 长参数的类
class Foo(
    val param1: String,  // 4个空格缩进
    val param2: String,
    val param3: Array[Byte])
  extends FooInterface  // 2个空格缩进
  with Logging {

  def firstMethod(): Unit = { ... }  // 正上方留空行
}
```

### 30行规则
- 方法应少于30行代码
- 类应少于30个方法

### 大括号
```scala
// 对多行块始终使用大括号
if (true) {
  println("Wow!")
}

// 例外：单行三元运算符（无副作用）
val result = if (condition) value1 else value2

// 对 try-catch 始终使用大括号
try {
  foo()
} catch {
  case e: Exception => handle(e)
}
```

### 长字面量
```scala
// 使用大写L表示长整型字面量
val longValue = 5432L  // 正确
val badValue = 5432l   // 不要这样做 - 难以辨认
```

### 括号
```scala
// 有副作用的方法使用括号
class Job {
  def killJob(): Unit = { ... }  // 正确 - 改变状态
  def getStatus: JobStatus = { ... }  // 正确 - 无副作用
}

// 调用处应与声明处一致
new Job().killJob()  // 正确
new Job().getStatus  // 正确
```

### 导入
```scala
// 除非导入6个以上实体，否则避免通配符导入
import scala.collection.mutable.{Map, HashMap, ArrayBuffer}

// 对隐式转换或6个以上项使用通配符是可接受的
import scala.collection.JavaConverters._
import java.util.{Map, HashMap, List, ArrayList, Set, HashSet}

// 始终使用绝对路径
import scala.util.Random  // 正确
// import util.Random     // 不要使用相对路径

// 导入顺序（中间留空行）：
import java.io.File
import javax.servlet.http.HttpServlet

import scala.collection.mutable.HashMap
import scala.util.Random

import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD

import com.databricks.MyClass
```

### 模式匹配
```scala
// 如果方法完全由模式匹配构成，将 match 放在同一线
def test(msg: Message): Unit = msg match {
  case TextMessage(text) => handleText(text)
  case ImageMessage(url) => handleImage(url)
}

// 单个 case 的闭包 - 同一线
list.zipWithIndex.map { case (elem, i) =>
  // 处理
}

// 多个 case - 缩进并换行
list.map {
  case a: Foo => processFoo(a)
  case b: Bar => processBar(b)
  case _ => handleDefault()
}

// 仅按类型匹配 - 不要展开所有参数
case class Pokemon(name: String, weight: Int, hp: Int, attack: Int, defense: Int)

// 坏 - 当字段变化时容易出错
targets.foreach {
  case Pokemon(_, _, hp, _, defense) =>
    // 容易出错
}

// 好 - 按类型匹配
targets.foreach {
  case p: Pokemon =>
    val loss = math.min(0, myAttack - p.defense)
    p.copy(hp = p.hp - loss)
}
```

### 匿名函数
```scala
// 避免过多括号
// 正确
list.map { item =>
  transform(item)
}

// 正确
list.map(item => transform(item))

// 错误 - 不必要的大括号
list.map(item => {
  transform(item)
})

// 错误 - 过多嵌套
list.map({ item => ... })
```

### 中缀方法
```scala
// 避免对非符号方法使用中缀
list.map(func)  // 正确
list map func   // 错误

// 对运算符使用中缀是可接受的
arrayBuffer += elem
```

## 语言特性

### 避免在类上使用 apply()
```scala
// 避免在类上使用 apply() - 难以追踪
class TreeNode {
  def apply(name: String): TreeNode = { ... }  // 不要这样做
}

// 伴生对象中作为工厂方法使用是可接受的
object TreeNode {
  def apply(name: String): TreeNode = new TreeNode(name)  // 可接受
}
```

### override 修饰符
```scala
// 始终使用 override - 即使是抽象方法
trait Parent {
  def hello(data: Map[String, String]): Unit
}

class Child extends Parent {
  // 不使用 override 时，可能并未真正覆盖!
  override def hello(data: Map[String, String]): Unit = {
    println(data)
  }
}
```

### 避免在构造函数中解构
```scala
// 不要在构造函数中使用解构绑定
class MyClass {
  // 坏 - 创建非瞬时的Tuple2
  @transient private val (a, b) = someFuncThatReturnsTuple2()

  // 好
  @transient private val tuple = someFuncThatReturnsTuple2()
  @transient private val a = tuple._1
  @transient private val b = tuple._2
}
```

### 避免 call-by-name
```scala
// 避免使用 call-by-name 参数
// 坏 - 调用者无法判断执行次数
def print(value: => Int): Unit = {
  println(value)
  println(value + 1)
}

// 好 - 显式函数类型
def print(value: () => Int): Unit = {
  println(value())
  println(value() + 1)
}
```

### 避免多个参数列表
```scala
// 除非是隐式转换，否则避免多个参数列表
// 坏
case class Person(name: String, age: Int)(secret: String)

// 好
case class Person(name: String, age: Int, secret: String)

// 例外：为隐式转换分离参数列表（但避免隐式转换！）
def foo(x: Int)(implicit ec: ExecutionContext): Future[Int]
```

### 符号方法
```scala
// 仅用于算术运算符
class Vector {
  def +(other: Vector): Vector = { ... }  // 可接受
  def -(other: Vector): Vector = { ... }  // 可接受
}

// 不用于其他方法
// 坏
channel ! msg
stream1 >>= stream2

// 好
channel.send(msg)
stream1.join(stream2)
```

### 类型推断
```scala
// 始终为公共方法指定类型
def getUserById(id: Long): Option[User] = { ... }

// 始终为隐式方法指定类型
implicit def stringToInt(s: String): Int = s.toInt

// 当不明显时使用类型变量（3秒规则）
val user: User = complexComputation()

// 当明显时可以省略
val count = 5
val name = "Alice"
```

### 返回语句
```scala
// 避免在闭包中使用 return - 内部使用异常
def receive(rpc: WebSocketRPC): Option[Response] = {
  tableFut.onComplete { table =>
    if (table.isFailure) {
      return None  // 不要这样做 - 错误线程!
    }
  }
}

// 使用 return 作为守卫语句简化控制流
def doSomething(obj: Any): Any = {
  if (obj eq null) {
    return null
  }
  // 执行操作
}

// 使用 return 提前退出循环
while (true) {
  if (cond) {
    return
  }
}
```

### 递归和尾递归
```scala
// 除非是自然递归（如树、图），否则避免递归
// 对尾递归方法使用 @tailrec
@scala.annotation.tailrec
def max0(data: Array[Int], pos: Int, max: Int): Int = {
  if (pos == data.length) {
    max
  } else {
    max0(data, pos + 1, if (data(pos) > max) data(pos) else max)
  }
}

// 更清晰地使用显式循环
def max(data: Array[Int]): Int = {
  var max = Int.MinValue
  for (v <- data) {
    if (v > max) {
      max = v
    }
  }
  max
}
```

### 隐式转换
```scala
// 除非：
// 1. 构建DSL
// 2. 隐式类型参数（ClassTag, TypeTag）
// 3. 在类内部进行私有类型转换

// 如果必须使用，不要重载
object ImplicitHolder {
  // 坏 - 无法选择性导入
  def toRdd(seq: Seq[Int]): RDD[Int] = { ... }
  def toRdd(seq: Seq[Long]): RDD[Long] = { ... }
}

// 好 - 不同的名称
object ImplicitHolder {
  def intSeqToRdd(seq: Seq[Int]): RDD[Int] = { ... }
  def longSeqToRdd(seq: Seq[Long]): RDD[Long] = { ... }
}
```

## 类型安全

### 代数数据类型
```scala
// 和类型 - 使用 sealed traits 和 case classes
sealed trait PaymentMethod
case class CreditCard(number: String, cvv: String) extends PaymentMethod
case class PayPal(email: String) extends PaymentMethod
case class BankTransfer(account: String, routing: String) extends PaymentMethod

def processPayment(payment: PaymentMethod): Either[Error, Receipt] = payment match {
  case CreditCard(number, cvv) => chargeCreditCard(number, cvv)
  case PayPal(email) => chargePayPal(email)
  case BankTransfer(account, routing) => chargeBankAccount(account, routing)
}

// 产品类型 - case classes
case class User(id: Long, name: String, email: String, age: Int)
case class Order(id: Long, userId: Long, items: List[Item], total: BigDecimal)
```

### 使用 Option 而不是 null
```scala
// 使用 Option 代替 null
def findUserById(id: Long): Option[User] = {
  database.query(id)
}

// 使用 Option() 来防范 null
def myMethod1(input: String): Option[String] = Option(transform(input))

// 不要使用 Some() - 无法防范 null
def myMethod2(input: String): Option[String] = Some(transform(input)) // 坏

// 对 Option 进行模式匹配
def processUser(id: Long): String = findUserById(id) match {
  case Some(user) => s"Found: ${user.name}"
  case None => "User not found"
}

// 除非绝对确定，不要调用 get()
val user = findUserById(123).get  // 危险！

// 使用 getOrElse、map、flatMap、fold 代替
val name = findUserById(123).map(_.name).getOrElse("Unknown")
```

### 使用 Either 进行错误处理
```scala
sealed trait ValidationError
case class InvalidEmail(email: String) extends ValidationError
case class InvalidAge(age: Int) extends ValidationError
case class MissingField(field: String) extends ValidationError

def validateUser(data: Map[String, String]): Either[ValidationError, User] = {
  for {
    name <- data.get("name").toRight(MissingField("name"))
    email <- data.get("email").toRight(MissingField("email"))
    validEmail <- validateEmail(email)
    ageStr <- data.get("age").toRight(MissingField("age"))
    age <- ageStr.toIntOption.toRight(InvalidAge(-1))
  } yield User(name, validEmail, age)
}
```

### Try 与异常
```scala
// 不要从API返回 Try
// 坏
def getUser(id: Long): Try[User]

// 好 - 显式抛出
@throws(classOf[DatabaseConnectionException])
def getUser(id: Long): Option[User]

// 使用 NonFatal 捕获异常
import scala.util.control.NonFatal

try {
  dangerousOperation()
} catch {
  case NonFatal(e) =>
    logger.error("操作失败", e)
  case e: InterruptedException =>
    // 处理中断
}
```

## 集合

### 优先使用不可变集合
```scala
import scala.collection.immutable._

// 好
val numbers = List(1, 2, 3, 4, 5)
val doubled = numbers.map(_ * 2)
val evens = numbers.filter(_ % 2 == 0)

val userMap = Map(
  1L -> "Alice",
  2L -> "Bob"
)
val updated = userMap + (3L -> "Charlie")

// 对于懒加载序列，使用 Stream（Scala 2.12）或 LazyList（Scala 2.13）
val fibonacci: LazyList[BigInt] =
  BigInt(0) #:: BigInt(1) #:: fibonacci.zip(fibonacci.tail).map { case (a, b) => a + b }

val first10 = fibonacci.take(10).toList
```

### 单子链式调用
```scala
// 避免超过3个操作的链式调用
// 在 flatMap 后中断
// 避免在 if-else 块中链式调用

// 坏 - 太复杂
database.get(name).flatMap { elem =>
  elem.data.get("address").flatMap(Option.apply)
}

// 好 - 更易读
def getAddress(name: String): Option[String] = {
  if (!database.contains(name)) {
    return None
  }

  database(name).data.get("address") match {
    case Some(null) => None
    case Some(addr) => Option(addr)
    case None => None
  }
}

// 不要使用 if-else 链式调用
// 坏
if (condition) {
  Seq(1, 2, 3)
} else {
  Seq(1, 2, 3)
}.map(_ + 1)

// 好
val seq = if (condition) Seq(1, 2, 3) else Seq(4, 5, 6)
seq.map(_ + 1)
```

## 性能优化

### 使用 while 循环
```scala
// 对性能关键代码，使用 while 而不是 for/map
val arr = Array.fill(1000)(Random.nextInt())

// 慢
val newArr = arr.zipWithIndex.map { case (elem, i) =>
  if (i % 2 == 0) 0 else elem
}

// 快
val newArr = new Array[Int](arr.length)
var i = 0
while (i < arr.length) {
  newArr(i) = if (i % 2 == 0) 0 else arr(i)
  i += 1
}
```

### 优先使用 null 而不是 Option
```scala
// 对性能关键代码，优先使用 null 而不是 Option
class Foo {
  @javax.annotation.Nullable
  private[this] var nullableField: Bar = _
}
```

### 使用 private[this]
```scala
// private[this] 生成字段，而非访问器方法
class MyClass {
  private val field1 = ...        // 可能使用访问器
  private[this] val field2 = ...  // 直接字段访问

  def perfSensitiveMethod(): Unit = {
    var i = 0
    while (i < 1000000) {
      field2  // 确保字段访问
      i += 1
    }
  }
}
```

### Java 集合
```scala
// 为了性能，优先使用 Java 集合
import java.util.{ArrayList, HashMap}

val list = new ArrayList[String]()
val map = new HashMap[String, Int]()
```

## 并发

### 优先使用 ConcurrentHashMap
```scala
// 使用 java.util.concurrent.ConcurrentHashMap
private[this] val map = new java.util.concurrent.ConcurrentHashMap[String, String]

// 或使用同步的 map 以降低竞争
private[this] val map = java.util.Collections.synchronizedMap(
  new java.util.HashMap[String, String]
)
```

### 显式同步
```scala
class Manager {
  private[this] var count = 0
  private[this] val map = new java.util.HashMap[String, String]

  def update(key: String, value: String): Unit = synchronized {
    map.put(key, value)
    count += 1
  }

  def getCount: Int = synchronized { count }
}
```

### 原子变量
```scala
import java.util.concurrent.atomic._

// 优先使用 Atomic 而不是 @volatile
val initialized = new AtomicBoolean(false)

// 明确表达仅执行一次的操作
if (!initialized.getAndSet(true)) {
  initialize()
}
```

## 测试

### 拦截特定异常
```scala
import org.scalatest._

// 坏 - 范围太广
intercept[Exception] {
  thingThatThrows()
}

// 好 - 特定类型
intercept[IllegalArgumentException] {
  thingThatThrows()
}
```

## SBT 配置

```scala
// build.sbt
ThisBuild / version := "0.1.0-SNAPSHOT"
ThisBuild / scalaVersion := "2.13.12"
ThisBuild / organization := "com.example"

lazy val root = (project in file("."))
  .settings(
    name := "my-application",

    libraryDependencies ++= Seq(
      "org.typelevel" %% "cats-core" % "2.10.0",
      "org.typelevel" %% "cats-effect" % "3.5.2",

      // 测试依赖
      "org.scalatest" %% "scalatest" % "3.2.17" % Test,
      "org.scalatestplus" %% "scalacheck-1-17" % "3.2.17.0" % Test
    ),

    scalacOptions ++= Seq(
      "-encoding", "UTF-8",
      "-feature",
      "-unchecked",
      "-deprecation",
      "-Xfatal-warnings"
    )
  )
```

## 杂项

### 使用 nanoTime
```scala
// 使用 nanoTime 计算持续时间，而不是 currentTimeMillis
val start = System.nanoTime()
doWork()
val elapsed = System.nanoTime() - start

import java.util.concurrent.TimeUnit
val elapsedMs = TimeUnit.NANOSECONDS.toMillis(elapsed)
```

### URI 而不是 URL
```scala
// 使用 URI 而不是 URL（URL.equals 会执行DNS查找！）
val uri = new java.net.URI("http://example.com")
// 不要使用：val url = new java.net.URL("http://example.com")
```

## 总结

1. **编写简单代码** - 优化可读性和可维护性
2. **使用不可变数据** - val、不可变集合、case类
3. **避免语言特性** - 限制隐式转换，避免符号方法
4. **为公共API指定类型** - 方法和字段的显式类型
5. **显式优于隐式** - 清晰胜于简洁
6. **使用标准库** - 不要重复造轮子
7. **遵循命名规范** - PascalCase、camelCase、UPPER_CASE
8. **保持方法简短** - 30行规则
9. **显式处理错误** - Option、Either、使用 @throws 的异常
10. **在优化前进行性能分析** - 测量，不要猜测

如需完整细节，请参阅 [Databricks Scala 风格指南](https://github.com/databricks/scala-style-guide)。
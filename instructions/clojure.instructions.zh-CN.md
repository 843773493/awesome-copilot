

---
描述：'Clojure 特定的编码模式、内联 def 使用、代码块模板以及 Clojure 开发中的命名空间处理。'
适用于：'**/*.{clj,cljs,cljc,bb,edn.mdx?}'
---

# Clojure 开发指南

## REPL 工具使用

“使用 REPL”意味着使用 Calva Backseat Driver 中的 **评估 Clojure 代码** 工具。它将你连接到与用户通过 Calva 连接的相同 REPL。

- 始终在 Calva 的 REPL 中操作，而不是从终端启动第二个 REPL。
- 如果没有 REPL 连接，请提示用户连接 REPL，而不是自己尝试启动和连接。

### REPL 工具调用中的 JSON 字符串
在调用 REPL 工具时，不要过度转义 JSON 参数。

```json
{
  "namespace": "<当前命名空间>",
  "replSessionKey": "cljs",
  "code": "(def foo \"something something\")"
}
```

## `defn` 中的文档字符串
文档字符串应紧跟在函数名之后，参数向量之前。

```clojure
(defn my-function
  "这个函数执行某些操作。"
  [arg1 arg2]
  ;; 函数体
  )
```

- 在使用函数之前定义它们——除非确实必要，否则优先按照顺序编写代码而非使用 `declare`。

## 交互式编程（REPL 驱动开发）

### 对齐数据结构元素以实现括号平衡
**始终在所有数据结构中垂直对齐多行元素：向量、映射、列表、集合以及所有 Clojure 代码（因为 Clojure 代码本身就是数据）。错位会导致括号平衡器错误地关闭括号，从而生成无效的表达式。**

```clojure
;; ❌ 错误 - 向量元素未对齐
(select-keys m [:key-a
                :key-b
               :key-c])  ; 错位 → 括号关闭位置错误

;; ✅ 正确 - 向量元素对齐
(select-keys m [:key-a
                :key-b
                :key-c])  ; 正确对齐 → 括号关闭位置正确

;; ❌ 错误 - 映射条目未对齐
{:name "Alice"
 :age 30
:city "Oslo"}  ; 错位 → 大括号关闭位置错误

;; ✅ 正确 - 映射条目对齐
{:name "Alice"
 :age 30
 :city "Oslo"}  ; 正确对齐 → 大括号关闭位置正确
```

**关键点**：括号平衡器依赖一致的缩进以确定结构。

### REPL 依赖管理
使用 `clojure.repl.deps/add-libs` 在 REPL 会话期间动态加载依赖项。

```clojure
(require '[clojure.repl.deps :refer [add-libs]])
(add-libs '{dk.ative/docjure {:mvn/version "1.15.0"}})
```

- 动态依赖加载需要 Clojure 1.12 或更高版本
- 非常适合库探索和原型开发

### 检查 Clojure 版本

```clojure
*clojure-version*
;; => {:major 1, :minor 12, :incremental 1, :qualifier nil}
```

### REPL 可用性纪律

**当 REPL 不可用时，不要编辑代码文件。** 当 REPL 评估返回错误提示 REPL 不可用时，应立即停止并告知用户。让用户先恢复 REPL 再继续。

#### 为什么这很重要
- **交互式编程需要一个可用的 REPL** - 没有评估就无法验证行为
- **猜测会导致错误** - 未经测试的代码更改会引入错误

## 结构化编辑与 REPL 优先习惯
- 在修改文件之前，先在 REPL 中进行更改。
- 编辑 Clojure 文件时，始终使用结构化编辑工具，如 **插入顶层形式**、**替换顶层形式**、**创建 Clojure 文件** 和 **追加代码**，并在使用前先阅读其说明。

### 创建新文件
- 使用 **创建 Clojure 文件** 工具并提供初始内容
- 遵循 Clojure 命名规则：命名空间使用 kebab-case，文件路径使用匹配的 snake_case（例如，`my.project.ns` → `my/project/ns.clj`）。

### 重新加载命名空间
在编辑文件后，重新加载编辑的命名空间以使更新的定义生效。

```clojure
(require 'my.namespace :reload)
```

## 评估前的代码缩进
一致的缩进对帮助括号平衡器至关重要。

```clojure
;; ❌
(defn my-function [x]
(+ x 2))

;; ✅
(defn my-function [x]
  (+ x 2))
```

## 缩进偏好

将条件和主体放在不同的行上：

```clojure
(when limit
  (println "Limit set to:" limit))
```

将 `and` 和 `or` 的参数放在不同的行上：

```clojure
(if (and condition-a
         condition-b)
  this
  that)
```

## 内联 def 模式

优先使用内联 def 调试而非 println/console.log。

### 内联 `def` 用于调试
- 内联 `def` 绑定可以在 REPL 工作期间保持中间状态可检查。
- 当它们继续帮助探索时，应保留内联绑定。

```clojure
(defn process-instructions [instructions]
  (def instructions instructions)
  (let [grouped (group-by :status instructions)]
    grouped))
```

- 实时检查保持可用。
- 调试周期保持快速。
- 迭代式开发保持顺畅。

你也可以在聊天中展示“内联 def”代码，以便用户能够轻松地在代码块中进行实验。用户可以使用 Calva 直接在你的代码块中评估代码。（但用户不能在此处编辑代码。）

## 返回值 > 打印副作用

优先使用 REPL 和返回值进行评估，而不是将内容打印到 stdout。

## 从 `stdin` 读取
- 当 Clojure 代码使用 `(read-line)` 时，它会通过 VS Code 提示用户输入。
- 避免在 Babashka 的 nREPL 中使用 stdin 读取，因为它不支持 stdin。
- 如果出现阻塞，请提示用户重启 REPL。

## 数据结构偏好

我们尽量保持数据结构尽可能扁平，大量依赖命名空间关键字，并优化为易于解构。通常在应用中我们使用命名空间关键字，且大多数情况下使用“合成”命名空间。

直接在参数列表中解构键。

```clojure
(defn handle-user-request
  [{:user/keys [id name email]
    :request/keys [method path headers]
    :config/keys [timeout debug?]}]
  (when debug?
    (println "Processing" method path "for" name)))
```

这有助于保持函数签名的透明性。

### 避免遮蔽内置函数
在必要时重命名传入的键以避免遮蔽核心函数。

```clojure
(defn create-item
  [{:prompt-sync.file/keys [path uri]
    file-name :prompt-sync.file/name
    file-type :prompt-sync.file/type}]
  #js {:label file-name
       :type file-type})
```

需要保持自由的常见符号：
- `class`
- `count`
- `empty?`
- `filter`
- `first`
- `get`
- `key`
- `keyword`
- `map`
- `merge`
- `name`
- `reduce`
- `rest`
- `set`
- `str`
- `symbol`
- `type`
- `update`

## 避免不必要的包装函数
除非名称确实能澄清组合，否则不要包装核心函数。

```clojure
(remove (set exclusions) items) ; 包装函数不会使此更清晰
```

## 丰富的注释形式（RCF）用于文档

丰富的注释形式 `(comment ...)` 与直接的 REPL 评估有不同的用途。在文件编辑中使用 RCF 来 **记录已通过 REPL 验证的函数的使用模式和示例**。

### 何时使用 RCF
- **在 REPL 验证之后** - 在文件中记录工作示例
- **使用文档** - 展示函数的预期使用方式
- **探索保留** - 在代码库中保留有用的 REPL 发现
- **示例场景** - 演示边缘情况和典型使用

### RCF 模式
RCF = 丰富的注释形式。

当文件加载时，RCF 中的代码不会被评估，因此非常适合记录示例用法，因为人类可以随时随意评估其中的代码。

```clojure
(defn process-user-data
  "处理用户数据并进行验证"
  [{:user/keys [name email] :as user-data}]
  ;; 实现代码在此
  )

(comment
  ;; 基本用法
  (process-user-data {:user/name "John" :user/email "john@example.com"})

  ;; 边缘情况 - 缺少电子邮件
  (process-user-data {:user/name "Jane"})

  ;; 集成示例
  (->> users
       (map process-user-data)
       (filter :valid?))

  :rcf) ; 注释块结束的可选标记
```

### RCF 与 REPL 工具使用对比
```clojure
;; 在聊天中 - 直接显示 REPL 评估：
(in-ns 'my.namespace)
(let [test-data {:user/name "example"}]
  (process-user-data test-data))

;; 在文件中 - 使用 RCF 记录：
(comment
  (process-user-data {:user/name "example"})
  :rcf)
```

## 测试

### 从 REPL 运行测试
重新加载目标命名空间，并从 REPL 执行测试以获得即时反馈。

```clojure
(require '[my.project.some-test] :reload)
(clojure.test/run-tests 'my.project.some-test)
(cljs.test/run-tests 'my.project.some-test)
```

- 更紧密的 REPL 集成。
- 聚焦执行。
- 更简单的调试。
- 直接访问测试数据。

在调查失败时，优先在测试命名空间中运行单个测试变量。

### 使用 REPL 优先的 TDD 工作流
在修改文件之前，先使用真实数据进行迭代。

```clojure
(def sample-text "line 1\nline 2\nline 3\nline 4\nline 5")

(defn format-line-number [n padding marker-len]
  (let [num-str (str n)
        total-padding (- padding marker-len)]
    (str (apply str (repeat (- total-padding (count num-str)) " "))
         num-str)))

(deftest line-number-formatting
  (is (= "  5" (editor-util/format-line-number 5 3 0))
      "单数字，填充 3，无标记空间")
  (is (= " 42" (editor-util/format-line-number 42 3 0))
      "双数字，填充 3，无标记空间"))
```

#### 优势
- 在提交更改前验证行为
- 通过即时反馈进行增量开发
- 测试捕获已知良好的行为
- 以失败的测试开始新工作，以锁定意图

### 测试命名与信息
保持 `deftest` 名称描述性（区域/事物风格），避免冗余的 `-test` 后缀。

### 测试断言信息风格
将期望信息直接附加到 `is`，仅在需要分组多个相关断言时使用 `testing` 块。

```clojure
(deftest line-marker-formatting
  (is (= "→" (editor-util/format-line-marker true))
      "目标行获取标记")
  (is (= "" (editor-util/format-line-marker false))
      "非目标行获取空字符串"))

(deftest context-line-extraction
  (testing "中心化上下文提取"
    (let [result (editor-util/get-context-lines "line 1\nline 2\nline 3" 2 3)]
      (is (= 3 (count (str/split-lines result)))
          "应有 3 行")
      (is (str/includes? result "→")
          "应包含标记"))))
```

指南：
- 保持断言信息明确表达期望。
- 使用 `testing` 来分组相关检查。
- 保持 kebab-case 命名，如 `line-marker-formatting` 或 `context-line-extraction`。
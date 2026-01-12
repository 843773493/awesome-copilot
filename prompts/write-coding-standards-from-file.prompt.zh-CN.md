

---
agent: "代理"
description: "根据提示中作为参数传递的文件（和/或）文件夹的编码风格，为项目编写编码规范文档。"
tools: ['创建文件', '编辑文件', '获取', 'GitHub仓库', '搜索', '测试失败']
---

# 从文件编写编码规范

使用文件（和/或）文件夹中的现有语法来建立项目的编码规范和风格指南。如果传递了多个文件或一个文件夹，则遍历每个文件或文件夹中的文件，将文件的数据追加到临时内存或文件中，然后在完成时使用临时数据作为单一实例；如同它是基于建立规范和风格指南的文件名。

## 规则和配置

以下是准配置的 `boolean` 和 `string[]` 变量集。处理 `true` 或每个变量的其他值的条件位于二级标题 `## 变量和参数配置条件` 下。

提示参数具有文本定义。有一个必需参数 **`${fileName}`**，以及多个可选参数 **`${folderName}`**、**`${instructions}`**，以及任何 **`[configVariableAsParameter]`**。

### 配置变量

* addStandardsTest = false;
* addToREADME = false;
* addToREADMEInsertions = ["atBegin", "middle", "beforeEnd", "bestFitUsingContext"];
  - 默认为 **beforeEnd**。
* createNewFile = true;
* fetchStyleURL = true;
* findInconsistencies = true;
* fixInconsistencies = true;
* newFileName = ["CONTRIBUTING.md", "STYLE.md", "CODE_OF_CONDUCT.md", "CODING_STANDARDS.md", "DEVELOPING.md", "CONTRIBUTION_GUIDE.md", "GUIDELINES.md", "PROJECT_STANDARDS.md", "BEST_PRACTICES.md", "HACKING.md"];
  - 对于 `${newFileName}` 中的每个文件名，如果文件不存在，则使用该文件名并 `break`，否则继续下一个 `${newFileName}` 文件名。
* outputSpecToPrompt = false;
* useTemplate = "verbose"; // 或 "v"
  - 可能的值为 `[["v", "详细"], ["m", "简洁"], ["b", "最佳适配"], ["自定义"]]`。
  - 选择提示文件中二级标题 `## 编码规范模板` 下的两个示例模板之一，或使用更合适的其他组合。
  - 如果 **custom**，则根据请求进行应用。

### 配置变量作为提示参数

如果任何变量名作为原始值或类似但明显相关的文本值传递到提示中，则覆盖默认变量值。

### 提示参数

* **fileName** = 将要分析的文件名称，分析其缩进、变量命名、注释、条件语句、函数语句以及其他与编程语言语法相关数据。
* folderName = 将要用于从多个文件中提取数据并生成一个汇总数据集的文件夹名称，该数据集将分析其缩进、变量命名、注释、条件和函数嵌套、字符串引号包装符（如 `'` 或 `"`）等与语法相关的内容。
* instructions = 将为特殊案例提供的额外指令、规则和流程。
* [configVariableAsParameter] = 如果传递，则覆盖配置变量的默认状态。示例：
  - useTemplate = 如果传递，则覆盖配置 `${useTemplate}` 的默认值。值为 `[["v", "详细"], ["m", "简洁"], ["b", "最佳适配"]]`。

#### 必需和可选参数

* **fileName** - 必需
* folderName - *可选*
* instructions - *可选*
* [configVariableAsParameter] - *可选*

## 变量和参数配置条件

### `${fileName}.length > 1 || ${folderName} != undefined`

* 如果为真，则切换 `${fixInconsistencies}` 为 false。

### `${addToREADME} == true`

* 如果为真，则将编码规范插入到 `README.md` 文件中，而不是输出到提示或创建新文件。
* 如果为真，则切换 `${createNewFile}` 和 `${outputSpecToPrompt}` 为 false。

### `${addToREADMEInsertions} == "atBegin"`

* 如果 `${addToREADME}` 为真，则在 `README.md` 文件标题之后插入编码规范数据在**开头**。

### `${addToREADMEInsertions} == "middle"`

* 如果 `${addToREADME}` 为真，则在 `README.md` 文件的**中间**插入编码规范数据，并将规范标题的标题行更改为与 `README.md` 的内容匹配。

### `${addToREADMEInsertions} == "beforeEnd"`

* 如果 `${addToREADME}` 为真，则在 `README.md` 文件的**结尾**插入编码规范数据，在最后一个字符后插入新行，然后在新行中插入数据。

### `${addToREADMEInsertions} == "bestFitUsingContext"`

* 如果 `${addToREADME}` 为真，则根据 `README.md` 的内容和数据流，在 `README.md` 文件的**最佳适配行**插入编码规范数据。

### `${addStandardsTest} == true`

* 一旦编码规范文件完成，编写一个测试文件以确保传递给它的文件或文件夹符合编码规范。

### `${createNewFile} == true`

* 使用 `${newFileName}` 的值或其可能的值创建新文件。
* 如果为真，则切换 `${outputSpecToPrompt}` 和 `${addToREADME}` 为 false。

### `${fetchStyleURL} == true`

* 根据编程语言，对于下面列表中的每个链接，如果编程语言是 `${fileName} == [<Language> 风格指南]`，则运行 `#fetch (URL)`。

### 获取链接

- [C 编程风格指南](https://users.ece.cmu.edu/~eno/coding/CCodingStandard.html)
- [C# 编程风格指南](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [C++ 编程风格指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [Go 编程风格指南](https://github.com/golang-standards/project-layout)
- [Java 编程风格指南](https://coderanch.com/wiki/718799/Style)
- [AngularJS 应用风格指南](https://github.com/mgechev/angularjs-style-guide)
- [jQuery 风格指南](https://contribute.jquery.org/style-guide/js/)
- [JavaScript 风格指南](https://www.w3schools.com/js/js_conventions.asp)
- [JSON 风格指南](https://google.github.io/styleguide/jsoncstyleguide.xml)
- [Kotlin 风格指南](https://kotlinlang.org/docs/coding-conventions.html)
- [Markdown 风格指南](https://cirosantilli.com/markdown-style-guide/)
- [Perl 风格指南](https://perldoc.perl.org/perlstyle)
- [PHP 风格指南](https://phptherightway.com/)
- [Python 风格指南](https://peps.python.org/pep-0008/)
- [Ruby 风格指南](https://rubystyle.guide/)
- [Rust 风格指南](https://github.com/rust-lang/rust/tree/HEAD/src/doc/style-guide/src)
- [Swift 风格指南](https://www.swift.org/documentation/api-design-guidelines/)
- [TypeScript 风格指南](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
- [Visual Basic 风格指南](https://en.wikibooks.org/wiki/Visual_Basic/Coding_Standards)
- [Shell 脚本风格指南](https://google.github.io/styleguide/shellguide.html)
- [Git 使用风格指南](https://github.com/agis/git-style-guide)
- [PowerShell 风格指南](https://github.com/PoshCode/PowerShellPracticeAndStyle)
- [CSS](https://cssguidelin.es/)
- [Sass 风格指南](https://sass-guidelin.es/)
- [HTML 风格指南](https://github.com/marcobiedermann/html-style-guide)
- [Linux 内核风格指南](https://www.kernel.org/doc/html/latest/process/coding-style.html)
- [Node.js 风格指南](https://github.com/felixge/node-style-guide)
- [SQL 风格指南](https://www.sqlstyle.guide/)
- [Angular 风格指南](https://angular.dev/style-guide)
- [Vue 风格指南](https://vuejs.org/style-guide/rules-strongly-recommended.html)
- [Django 风格指南](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
- [SystemVerilog 风格指南](https://github.com/lowRISC/style-guides/blob/master/VerilogCodingStyle.md)

## 编码规范模板

### `"m", "简洁"`

```text
    ```markdown
    ## 1. 引言
    *   **目的:** 简要说明为何要建立编码规范（例如，以提高代码质量、可维护性和团队协作）。
    *   **范围:** 定义该规范适用于哪些语言、项目或模块。

    ## 2. 命名约定
    *   **变量:** `camelCase`
    *   **函数/方法:** `PascalCase` 或 `camelCase`。
    *   **类/结构体:** `PascalCase`。
    *   **常量:** `UPPER_SNAKE_CASE`。

    ## 3. 格式化和风格
    *   **缩进:** 使用 4 个空格（或制表符）进行缩进。
    *   **行长度:** 限制行长度为最多 80 或 120 个字符。
    *   **大括号:** 使用 "K&R" 风格（大括号在同一行）或 "Allman" 风格（大括号在新行）。
    *   **空行:** 指定用于分隔逻辑代码块的空行数量。

    ## 4. 注释
    *   **文档字符串/函数注释:** 描述函数的目的、参数和返回值。
    *   **内联注释:** 解释复杂或不明显的逻辑。
    *   **文件头:** 指定文件头应包含哪些信息，如作者、日期和文件描述。

    ## 5. 错误处理
    *   **通用:** 如何处理和记录错误。
    *   **具体:** 使用哪些异常类型，以及在错误信息中应包含哪些信息。

    ## 6. 最佳实践和反模式
    *   **通用:** 列出应避免的常见反模式（例如，全局变量、魔术数字）。
    *   **语言特定:** 基于项目的编程语言的具体建议。

    ## 7. 示例
    *   提供一个小型代码示例，展示规则的正确应用。
    *   提供一个小型错误实现示例以及如何修复。

    ## 8. 贡献和执行
    *   解释规范如何执行（例如，通过代码审查）。
    *   提供对规范文档本身的贡献指南。
    ```
```

### `"v", verbose"`

```text
    ```markdown

    # 风格指南

    本文件定义了该项目使用的风格和约定。
    所有贡献应遵循这些规则，除非另有说明。

    ## 1. 通用代码风格

    - 优先清晰性而非简洁性。
    - 保持函数和方法的小而专注。
    - 避免重复逻辑；优先使用共享的辅助工具/实用程序。
    - 删除未使用的变量、导入、代码路径和文件。

    ## 2. 命名约定

    使用描述性名称。避免使用缩写，除非是众所周知的。

    | 项目            | 约定           | 示例            |
    |-----------------|----------------|-----------------|
    | 变量            | `lower_snake_case` | `buffer_size`      |
    | 函数            | `lower_snake_case()` | `read_file()`      |
    | 常量            | `UPPER_SNAKE_CASE` | `MAX_RETRIES`      |
    | 类型/结构体      | `PascalCase`    | `FileHeader`       |
    | 文件名          | `lower_snake_case` | `file_reader.c`    |

    ## 3. 格式化规则

    - 缩进：**4 个空格**
    - 行长度：**最多 100 个字符**
    - 编码：**UTF-8**，无 BOM
    - 以换行符结束文件

    ### 大括号（C 语言示例，请根据您的语言调整）

        ```c
        if (condition) {
            do_something();
        } else {
            do_something_else();
        }
        ```

    ### 空格

    - 关键字后加一个空格：`if (x)`，而不是 `if(x)`
    - 在顶层函数之间留一个空行

    ## 4. 注释与文档

    - 解释 *为什么*，而不是 *做什么*，除非意图不明确。
    - 随着代码更改，保持注释的更新。
    - 公共函数应包含其目的和参数的简要描述。

    推荐的标签：

        ```text
        TODO: 后续工作
        FIXME: 已知的错误行为
        NOTE: 非明显的架构决策
        ```

    ## 5. 错误处理

    - 明确处理错误条件。
    - 避免静默失败；要么返回错误，要么适当记录错误。
    - 在失败时清理资源（文件、内存、句柄）。

    ## 6. 提交与审查实践

    ### 提交
    - 每个提交对应一个逻辑更改。
    - 编写清晰的提交信息：

        ```text
        简短摘要（最多 ~50 个字符）
        可选的更长解释，说明上下文和理由。
        ```

    ### 审查
    - 保持拉取请求合理的小规模。
    - 在审查讨论中保持尊重和建设性。
    - 处理请求的更改，或解释不同意的原因。

    ## 7. 测试

    - 为新功能编写测试。
    - 测试应是确定性的（无随机性，除非已播种）。
    - 优先使用可读的测试用例而非复杂的测试抽象。

    ## 8. 对本指南的更改

    风格会演变。
    通过打开问题或发送更新此文档的补丁来提出改进。
    ```
```
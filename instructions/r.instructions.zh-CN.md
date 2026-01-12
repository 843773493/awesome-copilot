

---
描述：'R语言和文档格式（R、Rmd、Quarto）：为生成符合规范、安全且一致的R代码提供编码标准和Copilot指导。'
适用范围：'**/*.R, **/*.r, **/*.Rmd, **/*.rmd, **/*.qmd'
---

# R编程语言指南

## 目的

帮助GitHub Copilot在不同项目中生成符合规范、安全且易于维护的R代码。

## 核心规范

- **遵循项目风格。** 如果文件中已存在风格偏好（如tidyverse与基础R、`%>%`与`|>`），请遵循其规范。
- **优先使用清晰的向量化代码。** 保持函数简洁，避免隐藏的副作用。
- **在示例/代码片段中限定非基础函数，** 例如：`dplyr::mutate()`、`stringr::str_detect()`。在项目代码中，若该规范是仓库标准，则使用`library()`是可接受的。
- **命名：** 对象/文件使用`lower_snake_case`；避免在名称中使用点号（.）。
- **副作用：** 永远不要调用`setwd()`；优先使用相对于项目的路径（例如：`here::here()`）。
- **可重复性：** 使用`withr::with_seed()`在随机操作周围设置种子。
- **验证：** 验证并限制用户输入；尽可能使用类型检查和允许列表。
- **安全性：** 避免使用`eval(parse())`、未经验证的shell调用以及非参数化的SQL。

### 管道运算符

- **原生管道`|>`（R ≥ 4.1.0）：** 在R ≥ 4.1中优先使用（无需额外依赖）。
- **Magrittr管道`%>%`：** 在已采用magrittr的项目中继续使用，或在需要`.`, `%T>%`, `%$%`等特性时使用。
- **保持一致性：** 除非有明确的技术原因，否则不要在同一个脚本中混合使用`|>`和`%>%`。

## 性能考量

- **大型数据集：** 考虑使用`data.table`；根据实际工作负载进行基准测试。
- **dplyr兼容性：** 使用`dtplyr`编写dplyr语法，使其自动转换为data.table操作以实现性能提升。
- **性能分析：** 使用`profvis::profvis()`识别代码中的性能瓶颈。在优化前进行性能分析。
- **缓存：** 使用`memoise::memoise()`缓存昂贵的函数结果。特别适用于重复的API调用或复杂的计算。
- **向量化操作：** 优先使用向量化操作而非循环。对于剩余的迭代需求，使用`purrr::map_*()`家族或`apply()`家族。

## 工具与质量

- **格式化：** 使用`styler`（tidyverse风格），两空格缩进，约100字符的行宽。
- **代码检查：** 通过`.lintr`配置`lintr`。
- **预提交：** 考虑使用`precommit`钩子自动进行代码检查和格式化。
- **文档：** 使用`roxygen2`为导出函数编写文档（`@param`, `@return`, `@examples`）。
- **测试：** 优先使用小型、纯函数且易于组合的函数，以便进行单元测试。
- **依赖管理：** 使用`renv`进行管理；添加包后进行快照。
- **路径：** 优先使用`fs`和`here`以提高可移植性。

## 数据处理与输入输出

- **数据框：** 在以tidyverse为主的文件中优先使用tibbles；否则基础`data.frame()`即可。
- **迭代：** 在tidyverse代码中使用`purrr`。在基础风格代码中，优先使用类型稳定且向量化的模式，如`vapply()`（用于原子输出）或`Map()`（用于元素级操作），而非显式的`for`循环，当它们能提高清晰度或性能时。
- **字符串与日期：** 已使用`stringr`/`lubridate`时优先使用；否则使用清晰的基础函数（例如：`nchar()`、`substr()`、`as.Date()`并显式指定格式）。
- **输入输出：** 优先使用显式、类型化的读取器（例如：`readr::read_csv()`）；明确解析假设。

## 可视化

- 优先使用`ggplot2`生成出版质量的图表。保持图层可读，明确标注坐标轴和单位。

## 错误处理

- 在tidyverse上下文中，使用`rlang::abort()` / `rlang::warn()`处理结构化条件；在仅基础R的代码中，使用`stop()` / `warning()`。
- 对于可恢复的操作：
- 使用`purrr::possibly()`当需要同类型的备用值（更简单）。
- 使用`purrr::safely()`当需要捕获结果和错误以供后续检查或日志记录。
- 在基础R中使用`tryCatch()`实现精细控制或与非tidyverse代码兼容。
- 优先保持一致的返回结构——正常流程返回类型化输出，仅在需要错误详细信息时返回结构化列表。

## 安全最佳实践

- **命令执行：** 优先使用`processx::run()`或`sys::exec_wait()`而非`system()`；验证并清理所有参数。
- **数据库查询：** 使用参数化`DBI`查询以防止SQL注入。
- **文件路径：** 规范化和清理用户提供的路径（例如：`fs::path_sanitize()`），并验证允许列表。
- **凭证：** 永远不要硬编码敏感信息。使用环境变量（`Sys.getenv()`）、版本控制系统外的配置文件，或`keyring`。

## Shiny

- 对于非平凡的应用程序，模块化UI和服务器逻辑。使用`eventReactive()` / `observeEvent()`明确依赖关系。
- 使用`req()`验证输入，并提供清晰、用户友好的消息。
- 使用连接池（`pool`）进行数据库连接；避免长期存在的全局对象。
- 隔离昂贵的计算，并优先使用`reactiveVal()` / `reactiveValues()`处理小型状态。

## R Markdown / Quarto

- 保持代码块专注；优先使用显式的代码块选项（`echo`, `message`, `warning`）。
- 避免全局状态；优先使用局部辅助函数。使用`withr::with_seed()`确保代码块的确定性。

## Copilot特定指导

- 如果当前文件使用tidyverse，请**建议优先采用tidyverse模式**（例如：使用`dplyr::across()`而非已弃用的动词）。如果存在基础R风格，请**使用基础R的惯用法**。
- 在建议中限定非基础函数调用（例如：`dplyr::mutate()`）。
- 在符合惯用法时，建议使用向量化或整洁的解决方案而非循环。
- 优先使用小型辅助函数而非长管道。
- 当多种方法等效时，优先考虑可读性和类型稳定性，并解释权衡。

---

## 最小示例

```r
# 基础R版本
scores <- data.frame(id = 1:5, x = c(1, 3, 2, 5, 4))
safe_log <- function(x) tryCatch(log(x), error = function(e) NA_real_)
scores$z <- vapply(scores$x, safe_log, numeric(1))

# tidyverse版本（如果该文件使用tidyverse）
result <- tibble::tibble(id = 1:5, x = c(1, 3, 2, 5, 4)) |>
dplyr::mutate(z = purrr::map_dbl(x, purrr::possibly(log, otherwise = NA_real_))) |>
dplyr::filter(z > 0)

# 带roxygen2文档的可重用辅助函数示例
#' 计算数值向量的z分数
#' @param x 一个数值向量
#' @return z分数的数值向量
#' @examples z_score(c(1, 2, 3))
z_score <- function(x) (x - mean(x, na.rm = TRUE)) / stats::sd(x, na.rm = TRUE)
```
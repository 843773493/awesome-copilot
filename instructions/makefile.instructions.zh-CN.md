

---
description: "编写 GNU Make Makefile 的最佳实践"
applyTo: "**/Makefile, **/makefile, **/*.mk, **/GNUmakefile"
---

# Makefile 开发指南

编写清晰、可维护且可移植的 GNU Make Makefile 的指导原则。这些指导原则基于 [GNU Make 手册](https://www.gnu.org/software/make/manual/)。

## 通用原则

- 编写清晰且易于维护的 makefile，遵循 GNU Make 的规范
- 使用描述性的目标名称，明确表明其用途
- 将默认目标（第一个目标）设为最常见的构建操作
- 在编写规则和命令时优先考虑可读性而非简洁性
- 对于复杂规则、变量或非直观行为添加注释进行解释

## 命名规范

- 将 makefile 命名为 `Makefile`（推荐用于提高可见性）或 `makefile`
- 仅在需要 GNU Make 特定功能且与其他 make 实现不兼容时使用 `GNUmakefile`
- 使用标准变量名：`objects`、`OBJECTS`、`objs`、`OBJS`、`obj` 或 `OBJ` 表示对象文件列表
- 使用大写字母表示内置变量名（例如 `CC`、`CFLAGS`、`LDFLAGS`）
- 使用描述性的目标名称，反映其操作（例如 `clean`、`install`、`test`）

## 文件结构

- 将默认目标（主构建目标）作为 makefile 中的第一个规则
- 将相关的目标逻辑分组
- 在规则之前在 makefile 顶部定义变量
- 使用 `.PHONY` 声明不表示文件的目标
- 按以下结构组织 makefile：变量、规则、phony 目标

```makefile
# 变量
CC = gcc
CFLAGS = -Wall -g
objects = main.o utils.o

# 默认目标
all: program

# 规则
program: $(objects)
	$(CC) -o program $(objects)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# phony 目标
.PHONY: clean all
clean:
	rm -f program $(objects)
```

## 变量和替换

- 使用变量以避免重复并提高可维护性
- 使用 `:=`（简单展开）进行立即评估，使用 `=` 进行递归展开
- 使用 `?=` 设置默认值，该值可以被覆盖
- 使用 `+=` 向现有变量追加内容
- 使用 `$(VARIABLE)` 引用变量，而不是 `$VARIABLE`（除非是单字符变量）
- 在命令中使用自动变量（`$@`、`$<`、`$^`、`$?`、`$*`）使规则更通用

```makefile
# 简单展开（立即评估）
CC := gcc

# 递归展开（在使用时评估）
CFLAGS = -Wall $(EXTRA_FLAGS)

# 条件赋值
PREFIX ?= /usr/local

# 追加到变量
CFLAGS += -g
```

## 规则和依赖项

- 明确区分目标、依赖项和命令
- 对标准编译使用隐式规则（例如 `.c` 到 `.o`）
- 以逻辑顺序列出依赖项（常规依赖项在顺序依赖项之前）
- 使用顺序依赖项（在 `|` 后）用于不应触发重新构建的目录和依赖项
- 包含所有实际依赖项以确保正确重建
- 避免目标之间的循环依赖
- 注意顺序依赖项不会包含在自动变量如 `$^` 中，如需引用应显式声明

以下示例展示了一个模式规则，将对象文件编译到 `obj/` 目录中。目录本身被列为顺序依赖项，以便在编译前创建，但其时间戳变化时不会强制重新编译。

```makefile
# 常规依赖项
program: main.o utils.o
	$(CC) -o $@ $^

# 顺序依赖项（目录创建）
obj/%.o: %.c | obj
	$(CC) $(CFLAGS) -c $< -o $@

obj:
	mkdir -p obj
```

## 命令和操作

- 每个命令行以 **制表符** 开头（除非更改了 `.RECIPEPREFIX`）
- 适当使用 `@` 前缀来抑制命令回显
- 使用 `-` 前缀忽略特定命令的错误（谨慎使用）
- 在必须一起执行时，使用 `&&` 或 `;` 在同一行组合相关命令
- 保持命令可读；使用反斜杠续行符将长命令拆分为多行
- 在命令中需要时使用 shell 条件语句和循环

```makefile
# 静默命令
clean:
	@echo "正在清理..."
	@rm -f $(objects)

# 忽略错误
.PHONY: clean-all
clean-all:
	-rm -rf build/
	-rm -rf dist/

# 使用正确续行的多行命令
install: program
	install -d $(PREFIX)/bin && \
		install -m 755 program $(PREFIX)/bin
```

## phony 目标

- 始终使用 `.PHONY` 声明非文件目标，以避免与同名文件冲突
- 用于 `clean`、`install`、`test`、`all` 等操作
- 将 phony 目标声明靠近其规则定义或放在 makefile 末尾

```makefile
.PHONY: all clean test install

all: program

clean:
	-rm -f program $(objects)

test: program
	./run-tests.sh

install: program
	install -m 755 program $(PREFIX)/bin
```

## 模式规则和隐式规则

- 使用模式规则（`%.o: %.c`）进行通用转换
- 适当利用内置隐式规则（GNU Make 知道如何将 `.c` 转换为 `.o`）
- 覆盖隐式规则变量（如 `CC`、`CFLAGS`）而不是重写规则
- 仅在内置规则不足时定义自定义模式规则

```makefile
# 通过设置变量使用内置隐式规则
CC = gcc
CFLAGS = -Wall -Wextra -O2

# 自定义模式规则用于特殊情形
%.pdf: %.md
	pandoc $< -o $@
```

## 拆分长行

- 使用反斜杠换行符（`\`）拆分长行以提高可读性
- 注意在非命令上下文中，反斜杠换行符会被转换为单个空格
- 在命令中，反斜杠换行符会保留对 shell 的行继续
- 避免在反斜杠后留有尾随空格

### 拆分不添加空格

如果需要拆分一行而不添加空格，可以使用特殊技巧：插入 `$ `（美元符号加空格）后跟反斜杠换行符。`$ ` 指向一个名为单个空格的变量，该变量不存在，因此会扩展为空，从而在不插入空格的情况下连接行。

```makefile
# 不添加空格地连接字符串
# 以下代码生成值 "oneword"
var := one$ \
       word

# 等效于：
# var := oneword
```

```makefile
# 变量定义跨行
sources = main.c \
          utils.c \
          parser.c \
          handler.c

# 命令中长命令
build: $(objects)
	$(CC) -o program $(objects) \
	      $(LDFLAGS) \
	      -lm -lpthread
```

## 包含其他 Makefile

- 使用 `include` 指令在多个 makefile 之间共享通用定义
- 使用 `-include`（或 `sinclude`）包含可选 makefile，即使不存在也不会报错
- 在可能影响包含文件的变量定义之后放置 `include` 指令
- 使用 `include` 来共享变量、模式规则或通用目标

```makefile
# 包含通用设置
include config.mk

# 包含可选的本地配置
-include local.mk
```

## 条件指令

- 使用条件指令（`ifeq`、`ifneq`、`ifdef`、`ifndef`）处理平台或配置特定的规则
- 将条件指令放在 makefile 级别，而非命令中（在命令中使用 shell 条件指令）
- 保持条件指令简单且文档齐全

```makefile
# 平台特定设置
ifeq ($(OS),Windows_NT)
    EXE_EXT = .exe
else
    EXE_EXT =
endif

program: main.o
	$(CC) -o $@ $^
```

## 自动依赖项

- 生成依赖项而非手动维护
- 使用编译器标志如 `-MMD` 和 `-MP` 生成包含依赖项的 `.d` 文件
- 使用 `-include $(deps)` 包含生成的依赖项文件，以避免文件不存在时报错

```makefile
objects = main.o utils.o
deps = $(objects:.o=.d)

# 包含依赖项文件
-include $(deps)

# 使用自动依赖项生成编译
%.o: %.c
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@
```

## 错误处理和调试

- 使用 `$(error text)` 或 `$(warning text)` 函数进行构建时诊断
- 使用 `make -n`（干运行）查看命令而不执行
- 使用 `make -p` 打印规则和变量数据库用于调试
- 在 makefile 开头验证必需的变量和工具

```makefile
# 检查必需的工具
ifeq ($(shell which gcc),)
    $(error "gcc 未安装或不在 PATH 中")
endif

# 验证必需的变量
ifndef VERSION
    $(error VERSION 未定义)
endif
```

## 清理目标

- 始终提供一个 `clean` 目标以删除生成的文件
- 声明 `clean` 为 phony 目标以避免与名为 "clean" 的文件冲突
- 使用 `-` 前缀与 `rm` 命令以忽略文件不存在时的错误
- 考虑提供单独的 `clean`（删除对象文件）和 `distclean`（删除所有生成文件）目标

```makefile
.PHONY: clean distclean

clean:
	-rm -f $(objects)
	-rm -f $(deps)

distclean: clean
	-rm -f program config.mk
```

## 可移植性注意事项

- 如果需要移植到其他 make 实现，避免使用 GNU Make 特定功能
- 使用标准 shell 命令（优先使用 POSIX shell 构造）
- 使用 `make -B` 强制重新构建所有目标以测试
- 文档化任何平台特定要求或 GNU Make 扩展

## 性能优化

- 对不需要递归展开的变量使用 `:=`（更快）
- 避免不必要的 `$(shell ...)` 使用，因为其会创建子进程
- 有效排序依赖项（最频繁更改的文件放在最后）
- 在确保目标不冲突的前提下安全使用并行构建（`make -j`）

## 文档和注释

- 添加头部注释说明 makefile 的用途
- 文档化非直观的变量设置及其影响
- 在注释中包含用法示例或目标
- 对复杂规则或平台特定的解决方法添加内联注释

```makefile
# 用于构建示例应用程序的 Makefile
#
# 用法：
#   make          - 构建程序
#   make clean    - 删除生成的文件
#   make install  - 安装到 $(PREFIX)
#
# 变量：
#   CC       - C 编译器（默认为 gcc）
#   PREFIX   - 安装路径（默认为 /usr/local）

# 编译器和标志
CC ?= gcc
CFLAGS = -Wall -Wextra -O2

# 安装目录
PREFIX ?= /usr/local
```

## 特殊目标

- 使用 `.PHONY` 为非文件目标
- 使用 `.PRECIOUS` 保留中间文件
- 使用 `.INTERMEDIATE` 标记文件为中间文件（自动删除）
- 使用 `.SECONDARY` 防止删除中间文件
- 使用 `.DELETE_ON_ERROR` 在命令失败时删除目标
- 使用 `.SILENT` 抑制所有命令的回显（谨慎使用）

```makefile
# 不删除中间文件
.SECONDARY:

# 在命令失败时删除目标
.DELETE_ON_ERROR:

# 保留特定文件
.PRECIOUS: %.o
```

## 常见模式

### 标准项目结构

```makefile
CC = gcc
CFLAGS = -Wall -O2
objects = main.o utils.o parser.o

.PHONY: all clean install

all: program

program: $(objects)
	$(CC) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	-rm -f program $(objects)
```

### 管理多个程序

```makefile
programs = prog1 prog2 prog3

.PHONY: all clean

all: $(programs)

prog1: prog1.o common.o
	$(CC) -o $@ $^

prog2: prog2.o common.o
	$(CC) -o $@ $^

prog3: prog3.o
	$(CC) -o $@ $^

clean:
	-rm -f $(programs) *.o
```

## 避免的反模式

- 不要以空格开头命令行，而应使用制表符
- 避免在可以使用通配符或函数生成文件列表时硬编码文件列表
- 不要使用 `$(shell ls ...)` 获取文件列表（应使用 `$(wildcard ...)` 代替）
- 避免在命令中使用复杂的 shell 脚本（将其移至单独的脚本文件）
- 不要忘记将 phony 目标声明为 `.PHONY`
- 避免目标之间的循环依赖
- 除非绝对必要，否则避免使用递归 make（`$(MAKE) -C subdir`）
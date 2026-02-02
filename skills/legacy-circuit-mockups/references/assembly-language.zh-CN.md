# 6502 汇编语言与 AT28C256 EEPROM 的应用

一个用于编写**6502/65C02 汇编语言程序**的实用规范，这些程序旨在存储在并行 EEPROM **AT28C256 (32 KB)** 中并在单板计算机 (SBCs) 和复古系统中执行。

---

## 1. 范围与假设

本文件假设：

* 一个 **6502 家族 CPU**（6502、65C02 或兼容型号）
* 程序代码存储在 **AT28C256 (32K x 8) EEPROM** 中
* 内存映射输入/输出（例如 6522 VIA）
* 复位和中断向量位于 EEPROM 中
* 外部 RAM 映射在其他地址空间（例如 62256 SRAM）

---

## 2. AT28C256 EEPROM 概述

| 参数         | 值                     |
|--------------|------------------------|
| 容量         | 32 KB（32768 字节）     |
| 地址线       | A0-A14                 |
| 数据线       | D0-D7                  |
| 访问时间     | ~150 ns                |
| 供电电压     | 5 V                    |
| 封装类型     | DIP-28 / PLCC          |

### 典型内存映射使用

| 地址范围     | 使用方式               |
|--------------|------------------------|
| `$8000-$FFFF` | EEPROM（代码 + 向量）     |
| `$FFFA-$FFFF` | 中断向量               |

---

## 3. 6502 内存映射示例

```
$0000-$00FF  零页（RAM）
$0100-$01FF  堆栈
$0200-$7FFF  RAM / 输入/输出
$8000-$FFFF  AT28C256 EEPROM
```

---

## 4. 复位和中断向量

6502 从 **内存顶部** 读取向量：

| 向量   | 地址           | 描述                   |
|--------|----------------|------------------------|
| NMI    | `$FFFA-$FFFB`  | 不可屏蔽中断           |
| RESET  | `$FFFC-$FFFD`  | 复位入口点             |
| IRQ/BRK | `$FFFE-$FFFF`  | 可屏蔽中断             |

### 向量定义示例

```asm
        .org $FFFA
        .word nmi_handler
        .word reset
        .word irq_handler
```

---

## 5. 6502 汇编程序结构

### 典型布局

```asm
        .org $8000

reset:
        sei             ; 禁用 IRQ
        cld             ; 清除十进制模式
        ldx #$FF
        txs             ; 初始化堆栈

main:
        jmp main
```

---

## 6. 6502 的基本指令

### 寄存器

| 寄存器 | 用途               |
|--------|--------------------|
| A      | 累加器             |
| X, Y   | 索引寄存器         |
| SP     | 堆栈指针           |
| PC     | 程序计数器         |
| P      | 处理器状态         |

### 常用指令

| 指令     | 功能                   |
|----------|------------------------|
| LDA/STA  | 加载/存储累加器         |
| LDX/LDY  | 加载索引寄存器          |
| JMP/JSR  | 跳转 / 子程序调用        |
| RTS      | 从子程序返回             |
| BEQ/BNE  | 条件跳转                |
| SEI/CLI  | 禁用/启用 IRQ           |

---

## 7. 地址寻址模式（常见）

| 模式     | 示例             | 说明         |
|----------|------------------|--------------|
| 立即数   | `LDA #$01`       | 常量         |
| 零页     | `LDA $00`        | 快速访问     |
| 绝对地址 | `LDA $8000`      | 完整地址     |
| 索引     | `LDA $2000,X`    | 表格寻址     |
| 间接     | `JMP ($FFFC)`    | 向量寻址     |

---

## 8. 为 EEPROM 执行编写代码

### 关键注意事项

* 代码在运行时是 **只读的**
* 不建议使用自修改代码
* 将跳转表和常量存储在 EEPROM 中
* 使用 RAM 存储变量和堆栈

### 零页变量示例

```asm
counter = $00

        lda #$00
        sta counter
```

---

## 9. 时间与性能

* EEPROM 访问时间必须满足 CPU 时钟要求
* AT28C256 可轻松支持约 1 MHz 的时钟频率
* 更快的时钟可能需要等待状态或 ROM 阴影技术

---

## 10. 示例：简单 LED 切换（内存映射输入/输出）

```asm
PORTB = $6000
DDRB  = $6002

        .org $8000
reset:
        sei             ; 禁用 IRQ
        ldx #$FF
        txs

        lda #$FF
        sta DDRB

loop:
        lda #$FF
        sta PORTB
        jsr delay
        lda #$00
        sta PORTB
        jsr delay
        jmp loop
```

---

## 11. 汇编与编程工作流程

1. 编写源代码（`.asm`）
2. 汇编为二进制文件
3. 填充或调整到 `$8000` 地址
4. 通过 T48 / minipro 烧录 AT28C256
5. 插入 EEPROM 并复位 CPU

---

## 12. 常用汇编器指令

| 指令         | 用途                     |
|--------------|--------------------------|
| `.org`       | 设置程序起始地址           |
| `.byte`      | 定义字节                 |
| `.word`      | 定义字（小端格式）         |
| `.include`   | 包含文件                 |
| `.equ`       | 常量定义                 |

---

## 13. 常见错误

| 问题                   | 结果             |
|------------------------|------------------|
| 缺少向量               | CPU 在复位时挂起 |
| 错误的 `.org`          | 代码未执行       |
| 在 ROM 中使用 RAM 地址 | 系统崩溃         |
| 堆栈未初始化           | 未定义行为       |

---

## 14. 参考链接

* [https://www.masswerk.at/6502/6502_instruction_set.html](https://www.masswerk.at/6502/6502_instruction_set.html)
* [https://www.nesdev.org/wiki/6502](https://www.nesdev.org/wiki/6502)
* [https://www.westerndesigncenter.com/wdc/documentation](https://www.westerndesigncenter.com/wdc/documentation)
* [https://en.wikipedia.org/wiki/MOS_Technology_6502](https://en.wikipedia.org/wiki/MOS_Technology_6502)

---

**文档范围：** 存储在 AT28C256 EEPROM 中的 6502 汇编语言  
**受众：** 复古计算、单板计算机设计者、嵌入式爱好者  
**状态：** 稳定参考

# 6502 单板计算机汇编编译与ROM构建规范

## 概述

本文件定义了**用于6502汇编语言的完整编译规范**，该单板计算机由以下组件构成：

* **MOS 6502 处理器**
* **MOS 6522 VIA**
* **AS6C62256（32 KB SRAM）**
* **AT28C256（32 KB EEPROM / ROM）**
* **DFRobot FIT0127（兼容HD44780的16x2 LCD）**

重点在于**工具链行为、内存布局、ROM构建和固件约定**，而非电气布线。

---

## 目标系统架构

### 内存映射（规范格式）

```
$0000-$00FF  零页（RAM）
$0100-$01FF  堆栈（RAM）
$0200-$7FFF  通用RAM（AS6C62256）
$8000-$8FFF  6522 VIA I/O空间
$9000-$FFFF  ROM（AT28C256）
```

> 地址解码可能会镜像设备；汇编器假设此规范布局。

---

## ROM组织（AT28C256）

| 地址       | 用途               |
|------------|--------------------|
| $9000-$FFEF | 程序代码 + 数据     |
| $FFF0-$FFF9 | 可选系统数据        |
| $FFFA-$FFFB | 非屏蔽中断向量      |
| $FFFC-$FFFD | 复位向量           |
| $FFFE-$FFFF | 中断/断点向量       |

ROM镜像大小：**32,768字节**

---

## 复位与启动约定

复位时：

1. CPU从$FFFC地址获取复位向量
2. 代码初始化堆栈指针
3. 初始化零页变量
4. 配置VIA
5. 初始化LCD
6. 进入主程序

---

## 汇编器要求

汇编器**必须**支持：

* `.org`绝对寻址
* 符号标签
* 二进制输出（`.bin`）
* 小端格式的字输出
* 零页优化

推荐汇编器：

* **ca65**（cc65工具链）
* **vasm6502**
* **64tass**

---

## 汇编源代码结构

```asm
;---------------------------
; 复位向量入口点
;---------------------------
        .org $9000
RESET:
        sei
        cld
        ldx #$FF
        txs
        jsr init_via
        jsr init_lcd
MAIN:
        jsr lcd_print
        jmp MAIN
```

---

## 向量表定义

```asm
        .org $FFFA
        .word nmi_handler
        .word RESET
        .word irq_handler
```

---

## 6522 VIA编程模型

### 寄存器映射（基地址 = $8000）

| 偏移量 | 寄存器 |
|--------|--------|
| $0     | ORB    |
| $1     | ORA    |
| $2     | DDRB   |
| $3     | DDRA   |
| $4     | T1CL   |
| $5     | T1CH   |
| $6     | T1LL   |
| $7     | T1LH   |
| $8     | T2CL   |
| $9     | T2CH   |
| $B     | ACR    |
| $C     | PCR    |
| $D     | IFR    |
| $E     | IER    |

---

## LCD接口约定

### LCD布线假设

| LCD   | VIA     |
|-------|---------|
| D4-D7 | PB4-PB7 |
| RS    | PA0     |
| E     | PA1     |
| R/W   | GND     |

假设使用4位模式。

---

## LCD初始化序列

```asm
lcd_init:
        lda #$33
        jsr lcd_cmd
        lda #$32
        jsr lcd_cmd
        lda #$28
        jsr lcd_cmd
        lda #$0C
        jsr lcd_cmd
        lda #$06
        jsr lcd_cmd
        lda #$01
        jsr lcd_cmd
        rts
```

---

## LCD命令/数据接口

| 操作     | RS | 数据         |
|----------|----|--------------|
| 命令     | 0  | 指令         |
| 数据     | 1  | ASCII字符    |

---

## 零页使用约定

| 地址     | 用途         |
|----------|--------------|
| $00-$0F  | 临时存储区   |
| $10-$1F  | LCD程序      |
| $20-$2F  | VIA状态      |
| $30-$FF  | 用户自定义   |

---

## RAM使用（AS6C62256）

* 堆栈使用页面$01
* 所有RAM均假设为易失性
* 不进行ROM影射

---

## 构建流程

### 第一步：汇编

```bash
ca65 main.asm -o main.o
```

### 第二步：链接

```bash
ld65 -C rom.cfg main.o -o rom.bin
```

### 第三步：填充ROM

确保`rom.bin`恰好为**32768字节**。

---

## EEPROM编程

* 目标设备：**AT28C256**
* 编程器：**MiniPro / T48**
* 写入后验证

---

## 模拟器期望

模拟器必须：

* 在$9000-$FFFF地址加载ROM
* 模拟VIA I/O的副作用
* 渲染LCD输出
* 遵循复位向量

---

## 测试检查清单

* 复位向量执行
* VIA寄存器写入
* LCD显示正确文本
* 堆栈操作有效
* ROM镜像正确映射

---

## 参考资料

* [MOS 6502 编程手册](http://archive.6502.org/datasheets/synertek_programming_manual.pdf)
* [MOS 6522 VIA数据手册](http://archive.6502.org/datasheets/mos_6522_preliminary_nov_1977.pdf)
* [AT28C256数据手册](https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/AT28C256-Industrial-Grade-256-Kbit-Paged-Parallel-EEPROM-Data-Sheet-DS20006386.pdf)
* [HD44780 LCD数据手册](https://www.futurlec.com/LED/LCD16X2BLa.shtml)
* [cc65工具链文档](https://cc65.github.io/doc/cc65.html)

---

## 说明

本规范有意采用**端到端**的方式：从汇编源代码到EEPROM镜像，再到运行中的硬件或模拟器。它定义了一个稳定的协议，使ROM、模拟器和实际单板计算机的行为保持一致。

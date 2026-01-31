# minipro 芯片编程工具规范

## 1. 概述

**minipro** 是一个开源的命令行工具，用于通过支持的通用编程器（如 **T48**、**TL866II Plus** 及兼容型号）对多种 **EEPROM、Flash、EPROM、SRAM、GAL 和逻辑器件** 进行 **编程、读取、擦除和验证**。

它广泛应用于 **Linux**、**macOS** 和 **Windows** 环境中，特别是在 **老式计算机**、**固件开发** 和 **电子原型设计** 领域。

---

## 2. 支持的编程器

| 编程器       | 说明                  |
| ------------ | ---------------------- |
| T48          | 完全支持（推荐使用）   |
| TL866II Plus | 完全支持               |
| TL866A / CS  | 有限/旧版支持           |

---

## 3. 支持的器件类型

### 3.1 存储器件

* 并行EEPROM（例如 AT28C256）
* Flash 存储器（29xxx 系列）
* EPROM（27xxx 系列）
* SRAM（仅支持读取/验证）

### 3.2 逻辑与可编程逻辑器件（PLD）

* GAL16V8 / GAL22V10
* PAL 器件（有限支持）

### 3.3 其他器件

* 部分微控制器（器件依赖）
* 逻辑集成电路测试（特定型号支持）

---

## 4. 安装

### 4.1 Linux

```bash
sudo apt install minipro
```

或从源代码编译：

```bash
git clone https://github.com/vdudouyt/minipro.git
make
sudo make install
```

### 4.2 Windows

* 通过 MSYS2 或预编译二进制文件安装
* 需要 USB 驱动程序（WinUSB）

---

## 5. 基本命令语法

```bash
minipro [选项]
```

常用选项：

| 选项         | 描述                |
| ------------ | ------------------ |
| `-p <device>` | 选择目标器件         |
| `-r <file>`   | 将器件内容读取到文件中 |
| `-w <file>`   | 将文件写入器件       |
| `-e`          | 擦除器件            |
| `-v`          | 验证内容            |
| `-I`          | 显示器件信息         |
| `-l`          | 列出支持的器件       |

---

## 6. 常见编程操作

### 6.1 列出支持的器件

```bash
minipro -l
```

### 6.2 识别器件

```bash
minipro -p AT28C256 -I
```

### 6.3 读取芯片

```bash
minipro -p AT28C256 -r rom_dump.bin
```

### 6.4 写入芯片

```bash
minipro -p AT28C256 -w rom.bin
```

### 6.5 仅验证

```bash
minipro -p AT28C256 -v rom.bin
```

---

## 7. 编程 EEPROM（以 AT28C256 为例）

```bash
minipro -p AT28C256 -w monitor.bin
```

* 软件数据保护由工具自动处理
* 写入周期延迟由工具内部管理
* 编程后会自动进行验证

---

## 8. 编程 Flash 存储器

```bash
minipro -p SST39SF040 -e -w firmware.bin
```

* Flash 器件需要先执行擦除步骤
* 扇区擦除由工具自动处理

---

## 9. EPROM 操作

```bash
minipro -p 27C256 -r eprom.bin
```

* 重新编程前需进行 UV 擦除
* minipro 在写入前会验证空白状态

---

## 10. GAL 编程

```bash
minipro -p GAL22V10 -w logic.jed
```

* 使用 JEDEC 文件
* 支持读取、写入和验证
* 通过 `-I` 可查看熔丝映射

---

## 11. 错误处理与提示信息

| 提示信息               | 含义                    |
| ---------------------- | ---------------------- |
| `Device not found`     | 选择的器件不正确         |
| `Verification failed`  | 数据不匹配               |
| `Chip protected`       | 写入保护已启用           |
| `Overcurrent detected` | 插入或接线错误            |

---

## 12. 安全与最佳实践

* 始终确认器件在 ZIF 插座中的方向
* 使用正确的器件标识符（`-p`）
* 在操作过程中不要热插拔芯片
* 使用适配器处理 PLCC、SOP、TSOP 封装

---

## 13. 典型的老式计算机工作流程

1. 组装 ROM 镜像
2. 使用 minipro + T48 编程 EEPROM
3. 验证内容
4. 将芯片安装到单板计算机（SBC）
5. 测试系统启动

---

## 14. 局限性

* 并非所有器件都支持
* 某些微控制器需要专有工具
* 不支持在电路编程（ISP）

---

## 15. 参考资料

* <https://gitlab.com/DavidGriffith/minipro>
* <https://www.hadex.cz/spec/m545b.pdf>
* <https://github.com/mikeroyal/Firmware-Guide>
* <https://mike42.me/blog/2021-08-a-first-look-at-programmable-logic>
* <https://retrocomputingforum.com/>

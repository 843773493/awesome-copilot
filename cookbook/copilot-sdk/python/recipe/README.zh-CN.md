# 可运行的食谱示例

此文件夹包含每个烹饪书食谱的独立、可执行的Python示例。每个文件都可以直接作为Python脚本运行。

## 前提条件

- Python 3.8或更高版本
- 安装依赖项（此操作会从PyPI安装SDK）：

```bash
pip install -r requirements.txt
```

## 运行示例

每个`.py`文件都是一个完整的、可运行的程序，并具有可执行权限：

```bash
python <filename>.py
# 或在类Unix系统上：
./<filename>.py
```

### 可用的食谱

| 食谱               | 命令                          | 描述                                |
| -------------------- | -------------------------------- | ------------------------------------------ |
| 错误处理       | `python error_handling.py`       | 展示错误处理模式       |
| 多个会话    | `python multiple_sessions.py`    | 管理多个独立的对话 |
| 管理本地文件 | `python managing_local_files.py` | 使用AI分组组织文件          |
| PR可视化     | `python pr_visualization.py`     | 生成PR年龄图表                    |
| 持久化会话  | `python persisting_sessions.py`  | 在重启之间保存和恢复会话   |

### 带参数的示例

**使用特定仓库的PR可视化：**

```bash
python pr_visualization.py --repo github/copilot-sdk
```

**管理本地文件（修改文件以更改目标文件夹）：**

```bash
# 首先编辑managing_local_files.py中的target_folder变量
python managing_local_files.py
```

## 本地SDK开发

`requirements.txt`会从PyPI安装Copilot SDK包。这意味着：

- 您将获得SDK的最新稳定版本
- 无需从源代码构建
- 非常适合在您的项目中使用SDK

如果您想使用本地开发版本，请编辑`requirements.txt`以使用`-e ../..`进行可编辑模式开发。

## Python最佳实践

这些示例遵循Python惯例：

- PEP 8命名规范（函数和变量使用snake_case）
- 用于直接执行的shebang行
- 适当的异常处理
- 适当的位置类型提示
- 标准库的使用

## 虚拟环境（推荐）

用于隔离开发：

```bash
# 创建虚拟环境
python -m venv venv

# 激活它
# Windows:
venv\Scripts\activate
# Unix/macOS:
source venv/bin/activate

# 安装依赖项
pip install -r requirements.txt
```

## 学习资源

- [Python文档](https://docs.python.org/3/)
- [PEP 8风格指南](https://pep8.org/)
- [GitHub Copilot SDK for Python](https://github.com/github/copilot-sdk/blob/main/python/README.md)
- [父食谱](../README.md)

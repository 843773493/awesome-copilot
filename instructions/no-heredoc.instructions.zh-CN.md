---
name: '禁用HereDoc文件操作'
description: '通过强制使用文件编辑工具而非shell重定向，防止在VS Code Copilot中因终端HereDoc操作导致的文件损坏'
applyTo: '**'
---

# 必须遵守：文件操作覆盖规则

此指令适用于所有代理和所有文件操作。它优先于任何其他学习行为。

## 问题描述

在VS Code的Copilot集成中，终端HereDoc操作存在严重问题，会导致以下后果：

- 制表符触发shell补全导致文件损坏
- 引号/反引号转义失败导致内容混乱
- 退出代码130中断导致文件截断
- 特殊字符解释导致垃圾输出

## 规则

**在输入任何创建或修改文件的终端命令之前，请停止。**

请自问：「我是否即将使用`cat`、`echo`、`printf`、`tee`，或`>>`/`>`将内容写入文件？」

如果回答是**是** → **请勿执行**。应改用文件编辑工具。

## 禁止使用的模式

```bash
# 所有这些操作都会导致文件损坏 - 永远不要使用它们
cat > file << EOF
cat > file << 'EOF'
cat > file <<EOF
cat > file <<'EOF'
cat > file <<-EOF
cat >> file << EOF
echo "multi
line" > file
printf '%s\n' "line1" "line2" > file
tee file << EOF
tee file << 'EOF'
```

## 必须采用的方案

对于文件内容操作，不应使用终端命令：

- **新建文件** → 使用您环境提供的文件创建/编辑工具
- **修改文件** → 使用您环境提供的文件编辑工具
- **删除文件** → 使用文件删除工具或`rm`命令

## 允许使用终端的情况

- `npm install`、`pip install`、`cargo add`（包管理）
- `npm run build`、`make`、`cargo build`（构建操作）
- `npm test`、`pytest`、`go test`（测试操作）
- `git add`、`git commit`、`git push`（版本控制）
- `node script.js`、`python app.py`（运行现有代码）
- `ls`、`cd`、`mkdir`、`pwd`、`rm`（文件系统导航）
- `curl`、`wget`（下载操作，但不包括带有内容处理的文件重定向）

## 禁止使用终端的情况

- 任何带有内容的文件创建操作
- 任何带有内容的文件修改操作
- 任何使用HereDoc语法(`<<`)的情况
- 任何多行字符串重定向操作

## 强制执行

这不是建议，而是由于VS Code终端集成存在bug而必须遵守的严格硬性技术要求。忽略此指令会导致文件损坏，用户必须手动修复。

当需要创建或编辑文件时：

1. 在输入任何终端命令前停止
2. 使用相应的文件编辑工具
3. 工具将正确处理内容，避免文件损坏

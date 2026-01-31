---
name: mcp-cli
description: 通过命令行界面（CLI）与MCP（模型上下文协议）服务器交互。当需要通过MCP服务器与外部工具、API或数据源进行交互、列出可用的MCP服务器/工具，或从命令行调用MCP工具时使用。
---

# MCP-CLI

通过命令行访问MCP服务器。MCP允许与外部系统（如GitHub、文件系统、数据库和API）进行交互。

## 命令

| 命令                            | 输出                          |
| ---------------------------------- | ------------------------------- |
| `mcp-cli`                          | 列出所有服务器和工具名称        |
| `mcp-cli <server>`                 | 显示带有参数的工具              |
| `mcp-cli <server>/<tool>`          | 获取工具的JSON模式              |
| `mcp-cli <server>/<tool> '<json>'` | 使用参数调用工具                |
| `mcp-cli grep "<glob>"`            | 按名称搜索工具                  |

**添加 `-d` 以包含描述信息**（例如：`mcp-cli filesystem -d`）

## 工作流程

1. **发现**：`mcp-cli` → 查看可用的服务器和工具
2. **探索**：`mcp-cli <server>` → 查看带有参数的工具
3. **检查**：`mcp-cli <server>/<tool>` → 获取完整的JSON输入模式
4. **执行**：`mcp-cli <server>/<tool> '<json>'` → 使用参数运行工具

## 示例

```bash
# 列出所有服务器和工具名称
mcp-cli

# 查看所有带有参数的工具
mcp-cli filesystem

# 包含描述信息（更详细）
mcp-cli filesystem -d

# 获取特定工具的JSON模式
mcp-cli filesystem/read_file

# 调用工具
mcp-cli filesystem/read_file '{"path": "./README.md"}'

# 搜索工具
mcp-cli grep "*file*"

# 用于解析的JSON输出
mcp-cli filesystem/read_file '{"path": "./README.md"}' --json

# 包含引号的复杂JSON（使用here文档或标准输入）
mcp-cli server/tool <<EOF
{"content": "Text with 'quotes' inside"}
EOF

# 或者从文件/命令管道输入
cat args.json | mcp-cli server/tool

# 查找所有TypeScript文件并读取第一个文件
mcp-cli filesystem/search_files '{"path": "src/", "pattern": "*.ts"}' --json | jq -r '.content[0].text' | head -1 | xargs -I {} sh -c 'mcp-cli filesystem/read_file "{\"path\": \"{}\"}"'
```

## 选项

| 标志         | 用途                   |
| ------------ | ------------------------- |
| `-j, --json` | 用于脚本的JSON输出         |
| `-r, --raw`  | 原始文本内容              |
| `-d`         | 包含描述信息              |

## 退出代码

- `0`: 成功
- `1`: 客户端错误（参数错误、配置缺失）
- `2`: 服务器错误（工具执行失败）
- `3`: 网络错误

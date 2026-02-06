# Penpot MCP 服务器设置与故障排除

Penpot MCP 服务器的安装、配置和故障排除完整指南。

## 架构概述

Penpot MCP 集成需要 **三个组件** 协同工作：

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   MCP 客户端    │────▶│   MCP 服务器    │◀───▶│  Penpot 插件  │
│ (VS Code/Claude)│     │  (端口 4401)    │     │ (浏览器中)    │
└─────────────────┘     └────────┬────────┘     └────────┬────────┘
                                 │                       │
                                 │    WebSocket          │
                                 │    (端口 4402)        │
                                 └───────────────────────┘
```

1. **MCP 服务器** - 向您的 AI 客户端暴露工具（HTTP，端口 4401）
2. **插件服务器** - 提供 Penpot 插件文件（HTTP，端口 4400）
3. **Penpot MCP 插件** - 在 Penpot 浏览器中运行，执行设计命令

## 先决条件

- **Node.js v22+** - [下载](https://nodejs.org/)
- **Git** - 用于克隆仓库
- **现代浏览器** - Chrome、Firefox 或基于 Chromium 的浏览器

验证 Node.js 安装：
```bash
node --version  # 应为 v22.x 或更高版本
npm --version
npx --version
```

## 安装

### 步骤 1：克隆并安装

```bash
# 克隆仓库
git clone https://github.com/penpot/penpot-mcp.git
cd penpot-mcp

# 安装依赖项
npm install
```

### 步骤 2：构建并启动服务器

```bash
# 构建所有组件并启动服务器
npm run bootstrap
```

此命令：

- 安装所有组件的依赖项
- 构建 MCP 服务器和插件
- 启动两个服务器（MCP 在 4401 端口，插件在 4400 端口）

**预期输出：**

```txt
MCP 服务器正在监听 http://localhost:4401
插件服务器正在监听 http://localhost:4400
WebSocket 服务器正在监听端口 4402
```

### 步骤 3：在 Penpot 中加载插件

1. 在浏览器中打开 [Penpot](https://design.penpot.app/)
2. 打开或创建一个设计文件
3. 进入 **插件** 菜单（或点击插件图标）
4. 点击 **从 URL 加载插件**
5. 输入：`http://localhost:4400/manifest.json`
6. 插件界面将出现 - 点击 **"连接到 MCP 服务器"**
7. 状态应更改为 **"已连接到 MCP 服务器"**

> **重要提示**：在使用 MCP 工具时，请保持插件界面打开。关闭它会导致与服务器断开连接。

### 步骤 4：配置您的 MCP 客户端

#### VS Code 与 GitHub Copilot

将以下内容添加到您的 VS Code `settings.json` 文件中：

```json
{
  "mcp": {
    "servers": {
      "penpot": {
        "url": "http://localhost:4401/sse"
      }
    }
  }
}
```

或使用 HTTP 端点：

```json
{
  "mcp": {
    "servers": {
      "penpot": {
        "url": "http://localhost:4401/mcp"
      }
    }
  }
}
```

#### Claude Desktop

Claude Desktop 需要 `mcp-remote` 代理（仅限 stdio 传输）：

1. 安装代理：

   ```bash
   npm install -g mcp-remote
   ```

2. 编辑 Claude Desktop 配置：
   - **macOS**：`~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**：`%APPDATA%/Claude/claude_desktop_config.json`
   - **Linux**：`~/.config/Claude/claude_desktop_config.json`

3. 添加 Penpot 服务器：

   ```json
   {
     "mcpServers": {
       "penpot": {
         "command": "npx",
         "args": ["-y", "mcp-remote", "http://localhost:4401/sse", "--allow-http"]
       }
     }
   }
   ```

4. **完全退出** Claude Desktop（文件 → 退出，而不是仅关闭窗口），然后重新启动

#### Claude Code（CLI）

```bash
claude mcp add penpot -t http http://localhost:4401/mcp
```

## 故障排除

### 连接问题

#### "插件无法连接到 MCP 服务器"

**症状**：插件显示 "未连接"，即使点击了连接按钮

**解决方案**：

1. 验证服务器是否正在运行：
   ```bash
   # 检查端口是否被占用
   lsof -i :4401  # MCP 服务器
   lsof -i :4402  # WebSocket
   lsof -i :4400  # 插件服务器
   ```

2. 重启服务器：

   ```bash
   # 在 penpot-mcp 目录中
   npm run start:all
   ```

3. 检查浏览器控制台（按 F12）中的 WebSocket 错误

#### 浏览器阻止本地连接

**症状**：浏览器拒绝从 Penpot 连接到 localhost

**原因**：Chromium 142+ 强制执行私有网络访问（PNA）限制

**解决方案**：

1. **Chrome/Chromium**：当提示时，允许访问本地网络
2. **Brave**：禁用 Penpot 网站的 Shield 功能：
   - 点击地址栏中的 Brave Shield 图标
   - 关闭此网站的 Shield 功能
3. **尝试 Firefox**：Firefox 不像 Chromium 那样严格执行这些限制

#### "WebSocket 连接失败"

**解决方案**：

1. 检查防火墙设置 - 允许端口 4400、4401、4402
2. 如果有活动的 VPN，请禁用
3. 检查是否有其他应用程序使用相同端口

### MCP 客户端问题

#### VS Code/Claude 中工具未显示

1. **验证端点**：

   ```bash
   # 测试 SSE 端点
   curl http://localhost:4401/sse
   
   # 测试 MCP 端点
   curl http://localhost:4401/mcp
   ```

2. **检查配置语法** - JSON 必须有效
3. **完全重启** MCP 客户端
4. **检查 MCP 服务器日志**：

   ```bash
   # 日志位于 mcp-server/logs/
   tail -f mcp-server/logs/mcp-server.log
   ```

#### "工具执行超时"

**原因**：插件已断开连接或操作耗时过长

**解决方案**：

1. 确保 Penpot 中插件界面保持打开状态
2. 验证插件显示 "已连接" 状态
3. 尝试重新连接：在插件中点击断开连接然后重新连接

### 插件问题

#### "插件加载失败"

1. 验证插件服务器是否在 4400 端口运行
2. 尝试直接在浏览器中访问 `http://localhost:4400/manifest.json`
3. 清除浏览器缓存并重新加载 Penpot
4. 卸载并重新安装插件

#### "找不到 penpot 对象"

**原因**：插件未正确初始化或未打开设计文件

**解决方案**：

1. 确保已打开设计文件（而不是仅打开仪表板）
2. 在打开文件后等待几秒钟再连接
3. 刷新 Penpot 并重新加载插件

### 服务器问题

#### 端口已被占用

```bash
# 查找使用端口的进程
lsof -i :4401

# 如需终止进程，请执行
kill -9 <PID>
```

或通过环境变量配置不同的端口：
```bash
PENPOT_MCP_SERVER_PORT=4501 npm run start:all
```

#### 服务器启动时崩溃

1. 检查 Node.js 版本（必须为 v22+）
2. 删除 `node_modules` 并重新安装：

   ```bash
   rm -rf node_modules
   npm install
   npm run bootstrap
   ```

## 配置参考

### 环境变量

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `PENPOT_MCP_SERVER_PORT` | 4401 | HTTP/SSE 服务器端口 |
| `PENPOT_MCP_WEBSOCKET_PORT` | 4402 | WebSocket 服务器端口 |
| `PENPOT_MCP_SERVER_LISTEN_ADDRESS` | localhost | 服务器绑定地址 |
| `PENPOT_MCP_LOG_LEVEL` | info | 日志级别（trace/debug/info/warn/error） |
| `PENPOT_MCP_LOG_DIR` | logs | 日志文件目录 |
| `PENPOT_MCP_REMOTE_MODE` | false | 启用远程模式（禁用文件系统访问） |

### 示例：自定义配置

```bash
# 使用不同端口并启用调试日志
PENPOT_MCP_SERVER_PORT=5000 \
PENPOT_MCP_WEBSOCKET_PORT=5001 \
PENPOT_MCP_LOG_LEVEL=debug \
npm run start:all
```

## 验证设置

运行以下检查清单以确认一切正常：

1. **服务器正在运行**：
   ```bash
   curl -s http://localhost:4401/sse | head -1
   # 应返回 SSE 流的头部信息
   ```

2. **插件已连接**：插件界面显示 "已连接到 MCP 服务器"

3. **工具可用**：在您的 MCP 客户端中验证以下工具是否出现：
   - `mcp__penpot__execute_code`
   - `mcp__penpot__export_shape`
   - `mcp__penpot__import_image`
   - `mcp__penpot__penpot_api_info`

4. **测试执行**：请您的 AI 助手运行一个简单命令：
   > "使用 Penpot 获取当前页面名称"

## 获取帮助

- **GitHub 问题**：[penpot/penpot-mcp/issues](https://github.com/penpot/penpot-mcp/issues)
- **GitHub 讨论**：[penpot/penpot-mcp/discussions](https://github.com/penpot/penpot-mcp/discussions)
- **Penpot 社区**：[community.penpot.app](https://community.penpot.app/)

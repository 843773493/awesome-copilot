# Microsoft 365 Copilot 插件的 TypeSpec 支持

构建使用 TypeSpec 进行 Microsoft 365 Copilot 扩展性的声明式代理和 API 插件的完整提示、指令和资源集合。

## 安装

```bash
# 使用 Copilot CLI
copilot plugin install typespec-m365-copilot@awesome-copilot
```

## 包含内容

### 命令（斜杠命令）

| 命令 | 描述 |
|------|------|
| `/typespec-m365-copilot:typespec-create-agent` | 生成一个完整的 TypeSpec 声明式代理，包含指令、功能和对话启动项，用于 Microsoft 365 Copilot |
| `/typespec-m365-copilot:typespec-create-api-plugin` | 生成一个 TypeSpec API 插件，包含 REST 操作、身份验证和 Adaptive 卡片（自适应卡片），用于 Microsoft 365 Copilot |
| `/typespec-m365-copilot:typespec-api-operations` | 向 TypeSpec API 插件添加 GET、POST、PATCH 和 DELETE 操作，包含正确的路由、参数和 Adaptive 卡片 |

## 来源

该插件是 [Awesome Copilot](https://github.com/github/awesome-copilot) 的一部分，这是一个社区驱动的 GitHub Copilot 扩展集合。

## 许可证

MIT

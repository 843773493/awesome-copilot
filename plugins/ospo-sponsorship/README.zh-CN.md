# 开源赞助插件

为开源项目办公室（OSPO）提供的工具和资源，用于通过 GitHub Sponsors、Open Collective 和其他资助平台识别、评估和管理开源依赖项的赞助。

## 安装

```bash
# 使用 Copilot CLI
copilot plugin install ospo-sponsorship@awesome-copilot
```

## 包含内容

### 技能

| 技能 | 描述 |
|-------|-------------|
| `SKILL.md` | 通过 GitHub Sponsors 查找某个 GitHub 仓库的依赖项中哪些可以进行赞助。使用 deps.dev API 解析 npm、PyPI、Cargo、Go、RubyGems、Maven 和 NuGet 等多个包管理器的依赖关系。检查 npm 资助元数据、FUNDING.yml 文件以及网络搜索。验证所有链接。显示直接和间接依赖项，并结合 OSSF Scorecard 健康数据。通过提供 GitHub 所有者/仓库名称（例如："在 expressjs/express 仓库中查找可赞助的依赖项"）来调用。 |

## 来源

此插件是 [Awesome Copilot](https://github.com/github/awesome-copilot) 的一部分，这是一个社区驱动的 GitHub Copilot 扩展集合。

## 许可证

MIT

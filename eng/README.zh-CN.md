# 贡献者报告（维护者）🚧

此目录包含一个轻量级辅助工具，用于生成关于缺失贡献者的可读报告。

- `contributor-report.mjs` — 为缺失贡献者生成合并的PRs的Markdown报告（包含共享辅助工具）。
- `add-missing-contributors.mjs` — 按需维护者脚本，自动将缺失贡献者添加到 `.all-contributorsrc`（从合并的PR文件推断贡献类型，然后运行 all-contributors CLI）。

## 维护者关键注意事项

- 报告是按需生成的，并输出到 `reports/contributor-report.md` 供人工审核。
- 报告输出有意保持简洁：仅包含受影响的PR列表和一个添加缺失贡献者的命令。
- 此仓库需要完整的Git历史记录以进行准确分析。在CI中，请设置 `fetch-depth: 0`。
- 链接：[all-contributors CLI文档](https://allcontributors.org/docs/en/cli)

## 按需脚本（非CI）

这些是维护者工具。它们仅限按需使用（但未来可能接入CI）。

### `add-missing-contributors.mjs`

- 目的：检测缺失贡献者，从其合并的PR文件中推断贡献类型，并运行 `npx all-contributors add ...` 来更新 `.all-contributorsrc` 文件。
- 要求：
	- GitHub CLI (`gh`) 已安装（用于查询合并的PR）。
	- `.all-contributorsrc` 文件存在。
	- 设置认证令牌以避免GitHub的匿名请求限制：
		- 建议设置 `GITHUB_TOKEN`，或为 `gh` CLI 设置 `GH_TOKEN`。
		- 如果您本地使用 `PRIVATE_TOKEN`，`contributor-report.mjs` 会将其映射为 `GITHUB_TOKEN`。

## 平滑关闭

- `contributor-report.mjs` 在文件早期调用 `eng/utils/graceful-shutdown.mjs` 中的 `setupGracefulShutdown('脚本名称')`，以附加信号/异常处理程序。

## 测试与维护

- 辅助函数具有小型、确定性的行为，并包含JSDoc注释。
- `contributor-report.mjs` 中的 `getMissingContributors` 函数是检测 `all-contributors check` 输出中缺失贡献者的唯一数据来源。

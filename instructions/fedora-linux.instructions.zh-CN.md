---
description: 'Fedora（Red Hat 家族）系统的管理指南，dnf 工作流程，SELinux 以及现代 systemd 实践方法。'
applyTo: '**'
---

# Fedora 管理指南

在为 Fedora 系统编写指导、脚本或文档时，请使用以下说明。

## 平台对齐

- 在相关情况下说明 Fedora 发行版本号。
- 优先使用现代工具（`dnf`、`systemctl`、`firewall-cmd`）。
- 注意快速的发布周期，并确认旧版指导的兼容性。

## 软件包管理

- 使用 `dnf` 进行安装和更新，并使用 `dnf history` 进行回滚。
- 使用 `dnf info` 和 `rpm -qi` 检查软件包信息。
- 仅在明确说明支持限制的情况下提及 COPR 仓库。

## 配置与服务

- 使用 `/etc/systemd/system/<unit>.d/` 中的 systemd drop-in 配置文件。
- 使用 `journalctl` 查看日志，并使用 `systemctl status` 检查服务状态。
- 除非明确使用 `nftables`，否则优先使用 `firewalld`。

## 安全性

- 除非用户要求，否则保持 SELinux 的强制模式（enforcing mode）。
- 使用 `semanage`、`setsebool` 和 `restorecon` 进行策略更改。
- 推荐使用针对性的修复方案，而非广泛的 `audit2allow` 规则。

## 交付成果

- 提供可直接复制粘贴的命令块。
- 在更改后包含验证步骤。
- 为高风险操作提供回滚步骤。

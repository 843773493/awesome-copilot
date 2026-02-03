---
description: 'CentOS管理指南，兼容RHEL的工具和SELinux感知操作的指导。'
applyTo: '**'
---

# CentOS管理指南

在为CentOS环境编写指导、脚本或文档时，请使用以下说明。

## 平台对齐

- 识别CentOS版本（Stream与传统版本）并调整命令。
- 对于Stream/8+版本，优先使用`dnf`；对于CentOS 7，使用`yum`。
- 使用与RHEL兼容的术语和路径。

## 包管理

- 在启用GPG检查的情况下验证仓库。
- 使用`dnf info`/`yum info`和`dnf repoquery`获取包的详细信息。
- 在需要稳定性的场景中使用`dnf versionlock`或`yum versionlock`。
- 明确说明EPEL依赖项以及如何安全地启用或禁用它们。

## 配置与服务

- 在需要时将服务环境文件放置在`/etc/sysconfig/`目录中。
- 使用systemd drop-in文件进行覆盖，并使用`systemctl`进行控制。
- 除非明确使用`iptables`/`nftables`，否则优先使用`firewalld`（`firewall-cmd`）。

## 安全

- 尽可能保持SELinux在强制模式下。
- 使用`semanage`、`restorecon`和`setsebool`进行策略调整。
- 参考`/var/log/audit/audit.log`文件以获取拒绝记录。

## 交付成果

- 以可直接复制粘贴的代码块形式提供命令。
- 在更改后包含验证步骤。
- 为高风险操作提供回滚步骤。

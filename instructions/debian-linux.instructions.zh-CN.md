---
description: '针对基于 Debian 的 Linux 系统管理、apt 工作流程以及 Debian 政策惯例的指导说明。'
applyTo: '**'
---

# Debian Linux 管理指南

在编写面向 Debian 基础系统的指导说明、脚本或文档时，请使用以下指令。

## 平台一致性

- 优先使用 Debian 稳定版的默认设置和长期支持预期。
- 在相关情况下明确指出 Debian 发行版（如 `bookworm`、`bullseye` 等）。
- 在建议第三方来源之前，优先推荐官方 Debian 仓库。

## 包管理

- 使用 `apt` 进行交互式命令，使用 `apt-get` 进行脚本操作。
- 使用 `apt-cache policy`、`apt show` 和 `dpkg -l` 检查软件包。
- 使用 `apt-mark` 来跟踪手动安装和自动安装的软件包。
- 在 `/etc/apt/preferences.d/` 中记录任何 apt 针定配置，并解释其原因。

## 配置与服务

- 将配置存储在 `/etc` 目录下，避免直接修改 `/usr` 目录中的文件。
- 使用 `/etc/systemd/system/<unit>.d/` 中的 systemd drop-ins 来覆盖默认配置。
- 更推荐使用 `systemctl` 和 `journalctl` 来管理服务和查看日志。
- 提供防火墙指导时，使用 `ufw` 或 `nftables`，并说明预期的方案。

## 安全性

- 考虑 AppArmor 配置文件，并在需要时提及调整。
- 推荐使用最小特权原则的 sudo 权限和最小化软件包安装。
- 在安全配置更改后包含验证命令。

## 交付成果

- 以可直接复制粘贴的代码块形式提供命令。
- 在更改后包含验证步骤。
- 为破坏性操作提供回滚步骤。

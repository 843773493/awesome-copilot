---
name: nano-banana-pro-openrouter
description: '通过 OpenRouter 使用 Gemini 3 Pro Image 模型生成或编辑图像。适用于仅提示生成、单图编辑和多图合成；支持 1K/2K/4K 输出。'
metadata:
  emoji: 🍌
  requires:
    bins:
      - uv
    env:
      - OPENROUTER_API_KEY
  primaryEnv: OPENROUTER_API_KEY
---

# Nano Banana Pro OpenRouter

## 概述

使用 `google/gemini-3-pro-image-preview` 模型通过 OpenRouter 生成或编辑图像。支持仅提示生成、单图编辑和多图合成。

### 仅提示生成

```
uv run {baseDir}/scripts/generate_image.py \
  --prompt "一场电影感的雪山日落" \
  --filename sunset.png
```

### 编辑单张图像

```
uv run {baseDir}/scripts/generate_image.py \
  --prompt "将天空替换为壮观的极光" \
  --input-image input.jpg \
  --filename aurora.png
```

### 合成多张图像

```
uv run {baseDir}/scripts/generate_image.py \
  --prompt "将主体合成到一张 studio 风格的肖像中" \
  --input-image face1.jpg \
  --input-image face2.jpg \
  --filename composite.png
```

## 分辨率

- 使用 `--resolution` 参数指定 `1K`、`2K` 或 `4K`。
- 若未指定，默认使用 `1K`。

## 系统提示自定义

该功能从 `assets/SYSTEM_TEMPLATE` 读取可选的系统提示。这允许您在不修改代码的情况下自定义图像生成行为。

## 行为与限制

- 通过重复使用 `--input-image` 参数接受最多 3 张输入图像。
- `--filename` 参数支持相对路径（保存到当前目录）或绝对路径。
- 如果返回多张图像，会在文件名后追加 `-1`、`-2` 等数字。
- 每保存一张图像，打印 `MEDIA: <路径>`。不要将图像重新读取到响应中。

## 故障排除

如果脚本退出状态非零，请检查标准错误输出是否与以下常见问题相关：

| 问题 | 解决方案 |
|------|----------|
| `OPENROUTER_API_KEY is not set` | 请要求用户设置该密钥。PowerShell: `$env:OPENROUTER_API_KEY = "sk-or-..."` / bash: `export OPENROUTER_API_KEY="sk-or-..."` |
| `uv: command not found` 或未被识别 | macOS/Linux: <code>curl -LsSf https://astral.sh/uv/install.sh &#124; sh</code>。Windows: <code>powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 &#124; iex"</code>。然后重启终端。 |
| `AuthenticationError` / HTTP 401 | 密钥无效或已用完信用额度。请在 <https://openrouter.ai/settings/keys> 验证。 |

对于临时错误（HTTP 429、网络超时），请在 30 秒后重试一次。不要对同一错误重试超过两次——应将问题反馈给用户。

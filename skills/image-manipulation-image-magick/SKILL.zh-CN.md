---
名称：image-manipulation-image-magick
描述：使用 ImageMagick 处理和操作图像。支持调整大小、格式转换、批量处理以及获取图像元数据。在处理图像、创建缩略图、调整壁纸大小或执行批量图像操作时使用。
兼容性：需要已安装并可通过 `magick` 命令在 PATH 中访问 ImageMagick。提供了适用于 PowerShell（Windows）和 Bash（Linux/macOS）的跨平台示例。
---

# 使用 ImageMagick 进行图像处理

此技能可在 Windows、Linux 和 macOS 系统上实现图像处理和操作任务。

## 使用此技能的场景

当您需要以下操作时，请使用此技能：

- 调整图像大小（单张或批量）
- 获取图像尺寸和元数据
- 在不同图像格式之间进行转换
- 创建缩略图
- 为不同屏幕尺寸处理壁纸
- 根据特定条件批量处理多个图像

## 先决条件

- 系统上已安装 ImageMagick
- **Windows**：使用 PowerShell，ImageMagick 应作为 `magick` 命令在 PATH 中可用（或位于 `C:\Program Files\ImageMagick-*\magick.exe`）
- **Linux/macOS**：使用 Bash，通过包管理器（如 `apt`、`brew` 等）安装 ImageMagick

## 核心功能

### 1. 图像信息

- 获取图像尺寸（宽度 x 高度）
- 提取详细元数据（格式、颜色空间等）
- 识别图像格式

### 2. 图像调整大小

- 调整单张图像大小
- 批量调整多张图像大小
- 创建指定尺寸的缩略图
- 保持宽高比

### 3. 批量处理

- 根据尺寸处理图像
- 过滤并处理特定文件类型
- 对多个文件应用转换操作

## 使用示例

### 示例 0：解析 `magick` 可执行文件

**PowerShell（Windows）：**
```powershell
# 优先使用 PATH 中的 ImageMagick
$magick = (Get-Command magick -ErrorAction SilentlyContinue)?.Source

# 备选方案：常见安装路径在 Program Files 下
if (-not $magick) {
    $magick = Get-ChildItem "C:\\Program Files\\ImageMagick-*\\magick.exe" -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
}

if (-not $magick) {
    throw "未找到 ImageMagick。请安装它或将 'magick' 添加到 PATH 中。"
}
```

**Bash（Linux/macOS）：**
```bash
# 检查 magick 是否在 PATH 中可用
if ! command -v magick &> /dev/null; then
    echo "未找到 ImageMagick。请使用包管理器安装："
    echo "  Ubuntu/Debian: sudo apt install imagemagick"
    echo "  macOS: brew install imagemagick"
    exit 1
fi
```

### 示例 1：获取图像尺寸

**PowerShell（Windows）：**
```powershell
# 获取单张图像的尺寸
& $magick identify -format "%wx%h" path/to/image.jpg

# 获取多张图像的尺寸
Get-ChildItem "path/to/images/*" | ForEach-Object { 
    $dimensions = & $magick identify -format "%f: %wx%h`n" $_.FullName
    Write-Host $dimensions 
}
```

**Bash（Linux/macOS）：**
```bash
# 获取单张图像的尺寸
magick identify -format "%wx%h" path/to/image.jpg

# 获取多张图像的尺寸
for img in path/to/images/*; do
    magick identify -format "%f: %wx%h\n" "$img"
done
```

### 示例 2：调整图像大小

**PowerShell（Windows）：**
```powershell
# 调整单张图像大小
& $magick input.jpg -resize 427x240 output.jpg

# 批量调整图像大小
Get-ChildItem "path/to/images/*" | ForEach-Object { 
    & $magick $_.FullName -resize 427x240 "path/to/output/thumb_$($_.Name)"
}
```

**Bash（Linux/macOS）：**
```bash
# 调整单张图像大小
magick input.jpg -resize 427x240 output.jpg

# 批量调整图像大小
for img in path/to/images/*; do
    filename=$(basename "$img")
    magick "$img" -resize 427x240 "path/to/output/thumb_$filename"
done
```

### 示例 3：获取详细图像信息

**PowerShell（Windows）：**
```powershell
# 获取图像的详细信息
& $magick identify -verbose path/to/image.jpg
```

**Bash（Linux/macOS）：**
```bash
# 获取图像的详细信息
magick identify -verbose path/to/image.jpg
```

### 示例 4：根据尺寸处理图像

**PowerShell（Windows）：**
```powershell
Get-ChildItem "path/to/images/*" | ForEach-Object { 
    $dimensions = & $magick identify -format "%w,%h" $_.FullName
    if ($dimensions) {
        $width,$height = $dimensions -split ','
        if ([int]$width -eq 2560 -or [int]$height -eq 1440) {
            Write-Host "正在处理 $($_.Name)"
            & $magick $_.FullName -resize 427x240 "path/to/output/thumb_$($_.Name)"
        }
    }
}
```

**Bash（Linux/macOS）：**
```bash
for img in path/to/images/*; do
    dimensions=$(magick identify -format "%w,%h" "$img")
    if [[ -n "$dimensions" ]]; then
        width=$(echo "$dimensions" | cut -d',' -f1)
        height=$(echo "$dimensions" | cut -d',' -f2)
        if [[ "$width" -eq 2560 || "$height" -eq 1440 ]]; then
            filename=$(basename "$img")
            echo "正在处理 $filename"
            magick "$img" -resize 427x240 "thumbnails/thumb_$filename"
        fi
    fi
done
```

## 使用指南

1. **始终使用引号包裹文件路径** - 对可能包含空格的文件路径使用引号
2. **使用 `&` 运算符（PowerShell）** - 在 PowerShell 中使用 `&` 来调用 magick 可执行文件
3. **将路径存储在变量中（PowerShell）** - 将 ImageMagick 路径赋值给 `$magick` 以实现更清晰的代码
4. **使用循环** - 处理多个文件时，使用 `ForEach-Object`（PowerShell）或 `for` 循环（Bash）
5. **先验证尺寸** - 在处理前检查图像尺寸以避免不必要的操作
6. **使用适当的调整大小标志** - 考虑使用 `!` 强制精确尺寸或 `^` 用于最小尺寸

## 常见模式

### PowerShell 模式

#### 模式：存储 ImageMagick 路径

```powershell
$magick = (Get-Command magick).Source
```

#### 模式：获取尺寸作为变量

```powershell
$dimensions = & $magick identify -format "%w,%h" $_.FullName
$width,$height = $dimensions -split ','
```

#### 模式：条件处理

```powershell
if ([int]$width -gt 1920) {
    & $magick $_.FullName -resize 1920x1080 $outputPath
}
```

#### 模式：创建缩略图

```powershell
& $magick $_.FullName -resize 427x240 "thumbnails/thumb_$($_.Name)"
```

### Bash 模式

#### 模式：检查 ImageMagick 安装

```bash
command -v magick &> /dev/null || { echo "需要 ImageMagick"; exit 1; }
```

#### 模式：获取尺寸作为变量

```bash
dimensions=$(magick identify -format "%w,%h" "$img")
width=$(echo "$dimensions" | cut -d',' -f1)
height=$(echo "$dimensions" | cut -d',' -f2)
```

#### 模式：条件处理

```bash
if [[ "$width" -gt 1920 ]]; then
    magick "$img" -resize 1920x1080 "$outputPath"
fi
```

#### 模式：创建缩略图

```bash
filename=$(basename "$img")
magick "$img" -resize 427x240 "thumbnails/thumb_$filename"
```

## 局限性

- 大型批量操作可能占用大量内存
- 某些复杂操作可能需要额外的 ImageMagick 代理程序
- 在较旧的 Linux 系统上，请使用 `convert` 而不是 `magick`（ImageMagick 6.x 与 7.x 的区别）

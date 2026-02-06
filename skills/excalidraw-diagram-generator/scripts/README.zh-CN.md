# Excalidraw 库工具

此目录包含用于处理 Excalidraw 库的脚本。

## split-excalidraw-library.py

将 Excalidraw 库文件（`*.excalidrawlib`）拆分为单独的图标 JSON 文件，以提高 AI 助手的令牌使用效率。

### 依赖项

- Python 3.6 或更高版本
- 不需要其他依赖项（仅使用标准库）

### 使用方法

```bash
python split-excalidraw-library.py <库目录路径>
```

### 分步工作流程

1. **创建库目录**：
   ```bash
   mkdir -p skills/excalidraw-diagram-generator/libraries/aws-architecture-icons
   ```

2. **下载并放置库文件**：
   - 访问：https://libraries.excalidraw.com/
   - 搜索 "AWS Architecture Icons" 并下载 `.excalidrawlib` 文件
   - 将其重命名为与目录名匹配：`aws-architecture-icons.excalidrawlib`
   - 将其放置在第 1 步创建的目录中

3. **运行脚本**：
   ```bash
   python skills/excalidraw-diagram-generator/scripts/split-excalidraw-library.py skills/excalidraw-diagram-generator/libraries/aws-architecture-icons/
   ```

### 输出结构

脚本在库目录中创建以下结构：

```
skills/excalidraw-diagram-generator/libraries/aws-architecture-icons/
  aws-architecture-icons.excalidrawlib  # 原始文件（保留）
  reference.md                          # 生成：快速参考表
  icons/                                # 生成：单独的图标文件
    API-Gateway.json
    CloudFront.json
    EC2.json
    S3.json
    ...
```

### 脚本功能

1. **读取** `.excalidrawlib` 文件
2. **提取** `libraryItems` 数组中的每个图标
3. **清理** 图标名称以创建有效的文件名（空格 → 连字符，移除特殊字符）
4. **保存** 每个图标为 `icons/` 目录中的单独 JSON 文件
5. **生成** 一个 `reference.md` 文件，将图标名称映射到文件名

### 优势

- **令牌效率**：AI 可首先读取轻量级的 `reference.md` 文件以查找相关图标，然后仅加载所需的特定图标文件
- **组织性**：图标以清晰的目录结构进行组织
- **可扩展性**：用户可将多个库集并排添加

### 推荐工作流程

1. 从 https://libraries.excalidraw.com/ 下载所需的 Excalidraw 库
2. 对每个库文件运行此脚本
3. 将生成的文件夹移动到 `../libraries/`
4. AI 助手将使用 `reference.md` 文件高效定位和使用图标

### 库来源（示例 — 请验证可用性）

- 示例可能包含云/服务图标集，见 https://libraries.excalidraw.com/
- 可用性会随时间变化；使用前请在网站上确认确切的库名称
- 此脚本适用于您提供的任何有效的 `.excalidrawlib` 文件

### 故障排除

**错误：文件未找到**
- 检查文件路径是否正确
- 确保文件具有 `.excalidrawlib` 扩展名

**错误：无效的库文件格式**
- 确保文件是有效的 Excalidraw 库文件
- 检查文件是否包含 `libraryItems` 数组

### 许可证注意事项

使用第三方图标库时：
- **AWS Architecture Icons**：受 AWS 内容许可协议约束
- **GCP Icons**：受 Google 的条款约束
- **其他库**：请检查每个库的许可证

此脚本仅供个人/组织使用。拆分后的图标文件的再分发应遵守原始库的许可证条款。

## add-icon-to-diagram.py

将拆分后的 Excalidraw 库中的特定图标添加到现有的 `.excalidraw` 图表中。该脚本处理坐标转换和 ID 冲突避免，并可选择性地在图标下方添加标签。

### 依赖项

- Python 3.6 或更高版本
- 一个图表文件（`.excalidraw`）
- 一个拆分后的图标库目录（由 `split-excalidraw-library.py` 创建）

### 使用方法

```bash
python add-icon-to-diagram.py <图表路径> <图标名称> <x> <y> [选项]
```

**选项**
- `--library-path PATH` : 图标库目录路径（默认：`aws-architecture-icons`）
- `--label TEXT` : 在图标下方添加文本标签
- `--use-edit-suffix` : 通过 `.excalidraw.edit` 编辑以避免编辑器覆盖问题（默认启用；通过 `--no-use-edit-suffix` 禁用）

### 示例

```bash
# 在位置 (400, 300) 添加 EC2 图标
python add-icon-to-diagram.py diagram.excalidraw EC2 400 300

# 添加带有标签的 VPC 图标
python add-icon-to-diagram.py diagram.excalidraw VPC 200 150 --label "VPC"

# 默认启用安全编辑模式（避免编辑器覆盖问题）
# 使用 `--no-use-edit-suffix` 禁用
python add-icon-to-diagram.py diagram.excalidraw EC2 500 300

# 从另一个库添加图标
python add-icon-to-diagram.py diagram.excalidraw Compute-Engine 500 200 \
   --library-path libraries/gcp-icons --label "API Server"
```

### 脚本功能

1. **加载** 图标 JSON 文件（从库的 `icons/` 目录）
2. **计算** 图标的边界框
3. **偏移** 所有坐标到目标位置
4. **生成** 所有元素和组的唯一 ID
5. **追加** 转换后的元素到图表
6. **（可选）** 在图标下方添加标签

---

## add-arrow.py

在现有的 `.excalidraw` 图表中添加一条直线箭头。支持可选标签和线样式。

### 依赖项

- Python 3.6 或更高版本
- 一个图表文件（`.excalidraw`）

### 使用方法

```bash
python add-arrow.py <图表路径> <起点x> <起点y> <终点x> <终点y> [选项]
```

**选项**
- `--style {solid|dashed|dotted}` : 线样式（默认：`solid`）
- `--color HEX` : 箭头颜色（默认：`#1e1e1e`）
- `--label TEXT` : 在箭头上添加文本标签
- `--use-edit-suffix` : 通过 `.excalidraw.edit` 编辑以避免编辑器覆盖问题（默认启用；通过 `--no-use-edit-suffix` 禁用）

### 示例

```bash
# 添加简单箭头
python add-arrow.py diagram.excalidraw 300 200 500 300

# 添加带有标签的箭头
python add-arrow.py diagram.excalidraw 300 200 500 300 --label "HTTPS"

# 添加虚线箭头并自定义颜色
python add-arrow.py diagram.excalidraw 400 350 600 400 --style dashed --color "#7950f2"

# 默认启用安全编辑模式（避免编辑器覆盖问题）
# 使用 `--no-use-edit-suffix` 禁用
python add-arrow.py diagram.excalidraw 300 200 500 300
```

### 脚本功能

1. **根据给定坐标创建** 箭头元素
2. **（可选）** 在箭头中点附近添加标签
3. **追加** 元素到图表
4. **保存** 更新后的文件

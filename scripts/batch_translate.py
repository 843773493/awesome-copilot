#!/usr/bin/env python3
"""
批量翻译脚本：遍历项目中所有的.md文件，为缺少中文版(zh-CN.md)的文件生成翻译版本
使用并发请求加速翻译过程
"""

import os
import sys
from pathlib import Path
from typing import List

# Add scripts directory to path to import translate module
sys.path.insert(0, str(Path(__file__).parent))
from translate import TranslationConfig, MarkdownTranslator

def get_all_markdown_files(root_path: str) -> List[Path]:
    """
    获取所有需要翻译的.md文件（排除zh-CN.md和其他已翻译版本）

    Args:
        root_path: 项目根路径

    Returns:
        需要翻译的.md文件列表
    """
    root = Path(root_path)
    files_to_translate = []

    for md_file in root.rglob('*.md'):
        # 跳过zh-CN.md文件和其他语言版本
        if any(suffix in md_file.name for suffix in ['.zh-CN.md', '.zh-cn.md', '.en.md']):
            continue

        # 检查是否已存在中文版本
        stem = md_file.stem
        parent = md_file.parent
        chinese_filename = f"{stem}.zh-CN.md"
        chinese_path = parent / chinese_filename

        # 只添加未翻译的文件
        if not chinese_path.exists():
            files_to_translate.append(md_file)

    return sorted(files_to_translate)

def main():
    """主函数"""

    # 验证API Key
    api_key = os.getenv("DEFAULT_API_KEY")
    if not api_key:
        print("错误: 环境变量 DEFAULT_API_KEY 未设置")
        print("   请设置 DEFAULT_API_KEY 环境变量")
        sys.exit(1)

    # 获取项目根路径
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    print("=" * 70)
    print("批量翻译脚本 - 使用并发请求加速")
    print("=" * 70)
    print(f"项目根路径: {project_root}\n")

    # 获取所有需要翻译的.md文件
    files_to_translate = get_all_markdown_files(str(project_root))

    if not files_to_translate:
        print("✓ 所有.md文件都已有中文版本，无需翻译")
        return

    print(f"找到 {len(files_to_translate)} 个需要翻译的文件\n")

    # 获取相对路径用于显示
    file_paths_str = [str(f) for f in files_to_translate]

    # 创建翻译器并执行并发翻译
    config = TranslationConfig()
    translator = MarkdownTranslator(config)

    print(f"开始并发翻译（最大并发数: {config.max_concurrent}）:\n")
    results = translator.batch_translate(file_paths_str)

    # 统计结果
    successful = sum(1 for r in results if r and r.get("success"))
    failed = sum(1 for r in results if r and not r.get("success"))

    # 输出总结
    print("\n" + "=" * 70)
    print("翻译完成统计:")
    print(f"   成功: {successful}/{len(files_to_translate)}")
    print(f"   失败: {failed}/{len(files_to_translate)}")

    # 显示失败的文件
    if failed > 0:
        print("\n失败的文件:")
        for i, result in enumerate(results):
            if result and not result.get("success"):
                file_name = Path(files_to_translate[i]).relative_to(project_root)
                error = result.get("error", "未知错误")
                print(f"   - {file_name}: {error}")

    # 显示token使用统计
    total_tokens = sum(
        r.get("tokens_used", {}).get("total", 0)
        for r in results if r and r.get("success")
    )
    if total_tokens > 0:
        print(f"\n总Token使用: {total_tokens}")

    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断了翻译过程")
        sys.exit(1)
    except Exception as e:
        print(f"\n致命错误: {e}")
        sys.exit(1)

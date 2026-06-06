#!/usr/bin/env python3
"""
LiteParse Python Demo
=====================
展示如何使用 liteparse Python 包进行文档解析。

安装: pip install liteparse
文档: https://developers.llamaindex.ai/liteparse/
上游: https://github.com/run-llama/liteparse
"""

import json
import sys
from pathlib import Path

# 检查是否已安装 liteparse
try:
    from liteparse import LiteParse
except ImportError:
    print("❌ liteparse 未安装，请先运行: pip install liteparse")
    sys.exit(1)


def demo_basic_parse(parser: LiteParse, file_path: str):
    """基础解析演示"""
    print("\n" + "=" * 60)
    print("📄 基础解析 (parse)")
    print("=" * 60)

    result = parser.parse(file_path)
    print(f"\n✅ 解析完成，共 {len(result.pages)} 页")
    print(f"\n📝 文本内容预览 (前500字符):")
    print("-" * 40)
    print(result.text[:500] if len(result.text) > 500 else result.text)


def demo_json_parse(parser: LiteParse, file_path: str):
    """JSON格式解析演示（含边界框）"""
    print("\n" + "=" * 60)
    print("📐 JSON解析 (含边界框信息)")
    print("=" * 60)

    result = parser.parse_to_json(file_path)

    # 展示第一页的blocks结构
    if result.pages:
        page = result.pages[0]
        print(f"\n📑 第 {page.page_number} 页 (尺寸: {page.width}x{page.height})")
        print(f"   文本块数量: {len(page.blocks)}")

        if page.blocks:
            print("\n   前3个文本块示例:")
            for i, block in enumerate(page.blocks[:3]):
                print(f"\n   块 {block.id}:")
                print(f"文本: {block.text[:80]}{'...' if len(block.text) > 80 else ''}")
                print(f"   边界框: x={block.bbox.x}, y={block.bbox.y}, "
                      f"w={block.bbox.width}, h={block.bbox.height}")
                print(f"   字体大小: {block.font_size}")


def demo_specific_pages(parser: LiteParse, file_path: str):
    """指定页面解析"""
    print("\n" + "=" * 60)
    print("🎯 指定页面解析 (1-5, 10, 15-20)")
    print("=" * 60)

    result = parser.parse(file_path, target_pages="1-5,10,15-20")
    print(f"\n✅ 指定页面解析完成，共 {len(result.pages)} 页")


def demo_no_ocr(parser: LiteParse, file_path: str):
    """禁用OCR解析"""
    print("\n" + "=" * 60)
    print("🔇 禁用OCR解析")
    print("=" * 60)

    result = parser.parse(file_path, no_ocr=True)
    print(f"\n✅ 纯文本提取完成 (不调用OCR)，共 {len(result.pages)} 页")


def demo_screenshot(parser: LiteParse, file_path: str, output_dir: str):
    """生成页面截图"""
    print("\n" + "=" * 60)
    print("🖼️ 生成页面截图 (DPI=150)")
    print("=" * 60)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 解析前3页并生成截图
    result = parser.screenshot(file_path, output_dir=output_dir, dpi=150, target_pages="1-3")
    print(f"\n✅ 截图生成完成，共 {len(result.screenshots)} 张")


def demo_batch_parse(parser: LiteParse, input_dir: str, output_dir: str):
    """批量解析目录"""
    print("\n" + "=" * 60)
    print("📂 批量解析目录")
    print("=" * 60)

    results = parser.batch_parse(input_dir, output_dir, format="json", recursive=True)
    print(f"\n✅ 批量解析完成，共处理 {len(results)} 个文件")
    for r in results:
        print(f"   ✅ {r.filename} → {r.output_path}")


def main():
    """主函数"""
    print("🚀 LiteParse Python Demo")
    print("=" * 40)
    print("上游: https://github.com/run-llama/liteparse")
    print("星标: 9,285 (本周 +2,380)")
    print("=" * 40)

    # 初始化解析器
    parser = LiteParse()

    # 示例文件路径（替换为你的实际文件）
    demo_file = "sample.pdf"
    demo_output = "./liteparse_output"
    demo_screenshots = "./liteparse_screenshots"

    if not Path(demo_file).exists():
        print(f"\n⚠️  示例文件 '{demo_file}' 不存在")
        print("   请替换为实际 PDF 文件路径后运行")
        print("\n📌 可用方法一览:")
        print("   parser.parse(file)                      # 基础解析")
        print("   parser.parse_to_json(file)             # JSON解析")
        print("   parser.parse(file, target_pages='1-5') # 指定页面")
        print("   parser.parse(file, no_ocr=True)        # 禁用OCR")
        print("   parser.screenshot(file, output_dir)     # 生成截图")
        print("   parser.batch_parse(indir, outdir)       # 批量解析")
        return

    # 运行各演示
    demo_basic_parse(parser, demo_file)
    demo_json_parse(parser, demo_file)
    demo_specific_pages(parser, demo_file)
    demo_no_ocr(parser, demo_file)
    demo_screenshot(parser, demo_file, demo_screenshots)

    print("\n" + "=" * 60)
   print("🎉 所有演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
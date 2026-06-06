# LiteParse Wrap

>🚀 **LiteParse** — Rust 实现的高性能开源文档解析器，快速、精准、本地运行

[![Stars](https://img.shields.io/github/stars/run-llama/liteparse?style=flat&color=ff8700)](https://github.com/run-llama/liteparse)
[![License](https://img.shields.io/github/license/run-llama/liteparse)](https://opensource.org/licenses/Apache-2.0)
[![Rust](https://img.shields.io/badge/Rust-1.75%2B-orange)](https://www.rust-lang.org/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://pypi.org/project/liteparse/)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)](https://www.npmjs.com/package/@llamaindex/liteparse)

[English](#english) · [中文](#中文) · [快速开始](#快速开始) · [示例代码](#示例代码) · [架构概览](#架构概览)

---

## 中文

###是什么？

**LiteParse** 是 [run-llama/liteparse](https://github.com/run-llama/liteparse) 的 Python/Rust 封装包。它是一个完全本地运行的开源文档解析工具，专注于**快速、轻量的空间文本解析**，输出包含精确边界框（bounding box）的高质量结构化数据。

### 核心特性

| 特性 | 说明 |
|------|------|
| ⚡ **极速解析** | PDFium C 库驱动，空间文本提取，无需 LLM |
| 🔍 **灵活 OCR** | 内置 Tesseract（零配置），也支持 EasyOCR / PaddleOCR 等 HTTP OCR 服务 |
| 📐 **精确边界框** | 每个文本块均有坐标信息，便于下游 AI 应用使用 |
| 🖼️ **页面截图** | 生成高质量 PNG 截图，供多模态大模型使用 |
| 📄 **多格式支持** | PDF、DOCX、XLSX、PPTX、图片 |
| 🌐 **多语言绑定** | Rust / Python / Node.js / TypeScript / WASM |
| 🔒 **完全本地** | 无云依赖，不上传数据，隐私安全 |

### 与 LlamaParse 的关系

LiteParse 适合**简单文档、追求速度**的场景。如果处理复杂文档（密表格、多栏布局、图表、手写文字、扫描 PDF），推荐使用 [LlamaParse](https://cloud.llamaindex.ai)（LlamaIndex 官方云解析服务），效果更优。

### 安装

```bash
# Python
pip install liteparse

# Node.js / TypeScript
npm install @llamaindex/liteparse

# Rust CLI
cargo install liteparse

# Rust库
cargo add liteparse
```

### 快速开始

#### Python 示例

```python
from liteparse import LiteParse

# 初始化解析器
parser = LiteParse()

# 解析 PDF，返回结构化 JSON（含边界框）
result = parser.parse("document.pdf")
print(result.text) # 纯文本
print(result.json_data)  # JSON + bounding boxes

# 只解析前 5 页
result = parser.parse("document.pdf", target_pages="1-5")

# 禁用 OCR
result = parser.parse("document.pdf", no_ocr=True)

# 生成页面截图
parser.screenshot("document.pdf", output_dir="./screenshots")

# 批量解析目录
parser.batch_parse("./input", "./output", format="json")
```

#### Rust 示例

```rust
use liteparse::{LiteParse, OutputFormat};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let parser = LiteParse::new();

    // 解析 PDF
    let result = parser.parse("document.pdf", OutputFormat::Json)?;
    println!("{}", result.text());

    // 解析指定页面
    let result = parser.parse_with_options("document.pdf", &[
        ("target_pages", "1-5"),
        ("no_ocr", "false"),
    ])?;

    // 生成截图
    parser.screenshot("document.pdf", "./screenshots", 150)?;

    Ok(())
}
```

#### CLI 用法

```bash
# 基础解析
lit parse document.pdf

# JSON 输出
lit parse document.pdf --format json -o output.json

# 指定页面
lit parse document.pdf --target-pages "1-5,10,15-20"

# 禁用 OCR
lit parse document.pdf --no-ocr

# 批量解析目录
lit batch-parse ./input-dir ./output-dir

# 生成截图
lit screenshot document.pdf -o ./screenshots
```

### 输出格式示例

**JSON 输出（含边界框）：**

```json
{
  "pages": [
    {
      "page_number": 1,
      "width": 612,
      "height": 792,
      "blocks": [
        {
          "id": 0,
          "text": "Introduction to LiteParse",
          "bbox": { "x": 72, "y": 72, "width": 468, "height": 24 },
          "font_size": 18,
          "is_italic": false
        },
        {
          "id": 1,
          "text": "LiteParse is a fast, open-source document parser.",
          "bbox": { "x": 72, "y": 104, "width": 468, "height": 16 },
          "font_size": 12,
          "is_italic": false
        }
      ]
    }
  ],
  "metadata": {
    "total_pages": 10,
    "parser": "liteparse",
    "version": "0.2.0"
  }
}
```

### 架构概览

```
输入格式          Rust核心                          输出
─────────────────────────────────────────────────────────────
PDF         → 文本提取(PDFium)                    →  JSON
DOCX       →  格式转换(LibreOffice)                →  纯文本
XLSX       →  选择性OCR(Tesseract/HTTP) →  截图PNG
PPTX       →  OCR融合(原生文本+OCR结果)            ─────────
图片       →  网格投影(空间布局重构)
            ───────────────────────────────────────
            语言绑定: Python(PyO3) / Node(napi-rs) / WASM
```

### API 参考

| 方法 | 说明 |
|------|------|
| `parse(file, format='text')` | 解析单个文件 |
| `parse_to_json(file)` | 解析并返回 JSON（含边界框）|
| `screenshot(file, output_dir, dpi=150)` | 生成页面截图 |
| `batch_parse(input_dir, output_dir, format='text')` | 批量解析目录 |

---

## English

### What is LiteParse?

**LiteParse** is a Python/Rust wrapper for [run-llama/liteparse](https://github.com/run-llama/liteparse) — a standalone, open-source document parser written in Rust. It focuses exclusively on **fast and lightweight spatial text parsing** with precise bounding box output, no LLM required, no cloud dependency.

### Key Features

| Feature | Description |
|---------|-------------|
| ⚡ **Fast Parsing** | PDFium C library powered, spatial text extraction |
| 🔍 **Flexible OCR** | Built-in Tesseract (zero-config), also supports HTTP OCR servers |
| 📐 **Bounding Boxes** | Every text block includes precise coordinates |
| 🖼️ **Screenshots** | High-quality page screenshots for multimodal LLMs |
| 📄 **Multi-format** | PDF, DOCX, XLSX, PPTX, Images |
| 🌐 **Multi-language** | Rust / Python / Node.js / TypeScript / WASM |
| 🔒 **Fully Local** | No cloud, no data uploaded, privacy-first |

### When to Use LiteParse vs LlamaParse

LiteParse is great for **lightweight documents and speed**. For complex documents (dense tables, multi-column layouts, charts, handwriting, scanned PDFs), consider [LlamaParse](https://cloud.llamaindex.ai) — LlamaIndex's cloud-based parser with significantly better results.

### Installation

```bash
# Python
pip install liteparse

# Node.js / TypeScript
npm install @llamaindex/liteparse

# Rust CLI
cargo install liteparse

# Rust library
cargo add liteparse
```

### Quick Start

#### Python

```python
from liteparse import LiteParse

parser = LiteParse()

# Parse PDF to structured JSON with bounding boxes
result = parser.parse("document.pdf")
print(result.text)        # plain text
print(result.json_data)  # JSON + bounding boxes

# Parse specific pages
result = parser.parse("document.pdf", target_pages="1-5")

# Disable OCR
result = parser.parse("document.pdf", no_ocr=True)

# Generate page screenshots
parser.screenshot("document.pdf", output_dir="./screenshots")

# Batch parse directory
parser.batch_parse("./input", "./output", format="json")
```

#### Rust

```rust
use liteparse::{LiteParse, OutputFormat};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let parser = LiteParse::new();

    let result = parser.parse("document.pdf", OutputFormat::Json)?;
    println!("{}", result.text());

    let result = parser.parse_with_options("document.pdf", &[
        ("target_pages", "1-5"),
        ("no_ocr", "false"),
    ])?;

    parser.screenshot("document.pdf", "./screenshots", 150)?;

    Ok(())
}
```

#### CLI

```bash
# Basic
lit parse document.pdf

# JSON output
lit parse document.pdf --format json -o output.json

# Specific pages
lit parse document.pdf --target-pages "1-5,10,15-20"

# No OCR
lit parse document.pdf --no-ocr

# Batch
lit batch-parse ./input-dir ./output-dir

# Screenshots
lit screenshot document.pdf -o ./screenshots
```

---

## Star History

[![Star History](https://api.star-history.dev/svg?repos=run-llama/liteparse&type=timeline)](https://star-history.dev/#run-llama/liteparse)

---

## 许可证

Apache 2.0 License · ©2024 [run-llama/liteparse](https://github.com/run-llama/liteparse)

本项目是 LiteParse 的开源封装，仅整理和转发，如需最新功能和详细文档请访问[上游仓库](https://github.com/run-llama/liteparse)。

This is an open-source wrapper for LiteParse. For the latest features and documentation, visit the [upstream repository](https://github.com/run-llama/liteparse).
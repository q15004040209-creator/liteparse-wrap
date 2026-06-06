//! LiteParse Rust Demo
//! ====================
//! 展示如何使用 liteparse Rust 库进行文档解析。
//!
//! 安装依赖:
//! ```toml
//! [dependencies]
//! liteparse = "0.2"
//! ```
//!
//! 文档: https://developers.llamaindex.ai/liteparse/
//! 上游: https://github.com/run-llama/liteparse

use liteparse::{LiteParse, OutputFormat};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🚀 LiteParse Rust Demo");
    println!("========================");
    println!("上游: https://github.com/run-llama/liteparse");
    println!("星标: 9,285 (本周 +2,380)");
    println!();

    let parser = LiteParse::new();
    let demo_file = "sample.pdf";

    // ─────────────────────────────────────────────────────────────
    // 基础解析
    // ─────────────────────────────────────────────────────────────
    println!("\n{}", "=".repeat(60));
    println!("📄 基础解析 (parse)");
    println!("{}", "=".repeat(60));

    let result = parser.parse(demo_file, OutputFormat::Text)?;
    println!("\n✅ 解析完成");
    println!("文本预览:\n{}", &result.text().chars().take(500).collect::<String>());

    // ─────────────────────────────────────────────────────────────
    // JSON 解析 (含边界框)
    // ─────────────────────────────────────────────────────────────
    println!("\n{}", "=".repeat(60));
    println!("📐 JSON解析 (含边界框信息)");
    println!("{}", "=".repeat(60));

    let result = parser.parse(demo_file, OutputFormat::Json)?;
    let json_data = result.json_data();

    if let Some(pages) = json_data.get("pages").and_then(|p| p.as_array()) {
        if let Some(first_page) = pages.first() {
            println!("\n📑 第 {} 页", first_page["page_number"].as_i64().unwrap_or(0));
            println!("尺寸: {}x{}",
                first_page["width"].as_i64().unwrap_or(0),
                first_page["height"].as_i64().unwrap_or(0)
            );

            if let Some(blocks) = first_page.get("blocks").and_then(|b| b.as_array()) {
                println!("文本块数量: {}", blocks.len());
                println!("\n前3个文本块示例:");

                for (i, block) in blocks.iter().take(3).enumerate() {
                    println!("\n 块 {}:", i);
                    println!("  文本: {}",
                        block["text"].as_str().unwrap_or("").chars().take(80).collect::<String>());
                    if let Some(bbox) = block.get("bbox").and_then(|b| b.as_object()) {
                        println!("  边界框: x={}, y={}, w={}, h={}",
                            bbox.get("x").and_then(|v| v.as_i64()).unwrap_or(0),
                            bbox.get("y").and_then(|v| v.as_i64()).unwrap_or(0),
                            bbox.get("width").and_then(|v| v.as_i64()).unwrap_or(0),
                            bbox.get("height").and_then(|v| v.as_i64()).unwrap_or(0)
                        );
                    }
                    println!("  字体大小: {}",
                        block["font_size"].as_f64().unwrap_or(0.0));
                }
            }
        }
    }

    // ─────────────────────────────────────────────────────────────
    // 指定页面解析
    // ─────────────────────────────────────────────────────────────
    println!("\n{}", "=".repeat(60));
    println!("🎯 指定页面解析 (1-5, 10, 15-20)");
    println!("{}", "=".repeat(60));

    let result = parser.parse_with_options(demo_file, &[
        ("target_pages", "1-5,10,15-20"),
        ("format", "json"),
    ])?;
    println!("\n✅ 指定页面解析完成");

    // ─────────────────────────────────────────────────────────────
    // 禁用 OCR
    // ─────────────────────────────────────────────────────────────
    println!("\n{}", "=".repeat(60));
    println!("🔇 禁用 OCR 解析");
    println!("{}", "=".repeat(60));

    let result = parser.parse_with_options(demo_file, &[
        ("no_ocr", "true"),
        ("format", "text"),
    ])?;
    println!("\n✅ 纯文本提取完成 (不调用 OCR)");

    // ─────────────────────────────────────────────────────────────
    // 生成截图
    // ─────────────────────────────────────────────────────────────
    println!("\n{}", "=".repeat(60));
    println!("🖼️ 生成页面截图 (DPI=150)");
    println!("{}", "=".repeat(60));

    let result = parser.screenshot(demo_file, "./screenshots", 150, &[
        ("target_pages", "1-3"),
    ])?;
    println!("\n✅ 截图生成完成，共 {} 张", result.len());

    // ─────────────────────────────────────────────────────────────
    // 批量解析
    // ─────────────────────────────────────────────────────────────
    println!("\n{}", "=".repeat(60));
    println!("📂 批量解析目录");
    println!("{}", "=".repeat(60));

    let results = parser.batch_parse("./input", "./output", &[
        ("format", "json"),
        ("recursive", "true"),
    ])?;
    println!("\n✅ 批量解析完成，共处理 {} 个文件", results.len());

    println!("\n{}", "=".repeat(60));
    println!("🎉 所有演示完成!");
    println!("{}", "=".repeat(60));

    Ok(())
}
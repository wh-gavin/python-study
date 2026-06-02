import fitz  # PyMuPDF
import os
from collections import Counter

# PDF 文件路径（使用你原来的相对路径）
pdf_path = "../data/C2/pdf/rag.pdf"

# 打开 PDF 文档
doc = fitz.open(pdf_path)

# 存储解析出的元素
elements = []  # 每个元素是一个字典，包含文本、类型、页码等信息
element_types = Counter()

# 遍历每一页
for page_num in range(len(doc)):
    page = doc[page_num]

    # ------------------------------
    # 1. 提取文本块（按段落/行分组）
    # ------------------------------
    # 使用 "dict" 模式获取详细的文本块信息
    text_dict = page.get_text("dict")
    for block in text_dict.get("blocks", []):
        if block["type"] == 0:  # 文本块
            # 合并该块中的所有文本
            block_text = ""
            for line in block["lines"]:
                for span in line["spans"]:
                    block_text += span["text"]
            block_text = block_text.strip()
            if block_text:
                elements.append({
                    "page": page_num + 1,
                    "category": "Text",
                    "content": block_text
                })
                element_types["Text"] += 1

    # ------------------------------
    # 2. 提取表格（使用 find_tables）
    # ------------------------------
    tables = page.find_tables()
    if tables:
        for table in tables:
            # 将表格转为 DataFrame 再转为文本描述
            df = table.to_pandas()
            table_text = f"表格 ( {df.shape[0]} 行 x {df.shape[1]} 列 )\n" + df.to_string()
            elements.append({
                "page": page_num + 1,
                "category": "Table",
                "content": table_text
            })
            element_types["Table"] += 1

    # ------------------------------
    # 3. 提取图片（仅记录图片数量，不保存文件）
    # ------------------------------
    image_list = page.get_images()
    if image_list:
        for img_idx, img in enumerate(image_list):
            elements.append({
                "page": page_num + 1,
                "category": "Image",
                "content": f"[图片 {img_idx+1}]"
            })
            element_types["Image"] += 1

# 关闭文档
doc.close()

# 打印解析结果
print(f"解析完成: {len(elements)} 个元素, 总字符数: {sum(len(e['content']) for e in elements)}")
print(f"元素类型: {dict(element_types)}")

# 显示所有元素
print("\n所有元素:")
for i, elem in enumerate(elements, 1):
    print(f"Element {i} ({elem['category']}, 第{elem['page']}页):")
    # 对于文本内容过长的情况，截取前300字符
    content = elem['content']
    if len(content) > 300:
        content = content[:300] + "...(截断)"
    print(content)
    print("=" * 60)
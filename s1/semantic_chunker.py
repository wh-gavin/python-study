import os
# 设置 HuggingFace 镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from sentence_transformers import SentenceTransformer
from semantic_router.encoders import HuggingFaceEncoder  # 注意大小写
import semantic_chunkers as sc



# 1. 加载中文嵌入模型
base_model = SentenceTransformer("../../ai/models/bge-large-zh-v1.5", device="cpu", local_files_only=True)
#base_model.save_pretrained("../../ai/models/bge-large-zh-v1.5")

# 2. 用 HuggingFaceEncoder 包装（正确类名）
encoder = HuggingFaceEncoder(encoder=base_model)

# 3. 创建 StatisticalChunker
chunker = sc.StatisticalChunker(encoder=encoder)

# 4. 读取文本
file_path = "../data/C2/txt/蜂医.txt"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 5. 执行分块
chunks_result = chunker(docs=[text])  # 返回 List[List[Chunk]]
chunks = chunks_result[0]             # 取出第一个文档的分块

# 6. 输出结果
print(f"文本被切分为 {len(chunks)} 个语义块。\n")
for i, chunk in enumerate(chunks[:5]):
    print("=" * 60)
    print(f"块 {i+1} (长度: {len(chunk.content)} 字符): ")
    print(chunk.content)  # 只显示前200字符，避免刷屏
    print()
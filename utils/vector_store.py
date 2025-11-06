# utils/vector_store.py
import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Optional

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model_name)
        self.index = None
        self.embeddings = []
        self.metadata = []

    def add_texts(self, texts: List[str], metadata: Optional[List[dict]] = None):
        """添加文本并构建向量索引"""
        embeddings = self.model.encode(texts)
        self.embeddings.extend(embeddings)
        self.metadata.extend(metadata or [{} for _ in texts])

        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

        logger.info(f"已添加 {len(texts)} 个文本到向量库")

    def search(self, query: str, k: int = 3) -> List[dict]:
        logger.info("基于查询进行向量检索")
        query_embedding = self.model.encode([query])
        D, I = self.index.search(query_embedding, k)

        results = []
        for idx in I[0]:
            score = D[0][idx]
            text = self.metadata[idx].get("text", "")
            results.append({
                "score": float(score),
                "text": text,
                "metadata": self.metadata[idx]
            })
        logger.debug(f"检索结果数量: {len(results)}")
        return results
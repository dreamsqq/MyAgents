import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import os

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2",local_path='.\models'):
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        model_path = os.path.join(local_path, embedding_model_name)
        if not os.path.exists(model_path):
            logger.info(f"Embedding 模型不存在，正在下载: {embedding_model_name}")
            self.model = SentenceTransformer(embedding_model_name)
            self.model.save(model_path)
        else:
            self.model = SentenceTransformer(model_path)
        self.index = None
        self.embeddings = []
        self.metadata = []
        self.texts = []

    def add_texts(self, texts: List[str], metadata: Optional[List[dict]] = None):
        try:
            logging.info("添加文本并构建向量索引")
            if not texts:
                logger.warning("没有提供文本进行添加")
                return
            embeddings = self.model.encode(texts)
            self.embeddings.extend(embeddings)
            self.texts.extend(texts)
            self.metadata.extend(metadata or [{} for _ in texts])

            if self.index is None:
                dimension = embeddings.shape[1]
                self.index = faiss.IndexFlatL2(dimension)
            self.index.add(np.array(embeddings))

            logger.info(f"已添加 {len(texts)} 个文本到向量库")
        except Exception as e:
            logger.error(f"添加文本失败: {e}")

    def search(self, query: str, k: int = 3) -> List[dict]:
        logger.info("基于查询进行向量检索")
        query_embedding = self.model.encode([query])
        D, I = self.index.search(query_embedding, k)
        logger.info(f'{D}\n{I}\n')
        results = []
        for idx in range(len(I[0])):
            score = D[0][idx]
            text = self.metadata[I[0][idx]].get("text", "")
            logger.debug(f'文本：{text[:100]}')
            results.append({
                "score": float(score),
                "text":  self.texts[idx],
                "metadata": self.metadata[idx]
            })
        logger.debug(f"检索结果数量: {len(results)}")
        return results
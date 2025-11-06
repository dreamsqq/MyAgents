# main.py
import logging
import os
from pathlib import Path
from config.logging_config import setup_logging
from utils.document_parser import parse_document, split_text_into_chunks
from utils.vector_store import VectorStore
from agents.rag_agent import RAGAgent
from agents.chat_service import ChatService

# 初始化日志
setup_logging()
logger = logging.getLogger(__name__)

def load_documents(doc_dir: str = "data/documents"):
    logger.info("加载文档并构建向量库")
    vector_store = VectorStore()
    doc_dir = Path(doc_dir)
    if not doc_dir.exists():
        logger.error(f"文档目录不存在: {doc_dir},使用默认空向量库")
        return vector_store

    for file_path in doc_dir.glob("*.*"):
        try:
            text = parse_document(file_path)
            chunks = split_text_into_chunks(text, chunk_size=300)
            metadata = [{"text": chunk, "source": str(file_path)} for chunk in chunks]
            vector_store.add_texts(chunks, metadata)
        except Exception as e:
            logger.error(f"处理文件失败: {file_path}, 错误: {e}")
    logger.info(f"共加载 {len(vector_store.embeddings)} 个文本块")
    return vector_store

def main():
    logger.info("RAG Agent 项目启动")
    vector_store = load_documents()
    agent = RAGAgent(vector_store)
    chat_service = ChatService(agent)

    # 模拟用户提问
    questions = [
        "项目的核心功能是什么？",
        "如何使用 LangGraph？",
        "支持哪些文档格式？"
    ]

    for q in questions:
        result = chat_service.ask(q)
        print(f"问: {q}")
        print(f"答: {result['response']}\n")

if __name__ == "__main__":
    main()
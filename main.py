import logging
import os
from pathlib import Path
from config.logging_config import setup_logging
from utils.document_parser import parse_document, create_documents_with_metadata
from utils.vector_store import VectorStore
from agents.rag_agent import RAGAgent
from agents.chat_service import ChatService

# 初始化日志
setup_logging()
logger = logging.getLogger(__name__)

def load_documents(doc_dir: str = r"data"):
    logger.info("加载文档并构建向量库")
    vector_store = VectorStore()
    doc_dir = Path(doc_dir)
    if not doc_dir.exists():
        logger.error(f"文档目录不存在: {doc_dir} ")
        return None
    logger.info(f"正在处理目录: {doc_dir}")
    for file_path in doc_dir.glob("*.*"):
        try:
            # text = parse_document(file_path)
            # #按字符数切分文本为块
            # chunks = split_text_into_chunks(text, chunk_size=300)
            logger.info(f"正在处理文件: {file_path}")
            documents = create_documents_with_metadata(file_path)
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            # metadata = [{"source_doc": str(file_path),"content":str(chunk.page_content), "text": chunk.metadata, } for chunk in chunks]
            # logging.info(metadata[0]["content"])
            vector_store.add_texts(texts, metadatas)
        except Exception as e:
            logger.error(f"处理文件失败: {file_path}, 错误: {e}")
    logger.info(f"共加载 {len(vector_store.embeddings)} 个文本块")
    return vector_store

def main():
    try:
        logger.info("RAG Agent 项目启动")
        valid = False
        doc_dir=r'D:\C_Documents\sanziqi.docx'
        vector_store = load_documents()
        if vector_store is None:
            logger.info("向量库加载失败，请上传文件")
        agent = RAGAgent(vector_store)
        chat_service = ChatService(agent)
        
        while True:

            questions = input('请输入问题！')
            if questions.strip().lower() == 'exit':
                logger.info("用户选择退出程序")
                break
            elif not questions.strip():
                # # 模拟用户提问
                questions = [
                    "项目的核心功能是什么？",
                    "如何使用 LangGraph？",
                    "支持哪些文档格式？"
                ]
                for q in questions:
                    result = chat_service.ask(q)
                    print(f"问: {q}")
                    print(f"答: {result['response']}\n")

            result = chat_service.ask(questions)
            print(f"问: {questions}")
            print(f"答: {result['response']}\n")
    
    except KeyboardInterrupt:
        logger.info("程序中断，正在退出...")
    except Exception as e:
        logger.critical(f"程序异常终止: {e}")
if __name__ == "__main__":
    main()
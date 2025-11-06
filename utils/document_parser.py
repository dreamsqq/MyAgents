# utils/document_parser.py
import logging
import os
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {".pdf", ".docx", ".md", ".txt"}

def parse_document(file_path: str) -> str:
    logger.info(f"解析支持的文档格式并返回纯文本:{'、'.join(SUPPORTED_FORMATS)}")
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = Path(file_path).suffix.lower()
    if ext not in SUPPORTED_FORMATS:
        logger.error(f"不支持的文件格式: {ext}")
        raise ValueError(f"Unsupported file format: {ext}")

    try:
        if ext == ".pdf":
            return _parse_pdf(file_path)
        elif ext == ".docx":
            return _parse_docx(file_path)
        elif ext == ".md":
            return _parse_markdown(file_path)
        elif ext == ".txt":
            return _parse_txt(file_path)
    except Exception as e:
        logger.error(f"解析文件失败: {file_path}, 错误: {e}")
        raise

def _parse_pdf(file_path: str) -> str:
    from PyPDF2 import PdfReader
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    logger.info(f"成功解析 PDF 文件: {file_path}")
    return text

def _parse_docx(file_path: str) -> str:
    from docx import Document
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    logger.info(f"成功解析 Word 文件: {file_path}")
    return text

def _parse_markdown(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    logger.info(f"成功解析 Markdown 文件: {file_path}")
    return text

def _parse_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    logger.info(f"成功解析 TXT 文件: {file_path}")
    return text

def split_text_into_chunks(text: str, chunk_size: int = 500) -> List[str]:
    """按字符数切分文本为块"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    logger.debug(f"文本切分为 {len(chunks)} 个块")
    return chunks
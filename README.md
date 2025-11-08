# RAG Agent 项目

一个支持文档上传、解析、向量化、检索与多轮对话的 RAG Agent。

## 🚀 功能特性

- ✅ 支持 PDF、Word (.docx)、Markdown (.md)、TXT 文件上传与解析
- ✅ 文本分段与向量化（FAISS）
- ✅ 向量检索 + LLM 生成问答
- ✅ 多轮对话上下文保持
- ✅ 使用 LangGraph 构建 Agent 执行流程图
- ✅ 使用标准日志模块（logging）
- ✅ 使用 `uv` 管理依赖
- ✅ GitHub 项目仓库，具备分支管理

## 🧰 技术栈

- Python 3.10
- PyPDF2, python-docx, markdown
- FAISS + Sentence-BERT
- LangChain + LangGraph
- logging
- uv (pip 替代)

## 📦 安装与运行

```bash
# 克隆项目
git clone https://github.com/dreamsqq/MyAgents.git
cd MyAgents

# 使用 uv 安装依赖
uv pip install -e .

# 运行主程序
python main.py
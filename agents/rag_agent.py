# agents/rag_agent.py
import logging
from langgraph.graph import StateGraph, END
from typing import Dict, Any
from utils.vector_store import VectorStore

logger = logging.getLogger(__name__)

class RAGAgent:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.state_graph = StateGraph(dict)

    def _retrieve_context(self, query: str) -> str:
        results = self.vector_store.search(query, k=3)
        context = "\n\n".join([r["text"] for r in results])
        logger.info(f"检索到上下文: {context[:100]}...")
        return context

    def _generate_response(self, query: str, context: str) -> str:
        # 模拟 LLM 响应（实际可接入 OpenAI）
        response = f"根据上下文，回答如下：{query} 的相关信息是：{context[:100]}..."
        logger.info(f"LLM 生成响应: {response[:50]}...")
        return response

    def _process_question(self, state: Dict[str, Any]) -> Dict[str, Any]:
        query = state["query"]
        context = self._retrieve_context(query)
        response = self._generate_response(query, context)
        return {"response": response, "context": context}

    def build_graph(self):
        graph = self.state_graph
        graph.add_node("process", self._process_question)
        graph.set_entry_point("process")
        graph.add_edge("process", END)
        return graph.compile()

    def run(self, query: str) -> Dict[str, Any]:
        logger.info(f"收到用户提问: {query}")
        return self.build_graph().invoke({"query": query})
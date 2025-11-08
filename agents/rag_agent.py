import logging
from langgraph.graph import StateGraph, END
from typing import Dict, Any
from utils.vector_store import VectorStore
from utils.llm_response import get_llm_answer

logger = logging.getLogger(__name__)

class RAGAgent:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.state_graph = StateGraph(dict)

    def _retrieve_context(self, query: str) -> str:
        try:
            results = self.vector_store.search(query, k=3)
            if not results:
                logger.warning("未检索到相关上下文")
                return ""

            context = "\n\n".join([r["text"] for r in results])
            # logger.info(f"检索到上下文: {context}...")
            return context
        except Exception as e:
            logger.error(f"检索上下文失败: {e}")
            return ""

    def _generate_response(self, query: str, context: str, chat_history: list) -> str:
        try:
            # logger.info(f"type:{type(context)}\ncontext:{context}")
            response = get_llm_answer(
                user_query=query,
                context_docs=[{"page_content": context, "metadata": {"title": "检索结果"}}],
                chat_history=chat_history
            )

            # # 模拟 LLM 响应（实际可接入 OpenAI）
            # response = f"根据上下文，回答如下：{query} 的相关信息是：{context[:100]}..."
            logger.info(f"LLM 生成响应...")
            return response
        except Exception as e:  
            logger.error(f"生成响应失败: {e}")
            return "抱歉，无法生成回答。"
        
    def _process_question(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            query = state["query"]
            chat_history = state.get("chat_history", [])  # 从状态中获取历史
            context = self._retrieve_context(query)
            # 传入 chat_history 到生成响应的方法
            response = self._generate_response(query, context, chat_history)
            
            # 更新对话历史（将当前查询和响应加入历史）
            new_chat_history = chat_history + [
                {"role": "user", "content": query},
                {"role": "assistant", "content": response}
            ]
            return {"response": response,
                    "context": context,
                    "chat_history": new_chat_history}
        except Exception as e:
            logger.error(f"处理问题失败: {e}")
            return {"response": "抱歉，处理您的问题时出错了。", "context": ""}
        
    def build_graph(self):
        graph = self.state_graph
        if "process" not in graph.nodes:  # 防御性检查（可选）
            graph.add_node("process", self._process_question)
            graph.set_entry_point("process")
            graph.add_edge("process", END)
        return graph.compile()

    def run(self, query: str, chat_history: list = None) -> Dict[str, Any]:
        logger.info(f"收到用户提问: {query}")
        return self.build_graph().invoke({"query": query,"chat_history": chat_history})
# services/chat_service.py
import logging
from typing import List, Dict
from agents.rag_agent import RAGAgent

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, agent: RAGAgent):
        self.agent = agent
        self.history: List[Dict] = []

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict]:
        return self.history

    def ask(self, question: str) -> Dict[str, any]:
        result = self.agent.run(question)
        response = result["response"]
        self.add_message("user", question)
        self.add_message("assistant", response)
        logger.info(f"对话历史长度: {len(self.history)}")
        return {"response": response, "context": result.get("context")}
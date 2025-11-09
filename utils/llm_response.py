from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
import time
logger = logging.getLogger(__name__)
load_dotenv()

# 使用 @traceable 自动上报到 LangSmith
from langsmith import traceable
@traceable(run_type="chain")
def get_llm_answer(user_query, context_docs, chat_history):
    try:
        start_time = time.time()
        if chat_history is None:
            chat_history = []

        api_key=os.getenv("qianwen_api_key")
        if not api_key:
            logger.error("不存在密钥，请在环境变量中设置 qianwen_api_key")
            
        client = OpenAI(
            api_key=api_key, 
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        # 拼接上下文
        context = "\n\n".join([
            f"【主题】{doc['metadata']['title']}\n"
            f"【参考回答】{doc['page_content'].split('回答：')[-1].strip()}"
            for doc in context_docs
        ])

        system_prompt = f"""
        你是一名专业文档分析助手，请根据参考资料和对话历史回答用户问题。
        要求：
        1. 若问题与历史对话相关（如询问之前的提问、补充说明），优先使用对话历史回答；
        2. 若问题与文档内容相关，必须基于参考资料，不得编造；
        3. 语言正式、严谨，相关内容需注明依据（参考资料/对话历史）；
        4. 如果信息不足，请回答“暂无足够依据”。

        参考资料：
        {context}

        请用中文正式回答用户问题：
        """
        MAX_HISTORY_MESSAGES = 10
        if len(chat_history) > MAX_HISTORY_MESSAGES:
            chat_history = chat_history[-MAX_HISTORY_MESSAGES:]

        # 5. 构建完整 messages 列表
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        # 添加历史对话（user + assistant 交替）
        messages.extend(chat_history)
        # 添加当前用户新问题
        messages.append({"role": "user", "content": user_query})

        response = client.chat.completions.create(
            model="qwen-plus",  # 推荐使用 qwen-plus 或 qwen-max，法律理解更强
            messages=messages,
            temperature=0.1,   # 低温度，减少幻觉
            max_tokens=1024
        )
        answer = response.choices[0].message.content
        lasttime = time.time() - start_time
        result = {
            "input": {
                "user_query": user_query,
                "context_doc_count": len(context_docs),
                "chat_history_length": len(chat_history)
            },
            "output": {
                "answer": answer,
                "latency_seconds": round(lasttime, 3),
                "context_used": bool(context.strip())
            }
        }

        return result

    except Exception as e:
        lasttime = time.time() - start_time
        logger.error(f"调用llm回答失败: {e}")
        return {
            "input": {"user_query": user_query},
            "output": {
                "error": str(e),
                "latency_seconds": round(lasttime, 3),
                "answer": "调用 LLM 回答失败。"
            }
        }
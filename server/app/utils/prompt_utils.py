from typing import List
from app.data_models.schemas import ChatMessage

def format_chat_prompt(messages: List[ChatMessage]) -> str:
    prompt = ""
    for message in messages:
        if message.role == "user":
            prompt += f"Central Planner: {message.content}\n"
        elif message.role == "assistant":
            prompt += f"Assistant: {message.content}\n"
    prompt += "Assistant: "
    return prompt

def do_job_prompt(task:str, context:str) -> str:
    """Format"""
    return f"Do the job described: \n{task}\n using the context: \n{context}\n"
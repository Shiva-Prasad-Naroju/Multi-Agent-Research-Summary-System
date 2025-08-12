from langchain.schema import SystemMessage
from config import LLM_MODEL
from langchain.chat_models import init_chat_model

llm = init_chat_model(LLM_MODEL)
def writer_agent(state):
    """Writer agent that creates summaries"""
    messages = state["messages"]
    system_msg = SystemMessage(content="You are a technical writer. Create a concise summary of the findings.")
    
    response = llm.invoke([system_msg] + messages)
    
    return {
        "messages": [response],
        "final_answer": response.content,  
    }

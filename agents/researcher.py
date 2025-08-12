from langchain.schema import SystemMessage, HumanMessage
from config import LLM_MODEL
from langchain.chat_models import init_chat_model
from tools.search_web import search_web

llm = init_chat_model(LLM_MODEL)

def researcher_agent(state):
    messages = state["messages"]
    system_msg = SystemMessage(content=(
        "You are a research assistant. "
        "You must use the search_web tool to find fresh and relevant information before answering. "
        "Do not answer based on your internal knowledge alone."
    ))

    researcher_llm = llm.bind_tools([search_web])
    response = researcher_llm.invoke([system_msg] + messages)

    # Execute any tool calls
    tool_results = []
    if hasattr(response, "tool_calls") and response.tool_calls:
        for call in response.tool_calls:
            if call["name"] == "search_web":
                query = call["args"]["query"]
                result = search_web.invoke(query)
                tool_results.append(result)

    
    if tool_results:
        # Append the concatenated tool outputs as a human message
        tool_output = "\n\n".join(tool_results)
        new_messages = [response, HumanMessage(content=tool_output)]
    else:
        new_messages = [response]

    return {
        "messages": new_messages,
        "next_agent": "writer"
    }

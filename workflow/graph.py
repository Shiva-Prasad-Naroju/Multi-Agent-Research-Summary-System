from langgraph.graph import StateGraph, END
from workflow.state import AgentState
from agents.researcher import researcher_agent
from agents.writer import writer_agent

# Final collector node to ensure consistent output
def final_node(state: AgentState):
    messages = state.get("messages", [])
    if messages:
        last_message = messages[-1]
        if hasattr(last_message, "content"):
            content = last_message.content
        elif isinstance(last_message, dict):
            content = last_message.get("content", "")
        else:
            content = str(last_message)
    else:
        content = "No answer produced."
    return {"final_answer": content}

def build_workflow():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("final_node", final_node)
    
    # Edges
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "final_node")
    workflow.add_edge("final_node", END)
    
    return workflow.compile()

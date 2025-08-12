from typing import TypedDict, List, Optional
from langgraph.graph import MessagesState

class AgentState(MessagesState):
    next_agent: str  # Which agent should go next
    final_answer: Optional[str]  # To hold the final output from final_node or agents

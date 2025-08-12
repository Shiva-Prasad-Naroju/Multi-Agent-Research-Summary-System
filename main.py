from workflow.graph import build_workflow

if __name__ == "__main__":
    final_workflow = build_workflow()

    user_input = "Find the latest research on LangGraph multi-agent systems."
    result = final_workflow.invoke({"messages": [{"type": "human", "content": user_input}]})
    
    print(result["messages"][-1].content)

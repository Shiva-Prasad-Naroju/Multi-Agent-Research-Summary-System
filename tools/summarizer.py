from langchain_core.tools import tool

@tool
def write_summary(content: str) -> str:
    """Write a summary of the provided content."""
    summary = f"Summary of findings:\n\n{content[:500]}..."
    return summary

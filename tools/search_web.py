from langchain_core.tools import tool
from ddgs import DDGS

ddg_search = DDGS()

@tool
def search_web(query: str) -> str:
    """
    Search the web for information using DuckDuckGo.
    """
    results = []
    for res in ddg_search.text(query):
        # res is a dict, pick relevant fields
        title = res.get("title", "")
        href = res.get("href", "")
        body = res.get("body", "")
        # Format each result as a string
        result_str = f"Title: {title}\nURL: {href}\nSummary: {body}\n"
        results.append(result_str)
    return "\n\n".join(results)

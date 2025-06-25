from tavily import TavilyClient
from langchain.tools import tool
from dotenv import load_dotenv
import os
from typing import List
from pydantic import BaseModel

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class Resource(BaseModel):
    title: str
    type: str  # e.g., "article", "video"
    url: str
    description: str

@tool
def search_resources(query: str) -> List[Resource]:
    """Finds tutorials, guides, or videos from trusted sources related to the query."""
    results = client.search(query=query, include_answers=True, max_results=5)

    structured = []
    for r in results.get("results", []):
        structured.append(Resource(
            title=r["title"],
            type="article" if "youtube.com" not in r["url"] else "video",
            url=r["url"],
            description=r["content"][:200] + "..." if r["content"] else "No description"
        ))

    return structured

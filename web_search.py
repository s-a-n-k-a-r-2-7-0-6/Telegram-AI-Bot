import os
import requests
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")  # Custom Search Engine ID

def web_search(query):
    """Performs a Google search and returns summarized results."""
    if not GOOGLE_SEARCH_API_KEY or not GOOGLE_CSE_ID:
        return "⚠️ Google Search API is not configured properly."
    
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_SEARCH_API_KEY}&cx={GOOGLE_CSE_ID}"
    
    response = requests.get(url)
    data = response.json()
    
    if "items" not in data:
        return "❌ No results found."

    # Get top 3 search results
    results = data["items"][:3]
    summary = "\n".join([f"{i+1}. [{item['title']}]({item['link']})" for i, item in enumerate(results)])
    
    return f"🔍 **Search Results:**\n{summary}"

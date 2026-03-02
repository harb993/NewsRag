import requests
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class NewsRetriever:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        if not self.api_key:
            raise ValueError("NewsAPI key not found. Please set NEWS_API_KEY environment variable.")
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_articles(self, query: str, page_size: int = 5) -> Dict:
        """
        Fetches articles from NewsAPI based on a query.
        Returns a dictionary with 'articles' and potentially 'error'.
        """
        params = {
            "q": query,
            "pageSize": page_size,
            "apiKey": self.api_key,
            "language": "en",
            "sortBy": "relevancy"
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code != 200:
                error_data = response.json()
                return {"articles": [], "error": error_data.get("message", "Unknown API error")}
            
            data = response.json()
            articles = []
            for art in data.get("articles", []):
                articles.append({
                    "title": art.get("title"),
                    "description": art.get("description"),
                    "content": art.get("content"),
                    "url": art.get("url"),
                    "source": art.get("source", {}).get("name")
                })
            return {"articles": articles}
        except Exception as e:
            return {"articles": [], "error": str(e)}

if __name__ == "__main__":
    # Quick test
    retriever = NewsRetriever()
    results = retriever.fetch_articles("technology", page_size=2)
    for i, res in enumerate(results):
        print(f"{i+1}. {res['title']} ({res['source']})")

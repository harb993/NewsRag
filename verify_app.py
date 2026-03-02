from news_retriever import NewsRetriever
from embedding_engine import EmbeddingEngine
from summarizer import Summarizer
from user_manager import UserManager
import os
from dotenv import load_dotenv

def test_integration():
    load_dotenv()
    if not os.getenv("NEWS_API_KEY"):
        print("SKIP: NEWS_API_KEY not set. Skipping real API test.")
        return

    print("Step 1: News Retrieval")
    retriever = NewsRetriever()
    articles = retriever.fetch_articles("space exploration", page_size=3)
    assert len(articles) > 0, "No articles fetched"
    print(f"Fetched {len(articles)} articles.")

    print("\nStep 2: Embedding & Storage")
    engine = EmbeddingEngine(persist_directory="test_vault")
    engine.initialize_db(articles)
    docs = engine.query_articles("NASA")
    assert len(docs) > 0, "No documents retrieved from vector store"
    print(f"Retrieved {len(docs)} relevant documents.")

    print("\nStep 3: Summarization")
    summarizer = Summarizer()
    brief = summarizer.summarize_brief(docs)
    print(f"Brief Summary: {brief}")
    
    detailed = summarizer.summarize_detailed(docs)
    print(f"Detailed Summary: {detailed}")

    print("\nStep 4: User Management")
    mgr = UserManager("test_prefs.json")
    mgr.add_topic("Mars")
    mgr.add_to_history("SpaceX")
    assert "Mars" in mgr.get_topics()
    assert "SpaceX" in mgr.get_history()
    print("User management verified.")

if __name__ == "__main__":
    test_integration()

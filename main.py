import sys
import os
from dotenv import load_dotenv

# Import components
from news_retriever import NewsRetriever
from embedding_engine import EmbeddingEngine
from summarizer import Summarizer
from user_manager import UserManager

def main():
    load_dotenv()
    
    # Initialize components
    try:
        retriever = NewsRetriever()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please create a .env file with NEWS_API_KEY=your_key")
        sys.exit(1)
        
    engine = EmbeddingEngine()
    summarizer = Summarizer()
    user_mgr = UserManager()

    print("--- Welcome to the News Summarization Agent ---")
    
    while True:
        print("\nOptions:")
        print("1. Search & Summarize News")
        print("2. View Saved Topics")
        print("3. View Search History")
        print("4. Add Topic of Interest")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ")
        
        if choice == '1':
            query = input("Enter topic to search: ")
            user_mgr.add_to_history(query)
            
            print(f"Fetching news for '{query}'...")
            articles = retriever.fetch_articles(query)
            if not articles:
                print("No articles found.")
                continue
            
            print("Embedding articles...")
            engine.initialize_db(articles)
            
            print("Retrieving relevant snapshots...")
            docs = engine.query_articles(query)
            
            print("\nSelect Summary Type:")
            print("s. Short (1-2 sentences)")
            print("d. Detailed (Paragraph)")
            sum_type = input("Choice (s/d): ").lower()
            
            print("Generating summary...")
            if sum_type == 'd':
                summary = summarizer.summarize_detailed(docs)
            else:
                summary = summarizer.summarize_brief(docs)
                
            print("\n--- SUMMARY ---")
            print(summary)
            print("----------------")
            
        elif choice == '2':
            topics = user_mgr.get_topics()
            print(f"\nSaved Topics: {', '.join(topics) if topics else 'None'}")
            
        elif choice == '3':
            history = user_mgr.get_history()
            print("\nRecent Searches:")
            for h in history:
                print(f"- {h}")
                
        elif choice == '4':
            topic = input("Enter topic to save: ")
            user_mgr.add_topic(topic)
            print(f"Topic '{topic}' saved!")
            
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

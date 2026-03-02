from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from typing import List, Dict
import os

class EmbeddingEngine:
    def __init__(self, model_name: str = "nomic-embed-text", persist_directory: str = "news_vault"):
        self.embeddings = OllamaEmbeddings(model=model_name)
        self.persist_directory = persist_directory
        self.vector_store = None

    def initialize_db(self, articles: List[Dict]):
        """
        Creates a new vector store from a list of articles.
        """
        documents = []
        for art in articles:
            # Combine title and description for embedding if content is short or null
            text = f"{art['title']}\n\n{art['description'] or ''}\n\n{art['content'] or ''}"
            metadata = {
                "source": art["source"],
                "url": art["url"],
                "title": art["title"]
            }
            documents.append(Document(page_content=text, metadata=metadata))
        
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        # Chroma in recent versions persists automatically, but we ensure it's handled.
        print(f"Stored {len(documents)} articles in {self.persist_directory}")

    def query_articles(self, query: str, k: int = 3) -> List[Document]:
        """
        Retrieves relevant articles from the vector store.
        """
        if not self.vector_store:
            if os.path.exists(self.persist_directory):
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
            else:
                print("Vector store not initialized and no persist directory found.")
                return []
        
        return self.vector_store.similarity_search(query, k=k)

if __name__ == "__main__":
    # Test stub
    engine = EmbeddingEngine()
    # Assuming articles exist for testing...
    # engine.initialize_db(test_articles)
    # print(engine.query_articles("AI trends"))

from flask import Flask, request, jsonify
from flask_cors import CORS
from news_retriever import NewsRetriever
from embedding_engine import EmbeddingEngine
from summarizer import Summarizer
from user_manager import UserManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize core components
retriever = NewsRetriever()
engine = EmbeddingEngine()
summarizer = Summarizer()
user_mgr = UserManager()

@app.route('/api/search', methods=['POST'])
def search_news():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    user_mgr.add_to_history(query)
    result = retriever.fetch_articles(query)
    articles = result.get('articles', [])
    error = result.get('error')
    
    if error:
        return jsonify({"error": f"NewsAPI Error: {error}", "articles": []}), 500
    
    if articles:
        engine.initialize_db(articles)
        return jsonify({"message": f"Fetched and embedded {len(articles)} articles", "articles": articles})
    else:
        return jsonify({"message": "No articles found", "articles": []})

@app.route('/api/summarize', methods=['POST'])
def summarize_news():
    data = request.json
    query = data.get('query')
    summary_type = data.get('type', 'short') # 'short' or 'detailed'
    persona = data.get('persona', 'reporter')
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    docs = engine.query_articles(query)
    if not docs:
        return jsonify({"error": "No articles found in vault for this topic. Please search first."}), 404
    
    if summary_type == 'detailed':
        summary = summarizer.summarize_detailed(docs, persona=persona)
    else:
        summary = summarizer.summarize_brief(docs, persona=persona)
        
    return jsonify({"summary": summary})

@app.route('/api/preferences', methods=['GET', 'POST'])
def manage_preferences():
    if request.method == 'POST':
        data = request.json
        topic = data.get('topic')
        if topic:
            user_mgr.add_topic(topic)
            return jsonify({"message": f"Topic {topic} added", "topics": user_mgr.get_topics()})
        return jsonify({"error": "Topic is required"}), 400
    
    return jsonify({"topics": user_mgr.get_topics()})

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify({"history": user_mgr.get_history()})

if __name__ == '__main__':
    app.run(port=5000, debug=True)

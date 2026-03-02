# NewsRag: Persona-Driven News Summarization Engine

NewsRag is an advanced Retrieval-Augmented Generation (RAG) application that leverages local Large Language Models (LLMs) to provide customized news summaries. By integrating real-time data from NewsAPI with local inference via Ollama, the system ensures data privacy while providing grounded, up-to-date information across various analytical personas.

## Architecture and Key Features

### Technical Architecture
The application is built on a decoupled architecture comprising:
*   **Frontend**: A responsive React application built with Vite, utilizing a modern dark-themed interface and Lucide-React for iconography.
*   **Backend**: A Flask-based REST API that orchestrates the data flow between the web interface and the AI core.
*   **AI Core**: Built with LangChain and Ollama, utilizing ChromaDB for high-performance vector storage and retrieval.

### Core Capabilities
*   **Real-time Intelligence**: Integrates directly with NewsAPI to retrieve the latest articles on any subject.
*   **Semantic Search**: Utilizes the `nomic-embed-text` model to create high-dimensional embeddings, enabling conceptual search beyond simple keyword matching.
*   **Persona-Based Adaptation**: Supports three distinct analytical frameworks for summarization:
    *   **Reporter**: Objective, factual, and neutral reporting.
    *   **Visionary**: Innovation-focused with an emphasis on positive societal impact.
    *   **Skeptic**: Critical analysis focusing on risks, contradictions, and potential downsides.
*   **Local Inference**: All embedding and summarization processes occur locally using Ollama, ensuring that sensitive data and search intent never leave the local environment.

## Prerequisites

*   Python 3.10 or higher
*   Node.js 18 or higher
*   Ollama installed and running
*   Required Ollama Models:
    *   `qwen2.5:0.5b` (Summarization engine)
    *   `nomic-embed-text` (Embedding engine)
*   NewsAPI Key (obtainable at [newsapi.org](https://newsapi.org/))

## Installation and Configuration

### Environment Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/harb993/NewsRag.git
   cd NewsRag
   ```

2. Create and activate a virtual environment:
   ```bash
   conda create -n newsrag python=3.11
   conda activate newsrag
   ```

3. Install backend dependencies:
   ```bash
   pip install langchain langchain-community langchain-ollama chromadb requests python-dotenv flask flask-cors
   ```

4. Configure environment variables:
   Create a `.env` file in the root directory and add your NewsAPI key:
   ```env
   NEWS_API_KEY=your_news_api_key_here
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Execution

### Starting the Backend
From the root directory, execute the following:
```bash
python app.py
```
The Flask server will initialize on `http://localhost:5000`.

### Starting the Frontend
From the `frontend` directory, execute:
```bash
npm run dev
```
The web interface will be accessible at `http://localhost:5173`.

## Technical Implementation Details

The system employs a Retrieval-Augmented Generation (RAG) workflow to mitigate LLM hallucinations. When a query is processed:
1. Articles are retrieved via REST API.
2. Content is partitioned and embedded into a ChromaDB vector store.
3. Relevant context is retrieved through similarity search.
4. The selected Persona's system prompt is injected into the LangChain transformation chain.
5. The local LLM generates a grounded summary based strictly on the retrieved context.

## License
Open source under the MIT License.

import { useState, useEffect } from 'react'
import { Search, History, Bookmark, Loader2, Send, ChevronRight, LayoutList, TextQuote, Newspaper, Sparkles, ShieldQuestion } from 'lucide-react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [summary, setSummary] = useState('')
  const [summaryType, setSummaryType] = useState('short')
  const [persona, setPersona] = useState('reporter')
  const [loading, setLoading] = useState(false)
  const [topics, setTopics] = useState([])
  const [history, setHistory] = useState([])
  const [articles, setArticles] = useState([])

  const API_BASE = 'http://localhost:5000/api'

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const prefRes = await fetch(`${API_BASE}/preferences`)
      const prefData = await prefRes.json()
      setTopics(prefData.topics || [])

      const histRes = await fetch(`${API_BASE}/history`)
      const histData = await histRes.json()
      setHistory(histData.history || [])
    } catch (err) {
      console.error("Failed to fetch data", err)
    }
  }

  const handleSearch = async (e) => {
    e?.preventDefault()
    if (!query) return
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      const data = await res.json()
      if (!res.ok) {
        alert(data.error || "Search failed")
        return
      }
      setArticles(data.articles || [])
      setSummary('') // Clear previous summary
      fetchData() // Update history
    } catch (err) {
      alert("Search failed. Is the backend running?")
    } finally {
      setLoading(false)
    }
  }

  const handleSummarize = async () => {
    if (!query) return
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/summarize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, type: summaryType, persona })
      })
      const data = await res.json()
      if (!res.ok) {
        alert(data.error || "Summarization failed")
        return
      }
      setSummary(data.summary)
    } catch (err) {
      alert("Summarization failed.")
    } finally {
      setLoading(false)
    }
  }

  const addTopic = async (topic) => {
    try {
      await fetch(`${API_BASE}/preferences`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic })
      })
      fetchData()
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="app-container">
      <header className="header">
        <h1>News Summarizer <span className="badge">AI</span></h1>
        <p className="subtitle">Locally powered by LangChain & Ollama</p>
      </header>

      <main className="main-layout">
        <section className="interaction-zone">
          <form className="search-bar glass" onSubmit={handleSearch}>
            <Search className="icon-faded" size={20} />
            <input
              type="text"
              placeholder="Search news topics..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button type="submit" disabled={loading}>
              {loading ? <Loader2 className="spinner" size={20} /> : <Send size={20} />}
            </button>
          </form>

          {articles.length > 0 && (
            <div className="summary-controls glass">
              <div className="control-section">
                <label>Persona</label>
                <div className="toggle-group personas">
                  <button
                    className={persona === 'reporter' ? 'active' : ''}
                    onClick={() => setPersona('reporter')}
                    title="Professional Reporter"
                  >
                    <Newspaper size={16} /> Reporter
                  </button>
                  <button
                    className={persona === 'visionary' ? 'active' : ''}
                    onClick={() => setPersona('visionary')}
                    title="Tech Visionary"
                  >
                    <Sparkles size={16} /> Visionary
                  </button>
                  <button
                    className={persona === 'skeptic' ? 'active' : ''}
                    onClick={() => setPersona('skeptic')}
                    title="Critical Skeptic"
                  >
                    <ShieldQuestion size={16} /> Skeptic
                  </button>
                </div>
              </div>

              <div className="control-section">
                <label>Format</label>
                <div className="toggle-group">
                  <button
                    className={summaryType === 'short' ? 'active' : ''}
                    onClick={() => setSummaryType('short')}
                  >
                    <LayoutList size={16} /> Brief
                  </button>
                  <button
                    className={summaryType === 'detailed' ? 'active' : ''}
                    onClick={() => setSummaryType('detailed')}
                  >
                    <TextQuote size={16} /> Detailed
                  </button>
                </div>
              </div>

              <button
                className="btn-primary"
                onClick={handleSummarize}
                disabled={loading}
              >
                Generate Summary
              </button>
            </div>
          )}

          {summary && (
            <div className="summary-display glass animate-fade-in">
              <h3>Summary</h3>
              <p>{summary}</p>
            </div>
          )}

          {articles.length > 0 && (
            <div className="articles-list">
              <h3>Recent Articles</h3>
              {articles.map((art, i) => (
                <div key={i} className="article-card glass">
                  <div className="article-content">
                    <h4>{art.title}</h4>
                    <p>{art.source}</p>
                  </div>
                  <ChevronRight size={16} className="icon-faded" />
                </div>
              ))}
            </div>
          )}
        </section>

        <aside className="sidebar">
          <div className="sidebar-section glass">
            <div className="section-header">
              <Bookmark size={18} /> <h3>Saved Topics</h3>
            </div>
            <div className="tags">
              {topics.map((t, i) => (
                <span key={i} className="tag" onClick={() => { setQuery(t); handleSearch() }}>
                  {t}
                </span>
              ))}
              {topics.length === 0 && <p className="empty">No topics saved</p>}
            </div>
          </div>

          <div className="sidebar-section glass">
            <div className="section-header">
              <History size={18} /> <h3>History</h3>
            </div>
            <ul className="history-list">
              {history.map((h, i) => (
                <li key={i} onClick={() => { setQuery(h); handleSearch() }}>
                  {h}
                </li>
              ))}
              {history.length === 0 && <p className="empty">No history yet</p>}
            </ul>
          </div>
        </aside>
      </main>
    </div>
  )
}

export default App

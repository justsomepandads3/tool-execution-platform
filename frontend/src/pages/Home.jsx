/**
 * Home Page Component
 *
 * WHAT THIS PAGE DOES:
 * - Fetches the list of available tools from the backend
 * - Displays all tools as clickable cards
 * - Handles loading and error states
 *
 * HOW IT WORKS:
 * 1. On component mount, fetches /api/tools
 * 2. Stores tools in state
 * 3. Renders ToolCard for each tool
 * 4. Shows loading spinner while fetching
 * 5. Shows error message if fetch fails
 *
 * DATA FLOW:
 * Backend (/api/tools) → getTools() → tools state → map to ToolCard components
 *
 * WHAT NOT TO MODIFY:
 * - Do not hardcode tool list
 * - Do not add tool-specific logic
 * - All tool information comes from the backend
 */

import { useState, useEffect } from 'react'
import { getTools } from '../api/client'
import { ToolCard } from '../components/ToolCard'
import './Home.css'

export function Home() {
  // State management
  const [tools, setTools] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch tools on component mount
  useEffect(() => {
    const fetchTools = async () => {
      try {
        setLoading(true)
        const response = await getTools()

        // Backend returns: { tools: [...], count: number }
        setTools(response.data.tools || [])
        setError(null)
      } catch (err) {
        console.error('Failed to fetch tools:', err)
        setError(
          err.response?.data?.error ||
            'Failed to load tools. Please check the backend connection.'
        )
        setTools([])
      } finally {
        setLoading(false)
      }
    }

    fetchTools()
  }, [])

  // Render loading state
  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-spinner">
          <h2>⏳ Loading tools...</h2>
        </div>
      </div>
    )
  }

  // Render error state
  if (error) {
    return (
      <div className="page-container">
        <div className="error-message">
          <h2>❌ Error Loading Tools</h2>
          <p>{error}</p>
          <p className="error-hint">
            Make sure the backend is running at{' '}
            <code>{import.meta.env.VITE_API_BASE_URL}</code>
          </p>
          <button
            onClick={() => window.location.reload()}
            className="retry-button"
          >
            🔄 Retry
          </button>
        </div>
      </div>
    )
  }

  // Render empty state
  if (tools.length === 0) {
    return (
      <div className="page-container">
        <div className="empty-state">
          <h2>📭 No Tools Available</h2>
          <p>Check your backend connection and make sure tools are registered.</p>
        </div>
      </div>
    )
  }

  // Render tools grid
  return (
    <div className="page-container">
      <div className="home-header">
        <h1>🛠 Available Tools</h1>
        <p className="tools-count">{tools.length} tool(s) available</p>
      </div>

      <div className="tools-grid">
        {tools.map((tool) => (
          <ToolCard key={tool.name} tool={tool} />
        ))}
      </div>
    </div>
  )
}

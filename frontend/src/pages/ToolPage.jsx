/**
 * Tool Page Component
 *
 * WHAT THIS PAGE DOES:
 * - Displays a specific tool and its execution interface
 * - Fetches tool metadata from the backend
 * - Renders the dynamic form with the tool's input schema
 * - Executes the tool
 * - Displays the result
 *
 * HOW IT WORKS:
 * 1. Extracts tool name from URL params (/tool/:toolName)
 * 2. Fetches tool metadata on mount
 * 3. Renders tool information
 * 4. Shows DynamicForm with tool's input schema
 * 5. On form submit:
 *    - Calls runTool() API
 *    - Passes FormData or JSON based on inputs
 *    - Displays result in ResultViewer
 *
 * DATA FLOW:
 * URL param → toolName
 * getToolMetadata(toolName) → tool state
 * → render DynamicForm with tool.input_schema
 * → onFormSubmit → runTool(toolName, formData)
 * → response → ResultViewer
 *
 * WHAT NOT TO MODIFY:
 * - Do not hardcode tool-specific logic
 * - Do not modify form data before submission
 * - All tool logic should be generic
 */

import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getToolMetadata, runTool } from '../api/client'
import { DynamicForm } from '../components/DynamicForm'
import { ResultViewer } from '../components/ResultViewer'
import './ToolPage.css'

export function ToolPage() {
  // Get tool name from URL
  const { toolName } = useParams()
  const navigate = useNavigate()

  // State management
  const [tool, setTool] = useState(null)
  const [loading, setLoading] = useState(true)
  const [fetching, setFetching] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  // Fetch tool metadata on mount
  useEffect(() => {
    const fetchTool = async () => {
      try {
        setLoading(true)
        const response = await getToolMetadata(toolName)
        setTool(response.data)
        setError(null)
      } catch (err) {
        console.error('Failed to fetch tool:', err)
        setError(
          err.response?.data?.error ||
            'Failed to load tool. Please check the tool name.'
        )
        setTool(null)
      } finally {
        setLoading(false)
      }
    }

    fetchTool()
  }, [toolName])

  // Handle form submission
  const handleFormSubmit = async (formData) => {
    try {
      setFetching(true)
      setError(null)

      // Call the API to run the tool
      const response = await runTool(toolName, formData)

      // Store the response for ResultViewer
      // The response is a blob, but we need the headers too
      setResult(response)
    } catch (err) {
      console.error('Tool execution failed:', err)

      // Try to get error message from backend
      if (err.response?.data) {
        try {
          const reader = new FileReader()
          reader.onload = (e) => {
            try {
              const errorData = JSON.parse(e.target.result)
              setError(
                errorData.error || 'Tool execution failed. Please try again.'
              )
            } catch {
              setError('Tool execution failed. Please try again.')
            }
          }
          reader.readAsText(err.response.data)
        } catch {
          setError('Tool execution failed. Please try again.')
        }
      } else {
        setError(
          err.message || 'Network error. Please check your connection.'
        )
      }
    } finally {
      setFetching(false)
    }
  }

  // Render loading state
  if (loading) {
    return (
      <div className="page-container">
        <button onClick={() => navigate('/')} className="back-button">
          ← Back to Tools
        </button>
        <div className="loading-spinner">
          <h2>⏳ Loading tool...</h2>
        </div>
      </div>
    )
  }

  // Render error state
  if (!tool || error) {
    return (
      <div className="page-container">
        <button onClick={() => navigate('/')} className="back-button">
          ← Back to Tools
        </button>
        <div className="error-message">
          <h2>❌ Error</h2>
          <p>{error || 'Tool not found.'}</p>
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

  // Render tool page with form or result
  return (
    <div className="page-container">
      <button onClick={() => navigate('/')} className="back-button">
        ← Back to Tools
      </button>

      <div className="tool-header">
        <h1>{tool.name}</h1>
        <p className="tool-description">{tool.description}</p>
        <p className="tool-meta">
          Version: {tool.version} • Output: {tool.output_type}
        </p>
      </div>

      {/* Show form if no result yet, or show both form and result */}
      {!result && (
        <DynamicForm
          inputSchema={tool.input_schema}
          onSubmit={handleFormSubmit}
          isLoading={fetching}
        />
      )}

      {/* Show result if available */}
      {result && (
        <>
          <ResultViewer
            response={result}
            toolName={tool.name}
            onClose={() => setResult(null)}
          />

          {/* Show form again after result to allow re-running */}
          <div className="rerun-section">
            <h3>Run Again</h3>
            <DynamicForm
              inputSchema={tool.input_schema}
              onSubmit={handleFormSubmit}
              isLoading={fetching}
            />
          </div>
        </>
      )}

      {/* Show errors that happen during execution */}
      {error && !loading && (
        <div className="execution-error">
          <p>❌ {error}</p>
        </div>
      )}
    </div>
  )
}

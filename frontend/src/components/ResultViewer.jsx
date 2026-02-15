/**
 * ResultViewer Component
 *
 * WHAT THIS COMPONENT DOES:
 * - Displays the result of a tool execution
 * - Handles both JSON and file responses
 * - Shows pretty-printed JSON
 * - Creates download links for files
 *
 * HOW IT WORKS:
 * 1. Receives response blob from API
 * 2. Checks the Content-Type header
 * 3. If JSON: parses and displays formatted
 * 4. If file: creates blob URL and download link
 *
 * PROPS:
 * - response: axios response object
 * - toolName: string - name of the tool (used for filename)
 * - onClose: function - callback to close the result viewer
 *
 * RESPONSE STRUCTURE:
 * The Axios response has:
 * - response.data: the actual data (Blob in our case)
 * - response.headers: object with Content-Type, X-File-Extension, etc.
 * - response.status: HTTP status code
 *
 * BACKEND HEADERS FOR FILES:
 * - content-type: proper media type (image/png, image/jpeg, etc.)
 * - x-file-extension: file extension (e.g., .png, .jpg)
 * - x-file-name: full filename with extension
 *
 * FILE HANDLING:
 * - For file responses: creates a Blob object
 * - Uses extension from backend headers (x-file-extension)
 * - Creates a temporary download URL
 * - Creates a download link for the user
 * - Cleans up the URL when done
 *
 * WHAT NOT TO MODIFY:
 * - Do not hardcode file types
 * - Do not modify blob handling
 * - Do not assume response structure
 */

import { useState, useEffect } from 'react'
import './ResultViewer.css'

export function ResultViewer({ response, toolName, onClose }) {
  const [result, setResult] = useState(null)
  const [isFile, setIsFile] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!response) return

    try {
      // Get the content type from response headers
      const contentType = response.headers['content-type'] || ''

      if (contentType.includes('application/json')) {
        // Handle JSON response
        setIsFile(false)

        // Read blob as text and parse JSON
        const reader = new FileReader()
        reader.onload = (e) => {
          try {
            const jsonData = JSON.parse(e.target.result)
            setResult(jsonData)
          } catch (err) {
            setError('Failed to parse JSON response')
          }
        }
        reader.readAsText(response.data)
      } else {
        // Handle file response
        setIsFile(true)

        // Get custom headers from backend
        // These headers tell us the file extension and name
        const xFileExtension = response.headers['x-file-extension'] || ''
        const xFileName = response.headers['x-file-name'] || ''

        // Fallback: Extract filename from Content-Disposition header
        const contentDisposition = response.headers['content-disposition'] || ''
        let filename = toolName + '_result'
        let extension = xFileExtension

        // Prefer backend's filename if available
        if (xFileName) {
          filename = xFileName
        } else if (contentDisposition) {
          // Try to extract filename from: attachment; filename="name.ext"
          const filenameMatch = contentDisposition.match(
            /filename="?([^"]+)"?/
          )
          if (filenameMatch) {
            filename = filenameMatch[1]
          }
        }

        // Extract extension from filename if backend didn't provide it
        if (!extension && filename) {
          const dotIndex = filename.lastIndexOf('.')
          if (dotIndex > -1) {
            extension = filename.substring(dotIndex)
          }
        }

        setResult({
          blob: response.data,
          filename: filename,
          extension: extension,
          size: response.data.size,
          type: contentType,
        })
      }
    } catch (err) {
      setError('Failed to process result: ' + err.message)
    }
  }, [response, toolName])

  if (error) {
    return (
      <div className="result-viewer">
        <div className="result-error">
          <h3>❌ Error</h3>
          <p>{error}</p>
          <button onClick={onClose} className="result-close-button">
            Close
          </button>
        </div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="result-viewer">
        <div className="result-loading">
          <p>⏳ Processing result...</p>
        </div>
      </div>
    )
  }

  if (isFile) {
    return (
      <div className="result-viewer">
        <div className="result-file">
          <h3>✅ File Ready for Download</h3>

          <div className="file-info">
            <p>
              <strong>Filename:</strong> {result.filename}
            </p>
            {result.extension && (
              <p>
                <strong>Extension:</strong> {result.extension}
              </p>
            )}
            <p>
              <strong>Size:</strong> {(result.size / 1024).toFixed(2)} KB
            </p>
            <p>
              <strong>Type:</strong> {result.type || 'binary file'}
            </p>
          </div>

          <button
            onClick={() => {
              // Create a temporary download link
              const url = window.URL.createObjectURL(result.blob)
              const link = document.createElement('a')
              link.href = url
              link.download = result.filename
              document.body.appendChild(link)
              link.click()

              // Clean up
              document.body.removeChild(link)
              window.URL.revokeObjectURL(url)
            }}
            className="download-button"
          >
            ⬇ Download File
          </button>

          <button onClick={onClose} className="result-close-button">
            Close
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="result-viewer">
      <div className="result-json">
        <h3>✅ Tool Executed Successfully</h3>

        <div className="json-output">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>

        <button
          onClick={() => {
            // Copy JSON to clipboard
            navigator.clipboard.writeText(JSON.stringify(result, null, 2))
            alert('Copied to clipboard!')
          }}
          className="copy-button"
        >
          📋 Copy JSON
        </button>

        <button onClick={onClose} className="result-close-button">
          Close
        </button>
      </div>
    </div>
  )
}

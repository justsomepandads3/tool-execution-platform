/**
 * App Component
 *
 * WHAT THIS COMPONENT DOES:
 * - Sets up React Router with two main pages
 * - Provides app header and layout
 * - Routes:
 *   / → Home (tool listing)
 *   /tool/:toolName → Tool execution page
 *
 * HOW IT WORKS:
 * - Uses BrowserRouter from react-router-dom
 * - Defines routes for Home and ToolPage
 * - Renders a header with app name
 * - Uses Outlet to render page content
 *
 * WHAT NOT TO MODIFY:
 * - Do not add tool-specific routes
 * - Do not hardcode navigations
 * - Keep routing simple and generic
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Home } from './pages/Home'
import { ToolPage } from './pages/ToolPage'
import './App.css'

function App() {
  const appName = import.meta.env.VITE_APP_NAME || 'Tool Execution Platform'

  return (
    <BrowserRouter>
      <div className="app">
        {/* Header */}
        <header className="app-header">
          <div className="header-container">
            <h1 className="app-title">
              <a href="/" className="app-logo">
                🛠 {appName}
              </a>
            </h1>
            <p className="app-subtitle">
              Unified platform for executing utility tools
            </p>
          </div>
        </header>

        {/* Main Content */}
        <main className="app-main">
          <Routes>
            {/* Home page - shows list of tools */}
            <Route path="/" element={<Home />} />

            {/* Tool page - shows form to execute a specific tool */}
            <Route path="/tool/:toolName" element={<ToolPage />} />

            {/* Catch-all 404 */}
            <Route
              path="*"
              element={
                <div className="page-container">
                  <div className="error-message">
                    <h2>❌ Page Not Found</h2>
                    <p>The page you're looking for doesn't exist.</p>
                    <a href="/" className="back-button">
                      ← Back to Home
                    </a>
                  </div>
                </div>
              }
            />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="app-footer">
          <p>
            A modular tool execution platform built with React + FastAPI
          </p>
        </footer>
      </div>
    </BrowserRouter>
  )
}

export default App

/**
 * Main Entry Point for the React Application
 *
 * WHAT THIS FILE DOES:
 * - Initializes React
 * - Mounts the App component to the DOM
 * - Loads global styles
 *
 * HOW IT WORKS:
 * 1. Imports React and ReactDOM
 * 2. Imports the App component
 * 3. Imports global CSS
 * 4. Creates a React root at #root element
 * 5. Renders the App component
 *
 * WHAT NOT TO MODIFY:
 * - Do not change the root element ID (#root)
 * - Do not add global state here
 * - Keep this file simple
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)

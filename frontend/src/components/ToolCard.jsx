/**
 * ToolCard Component
 *
 * WHAT THIS COMPONENT DOES:
 * - Displays a single tool as a clickable card
 * - Shows tool name, description, and version
 * - Links to the tool's execution page
 *
 * PROPS:
 * - tool: object with { name, description, version }
 *
 * HOW IT WORKS:
 * - Uses React Router's Link to navigate to /tool/{name}
 * - Styling is minimal CSS for a card layout
 * - No tool-specific logic - works with any tool
 *
 * WHAT NOT TO MODIFY:
 * - Do not hardcode tool names or behaviors
 * - Do not add tool-specific icons or descriptions
 */

import { Link } from 'react-router-dom'
import './ToolCard.css'

export function ToolCard({ tool }) {
  return (
    <Link to={`/tool/${tool.name}`} className="tool-card-link">
      <div className="tool-card">
        <h3 className="tool-card-title">{tool.name}</h3>
        <p className="tool-card-description">{tool.description}</p>
        <p className="tool-card-version">v{tool.version}</p>
        <button className="tool-card-button">Run Tool →</button>
      </div>
    </Link>
  )
}

/**
 * API Client for the Tool Execution Platform Frontend
 *
 * This file creates an Axios instance that communicates with the backend API.
 *
 * WHAT THIS FILE DOES:
 * - Creates an Axios instance with the backend URL from .env
 * - Provides helper functions to call the backend API
 * - Handles both JSON and file responses
 * - Includes debug logging when VITE_DEBUG is enabled
 *
 * HOW ENVIRONMENT VARIABLES WORK:
 * - In Vite, environment variables must start with VITE_
 * - They are imported using: import.meta.env.VITE_VARIABLE_NAME
 * - Variables are replaced at build time
 * - They are safe to expose (no secrets here)
 *
 * HOW TO CHANGE THE BACKEND URL:
 * 1. Open the .env file in the project root
 * 2. Change VITE_API_BASE_URL to your backend URL
 * 3. No code changes needed - Vite will reload automatically
 *
 * WHAT NOT TO MODIFY:
 * - Do not remove import.meta.env usage
 * - Do not hardcode URLs in this file
 * - Do not add API keys or secrets here
 */

import axios from 'axios'

// Get the backend URL from environment variables
// If VITE_API_BASE_URL is not set, default to localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const DEBUG = import.meta.env.VITE_DEBUG === 'true'

// Log the API base URL when in debug mode
if (DEBUG) {
  console.log('🔌 API Base URL:', API_BASE_URL)
}

// Create the Axios instance with the backend URL
// This instance is used for all API calls
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout
})

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    if (DEBUG) {
      console.log(`📤 API Request: ${config.method.toUpperCase()} ${config.url}`)
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Add response interceptor for logging
apiClient.interceptors.response.use(
  (response) => {
    if (DEBUG) {
      console.log(`📥 API Response: ${response.status} ${response.config.url}`)
    }
    return response
  },
  (error) => {
    if (DEBUG) {
      console.error('❌ API Error:', error.response?.status, error.message)
    }
    return Promise.reject(error)
  }
)

/**
 * Fetch the list of all available tools
 * Calls: GET /api/tools
 *
 * Returns:
 * - Array of tool objects with: name, description, version, input_schema, output_type
 */
export function getTools() {
  return apiClient.get('/api/system/tools')
}

/**
 * Fetch metadata for a specific tool
 * Calls: GET /api/tools/{tool_name}
 *
 * Args:
 * - toolName: string - the name of the tool
 *
 * Returns:
 * - Tool object with: name, description, version, input_schema, output_type
 */
export function getToolMetadata(toolName) {
  return apiClient.get(`/api/system/tools/${toolName}`)
}

/**
 * Execute a tool with the provided input
 * Calls: POST /api/tools/{tool_name}/run
 *
 * This function automatically handles both JSON and FormData:
 * - If formData is provided, sends as multipart/form-data
 * - Otherwise, sends as application/json
 *
 * Args:
 * - toolName: string - the name of the tool to run
 * - data: object or FormData - the input data
 *
 * Returns:
 * - For JSON output: response.data (the JSON result)
 * - For file output: response.data (Blob object - will be handled by ResultViewer)
 */
export function runTool(toolName, data) {
  const config = {}

  // If data is FormData, let Axios handle the content-type automatically
  // FormData is used when there's a file input
  if (data instanceof FormData) {
    config.headers = {
      'Content-Type': 'multipart/form-data',
    }
  }
  // Otherwise, send as JSON
  else {
    config.headers = {
      'Content-Type': 'application/json',
    }
  }

  if (DEBUG) {
    console.log(
      `🚀 Running tool: ${toolName}`,
      data instanceof FormData ? '(with file)' : '(JSON)'
    )
  }

  return apiClient.post(`/api/system/tools/${toolName}/run`, data, {
    ...config,
    responseType: 'blob', // Get response as blob to handle both JSON and files
  })
}

/**
 * Fetch health status
 * Calls: GET /api/system/health
 *
 * Returns:
 * - { status: "ok" }
 */
export function getHealth() {
  return apiClient.get('/api/system/health')
}

export default apiClient

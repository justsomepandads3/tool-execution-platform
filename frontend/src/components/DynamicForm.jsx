/**
 * DynamicForm Component
 *
 * WHAT THIS COMPONENT DOES:
 * - Generates a form dynamically from a JSON schema
 * - Supports string, number, and file input types
 * - Automatically detects if file input is present
 * - Submits as JSON or FormData depending on inputs
 *
 * HOW IT WORKS:
 * 1. Receives input_schema from the backend
 * 2. Loops through schema properties
 * 3. Creates appropriate input elements (text, number, file)
 * 4. Handles form submission:
 *    - If file input exists: creates FormData
 *    - Otherwise: sends as JSON
 * 5. Calls onSubmit with the form data
 *
 * SCHEMA FORMAT (from backend):
 * {
 *   "type": "object",
 *   "properties": {
 *     "data": {
 *       "type": "string",
 *       "description": "Data to encode...",
 *       "example": "Hello"
 *     },
 *     "quality": {
 *       "type": "integer",
 *       "description": "Quality...",
 *       "default": 85
 *     }
 *   },
 *   "required": ["data"]
 * }
 *
 * PROPS:
 * - inputSchema: object - the JSON schema from backend
 * - onSubmit: function - callback(data) called when form is submitted
 * - isLoading: boolean - true while tool is executing
 *
 * TO EXTEND FOR NEW INPUT TYPES:
 * 1. Add a new case in the type switch statement
 * 2. Create the appropriate HTML input element
 * 3. Add to formData in handleSubmit
 *
 * WHAT NOT TO MODIFY:
 * - Do not hardcode input names or types
 * - Do not add tool-specific validation
 * - Keep all logic generic for any tool
 */

import { useState } from 'react'
import './DynamicForm.css'

export function DynamicForm({ inputSchema, onSubmit, isLoading }) {
  // Store form values in state
  const [formValues, setFormValues] = useState({})

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value, type, files } = e.target

    if (type === 'file') {
      // For file inputs, store the file object
      setFormValues({
        ...formValues,
        [name]: files[0],
      })
    } else {
      // For text/number inputs, store the string value
      setFormValues({
        ...formValues,
        [name]: value,
      })
    }
  }

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault()

    // Check if any file inputs exist in the schema
    const hasFileInput = Object.values(inputSchema.properties || {}).some(
      (prop) => prop.type === 'file'
    )

    let dataToSubmit

    if (hasFileInput) {
      // If there are file inputs, create FormData for multipart submission
      dataToSubmit = new FormData()

      // Add all form values to FormData
      Object.keys(formValues).forEach((key) => {
        const value = formValues[key]
        if (value !== undefined && value !== '') {
          if (value instanceof File) {
            // For file inputs, append the file
            dataToSubmit.append(key, value)
          } else {
            // For other inputs, append as string
            dataToSubmit.append(key, value)
          }
        }
      })
    } else {
      // If no files, send as JSON
      // Filter out empty values
      dataToSubmit = {}
      Object.keys(formValues).forEach((key) => {
        const value = formValues[key]
        if (value !== undefined && value !== '') {
          // Convert to appropriate type based on schema
          const property = inputSchema.properties[key]
          if (property.type === 'number' || property.type === 'integer') {
            dataToSubmit[key] = Number(value)
          } else {
            dataToSubmit[key] = value
          }
        }
      })
    }

    // Call the parent's submit handler
    onSubmit(dataToSubmit)
  }

  // Extract properties from schema
  const properties = inputSchema.properties || {}
  const required = inputSchema.required || []

  return (
    <form onSubmit={handleSubmit} className="dynamic-form">
      <div className="form-fields">
        {Object.entries(properties).map(([fieldName, fieldSchema]) => {
          const isRequired = required.includes(fieldName)
          const fieldType = fieldSchema.type || 'string'

          return (
            <div key={fieldName} className="form-group">
              <label htmlFor={fieldName} className="form-label">
                {fieldName}
                {isRequired && <span className="required"> *</span>}
              </label>

              {fieldSchema.description && (
                <p className="form-description">{fieldSchema.description}</p>
              )}

              {/* Render different input types based on schema */}
              {fieldType === 'string' && (
                <>
                  {fieldSchema.enum ? (
                    // If enum is specified, render as select dropdown
                    <select
                      id={fieldName}
                      name={fieldName}
                      value={formValues[fieldName] || ''}
                      onChange={handleInputChange}
                      required={isRequired}
                      className="form-input"
                    >
                      <option value="">-- Select {fieldName} --</option>
                      {fieldSchema.enum.map((option) => (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      ))}
                    </select>
                  ) : (
                    // Otherwise render as text input
                    <input
                      id={fieldName}
                      type="text"
                      name={fieldName}
                      value={formValues[fieldName] || ''}
                      onChange={handleInputChange}
                      placeholder={fieldSchema.example || `Enter ${fieldName}`}
                      required={isRequired}
                      className="form-input"
                    />
                  )}
                </>
              )}

              {(fieldType === 'number' || fieldType === 'integer') && (
                <input
                  id={fieldName}
                  type="number"
                  name={fieldName}
                  value={formValues[fieldName] || ''}
                  onChange={handleInputChange}
                  placeholder={fieldSchema.example || `Enter ${fieldName}`}
                  min={fieldSchema.minimum}
                  max={fieldSchema.maximum}
                  required={isRequired}
                  className="form-input"
                />
              )}

              {fieldType === 'file' && (
                <input
                  id={fieldName}
                  type="file"
                  name={fieldName}
                  onChange={handleInputChange}
                  required={isRequired}
                  className="form-input"
                />
              )}
            </div>
          )
        })}
      </div>

      {Object.keys(properties).length === 0 && (
        <p className="no-inputs">This tool requires no inputs.</p>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="form-submit-button"
      >
        {isLoading ? '⏳ Running...' : '▶ Run Tool'}
      </button>
    </form>
  )
}

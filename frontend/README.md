# Tool Execution Platform - Frontend

A clean, beginner-friendly React + Vite frontend for the Tool Execution Platform backend.

## Overview

This frontend provides a unified interface for executing tools from your backend:

- **Dynamic Tool Discovery**: Automatically fetches available tools from the backend
- **Schema-Driven Forms**: Generates forms dynamically from backend input schemas
- **No Hardcoding**: All tool information comes from the backend (zero tool-specific code)
- **Flexible Responses**: Handles both JSON and file responses
- **Environment-Configurable**: All backend URLs via `.env` file
- **Beginner-Friendly**: Clean code with detailed comments explaining every concept

## Features

- 🛠 Browse all available tools from backend
- 📝 Dynamically generated forms based on tool schemas
- 📤 Support for JSON and file uploads
- 📥 Handle JSON and file download responses
- 🎨 Clean, responsive UI
- 🔗 React Router for navigation
- 📝 Comprehensive error handling
- 🔌 Easy backend URL configuration via `.env`

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool (fast, modern)
- **Axios** - HTTP client
- **React Router** - Navigation
- **Vanilla CSS** - Styling (no heavy frameworks)

## Project Structure

```
frontend/
├── .env                        # Environment variables (CREATE THIS)
├── index.html                  # HTML entry point
├── package.json                # Dependencies
├── vite.config.js              # Vite configuration
│
├── src/
│   ├── main.jsx                # React entry point
│   ├── App.jsx                 # Main app component
│   ├── App.css                 # App styles
│   ├── index.css               # Global styles
│   │
│   ├── api/
│   │   └── client.js           # Axios API client
│   │
│   ├── components/
│   │   ├── ToolCard.jsx        # Tool card display
│   │   ├── ToolCard.css
│   │   ├── DynamicForm.jsx     # Schema-driven form
│   │   ├── DynamicForm.css
│   │   ├── ResultViewer.jsx    # Result display
│   │   └── ResultViewer.css
│   │
│   └── pages/
│       ├── Home.jsx            # Tool listing page
│       ├── Home.css
│       ├── ToolPage.jsx        # Tool execution page
│       └── ToolPage.css
│
└── README.md                   # This file
```

## Installation & Setup

### Prerequisites

- Node.js 16+ and npm (or yarn)
- Backend running at `http://localhost:8000` (or configured via `.env`)

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

### Step 2: Configure Environment

Create a `.env` file in the `frontend/` directory:

```env
# Backend URL (change this to match your backend)
VITE_API_BASE_URL=http://localhost:8000

# Application name shown in header
VITE_APP_NAME=Modular Tool Platform

# Enable debug logging in browser console
VITE_DEBUG=true
```

**Important:** Environment variables must start with `VITE_` to be accessible in the frontend.

### Step 3: Start Development Server

```bash
npm run dev
```

The app will open at `http://localhost:5173`

### Step 4: Build for Production

```bash
npm run build
```

Output will be in the `dist/` folder.

To preview the production build:

```bash
npm run preview
```

## How Environment Variables Work in Vite

Vite exposes environment variables via `import.meta.env`:

```javascript
// BAD (won't work):
const url = process.env.VITE_API_BASE_URL  // ❌ undefined

// GOOD (works):
const url = import.meta.env.VITE_API_BASE_URL  // ✅ correct
```

**Key Points:**

1. Environment variables must start with `VITE_`
2. Access them using `import.meta.env.VITE_VARIABLE_NAME`
3. Variables are replaced at **build time**
4. For development, create a `.env` file
5. For production, set environment variables in your deployment platform

## Configuration Options

### `.env` File Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend API URL |
| `VITE_APP_NAME` | `Tool Execution Platform` | App title shown in header |
| `VITE_DEBUG` | `false` | Enable console logging |

### Changing Backend URL

**Development:**
1. Edit `.env` file
2. Change `VITE_API_BASE_URL` to your backend URL
3. Vite will auto-reload

**Production:**
1. Build the app with the correct environment variable
2. Example: `VITE_API_BASE_URL=https://api.example.com npm run build`

## How the Frontend Works

### 1. Home Page (`pages/Home.jsx`)

- Fetches `/api/tools` from backend on load
- Displays all tools as clickable cards
- Links to individual tool pages

### 2. Tool Page (`pages/ToolPage.jsx`)

- Fetches tool metadata from `/api/tools/{toolName}`
- Renders the tool information
- Shows `DynamicForm` with the tool's input schema

### 3. Dynamic Form (`components/DynamicForm.jsx`)

**This is the heart of the system!**

The form reads the backend's `input_schema` and dynamically generates inputs:

**Example Backend Schema:**

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "string",
      "description": "Data to encode"
    },
    "quality": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "default": 85
    }
  },
  "required": ["data"]
}
```

**Supported Input Types:**

- `string` - text input (or dropdown if `enum` is specified)
- `number` / `integer` - number input
- `file` - file upload input

**Form Submission:**

- If the schema has file inputs: submits as `FormData` (multipart)
- Otherwise: submits as JSON

### 4. Result Viewer (`components/ResultViewer.jsx`)

Handles all possible responses:

**For JSON Response:**
- Pretty-prints the JSON
- Shows "Copy" button
- No assumptions about structure

**For File Response:**
- Shows file info (name, size, type)
- Creates download link
- Uses Blob URLs for safe handling

## Adding a New Tool (Backend Side)

This frontend **requires zero code changes** when you add a new tool to the backend!

**Steps to add a tool:**

1. **Create the tool** in `backend/app/tools/` with the new tool code
2. **Register it** in `backend/app/core/tool_registry.py`
3. **Define input_schema** in the tool class
4. **Restart the backend**

That's it! The frontend will automatically:
- Fetch the new tool on the Home page
- Render the appropriate form based on `input_schema`
- Execute it correctly

## Component Guide

### ToolCard Component

Displays a single tool in a grid.

**Props:**
- `tool` - Tool object from backend

**Do NOT modify:**
- Don't add tool-specific logic
- Don't hardcode tool names

### DynamicForm Component

**Core concept:** Reads ANY JSON schema and renders a form.

**Props:**
- `inputSchema` - The tool's input_schema from backend
- `onSubmit` - Callback function with form data
- `isLoading` - Boolean, disables button while loading

**To add a new input type:**

1. Open `DynamicForm.jsx`
2. Find the comment: `Render different input types`
3. Add a new `if` block for the new type
4. Update the schema parsing logic in `handleSubmit`

Example for a new `boolean` type:

```javascript
{fieldType === 'boolean' && (
  <input
    id={fieldName}
    type="checkbox"
    name={fieldName}
    checked={formValues[fieldName] || false}
    onChange={handleInputChange}
    className="form-input"
  />
)}
```

### ResultViewer Component

Displays results from tool execution.

**Props:**
- `response` - Axios response object
- `toolName` - Tool name (for filename)
- `onClose` - Callback to close result

**How it detects response type:**
- Checks `Content-Type` header
- If `application/json`: displays JSON
- Otherwise: treats as file download

## API Client (`api/client.js`)

Provides helper functions to call the backend:

```javascript
// List all tools
const response = await getTools()
// Returns: { tools: [...], count: number }

// Get single tool metadata
const response = await getToolMetadata('qr-generator')
// Returns: { name, description, version, input_schema, output_type }

// Run a tool
const response = await runTool('qr-generator', { data: 'Hello' })
// For JSON output: response.data = { ... }
// For file output: response.data = Blob object

// Health check
const response = await getHealth()
// Returns: { status: 'ok' }
```

## Error Handling

The frontend gracefully handles errors:

1. **Network Errors**: Shows user-friendly message
2. **Backend Errors**: Displays error from response
3. **File Processing Errors**: Shows specific error
4. **Invalid Data**: Form validation errors

All error messages are safe for users to see (no technical stack traces).

## Styling Architecture

Uses **vanilla CSS** with CSS variables for easy customization.

**CSS Variables** (in `src/index.css`):

```css
--color-primary: #667eea
--color-success: #27ae60
--color-error: #e74c3c
--spacing-md: 16px
--radius-md: 8px
```

To change colors globally, edit these variables in `src/index.css`.

## Responsive Design

Built mobile-first with media queries:

- Responsive grid layout
- Touch-friendly buttons
- Proper spacing on all screen sizes
- Tested on mobile, tablet, desktop

## Troubleshooting

### Backend not responding

**Error:** "Failed to load tools. Please check the backend connection."

**Solution:**
1. Check backend is running: `http://localhost:8000/api/system/health`
2. Check `.env` has correct `VITE_API_BASE_URL`
3. Restart the dev server: `npm run dev`

### Form not showing inputs

**Issue:** Form appears but has no fields

**Possible causes:**
- Backend tool's `input_schema` is empty or malformed
- Check `GET /api/tools/{tool_name}` returns valid schema

### File download not working

**Issue:** File appears ready but doesn't download

**Possible causes:**
- Check browser console for errors
- Verify backend returns file with correct `Content-Type` header

### Environment variables not updating

**Issue:** Changed `.env` but values not updating

**Solution:**
- Restart dev server: `npm run dev`
- Clear browser cache if needed
- Environment variables are replaced at build time

## Code Style & Conventions

### Naming

- Components: PascalCase (`ToolCard.jsx`)
- Functions: camelCase (`handleFormSubmit`)
- Constants: UPPER_SNAKE_CASE (`API_BASE_URL`)
- CSS classes: kebab-case (`.tool-card`)

### Comments

Every file has:
1. Top-level comment explaining purpose
2. Section comments for major code blocks
3. Inline comments for complex logic
4. "What NOT to modify" section

### Component Structure

```jsx
/**
 * Component Name
 *
 * WHAT THIS DOES:
 * - Brief description
 *
 * PROPS:
 * - propName: type - description
 *
 * WHAT NOT TO MODIFY:
 * - Things beginners should avoid
 */

export function ComponentName({ prop1, prop2 }) {
  // Implementation
}
```

## Adding Custom Styling

To add custom styles:

1. Create a `.css` file next to the component
2. Use the CSS variables from `src/index.css`
3. Follow BEM naming convention: `.component-name` or `.component-name-child`

Example:

```css
.my-component {
  color: var(--color-text);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
}
```

## Extending the Frontend

### Add a New Page

1. Create `src/pages/MyPage.jsx`
2. Create `src/pages/MyPage.css`
3. Add route in `src/App.jsx`:

```javascript
<Route path="/my-page" element={<MyPage />} />
```

4. Add link in navigation

### Add a New Component

1. Create `src/components/MyComponent.jsx`
2. Create `src/components/MyComponent.css`
3. Import and use in pages

### Add a New Input Type to Forms

See "DynamicForm Component" section under "Component Guide" above.

## Performance

- **Lazy loading**: Not needed for small number of tools
- **Code splitting**: Happens automatically with Vite
- **Caching**: Browser caches API responses automatically
- **Bundling**: Vite optimizes for production

## Deployment

### Vercel (Recommended for Vite)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build and deploy
netlify deploy --prod
```

### Static Host (GitHub Pages, S3, etc.)

```bash
# Build for production
npm run build

# Upload dist/ folder to your host
```

**Important:** Set environment variables in your hosting platform's settings!

## Development Workflow

### 1. Local Development

```bash
npm run dev
```

- Hot reload on file changes
- Debug in browser DevTools

### 2. Testing in Browser

- Open http://localhost:5173
- Test with real backend at http://localhost:8000
- Check console for logs (if `VITE_DEBUG=true`)

### 3. Production Build

```bash
VITE_API_BASE_URL=https://api.example.com npm run build
npm run preview
```

### 4. Deploy

Push `dist/` folder to your hosting

## FAQ

**Q: Do I need to modify the frontend when I add a new tool?**
A: No! The frontend fetches tools from the backend and generates forms automatically.

**Q: Can I change the backend URL without rebuilding?**
A: Only for development. For production, set the env variable before building.

**Q: How do I add authentication?**
A: Modify `api/client.js` to add auth headers to requests.

**Q: Can I use TypeScript?**
A: Yes, but it's not needed for this project. Change `.jsx` to `.tsx` if you want.

**Q: How do I add a state management library?**
A: This project uses React hooks for simplicity. Add Redux/Zustand if you need it later.

## Support & Troubleshooting

1. **Check the logs**: Browser console and backend logs
2. **Verify backend**: Visit `/api/system/health`
3. **Check environment**: Review `.env` file
4. **Clear cache**: Hard refresh browser (Ctrl+Shift+R)

## License

Same as the backend project.

---

**Happy coding!** 🎉

This frontend is designed to be maintainable and easy to extend. All tool-specific logic comes from the backend—the frontend remains completely generic.

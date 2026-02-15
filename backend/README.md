# Tool Execution Platform

A modular FastAPI-based backend system for executing utility tools (QR generator, image converter, etc.).

## Overview

This is a clean, beginner-friendly backend platform that:

- Provides a unified API for running utility tools
- Has a simple modular architecture for adding new tools
- Supports both JSON and file upload input
- Returns either JSON responses or file downloads
- Uses FastAPI, Pydantic, Pillow, qrcode, and loguru
- Is production-aware but not overengineered

## Features

- **Tool Registry**: Simple manual registry of available tools
- **Base Tool System**: All tools inherit from `BaseTool` for consistency
- **File Handling**: Safe file upload handling with validation
- **Error Handling**: Centralized error handling that doesn't leak internal details
- **Logging**: Comprehensive logging with loguru
- **API Documentation**: Auto-generated Swagger docs at `/docs`

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app setup
│   ├── core/
│   │   ├── config.py          # Pydantic configuration
│   │   ├── base_tool.py       # BaseTool abstract class
│   │   ├── tool_registry.py   # Tool registry
│   │   └── exceptions.py      # Custom exceptions
│   ├── api/
│   │   ├── routes_tools.py    # Tool execution endpoints
│   │   └── routes_system.py   # System endpoints (health, listing)
│   ├── tools/
│   │   ├── qr_generator/
│   │   │   ├── tool.py
│   │   │   ├── logic.py
│   │   │   └── schemas.py
│   │   └── image_converter/
│   │       ├── tool.py
│   │       ├── logic.py
│   │       └── schemas.py
│   ├── services/
│   │   └── file_service.py    # File upload handling
│   └── utils/
│       └── helpers.py         # Utility functions
├── requirements.txt
├── Dockerfile
└── README.md
```

## Available Tools

### 1. QR Generator

Generate QR codes from text.

**Endpoint:** `POST /api/tools/qr-generator/run`

**Input (JSON):**
```json
{
  "data": "https://example.com"
}
```

**Output:** PNG image file

**Example:**
```bash
curl -X POST "http://localhost:8000/api/tools/qr-generator/run" \
  -H "Content-Type: application/json" \
  -d '{"data": "Hello World"}' \
  --output qr.png
```

### 2. Image Converter

Convert images between formats (PNG, JPG, WebP, GIF, BMP).

**Endpoint:** `POST /api/tools/image-converter/run`

**Input (multipart/form-data):**
- `file`: Image file to convert (upload)
- `target_format`: png, jpg, jpeg, webp, gif, bmp
- `quality`: (optional) 1-100, default 85

**Output:** Converted image file

**Example:**
```bash
curl -X POST "http://localhost:8000/api/tools/image-converter/run" \
  -F "file=@input.jpg" \
  -F "target_format=png" \
  -F "quality=90" \
  --output converted.png
```

## API Endpoints

### System Endpoints

**Health Check**
```
GET /api/system/health
```
Returns: `{"status": "ok"}`

**List All Tools**
```
GET /api/system/tools
```
Returns tool metadata and count.

**Get Tool Metadata**
```
GET /api/system/tools/{tool_name}
```
Returns metadata for a specific tool.

### Tool Execution

**Run Tool**
```
POST /api/tools/{tool_name}/run
```
Supports both `application/json` and `multipart/form-data` content types.

## Installation and Setup

### Prerequisites

- Python 3.11+
- pip

### Local Development

1. **Clone the repository:**
```bash
cd backend
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
uvicorn app.main:app --reload
```

The application will start at `http://localhost:8000`

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/system/health

### Using Docker

1. **Build the image:**
```bash
docker build -t tool-execution-platform .
```

2. **Run the container:**
```bash
docker run -p 8000:8000 tool-execution-platform
```

The application will be available at `http://localhost:8000`

## Adding a New Tool

Adding a new tool is simple and follows a pattern:

### Step 1: Create Tool Package

Create a new package in `app/tools/{tool_name}/` with these files:
- `__init__.py`
- `schemas.py` (Pydantic input/output models)
- `logic.py` (Business logic)
- `tool.py` (Tool class)

### Step 2: Define Input/Output Schemas

In `schemas.py`:
```python
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    """Input schema for my tool."""
    param1: str = Field(..., description="Parameter 1")
    param2: int = Field(default=10, description="Parameter 2")

class MyToolOutput(BaseModel):
    """Output schema for my tool."""
    result: str = Field(description="Result")
```

### Step 3: Implement Business Logic

In `logic.py`:
```python
def my_tool_logic(param1: str, param2: int) -> str:
    """Core logic for the tool."""
    # Your implementation here
    return "result"
```

### Step 4: Create Tool Class

In `tool.py`:
```python
from app.core.base_tool import BaseTool

class MyTool(BaseTool):
    name = "my-tool"
    description = "Description of what the tool does"
    version = "1.0.0"
    output_type = "json"  # or "file"
    input_schema = {
        "type": "object",
        "properties": {
            "param1": {"type": "string"},
            "param2": {"type": "integer"}
        },
        "required": ["param1"]
    }

    def run(self, **kwargs):
        # Validate input
        # Call logic function
        # Return result
        pass
```

### Step 5: Register the Tool

In `app/core/tool_registry.py`:
```python
from app.tools.my_tool.tool import MyTool

TOOLS = {
    "my-tool": MyTool(),
    # ... other tools
}
```

That's it! The tool is now available at:
- `GET /api/system/tools/{tool_name}` (metadata)
- `POST /api/tools/{tool_name}/run` (execution)

## Configuration

Configuration is handled through environment variables in `app/core/config.py`.

**Available settings:**
- `APP_NAME`: Application name (default: "Tool Execution Platform")
- `DEBUG`: Debug mode (default: False)
- `MAX_FILE_SIZE`: Max file upload size in bytes (default: 10MB)
- `TEMP_DIR`: Temporary directory path (default: "/tmp/tool-execution")
- `ALLOWED_IMAGE_FORMATS`: Tuple of allowed image formats

**Set via .env file:**
```
DEBUG=True
MAX_FILE_SIZE=52428800
TEMP_DIR=/var/tmp/tools
```

## Logging

Logging is configured via loguru. Logs are printed to console and can be extended to log to files.

**Log outputs:**
- Tool execution start
- Successful execution
- Errors and warnings
- Debug information (when DEBUG=True)

## Error Handling

All errors return a standardized JSON response format:
```json
{
  "error": "Human-readable error message"
}
```

The system never exposes internal stack traces to clients.

**Error types:**
- `400 Bad Request`: Invalid input or file processing errors
- `404 Not Found`: Tool not found
- `500 Server Error`: Tool execution failures

## File Handling

The `FileService` class handles:
- Safe file uploads with size validation
- Filename sanitization to prevent directory traversal
- Automatic temporary file management
- Output file path generation

All files are saved to `TEMP_DIR` (default: `/tmp/tool-execution`).

## Performance Considerations

- Single-service architecture (no async workers needed for basic use)
- File operations are synchronous and suitable for I/O-bound tasks
- For resource-intensive operations, consider async tools or job queues

## Testing the Tools

### Test QR Generator via curl:

```bash
# JSON input
curl -X POST "http://localhost:8000/api/tools/qr-generator/run" \
  -H "Content-Type: application/json" \
  -d '{"data": "Hello World"}' \
  -o qr.png
```

### Test Tool Listing:

```bash
curl "http://localhost:8000/api/system/tools" | python -m json.tool
```

### Test Tool Metadata:

```bash
curl "http://localhost:8000/api/system/tools/qr-generator" | python -m json.tool
```

## Troubleshooting

**Port already in use:**
```bash
uvicorn app.main:app --port 8080
```

**Permission denied on temp directory:**
Check that `/tmp/tool-execution` exists and is writable.

**Module import errors:**
Ensure you're running from the `backend/` directory and have activated the virtual environment.

## Architecture Decisions

1. **No Database**: Tools operate on request/response basis without persistence
2. **No Background Jobs**: All operations are synchronous for simplicity
3. **Manual Tool Registry**: Beginner-friendly, explicit tool listing
4. **File System for Temp Files**: Simple, no external dependencies
5. **Single Service**: No microservices complexity
6. **Pydantic for Validation**: Schema-driven input validation
7. **Loguru for Logging**: Easy-to-use, contextual logging

## Code Style

- Clear docstrings on all public functions and classes
- Inline comments for complex logic
- Type hints throughout
- Small, focused functions
- Readable variable names
- No advanced metaprogramming

## Future Enhancements

Potential future additions (but not in this version):
- Database for tool statistics/history
- Authentication and authorization
- Async task execution with background jobs
- Auto-discovery of tools
- Rate limiting
- API key management

## License

This project is provided as-is for educational and commercial use.
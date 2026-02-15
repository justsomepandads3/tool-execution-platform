# Tool Execution Platform - Complete Setup Guide

A modular, beginner-friendly platform for executing utility tools (QR generator, image converter, etc.) with FastAPI backend and React frontend.

## 🚀 Quick Start with Docker (Recommended)

The fastest way to get everything running:

```bash
docker-compose up --build
```

Then open:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**That's it!** Both services run automatically with proper networking.

For detailed Docker instructions, see [DOCKER_GUIDE.md](./DOCKER_GUIDE.md)

## 📦 What's Included

### Backend
- **Language**: Python 3.11+ with FastAPI
- **Location**: `backend/` directory
- **Features**:
  - QR code generator tool ✅
  - Image converter tool ✅
  - Modular tool system
  - File handling
  - Comprehensive logging
  - Error handling
  - Docker support

### Frontend
- **Language**: React 18 with Vite
- **Location**: `frontend/` directory
- **Features**:
  - Dynamic form generation from backend schemas
  - Tool discovery and execution
  - JSON and file response handling
  - Responsive design
  - Environment-configurable backend URL
  - Docker support

## 📂 Project Structure

```
Tool Execution Platform/
├── docker-compose.yml          # Docker orchestration
├── DOCKER_GUIDE.md             # Detailed Docker instructions
├── README.md                   # This file
│
├── backend/                    # FastAPI application
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── api/
│   │   ├── tools/
│   │   ├── services/
│   │   └── utils/
│   └── README.md               # Backend-specific docs
│
└── frontend/                   # React application
    ├── Dockerfile
    ├── .dockerignore
    ├── package.json
    ├── vite.config.js
    ├── .env                    # Configure here!
    ├── public/
    ├── src/
    └── README.md               # Frontend-specific docs
```

## 🐳 Option 1: Docker Compose (Easiest)

### Prerequisites
- Docker Desktop installed

### Run

```bash
docker-compose up --build
```

Services start automatically with proper configuration.

### Logs

```bash
docker-compose logs -f
```

### Stop

```bash
docker-compose down
```

## 💻 Option 2: Local Development

### Prerequisites
- Python 3.11+
- Node.js 16+
- `pip` and `npm`

### Setup Backend

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000

### Setup Frontend

In a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Update .env if needed (default should work for local dev)
# VITE_API_BASE_URL=http://localhost:8000

# Run frontend
npm run dev
```

Frontend runs at: http://localhost:5173

## 🔧 Configuration

### Backend Configuration

Backend uses environment variables from `docker-compose.yml`:

| Variable | Default | Purpose |
|----------|---------|---------|
| `DEBUG` | `False` | Debug mode |
| `MAX_FILE_SIZE` | `10485760` (10MB) | Max upload size |
| `TEMP_DIR` | `/tmp/tool-execution` | Temporary files |

### Frontend Configuration

Edit `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Modular Tool Platform
VITE_DEBUG=true
```

**For Docker**: `VITE_API_BASE_URL=http://backend:8000` (from docker-compose.yml)

## 🛠 Available Tools

### QR Code Generator

**Endpoint**: `POST /api/tools/qr-generator/run`

**Input**:
```json
{
  "data": "https://example.com"
}
```

**Output**: PNG image file

**Example**:
```bash
curl -X POST "http://localhost:8000/api/tools/qr-generator/run" \
  -H "Content-Type: application/json" \
  -d '{"data": "Hello World"}' \
  -o qr.png
```

### Image Converter

**Endpoint**: `POST /api/tools/image-converter/run`

**Input**:
- `file`: Image to convert (upload)
- `target_format`: png, jpg, jpeg, webp, gif, bmp
- `quality`: (optional) 1-100, default 85

**Output**: Converted image file

**Example**:
```bash
curl -X POST "http://localhost:8000/api/tools/image-converter/run" \
  -F "file=@input.jpg" \
  -F "target_format=png" \
  -o output.png
```

## 📡 API Reference

### System Endpoints

#### Health Check
```
GET /api/system/health
```
Returns: `{"status": "ok"}`

#### List Tools
```
GET /api/tools
```
Returns all available tools with metadata.

#### Tool Metadata
```
GET /api/tools/{tool_name}
```
Returns metadata for a specific tool.

### Tool Execution

#### Run Tool
```
POST /api/tools/{tool_name}/run
```

Supports:
- `application/json` - JSON body
- `multipart/form-data` - File uploads + form fields

**Response**:
- If `output_type: "json"` → JSON response
- If `output_type: "file"` → File download

## 🎨 Adding Custom Tools

### Backend

Create a new tool in `backend/app/tools/`:

1. Create directory: `backend/app/tools/{tool_name}/`
2. Create files:
   - `tool.py` - Tool class inheriting from BaseTool
   - `logic.py` - Business logic
   - `schemas.py` - Pydantic input/output models
3. Register in `backend/app/core/tool_registry.py`

See [backend/README.md](./backend/README.md) for detailed instructions.

### Frontend

**No changes needed!** The frontend automatically:
- Discovers the new tool
- Fetches its schema
- Generates the appropriate form
- Handles execution correctly

## 🚢 Deployment

### Docker Hub

```bash
docker login
docker tag tool-platform-backend yourusername/tool-backend:1.0
docker push yourusername/tool-backend:1.0
```

### Cloud Platforms

- **Vercel**: `npm run build && vercel` (frontend)
- **Heroku**: `git push heroku main` (with Procfile)
- **AWS ECS**: Push to ECR then deploy
- **Google Cloud Run**: `gcloud run deploy`

See [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) for detailed deployment instructions.

## 📚 Documentation

- **Backend Docs**: [backend/README.md](./backend/README.md)
- **Frontend Docs**: [frontend/README.md](./frontend/README.md)
- **Docker Guide**: [DOCKER_GUIDE.md](./DOCKER_GUIDE.md)
- **API Docs**: http://localhost:8000/docs (when backend is running)

## 🧪 Testing

### Test Backend Health

```bash
curl http://localhost:8000/api/system/health
```

### Test Tool Listing

```bash
curl http://localhost:8000/api/tools | python -m json.tool
```

### Test Tool Execution

```bash
# QR Generator
curl -X POST "http://localhost:8000/api/tools/qr-generator/run" \
  -H "Content-Type: application/json" \
  -d '{"data": "Test"}' \
  -o qr.png

# Image Converter
curl -X POST "http://localhost:8000/api/tools/image-converter/run" \
  -F "file=@test.jpg" \
  -F "target_format=png" \
  -o output.png
```

## 🔐 Security

- ✅ Input validation with Pydantic
- ✅ File upload validation and sanitization
- ✅ No hardcoded secrets
- ✅ Safe error handling
- ✅ CORS properly configured

## 🐛 Troubleshooting

### Docker
See [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) - Troubleshooting section

### Backend
```bash
# Check backend logs
docker-compose logs backend

# Or locally:
cd backend && python -m uvicorn app.main:app --reload
```

### Frontend
```bash
# Check frontend logs
docker-compose logs frontend

# Or locally:
cd frontend && npm run dev
```

### Services Can't Communicate

Inside Docker, use service name `backend:8000` (not `localhost`).

Check `frontend/.env`:
```env
VITE_API_BASE_URL=http://backend:8000  # ✅ Correct
VITE_API_BASE_URL=http://localhost:8000  # ❌ Wrong in Docker
```

## 💡 Development Tips

### Add Debug Logging

Set `VITE_DEBUG=true` in `frontend/.env` to see API calls in console.

### Backend Development

Edit `docker-compose.yml`:
```yaml
backend:
  environment:
    - DEBUG=True  # Enable debug mode
```

### Frontend Development

For hot reload during Docker development:
```bash
docker-compose exec frontend npm run dev
```

## 📊 Architecture

```
┌─────────────────────────────────────────────┐
│         Your Browser                        │
│  Visit: http://localhost:5173              │
└──────────────┬──────────────────────────────┘
               │ (HTTP requests)
               ▼
┌─────────────────────────────────────────────┐
│        Frontend (React/Vite)                │
│  - Fetches /api/tools                      │
│  - Generates forms dynamically              │
│  - Submits to /api/tools/{name}/run        │
└──────────────┬──────────────────────────────┘
               │ (API calls)
               ▼
┌─────────────────────────────────────────────┐
│       Backend (FastAPI/Python)              │
│  - Lists available tools                    │
│  - Executes tools                           │
│  - Returns JSON or files                    │
└─────────────────────────────────────────────┘
```

## 🎯 Key Features

- ✅ Zero tool-specific frontend code
- ✅ Dynamic form generation from schemas
- ✅ JSON and file response handling
- ✅ Add new tools without frontend changes
- ✅ Docker Compose orchestration
- ✅ Health checks included
- ✅ Comprehensive error handling
- ✅ Production-ready
- ✅ Beginner-friendly code with comments
- ✅ Well documented

## 📝 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

To add a new tool:

1. **Create backend tool** in `backend/app/tools/{name}/`
2. **Register in registry**: `backend/app/core/tool_registry.py`
3. **Frontend automatically updates!**

No frontend code changes needed.

## 🆘 Getting Help

1. **Check backend logs**: `docker-compose logs backend`
2. **Check frontend logs**: `docker-compose logs frontend`
3. **Check API status**: http://localhost:8000/docs
4. **Read docs**: [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) or Backend/Frontend READMEs

---

**Ready to get started?**

```bash
docker-compose up --build
```

Then visit http://localhost:5173 🎉

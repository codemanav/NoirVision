# NoirVision Backend

Forensic video analysis backend with TwelveLabs video processing and Backboard.io AI credibility verification.

## 🚀 Quick Start

### 1. Setup Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```env
# Backboard.io for AI credibility analysis
BACKBOARD_API_KEY=your_backboard_api_key_here

# TwelveLabs for video analysis
TWELVELABS_API_KEY=your_twelvelabs_api_key_here
TWELVELABS_INDEX_ID=your_index_id_here
TWELVELABS_MOCK=false

# S3 for video storage (optional)
S3_BUCKET=your-bucket
AWS_REGION=us-east-1

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 3. Run Server

```bash
python -m app.main
```

Server starts at: `http://localhost:8000`

## 📡 API Endpoints

### Video Processing (TwelveLabs)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/videos/upload` | POST | Upload and process video |
| `/api/videos/{job_id}` | GET | Check video processing status |
| `/api/videos/{video_id}/query` | POST | Query video with natural language |

### Credibility Analysis (Backboard AI)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze` | POST | Full claim vs video analysis |
| `/analyze/text` | POST | Quick analysis with mock video |
| `/demo/supported` | GET | Demo: Supported claim |
| `/demo/contradicted` | GET | Demo: Contradicted claim |

### System

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |

### API Documentation

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🧪 Testing

### Quick Tests

```bash
# Health check
curl http://localhost:8000/health

# Test Backboard AI analysis
curl http://localhost:8000/demo/supported
curl http://localhost:8000/demo/contradicted

# Upload video for TwelveLabs processing
curl -X POST "http://localhost:8000/api/videos/upload" \
  -F "file=@path/to/video.mp4"
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI server
│   ├── config.py               # Configuration
│   ├── db.py                   # Database utilities
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   ├── evidence.py
│   │   └── jobs.py
│   ├── routers/                # API routes
│   │   ├── __init__.py
│   │   └── videos.py
│   ├── services/               # External services
│   │   ├── __init__.py
│   │   ├── s3_store.py
│   │   └── twelvelabs_client.py
│   ├── backboard_agent.py      # Backboard AI integration
│   ├── report_generator.py     # Report formatting
│   └── mock_data.py            # Mock data for testing
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
├── .env                        # API keys (not in git)
└── README.md
```

## 🔧 Tech Stack

- **Framework:** FastAPI
- **Video Processing:** TwelveLabs API
- **AI Analysis:** Backboard.io (LLM orchestration)
- **Storage:** AWS S3 (optional)
- **Database:** SQLModel (in-memory or persistent)
- **Language:** Python 3.11+

## 🎯 Features

### TwelveLabs Integration
✅ Video upload and indexing  
✅ Natural language video search  
✅ Scene detection and analysis  
✅ Job status tracking  

### Backboard AI Integration
✅ AI-powered claim parsing  
✅ Intelligent video comparison  
✅ Credibility scoring (0-100)  
✅ Noir-styled reports  
✅ Investigation recommendations  
✅ Creative case titles  

## 🐛 Troubleshooting

**Server won't start?**
```bash
source venv/bin/activate
python -m app.main
```

**Port 8000 in use?**
Change `PORT` in `.env` file

**Missing dependencies?**
```bash
pip install -r requirements.txt
```

**TwelveLabs mock mode?**
Set `TWELVELABS_MOCK=true` in `.env` for development without API

## 📄 License

MIT License

---

**"In the city of lies, trust the footage."** 🎷

# NoirVision Backend

Forensic video analysis backend powered by Backboard.io AI for credibility verification.

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
```
BACKBOARD_API_KEY=your_backboard_api_key_here
TWELVELABS_API_KEY=your_twelvelabs_api_key_here
```

### 3. Run Server

```bash
python -m app.main
```

Server starts at: `http://localhost:8000`

## 📡 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/analyze` | POST | Full analysis (claim + video) |
| `/demo/supported` | GET | Demo: Supported claim scenario |
| `/demo/contradicted` | GET | Demo: Contradicted claim scenario |

### API Documentation

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🧪 Testing

### Quick Test

```bash
# Health check
curl http://localhost:8000/health

# Test supported claim
curl http://localhost:8000/demo/supported

# Test contradicted claim
curl http://localhost:8000/demo/contradicted
```

### Example Request

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "claim": {
      "claim_text": "I was robbed at the warehouse"
    },
    "video_analysis": {
      "source": "video.mp4",
      "duration": "2m 30s",
      "detections": [...]
    }
  }'
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI server
│   ├── models.py               # Data models
│   ├── backboard_agent.py      # Backboard AI integration
│   ├── report_generator.py     # Report formatting
│   └── mock_data.py            # Mock TwelveLabs data
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
├── .env                        # API keys (not in git)
└── README.md
```

## 🔧 Tech Stack

- **Framework:** FastAPI
- **AI Engine:** Backboard.io (LLM orchestration)
- **Video Analysis:** TwelveLabs (mock data included)
- **Language:** Python 3.13+

## 🎯 Features

✅ AI-powered claim parsing  
✅ Intelligent video comparison  
✅ Credibility scoring (0-100)  
✅ Noir-styled reports  
✅ Investigation recommendations  
✅ Creative case titles  

## 🔌 TwelveLabs Integration

Currently using mock data. To integrate real TwelveLabs:

1. Get TwelveLabs API key
2. Update `.env` with `TWELVELABS_API_KEY`
3. Replace mock data in `mock_data.py` with real API calls
4. Data structure in `models.py` matches TwelveLabs output

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

## 📄 License

MIT License

---

**"In the city of lies, trust the footage."** 🎷

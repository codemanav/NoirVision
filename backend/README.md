# NoirVision Backend

Complete forensic video analysis system integrating TwelveLabs video intelligence with Backboard AI credibility verification.

## Architecture

```
Video Input → TwelveLabs Analysis → Backboard AI → Credibility Report
```

## Features

- **TwelveLabs Integration**: Automated video analysis for evidence extraction
  - Object & action detection
  - Speech transcription
  - Scene segmentation
  - Temporal event tracking

- **Backboard AI Analysis**: Intelligent claim verification
  - Structured claim parsing
  - Multi-point comparison (time, location, objects, events)
  - Evidence-based scoring
  - Investigation recommendations

- **NoirVision Analyzer**: End-to-end pipeline
  - Converts TwelveLabs evidence to analysis format
  - Coordinates AI credibility assessment
  - Generates formatted ASCII reports

## Setup

1. **Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required environment variables:
- `BACKBOARD_API_KEY`: Your Backboard.io API key
- `TWELVELABS_API_KEY`: Your TwelveLabs API key
- `TWELVELABS_INDEX_ID`: Your TwelveLabs index ID
- `TWELVELABS_MOCK=true`: Use mock data for testing (optional)

3. **Run Server**
```bash
python -m uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### Complete Analysis (End-to-End)

**POST `/analyze/complete`**

Submit video and witness claim for complete analysis.

```bash
# With video file
curl -X POST http://localhost:8000/analyze/complete \
  -F "claim=I saw a robbery at midnight near the warehouse" \
  -F "video_file=@evidence.mp4"

# With video URL
curl -X POST http://localhost:8000/analyze/complete \
  -F "claim=I saw a robbery at midnight near the warehouse" \
  -F "video_url=https://example.com/video.mp4"
```

Response:
```json
{
  "report": { ... },
  "formatted_report": "╔═══ VERITAS CREDIBILITY REPORT ═══╗\n...",
  "video_id": "twelvelabs-video-id"
}
```

### TwelveLabs Video Analysis (Advanced)

**POST `/api/videos/analyze`**

Submit video for TwelveLabs processing (returns job ID for async polling).

**GET `/api/videos/analyze/{job_id}`**

Check analysis job status.

**GET `/api/videos/{video_id}/evidence`**

Retrieve processed evidence pack.

## Testing

Run the integration test:
```bash
python test_integration.py
```

This tests the complete flow:
1. TwelveLabs video processing (mocked)
2. Backboard AI analysis
3. Report generation

## Project Structure

```
backend/
├── app/
│   ├── main.py                      # FastAPI application
│   ├── config.py                    # Environment configuration
│   ├── noirvision_analyzer.py       # End-to-end integration
│   ├── backboard_agent.py           # Backboard AI client
│   ├── report_generator.py          # ASCII report formatter
│   ├── models.py                    # NoirVision data models
│   ├── db.py                        # SQLite job storage
│   ├── models_twelvelabs/           # TwelveLabs models
│   │   ├── evidence.py              # Evidence pack structure
│   │   └── jobs.py                  # Job management models
│   ├── routers/
│   │   └── videos.py                # TwelveLabs endpoints
│   └── services/
│       ├── twelvelabs_client.py     # TwelveLabs API wrapper
│       └── s3_store.py              # S3 storage (optional)
├── requirements.txt
├── .env.example
└── test_integration.py              # Integration test
```

## Development

- **Mock Mode**: Set `TWELVELABS_MOCK=true` to test without TwelveLabs API
- **Logging**: All modules use Python logging (INFO level by default)
- **Database**: SQLite for job tracking (`noirvision_jobs.db`)

## Production Considerations

1. **API Keys**: Use secrets management (AWS Secrets Manager, HashiCorp Vault)
2. **Video Storage**: Configure S3 bucket for evidence persistence
3. **CORS**: Update `allow_origins` in `main.py` for your frontend domain
4. **Rate Limiting**: Add rate limiting middleware for public endpoints
5. **Error Handling**: Monitor Backboard and TwelveLabs API errors

## License

NoirVision - "In the city of lies, trust the footage."

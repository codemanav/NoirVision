# NoirVision Testing Guide

## Quick Test

Run the integration test to verify the complete pipeline:

```bash
cd backend
source venv/bin/activate
python test_integration.py
```

This tests:
- TwelveLabs video processing (mock mode)
- Backboard AI credibility analysis
- Report generation

Expected output: ASCII art credibility report with case details and verdict.

## API Testing

### 1. Start the Server

```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Health Check

```bash
curl http://localhost:8000/health
```

### 3. Complete Analysis (with mock video)

```bash
curl -X POST http://localhost:8000/analyze/complete \
  -F "claim=On Friday night around 11 PM, I was attacked by a man in a trench coat" \
  -F "video_url=https://example.com/test.mp4" \
  -F "case_id=TEST-001"
```

### 4. Test with Real TwelveLabs

1. Set `TWELVELABS_MOCK=false` in `.env`
2. Ensure `TWELVELABS_API_KEY` and `TWELVELABS_INDEX_ID` are configured
3. Upload a test video:

```bash
curl -X POST http://localhost:8000/analyze/complete \
  -F "claim=Test claim about the video" \
  -F "video_file=@/path/to/test-video.mp4"
```

## Environment Variables for Testing

```bash
# .env for testing
BACKBOARD_API_KEY=your_key_here
TWELVELABS_API_KEY=your_key_here
TWELVELABS_INDEX_ID=your_index_id
TWELVELABS_MOCK=true  # Use mock for fast testing
DEBUG=True
```

## Expected Response Format

```json
{
  "report": {
    "case_id": "TEST-001",
    "case_title": "The Shadow's Confession",
    "credibility_score": 85,
    "verdict": "✅ CLAIM SUPPORTED",
    "comparisons": [...]
  },
  "formatted_report": "╔═══ VERITAS CREDIBILITY REPORT ═══╗\n...",
  "video_id": "video-12345"
}
```

## Troubleshooting

- **500 Error - Backboard not configured**: Check `BACKBOARD_API_KEY` in `.env`
- **TwelveLabs timeout**: Increase `TWELVELABS_POLL_TIMEOUT_SECONDS` in `.env`
- **Validation errors**: Ensure video source type is "youtube" or "s3"

# POIBenchWeb

Self-hosted web version of POIBench (demo).

## Structure

- `backend/main.py` — FastAPI app: computation API (`/api/...`) and serves the frontend
- `frontend/index.html` — web page that calls the API

## Run locally

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --port 8000
```

Open http://localhost:8000

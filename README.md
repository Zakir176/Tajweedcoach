# Tajweed Recitation Coach 🎙️📖

[![Local-Only](https://img.shields.io/badge/deployment-local-brightgreen)](#)
[![License](https://img.shields.io/badge/license-MIT-blue)](#)

An open-source, privacy-first web app to help learners improve Quran recitation. Record a verse in-browser, get a local transcription and a pronunciation-focused feedback report, then listen to reference recitations.

## Table of Contents
- Features
- Quickstart
- Architecture & Tech Stack
- Detailed Setup
- Usage Examples
- Contributing
- Troubleshooting
- Project Documentation

---

## Features
- Select any verse from the 114 Surahs and practice.
- Record audio in-browser using the Web Audio API.
- Local speech-to-text (Faster-Whisper) for private transcription.
- Local LLM feedback (Ollama) for pronunciation guidance.
- Reference audio player streaming from EveryAyah's CDN.

---

## Quickstart (recommended)
1. Start backend services:

   cd backend
   docker compose up -d

2. Start frontend:

   cd frontend
   npm install
   npm run dev

Visit the Vite URL (usually http://localhost:5173) and the backend at http://localhost:8000.

---

## Architecture & Tech Stack
- Frontend: Vue 3 (Composition API), Vite, Tailwind CSS, Pinia
- Backend: FastAPI (Python)
- Persistence: PostgreSQL, Redis (cache)
- Local ML: Faster-Whisper (speech-to-text), Ollama (LLM for feedback)

This repo is designed for fully-local inference to preserve user privacy and reduce runtime costs.

---

## Detailed Setup
### Prerequisites
- Docker & Docker Compose
- Node.js v18+
- Python 3.10+ (for local development in the backend)
- Ollama installed on the host (for the LLM feedback service)

### Backend (local dev)
1. From the repository root:

   cd backend
   docker compose up -d

2. (Optional) For working directly with the Python environment instead of Docker:

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1    # PowerShell
   pip install -r requirements.txt
   uvicorn app.main:app --reload

3. Environment variables
Create a .env in backend/ (see backend/.env.example if present) with values such as:

   DATABASE_URL=postgresql://user:password@localhost:5432/tajweed
   REDIS_URL=redis://localhost:6379
   OLLAMA_BASE_URL=http://localhost:11434    # adjust if Ollama listens elsewhere

### Ollama
Install Ollama from https://ollama.com/. Start or run a model; one common command pattern is:

   ollama run <model-name>

Confirm Ollama is reachable at the OLLAMA_BASE_URL above before starting the app.

### Frontend

   cd frontend
   npm install
   npm run dev

Open the URL shown by Vite (default: http://localhost:5173).

---

## Usage Examples
- **Recording and feedback:** Use the web UI to select a verse, record, and request feedback.
- **Interactive API docs (Swagger UI):** Once the backend is running, visit **http://localhost:8000/docs** to explore and test all endpoints directly in the browser. ReDoc is also available at http://localhost:8000/redoc.

### `curl` Examples

**Fetch all Surahs:**
```bash
curl http://localhost:8000/api/v1/surahs
```

**Fetch verses for Surah Al-Fatihah (ID 1):**
```bash
curl http://localhost:8000/api/v1/surahs/1/verses
```

**Upload a recitation for feedback** (multipart, `.webm` blob required):
```bash
curl -X POST http://localhost:8000/api/v1/recitations/upload \
  -F "audio=@/path/to/recording.webm;type=audio/webm" \
  -F "verse_id=1"
```

**Health check:**
```bash
curl http://localhost:8000/health
```

---

## Contributing
Contributions welcome. Please:
1. Fork the repo and create a feature branch.
2. Open a pull request with a clear description and tests where applicable.
3. Follow code style in existing files.

See CONTRIBUTING.md (in /docs or add one) for full instructions.

---

## Troubleshooting
- Backend not reachable: ensure `docker compose ps` shows postgres, redis, and backend containers running.
- Ollama errors: confirm the model is running and OLLAMA_BASE_URL is correct.
- Frontend build errors: delete node_modules and reinstall with `npm ci`.

---

## Project Documentation
- [System Architecture](docs/SYSTEM_ARCHITECTURE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Development Guide](docs/DEVELOPMENT_GUIDE.md)
- [Contributing](CONTRIBUTING.md)

---

## License
MIT — see LICENSE file.

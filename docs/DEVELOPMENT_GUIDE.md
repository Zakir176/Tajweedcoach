# Development Guide

This guide covers day-to-day development practices for the Tajweed Recitation Coach project: running services locally, understanding the codebase structure, working with the database, and debugging the ML pipeline.

---

## Table of Contents
- [Project Structure](#project-structure)
- [Local Development Setup](#local-development-setup)
- [Environment Variables](#environment-variables)
- [Running Services](#running-services)
- [Interactive API Docs (Swagger)](#interactive-api-docs-swagger)
- [Database Management](#database-management)
- [Working with the ML Pipeline](#working-with-the-ml-pipeline)
- [Frontend Development](#frontend-development)
- [Code Style & Linting](#code-style--linting)
- [Testing](#testing)
- [Common Debugging Tips](#common-debugging-tips)

---

## Project Structure

```
Tajweedcoach/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/          # FastAPI route handlers (verses, recitations)
│   │   ├── core/
│   │   │   ├── config.py        # Pydantic settings (reads from .env)
│   │   │   └── database.py      # SQLAlchemy async engine & session factory
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── whisper_service.py   # Faster-Whisper STT integration
│   │   │   └── feedback_service.py  # Ollama LLM feedback integration
│   │   └── main.py              # FastAPI app entry point
│   ├── .env                     # Local secrets (gitignored)
│   ├── .env.example             # Template for environment variables
│   ├── docker-compose.yml       # Postgres + Redis + backend container
│   ├── Dockerfile               # Backend container image
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable Vue components
│   │   ├── views/               # Page-level Vue components
│   │   ├── stores/              # Pinia state stores
│   │   └── App.vue
│   └── package.json
└── docs/                        # Project documentation
```

---

## Local Development Setup

### Prerequisites
| Tool | Version | Purpose |
|---|---|---|
| Docker Desktop | Latest | Runs Postgres, Redis, and optionally the backend |
| Node.js | v18+ | Frontend dev server |
| Python | 3.10+ | Backend (if not using Docker) |
| Ollama | Latest | Local LLM for feedback generation |

### 1. Clone and configure

```bash
git clone https://github.com/<your-fork>/Tajweedcoach.git
cd Tajweedcoach
cp backend/.env.example backend/.env
# Edit backend/.env with your local values
```

### 2. Pull and start an Ollama model

```bash
# Install Ollama from https://ollama.com then pull a model, e.g.:
ollama pull llama3
ollama run llama3
```

Keep Ollama running in the background — the backend calls it via HTTP on port `11434`.

---

## Environment Variables

All settings are loaded via `backend/app/core/config.py` using `pydantic-settings`. Copy `backend/.env.example` to `backend/.env` and set the following:

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://user:password@db:5432/tajweed_coach` | Async PostgreSQL connection string |
| `REDIS_URL` | `redis://cache:6379/0` | Redis connection string |
| `SECRET_KEY` | *(required)* | JWT signing secret — use a strong random string |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT expiry duration |
| `DEBUG` | `True` | Enables FastAPI debug mode and hot-reload |
| `ALLOWED_ORIGINS` | `http://localhost:5173` | CORS origins (comma-separated) |

> **Note:** `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` are present in the config but are not currently used. The feedback pipeline runs entirely through local Ollama.

---

## Running Services

### Option A — Docker (recommended)

Starts Postgres, Redis, and the FastAPI backend together:

```bash
cd backend
docker compose up -d
```

Check service health:

```bash
docker compose ps
docker compose logs -f backend
```

Stop services:

```bash
docker compose down
```

### Option B — Local Python (for active backend development)

```bash
cd backend
python -m venv .venv

# Activate (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (bash/zsh)
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The `--reload` flag watches for file changes and restarts automatically.

---

## Interactive API Docs (Swagger)

FastAPI auto-generates interactive documentation. Once the backend is running:

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | **Swagger UI** — explore and test all endpoints interactively |
| `http://localhost:8000/redoc` | **ReDoc** — clean, read-only API reference |
| `http://localhost:8000/openapi.json` | Raw OpenAPI schema |

The Swagger UI allows you to submit real requests (including multipart audio file uploads) directly from the browser — no `curl` required during development.

---

## Database Management

The backend uses **SQLAlchemy async** with **asyncpg**. Tables are auto-created on startup via `Base.metadata.create_all`.

### Connect directly to Postgres (Docker)

```bash
docker compose exec db psql -U user -d tajweed_coach
```

### Useful psql queries

```sql
-- List all tables
\dt

-- Check seeded surahs
SELECT id, name_english, ayah_count FROM surahs LIMIT 10;

-- Review recent recitation sessions
SELECT id, verse_id, accuracy_score, created_at FROM recitation_sessions ORDER BY created_at DESC LIMIT 5;
```

---

## Working with the ML Pipeline

### Faster-Whisper (Speech-to-Text)

The `whisper_service.py` service runs a local `faster-whisper` model. The model is downloaded on first use and cached on disk.

- **Language:** forced to `ar` (Arabic)
- **Model size:** configurable — currently `small` for a balance of speed and accuracy
- **Prompt injection:** the expected verse text is passed as an `initial_prompt` to bias the transcription towards correct Quranic vocabulary

To test transcription in isolation:

```bash
# From the backend/ directory with venv active
python -c "
from app.services.whisper_service import transcribe_audio
# Pass a path to a local .webm or .wav file
result = transcribe_audio('path/to/test_audio.webm', expected_text='بِسْمِ اللَّهِ')
print(result)
"
```

### Ollama (LLM Feedback)

The `feedback_service.py` service calls the Ollama HTTP API on the host machine.

Verify Ollama is reachable:

```bash
curl http://localhost:11434/api/tags
```

Test a feedback generation call:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Give Tajweed feedback for: transcription=bism allah, expected=bismillah",
  "stream": false
}'
```

---

## Frontend Development

```bash
cd frontend
npm install
npm run dev
```

- Vue 3 with the **Composition API** (`<script setup>`)
- State management via **Pinia**
- Styling via **Tailwind CSS**
- Build tool: **Vite**

The `VITE_API_BASE_URL` environment variable controls which backend the frontend points to. For local dev, it defaults to `http://localhost:8000`.

---

## Code Style & Linting

### Backend (Python)

```bash
cd backend
# Format
black app/
isort app/

# Lint
flake8 app/
```

### Frontend (JavaScript/Vue)

```bash
cd frontend
npm run lint       # ESLint
npm run format     # Prettier
```

Run formatters before every commit. CI will enforce these on pull requests.

---

## Testing

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm test
```

---

## Common Debugging Tips

| Symptom | Fix |
|---|---|
| `Connection refused` on `localhost:8000` | Run `docker compose ps` — check if the backend container exited. Check logs with `docker compose logs backend`. |
| Whisper model not found | First run downloads the model. Ensure disk space is available and the container has internet access on first start. |
| Ollama returns 404 or connection error | Confirm Ollama is running (`ollama list`) and `OLLAMA_BASE_URL` in `.env` is correct. |
| Frontend can't reach API | Check CORS — `ALLOWED_ORIGINS` in `.env` must include the Vite dev server URL (default `http://localhost:5173`). |
| Postgres auth error | Ensure `DATABASE_URL` credentials match the values in `docker-compose.yml`. |
| `npm run dev` fails | Delete `node_modules` and run `npm ci` for a clean install. |

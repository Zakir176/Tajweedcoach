# Development Guide

A practical reference for contributors working on the Tajweed Recitation Coach backend and frontend. This document covers the project layout, local development setup, service integrations, and patterns to follow when extending the codebase.

---

## Table of Contents

- [Project Layout](#project-layout)
- [Environment Variables](#environment-variables)
- [Running the Stack](#running-the-stack)
  - [Docker (recommended)](#docker-recommended)
  - [Local Python (no Docker)](#local-python-no-docker)
  - [Frontend Dev Server](#frontend-dev-server)
- [Interactive API Docs](#interactive-api-docs)
- [Service Integrations](#service-integrations)
  - [Speech-to-Text — Groq Whisper](#speech-to-text--groq-whisper)
  - [Feedback Engine — Groq LLM](#feedback-engine--groq-llm)
  - [Diff Engine](#diff-engine)
- [Database](#database)
  - [Seeding Quran Data](#seeding-quran-data)
  - [Migrations](#migrations)
- [Adding a New API Route](#adding-a-new-api-route)
- [Code Style](#code-style)
- [Common Gotchas](#common-gotchas)

---

## Project Layout

```
Tajweedcoach/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py              # Shared FastAPI dependencies (get_db)
│   │   │   └── routes/
│   │   │       ├── verses.py        # GET /surahs, GET /surahs/{id}/verses
│   │   │       └── recitations.py   # POST /recitations/upload
│   │   ├── core/
│   │   │   ├── config.py            # Pydantic settings (reads .env)
│   │   │   └── database.py          # Async SQLAlchemy engine + session factory
│   │   ├── models/
│   │   │   └── verse.py             # Surah and Verse ORM models
│   │   ├── services/
│   │   │   ├── whisper_service.py   # Groq Whisper-large-v3 transcription
│   │   │   ├── feedback_service.py  # Groq LLaMA feedback generation
│   │   │   └── diff_service.py      # Arabic word-level diff comparison
│   │   ├── seed_quran.py            # One-time DB seeding script
│   │   └── main.py                  # FastAPI app + router registration
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── .env.example                 # Template — copy to .env
│   └── .env                         # Your local secrets (git-ignored)
├── frontend/
│   ├── src/
│   │   ├── components/              # Vue SFCs (VerseSelector, FeedbackCard, etc.)
│   │   ├── stores/                  # Pinia state stores
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
└── docs/
    ├── API_REFERENCE.md
    ├── SYSTEM_ARCHITECTURE.md
    └── DEVELOPMENT_GUIDE.md         ← you are here
```

---

## Environment Variables

Create `backend/.env` by copying the example:

```bash
cp backend/.env.example backend/.env
```

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://user:password@localhost:5432/tajweed_coach` | Postgres connection string. Within Docker Compose use the `db` service hostname; locally use `localhost:5433`. |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection. Within Docker Compose use `cache`; locally use `localhost:6380`. |
| `GROQ_API_KEY` | *(required)* | Groq Cloud API key — used for **both** Whisper transcription and LLM feedback. Get one free at [console.groq.com](https://console.groq.com). |
| `SECRET_KEY` | `secret` | JWT signing secret — **replace before any deployment**. |
| `ALGORITHM` | `HS256` | JWT algorithm. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT token TTL in minutes. |
| `DEBUG` | `True` | Enables SQLAlchemy query logging and FastAPI debug mode. Set `False` in production. |
| `ALLOWED_ORIGINS` | `http://localhost:5173` | CORS allow-list (comma-separated). Add your Vercel/Railway URLs here. |

> [!IMPORTANT]
> `GROQ_API_KEY` is the single most critical environment variable. Both the transcription and feedback pipelines call Groq's API. Without it, all `/recitations/upload` requests will fail with a `401`.

---

## Running the Stack

### Docker (recommended)

The `docker-compose.yml` defines three services: `api`, `db` (Postgres 15), and `cache` (Redis 7).

```bash
cd backend
docker compose up -d
```

**Port mapping — note the non-standard host ports to avoid conflicts:**

| Service | Container port | Host port |
|---|---|---|
| FastAPI API | 8000 | **8000** |
| PostgreSQL | 5432 | **5433** |
| Redis | 6379 | **6380** |

After first start, [seed the Quran data](#seeding-quran-data).

Useful commands:

```bash
docker compose ps              # Check running services
docker compose logs -f api     # Tail the FastAPI logs
docker compose down            # Stop all services
docker compose down -v         # Stop and delete volumes (full reset)
```

### Local Python (no Docker)

Best for rapid iteration on backend code without rebuilding the image.

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1      # PowerShell
# source .venv/bin/activate       # bash/zsh

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Keep the database and cache running via Docker while the API runs locally:

```bash
docker compose up -d db cache
```

Then update your `backend/.env` to use the **host-mapped ports**:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5433/tajweed_coach
REDIS_URL=redis://localhost:6380/0
```

### Frontend Dev Server

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server starts at `http://localhost:5173` and proxies API calls to the backend at `http://localhost:8000`.

---

## Interactive API Docs

FastAPI generates interactive documentation automatically. With the backend running:

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | **Swagger UI** — test endpoints including multipart audio upload |
| `http://localhost:8000/redoc` | **ReDoc** — clean read-only reference |
| `http://localhost:8000/openapi.json` | Raw OpenAPI 3.x schema |
| `http://localhost:8000/health` | Health check endpoint |

---

## Service Integrations

### Speech-to-Text — Groq Whisper

**File:** `backend/app/services/whisper_service.py`

The app uses **Groq's hosted `whisper-large-v3`** for Arabic transcription. This provides GPU-accelerated, high-accuracy transcription via API without requiring local ML hardware.

```python
# Called from recitations.py after saving the uploaded file
transcription = await whisper_service.transcribe(
    file_path="/tmp/<uuid>.webm",
    expected_text=verse.text_arabic   # Optional but strongly recommended
)
```

**Prompt injection for accuracy:** When `expected_text` is provided, the service strips Arabic diacritics (tashkeel) from the verse and injects the cleaned text as Whisper's `prompt` parameter. This primes the model with the correct Quranic vocabulary and dramatically improves word-boundary detection.

To test different models, change the `model=` argument in `whisper_service.py`. Groq currently supports `whisper-large-v3` and `whisper-large-v3-turbo`.

> [!NOTE]
> Audio must be a `.webm` blob. The file is saved to `/tmp/` inside the container, processed, then deleted in the `finally` block — no audio is persisted to disk.

### Feedback Engine — Groq LLM

**File:** `backend/app/services/feedback_service.py`

Pedagogical feedback is generated by **Groq's `llama-3.3-70b-versatile`** model. The service receives the student's transcription, the expected Arabic verse, and the word-level diff, then returns 3–4 sentences of warm, targeted coaching.

```python
feedback = await feedback_service.generate_feedback(
    transcription="bism allah",
    expected=verse.text_arabic,
    diff=diff_results   # List of {word, status, expected?} dicts
)
```

The response is capped at `max_tokens=300` to keep feedback concise and on-screen friendly. To tune the coaching tone or detail level, edit the system prompt in `feedback_service.py`.

### Diff Engine

**File:** `backend/app/services/diff_service.py`

Compares the Whisper transcription against the expected verse text at the word level using Python's `difflib`. Returns:
- `accuracy_score` — a float `0.0–1.0` representing the edit-distance ratio
- `diff` — an array of `{ word, status }` objects consumed by the frontend's color-coded word highlighting

---

## Database

The app uses **SQLAlchemy async** (`asyncpg` driver) with declarative ORM models. Tables are auto-created on startup via `Base.metadata.create_all()` — no separate migration step is needed for a fresh environment.

**Connect directly to Postgres:**

```bash
# Via Docker
docker compose exec db psql -U <POSTGRES_USER> -d <POSTGRES_DB>

# Directly from host (note port 5433)
psql -h localhost -p 5433 -U <POSTGRES_USER> -d <POSTGRES_DB>
```

**Useful queries:**

```sql
-- Check seeded surahs
SELECT id, name_english, ayah_count FROM surahs LIMIT 10;

-- Inspect a verse
SELECT id, surah_id, ayah_number, text_arabic FROM verses WHERE surah_id = 1;

-- Review recitation sessions
SELECT id, verse_id, accuracy_score, created_at
FROM recitation_sessions
ORDER BY created_at DESC
LIMIT 10;
```

### Seeding Quran Data

Run the seed script once after the database tables have been created:

```bash
# Via Docker
docker compose exec api python app/seed_quran.py

# Locally (with venv active)
cd backend
python app/seed_quran.py
```

> [!CAUTION]
> Re-running the seed script on a populated database may create duplicates if upsert logic is not in place. Verify idempotency in `seed_quran.py` before re-running.

### Migrations

For schema changes beyond initial table creation, use **Alembic**:

```bash
pip install alembic
alembic init alembic
# Configure alembic/env.py to point at settings.DATABASE_URL
alembic revision --autogenerate -m "add user sessions table"
alembic upgrade head
```

---

## Adding a New API Route

1. **Create the route module** in `backend/app/api/routes/your_feature.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db

router = APIRouter()

@router.get("/your-endpoint")
async def your_endpoint(db: AsyncSession = Depends(get_db)):
    ...
```

2. **Register it** in `backend/app/main.py`:

```python
from app.api.routes import your_feature
app.include_router(your_feature.router, prefix="/api/v1", tags=["your-feature"])
```

3. **Add Pydantic response models** inline or in a dedicated `app/schemas/` file to ensure clean, validated API responses.

4. **Document the endpoint** in `docs/API_REFERENCE.md`.

---

## Code Style

| Layer | Tool | Command |
|---|---|---|
| Python formatting | `black` | `black app/` |
| Python import order | `isort` | `isort app/` |
| Python linting | `flake8` | `flake8 app/` |
| JS/Vue formatting | `prettier` | `npm run format` |
| JS/Vue linting | `eslint` | `npm run lint` |

Run formatters before every commit. CI enforces these checks on all pull requests.

---

## Common Gotchas

| Symptom | Cause | Fix |
|---|---|---|
| `Connection refused` on port 5432 | Docker maps Postgres to **5433** on the host | Use `localhost:5433` in your local `.env` |
| `Connection refused` on port 6379 | Docker maps Redis to **6380** on the host | Use `localhost:6380` in your local `.env` |
| `401 Unauthorized` on `/recitations/upload` | `GROQ_API_KEY` missing or invalid | Set a valid key in `.env` and restart the service |
| `404 Verse not found` on upload | Database not seeded yet | Run `seed_quran.py` |
| `asyncpg` connection error | URL uses `postgresql://` instead of `postgresql+asyncpg://` | `database.py` handles the rewrite automatically; check for typos in `DATABASE_URL` |
| Frontend can't reach backend | CORS misconfiguration | Ensure `ALLOWED_ORIGINS` in `.env` includes `http://localhost:5173` |
| `npm run dev` fails on install | Stale `node_modules` | Delete `node_modules/` and run `npm ci` |

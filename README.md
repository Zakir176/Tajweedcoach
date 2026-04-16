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
- Recording and feedback: Use the web UI to select a verse, record, and request feedback.
- API (developer): See docs/API_REFERENCE.md for exact endpoints. Example (high-level):

  POST /api/feedback  - multipart/form-data { audio: file, verse: "2:255" }

If you want precise curl examples, confirm which endpoints to document and they will be added here.

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
- docs/SYSTEM_ARCHITECTURE.md
- docs/API_REFERENCE.md
- docs/DEVELOPMENT_GUIDE.md

---

## License
MIT — see LICENSE file.

---

If this README should include concrete curl examples, screenshots, or CI badges, confirm which endpoints and assets to include and they will be added.

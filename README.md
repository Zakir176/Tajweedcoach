# Tajweed Recitation Coach 🎙️📖

An AI-powered web application designed to help self-teaching Muslims improve their Quran recitation. The app provides a full feedback loop: users record their recitation of a specific verse, and our on-device, localized AI engine provides transcription, an expected diff, and detailed pronunciation guidance—finished off with reference audio from world-renowned shuyookh.

## Table of Contents
- [Features](#features)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Getting Started](#getting-started)
- [Project Documentation](#project-documentation)

---

## Features

- **Verse Selection**: Explore and practice any verse from the 114 Surahs.
- **In-Browser Recording**: Native audio capture through the browser's Web Audio API. 
- **Local AI Analysis**: Audio is processed privately and securely. We use Faster-Whisper to transcribe Arabic speech, and evaluate it locally against a known Quranic dictionary.
- **Actionable Feedback**: Ollama generates dynamic, localized feedback breaking down your recitation's mistakes or successes.
- **Reference Player**: Instantly play the professionally recorded recitation for your exact verse by renowned reciters (Husary and Sudais) seamlessly streaming from EveryAyah's CDN.

## Architecture & Tech Stack

This project was intentionally pivoted from a cloud-based architecture to a **100% localized stack** to enforce privacy and minimize recurring API costs.

### Frontend
- **Framework**: Vue 3 (Composition API) + Vite
- **Styling**: Tailwind CSS
- **State Management**: Pinia

### Backend
- **Framework**: Python FastAPI
- **Database**: PostgreSQL (Relational persistence) + Redis (In-memory caching)
- **AI/ML Layer**:
  - **Speech-to-Text**: [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) (Robust local offline model for Arabic audio)
  - **Feedback LLM**: [Ollama](https://ollama.com/) (For generating natural, privacy-first user feedback)

---

## Getting Started

Follow these instructions to run the Tajweed Coach environment locally.

### Prerequisites
- [Docker & Docker Compose](https://www.docker.com/) installed
- [Node.js](https://nodejs.org/) (v18+)
- [Ollama](https://ollama.com/) installed on your host machine to run local language models.

### Step 1: Clone and Infrastructure Setup

Boot the backend environment comprising FastAPI, PostgreSQL, and Redis:
```bash
cd backend
docker compose up -d
```
*(Note: The backend API runs on `http://localhost:8000`)*

### Step 2: Set Up Ollama

If you haven't already, install Ollama and pull your desired language model that will generate the recitation feedback.
For example, to pull Llama 3:
```bash
ollama run llama3
```
Ensure Ollama's HTTP server is running so the FastAPI backend can communicate with it to fetch human-readable suggestions.

### Step 3: Start the Frontend

In a separate terminal tab, initialize the Vue application:
```bash
cd frontend
npm install
npm run dev
```
*(The frontend runs on `http://localhost:5173` locally)*

You can now visit the URL provided by Vite and start practicing!

---

## Project Documentation

For deeper dives into how this software is orchestrated, kindly review the following manuals located in the `/docs` directory:
- 🧩 **[System Architecture](docs/SYSTEM_ARCHITECTURE.md)** (Detailed data modeling and logic loops)
- 🔌 **[API Reference](docs/API_REFERENCE.md)** (Contracts for the FastAPI Python Endpoints)

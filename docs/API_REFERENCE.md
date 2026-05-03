# API Reference

All backend API requests are prefixed under `/api/v1`. The API is built with Python FastAPI and returns JSON for all responses. Audio ingestion uses `multipart/form-data`.

**Base URL (local):** `http://localhost:8000/api/v1`

Interactive documentation is available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc`.

---

## Health Check

### `GET /health`

Simple liveness check. No authentication required.

**Response:**
```json
{ "status": "healthy", "version": "1.0.0" }
```

---

## Verses API (`/api/v1/surahs`)

Provides Surah and Ayah metadata. All endpoints are read-only and require no authentication.

### `GET /surahs`

Fetch all 114 Surahs ordered sequentially by Surah number.

**Example Response:**
```json
[
  {
    "id": 1,
    "name_arabic": "الفاتحة",
    "name_english": "Al-Fatihah",
    "ayah_count": 7,
    "revelation_type": "Meccan"
  }
]
```

---

### `GET /surahs/{surah_id}/verses`

Fetch all verses within a given Surah, ordered by Ayah number ascending.

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `surah_id` | Integer | Surah number (1–114) |

**Example Response:**
```json
[
  {
    "id": 1,
    "surah_id": 1,
    "ayah_number": 1,
    "text_arabic": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
    "text_english": "In the name of Allah, the Entirely Merciful, the Especially Merciful."
  }
]
```

**Error Responses:**

| Status | Condition |
|---|---|
| `404 Not Found` | `surah_id` does not exist or has no verses in the database |

---

## Recitation Pipeline (`/api/v1/recitations`)

The core recitation processing endpoint. Accepts a `.webm` audio blob, transcribes it via Groq Whisper, runs a word-level Arabic diff, and generates pedagogical feedback via Groq LLM.

> [!IMPORTANT]
> All audio must be submitted as raw `.webm` blobs via `multipart/form-data`. Base64-encoded audio is not accepted.

### `POST /recitations/upload`

**Content-Type:** `multipart/form-data`

**Form Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `audio_file` | File | ✅ | `.webm` audio blob captured from the browser's MediaRecorder API |
| `verse_id` | Integer | ✅ | ID of the verse the student is reciting (from `/surahs/{id}/verses`) |

**Example Response (200 OK):**
```json
{
  "session_id": "a3f2c1d4-...",
  "transcription": "بسم الله الرحمن الرحيم",
  "accuracy_score": 0.75,
  "diff": [
    { "word": "بِسْمِ", "status": "correct" },
    { "word": "اللَّهِ", "status": "correct" },
    { "word": "الرَّحْمَٰنِ", "status": "incorrect" },
    { "word": "الرَّحِيمِ", "status": "correct" }
  ],
  "feedback": "ما شاء الله, your opening was clear and well-paced! The word Al-Rahman needs slightly heavier emphasis on the letter R — try holding it a moment longer before continuing. Keep practicing and you will master it soon.",
  "duration_seconds": 0
}
```

**Response Fields:**

| Field | Type | Description |
|---|---|---|
| `session_id` | UUID string | Unique ID for this recitation attempt |
| `transcription` | String | Arabic text returned by Groq Whisper |
| `accuracy_score` | Float (0.0–1.0) | Word-level match ratio from the diff engine |
| `diff` | Array | Per-word comparison result: `{ word, status }` where `status` is `"correct"` or `"incorrect"` |
| `feedback` | String | 3–4 sentence pedagogical response from Groq LLaMA |
| `duration_seconds` | Float | Audio duration (reserved; currently always `0`) |

**Processing Pipeline (internal):**
1. The uploaded `.webm` file is saved to a temporary path inside the container.
2. The expected verse's Arabic text is fetched from PostgreSQL.
3. Groq `whisper-large-v3` transcribes the audio with the expected text injected as a prompt to improve Quranic vocabulary accuracy.
4. `diff_service` normalizes both the transcription and the expected text (strips diacritics, normalises alef/yeh variants) and computes a word-level `SequenceMatcher` diff.
5. Groq `llama-3.3-70b-versatile` generates feedback from the transcription, expected text, and diff results.
6. The temp audio file is deleted. The response is returned.

**Error Responses:**

| Status | Condition |
|---|---|
| `404 Not Found` | `verse_id` does not exist in the database |
| `422 Unprocessable Entity` | Missing or invalid form fields |
| `500 Internal Server Error` | Groq API unreachable or invalid `GROQ_API_KEY` |

---

## Authentication (`/api/v1/auth`) *(planned)*

> [!NOTE]
> Authentication routes are not yet implemented. The schema below reflects the planned design based on the existing `config.py` JWT settings (`SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`). Recitation sessions currently run as guest (no `user_id` association).

The authentication system will use **JWT Bearer tokens** issued on login and expected in the `Authorization` header of protected requests.

### `POST /auth/register`

Create a new user account.

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "securepassword"
}
```

**Example Response (201 Created):**
```json
{
  "id": "b7e3a2f1-...",
  "email": "student@example.com",
  "created_at": "2025-04-01T12:00:00Z"
}
```

**Error Responses:**

| Status | Condition |
|---|---|
| `400 Bad Request` | Email already registered |
| `422 Unprocessable Entity` | Invalid email format or missing fields |

---

### `POST /auth/login`

Authenticate and receive a JWT access token.

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "securepassword"
}
```

**Example Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Error Responses:**

| Status | Condition |
|---|---|
| `401 Unauthorized` | Invalid credentials |

---

### `GET /auth/me`

Return the currently authenticated user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Example Response (200 OK):**
```json
{
  "id": "b7e3a2f1-...",
  "email": "student@example.com",
  "created_at": "2025-04-01T12:00:00Z"
}
```

**Error Responses:**

| Status | Condition |
|---|---|
| `401 Unauthorized` | Token missing, expired, or invalid |

---

## Recitation History (`/api/v1/history`) *(planned)*

> [!NOTE]
> History endpoints are not yet implemented. They depend on the authentication system above and require persisting `user_id` on `recitation_sessions` rows at upload time.

### `GET /history`

Return a paginated list of the authenticated user's past recitation sessions, newest first.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | Integer | `1` | Page number (1-indexed) |
| `per_page` | Integer | `20` | Results per page (max 100) |

**Example Response (200 OK):**
```json
{
  "total": 47,
  "page": 1,
  "per_page": 20,
  "sessions": [
    {
      "session_id": "a3f2c1d4-...",
      "verse_id": 1,
      "surah": "Al-Fatihah",
      "ayah_number": 1,
      "accuracy_score": 0.75,
      "created_at": "2025-05-01T09:15:00Z"
    }
  ]
}
```

---

### `GET /history/{session_id}`

Return the full detail of a single past recitation session.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `session_id` | UUID string | The `session_id` from a previous upload response |

**Example Response (200 OK):**
```json
{
  "session_id": "a3f2c1d4-...",
  "verse_id": 1,
  "surah": "Al-Fatihah",
  "ayah_number": 1,
  "transcription": "بسم الله الرحمن الرحيم",
  "accuracy_score": 0.75,
  "diff": [
    { "word": "بِسْمِ", "status": "correct" },
    { "word": "اللَّهِ", "status": "correct" },
    { "word": "الرَّحْمَٰنِ", "status": "incorrect" },
    { "word": "الرَّحِيمِ", "status": "correct" }
  ],
  "feedback": "Your opening was clear and well-paced! ...",
  "created_at": "2025-05-01T09:15:00Z"
}
```

**Error Responses:**

| Status | Condition |
|---|---|
| `401 Unauthorized` | Token missing or invalid |
| `403 Forbidden` | Session belongs to a different user |
| `404 Not Found` | `session_id` does not exist |

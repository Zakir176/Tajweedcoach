# API Reference

All backend API requests are prefixed under `/api/v1` and managed by Python FastAPI. The application returns native JSON datasets across all `GET` routes, and specifically isolates raw HTTP Form Multipart processing for the audio intake endpoints.

> **💡 Interactive Docs:** When the backend is running, FastAPI auto-generates fully interactive documentation. No `curl` required — you can send real requests directly from the browser:
> - **Swagger UI:** http://localhost:8000/docs
> - **ReDoc:** http://localhost:8000/redoc
> - **OpenAPI schema:** http://localhost:8000/openapi.json

---

## Verses API (`/api/v1/surahs`)

Provides structural metadata linking standard Surah data against specific localized Ayah lookups.

### 1. `GET /surahs`
Fetch all 114 Surahs ordered sequentially.
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

### 2. `GET /surahs/{surah_id}/verses`
Fetch a chronologically descending array of all verses housed within a specific `surah_id`.
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

---

## Recitation Analytics Pipeline (`/api/v1/recitations`)

Because the core processing model requires direct ingestion of hardware-level Microphone binary blobbing, this POST relies exclusively on standard Web Multipart Forms. Let it be explicitly noted that **No Base64 Audio decoding is allowed** — pure `.webm` blobs must be directly uploaded.

### `POST /recitations/upload`

**Content-Type:** `multipart/form-data`

| Parameter | Type | Requirements |
| --- | --- | --- |
| `audio` | File Blob | Must be a webm or explicitly supported Whisper stream |
| `verse_id` | Integer | Required to isolate the targeted Diff string |
| `user_id` | Integer | Nullable. If absent, analytics are processed as Guest |

**Example Response (200 OK - Processed):**
```json
{
  "transcription": "bism allah alrahman alrahim",
  "expected": "bismillahi alrrahmani alrraheemi",
  "accuracy_score": 0.87,
  "diff": [
    { "word": "bism allah", "status": "correct" },
    { "word": "alrahman",   "status": "incorrect", "expected": "alrrahmani" }
  ],
  "feedback": "Your Bismillah opening was clear and well-paced. The letter R in Al-Rahman needs heavier emphasis — it is a heavy letter (ra mushaddada). Try holding it slightly longer before continuing.",
  "duration_seconds": 4.2
}
```

*Note on Analytics Processing:*
1. The uploaded user WebM is directly passed off to the local `Faster-Whisper` binary running on the physical disk for isolation mapping.
2. The transcript string is run through the `Python difflib` engine against `expected`.
3. An internal REST jump is securely made to the localized instances of Ollama via `httpx` to populate the final `feedback` output strings prior to the API completion return to the Frontend.

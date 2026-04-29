import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

async def transcribe(file_path: str, expected_text: str = None) -> str:
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            language="ar",
            prompt=expected_text or "",
            response_format="text"
        )
    return transcription.strip()

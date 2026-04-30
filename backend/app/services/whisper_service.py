import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

async def transcribe(file_path: str, expected_text: str = None) -> str:
    prompt = ""
    if expected_text:
        # Strip diacritics from prompt to guide Whisper
        import re
        clean = re.sub(r'[\u0610-\u061A\u064B-\u065F\u0670\u0671]', '', expected_text)
        prompt = f"بسم الله الرحمن الرحيم. {clean}"
    else:
        prompt = "بسم الله الرحمن الرحيم. القرآن الكريم."
    
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            language="ar",
            prompt=prompt,
            response_format="text"
        )
    return transcription.strip()

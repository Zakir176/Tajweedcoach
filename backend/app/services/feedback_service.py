import httpx
import json

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
MODEL_NAME = "llama3.2"

async def generate_feedback(transcription: str, expected: str, diff: list) -> str:
    """
    Generates warm, encouraging tajweed feedback using a local Ollama instance.
    """
    prompt = f"""You are a Quran recitation teacher. 
A student attempted to recite the following verse:

Expected Arabic: {expected}
Student recited: {transcription}
Word analysis: {json.dumps(diff, ensure_ascii=False)}

Give brief encouraging feedback (3-4 sentences max). 
Point out specific errors and give one concrete tip to improve. 
Be warm and supportive. 
Speak directly to the student."""

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "Keep practicing! You are making great progress.")
    except Exception as e:
        print(f"Ollama Error: {e}")
        return "Excellent attempt! Remember to focus on the articulation points of each letter. Keep practicing!"

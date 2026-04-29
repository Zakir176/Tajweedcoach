import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

async def generate_feedback(transcription: str, 
    expected: str, diff: list) -> str:
    
    prompt = f"""You are a Quran recitation teacher. 
A student attempted to recite the following verse:

Expected Arabic: {expected}
Student recited: {transcription}
Word analysis: {diff}

Give brief encouraging feedback (3-4 sentences max). 
Point out specific errors and give one concrete tip 
to improve. Be warm and supportive."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()

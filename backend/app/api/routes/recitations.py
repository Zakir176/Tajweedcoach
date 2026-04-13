import uuid
import os
import difflib
import re
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db
from app.models.verse import Verse
from app.services import whisper_service, feedback_service, diff_service

router = APIRouter()

@router.post("/upload")
async def upload_recitation(
    audio_file: UploadFile = File(...),
    verse_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # 1. Fetch expected verse text
    result = await db.execute(select(Verse).where(Verse.id == verse_id))
    verse = result.scalar_one_or_none()
    if not verse:
        raise HTTPException(status_code=404, detail="Verse not found")
        
    # 2. Save the file temporarily
    file_id = uuid.uuid4()
    temp_filename = f"/tmp/{file_id}.webm"
    os.makedirs(os.path.dirname(temp_filename), exist_ok=True)
    
    try:
        with open(temp_filename, "wb") as buffer:
            content = await audio_file.read()
            buffer.write(content)
            
        # 3. Transcribe using local Whisper
        transcription = await whisper_service.transcribe(temp_filename)
        
        # 4. Accurate Arabic comparison
        accuracy, diff_results = diff_service.compare_recitation(
            verse.text_arabic, 
            transcription
        )
        
        print(f"Whisper transcription: {transcription}")
        print(f"Expected text: {verse.text_arabic}")
        print(f"Accuracy score: {accuracy}")
        
        # 5. Generate warm feedback via local Ollama
        feedback = await feedback_service.generate_feedback(transcription, verse.text_arabic, diff_results)
        
        return {
            "session_id": str(file_id),
            "transcription": transcription,
            "accuracy_score": accuracy,
            "diff": diff_results,
            "feedback": feedback,
            "duration_seconds": 0
        }

    finally:
        # Cleanup temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

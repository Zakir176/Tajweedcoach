from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.models.verse import Surah, Verse
from pydantic import BaseModel

router = APIRouter()

# Pydantic models for responses
class SurahResponse(BaseModel):
    id: int
    name_arabic: str
    name_english: str
    ayah_count: int
    revelation_type: str

    class Config:
        from_attributes = True

class VerseResponse(BaseModel):
    id: int
    ayah_number: int
    text_arabic: str
    text_english: str

    class Config:
        from_attributes = True

@router.get("/surahs", response_model=List[SurahResponse])
async def get_surahs(db: AsyncSession = Depends(get_db)):
    """Fetch all 114 surahs ordered by ID."""
    result = await db.execute(select(Surah).order_by(Surah.id))
    return result.scalars().all()

@router.get("/surahs/{surah_id}/verses", response_model=List[VerseResponse])
async def get_verses(surah_id: int, db: AsyncSession = Depends(get_db)):
    """Fetch all verses for a given surah ID."""
    result = await db.execute(
        select(Verse).where(Verse.surah_id == surah_id).order_by(Verse.ayah_number)
    )
    verses = result.scalars().all()
    if not verses:
        raise HTTPException(status_code=404, detail="Surah not found or has no verses")
    return verses

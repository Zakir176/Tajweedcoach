import httpx
import re
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.verse import Surah, Verse

BASE_URL = "https://api.quran.com/api/v3"
TRANSLATION_ID = 131 

async def fetch_surahs(client: httpx.AsyncClient):
    response = await client.get("https://api.quran.com/api/v4/chapters?language=en")
    response.raise_for_status()
    return response.json()["chapters"]

async def fetch_verses(client: httpx.AsyncClient, surah_id: int):
    verses = []
    page = 1
    while True:
        url = f"{BASE_URL}/chapters/{surah_id}/verses?language=en&translations={TRANSLATION_ID}&per_page=50&page={page}"
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        verses.extend(data["verses"])
        pagination = data.get("pagination")
        if not pagination or pagination.get("next_page") is None:
            break
        page = pagination["next_page"]
    return verses

async def seed_quran_data(db: AsyncSession):
    # Check if data already exists
    surah_count_result = await db.execute(select(func.count(Surah.id)))
    surah_count = surah_count_result.scalar()
    
    if surah_count >= 114:
        verse_count_result = await db.execute(select(func.count(Verse.id)))
        verse_count = verse_count_result.scalar()
        return surah_count, verse_count

    async with httpx.AsyncClient(timeout=60.0) as client:
        chapters_data = await fetch_surahs(client)
        
        # Seed Surahs
        for ch in chapters_data:
            stmt = insert(Surah).values(
                id=ch["id"],
                name_arabic=ch["name_arabic"],
                name_english=ch["name_simple"],
                ayah_count=ch["verses_count"],
                revelation_type=ch["revelation_place"].capitalize()
            ).on_conflict_do_nothing()
            await db.execute(stmt)
        
        await db.commit()

        # Seed Verses
        for ch in chapters_data:
            surah_id = ch["id"]
            verses_data = await fetch_verses(client, surah_id)
            
            verse_values = []
            for v in verses_data:
                translation_text = ""
                if "translations" in v and len(v["translations"]) > 0:
                    translation_text = v["translations"][0]["text"]
                    translation_text = re.sub(r'<sup\b[^>]*>.*?</sup>', '', translation_text)
                    translation_text = re.sub(r'<[^>]+>', '', translation_text)
                
                verse_values.append({
                    "surah_id": surah_id,
                    "ayah_number": v["verse_number"],
                    "text_arabic": v.get("text_madani", ""),
                    "text_english": translation_text,
                    "page_number": v.get("page_number", 1)
                })
            
            if verse_values:
                await db.execute(delete(Verse).where(Verse.surah_id == surah_id))
                await db.execute(insert(Verse).values(verse_values))
                await db.commit()

    # Get final counts
    surah_count_result = await db.execute(select(func.count(Surah.id)))
    verse_count_result = await db.execute(select(func.count(Verse.id)))
    
    return surah_count_result.scalar(), verse_count_result.scalar()

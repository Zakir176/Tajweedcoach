import asyncio
import httpx
from sqlalchemy.dialects.postgresql import insert
from app.core.database import SessionLocal
from app.models.verse import Surah, Verse
from sqlalchemy import delete

# Stable Quran.com V3 API for bulk data with translations
BASE_URL = "https://api.quran.com/api/v3"
# Dr. Mustafa Khattab, The Clear Quran
TRANSLATION_ID = 131 

async def fetch_surahs(client: httpx.AsyncClient):
    print("Fetching Surahs...")
    # Using V4 for surahs as it's fine
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
        
        # V3 Pagination structure
        pagination = data.get("pagination")
        if not pagination or pagination.get("next_page") is None:
            break
        page = pagination["next_page"]
        
    return verses

async def seed_data():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Fetch Surahs
        chapters_data = await fetch_surahs(client)
        
        async with SessionLocal() as session:
            # Seed Surahs
            print(f"Seeding {len(chapters_data)} Surahs...")
            for ch in chapters_data:
                stmt = insert(Surah).values(
                    id=ch["id"],
                    name_arabic=ch["name_arabic"],
                    name_english=ch["name_simple"],
                    ayah_count=ch["verses_count"],
                    revelation_type=ch["revelation_place"].capitalize()
                ).on_conflict_do_nothing()
                await session.execute(stmt)
            
            await session.commit()
            print("Surahs seeding completed.")

            # 2. Fetch and Seed Verses for each Surah
            for ch in chapters_data:
                surah_id = ch["id"]
                print(f"Fetching Verses for Surah {surah_id}: {ch['name_simple']}...")
                
                verses_data = await fetch_verses(client, surah_id)
                print(f"Seeding {len(verses_data)} verses for Surah {surah_id}...")
                
                verse_values = []
                import re
                for v in verses_data:
                    # Translation text parsing from V3 structure
                    translation_text = ""
                    if "translations" in v and len(v["translations"]) > 0:
                        translation_text = v["translations"][0]["text"]
                        # Strip footnote tags and their contents (the footnote numbers)
                        translation_text = re.sub(r'<sup\b[^>]*>.*?</sup>', '', translation_text)
                        # Also strip any other stray HTML tags
                        translation_text = re.sub(r'<[^>]+>', '', translation_text)
                    
                    verse_values.append({
                        "surah_id": surah_id,
                        "ayah_number": v["verse_number"],
                        "text_arabic": v.get("text_madani", ""),
                        "text_english": translation_text,
                        "page_number": v.get("page_number", 1)
                    })
                
                if verse_values:
                    # Clean up existing verses for this surah first to ensure accuracy
                    await session.execute(delete(Verse).where(Verse.surah_id == surah_id))
                    
                    # Batch insert
                    await session.execute(insert(Verse).values(verse_values))
                    await session.commit()
                    print(f"Surah {surah_id} completed.")

    print("Seeding process finished successfully with accurate Quran.com V3/V4 data!")

if __name__ == "__main__":
    asyncio.run(seed_data())

import asyncio
from app.core.database import engine, Base
from app.models import User, Surah, Verse, RecitationSession  # Essential for registration

async def init_db():
    async with engine.begin() as conn:
        # Import all models before calling create_all
        # to ensure they are registered with the Base metadata.
        print("Creating table structures...")
        await conn.run_sync(Base.metadata.create_all)
        print("All tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())

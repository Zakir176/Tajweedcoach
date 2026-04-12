from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Surah(Base):
    __tablename__ = "surahs"

    id = Column(Integer, primary_key=True) # 1 to 114
    name_arabic = Column(String(100), nullable=False)
    name_english = Column(String(100), nullable=False)
    ayah_count = Column(Integer, nullable=False)
    revelation_type = Column(String(10), nullable=False) # Meccan or Medinan

    verses = relationship("Verse", back_populates="surah")

class Verse(Base):
    __tablename__ = "verses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    surah_id = Column(Integer, ForeignKey("surahs.id"), nullable=False)
    ayah_number = Column(Integer, nullable=False)
    text_arabic = Column(Text, nullable=False)
    text_english = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=True)

    surah = relationship("Surah", back_populates="verses")
    recitations = relationship("RecitationSession", back_populates="verse")

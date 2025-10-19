from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)

    cards = relationship("Card", back_populates="deck", cascade="all, delete-orphan")

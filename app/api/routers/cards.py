from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.card import CardCreate, CardOut
from app.services.storage import DatabaseStorage

router = APIRouter(prefix="/cards", tags=["cards"])


@router.post("", response_model=CardOut)
def create_card(payload: CardCreate, db: Session = Depends(get_db)):
    storage = DatabaseStorage(db)
    card = storage.create_card(payload.deck_id, payload.front, payload.back)
    if not card:
        raise HTTPException(status_code=404, detail="deck not found")
    return card


@router.get("/{card_id}", response_model=CardOut)
def get_card(card_id: int, db: Session = Depends(get_db)):
    storage = DatabaseStorage(db)
    card = storage.get_card(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="card not found")
    return card

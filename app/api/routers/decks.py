from fastapi import APIRouter, HTTPException

from app.schemas.deck import DeckCreate, DeckOut, DeckUpdate
from app.services import storage

router = APIRouter(prefix="/decks", tags=["decks"])


@router.post("", response_model=DeckOut)
def create_deck(payload: DeckCreate):
    deck = storage.create_deck(payload.title)
    return deck


@router.get("", response_model=list[DeckOut])
def list_decks():
    return storage.list_decks()


@router.get("/{deck_id}", response_model=DeckOut)
def get_deck(deck_id: int):
    deck = storage.get_deck(deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="deck not found")
    return deck


@router.patch("/{deck_id}", response_model=DeckOut)
def update_deck(deck_id: int, payload: DeckUpdate):
    deck = storage.update_deck(deck_id, payload.title)
    if not deck:
        raise HTTPException(status_code=404, detail="deck not found")
    return deck


@router.delete("/{deck_id}", status_code=204)
def delete_deck(deck_id: int):
    deleted = storage.delete_deck(deck_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="deck not found")

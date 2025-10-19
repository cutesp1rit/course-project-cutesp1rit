from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.card import Card
from app.models.deck import Deck


class DatabaseStorage:
    def __init__(self, db: Session):
        self.db = db

    # Decks
    def create_deck(self, title: str) -> Dict:
        deck = Deck(title=title)
        self.db.add(deck)
        self.db.commit()
        self.db.refresh(deck)
        return {"id": deck.id, "title": deck.title}

    def list_decks(self) -> List[Dict]:
        decks = self.db.query(Deck).all()
        return [{"id": deck.id, "title": deck.title} for deck in decks]

    def get_deck(self, deck_id: int) -> Optional[Dict]:
        deck = self.db.query(Deck).filter(Deck.id == deck_id).first()
        if not deck:
            return None
        return {"id": deck.id, "title": deck.title}

    def update_deck(self, deck_id: int, title: Optional[str]) -> Optional[Dict]:
        deck = self.db.query(Deck).filter(Deck.id == deck_id).first()
        if not deck:
            return None
        if title is not None:
            deck.title = title
            self.db.commit()
            self.db.refresh(deck)
        return {"id": deck.id, "title": deck.title}

    def delete_deck(self, deck_id: int) -> bool:
        deck = self.db.query(Deck).filter(Deck.id == deck_id).first()
        if not deck:
            return False
        self.db.delete(deck)
        self.db.commit()
        return True

    # Cards
    def create_card(self, deck_id: int, front: str, back: str) -> Optional[Dict]:
        # Check if deck exists
        deck = self.db.query(Deck).filter(Deck.id == deck_id).first()
        if not deck:
            return None
        card = Card(deck_id=deck_id, front=front, back=back)
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return {
            "id": card.id,
            "deck_id": card.deck_id,
            "front": card.front,
            "back": card.back,
        }

    def get_card(self, card_id: int) -> Optional[Dict]:
        card = self.db.query(Card).filter(Card.id == card_id).first()
        if not card:
            return None
        return {
            "id": card.id,
            "deck_id": card.deck_id,
            "front": card.front,
            "back": card.back,
        }

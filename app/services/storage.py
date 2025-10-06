from typing import Dict, List, Optional


class InMemoryStorage:
    def __init__(self):
        self.decks: List[Dict] = []
        self.cards: List[Dict] = []
        self._deck_id = 0
        self._card_id = 0

    # Decks
    def create_deck(self, title: str) -> Dict:
        self._deck_id += 1
        deck = {"id": self._deck_id, "title": title}
        self.decks.append(deck)
        return deck

    def list_decks(self) -> List[Dict]:
        return list(self.decks)

    def get_deck(self, deck_id: int) -> Optional[Dict]:
        return next((d for d in self.decks if d["id"] == deck_id), None)

    def update_deck(self, deck_id: int, title: Optional[str]) -> Optional[Dict]:
        deck = self.get_deck(deck_id)
        if not deck:
            return None
        if title is not None:
            deck["title"] = title
        return deck

    def delete_deck(self, deck_id: int) -> bool:
        before = len(self.decks)
        self.decks = [d for d in self.decks if d["id"] != deck_id]
        # каскадно удалим карточки этой колоды
        self.cards = [c for c in self.cards if c["deck_id"] != deck_id]
        return len(self.decks) < before

    # Cards
    def create_card(self, deck_id: int, front: str, back: str) -> Optional[Dict]:
        if not self.get_deck(deck_id):
            return None
        self._card_id += 1
        card = {"id": self._card_id, "deck_id": deck_id, "front": front, "back": back}
        self.cards.append(card)
        return card

    def get_card(self, card_id: int) -> Optional[Dict]:
        return next((c for c in self.cards if c["id"] == card_id), None)

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_card(test_db):
    r = client.post("/decks", json={"title": "Deck for cards"})
    deck_id = r.json()["id"]

    r = client.post(
        "/cards", json={"deck_id": deck_id, "front": "manger", "back": "to eat"}
    )
    assert r.status_code == 200
    card = r.json()
    assert card["deck_id"] == deck_id and card["id"] >= 1

    r = client.get(f"/cards/{card['id']}")
    assert r.status_code == 200
    assert r.json() == card


def test_create_card_on_missing_deck(test_db):
    r = client.post("/cards", json={"deck_id": 999999, "front": "x", "back": "y"})
    assert r.status_code == 404

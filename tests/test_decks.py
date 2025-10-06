from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_deck():
    r = client.post("/decks", json={"title": "French A1"})
    assert r.status_code == 200
    deck = r.json()
    assert deck["id"] >= 1 and deck["title"] == "French A1"

    r = client.get(f"/decks/{deck['id']}")
    assert r.status_code == 200
    assert r.json() == deck


def test_list_and_update_and_delete_deck():
    r = client.post("/decks", json={"title": "Temp"})
    deck = r.json()
    did = deck["id"]

    r = client.get("/decks")
    assert r.status_code == 200
    assert any(d["id"] == did for d in r.json())

    r = client.patch(f"/decks/{did}", json={"title": "Temp v2"})
    assert r.status_code == 200
    assert r.json()["title"] == "Temp v2"

    r = client.delete(f"/decks/{did}")
    assert r.status_code == 204

    r = client.get(f"/decks/{did}")
    assert r.status_code == 404

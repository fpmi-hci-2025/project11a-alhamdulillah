from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_menu():
    response = client.get("/api/menu")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_categories():
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

def test_get_menu_item_not_found():
    response = client.get("/api/menu/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404





import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from autorestify.api.router_factory import create_router
from autorestify.storage.base import Database


@pytest.fixture
def client():
    """
    Create a TestClient with isolated in-memory database.
    """

    app = FastAPI()

    # In-memory SQLite database (isolated per test)
    test_db = Database(database_url="sqlite:///:memory:")

    app.include_router(create_router(database=test_db))

    return TestClient(app)


def test_upload_and_crud(client: TestClient):
    payload = {
        "collection": "clientes",
        "documents": [
            {"name": "Ana", "age": 30},
            {"name": "Carlos", "age": 25},
        ],
    }

    # -------------------------
    # Upload collection
    # -------------------------
    response = client.post("/upload", json=payload)
    assert response.status_code == 200

    # -------------------------
    # List
    # -------------------------
    response = client.get("/clientes")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2

    # -------------------------
    # Create new item
    # -------------------------
    response = client.post(
        "/clientes",
        json={"name": "Joao", "age": 40},
    )
    assert response.status_code == 200

    new_id = response.json()["id"]
    assert isinstance(new_id, int)

    # -------------------------
    # Get item
    # -------------------------
    response = client.get(f"/clientes/{new_id}")
    assert response.status_code == 200

    item = response.json()
    assert item["name"] == "Joao"
    assert item["age"] == 40

    # -------------------------
    # Update item
    # -------------------------
    response = client.put(
        f"/clientes/{new_id}",
        json={"age": 41},
    )
    assert response.status_code == 200

    response = client.get(f"/clientes/{new_id}")
    assert response.json()["age"] == 41

    # -------------------------
    # Delete item
    # -------------------------
    response = client.delete(f"/clientes/{new_id}")
    assert response.status_code == 200

    response = client.get(f"/clientes/{new_id}")
    assert response.status_code == 404

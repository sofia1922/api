from fastapi.testclient import TestClient
from main import app
import pytest

def test_create_book(client):
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": "Author",
        "description": "Desc",
        "status": "available",
        "year": 2020
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Book"

def test_get_books(client):
    # Create a book first
    client.post("/books/", json={
        "title": "Test Book 2",
        "author": "Author 2",
        "description": "Desc 2",
        "status": "available",
        "year": 2021
    })

    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_books_pagination(client):
    # Create multiple books
    for i in range(5):
        client.post("/books/", json={
            "title": f"Test Book {i}",
            "author": f"Author {i}",
            "description": f"Desc {i}",
            "status": "available",
            "year": 2020 + i
        })

    # Test limit
    response = client.get("/books/?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Test skip
    response = client.get("/books/?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_delete_idempotent(client):
    response = client.delete("/books/123")
    assert response.status_code == 204
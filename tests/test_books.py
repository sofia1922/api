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
    assert "data" in data
    assert "pagination" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 1
    assert data["pagination"]["offset"] == 0
    assert data["pagination"]["limit"] == 100
    assert data["pagination"]["has_next"] in (True, False)
    assert data["pagination"]["has_prev"] == False
    assert "next_cursor" in data["pagination"]

def test_get_books_pagination_success(client):
    
    for i in range(5):
        client.post("/books/", json={
            "title": f"Test Book {i}",
            "author": f"Author {i}",
            "description": f"Desc {i}",
            "status": "available",
            "year": 2020 + i
        })

    response = client.get("/books/?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["pagination"]["limit"] == 2
    assert data["pagination"]["has_next"] == True
    assert data["pagination"]["next_cursor"] is not None

    next_cursor = data["pagination"]["next_cursor"]
    response = client.get(f"/books/?cursor={next_cursor}&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["pagination"]["has_next"] in (True, False)

    response = client.get("/books/?offset=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["pagination"]["offset"] == 2
    assert data["pagination"]["has_prev"] == True


def test_get_books_pagination_offset_out_of_range(client):
    for i in range(3):
        client.post("/books/", json={
            "title": f"Edge Book {i}",
            "author": f"Edge Author {i}",
            "description": f"Edge Desc {i}",
            "status": "available",
            "year": 2020 + i
        })

    response = client.get("/books/?offset=100&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == []
    assert data["pagination"]["has_next"] == False
    assert data["pagination"]["has_prev"] == True
    assert data["pagination"]["next_cursor"] is None


def test_get_books_pagination_invalid_cursor(client):
    for i in range(3):
        client.post("/books/", json={
            "title": f"Edge Book {i}",
            "author": f"Edge Author {i}",
            "description": f"Edge Desc {i}",
            "status": "available",
            "year": 2020 + i
        })

    response = client.get("/books/?cursor=00000000-0000-0000-0000-000000000000&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["data"], list)
    assert data["pagination"]["has_next"] in (True, False)


def test_cursor_and_offset_conflict(client):
    response = client.get("/books/?offset=2&cursor=123&limit=2")
    assert response.status_code == 400


def test_get_book_not_found(client):
    response = client.get("/books/nonexistent-id")
    assert response.status_code == 404


def test_delete_idempotent(client):
    response = client.delete("/books/123")
    assert response.status_code == 204
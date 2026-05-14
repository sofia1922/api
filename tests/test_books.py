def create_book(client, title="API Book", author="API Author", description="Desc", status="available", year=2023):
    payload = {
        "title": title,
        "author": author,
        "description": description,
        "status": status,
        "year": year,
    }
    response = client.post("/books/", json=payload)
    assert response.status_code == 201
    return response.get_json()


def test_create_book_http(client):
    result = create_book(client)

    assert result["title"] == "API Book"
    assert result["author"] == "API Author"
    assert result["status"] == "available"


def test_list_books_http(client):
    create_book(client, title="Book 1")
    create_book(client, title="Book 2")
    create_book(client, title="Book 3")

    response = client.get("/books/?offset=0&limit=2")

    assert response.status_code == 200
    data = response.get_json()
    assert data["pagination"]["total"] == 3
    assert len(data["data"]) == 2


def test_get_book_http(client):
    book = create_book(client, title="Get Me")

    response = client.get(f"/books/{book['id']}")

    assert response.status_code == 200
    assert response.get_json()["id"] == book["id"]
    assert response.get_json()["title"] == "Get Me"


def test_get_nonexistent_book_http(client):
    response = client.get("/books/nonexistent-id")

    assert response.status_code == 404


def test_delete_book_http(client):
    book = create_book(client, title="To Delete")

    response = client.delete(f"/books/{book['id']}")

    assert response.status_code == 204

    get_response = client.get(f"/books/{book['id']}")
    assert get_response.status_code == 404


def test_delete_nonexistent_book_http(client):
    response = client.delete("/books/nonexistent-id")

    assert response.status_code == 404


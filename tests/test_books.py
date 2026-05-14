import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from repository.book_repository import add, get_all, get_by_id, delete
from schemas.book import BookCreate

TEST_MONGODB_URL = "mongodb://admin:password@localhost:27017/test_library_db?authSource=admin"

@pytest.mark.asyncio
async def test_repository_lifecycle():
    client = AsyncIOMotorClient(TEST_MONGODB_URL)
    db = client.test_library_db
    await db.books.delete_many({})

    book_data = BookCreate(title="Test", author="Auth", description="D", status="available", year=2020)
    
    book = await add(db, book_data)
    assert book.id is not None
    
    found = await get_by_id(db, book.id)
    assert found.title == "Test"
    
    result = await delete(db, book.id)
    assert result is True
    
    client.close()

@pytest.mark.asyncio
async def test_repository_pagination(db):
    await db.books.delete_many({})
    
    for i in range(5):
        await add(db, BookCreate(title=f"B{i}", author="A", description="D", status="available", year=2020))

    books, total = await get_all(db, offset=0, limit=2)
    
    assert len(books) == 2 
    assert total == 5      

@pytest.mark.asyncio
async def test_create_book_http(client):
    payload = {"title": "API Book", "author": "API Author", "description": "D", "status": "available", "year": 2023}
    response = await client.post("/books/", json=payload)
    
    assert response.status_code == 201 
    assert response.json()["title"] == "API Book"

@pytest.mark.asyncio
async def test_get_book_http(client, db):
    book = await add(db, BookCreate(title="T", author="A", description="D", status="available", year=2020))
    
    response = await client.get(f"/books/{book.id}")
    assert response.status_code == 200  
    assert response.json()["id"] == book.id

@pytest.mark.asyncio
async def test_get_nonexistent_book_http(client):
    response = await client.get("/books/nonexistent-id")
    assert response.status_code == 404  

@pytest.mark.asyncio
async def test_delete_book_http(client, db):
    book = await add(db, BookCreate(title="To Delete", author="A", description="D", status="available", year=2020))
    
    response = await client.delete(f"/books/{book.id}")
    assert response.status_code == 204  

@pytest.mark.asyncio
async def test_delete_nonexistent_book_http(client):
    response = await client.delete("/books/nonexistent-id")
    assert response.status_code == 404  

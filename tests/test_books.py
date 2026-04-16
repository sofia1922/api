import pytest
from motor.motor_asyncio import AsyncIOMotorClient

TEST_MONGODB_URL = "mongodb://admin:password@localhost:27017/test_library_db?authSource=admin"

@pytest.mark.asyncio
async def test_create_book():
    client = AsyncIOMotorClient(TEST_MONGODB_URL)
    database = client.test_library_db
    
    # Clear collection
    await database.books.delete_many({})
    
    from repository.book_repository import add
    from schemas.book import BookCreate
    
    book_data = BookCreate(
        title="Test Book",
        author="Author",
        description="Desc",
        status="available",
        year=2020
    )
    
    book = await add(database, book_data)
    
    assert book.title == "Test Book"
    assert book.author == "Author"
    assert book.status == "available"
    assert book.year == 2020
    assert book.id is not None
    
    # Verify in database
    doc = await database.books.find_one({"id": book.id})
    assert doc is not None
    assert doc["title"] == "Test Book"
    
    client.close()

@pytest.mark.asyncio
async def test_get_books_pagination():
    client = AsyncIOMotorClient(TEST_MONGODB_URL)
    database = client.test_library_db
    
    # Clear collection
    await database.books.delete_many({})
    
    from repository.book_repository import add, get_all
    from schemas.book import BookCreate
    
    # Add test books
    for i in range(5):
        book_data = BookCreate(
            title=f"Test Book {i}",
            author=f"Author {i}",
            description=f"Desc {i}",
            status="available",
            year=2020 + i
        )
        await add(database, book_data)
    
    # Test pagination
    books, total = await get_all(database, offset=0, limit=2)
    assert len(books) == 2
    assert total == 5
    
    books, total = await get_all(database, offset=2, limit=2)
    assert len(books) == 2
    assert total == 5
    
    client.close()
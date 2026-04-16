from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional, Tuple
from models.book_model import Book
from schemas.book import BookCreate

async def get_all(db: AsyncIOMotorDatabase, offset: int = 0, limit: int = 100,
                  status: Optional[str] = None, author: Optional[str] = None,
                  sort_by: Optional[str] = None) -> Tuple[List[Book], int]:
    collection = db.books

    # Build filter
    filter_query = {}
    if status:
        filter_query["status"] = status
    if author:
        filter_query["author"] = {"$regex": author, "$options": "i"}  # Case-insensitive search

    # Get total count
    total = await collection.count_documents(filter_query)

    # Build sort
    sort_query = []
    if sort_by == "title":
        sort_query = [("title", 1)]
    elif sort_by == "year":
        sort_query = [("year", 1)]

    # Get documents with pagination
    if sort_query:
        cursor = collection.find(filter_query).sort(sort_query).skip(offset).limit(limit)
    else:
        cursor = collection.find(filter_query).skip(offset).limit(limit)
    documents = await cursor.to_list(length=None)

    # Convert to Book models
    books = [Book(**doc) for doc in documents]

    return books, total

async def get_by_id(db: AsyncIOMotorDatabase, book_id: str) -> Optional[Book]:
    collection = db.books
    document = await collection.find_one({"id": book_id})
    if document:
        return Book(**document)
    return None

async def add(db: AsyncIOMotorDatabase, book_data: BookCreate) -> Book:
    collection = db.books
    book_dict = book_data.model_dump()
    book = Book(**book_dict)
    await collection.insert_one(book.model_dump())
    return book

async def delete(db: AsyncIOMotorDatabase, book_id: str) -> bool:
    collection = db.books
    result = await collection.delete_one({"id": book_id})
    return result.deleted_count > 0
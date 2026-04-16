from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional, Tuple
from repository import book_repository
from models.book_model import Book
from schemas.book import BookCreate

async def get_books(db: AsyncIOMotorDatabase, offset: int = 0, limit: int = 100,
                   status: Optional[str] = None, author: Optional[str] = None,
                   sort_by: Optional[str] = None) -> Tuple[List[Book], int]:
    return await book_repository.get_all(db, offset, limit, status, author, sort_by)

async def get_book(db: AsyncIOMotorDatabase, book_id: str) -> Optional[Book]:
    return await book_repository.get_by_id(db, book_id)

async def create_book(db: AsyncIOMotorDatabase, book_data: BookCreate) -> Book:
    return await book_repository.add(db, book_data)

async def delete_book(db: AsyncIOMotorDatabase, book_id: str) -> bool:
    return await book_repository.delete(db, book_id)
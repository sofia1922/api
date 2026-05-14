from typing import List, Optional, Tuple
from repository import book_repository
from models.book_model import Book
from schemas.book import BookCreate


def get_books(
    db: Optional[object],
    offset: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    author: Optional[str] = None,
    sort_by: Optional[str] = None,
) -> Tuple[List[Book], int]:
    return book_repository.get_all(db, offset, limit, status, author, sort_by)


def get_book(db: Optional[object], book_id: str) -> Optional[Book]:
    return book_repository.get_by_id(db, book_id)


def create_book(db: Optional[object], book_data: BookCreate) -> Book:
    return book_repository.add(db, book_data)


def delete_book(db: Optional[object], book_id: str) -> bool:
    return book_repository.delete(db, book_id)

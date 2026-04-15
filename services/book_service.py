from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from repository import book_repository
from models.book_model import Book
from schemas.book import BookCreate
from database import get_db

def get_books(db: Session, offset: int = 0, cursor: Optional[str] = None, limit: int = 100,
              status: Optional[str] = None, author: Optional[str] = None,
              sort_by: Optional[str] = None) -> Tuple[List[Book], Optional[int], Optional[str], bool]:
    return book_repository.get_all(db, offset, cursor, limit, status, author, sort_by)

def get_book(db: Session, book_id: str) -> Optional[Book]:
    return book_repository.get_by_id(db, book_id)

def create_book(db: Session, book_data: BookCreate) -> Book:
    return book_repository.add(db, book_data)

def delete_book(db: Session, book_id: str):
    book_repository.delete(db, book_id)

def get_book(db: Session, book_id: str) -> Optional[Book]:
    return book_repository.get_by_id(db, book_id)

def create_book(db: Session, book_data: BookCreate) -> Book:
    return book_repository.add(db, book_data)

def delete_book(db: Session, book_id: str):
    book_repository.delete(db, book_id)
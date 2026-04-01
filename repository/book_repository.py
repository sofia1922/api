from sqlalchemy.orm import Session
from typing import List, Optional
from models.book_model import Book
from schemas.book import BookCreate

def get_all(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None, author: Optional[str] = None, sort_by: Optional[str] = None):
    query = db.query(Book)

    if status:
        query = query.filter(Book.status == status)

    if author:
        query = query.filter(Book.author == author)

    if sort_by == "title":
        query = query.order_by(Book.title)
    elif sort_by == "year":
        query = query.order_by(Book.year)

    return query.offset(skip).limit(limit).all()

def get_by_id(db: Session, book_id: str) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()

def add(db: Session, book_data: BookCreate) -> Book:
    book = Book(**book_data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def delete(db: Session, book_id: str):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
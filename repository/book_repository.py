from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from models.book_model import Book
from schemas.book import BookCreate

def get_all(db: Session, offset: int = 0, cursor: Optional[str] = None, limit: int = 100,
            status: Optional[str] = None, author: Optional[str] = None,
            sort_by: Optional[str] = None) -> Tuple[List[Book], Optional[int], Optional[str], bool]:
    query = db.query(Book)

    if status:
        query = query.filter(Book.status == status)

    if author:
        query = query.filter(Book.author == author)

    if cursor:
        # Cursor pagination with stable ordering
        if sort_by == "title":
            query = query.order_by(Book.title, Book.id)
        elif sort_by == "year":
            query = query.order_by(Book.year, Book.id)
        else:
            query = query.order_by(Book.id)

        cursor_book = db.query(Book).filter(Book.id == cursor).first()
        if cursor_book:
            if sort_by == "title":
                query = query.filter(
                    (Book.title > cursor_book.title) |
                    ((Book.title == cursor_book.title) & (Book.id > cursor))
                )
            elif sort_by == "year":
                query = query.filter(
                    (Book.year > cursor_book.year) |
                    ((Book.year == cursor_book.year) & (Book.id > cursor))
                )
            else:
                query = query.filter(Book.id > cursor)

        books = query.limit(limit + 1).all()
        next_cursor = None
        if len(books) > limit:
            next_cursor = books[-1].id
            books = books[:-1]

        return books, None, next_cursor, False

    # Offset pagination falls back here
    if sort_by == "title":
        query = query.order_by(Book.title, Book.id)
    elif sort_by == "year":
        query = query.order_by(Book.year, Book.id)
    else:
        query = query.order_by(Book.id)

    total = query.count()
    books = query.offset(offset).limit(limit).all()
    has_prev = offset > 0
    next_cursor = None
    if books and (offset + len(books)) < total:
        next_cursor = books[-1].id

    return books, total, next_cursor, has_prev

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
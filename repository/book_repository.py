from typing import List, Optional, Tuple
from models.book_model import Book
from schemas.book import BookCreate

_BOOKS: List[Book] = []


def _filter_books(
    books: List[Book],
    status: Optional[str],
    author: Optional[str],
) -> List[Book]:
    result = books
    if status:
        result = [book for book in result if book.status == status]
    if author:
        result = [book for book in result if author.lower() in book.author.lower()]
    return result


def get_all(
    db: Optional[object],
    offset: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    author: Optional[str] = None,
    sort_by: Optional[str] = None,
) -> Tuple[List[Book], int]:
    books = _filter_books(_BOOKS, status, author)

    if sort_by == "title":
        books = sorted(books, key=lambda book: book.title)
    elif sort_by == "year":
        books = sorted(books, key=lambda book: book.year)

    total = len(books)
    paginated = books[offset : offset + limit]
    return paginated, total


def clear(db: Optional[object] = None) -> None:
    _BOOKS.clear()


def get_by_id(db: Optional[object], book_id: str) -> Optional[Book]:
    for book in _BOOKS:
        if book.id == book_id:
            return book
    return None


def add(db: Optional[object], book_data: BookCreate) -> Book:
    book = Book(**book_data.model_dump())
    _BOOKS.append(book)
    return book


def delete(db: Optional[object], book_id: str) -> bool:
    global _BOOKS
    for index, book in enumerate(_BOOKS):
        if book.id == book_id:
            del _BOOKS[index]
            return True
    return False
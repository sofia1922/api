from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas.book import BookCreate, BookResponse, BooksResponse, PaginationMeta
from services import book_service
from database import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=BooksResponse)
async def get_books(db: Session = Depends(get_db),
                    offset: int = Query(0, ge=0),
                    cursor: Optional[str] = None,
                    limit: int = Query(100, ge=1, le=1000),
                    status: Optional[str] = None,
                    author: Optional[str] = None,
                    sort_by: Optional[str] = Query(None, pattern="^(title|year)$")):
    if cursor and offset != 0:
        raise HTTPException(status_code=400, detail="Use either cursor or offset, not both")

    books, total, next_cursor, has_prev = book_service.get_books(
        db, offset, cursor, limit, status, author, sort_by
    )

    has_next = next_cursor is not None if cursor else (offset + limit) < (total or 0)

    pagination = PaginationMeta(
        total=total,
        offset=offset,
        limit=limit,
        has_next=has_next,
        has_prev=has_prev,
        next_cursor=next_cursor
    )

    return BooksResponse(data=books, pagination=pagination)

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: str, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse,
             status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(db, book)

@router.delete("/{book_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db: Session = Depends(get_db)):
    book_service.delete_book(db, book_id)
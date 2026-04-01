from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas.book import BookCreate, BookResponse
from services import book_service
from database import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookResponse])
async def get_books(db: Session = Depends(get_db),
                    skip: int = Query(0, ge=0),
                    limit: int = Query(100, ge=1, le=1000),
                    status: Optional[str] = None,
                    author: Optional[str] = None,
                    sort_by: Optional[str] = Query(None, pattern="^(title|year)$")):
    return book_service.get_books(db, skip, limit, status, author, sort_by)

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
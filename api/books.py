from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.book import BookCreate, BookResponse, BooksResponse, PaginationMeta
from services import book_service
from database import get_database
from api.auth import get_current_user
from models.user_model import User

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=BooksResponse)
async def get_books(db: AsyncIOMotorDatabase = Depends(get_database),
                    offset: int = Query(0, ge=0),
                    limit: int = Query(100, ge=1, le=1000),
                    status: Optional[str] = None,
                    author: Optional[str] = None,
                    sort_by: Optional[str] = Query(None, pattern="^(title|year)$"),
                    current_user: User = Depends(get_current_user)):
    books, total = await book_service.get_books(db, offset, limit, status, author, sort_by)

    has_next = (offset + limit) < total
    has_prev = offset > 0

    pagination = PaginationMeta(
        total=total,
        offset=offset,
        limit=limit,
        has_next=has_next,
        has_prev=has_prev
    )

    return BooksResponse(data=books, pagination=pagination)

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_database),
                   current_user: User = Depends(get_current_user)):
    book = await book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse,
             status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncIOMotorDatabase = Depends(get_database),
                      current_user: User = Depends(get_current_user)):
    return await book_service.create_book(db, book)

@router.delete("/{book_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_database),
                      current_user: User = Depends(get_current_user)):
    deleted = await book_service.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
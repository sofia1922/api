from typing import List, Optional
from repository import book_repository
from models.book_model import create_book_dict

async def get_books(status: Optional[str] = None,
                    author: Optional[str] = None,
                    sort_by: Optional[str] = None):

    books = await book_repository.get_all()

    if status:
        books = [b for b in books if b["status"] == status]

    if author:
        books = [b for b in books if b["author"] == author]

    if sort_by == "title":
        books = sorted(books, key=lambda x: x["title"])
    elif sort_by == "year":
        books = sorted(books, key=lambda x: x["year"])

    return books


async def get_book(book_id: str):
    return await book_repository.get_by_id(book_id)


async def create_book(data: dict):
    book = create_book_dict(data)
    return await book_repository.add(book)


async def delete_book(book_id: str):
    await book_repository.delete(book_id)
from typing import List, Dict, Optional

books_db: List[Dict] = []

async def get_all():
    return books_db

async def get_by_id(book_id: str) -> Optional[Dict]:
    return next((b for b in books_db if b["id"] == book_id), None)

async def add(book: Dict):
    books_db.append(book)
    return book

async def delete(book_id: str):
    global books_db
    books_db = [b for b in books_db if b["id"] != book_id]
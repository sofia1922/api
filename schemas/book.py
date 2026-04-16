from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from enum import Enum
from typing import List

class BookStatus(str, Enum):
    available = "available"
    issued = "issued"

class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str
    status: BookStatus
    year: int = Field(ge=1500, le=2100)

class BookResponse(BookCreate):
    id: str

    model_config = ConfigDict(from_attributes=True)

class PaginationMeta(BaseModel):
    total: int
    offset: int
    limit: int
    has_next: bool
    has_prev: bool

class BooksResponse(BaseModel):
    data: List[BookResponse]
    pagination: PaginationMeta
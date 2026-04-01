from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from enum import Enum

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
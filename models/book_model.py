from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4
from schemas.book import BookStatus

class Book(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str
    status: BookStatus
    year: int = Field(ge=1500, le=2100)
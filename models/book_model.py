from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from database import Base
from schemas.book import BookStatus
import uuid

class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLEnum(BookStatus), nullable=False)
    year = Column(Integer, nullable=False)
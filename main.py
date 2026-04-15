from contextlib import asynccontextmanager
from fastapi import FastAPI
from api import books
from database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(books.router)
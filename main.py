from contextlib import asynccontextmanager
from fastapi import FastAPI
from api import books
from database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    # Add cleanup code here if needed

app = FastAPI(lifespan=lifespan)

app.include_router(books.router)
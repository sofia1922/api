from contextlib import asynccontextmanager
from fastapi import FastAPI
from api import books, auth
from database import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(books.router)    
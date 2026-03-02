from fastapi import FastAPI
from api import books

app = FastAPI()

app.include_router(books.router)
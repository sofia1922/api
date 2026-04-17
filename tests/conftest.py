import os
import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient, ASGITransport

from main import app
from database import get_database

TEST_MONGODB_URL = "mongodb://admin:password@localhost:27017/test_library_db?authSource=admin"

@pytest_asyncio.fixture(scope="function")
async def db():
    client = AsyncIOMotorClient(TEST_MONGODB_URL)
    database = client.test_library_db
    
    await database.books.delete_many({})
    
    yield database  
    
    await database.books.delete_many({})
    client.close()

@pytest_asyncio.fixture(scope="function")
async def client():
    async def override_get_database():
        client = AsyncIOMotorClient(TEST_MONGODB_URL)
        database = client.test_library_db
        try:
            yield database
        finally:
            client.close()

    app.dependency_overrides[get_database] = override_get_database
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()
import os
os.environ["MONGODB_URL"] = "mongodb://admin:password@localhost:27017/test_library_db?authSource=admin"

import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from database import get_database
from main import app
from httpx import AsyncClient

TEST_MONGODB_URL = "mongodb://admin:password@localhost:27017/test_library_db?authSource=admin"

@pytest.fixture(scope="function")
async def db():
    client = AsyncIOMotorClient(TEST_MONGODB_URL)
    database = client.test_library_db

    # Clear the collection before each test
    await database.books.delete_many({})

    try:
        yield database
    finally:
        await database.books.delete_many({})
        client.close()

@pytest.fixture
async def client():
    async def override_get_database():
        client = AsyncIOMotorClient(TEST_MONGODB_URL)
        database = client.test_library_db
        try:
            yield database
        finally:
            client.close()

    app.dependency_overrides[get_database] = override_get_database
    client = AsyncClient(app=app, base_url="http://testserver")
    yield client
    await client.aclose()
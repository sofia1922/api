from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://admin:password@localhost:27017/library_db?authSource=admin")

client: AsyncIOMotorClient = None
database = None

async def connect_to_mongo():
    global client, database
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        database = client.library_db
        await client.admin.command('ping')
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        database = None

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")

async def get_database():
    global database
    if database is None:
        await connect_to_mongo()
    if database is None:
        raise Exception("Database connection failed")
    yield database
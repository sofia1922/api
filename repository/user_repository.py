from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional
from models.user_model import User
from schemas.auth import UserCreate

async def get_by_username(db: AsyncIOMotorDatabase, username: str) -> Optional[User]:
    collection = db.users
    document = await collection.find_one({"username": username})
    if document:
        return User(**document)
    return None

async def get_by_id(db: AsyncIOMotorDatabase, user_id: str) -> Optional[User]:
    collection = db.users
    document = await collection.find_one({"id": user_id})
    if document:
        return User(**document)
    return None

async def add(db: AsyncIOMotorDatabase, user: User) -> User:
    collection = db.users
    await collection.insert_one(user.model_dump())
    return user
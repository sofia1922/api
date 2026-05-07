from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.auth import UserCreate, UserLogin, Token
from services import auth_service
from database import get_database
from repository import user_repository

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    user = await auth_service.create_user(db, user_data)
    return {"message": "User created successfully", "user_id": user.id}

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: AsyncIOMotorDatabase = Depends(get_database)):
    user = await auth_service.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(data={"sub": user.username})
    refresh_token = auth_service.create_refresh_token(data={"sub": user.username})
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=dict)
async def refresh_token(refresh_token: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    access_token = await auth_service.refresh_access_token(refresh_token)
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncIOMotorDatabase = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = auth_service.verify_token(token, credentials_exception)
    user = await user_repository.get_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user
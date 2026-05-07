from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None
from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4

class User(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))
    username: str = Field(min_length=1)
    hashed_password: str
    is_active: bool = True
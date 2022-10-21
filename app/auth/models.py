from datetime import datetime
from typing import Optional
import uuid
from pydantic import Field, BaseModel, EmailStr


class UserModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    full_name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "name": "vuluu2k",
                "email": "vuluu040320@gmail.com",
                "password": "12345678",
            },
            "user_demo": {
                "name": "vuluu2k",
                "email": "vuluu040320@gmail.com",
                "password": "12345678",
            }
        }


class UserLoginModel(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "email": "vuluu040320@gmail.com",
                "password": "12345678",
            },
            "user_demo": {
                "email": "vuluu040320@gmail.com",
                "password": "12345678",
            }
        }

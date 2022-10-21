from datetime import datetime
from typing import Optional
import uuid
from pydantic import Field, BaseModel
from app.auth.models import UserModel


class TaskModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    image_url: str = Field(default=None, alias="image_url")
    content: str = Field(...)
    completed: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Learn FARM Intro",
                "completed": False,
                "content": "CRUD FastAPI , ReactJs, MongoDB",
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQb-oKFFYpkJj1_6vGlDVlKFjuRIfcDIa4qhbFlDHA3TA&s",
            }
        }


class UpdateTaskModel(BaseModel):
    name: Optional[str]
    completed: Optional[bool]
    image_url: Optional[str]
    content: Optional[str]
    updated_at: datetime = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "name": "Learn FARM",
                "completed": True,
                "content": "CRUD FastAPI , ReactJs, MongoDB, Update level Now",
            }
        }

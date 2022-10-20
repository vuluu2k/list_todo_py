from datetime import datetime
from typing import Optional
import uuid
from pydantic import Field, BaseModel


class TaskModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    completed: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Learn FARM Intro",
                "completed": False,
            }
        }


class UpdateTaskModel(BaseModel):
    name: Optional[str]
    completed: Optional[bool]
    updated_at: datetime = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "name": "Learn FARM Intro Edit",
                "completed": True,
            }
        }

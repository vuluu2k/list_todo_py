from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import dns

from .config import settings
from .todo.routes import router as todo_router

app = FastAPI()

app.include_router(todo_router, tags=["tasks"], prefix="/task")


@app.on_event("startup")
async def start_up_mongodb():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown_mongodb():
    app.mongodb_client.close()

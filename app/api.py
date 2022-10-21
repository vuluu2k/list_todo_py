from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .todo.routes import router as todo_router
from .auth.routes import router as user_router


app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router, tags=["tasks"], prefix="/task")
app.include_router(user_router,tags=["users"],prefix="/auth")


@app.on_event("startup")
async def start_up_mongodb():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown_mongodb():
    app.mongodb_client.close()

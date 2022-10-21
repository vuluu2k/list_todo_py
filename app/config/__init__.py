from pydantic import BaseSettings
from decouple import config

DB_USERNAME = config("DB_USERNAME")
DB_PASSWORD = config("DB_PASSWORD")


class DatabaseSettings(BaseSettings):
    DB_URL: str = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@todos.rg4euf1.mongodb.net/?retryWrites=true"
    DB_NAME: str = "Todos"


class Settings(DatabaseSettings):
    pass


settings = Settings()

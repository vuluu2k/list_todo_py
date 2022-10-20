from pydantic import BaseSettings
import dns


class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb+srv://vuluu2k:1234@todos.rg4euf1.mongodb.net/?retryWrites=true"
    DB_NAME: str = "Todos"


class Settings(DatabaseSettings):
    pass


settings = Settings()

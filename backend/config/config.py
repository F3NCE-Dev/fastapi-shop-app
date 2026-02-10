from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///backend/app.db"
    FRONTEND_ORIGINS: list[str] = ["http://localhost:5500", "http://127.0.0.1:5500"]
    DEBUG_MODE: bool = True
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "Secret_Key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DATABASE_URL: str = "sqlite+aiosqlite:///backend/app.db"
    PROFILE_PICTURES_PATH: str = "backend/static/profile_pictures"
    DEFAULT_PROFILE_PICTURE_URL: str = "backend/static/default_profile_pic/default.png"
    FRONTEND_ORIGINS: list[str] = ["http://localhost:5500", "http://127.0.0.1:5500"]
    DEBUG_MODE: bool = True
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "Secret_Key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    STATIC_FOLDER: str = "static"
    PROFILE_PICTURES_PATH: str = "static/profile_pictures"
    DEFAULT_PROFILE_PICTURE_URL: str = "static/default_profile_pic/default.png"
    PRODUCT_IMAGES_PATH: str = "static/product_images"

    FRONTEND_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    REDIRECT_URI: str = "http://localhost:5173/"

    OAUTH_GOOGLE_CLIENT_ID: str = "Google ID"
    OAUTH_GOOGLE_CLIENT_SECRET: str = "Google Secret"

    DEBUG_MODE: bool = True
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

from fastapi import Depends, HTTPException, status, UploadFile

from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserORM

from app.redis_client import get_redis_client
from redis.asyncio import Redis

from app.config.config import settings
from app.auth.security import oauth2_scheme
import jwt

from typing import Annotated
from pathlib import Path
import aiofiles

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
) -> UserORM:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = await db.get(UserORM, int(user_id))
    if user is None:
        raise credentials_exception

    return user

async def upload_image(file: UploadFile, dir: str, folder_name: str) -> str:
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(400, "Invalid image type")
    img_name = Path(file.filename).name
    dir = Path(dir) / folder_name
    dir.mkdir(parents=True, exist_ok=True)
    file_path = dir / img_name
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await file.read())
    return file_path.as_posix()

async def update_image(old_image_path: str, new_image: UploadFile, dir: str, folder_name: str, default_image: str | None = None) -> str:
    old_file = Path(old_image_path)
    if old_file.exists() and old_file != Path(default_image) if default_image else True:
        old_file.unlink()

    try:
        return await upload_image(file=new_image, dir=dir, folder_name=folder_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update image") from e

def get_image_url(image_path: str) -> str:
    if image_path and image_path.startswith("backend/"):
        return image_path.replace("backend/", "", 1)
    return image_path

DBSession = Annotated[AsyncSession, Depends(get_db)]
REDIS = Annotated[Redis, Depends(get_redis_client)]
CurrentUser = Annotated[UserORM, Depends(get_current_user)]

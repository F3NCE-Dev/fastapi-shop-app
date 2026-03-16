from fastapi import HTTPException, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dependencies import get_image_url
from models.user import UserORM
from auth.security import create_access_token, hash_password

from config.config import settings

from pathlib import Path
import aiofiles

class ProfileEdit:
    @classmethod
    async def EditUsername(cls, new_username: str, profile_id: int, db: AsyncSession) -> str:
        result_existing = await db.execute(select(UserORM).where(UserORM.username == new_username))

        if result_existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already exists")

        result = await db.execute(select(UserORM).where(UserORM.id == profile_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.username = new_username
        await db.commit()

        return create_access_token({"sub": new_username})
    
    @classmethod
    async def EditPassword(cls, profile_id: int, password: str, db: AsyncSession) -> str:
        result = await db.execute(select(UserORM).where(UserORM.id == profile_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.hashed_password = hash_password(password=password)
        await db.commit()

        return create_access_token({"sub": user.username})
    
    @classmethod
    async def EditProfilePicture(cls, image: UploadFile, profile_id: int, db: AsyncSession) -> None:
        user = await db.get(UserORM, profile_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if image.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(400, "Invalid image type")
        
        filename = Path(image.filename).name

        user_dir = Path(settings.PROFILE_PICTURES_PATH) / str(profile_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        file_path = user_dir / filename
        
        old_file = Path(user.profile_picture_url)

        if old_file.exists() and old_file != Path(settings.DEFAULT_PROFILE_PICTURE_URL):
            old_file.unlink()

        async with aiofiles.open(file_path, "wb") as file:
            await file.write(await image.read())
        
        user.profile_picture_url = file_path.as_posix()

        await db.commit()

    @classmethod
    async def GetProfilePicture(cls, profile_id: int, db: AsyncSession) -> str:
        user = await db.get(UserORM, profile_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return get_image_url(user.profile_picture_url)

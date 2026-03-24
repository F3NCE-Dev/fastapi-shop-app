from fastapi import HTTPException, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserORM

from app.schemas.user import UserUpdate
from app.auth.security import create_access_token, hash_password
from app.dependencies import update_image

from app.config.config import settings

class ProfileEdit:
    @classmethod
    async def EditProfile(cls, profile_id: int, data: UserUpdate, db: AsyncSession) -> str:
        user = await db.get(UserORM, profile_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
            if field == "password":
                setattr(user, "hashed_password", hash_password(value))
            else:
                setattr(user, field, value)

        await db.commit()
        return create_access_token({"sub": user.username})

    @classmethod
    async def UpdateProfileImage(cls, profile_id: int, image: UploadFile, db: AsyncSession) -> None:
        user = await db.get(UserORM, profile_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        try:
            user.profile_picture_url = await update_image(old_image_path=user.profile_picture_url,
                                                          new_image=image,
                                                          dir=settings.PROFILE_PICTURES_PATH,
                                                          folder_name=str(profile_id),
                                                          default_image=settings.DEFAULT_PROFILE_PICTURE_URL)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Failed to update profile picture") from e
        await db.commit()

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserORM
from app.schemas.user import User
from app.dependencies import get_image_url

class UserRepository:
    @classmethod
    async def get_user(cls, user_id: int, db: AsyncSession) -> User:
        user = await db.get(UserORM, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.profile_picture_url = get_image_url(user.profile_picture_url)
        return User.model_validate(user)

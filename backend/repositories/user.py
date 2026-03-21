from schemas.user import User
from models.user import UserORM
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    @classmethod
    async def get_user(cls, user_id: int, db: AsyncSession) -> User:
        user = await db.get(UserORM, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(user)

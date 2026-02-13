from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.user import UserORM
from auth.security import create_access_token

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

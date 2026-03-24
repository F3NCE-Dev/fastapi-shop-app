from fastapi import HTTPException, status

from app.models.user import UserORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserAuth
from app.auth.security import hash_password, verify_password, create_access_token

class AuthRepository:
    @classmethod
    async def register(cls, data: UserAuth, db: AsyncSession) -> int:
        result = await db.execute(select(UserORM).where(UserORM.username == data.username))

        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="User already exists")
        
        new_user = UserORM(
            username=data.username,
            hashed_password=hash_password(data.password),
        )

        db.add(new_user)
        await db.commit()
        return new_user.id
    
    @classmethod
    async def login_user(cls, credentials: UserAuth, db: AsyncSession) -> str:
        result = await db.execute(select(UserORM).where(UserORM.username == credentials.username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        return create_access_token({"sub": user.username})

from datetime import datetime, timezone
from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserORM
from app.models.refresh_token import RefreshTokenORM
from app.schemas.user import User
from app.dependencies import get_image_url
from app.repositories.refresh_token import RefreshTokenRepository
from app.auth.security import create_access_token, create_refresh_token, get_refresh_token_expiry

class UserRepository:
    @classmethod
    async def get_user(cls, user_id: int, db: AsyncSession, redis: Redis) -> User:
        cached = await redis.get(f"user:{user_id}")
        if cached:
            user = User.model_validate_json(cached)
            user.profile_picture_url = get_image_url(user.profile_picture_url)
            return user
        
        user = await db.get(UserORM, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = User.model_validate(user)
        await redis.set(f"user:{user_id}", user.model_dump_json(), ex=3600)
        
        user.profile_picture_url = get_image_url(user.profile_picture_url)
        return user

    @classmethod
    async def refresh_token(cls, refresh_token_value: str, db: AsyncSession) -> tuple[str, str]:
        token = await RefreshTokenRepository.get_by_token(refresh_token_value, db)

        if not token or token.revoked:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        
        if token.expires_at.tzinfo is None:
            token.expires_at = token.expires_at.replace(tzinfo=timezone.utc)

        if token.expires_at < datetime.now(timezone.utc):
            await RefreshTokenRepository.revoke_token(token)
            await db.commit()
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        await RefreshTokenRepository.revoke_token(token)

        user = await db.get(UserORM, token.user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        new_refresh_token_value = create_refresh_token()
        new_refresh_token = RefreshTokenORM(
            user_id=token.user_id,
            token=new_refresh_token_value,
            expires_at=get_refresh_token_expiry(),
        )
        await RefreshTokenRepository.create_refresh_token(new_refresh_token, db)

        access_token = create_access_token({"sub": str(user.id), "role": user.role.value})

        await db.commit()

        return access_token, new_refresh_token_value
    
    @classmethod
    async def logout(cls, refresh_token_value: str, db: AsyncSession) -> None:
        token = await RefreshTokenRepository.get_by_token(refresh_token_value, db)

        if token and not token.revoked:
            await RefreshTokenRepository.revoke_token(token)
            await db.commit()

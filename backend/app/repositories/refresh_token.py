from app.models.refresh_token import RefreshTokenORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class RefreshTokenRepository:
    @classmethod
    async def create_refresh_token(cls, refresh_token: RefreshTokenORM, db: AsyncSession) -> RefreshTokenORM:
        db.add(refresh_token)
        await db.flush()
        return refresh_token
    
    @classmethod
    async def get_by_token(cls, token: str, db: AsyncSession) -> RefreshTokenORM | None:
        result = await db.execute(select(RefreshTokenORM).where(RefreshTokenORM.token == token))
        return result.scalar_one_or_none()
    
    @classmethod
    async def revoke_token(cls, token: RefreshTokenORM) -> None:
        token.revoked = True

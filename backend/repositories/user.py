from models.product import ProductORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    @classmethod
    async def get_all_products(cls, db: AsyncSession):
        result = await db.execute(select(ProductORM))
        return result.scalars().all()

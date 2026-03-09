from fastapi import HTTPException
from models.product import ProductORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    @classmethod
    async def get_products(cls,category: str, search: str, db: AsyncSession):
        query = select(ProductORM)
        
        if category:
            query = query.where(ProductORM.category == category)
        if search:
            query = query.where(ProductORM.name.ilike(f"%{search}%"))

        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_product(cls, product_id: int, db: AsyncSession):
        result = await db.execute(select(ProductORM).where(ProductORM.id == product_id))
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

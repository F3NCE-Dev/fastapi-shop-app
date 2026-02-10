from database import ProductORM
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.product import ProductBase

class AdminCommands:
    @classmethod
    async def add_new_product(cls, data: ProductBase, db: AsyncSession) -> int:
        new_product = ProductORM(**data.model_dump())
        db.add(new_product)
        await db.commit()
        return new_product.id

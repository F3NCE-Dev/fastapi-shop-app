from fastapi import HTTPException

from database import ProductORM
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.product import ProductBase

class AdminCommands:
    @classmethod
    async def add_product(cls, data: ProductBase, db: AsyncSession) -> int:
        new_product = ProductORM(**data.model_dump())
        db.add(new_product)
        await db.commit()
        return new_product.id
    
    @classmethod
    async def remove_product(cls, product_id: int, db: AsyncSession) -> int:
        product = await db.get(ProductORM, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        await db.delete(product)
        await db.commit()
        return product.id
from fastapi import HTTPException

from models.product import ProductORM
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.product import ProductBase
from permissions.permissions import admin_required
from permissions.roles import Role

class AdminCommands:
    @classmethod
    async def add_product(cls, data: ProductBase, role: Role, db: AsyncSession) -> int:
        admin_required(role)
        new_product = ProductORM(**data.model_dump())
        db.add(new_product)
        await db.commit()
        return new_product.id
    
    @classmethod
    async def remove_product(cls, product_id: int, role: Role, db: AsyncSession) -> int:
        admin_required(role)
        product = await db.get(ProductORM, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        await db.delete(product)
        await db.commit()
        return product.id

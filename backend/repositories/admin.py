from fastapi import HTTPException

from models.product import ProductORM
from models.order import OrderORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from schemas.product import ProductBase
from schemas.order import Order
from enums.order_status import OrderStatus

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

    @classmethod
    async def update_product(cls, product_id: int, data: ProductBase, db: AsyncSession) -> int:
        product = await db.get(ProductORM, product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        for key, value in data.model_dump().items():
            setattr(product, key, value)

        await db.commit()
        return product.id
    
    @classmethod
    async def update_order_status(cls, order_id: int, status: OrderStatus, db: AsyncSession) -> int:
        result = await db.execute(select(OrderORM).where(OrderORM.id == order_id))
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order.status = status
        await db.commit()
        return order.id
        
    @classmethod
    async def get_all_orders(cls, db: AsyncSession) -> list[Order]:
        result = await db.execute(select(OrderORM).options(selectinload(OrderORM.items)))
        orders = result.scalars().all()
        
        if not orders:
            raise HTTPException(status_code=404, detail="Orders not found")
            
        return orders

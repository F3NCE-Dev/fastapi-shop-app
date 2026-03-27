from fastapi import HTTPException

from app.models.product import ProductORM
from app.models.order import OrderORM, OrderItemORM
from app.models.cart import CartORM
from app.schemas.order import Order
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class OrderRepository:
    @classmethod
    async def add_order(cls, user_id: int, db: AsyncSession) -> int:
        cart_result = await db.execute(select(CartORM).where(CartORM.user_id == user_id).options(selectinload(CartORM.items)))
        cart = cart_result.scalar_one_or_none()

        if not cart or not cart.items:
            raise HTTPException(400, "Cart is empty")

        order = OrderORM(user_id=user_id)
        db.add(order)
        await db.flush()

        total = 0

        for item in cart.items:
            product = await db.get(ProductORM, item.product_id)
            if not product:
                raise HTTPException(404, f"Product {item.product_id} not found")

            db.add(OrderItemORM(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price_at_purchase=product.price
            ))
            total += product.price * item.quantity

        order.total_price = total

        cart.items.clear()

        await db.commit()
        await db.refresh(order)

        return order.id
    
    @classmethod
    async def delete_order(cls, user_id: int, order_id: int, db: AsyncSession) -> None:
        result = await db.execute(select(OrderORM).where(OrderORM.user_id == user_id, OrderORM.id == order_id))
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(404, "Order not found")
        
        await db.delete(order)
        await db.commit()

    @classmethod
    async def get_orders(cls, user_id: int, db: AsyncSession) -> list[Order]:
        result = await db.execute(select(OrderORM).where(OrderORM.user_id == user_id).options(selectinload(OrderORM.items)))
        order = result.scalars().all()

        if not order:
            raise HTTPException(404, "Order not found")

        return order

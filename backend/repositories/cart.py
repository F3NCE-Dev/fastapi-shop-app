from fastapi import HTTPException

from models.cart import CartORM, CartItemORM
from models.product import ProductORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class CartRepository:
    @classmethod
    async def add_to_cart(cls, user_id: int, product_id: int, quantity: int, db: AsyncSession) -> int:
        cart = await db.execute(select(CartORM).where(CartORM.user_id == user_id))
        cart = cart.scalar_one_or_none()

        if not cart:
            cart = CartORM(user_id=user_id)
            db.add(cart)
            await db.flush()
        
        product = await db.get(ProductORM, product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        result = await db.execute(select(CartItemORM).where(CartItemORM.cart_id == cart.id, CartItemORM.product_id == product_id))
        item = result.scalar_one_or_none()

        if item:
            item.quantity += quantity
        else:
            db.add(CartItemORM(cart_id=cart.id, product_id=product_id, quantity=quantity))
        
        await db.commit()
        await db.refresh(cart)

        return cart.id

from fastapi import HTTPException

from app.models.cart import CartORM, CartItemORM
from app.models.product import ProductORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.schemas.cart import Cart

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
    
    @classmethod
    async def remove_from_cart(cls, user_id: int, product_id: int, quantity: int | None, db: AsyncSession) -> int:
        result = await db.execute(select(CartORM).where(CartORM.user_id == user_id).options(selectinload(CartORM.items)))
        cart = result.scalar_one_or_none()

        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        item_to_remove = None

        for item in cart.items:
            if item.product_id == product_id:
                item_to_remove = item
                break

        if not item_to_remove:
            raise HTTPException(status_code=404, detail="Product not in cart")
        
        if quantity and item_to_remove.quantity > quantity:
            item_to_remove.quantity -= quantity
        else:
            await db.delete(item_to_remove)

        await db.commit()
        return cart.id
    
    @classmethod
    async def clear_cart(cls, user_id: int, db: AsyncSession) -> int:
        result = await db.execute(select(CartORM).where(CartORM.user_id == user_id).options(selectinload(CartORM.items)))
        cart = result.scalar_one_or_none()

        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        cart.items.clear()
        await db.commit()
        return cart.id

    @classmethod
    async def get_cart_items(cls, user_id: int, db: AsyncSession) -> Cart:
        result = await db.execute(select(CartORM).where(CartORM.user_id == user_id).options(selectinload(CartORM.items)))
        cart = result.scalar_one_or_none()

        if not cart:
            return {"items": [], "total_price": 0}
        
        items = []
        total_price = 0

        for item in cart.items:
            product =  await db.get(ProductORM, item.product_id)
            if product:
                item_data = {
                    "product_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": item.quantity,
                    "total_price": product.price * item.quantity
                }
                items.append(item_data)
                total_price += item_data["total_price"]

        return {"items": items, "total_price": total_price}

from fastapi import HTTPException, UploadFile

from models.product import ProductORM
from models.order import OrderORM
from models.user import UserORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from schemas.product import ProductBase
from schemas.order import Order
from schemas.user import User
from enums.order_status import OrderStatus
from pathlib import Path
import aiofiles
from config.config import settings

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
    async def update_product_image(cls, product_id: int, image: UploadFile, db: AsyncSession) -> int:
        if image.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(400, "Invalid image type")
        
        product = await db.get(ProductORM, product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        old_image_path = product.image_url
        if old_image_path:
            old_file = Path(old_image_path)
            if old_file.exists() and old_file.is_file():
                try:
                    old_file.unlink()
                except Exception as e:
                    print(f"Failed to delete old image: {e}")
        
        img_name = Path(image.filename).name

        product_dir = Path(settings.PRODUCT_IMAGES_PATH)
        product_dir.mkdir(parents=True, exist_ok=True)

        file_path = product_dir / img_name

        async with aiofiles.open(file_path, "wb") as file:
            await file.write(await image.read())

        product.image_url = file_path.as_posix()
        await db.commit()
        return product.id
    
    @classmethod
    async def update_order_status(cls, order_id: int, status: OrderStatus, db: AsyncSession) -> None:
        result = await db.execute(select(OrderORM).where(OrderORM.id == order_id))
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order.status = status
        await db.commit()
    
    @classmethod
    async def get_all_orders(cls, db: AsyncSession) -> list[Order]:
        result = await db.execute(select(OrderORM).options(selectinload(OrderORM.items)))
        orders = result.scalars().all()
        
        if not orders:
            raise HTTPException(status_code=404, detail="Orders not found")
            
        return orders
    
    @classmethod
    async def get_order(cls, order_id: int, db: AsyncSession) -> Order:
        result = await db.execute(select(OrderORM).where(OrderORM.id == order_id).options(selectinload(OrderORM.items)))
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return order
    
    @classmethod
    async def get_all_users(cls, limit: int, offset: int, db: AsyncSession) -> list[User]:
        query = select(UserORM)

        query = query.limit(limit).offset(offset)

        result = await db.execute(query)
        users = result.scalars().all()
        user_schemas = [User.model_validate(user) for user in users]
        return user_schemas
    
    @classmethod
    async def get_user(cls, user_id: int, db: AsyncSession) -> User:
        user = await db.get(UserORM, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(user)

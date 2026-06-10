from fastapi import HTTPException, UploadFile

from app.models.product import ProductORM
from app.models.order import OrderORM
from app.models.user import UserORM
from app.models.category import CategoryORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from redis.asyncio import Redis

from app.schemas.product import ProductBase, ProductUpdate
from app.schemas.order import Order
from app.schemas.user import UserID
from app.schemas.category import CategoryBase
from app.enums.order_status import OrderStatus
from app.enums.roles import Role
from app.config.config import settings
from app.dependencies import upload_image, update_image
from app.auth.security import create_access_token

async def _invalidate_product_cache(product_id: int, redis: Redis) -> None:
    await redis.delete(f"product:{product_id}")
    async for key in redis.scan_iter("products:*"):
        await redis.delete(key)

async def _invalidate_category_cache(redis: Redis) -> None:
    await redis.delete("categories")

class AdminCommands:
    @classmethod
    async def add_product(cls, data: ProductBase, image: UploadFile, db: AsyncSession, redis: Redis) -> int:
        new_product = ProductORM(**data.model_dump(), image_url="")

        try:
            db.add(new_product)
            await db.flush()
            new_product.image_url = await upload_image(file=image, dir=settings.PRODUCT_IMAGES_PATH, folder_name=str(new_product.id))
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Failed to add product") from e
        await db.commit()
        await _invalidate_product_cache(new_product.id, redis)
        return new_product.id

    @classmethod
    async def remove_product(cls, product_id: int, db: AsyncSession, redis: Redis) -> int:
        product = await db.get(ProductORM, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        await db.delete(product)
        await db.commit()
        await _invalidate_product_cache(product.id, redis)
        return product.id

    @classmethod
    async def update_product(cls, product_id: int, data: ProductUpdate, image: UploadFile | None, db: AsyncSession, redis: Redis) -> int:
        product = await db.get(ProductORM, product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        for key, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
                setattr(product, key, value)

        if image:
            try:
                product.image_url = await update_image(old_image_path=product.image_url,
                                                        new_image=image,
                                                        dir=settings.PRODUCT_IMAGES_PATH,
                                                        folder_name=str(product.id))
            except Exception as e:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Failed to update product image") from e

        await db.commit()
        await _invalidate_product_cache(product.id, redis)
        return product.id
    
    @classmethod
    async def add_category(cls, data: CategoryBase, db: AsyncSession, redis: Redis) -> int:
        new_category = CategoryORM(**data.model_dump())
        db.add(new_category)
        await db.commit()
        await _invalidate_category_cache(redis)
        return new_category.id

    @classmethod
    async def delete_category(cls, category_id: int, db: AsyncSession, redis: Redis) -> int:
        category = await db.get(CategoryORM, category_id)

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        await db.delete(category)
        await db.commit()
        await _invalidate_category_cache(redis)
        return category.id
    
    @classmethod
    async def update_order_status(cls, order_id: int, status: OrderStatus, db: AsyncSession) -> None:
        order = await db.get(OrderORM, order_id)

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
    async def update_user_role(cls, user_id: int, role: Role, db: AsyncSession) -> str:
        user = await db.get(UserORM, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.role = role
        await db.commit()
        return create_access_token({"sub": str(user.id), "role": user.role.value})
    
    @classmethod
    async def get_all_users(cls, limit: int, offset: int, db: AsyncSession) -> list[UserID]:
        query = select(UserORM)

        query = query.limit(limit).offset(offset)

        result = await db.execute(query)
        users = result.scalars().all()
        user_schemas = [UserID.model_validate(user) for user in users]
        return user_schemas
    
    @classmethod
    async def get_user(cls, user_id: int, db: AsyncSession) -> UserID:
        user = await db.get(UserORM, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserID.model_validate(user)

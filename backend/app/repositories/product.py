from fastapi import HTTPException
from app.dependencies import get_image_url
from app.schemas.product import ProductResponse
from app.models.product import ProductORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from typing import Optional
import json

class ProductRepository:
    @classmethod
    async def get_products(cls, category_id: int,
                           search: str,
                           limit: int,
                           offset: int,
                           sort: Optional[str],
                           db: AsyncSession,
                           redis: Redis) -> list[ProductResponse]:
        cache_key = f"products:{category_id}:{search}:{limit}:{offset}:{sort}"

        cached = await redis.get(cache_key)
        if cached:
            return [ProductResponse(**p) for p in json.loads(cached)]

        query = select(ProductORM)
        
        if category_id:
            query = query.where(ProductORM.category_id == category_id)
        if search:
            query = query.where(ProductORM.name.ilike(f"%{search}%"))

        if sort:
            descending = sort.startswith("-")
            field = sort.lstrip("-")
            
            if hasattr(ProductORM, field):
                column = getattr(ProductORM, field)
                query = query.order_by(column.desc() if descending else column.asc())

        query = query.limit(limit).offset(offset)

        result = await db.execute(query)
        products = result.scalars().all()

        for product in products:
            product.image_url = get_image_url(product.image_url)
        
        await redis.set("products", json.dumps([ProductResponse.model_validate(p).model_dump() for p in products]), ex=600)
        return products

    @classmethod
    async def get_product(cls, product_id: int, db: AsyncSession, redis: Redis) -> ProductResponse:
        cache_key = f"product:{product_id}"
        cached = await redis.get(cache_key)
        if cached:
            return ProductResponse(**json.loads(cached))
        
        result = await db.execute(select(ProductORM).where(ProductORM.id == product_id))
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product.image_url = get_image_url(product.image_url)

        await redis.set(cache_key, ProductResponse.model_validate(product).model_dump_json(), ex=600)

        return product
